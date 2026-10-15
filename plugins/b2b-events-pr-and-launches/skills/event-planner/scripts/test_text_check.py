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
def date_reports_days_from_today():
    future = (datetime.date.today() + datetime.timedelta(days=17)).isoformat()
    code, out = run("date", future)
    assert code == 0 and "17 days from today" in out, out
    past = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    code, out = run("date", past)
    assert code == 0 and "1 day ago" in out, out
    code, out = run("date", datetime.date.today().isoformat())
    assert code == 0 and "(today;" in out, out


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


@test
def s2_cp1252_output_is_utf8():
    """S2, run 32A: a weekday argument with a rupee sign is echoed as UTF-8, never an encoding error, on a code page 1252 pipe."""
    env = dict(os.environ, PYTHONIOENCODING="cp1252")
    p = subprocess.run([sys.executable, SCRIPT, "date", "2026-10-28", "\u20b9day"], capture_output=True, env=env)
    assert b"Traceback" not in p.stderr, p.stderr.decode("utf-8", "replace")
    assert p.returncode == 2 and "\u20b9day".encode("utf-8") in p.stdout, (p.returncode, p.stdout)


@test
def file_name_without_flag_refused_dashes():
    """Run 33A (judge 33A-5, EVK-2): `dashes draft.txt` without -f checked the 9 characters "draft.txt" and said "none found";
    a lone argument that names an existing file is bad input with a message that points to -f, never a silent pass."""
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "draft.txt")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("Launch day " + chr(0x2014) + " set by you\n")
        code, out = run("dashes", path)
        assert code == 2 and "-f" in out and "none found" not in out, (code, out)
        code, out = run("dashes", "-f", path)
        assert code == 1 and "long dash" in out, (code, out)


@test
def file_like_name_without_flag_refused():
    """Run 33A: a lone argument shaped like a file name (no space, a text file ending) is refused even when the file is not in the
    current folder, for dashes and count, so a wrong folder can never pass as a clean draft."""
    for cmd in ("dashes", "count"):
        for name in ("draft.txt", "notes.md", "kit.markdown", "rows.csv"):
            code, out = run(cmd, name)
            assert code == 2 and "-f" in out, (cmd, name, code, out)


@test
def count_existing_file_without_flag_refused():
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "headline.txt")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("A headline\n")
        code, out = run("count", path)
        assert code == 2 and "-f" in out, (code, out)


@test
def ordinary_strings_still_checked():
    """Parity: text with a space, or a single word that is not a file name, is still checked as text."""
    assert run("dashes", "Launch day set by you") == (0, "dashes: none found\n")
    code, out = run("count", "Launch")
    assert code == 0 and "characters=6" in out, out
    code, out = run("count", "v2.0")
    assert code == 0 and "characters=4" in out, out


@test
def missing_or_bad_file_is_bad_input():
    """Run 33A auditor S1: -f or --file with a missing file or a folder ends with bad input (exit 2), never a traceback or exit 1."""
    with tempfile.TemporaryDirectory() as d:
        for cmd in ("dashes", "count"):
            for flag in ("-f", "--file"):
                for target in (os.path.join(d, "nofile.txt"), d):
                    p = subprocess.run([sys.executable, "-I", SCRIPT, cmd, flag, target], capture_output=True, text=True)
                    assert p.returncode == 2 and "Traceback" not in p.stderr and "bad input" in p.stdout, (cmd, flag, target, p.returncode, p.stdout, p.stderr)


@test
def file_flag_without_path_is_bad_input():
    """Run 33A auditor S2: `dashes -f` or `count --file` with no path was read as the text "-f" and passed; it is bad input."""
    for cmd in ("dashes", "count"):
        for flag in ("-f", "--file"):
            code, out = run(cmd, flag)
            assert code == 2 and "bad input" in out, (cmd, flag, code, out)


@test
def more_file_endings_and_folders_refused():
    """Run 33A auditor S3: other document endings and an existing folder name given alone are refused, not checked as text."""
    for name in ("draft.docx", "draft.rtf", "draft.tex", "draft.text", "draft.pdf"):
        code, out = run("dashes", name)
        assert code == 2 and "-f" in out, (name, code, out)
    with tempfile.TemporaryDirectory() as d:
        code, out = run("dashes", d)
        assert code == 2, (d, code, out)




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
