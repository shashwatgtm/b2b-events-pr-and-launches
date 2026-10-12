# Mapping and consent

Always in this order. Do not jump to the field table before the plain words are agreed.

## 1. Plain words
A short description anyone on the team can read: where the event data comes from (registration form, badge scans, session check-ins, meeting notes), what happens to it, who sees it, and where it ends up. If the user says it is too complicated, rewrite it simpler before moving on.

## 2. Field mapping
| Source (system and field as the user names it) | Meaning in plain words | Destination (system and field as the user names it) | Transformation | Required or optional | Owner |
|---|---|---|---|---|---|
Field names are the user's own. The skill never invents field names; if a name is not given, "[User to add: field name in <system>]".

## 3. Cell references
When the mapping lives in a spreadsheet the user shares, point to the exact sheet, column and row for each mapping line, so the admin can find it. If no sheet is shared, skip this step and say so.

## 4. Consent and data rules (as bullets)
- The lawful basis or consent for each region the attendees come from: [User and legal to confirm]. The skill does not decide legal questions; it lists the questions for the user's counsel.
- What the registration form told attendees about follow-up, quoted from the form if the user shares it.
- Opt-out handling: where an unsubscribe is recorded and how fast it reaches every system (the user's rule).
- Data retention: how long event data is kept and where (the user's rule).
- Restricted regions and competitor addresses: excluded from journeys, rule set by the user.
- Sensitive data: never collect or move data the follow-up does not need.
- Email authentication and deliverability prerequisites (for example sender domain authentication) to confirm with the platform admin: only the ones the user's setup needs.

## 5. Check before the build
The user confirms the plain words, the mapping and the consent bullets, then the comprehension gate (handoff-brief.md) runs before any build brief is written.
