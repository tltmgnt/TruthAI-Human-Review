# Evaluation and acceptance limits

The analyzer evaluates a complete captured review snapshot. It separates invalid
transport/workflow records (exit 2) from valid but incomplete review (exit 0 with
review_required and ResearchOS assurance blockers). Acceptance means declared
workflow criteria were met, not that the reviewed claim is true.

Review time is the sum of caller-supplied seconds. Finding counts are observations,
not precision or recall. There is no adjudicated ground-truth issue set in this
first release, so fewer findings cannot be called higher review quality. No comparative
speed or accuracy advantage is claimed. Verdict disagreement remains visible after
an adjudicator settles a case; no vote silently changes its disposition.

Before an expert-review evaluation, freeze cases/artifact versions, reference issues,
reviewer qualifications, conflicts, baseline and assisted conditions, assignment and
counterbalancing, elapsed-time collection, accuracy noninferiority margin, minimum
practical time saving, missing-data rules and sample-size rationale. Protect held-out
labels and report errors, unresolved cases and negative outcomes. Reviewer and case
correlation must be considered in statistical analysis.

Cross-repository boundary: MathOS can emit review packets, but this release does not
silently convert its statement text into authenticated artifacts or claim that a live
TruthAi account was connected. A future adapter must define stable case IDs, explicit
versions, artifact-byte capture/digests, finding identifiers and schema versions. The
ResearchOS controller is integrated locally now; platform account integration is not.

No declared reviewer identity, conflict list or independence weight proves independence.
External review, source custody and reproduction remain separately supplied evidence.
Canonical controller attack gates stay open; regression tests cannot substitute for
real domain attack results. No invitations, payments, automatic approval, operational
authorization or recurring activity are enabled by this repository.
