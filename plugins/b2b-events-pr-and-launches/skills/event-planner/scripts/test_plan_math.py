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


# Run 31C, Codex finding F001: a non finite number or a row that is not an object is bad input (exit 2), never a traceback;
# needed with accepted=0 answers 0 events; a zero rate with a positive target stays a refusal.
def type_json(**over):
    t = dict(FULL_TYPE, **{k: "@" + k for k in over})
    text = json.dumps({"target": 40, "event_share": 50, "types": [t]})
    for k, v in over.items():
        text = text.replace(json.dumps("@" + k), v)
    return text


@test
def portfolio_nan_is_bad_input():
    code, out = portfolio(type_json(events="NaN"))
    assert code == 2 and "bad input" in out and "finite" in out, out


@test
def portfolio_infinity_is_bad_input():
    for over in ({"events": "Infinity"}, {"cost_per_event": "Infinity"}, {"relevant_share": "-Infinity"}):
        code, out = portfolio(type_json(**over))
        assert code == 2 and "bad input" in out, (over, out)


@test
def portfolio_nan_target_or_share_is_bad_input():
    for text in ('{"target": NaN, "event_share": 50, "types": [%s]}' % json.dumps(FULL_TYPE),
                 '{"target": 40, "event_share": Infinity, "types": [%s]}' % json.dumps(FULL_TYPE)):
        code, out = portfolio(text)
        assert code == 2 and "bad input" in out and "finite" in out, (text, out)


@test
def portfolio_row_not_an_object_is_bad_input():
    for row in (1, "Roundtable", None, [1, 2]):
        code, out = portfolio({"target": 40, "event_share": 50, "types": [FULL_TYPE, row]})
        assert code == 2 and "bad input" in out and "object" in out, (row, out)


@test
def portfolio_overflow_is_bad_input():
    big = dict(FULL_TYPE, events=1e308, contacts_per_event=1e308)
    code, out = portfolio({"target": 40, "event_share": 50, "types": [big]})
    assert code == 2 and "bad input" in out, out


@test
def needed_non_finite_flag_is_bad_input():
    for flag in ("accepted=nan", "accepted=inf", "contacts-per-event=Infinity"):
        args = {"accepted": "accepted=10", "first-rate": "first-rate=50", "accepted-rate": "accepted-rate=50",
                "relevant": "relevant=100", "contacts-per-event": "contacts-per-event=20"}
        args[flag.split("=")[0]] = flag
        code, out = run("needed", *args.values())
        assert code == 2 and "bad input" in out, (flag, out)


@test
def needed_accepted_zero_needs_no_events():
    code, out = run("needed", "accepted=0", "first-rate=0", "accepted-rate=10", "relevant=100", "contacts-per-event=10")
    assert code == 0 and "Events needed (rounded up): 0" in out, out
    code, out = run("needed", "accepted=0", "first-rate=0", "accepted-rate=0", "relevant=0", "contacts-per-event=0")
    assert code == 0 and "Events needed (rounded up): 0" in out, out


@test
def portfolio_huge_integer_is_bad_input():
    # Run 31C auditor gap A: an integer too large for a float is bad input, never a traceback
    code, out = portfolio('{"target": 1%s, "event_share": 50, "types": [%s]}' % ("0" * 400, json.dumps(FULL_TYPE)))
    assert code == 2 and "bad input" in out, out


@test
def portfolio_file_not_utf8_is_bad_input():
    # Run 31C auditor gap B: a plan file that is not UTF-8 text is bad input ("cannot read"), never a traceback
    fh = tempfile.NamedTemporaryFile("wb", delete=False, suffix=".json")
    fh.write(b'{"target": 40, "event_share": 50, "types": [{"name": "\xff"}]}')
    fh.close()
    try:
        code, out = run("portfolio", fh.name)
    finally:
        os.unlink(fh.name)
    assert code == 2 and "cannot read" in out, out


@test
def needed_zero_rate_with_positive_target_still_refused():
    code, out = run("needed", "accepted=10", "first-rate=50", "accepted-rate=0", "relevant=100", "contacts-per-event=20")
    assert code == 2 and "is 0" in out, out


@test
def s2_cp1252_type_name_with_rupee():
    """S2, run 32A: a type name with a rupee sign, a Unicode minus and curly quotes is printed as UTF-8 on a code page 1252 pipe."""
    name = "Round table \u20b9 \u2212 \u201cA\u201d"
    path = plan_file({"target": 10, "event_share": 50, "types": [{"name": name, "events": 1, "contacts_per_event": 10, "relevant_share": 100,
                                                                   "first_stage_rate": 50, "accepted_rate": 50, "cost_per_event": 100}]})
    try:
        env = dict(os.environ, PYTHONIOENCODING="cp1252")
        p = subprocess.run([sys.executable, SCRIPT, "portfolio", path], capture_output=True, env=env)
    finally:
        os.unlink(path)
    assert b"Traceback" not in p.stderr, p.stderr.decode("utf-8", "replace")
    assert p.returncode == 0 and name.encode("utf-8") in p.stdout, (p.returncode, p.stdout)


@test
def needed_underflow_is_bad_input():
    """Run 32A (coordinator review of run 31C): an accepted target so small that the result underflows is bad input, never "0 events"."""
    code, out = run("needed", "accepted=1e-320", "first-rate=50", "accepted-rate=50", "relevant=100", "contacts-per-event=20")
    assert code == 2 and "bad input" in out and "Events needed" not in out, out


@test
def needed_tiny_positive_target_never_zero_events():
    """Run 32A: a positive accepted target never answers 0 events needed."""
    code, out = run("needed", "accepted=1e-12", "first-rate=50", "accepted-rate=50", "relevant=100", "contacts-per-event=20")
    assert code == 2 and "bad input" in out and "Events needed (rounded up): 0" not in out, out


@test
def needed_small_fraction_still_computed():
    """Run 32A parity guard: a small but normal accepted target is still computed and rounds up to 1 event (hypothetical figures)."""
    code, out = run("needed", "accepted=0.5", "first-rate=50", "accepted-rate=50", "relevant=100", "contacts-per-event=20")
    assert code == 0 and "Events needed (rounded up): 1" in out, out


@test
def portfolio_subnormal_value_is_bad_input():
    """Run 32A: a value too small to compute (below the smallest normal number) is bad input in a plan too."""
    path = plan_file({"target": 10, "event_share": 50, "types": [{"name": "Roundtable", "events": 1e-320, "contacts_per_event": 10, "relevant_share": 100,
                                                                   "first_stage_rate": 50, "accepted_rate": 50, "cost_per_event": 100}]})
    try:
        code, out = run("portfolio", path)
    finally:
        os.unlink(path)
    assert code == 2 and "bad input" in out, out


@test
def needed_value_that_parses_to_zero_is_bad_input():
    """Run 32A: a written value that is not 0 but too small to hold (1e-400 reads as 0.0) is bad input, never "0 events"."""
    code, out = run("needed", "accepted=1e-400", "first-rate=50", "accepted-rate=50", "relevant=100", "contacts-per-event=20")
    assert code == 2 and "bad input" in out and "Events needed" not in out, out


@test
def portfolio_value_that_parses_to_zero_is_bad_input():
    """Run 32A: the same in a plan file."""
    path = plan_file('{"target": 10, "event_share": 50, "types": [{"name": "Roundtable", "events": 1e-400, "contacts_per_event": 10, '
                     '"relevant_share": 100, "first_stage_rate": 50, "accepted_rate": 50, "cost_per_event": 100}]}')
    try:
        code, out = run("portfolio", path)
    finally:
        os.unlink(path)
    assert code == 2 and "bad input" in out, out


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
