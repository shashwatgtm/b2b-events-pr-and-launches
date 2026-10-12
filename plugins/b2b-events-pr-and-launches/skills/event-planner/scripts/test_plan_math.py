#!/usr/bin/env python3
"""Tests for plan_math.py. Run: python3 test_plan_math.py (prints one line per test and a total).

Every number below is a hypothetical test input, chosen only to make the arithmetic easy to check.
None of them is a benchmark or a suggestion.
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "plan_math.py")


def run(*args):
    p = subprocess.run([sys.executable, "-I", SCRIPT, *args], capture_output=True, text=True)
    return p.returncode, p.stdout


def plan_file(plan):
    fh = tempfile.NamedTemporaryFile("w", delete=False, suffix=".json", encoding="utf-8")
    if isinstance(plan, str):
        fh.write(plan)
    else:
        json.dump(plan, fh)
    fh.close()
    return fh.name


def portfolio(plan):
    path = plan_file(plan)
    try:
        return run("portfolio", path)
    finally:
        os.unlink(path)


FULL_TYPE = {"name": "Roundtable", "events": 2, "contacts_per_event": 20, "relevant_share": 100,
             "first_stage_rate": 50, "accepted_rate": 50, "cost_per_event": 1000}

TESTS = []


def test(fn):
    TESTS.append(fn)
    return fn


@test
def portfolio_complete_with_gap():
    code, out = portfolio({"target": 40, "event_share": 50, "types": [FULL_TYPE]})
    assert code == 0, out
    assert "| Roundtable | 40 | 40 | 20 | 10 | 2,000.00 | 200.00 |" in out, out
    assert "Needed from events (target x event share): 20" in out, out
    assert "Gap: 10 accepted leads short" in out, out


@test
def portfolio_covers_share():
    code, out = portfolio({"target": 10, "event_share": 50, "types": [FULL_TYPE]})
    assert code == 0 and "Gap: none; the plan covers the share by 5" in out, out


@test
def portfolio_two_types_blended_cost():
    second = dict(FULL_TYPE, name="Webinar", events=1, contacts_per_event=100, relevant_share=50,
                  first_stage_rate=20, accepted_rate=50, cost_per_event=500)
    code, out = portfolio({"target": 40, "event_share": 50, "types": [FULL_TYPE, second]})
    assert code == 0, out
    assert "| Webinar | 100 | 50 | 10 | 5 | 500.00 | 100.00 |" in out, out
    assert "Planned accepted leads from events: 15" in out, out
    assert "Blended cost per accepted lead: 166.67" in out, out


@test
def portfolio_missing_field_not_filled():
    partial = dict(FULL_TYPE)
    del partial["accepted_rate"]
    code, out = portfolio({"target": 40, "event_share": 50, "types": [partial]})
    assert code == 1, out
    assert "[User to add: Roundtable accepted rate]" in out, out
    assert "| Roundtable | 40 | 40 | 20 | not computed | 2,000.00 | not computed |" in out, out
    assert "Planned accepted leads from events: not computed" in out and "Gap:" not in out, out


@test
def portfolio_missing_target():
    code, out = portfolio({"types": [FULL_TYPE]})
    assert code == 1 and "[User to add: sales target in your accepted stage]" in out, out
    assert "[User to add: share of the target events must deliver]" in out, out
    assert "Needed from events (target x event share): not computed" in out, out


@test
def portfolio_zero_accepted_note():
    zero = dict(FULL_TYPE, accepted_rate=0)
    code, out = portfolio({"target": 40, "event_share": 50, "types": [zero]})
    assert code == 0 and "cannot be computed" in out and "Blended cost" not in out, out


@test
def portfolio_rejects_percent_over_100():
    code, out = portfolio({"target": 40, "event_share": 150, "types": [FULL_TYPE]})
    assert code == 2 and "must be 0 to 100" in out, out


@test
def portfolio_rejects_text_value():
    bad = dict(FULL_TYPE, events="four")
    code, out = portfolio({"target": 40, "event_share": 50, "types": [bad]})
    assert code == 2 and "must be a number" in out, out


@test
def portfolio_rejects_negative():
    bad = dict(FULL_TYPE, cost_per_event=-1)
    code, out = portfolio({"target": 40, "event_share": 50, "types": [bad]})
    assert code == 2 and "must not be negative" in out, out


@test
def portfolio_rejects_broken_json():
    code, out = portfolio("{not json")
    assert code == 2 and "cannot read" in out, out


@test
def portfolio_rejects_empty_types():
    code, out = portfolio({"target": 40, "types": []})
    assert code == 2 and "non empty" in out, out


@test
def needed_backwards():
    code, out = run("needed", "accepted=10", "first-rate=50", "accepted-rate=50",
                    "relevant=100", "contacts-per-event=15")
    assert code == 0, out
    assert "First stage leads needed: 20" in out and "Total contacts needed: 40" in out, out
    assert "Events needed (rounded up): 3" in out, out


@test
def needed_exact_division_not_rounded_up():
    code, out = run("needed", "accepted=10", "first-rate=50", "accepted-rate=50",
                    "relevant=100", "contacts-per-event=20")
    assert code == 0 and "Events needed (rounded up): 2" in out, out


@test
def needed_missing_flag():
    code, out = run("needed", "accepted=10")
    assert code == 1 and "[User to add: first stage rate]" in out and "Events needed" not in out, out


@test
def needed_zero_rate():
    code, out = run("needed", "accepted=10", "first-rate=0", "accepted-rate=50",
                    "relevant=100", "contacts-per-event=20")
    assert code == 2 and "is 0" in out, out


@test
def needed_bad_pair():
    code, out = run("needed", "accepted")
    assert code == 2 and "expected name=value" in out, out


@test
def unknown_command():
    code, out = run("nonsense")
    assert code == 2 and "unknown command" in out, out


def main():
    passed = 0
    for fn in TESTS:
        try:
            fn()
            print(f"PASS {fn.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL {fn.__name__}: {e}")
    print(f"{passed} of {len(TESTS)} tests passed")
    return 0 if passed == len(TESTS) else 1


if __name__ == "__main__":
    sys.exit(main())
