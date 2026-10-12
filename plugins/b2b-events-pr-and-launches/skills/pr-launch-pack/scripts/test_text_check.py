#!/usr/bin/env python3
"""Tests for text_check.py. Run: python3 test_text_check.py (prints one line per test and a total)."""
import datetime
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "text_check.py")


def run(*args):
    p = subprocess.run([sys.executable, "-I", SCRIPT, *args], capture_output=True, text=True)
    return p.returncode, p.stdout


TESTS = []


def test(fn):
    TESTS.append(fn)
    return fn


@test
def count_ascii():
    code, out = run("count", "Launch day set by your audience")
    assert code == 0 and "characters=31" in out and "words=6" in out, out


@test
def count_devanagari_by_code_points():
    text = "".join(chr(c) for c in (0x928, 0x92E, 0x938, 0x94D, 0x924, 0x947))  # a six code point Hindi word
    code, out = run("count", text)
    assert code == 0 and "characters=6" in out and "words=1" in out, out


@test
def count_emoji_flags_utf16():
    code, out = run("count", "Go \U0001F680")
    assert code == 0 and "characters=4" in out and "utf16_units=5" in out and "NOTE" in out, out


@test
def count_file_lines():
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt", encoding="utf-8") as fh:
        fh.write("Subject one\n\nSubject two is longer\n")
        path = fh.name
    code, out = run("count", "-f", path)
    os.unlink(path)
    assert code == 0 and "line 1: characters=11" in out and "line 3: characters=21" in out and "line 2" not in out, out


@test
def count_file_long_flag():
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt", encoding="utf-8") as fh:
        fh.write("One line\n")
        path = fh.name
    code, out = run("count", "-" * 2 + "file", path)
    os.unlink(path)
    assert code == 0 and "line 1: characters=8" in out, out


@test
def date_known_weekday_match():
    code, out = run("date", "2026-10-28", "Wednesday")
    assert code == 0 and "is a Wednesday" in out and "MATCH" in out, out


@test
def date_known_weekday_mismatch():
    code, out = run("date", "2026-03-20", "Thursday")
    assert code == 1 and "MISMATCH" in out and "Friday" in out, out


@test
def date_bad_input():
    code, out = run("date", "2026-02-30")
    assert code == 2 and "not a valid" in out, out


@test
def date_reports_past_or_future():
    code, out = run("date", "2000-01-01")
    assert code == 0 and "in the past" in out, out


@test
def dashes_none():
    code, out = run("dashes", "A plain sentence with a well-known hyphen.")
    assert code == 0 and "none found" in out, out


@test
def dashes_long_and_short():
    code, out = run("dashes", "Fast " + chr(0x2014) + " and 2024" + chr(0x2013) + "2026")
    assert code == 1 and "long dash" in out and "short dash" in out and "2 found" in out, out


@test
def dashes_spaced_and_double_hyphen():
    code, out = run("dashes", "word " + "-" + " word and this" + "-" * 2 + "that")
    assert code == 1 and "spaced hyphen" in out and "double hyphen" in out, out


@test
def today_runs():
    code, out = run("today")
    assert code == 0 and datetime.date.today().isoformat()[:4] in out, out


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
