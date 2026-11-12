# Plan arithmetic: the method

This file sets out two fixed calculations on the user's own figures: "portfolio" (each event type run through the funnel, then compared with the share of the target events must deliver) and "needed" (one event type worked backwards: the contacts and events needed for a number of accepted leads). Follow the rules exactly. When code execution is available, write your own calculation from these rules and run it; otherwise work it out by hand and say "counted by hand per the method". Either way the printed lines must match the shapes below character for character.

The method never supplies a figure. Every input comes from the user; a missing input is reported as "[User to add: ...]" and every value that depends on it is left out. All percentages are written 0 to 100. If the user's conversion rates are measured on all contacts, use a relevant share of 100.

## Part 1. Checking one figure

Both calculations check each figure the same way, in this order. The first rule that fails refuses the whole input with one line, `bad input: <message>`, and nothing else is printed (result code 2). <where> and <field> are given in Parts 2 and 3.

| Order | Figure | Message |
|---|---|---|
| 1 | Not given (absent, or null in the plan) | Not a refusal: the figure is missing. |
| 2 | true or false, text, a list or an object | `<where> <field> must be a number, got <value>` |
| 3 | A whole number written with digits only that is too large for a double precision number (about 1.8e308 or more) | `<where> <field> is too large to compute; check the figure` |
| 4 | Not a finite number (NaN, Infinity, -Infinity, or a written number so large that it becomes Infinity, such as 1e400) | `<where> <field> must be a finite number, got <nan, inf or -inf>` |
| 5 | Above 0 but below 2.2250738585072014e-308 (the smallest normal double) | `<where> <field> is too small to compute; check the figure` |
| 6 | Below 0 (minus zero, -0, is not below 0) | `<where> <field> must not be negative` |
| 7 | A percentage field above 100 | `<where> <field> is a percentage and must be 0 to 100` |

The percentage fields are relevant_share, first_stage_rate, accepted_rate and event_share. Other fields (events, contacts per event, cost per event, the target, the accepted leads wanted) have no upper limit.

<value> in rule 2 is written the way Python writes the value: text in single quotes ('four', or in double quotes when it holds a single quote and no double quote), true and false as True and False, null as None, a list as [1, 2], an object as {'name': 'Roundtable'}.

Every figure that passes is used as a double precision floating point number. All arithmetic below is double precision, in exactly the order written ("a x b / 100" means multiply a by b, then divide by 100).

## Part 2. Number formatting

| Kind | Rule | Examples |
|---|---|---|
| Not computed | The text `not computed` | |
| Money (total cost, cost per accepted, blended cost) | Two decimals, a comma every three digits in the whole part | 24000 is `24,000.00`; 1666.666... is `1,666.67` |
| Any other value | If the value is close to a whole number, the whole number with a comma every three digits; otherwise one decimal with a comma every three digits | 1200 is `1,200`; 14.4 is `14.4`; 0.01 is `0.0` |

"Close to a whole number": take the nearest whole number (an exact half goes to the even one) and compare. The value counts as whole when the distance is at most the larger of 0.000000001 and one billionth (0.000000001 times) of the larger of the two absolute values. So 66.00000000000001 is `66`, 0.01 is not whole and is shown `0.0`, and a large value such as 1234567890.5 counts as whole (its tolerance is about 1.23) and is shown as `1,234,567,890`, the even neighbour.

Rounding to two decimals or one decimal is done on the exact double value: a value exactly halfway goes to the even last digit (0.125 shows as `0.12`, 0.0625 as `0.06`, 0.25 to one decimal as `0.2`). A value that is a decimal halfway point when written by hand, such as 3 x 999.995 = 2999.985, is stored as a double slightly above or below the halfway point, and is rounded from that stored value (2999.985 computed this way shows as `2,999.99`). Without code execution, round half up and say the cents may differ by one from a computed result.

## Part 3. Portfolio

### Inputs

A plan, as JSON (from a saved PLAN.json file, or the user's figures written in that shape):

| Key | Meaning |
|---|---|
| target | Sales target in the user's accepted stage, for the period. |
| event_share | Share of that target events must deliver, percent. |
| types | A list with one object per event type: name, events, contacts_per_event, relevant_share, first_stage_rate, accepted_rate, cost_per_event. |

Other keys are ignored. The JSON may write NaN, Infinity and -Infinity; they are refused by Part 1 rule 4.

### Rules, in this order

Stop at the first rule that refuses. A refusal is one line starting "bad input: " (result code 2).

| Rule | When | Printed line |
|---|---|---|
| P1 | Not exactly one plan file named | `bad input: give one PLAN.json path` |
| P2 | The file cannot be read, is not UTF-8, or is not valid JSON | `bad input: cannot read <path>: <reason>`, where the reason is the reader's own text; for a missing file it is `[Errno 2] No such file or directory: '<path>'` |
| P3 | A number in the file has a decimal point or an exponent, reads as 0, but has a digit 1 to 9 before any "e" or "E" (for example 1e-400 or -2.5E-500) | `bad input: the plan holds <the number as written>, a number too small to compute; check the figure` |
| P4 | The plan is not an object, or it has no "types" key, or "types" is not a list, or the list is empty | `bad input: the plan needs a non empty "types" list` |
| P5 | Check target (<where> is `plan`, <field> is `target`), then event_share (`plan`, `event_share`), by Part 1 | per Part 1 |
| P6 | Then each row of types, in order. A row that is not an object | `bad input: types row <n> must be an object with a name and the funnel figures, got <row written as in Part 1>` (n counts from 1) |
| P7 | Otherwise check the row's figures by Part 1 in this order: events, contacts_per_event, relevant_share, first_stage_rate, accepted_rate, cost_per_event. <where> is the row's name, <field> the key as written (with underscores) | per Part 1 |
| P8 | Work out the row (below). If any computed value of the row is not finite | `bad input: <name>: a result is too large to compute; check the figures` |
| P9 | After all rows: if the sum of accepted leads of the rows that have it, the sum of total cost of the rows that have it, or target x event_share / 100 is not finite | `bad input: plan: a result is too large to compute; check the figures` |

The row's name is its "name" value written as text; when the name is absent, null, empty, false or 0, the name is `unnamed type`. A number used as a name is written as Python writes it (2026 stays 2026).

P2 to P3: the file is read in one pass, so whichever problem comes first in the file decides the message. P3 does not apply to whole numbers written without a decimal point or exponent, or to numbers written as zero (0.0, 0e5).

### Each row

Missing figures are noted in this order: events, contacts per event, relevant share, first stage rate, accepted rate, cost per event, each as `[User to add: <name> <field with spaces for underscores>]`, for example `[User to add: Roundtable cost per event]`.

| Value | Formula | Not computed when |
|---|---|---|
| total contacts | events x contacts_per_event | either is missing |
| relevant contacts | total contacts x relevant_share / 100 | either is missing |
| first stage | relevant contacts x first_stage_rate / 100 | either is missing |
| accepted | first stage x accepted_rate / 100 | either is missing |
| total cost | events x cost_per_event | either is missing |
| cost per accepted | total cost / accepted | total cost or accepted is missing, or accepted is exactly 0 |

When total cost and accepted are both computed and accepted is exactly 0, cost per accepted is not computed and the row gets this note: `no accepted leads on these figures, so cost per accepted lead cannot be computed`.

Because of the order of operations, a very large product (events x contacts_per_event x relevant_share, before the division by 100) can become Infinity even when the result divided by 100 would fit; that is refused by P8.

### The totals

| Total | Formula | Not computed when |
|---|---|---|
| planned | the accepted values of all rows added in row order | any row's accepted is not computed |
| cost | the total costs of all rows added in row order | any row's total cost is not computed |
| blended | cost / planned | either is not computed, or planned is 0 (the line is then left out entirely) |
| needed | target x event_share / 100 | target or event_share is missing |
| gap | needed minus planned | needed or planned is not computed (the line is then left out) |

Missing target adds `[User to add: sales target in your accepted stage]` and missing event_share adds `[User to add: share of the target events must deliver]`, after all the rows' missing fields.

### Printed output

Line by line:

| Line | Exact shape | When |
|---|---|---|
| 1 | `Formulas: relevant contacts = events x contacts per event x relevant share; accepted = relevant x first stage rate x accepted rate; cost per accepted = total cost / accepted` | Always |
| 2 | `\| Type \| Total contacts \| Relevant contacts \| First stage \| Accepted \| Total cost \| Cost per accepted \|` | Always |
| 3 | `\|---\|---\|---\|---\|---\|---\|---\|` | Always |
| one per row | `\| <name> \| <total contacts> \| <relevant contacts> \| <first stage> \| <accepted> \| <total cost, money> \| <cost per accepted, money> \|` | In row order |
| after a row with a note | `note for <name>: no accepted leads on these figures, so cost per accepted lead cannot be computed` | Directly after that row |
| next | `Planned accepted leads from events: <planned>` | Always |
| next | `Total event cost: <cost, money>` | Always |
| next | `Blended cost per accepted lead: <blended, money>` | Only when cost and planned are computed and planned is above 0 |
| next | `Needed from events (target x event share): <needed>` | Always |
| next | `Gap: <gap> accepted leads short of the share events must deliver` | When gap is computed and above 0.000000001 |
| or | `Gap: none; the plan covers the share by <planned minus needed>` | When gap is computed and 0.000000001 or less |
| next | `Missing fields (values that depend on them were not computed):` | When anything is missing |
| one per missing field | two spaces, then the field, for example `  [User to add: Roundtable cost per event]` | In the order above |

(The backslashes before the bars in this table only escape them in Markdown; the printed lines have plain bars and no backslashes.)

Result code 0 when nothing is missing, 1 when anything is missing (the values that could be computed are still printed).

### Worked portfolio

Target 400, event_share 25. Rows: Roundtable (6 events, 12 contacts per event, relevant 90, first stage 50, accepted 60, cost 5,500), Trade show booth (2, 300, 40, 20, 50, 42,000), Webinar (10, 120, 60, 10, 40, 1,500).

Roundtable: 6 x 12 = 72 contacts; 72 x 90 / 100 = 64.8 relevant; 64.8 x 50 / 100 = 32.4 first stage; 32.4 x 60 / 100 = 19.44 accepted, shown `19.4`; cost 6 x 5,500 = 33,000; 33,000 / 19.44 = 1,697.53. Planned is 19.44 + 24 + 28.8 = 72.24, needed 400 x 25 / 100 = 100, gap 27.76.

| Line | Text |
|---|---|
| 1 | `Formulas: relevant contacts = events x contacts per event x relevant share; accepted = relevant x first stage rate x accepted rate; cost per accepted = total cost / accepted` |
| 2 | `\| Type \| Total contacts \| Relevant contacts \| First stage \| Accepted \| Total cost \| Cost per accepted \|` |
| 3 | `\|---\|---\|---\|---\|---\|---\|---\|` |
| 4 | `\| Roundtable \| 72 \| 64.8 \| 32.4 \| 19.4 \| 33,000.00 \| 1,697.53 \|` |
| 5 | `\| Trade show booth \| 600 \| 240 \| 48 \| 24 \| 84,000.00 \| 3,500.00 \|` |
| 6 | `\| Webinar \| 1,200 \| 720 \| 72 \| 28.8 \| 15,000.00 \| 520.83 \|` |
| 7 | `Planned accepted leads from events: 72.2` |
| 8 | `Total event cost: 132,000.00` |
| 9 | `Blended cost per accepted lead: 1,827.24` |
| 10 | `Needed from events (target x event share): 100` |
| 11 | `Gap: 27.8 accepted leads short of the share events must deliver` |

Result code 0. If the Webinar row had no cost_per_event, its total cost and cost per accepted would be `not computed`, line 8 would be `Total event cost: not computed`, line 9 would be left out, and the output would end with `Missing fields (values that depend on them were not computed):` and `  [User to add: Webinar cost per event]`, result code 1.

A row with 1 event of 20 contacts, relevant 100, first stage 0, accepted 50, cost 15,000 prints `\| Analyst day \| 20 \| 20 \| 0 \| 0 \| 15,000.00 \| not computed \|`, then `note for Analyst day: no accepted leads on these figures, so cost per accepted lead cannot be computed`.

## Part 4. Needed

### Inputs

The user's figures as name=value pairs:

| Name | Field (used in messages) | Meaning |
|---|---|---|
| accepted | accepted | Accepted leads wanted from this event type. |
| first-rate | first_stage_rate | First stage rate, percent. |
| accepted-rate | accepted_rate | Accepted rate, percent. |
| relevant | relevant_share | Relevant share, percent. |
| contacts-per-event | contacts_per_event | Contacts per event. |

### Rules, in this order

Stop at the first rule that refuses (one "bad input: " line, result code 2).

| Rule | When | Printed line |
|---|---|---|
| N1 | Going through the pairs in order: a pair with no "=", or with nothing before the first "=" | `bad input: expected name=value, got '<pair as written>'` |
| N2 | In the same pass: the value (everything after the first "=") is not a number | `bad input: <name> must be a number, got '<value as written>'` |
| N3 | In the same pass: the value reads as 0 but has a digit 1 to 9 before any "e" or "E" (such as 1e-400) | `bad input: <name> is too small to compute; check the figure` |
| N4 | After the pass: a name not in the table above (the first such name, in order of first appearance) | `bad input: unknown name <name>` |
| N5 | Check each figure by Part 1, in order of first appearance of its name; <where> is `needed`, <field> is from the table | per Part 1, for example `bad input: needed first_stage_rate must not be negative` |
| N6 | Any of the five is missing | `Missing fields; nothing computed:` then one line per missing figure, in the table's order, each two spaces then `[User to add: <field with spaces for underscores>]` (result code 1, not 2) |
| N7 | accepted is 0 | Not a refusal: every needed value is 0 and the events needed is 0 (skip N8 to N10) |
| N8 | Otherwise, the first of first_stage_rate, accepted_rate, relevant_share, contacts_per_event (in that order) that is 0 | `bad input: <field with spaces> is 0, so no number of events can reach the target` |
| N9 | A worked value below is not finite | `bad input: needed: a result is too large to compute; check the figures` |
| N10 | The events needed works out to 0 | `bad input: needed: the accepted target is too small to compute; check the figures` |

A value is a number when, after white space at both ends is removed, it is an optional + or - sign followed by digits with an optional decimal point and an optional exponent (e or E, an optional sign, digits); single underscores between digits are allowed (1_000 is 1000, 1__000 is not a number); or it is inf, infinity or nan in any letter case, with an optional sign. An empty value is not a number. When a name is given twice, the later value is used, and the name keeps the position of its first appearance.

### Working backwards

| Value | Formula |
|---|---|
| first stage needed | accepted / (accepted_rate / 100) |
| relevant needed | first stage needed / (first_stage_rate / 100) |
| contacts needed | relevant needed / (relevant_share / 100) |
| events | contacts needed / contacts_per_event |
| events needed | events rounded to 9 decimal places (an exact half to even), then rounded up to the next whole number (a whole number stays as it is) |

Rounding to 9 decimal places first means floating point noise such as 10.000000000000002 gives 10 events, not 11; a real excess such as 1.00000001 events still rounds up to 2.

### Printed output

| Line | Exact shape |
|---|---|
| 1 | `Formulas: first stage needed = accepted / accepted rate; relevant needed = first stage / first stage rate; contacts needed = relevant / relevant share; events needed = contacts / contacts per event, rounded up` |
| 2 | `First stage leads needed: <first stage needed>` |
| 3 | `Relevant contacts needed: <relevant needed>` |
| 4 | `Total contacts needed: <contacts needed>` |
| 5 | `Events needed (rounded up): <events needed>` |

Lines 2 to 4 use the "any other value" format of Part 2. Line 5 is the whole number in plain digits with no thousands separator (11905, not 11,905). Result code 0.

### Worked needed

accepted=1500, first-rate=2.5, accepted-rate=12, relevant=35, contacts-per-event=120. First stage needed 1500 / 0.12 = 12,500; relevant needed 12,500 / 0.025 = 500,000; contacts needed 500,000 / 0.35 = 1,428,571.43; events 11,904.76, rounded up to 11905.

| Line | Text |
|---|---|
| 1 | `Formulas: first stage needed = accepted / accepted rate; relevant needed = first stage / first stage rate; contacts needed = relevant / relevant share; events needed = contacts / contacts per event, rounded up` |
| 2 | `First stage leads needed: 12,500` |
| 3 | `Relevant contacts needed: 500,000` |
| 4 | `Total contacts needed: 1,428,571.4` |
| 5 | `Events needed (rounded up): 11905` |

With accepted=0 the four lines read `0`, `0`, `0` and `0`. With first-rate=0 and accepted=10 the only line is `bad input: first stage rate is 0, so no number of events can reach the target`. With contacts-per-event missing, the lines are `Missing fields; nothing computed:` and `  [User to add: contacts per event]`, result code 1.

## Results in short

| Result code | Meaning |
|---|---|
| 0 | Complete: copy the table or lines exactly into the answer, labelled "by a fixed method, your figures". |
| 1 | Computed with missing fields: show what was computed, list the fields, and ask the user for them; never estimate them. |
| 2 | Bad input: show the line as written, ask the user for the right figure or row, and never correct it by guess. |

Any mode other than portfolio or needed is refused with `bad input: unknown command <mode as typed>`.
