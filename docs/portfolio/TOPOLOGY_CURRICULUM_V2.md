# Topology compatibility and curriculum v2 — TruthAI-Human-Review

Version 2 adapts the explicit-molecular-graph teaching pattern to this repository's actual role. This is documentation and a learning/decision framework; it introduces no mathematical engine, runtime dependency or operational permission.

## Repository decision

| Question | Repository-specific answer |
| --- | --- |
| Architectural role | specialized workflow |
| Minimum useful mathematics | Directed assignment/review dependencies and explicit adjudication |
| Relationships to preserve | Snapshot bindings, reviewer assignments, findings and decisions |
| Concrete operation / capstone | Change a reviewed artifact digest and explain why the old review cannot transfer automatically |
| Necessity and scope boundary | Review declarations do not authenticate reviewers; no invitations or external messages are sent |

The decision is a source-based recommendation, not measured proof that a new specialty improves this repository. Start with the existing implementation and compare any proposed abstraction against a simpler alternative.

## Six-criterion compatibility scorecard

Complete one scorecard per proposed candidate and per concrete operation. Leave unmeasured entries unknown. Scores are human judgments from 0 (no fit) to 5 (strong evidenced fit); unknown is not zero. Do not sum an incomplete card. A total out of 30 is a heuristic, not adoption approval, and feasibility or necessity can veto a high total.

| Criterion | Score | Required evidence |
| --- | --- | --- |
| Structural compatibility | Not yet scored | Map the repository objects and the relationships above without losing direction, labels, units or missingness. |
| Transformation support | Not yet scored | Demonstrate the capstone operation on accepted and rejected inputs. |
| Invariant preservation | Not yet scored | State the property preserved and supply a counterexample or perturbation. |
| Computational feasibility | Not yet scored | Measure size, time and memory on bounded fixtures; record limits. |
| Integration compatibility | Not yet scored | Verify existing schemas, APIs and neighboring contracts remain compatible. |
| Mathematical necessity | Not yet scored | Compare with directed assignment/review dependencies and explicit adjudication and explain the additional capability, if any. |

## Curriculum

Prerequisites: basic programming, sets, functions and graph vocabulary. Work in six competency-gated sessions, approximately 60–90 minutes each; empirical evaluation is a separate research activity.

| Session | Learning objective | Exercise | Completion evidence |
| --- | --- | --- | --- |
| 1. Model | Identify snapshot bindings, reviewer assignments, findings and decisions. | Draw a minimal valid example and one excluded relationship. | Annotated object/relation inventory with explicit assumptions. |
| 2. Contract | Distinguish schema validity from substantive correctness. | Trace validation and propose malformed, missing and boundary inputs. | Input-to-rejection table grounded in current source. |
| 3. Operation | Explain directed assignment/review dependencies and explicit adjudication. | Change a reviewed artifact digest and explain why the old review cannot transfer automatically. | Hand trace compared with existing software, or a clearly labeled specification when no runtime exists. |
| 4. Preservation | State what a transformation must preserve. | Rename identifiers, reorder records, then alter one meaningful relation; predict each effect under the actual contract. | Separate invariant, expected change and unsupported transformation. |
| 5. Comparison | Justify mathematical necessity and cost. | Complete the six-criterion card for the existing approach and one proposed alternative; record unknowns honestly. | Evidence-backed recommendation with baseline and explicit veto conditions. |
| 6. Reproduction | Communicate the bounded result. | Reproduce the capstone using existing offline fixtures and record software version, inputs, outputs and limitations. | Reviewable notebook or report distinguishing computation, replay, independent evaluation and authorization. |

## Source-linked reading laboratory

The table is a guided selection of source lines, not an assertion that the whole repository is covered. Line numbers refer to the inspected source blob `176647a962efa1c89181265201e2fecd256b5d5c` in [human_review/workflow.py](../../human_review/workflow.py). Recheck anchors after source changes.

| Line | Statement | Learning check |
| --- | --- | --- |
| [6](../../human_review/workflow.py#L6) | `def sha(value):` | State the input/output contract and trace one normal and one failing case. |
| [8](../../human_review/workflow.py#L8) | `raise ValueError('SHA-256 artifact reference required')` | Construct the triggering input and explain why rejection preserves the contract. |
| [11](../../human_review/workflow.py#L11) | `def indexed(items, maximum):` | State the input/output contract and trace one normal and one failing case. |
| [13](../../human_review/workflow.py#L13) | `raise ValueError('Nonempty bounded records required')` | Construct the triggering input and explain why rejection preserves the contract. |
| [17](../../human_review/workflow.py#L17) | `raise ValueError('Object records required')` | Construct the triggering input and explain why rejection preserves the contract. |
| [20](../../human_review/workflow.py#L20) | `raise ValueError('Duplicate record ID')` | Construct the triggering input and explain why rejection preserves the contract. |
| [22](../../human_review/workflow.py#L22) | `return result` | Predict the returned value and distinguish a computed result from authorization. |
| [25](../../human_review/workflow.py#L25) | `def labels(items):` | State the input/output contract and trace one normal and one failing case. |
| [27](../../human_review/workflow.py#L27) | `raise ValueError('List of identifiers required')` | Construct the triggering input and explain why rejection preserves the contract. |
| [31](../../human_review/workflow.py#L31) | `raise ValueError('Duplicate identifier')` | Construct the triggering input and explain why rejection preserves the contract. |
| [34](../../human_review/workflow.py#L34) | `def evaluate(data):` | State the input/output contract and trace one normal and one failing case. |
| [35](../../human_review/workflow.py#L35) | `fields(data, ('schema_version', 'as_of', 'expires_at', 'cases', 'reviewers',` | Separate type, shape and value checks; test a missing field and an invalid value. |
| [37](../../human_review/workflow.py#L37) | `if type(data['schema_version']) is not int or data['schema_version'] != 1:` | Separate type, shape and value checks; test a missing field and an invalid value. |
| [38](../../human_review/workflow.py#L38) | `raise ValueError('Unsupported schema version')` | Construct the triggering input and explain why rejection preserves the contract. |
| [40](../../human_review/workflow.py#L40) | `raise ValueError('Expiry must follow assessment time')` | Construct the triggering input and explain why rejection preserves the contract. |
| [46](../../human_review/workflow.py#L46) | `raise ValueError('Positive case version required')` | Construct the triggering input and explain why rejection preserves the contract. |
| [48](../../human_review/workflow.py#L48) | `raise ValueError('Between 1 and 10 reviews required')` | Construct the triggering input and explain why rejection preserves the contract. |
| [50](../../human_review/workflow.py#L50) | `raise ValueError('Unknown or self dependency')` | Construct the triggering input and explain why rejection preserves the contract. |
| [52](../../human_review/workflow.py#L52) | `def visit(cid):` | State the input/output contract and trace one normal and one failing case. |
| [53](../../human_review/workflow.py#L53) | `if cid in visiting: raise ValueError('Cyclic case dependencies')` | Construct the triggering input and explain why rejection preserves the contract. |
| [63](../../human_review/workflow.py#L63) | `raise ValueError('Unknown or empty roles')` | Construct the triggering input and explain why rejection preserves the contract. |
| [65](../../human_review/workflow.py#L65) | `raise ValueError('Unknown conflict case')` | Construct the triggering input and explain why rejection preserves the contract. |
| [67](../../human_review/workflow.py#L67) | `raise ValueError('Bounded reviewer capacity required')` | Construct the triggering input and explain why rejection preserves the contract. |
| [71](../../human_review/workflow.py#L71) | `raise ValueError('Bounded workflow lists required')` | Construct the triggering input and explain why rejection preserves the contract. |
## Assessment and verification

A learner must explain the model, trace the capstone, identify a counterexample and state the scope boundary. Assess these four competencies equally; a numerical score cannot compensate for an unsupported scientific or operational claim.

Relevant existing checks:

- [tests/test_review.py](../../tests/test_review.py)

Follow [README](../../README.md) for environment and installed-package instructions. Read scripts before execution; source-reading exercises do not authorize provider calls, model downloads, live orders, hardware actions or messages. Synthetic fixtures establish software behavior only. This documentation change does not report those exercises as already executed.

## Interoperability and adoption gate

Retain explicit domain contracts. Shared assurance records should refer to domain evidence and its assumptions rather than relabeling graph reachability, homology, statistical calibration and epistemic acceptance as interchangeable quantities. The canonical ResearchOs controller remains owned by ResearchOs; this curriculum does not create another controller fork.

Adopt additional mathematics only after a versioned experiment demonstrates a useful operation, the scorecard has evidence, the simpler baseline is inadequate and existing conformance checks remain satisfied. Review declarations do not authenticate reviewers; no invitations or external messages are sent.
