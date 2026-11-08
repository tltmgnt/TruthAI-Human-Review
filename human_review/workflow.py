"""Explicit assignments, review declarations and adjudication; no majority acceptance."""
import math
from ._tect.core import fields, text, date, digest


def sha(value):
    if type(value) is not str or len(value) != 64 or any(c not in '0123456789abcdef' for c in value):
        raise ValueError('SHA-256 artifact reference required')


def indexed(items, maximum):
    if type(items) is not list or not 1 <= len(items) <= maximum:
        raise ValueError('Nonempty bounded records required')
    result = {}
    for item in items:
        if type(item) is not dict:
            raise ValueError('Object records required')
        identifier = text(item.get('id'))
        if identifier in result:
            raise ValueError('Duplicate record ID')
        result[identifier] = item
    return result


def labels(items):
    if type(items) is not list:
        raise ValueError('List of identifiers required')
    for value in items:
        text(value)
    if len(items) != len(set(items)):
        raise ValueError('Duplicate identifier')


def evaluate(data):
    fields(data, ('schema_version', 'as_of', 'expires_at', 'cases', 'reviewers',
                  'assignments', 'submissions', 'adjudications'))
    if type(data['schema_version']) is not int or data['schema_version'] != 1:
        raise ValueError('Unsupported schema version')
    if date(data['expires_at']) <= date(data['as_of']):
        raise ValueError('Expiry must follow assessment time')
    cases, reviewers = indexed(data['cases'], 32), indexed(data['reviewers'], 128)
    for case in cases.values():
        fields(case, ('id', 'version', 'statement', 'artifact_sha256', 'minimum_reviews', 'dependencies'))
        text(case['statement']); sha(case['artifact_sha256']); labels(case['dependencies'])
        if type(case['version']) is not int or case['version'] < 1:
            raise ValueError('Positive case version required')
        if type(case['minimum_reviews']) is not int or not 1 <= case['minimum_reviews'] <= 10:
            raise ValueError('Between 1 and 10 reviews required')
        if any(d not in cases or d == case['id'] for d in case['dependencies']):
            raise ValueError('Unknown or self dependency')
    order, visiting, visited = [], set(), set()
    def visit(cid):
        if cid in visiting: raise ValueError('Cyclic case dependencies')
        if cid in visited: return
        visiting.add(cid)
        for dep in cases[cid]['dependencies']: visit(dep)
        visiting.remove(cid); visited.add(cid); order.append(cid)
    for cid in cases: visit(cid)
    for reviewer in reviewers.values():
        fields(reviewer, ('id', 'roles', 'conflicts', 'max_assignments'))
        labels(reviewer['roles']); labels(reviewer['conflicts'])
        if not reviewer['roles'] or any(r not in ('reviewer', 'adjudicator') for r in reviewer['roles']):
            raise ValueError('Unknown or empty roles')
        if any(c not in cases for c in reviewer['conflicts']):
            raise ValueError('Unknown conflict case')
        if type(reviewer['max_assignments']) is not int or not 1 <= reviewer['max_assignments'] <= 32:
            raise ValueError('Bounded reviewer capacity required')
    assigned, loads = set(), dict.fromkeys(reviewers, 0)
    for name, maximum in (('assignments', 320), ('submissions', 320), ('adjudications', 32)):
        if type(data[name]) is not list or len(data[name]) > maximum:
            raise ValueError('Bounded workflow lists required')
    for item in data['assignments']:
        fields(item, ('case_id', 'reviewer_id'))
        cid, rid = item['case_id'], item['reviewer_id']
        if cid not in cases or rid not in reviewers or (cid, rid) in assigned:
            raise ValueError('Invalid or duplicate assignment')
        person = reviewers[rid]
        if 'reviewer' not in person['roles'] or cid in person['conflicts']:
            raise ValueError('Assignment role or conflict violation')
        assigned.add((cid, rid)); loads[rid] += 1
        if loads[rid] > person['max_assignments']:
            raise ValueError('Reviewer capacity exceeded')
    submissions, per_case, pairs = {}, {c: [] for c in cases}, set()
    for item in data['submissions']:
        fields(item, ('id', 'case_id', 'case_version', 'artifact_sha256', 'reviewer_id',
                      'verdict', 'seconds', 'findings', 'reviewed_at'))
        sid, cid, rid = text(item['id']), item['case_id'], item['reviewer_id']
        if sid in submissions or (cid, rid) not in assigned or (cid, rid) in pairs:
            raise ValueError('Duplicate or unassigned submission')
        case = cases[cid]
        if type(item['case_version']) is not int or item['case_version'] != case['version'] or item['artifact_sha256'] != case['artifact_sha256']:
            raise ValueError('Stale review version or artifact')
        if item['verdict'] not in ('accept', 'revise', 'reject'):
            raise ValueError('Unknown review verdict')
        if type(item['seconds']) not in (int, float) or not math.isfinite(item['seconds']) or not 0 < item['seconds'] <= 31536000:
            raise ValueError('Positive bounded review time required')
        if date(item['reviewed_at']) > date(data['as_of']):
            raise ValueError('Future review declaration')
        if type(item['findings']) is not list or len(item['findings']) > 100:
            raise ValueError('Bounded findings required')
        finding_ids = set()
        for finding in item['findings']:
            fields(finding, ('id', 'severity', 'statement'))
            fid = text(finding['id']); text(finding['statement'])
            if fid in finding_ids or finding['severity'] not in ('minor', 'major', 'blocking'):
                raise ValueError('Invalid or duplicate finding')
            finding_ids.add(fid)
        pairs.add((cid, rid)); submissions[sid] = item; per_case[cid].append(item)
    adjudications = {}
    for item in data['adjudications']:
        fields(item, ('case_id', 'case_version', 'artifact_sha256', 'adjudicator_id',
                      'decision', 'reason', 'submission_ids', 'resolutions', 'adjudicated_at'))
        cid, rid = item['case_id'], item['adjudicator_id']
        if cid not in cases or rid not in reviewers or cid in adjudications:
            raise ValueError('Invalid or duplicate adjudication')
        case, person = cases[cid], reviewers[rid]
        if 'adjudicator' not in person['roles'] or cid in person['conflicts'] or (cid, rid) in assigned:
            raise ValueError('Adjudication role, conflict or self-review violation')
        if type(item['case_version']) is not int or item['case_version'] != case['version'] or item['artifact_sha256'] != case['artifact_sha256']:
            raise ValueError('Stale adjudication')
        text(item['reason']); labels(item['submission_ids'])
        if item['decision'] not in ('accept', 'revise', 'reject'):
            raise ValueError('Unknown adjudication decision')
        expected = {s['id'] for s in per_case[cid]}
        if set(item['submission_ids']) != expected or not expected:
            raise ValueError('Adjudication must cover all current submissions')
        timestamp = date(item['adjudicated_at'])
        if timestamp > date(data['as_of']) or any(date(s['reviewed_at']) > timestamp for s in per_case[cid]):
            raise ValueError('Invalid adjudication time')
        findings = {(s['id'], f['id']): f for s in per_case[cid] for f in s['findings']}
        if type(item['resolutions']) is not list or len(item['resolutions']) > 1000:
            raise ValueError('Bounded finding resolutions required')
        resolved = set()
        for resolution in item['resolutions']:
            fields(resolution, ('submission_id', 'finding_id', 'disposition', 'reason'))
            key = (resolution['submission_id'], resolution['finding_id'])
            if key not in findings or key in resolved or resolution['disposition'] not in ('sustained', 'dismissed'):
                raise ValueError('Invalid finding resolution')
            text(resolution['reason']); resolved.add(key)
            if item['decision'] == 'accept' and resolution['disposition'] == 'sustained' and findings[key]['severity'] in ('major', 'blocking'):
                raise ValueError('Cannot accept sustained major or blocking findings')
        if resolved != set(findings):
            raise ValueError('Every finding requires explicit resolution')
        adjudications[cid] = item
    results = {}
    for cid in order:
        case, reviews, blockers = cases[cid], per_case[cid], []
        if len(reviews) < case['minimum_reviews']: blockers.append('MINIMUM_REVIEWS_MISSING')
        if cid not in adjudications: blockers.append('ADJUDICATION_MISSING')
        elif adjudications[cid]['decision'] != 'accept': blockers.append('ADJUDICATOR_REQUIRES_'+adjudications[cid]['decision'].upper())
        for dep in case['dependencies']:
            if results[dep]['disposition'] != 'accepted_declared': blockers.append('DEPENDENCY_NOT_ACCEPTED:'+dep)
        results[cid] = {'case_version': case['version'], 'artifact_sha256': case['artifact_sha256'],
                        'disposition': 'accepted_declared' if not blockers else 'review_required',
                        'blockers': blockers, 'review_count': len(reviews),
                        'verdict_disagreement': len({s['verdict'] for s in reviews}) > 1,
                        'recorded_review_seconds': sum(s['seconds'] for s in reviews),
                        'finding_count': sum(len(s['findings']) for s in reviews),
                        'adjudicator': adjudications.get(cid, {}).get('adjudicator_id')}
    return {'schema_version': 1, 'input_sha256': digest(data), 'case_order': order,
            'cases': results, 'assignment_loads': loads,
            'total_recorded_review_seconds': sum(s['seconds'] for s in submissions.values()),
            'reviewer_independence_established': False,
            'status': 'declared_human_workflow_not_authenticated_review',
            'limitations': ['Actors, conflicts, elapsed time and artifact hashes are caller declarations',
                           'No source bytes, reviewer identity or external independence authenticated',
                           'Recorded time and finding counts do not establish faster or more accurate review',
                           'Acceptance requires explicit adjudication, not a vote or scientific truth certificate']}
