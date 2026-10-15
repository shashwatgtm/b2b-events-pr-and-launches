#!/usr/bin/env python3
"""Event plan arithmetic from the user's own figures. Standard library only.

The script never supplies a figure. Every input comes from the user; a missing input is
reported as "[User to add: ...]" and every value that depends on it is left out. It reads
only the file or arguments it is given and writes nothing.

Usage:
  python3 plan_math.py portfolio PLAN.json
      Runs each event type through the funnel and compares the result with the share of
      the target events must deliver.
  python3 plan_math.py needed accepted=N first-rate=P accepted-rate=P relevant=P contacts-per-event=N
      Works one event type backwards: contacts and events needed for N accepted leads.

PLAN.json (all percentages are 0 to 100; every key is the user's figure):
  {
    "target": 0,                 sales target in the user's accepted stage, for the period
    "event_share": 0,            share of that target events must deliver, percent
    "types": [
      {"name": "Roundtable", "events": 0, "contacts_per_event": 0, "relevant_share": 0,
       "first_stage_rate": 0, "accepted_rate": 0, "cost_per_event": 0}
    ]
  }

Formulas (stated in the output too):
  total contacts      = events x contacts per event
  relevant contacts   = total contacts x relevant share
  first stage leads   = relevant contacts x first stage rate
  accepted leads      = first stage leads x accepted rate
  total cost          = events x cost per event
  cost per accepted   = total cost / accepted leads
  needed from events  = target x event share
If the user's conversion rates are measured on all contacts, enter a relevant share of 100.

Bad input (exit 2, never a traceback): a value that is not a number, a negative value, a
percentage over 100, a number that is not finite (NaN, Infinity), too large or too small to compute,
a "types" row that is not an object, and a plan file that is not UTF-8 JSON. needed with accepted=0 answers 0 events
needed; a rate of 0 with a positive accepted target is refused.

Exit codes: 0 = complete, 1 = computed with missing fields reported, 2 = bad input.
"""
import json
import math
import sys

TYPE_FIELDS = ["events", "contacts_per_event", "relevant_share", "first_stage_rate",
               "accepted_rate", "cost_per_event"]
PERCENT_FIELDS = {"relevant_share", "first_stage_rate", "accepted_rate", "event_share"}


def utf8_output():
    """Write UTF-8, so a rupee sign, a Unicode minus or a curly quote never stops the script on a Windows console or pipe
    set to code page 1252 (S2, version 1.0.2). A stream that cannot be reconfigured (a test buffer) is left as it is."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


class BadInput(Exception):
    pass


def number(value, field, where):
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise BadInput(f"{where} {field} must be a number, got {value!r}")
    try:
        finite_value = math.isfinite(value)
    except OverflowError:   # an integer too large for a float
        raise BadInput(f"{where} {field} is too large to compute; check the figure")
    if not finite_value:
        raise BadInput(f"{where} {field} must be a finite number, got {value!r}")
    if 0 < value < sys.float_info.min:   # too small to compute: results would underflow to 0
        raise BadInput(f"{where} {field} is too small to compute; check the figure")
    if value < 0:
        raise BadInput(f"{where} {field} must not be negative")
    if field in PERCENT_FIELDS and value > 100:
        raise BadInput(f"{where} {field} is a percentage and must be 0 to 100")
    return float(value)


def fmt(x, money=False):
    if x is None:
        return "not computed"
    if money:
        return f"{x:,.2f}"
    return f"{int(round(x)):,}" if math.isclose(x, round(x), abs_tol=1e-9) else f"{x:,.1f}"


def finite(values, where):
    for x in values:
        if x is not None and not math.isfinite(x):
            raise BadInput(f"{where}: a result is too large to compute; check the figures")


def run_type(t, missing, n=1):
    if not isinstance(t, dict):
        raise BadInput(f"types row {n} must be an object with a name and the funnel figures, got {t!r}")
    name = t.get("name") or "unnamed type"
    v = {f: number(t.get(f), f, name) for f in TYPE_FIELDS}
    for f in TYPE_FIELDS:
        if v[f] is None:
            missing.append(f"[User to add: {name} {f.replace('_', ' ')}]")
    r = {"name": name}

    def mul(a, b, pct=False):
        if a is None or b is None:
            return None
        return a * b / 100.0 if pct else a * b

    r["total_contacts"] = mul(v["events"], v["contacts_per_event"])
    r["relevant_contacts"] = mul(r["total_contacts"], v["relevant_share"], pct=True)
    r["first_stage"] = mul(r["relevant_contacts"], v["first_stage_rate"], pct=True)
    r["accepted"] = mul(r["first_stage"], v["accepted_rate"], pct=True)
    r["total_cost"] = mul(v["events"], v["cost_per_event"])
    if r["total_cost"] is None or r["accepted"] is None:
        r["cost_per_accepted"] = None
    elif r["accepted"] == 0:
        r["cost_per_accepted"] = None
        r["note"] = "no accepted leads on these figures, so cost per accepted lead cannot be computed"
    else:
        r["cost_per_accepted"] = r["total_cost"] / r["accepted"]
    finite([r[k] for k in r if k not in ("name", "note")], name)
    return r


def cmd_portfolio(args):
    if len(args) != 1:
        print("bad input: give one PLAN.json path")
        return 2
    try:
        with open(args[0], encoding="utf-8") as fh:
            plan = json.load(fh, parse_float=_plan_float)
    except (OSError, json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"bad input: cannot read {args[0]}: {e}")
        return 2
    except BadInput as e:
        print(f"bad input: {e}")
        return 2
    if not isinstance(plan, dict) or not isinstance(plan.get("types"), list) or not plan["types"]:
        print("bad input: the plan needs a non empty \"types\" list")
        return 2
    missing = []
    try:
        target = number(plan.get("target"), "target", "plan")
        share = number(plan.get("event_share"), "event_share", "plan")
        rows = [run_type(t, missing, n) for n, t in enumerate(plan["types"], 1)]
        sums = [sum(r["accepted"] for r in rows if r["accepted"] is not None), sum(r["total_cost"] for r in rows if r["total_cost"] is not None)]
        finite(sums + [target * share / 100.0 if target is not None and share is not None else None], "plan")
    except BadInput as e:
        print(f"bad input: {e}")
        return 2
    if target is None:
        missing.append("[User to add: sales target in your accepted stage]")
    if share is None:
        missing.append("[User to add: share of the target events must deliver]")

    print("Formulas: relevant contacts = events x contacts per event x relevant share; "
          "accepted = relevant x first stage rate x accepted rate; cost per accepted = total cost / accepted")
    print("| Type | Total contacts | Relevant contacts | First stage | Accepted | Total cost | Cost per accepted |")
    print("|---|---|---|---|---|---|---|")
    for r in rows:
        print(f"| {r['name']} | {fmt(r['total_contacts'])} | {fmt(r['relevant_contacts'])} | "
              f"{fmt(r['first_stage'])} | {fmt(r['accepted'])} | {fmt(r['total_cost'], True)} | "
              f"{fmt(r['cost_per_accepted'], True)} |")
        if r.get("note"):
            print(f"note for {r['name']}: {r['note']}")

    complete = [r for r in rows if r["accepted"] is not None]
    planned = sum(r["accepted"] for r in complete) if len(complete) == len(rows) else None
    cost = sum(r["total_cost"] for r in rows) if all(r["total_cost"] is not None for r in rows) else None
    print(f"Planned accepted leads from events: {fmt(planned)}")
    print(f"Total event cost: {fmt(cost, True)}")
    if planned is not None and cost is not None and planned > 0:
        print(f"Blended cost per accepted lead: {fmt(cost / planned, True)}")
    needed = target * share / 100.0 if target is not None and share is not None else None
    print(f"Needed from events (target x event share): {fmt(needed)}")
    if needed is not None and planned is not None:
        gap = math.fsum([needed, -planned])
        if gap > 1e-9:
            print(f"Gap: {fmt(gap)} accepted leads short of the share events must deliver")
        else:
            print(f"Gap: none; the plan covers the share by {fmt(-gap)}")
    if missing:
        print("Missing fields (values that depend on them were not computed):")
        for m in missing:
            print(f"  {m}")
        return 1
    return 0


def _written_non_zero(text):
    """True when a number is written with a non zero digit before any exponent (1e-400 is written non zero but reads as 0.0)."""
    mantissa = text.strip().lower().split("e")[0]
    return any(c in "123456789" for c in mantissa)


def _plan_float(text):
    value = float(text)
    if value == 0 and _written_non_zero(text):
        raise BadInput(f"the plan holds {text}, a number too small to compute; check the figure")
    return value


def parse_flags(args):
    out = {}
    for arg in args:
        key, sep, value = arg.partition("=")
        if not sep or not key:
            raise BadInput(f"expected name=value, got {arg!r}")
        try:
            out[key] = float(value)
        except ValueError:
            raise BadInput(f"{key} must be a number, got {value!r}")
        if out[key] == 0 and _written_non_zero(value):
            raise BadInput(f"{key} is too small to compute; check the figure")
    return out


def cmd_needed(args):
    try:
        f = parse_flags(args)
        names = {"accepted": "accepted", "first-rate": "first_stage_rate",
                 "accepted-rate": "accepted_rate", "relevant": "relevant_share",
                 "contacts-per-event": "contacts_per_event"}
        unknown = [k for k in f if k not in names]
        if unknown:
            raise BadInput(f"unknown name {unknown[0]}")
        v = {names[k]: number(val, names[k], "needed") for k, val in f.items()}
    except BadInput as e:
        print(f"bad input: {e}")
        return 2
    missing = [f"[User to add: {k.replace('_', ' ')}]" for k in
               ["accepted", "first_stage_rate", "accepted_rate", "relevant_share", "contacts_per_event"]
               if v.get(k) is None]
    if missing:
        print("Missing fields; nothing computed:")
        for m in missing:
            print(f"  {m}")
        return 1
    if v["accepted"] == 0:
        first_needed = relevant_needed = contacts_needed = 0.0   # no accepted leads needed, so nothing to divide
        events_needed = 0
    else:
        for k in ["first_stage_rate", "accepted_rate", "relevant_share", "contacts_per_event"]:
            if v[k] == 0:
                print(f"bad input: {k.replace('_', ' ')} is 0, so no number of events can reach the target")
                return 2
        first_needed = v["accepted"] / (v["accepted_rate"] / 100.0)
        relevant_needed = first_needed / (v["first_stage_rate"] / 100.0)
        contacts_needed = relevant_needed / (v["relevant_share"] / 100.0)
        events = contacts_needed / v["contacts_per_event"]
        if not all(math.isfinite(x) for x in (first_needed, relevant_needed, contacts_needed, events)):
            print("bad input: needed: a result is too large to compute; check the figures")
            return 2
        events_needed = math.ceil(round(events, 9))
        if events_needed == 0:   # a positive target never needs 0 events; the figures are too small to compute
            print("bad input: needed: the accepted target is too small to compute; check the figures")
            return 2
    print("Formulas: first stage needed = accepted / accepted rate; relevant needed = first stage / first stage rate; "
          "contacts needed = relevant / relevant share; events needed = contacts / contacts per event, rounded up")
    print(f"First stage leads needed: {fmt(first_needed)}")
    print(f"Relevant contacts needed: {fmt(relevant_needed)}")
    print(f"Total contacts needed: {fmt(contacts_needed)}")
    print(f"Events needed (rounded up): {events_needed}")
    return 0


def main(argv):
    utf8_output()
    if not argv:
        print(__doc__)
        return 2
    cmd, rest = argv[0], argv[1:]
    handlers = {"portfolio": cmd_portfolio, "needed": cmd_needed}
    if cmd not in handlers:
        print(f"bad input: unknown command {cmd}")
        return 2
    return handlers[cmd](rest)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
