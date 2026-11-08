import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from human_review.workflow import evaluate
from human_review.researchos import assess
from human_review.bundle import write, verify, contents
from human_review._tect.core import replay
from human_review._tect.io import load

ROOT = Path(__file__).resolve().parents[1]


def sample():
    return json.loads((ROOT/'examples/review.json').read_text())


class ReviewTests(unittest.TestCase):
    def test_complete_declared_review(self):
        report = evaluate(sample())
        self.assertEqual(report['cases']['claim-a']['disposition'], 'accepted_declared')
        self.assertEqual(report['total_recorded_review_seconds'], 180)
        self.assertFalse(report['reviewer_independence_established'])

    def test_votes_do_not_replace_adjudication(self):
        data = sample(); data['adjudications'] = []
        case = evaluate(data)['cases']['claim-a']
        self.assertEqual(case['disposition'], 'review_required')
        self.assertIn('ADJUDICATION_MISSING', case['blockers'])
        data['submissions'][1]['verdict'] = 'reject'
        self.assertTrue(evaluate(data)['cases']['claim-a']['verdict_disagreement'])

    def test_conflict_and_capacity(self):
        data = sample(); data['reviewers'][0]['conflicts'] = ['claim-a']
        with self.assertRaises(ValueError): evaluate(data)
        data = sample(); data['reviewers'][2]['conflicts'] = ['claim-a']
        with self.assertRaises(ValueError): evaluate(data)
        data = sample(); data['cases'].append({**data['cases'][0], 'id':'claim-b'})
        data['reviewers'][0]['max_assignments'] = 1
        data['assignments'].append({'case_id':'claim-b', 'reviewer_id':'reviewer-1'})
        with self.assertRaises(ValueError): evaluate(data)

    def test_self_adjudication_and_roles(self):
        data = sample(); data['reviewers'][0]['roles'].append('adjudicator')
        data['adjudications'][0]['adjudicator_id'] = 'reviewer-1'
        with self.assertRaises(ValueError): evaluate(data)
        data = sample(); data['reviewers'][2]['roles'] = ['reviewer']
        with self.assertRaises(ValueError): evaluate(data)

    def test_stale_review_and_artifact(self):
        for field, value in [('case_version',2), ('artifact_sha256','b'*64)]:
            for key in ('submissions', 'adjudications'):
                data = sample(); data[key][0][field] = value
                with self.subTest(key=key, field=field), self.assertRaises(ValueError): evaluate(data)

    def test_finding_resolution_is_explicit(self):
        data = sample()
        data['submissions'][0]['findings'] = [{'id':'gap','severity':'blocking','statement':'Missing assumption'}]
        with self.assertRaises(ValueError): evaluate(data)
        resolution = {'submission_id':'review-1','finding_id':'gap','disposition':'sustained','reason':'Gap remains'}
        data['adjudications'][0]['resolutions'] = [resolution]
        with self.assertRaises(ValueError): evaluate(data)
        data['adjudications'][0]['decision'] = 'revise'
        self.assertEqual(evaluate(data)['cases']['claim-a']['disposition'], 'review_required')
        data['adjudications'][0]['decision'] = 'accept'
        resolution.update(disposition='dismissed', reason='Explicit synthetic override explanation')
        self.assertEqual(evaluate(data)['cases']['claim-a']['disposition'], 'accepted_declared')

    def test_missing_reviews_and_adjudication_coverage(self):
        data = sample(); data['cases'][0]['minimum_reviews'] = 3
        self.assertIn('MINIMUM_REVIEWS_MISSING', evaluate(data)['cases']['claim-a']['blockers'])
        data = sample(); data['adjudications'][0]['submission_ids'] = ['review-1']
        with self.assertRaises(ValueError): evaluate(data)

    def test_dependency_gaps_and_cycles(self):
        data = sample()
        data['cases'].append({**data['cases'][0], 'id':'claim-b', 'dependencies':['claim-a']})
        report = evaluate(data)
        self.assertEqual(report['case_order'], ['claim-a','claim-b'])
        scenario, _, controller_report = assess(data, report)
        c = replay(scenario)
        c.apply({'op':'revise','actor':'author','data':{'claim':'claim-a','statement':'Changed claim',
                 'provenance':['changed-artifact'], 'confidence':.5,'assurance_scope':'Declared review only'}})
        self.assertEqual(c.snapshot()['claims']['claim-a']['state'], 'UNVERIFIED')
        self.assertEqual(c.snapshot()['claims']['claim-b']['state'], 'UNVERIFIED')
        data['cases'][0]['dependencies'] = ['claim-b']
        with self.assertRaises(ValueError): evaluate(data)
        data = sample(); data['cases'][0]['dependencies'] = ['unknown']
        with self.assertRaises(ValueError): evaluate(data)

    def test_researchos_missing_reproduction_and_pending_review(self):
        data = sample(); scenario, ledger, report = assess(data, evaluate(data))
        self.assertEqual(ledger[-1]['outcome'], 'UNCERTAIN')
        self.assertIn('SEPARATE_REPRODUCTION_MISSING', ledger[-1]['reasons'])
        self.assertFalse(report['execution_authorized'])
        data['adjudications'] = []
        _, _, report = assess(data, evaluate(data))
        self.assertEqual(report['state']['claims']['claim-a']['state'], 'UNVERIFIED')

    def test_future_times_duplicates_and_invalid_inputs(self):
        for mutation in ('future','adjudication_time','duplicate','time','unknown','assignment'):
            data = sample()
            if mutation == 'future': data['submissions'][0]['reviewed_at'] = '2027-01-01T00:00:00Z'
            if mutation == 'adjudication_time': data['adjudications'][0]['adjudicated_at'] = '2026-01-01T00:00:00Z'
            if mutation == 'duplicate': data['submissions'].append(copy.deepcopy(data['submissions'][0]))
            if mutation == 'time': data['submissions'][0]['seconds'] = float('nan')
            if mutation == 'unknown': data['cases'][0]['unknown'] = True
            if mutation == 'assignment': data['assignments'].pop()
            with self.subTest(mutation=mutation), self.assertRaises(ValueError): evaluate(data)

    def test_core_integrity_role_and_expiry_probes(self):
        data = sample(); scenario, _, _ = assess(data, evaluate(data))
        for change in ('hash','actor','expiry'):
            altered = copy.deepcopy(scenario)
            operation = next(op for op in altered['operations'] if op['op']=='evidence')
            if change == 'hash': operation['data']['sha256'] = '0'*64
            if change == 'actor': operation['actor'] = 'author'
            if change == 'expiry': operation['data']['expires_at'] = data['as_of']
            c = replay(altered)
            self.assertTrue(any(e['outcome']=='FAIL' for e in c.ledger))
            self.assertNotEqual(c.snapshot()['claims']['claim-a']['state'], 'ASSURED')

    def test_bundle_tamper_escaping_and_strict_json(self):
        data = sample(); data['cases'][0]['statement'] = '<script>bad()</script>'
        # Input is captured in the scenario; output still cannot inject HTML.
        self.assertNotIn('<script>', contents(data)['review.html'])
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)/'run'
            write(data, output); verify(output)
            with self.assertRaises(FileExistsError): write(data, output)
            (output/'reviews.json').write_text('{}')
            with self.assertRaises(ValueError): verify(output)
            bad = Path(tmp)/'input.json'; bad.write_text('{"a":1,"a":2}')
            with self.assertRaises(ValueError): load(bad)

    def test_canonical_core_conformance(self):
        lock = json.loads((ROOT/'researchos-lock.json').read_text())
        for name, expected in lock['release']['modules'].items():
            self.assertEqual(hashlib.sha256((ROOT/'human_review/_tect'/name).read_bytes()).hexdigest(), expected)


if __name__ == '__main__':
    unittest.main()
