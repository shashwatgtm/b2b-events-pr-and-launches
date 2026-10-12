# Audit mode: reviewing a requirements or design document

Use when the user brings a requirements document, a design document, a specification or a workshop output for an event follow-up or nurture programme and wants it checked.

## 1. Before auditing
- Read the whole document. If any part cannot be read (an image, a broken table, a locked file), say which part and stop short of judging it.
- Find the locked decisions: the decisions the user's team has already agreed (meeting notes, a decision log, an earlier signed off version). If there is no list, ask for it; without it, the audit can only check internal consistency, and the output says so.
- When two versions exist, the newer locked decision wins over the older document; say so in the audit.

## 2. Table of contents first
Start the output with the document's table of contents as it is, then the audit's own contents. If the document has none, build one from its headings and say it was built.

## 3. Business context before technology
Before any finding about fields, journeys or integrations, write one short section on the business context the document assumes: the events in scope, the goal of follow-up, who the buyers are, which accounts count, who in sales receives what. If the document does not state these, the first findings are the missing business questions, for example:
- what happened before, during and after recent events, and what each event format is meant to achieve;
- why some lead sources are left out of the first phase;
- the ideal customer and account definition;
- who decides when a lead goes to sales.

## 4. The issue table
| # | Where (section, page) | What the document says | Locked decision it conflicts with, or the gap | Why it matters to the business | Suggested fix | Bucket |
|---|---|---|---|---|---|---|
- Tabulate every issue, however many there are. Do not trim the list to look tidy.
- Bucket each issue: immediate attention, low hanging fruit, longer term. The user sets the time boundary for each bucket; ask if it is not given.
- "Don't over engineer, if there are no inconsistencies then say truthfully, don't manufacture issues." If nothing conflicts, the output says "No inconsistencies found against the locked decisions" and lists what was checked.

## 5. Keep design and specification apart
The design document explains why and what (goals, flows, choices). The specification says exactly how (fields, rules, triggers, values). If the document mixes them, the audit recommends splitting them and lists which sections belong where. Diagrams stay plain, like those people draw, not decorative.

## 6. Ask before assuming a system is broken
If the document or the user hints that a system or connector is not working, ask what was seen (error, missing records, wrong values) and when. List the evidence that would confirm it. Never plan around a broken system on a guess.

## 7. Platform roles
A marketing automation platform runs nurture, scoring and email. It is not the CRM of record and not an account based advertising platform. If the document gives it those jobs, raise it as an issue.

## 8. Sequencing
Check what the pilot tries to do first. Account based work usually needs the basics (clean data, the account gate, scoring, hand-off to sales) working first; ask the user where it sits rather than assuming.

## 9. Test list
Count first ("12 tests"), then each test in one or two lines:
| # | Test name | What it checks |
|---|---|---|
Realistic tests only: each must be runnable on the user's platform with real or test records, and each checks one business rule or one data rule. No tests for features the pilot does not include.

## 10. Output order
1. Table of contents.
2. Business context (or the missing business questions).
3. The issue table, or the honest "no inconsistencies" result with what was checked.
4. Design and specification split recommendation, if needed.
5. Test list.
6. Open questions for the user, in one block.
