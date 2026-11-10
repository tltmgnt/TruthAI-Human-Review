"""Offline curriculum answer key. Synthetic checks, never operational approval."""
import ast
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
for base in (ROOT, ROOT / "src", ROOT / "layer-b"):
    sys.path.insert(0, str(base))
CASES = []

def check(name, actual, expected):
    passed = actual == expected
    CASES.append({"case": name, "actual": actual, "expected": expected, "passed": passed})
    if not passed:
        raise AssertionError(f"{name}: expected {expected!r}, got {actual!r}")

def rejects(name, call, error=ValueError):
    try:
        call()
    except error:
        check(name, error.__name__, error.__name__)
    else:
        raise AssertionError(f"{name}: expected {error.__name__}")

def sample(path):
    return json.loads((ROOT / path).read_text())



def run():
    from human_review.workflow import evaluate
    data = sample("examples/review.json")
    r = evaluate(data)
    check("explicit adjudication records declared acceptance", r["cases"]["claim-a"]["disposition"], "accepted_declared")
    check("declared review effort", r["total_recorded_review_seconds"], 180)
    check("independence is not authenticated", r["reviewer_independence_established"], False)
    bad = copy.deepcopy(data); bad["adjudications"] = []
    q = evaluate(bad)["cases"]["claim-a"]
    check("votes alone do not adjudicate", q["disposition"], "review_required")
    check("missing adjudication is visible", "ADJUDICATION_MISSING" in q["blockers"], True)
    bad = copy.deepcopy(data); bad["submissions"][0]["case_version"] = 2
    rejects("stale version-bound review", lambda: evaluate(bad))

if __name__ == "__main__":
    if sys.argv[1:] not in ([], ["--verify"]):
        raise SystemExit("Usage: python curriculum/lab.py [--verify]")
    run()
    report = {"schema_version": 1, "status": "PASS", "case_count": len(CASES),
              "cases": CASES, "scope": "Synthetic curriculum checks only"}
    if sys.argv[1:] == ["--verify"]:
        expected = json.loads((Path(__file__).parent / "expected.json").read_text())
        if report != expected:
            raise AssertionError("Observed answers differ from curriculum/expected.json")
    print(json.dumps(report, sort_keys=True, indent=2, allow_nan=False))
