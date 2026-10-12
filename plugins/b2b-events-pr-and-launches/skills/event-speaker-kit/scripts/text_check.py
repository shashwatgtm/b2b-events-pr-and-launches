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
  python3 text_check.py today                           today's date and weekday (UTC and local)

Exit codes: 0 = ok, 1 = a check failed (MISMATCH or dashes found), 2 = bad input.
"""
import datetime
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


def read_source(args):
    if len(args) >= 2 and args[0] in FILE_FLAGS:
        with open(args[1], encoding="utf-8", errors="replace") as fh:
            return fh.read(), True
    if args:
        return " ".join(args), False
    return None, False


def cmd_count(args):
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
    if not argv:
        print(__doc__)
        return 2
    cmd, rest = argv[0], argv[1:]
    handlers = {"count": cmd_count, "date": cmd_date, "dashes": cmd_dashes, "today": cmd_today}
    if cmd not in handlers:
        print(f"bad input: unknown command {cmd}")
        return 2
    return handlers[cmd](rest)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
