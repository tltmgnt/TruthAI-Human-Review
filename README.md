# TruthAI Human Review

Offline, snapshot-bound reviewer assignments, findings, explicit adjudication and
ResearchOS evidence replay. The package checks supplied review declarations; it does
not authenticate reviewers, send invitations, host accounts or establish scientific truth.

## Install and run

Python 3.10 or later; standard-library runtime, no service account required.

```bash
python -m pip install .
mkdir -p runs
truthai-review analyze examples/review.json --output runs/example
truthai-review verify runs/example
python -m unittest discover -s tests -v
python tests/check_installed.py
```

Without installation use `python -m human_review`. Open `runs/example/review.html`
for the captured case, assignments, review findings, adjudication and assurance blockers.
The example contains fictional reviewer IDs, findings and timing declarations; it is
not a record of real expert review. Output directories must be new with existing parents.

Exit 0 means scoped computation or exact historical replay succeeded. The printed
UNASSURED status remains explicit. Invalid inputs, stale reviews, conflicting assignments,
existing destinations and changed bundles exit 2. Fixed example assessment times are
not renewed; a new study must supply its own assessment and expiry times.

## Implemented workflow

| Stage | Enforced behavior |
| --- | --- |
| Case registration | Case ID, positive version, statement, artifact digest, required review count, acyclic dependencies |
| Assignment | Explicit reviewer role, declared conflicts, capacity limits, unique reviewer/case pairs |
| Submission | Current case version/artifact, assigned reviewer, verdict, measured-time declaration and severity-tagged findings |
| Adjudication | Separate eligible adjudicator, all current submissions covered, explicit reasons and resolution of every finding |
| Acceptance | Required review count, explicit accept adjudication, no sustained major/blocking finding and accepted dependencies |
| Change handling | Changed versions/artifacts reject stale submissions; dependent dispositions recompute from the full input snapshot |
| Evidence | Canonical ResearchOS controller, recorded domain receipt, rejection ledger and replay bundle |

Consensus is reported but cannot replace adjudication. An adjudicator can override
review verdicts only through a captured decision and explicit finding resolutions.
A sustained major or blocking finding prevents acceptance of the same artifact. Fixes
require a new artifact/version and new review declarations. Minor sustained findings
may remain with a documented accept decision. A minimum-review count establishes
quantity, not independent expertise.

## Input and output

The complete schema is illustrated by [examples/review.json](examples/review.json).
Top-level fields: `schema_version`, `as_of`, `expires_at`, `cases`, `reviewers`,
`assignments`, `submissions`, `adjudications`. Unknown fields and duplicate JSON keys
are rejected. Case/reviewer IDs must be unique. Reviews bind both a case version and
artifact SHA-256; source artifact bytes are not imported or authenticated.

Limits: 32 cases, 128 reviewer declarations, 320 assignments/submissions, 32
adjudications, 100 findings per submission and 8 MiB input/output files. Review time
must be positive, finite and no greater than one year. Times are caller declarations;
future reviews and adjudications preceding their reviews are rejected. Declared
conflicts are scoped to individual case IDs; undisclosed conflicts are not detected.

Bundles contain `input.json`, `reviews.json`, `scenario.json`, `ledger.json`,
`researchos.json`, `review.html` and `manifest.json`. HTML is escaped and uses no
external assets. Exact verification recomputes domain results, controller operations
and every output byte, with implementation fingerprints. Hashes/replay establish
consistency, not authenticity; a different internally consistent input is a new study.
Replay uses captured assessment time, not current evidence validity.

Reviewers should use pseudonyms. Input captures all supplied findings and statements;
keep private records out of public bundles. The software has no invitation, messaging,
clinical or external execution capability.

## ResearchOS integration

Six unchanged canonical v0.1.0 modules are vendored under `human_review._tect`.
[researchos-lock.json](researchos-lock.json) pins the source commit and release hashes;
tests enforce byte conformance. The domain adapter calls the real Controller. Its
dependency direction is prerequisite source to dependent target. Actor identities are
declared local policy roles rather than authenticated reviewer accounts.

Accepted declarations become PASS evidence about local workflow satisfaction. Missing
or adverse adjudication becomes UNCERTAIN evidence and leaves the claim unsupported;
it does not disappear from the report. Supported cases can reach ADVERSARIAL_TEST,
but independent reproduction and required domain attacks remain missing. They cannot
reach ASSURED from the supplied records. Policy density threshold .001 and evidence
weights are local acceptance settings, not calibrated probabilities or scientific trust.

ResearchOS claim version starts at 1 in each newly constructed controller; the actual
domain case version is bound in the receipt and captured input. This is a replayable
snapshot workflow, not a persistent multi-user review service. Canonical revision and
dependency invalidation are tested separately. See [evaluation and limits](docs/EVALUATION.md).

## Validation and scope

Tests cover conflicts, capacity, roles, stale versions/artifacts, missing reviews,
disagreement, explicit resolutions, dependency gaps/cycles, time declarations, tampering,
HTML escaping, canonical hashes and ResearchOS rejection/invalidation. The installed
workflow check imports outside the source checkout. CI runs Python 3.10, 3.12 and 3.13
and publishes only the fictional example.

Not implemented: authenticated users/signatures, persistent concurrent editing,
automatic expert recruitment, real artifact custody, blinded comparative trials or
verified review-time savings. Existing Apache-2.0 license retained; canonical vendored
ResearchOs code is Apache-2.0.

**∞**

## Topology compatibility and curriculum

See the [repository-specific v2 curriculum](docs/portfolio/TOPOLOGY_CURRICULUM_V2.md) for topology choices, worked explanations, a graded laboratory and adoption boundaries. Run the offline answer key from this repository root:\n\n```sh\npython curriculum/lab.py --verify\n```\n\n[Expected answers](curriculum/expected.json) · [Recorded local validation](curriculum/VALIDATION.json). The guide states any existing dependency needed for the lab.
