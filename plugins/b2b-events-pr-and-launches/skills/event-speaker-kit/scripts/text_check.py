#!/usr/bin/env python3
"""Deterministic text checks for drafts: character counts, date and weekday checks, dash checks.

Counts are made by this script, never estimated. Standard library only. Reads only the text or
file it is given and writes nothing.

Usage:
  python3 text_check.py count "Headline text"          count one string
  python3 text_check.py count -f draft.txt                count each non empty line of a file
  python3 text_check.py date 2026-10-28 [Wednesday]     weekday for a date; MATCH or MISMATCH if a weekday is given
  python3 text_check.py dashes -f draft.txt               list long dashes, short dashes and dash-like hyphens
  python3 text_check.py dashes "some text"
  (a lone argument that names a file or folder or looks like a file name, such as draft.txt, is refused: use -f for files;
   -f with no path, or a file that cannot be read, is bad input too)
  python3 text_check.py today                           today's date and weekday (UTC and local)

Exit codes: 0 = ok, 1 = a check failed (MISMATCH or dashes found), 2 = bad input.
"""
import datetime
import os
import re
import sys

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

# Characters treated as long or short dashes. Hyphen-minus inside a word is fine.
DASH_CHARS = {
    chr(0x2014): "long dash (em dash)",
    chr(0x2013): "short dash (en dash)",
    chr(0x2012): "figure dash",
    chr(0x2015): "horizontal bar",
    chr(0x2212): "minus sign used as dash",
}
SPACED_HYPHEN = re.compile(r"(?<=\S) [-] (?=\S)")
DOUBLE_HYPHEN = re.compile(r"(?<!-)-{2}(?!-)")
FILE_FLAGS = ("-f", "-" * 2 + "file")


def utf8_output():
    """Write UTF-8, so a rupee sign, a Unicode minus or a curly quote never stops the script on a Windows console or pipe
    set to code page 1252 (S2, version 1.0.2). A stream that cannot be reconfigured (a test buffer) is left as it is."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


def utf16_units(text):
    return len(text.encode("utf-16-le")) // 2


def count_one(text):
    return {
        "characters": len(text),
        "utf16_units": utf16_units(text),
        "words": len(text.split()),
        "utf8_bytes": len(text.encode("utf-8")),
    }


def fmt_count(label, text):
    c = count_one(text)
    note = ""
    if c["characters"] != c["utf16_units"]:
        note = " NOTE: some platforms count UTF-16 units; use the higher number when unsure"
    return (f"{label}: characters={c['characters']} utf16_units={c['utf16_units']} "
            f"words={c['words']} utf8_bytes={c['utf8_bytes']}{note}")


FILE_LIKE = re.compile(r"^\S+\.(txt|text|md|markdown|csv|html?|json|docx?|rtf|tex|odt|pdf)$", re.IGNORECASE)


def looks_like_file(args):
    """Run 33A: a lone argument that names an existing file, or is shaped like a text file name, was checked as the text
    "draft.txt" and passed; it is refused as bad input so a draft is never reported clean without being read."""
    return len(args) == 1 and (os.path.exists(args[0]) or bool(FILE_LIKE.match(args[0])))


class BadInput(Exception):
    """Run 33A: a file flag with no path, or a file that cannot be read, is bad input (exit 2), never a traceback or a silent pass."""


def read_source(args):
    if args and args[0] in FILE_FLAGS:
        if len(args) < 2:
            raise BadInput(f"give a path after {args[0]}")
        try:
            with open(args[1], encoding="utf-8", errors="replace") as fh:
                return fh.read(), True
        except OSError as e:
            raise BadInput(f"cannot read {args[1]!r} ({e.strerror or type(e).__name__})")
    if args:
        return " ".join(args), False
    return None, False


def bad_file_name(args):
    if looks_like_file(args):
        print(f"bad input: {args[0]!r} looks like a file name; to check a file use -f {args[0]} (a string is checked as text only)")
        return True
    return False


def cmd_count(args):
    if bad_file_name(args):
        return 2
    text, from_file = read_source(args)
    if text is None:
        print("bad input: give a string or -f PATH")
        return 2
    if from_file:
        n = 0
        for i, line in enumerate(text.splitlines(), 1):
            if line.strip():
                print(fmt_count(f"line {i}", line))
                n += 1
        print(fmt_count("whole file", text))
        return 0
    print(fmt_count("text", text))
    return 0


def cmd_date(args):
    if not args:
        print("bad input: give YYYY-MM-DD and optionally a weekday")
        return 2
    try:
        d = datetime.date.fromisoformat(args[0])
    except ValueError:
        print(f"bad input: {args[0]} is not a valid YYYY-MM-DD date")
        return 2
    actual = WEEKDAYS[d.weekday()]
    today = datetime.date.today()
    rel = "today" if d == today else ("in the past" if d < today else "in the future")
    print(f"{d.isoformat()} is a {actual.capitalize()} ({rel}; today is {today.isoformat()})")
    if len(args) >= 2:
        claimed = args[1].strip().lower()
        if claimed not in WEEKDAYS:
            print(f"bad input: {args[1]} is not a weekday name")
            return 2
        if claimed == actual:
            print("MATCH")
            return 0
        print(f"MISMATCH: the text says {claimed.capitalize()}, the date is a {actual.capitalize()}")
        return 1
    return 0


def find_dashes(text):
    hits = []
    for ln, line in enumerate(text.splitlines(), 1):
        for ch, name in DASH_CHARS.items():
            for m in re.finditer(re.escape(ch), line):
                hits.append((ln, m.start() + 1, name))
        for m in SPACED_HYPHEN.finditer(line):
            hits.append((ln, m.start() + 1, "spaced hyphen used as a dash"))
        for m in DOUBLE_HYPHEN.finditer(line):
            hits.append((ln, m.start() + 1, "double hyphen used as a dash"))
    return sorted(hits)


def cmd_dashes(args):
    if bad_file_name(args):
        return 2
    text, _ = read_source(args)
    if text is None:
        print("bad input: give a string or -f PATH")
        return 2
    hits = find_dashes(text)
    if not hits:
        print("dashes: none found")
        return 0
    for ln, col, name in hits:
        print(f"line {ln} column {col}: {name}")
    print(f"dashes: {len(hits)} found")
    return 1


def cmd_today(_args):
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_local = datetime.datetime.now().astimezone()
    print(f"UTC: {now_utc.date().isoformat()} {WEEKDAYS[now_utc.weekday()].capitalize()}")
    print(f"local ({now_local.tzname()}): {now_local.date().isoformat()} {WEEKDAYS[now_local.weekday()].capitalize()}")
    return 0


def main(argv):
    utf8_output()
    if not argv:
        print(__doc__)
        return 2
    cmd, rest = argv[0], argv[1:]
    handlers = {"count": cmd_count, "date": cmd_date, "dashes": cmd_dashes, "today": cmd_today}
    if cmd not in handlers:
        print(f"bad input: unknown command {cmd}")
        return 2
    try:
        return handlers[cmd](rest)
    except BadInput as e:
        print(f"bad input: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
