# Spec mode: the event follow-up pilot specification

Structure only. Every weight, threshold, stage rule, timing and benchmark is the user's. Where the user has not given one, the spec shows "[User to set: ...]" and a short note on how to decide it from their own data or their sales agreement. The skill never proposes a number.

## Sections, in this order

### 1. What this pilot proves, and what it does not
- Proves: one to three statements the pilot will show with evidence by its end (for example "event attendees from accounts that pass the account gate reach a sales conversation through this journey").
- What we are not doing: everything left out on purpose, each with a reason (time, data, platform, team). Over-ambitious items go here.
- Suggested default, shown as a common choice the user decides on, never as a rule: account based marketing comes last in a pilot (first prove the import, consent, fit gate and one journey; add account based plays after), so it usually sits under "what we are not doing" for the first pilot. Ask the user; if they want it in, it goes in.
- Pilot window: [User to set: start and end dates]. Only what can be built and measured inside the window is in scope.
- Pilot sequence: lock the rules, build, run on a small cohort, then tune. The cohort and the length of each phase: [User to set].
- What the pilot measures, in six groups: account quality, data quality, engagement, progression through the user's stages, sales feedback and outcome. Each with the user's measure and target [User to set].

### 2. Since the last draft (change log)
| Date | What changed | Who asked | Why |
|---|---|---|---|
Record every change the user made by hand before extending the spec. Work on the user's edited version, never on an older copy.

### 3. Cards on the table (assumptions register)
| # | Assumption | Status | Owner | Needed by |
|---|---|---|---|---|
Status labels: Confirmed; Need from you; Unconfirmed; A hypothesis; Don't have it. "None of this gets hard-coded until you confirm it. If we guessed, we said so."

### 4. Who owns each gate
The flow, in this order: event import; consent and dedupe; account fit; active customer check; persona path; the user's lifecycle stages; recycle and learn.
| Gate | Owner (role) | Decision rule | On pass | On fail | Where it is recorded |
|---|---|---|---|---|---|

### 5. The account gate comes before the person
"Pick the account first. Pick the words second."
Before the account gate: import the event list, then consent and dedupe. Duplicates are merged into one record, and contacts without the consent the user's rules require stop here.
Fit decides whether a person ever enters the engine.
1. Account question: does the account fit the user's ideal customer definition? If not, it does not enter nurture. [User to set: the account definition and data source.]
2. Is the account an active customer? Active customers go to their account owner, not into nurture. [User to set: where customer status lives.]
3. Person question: is this person someone the user wants to reach (role, function, region)? [User to set: the person criteria.]
The account question and the person question are scored and recorded separately.
4. Persona path: each person who passes follows the path for their persona. The personas are the user's own; a starting shape the user can change is technical, economic, procurement and referral. Each persona has its own proof and its own ask. [User to set: the personas and how a person is assigned to one.]

### 6. Engagement scoring
- Score clicks, visits and downloads (and other actions the user tracks, such as attending a session, booking a meeting, replying).
- Opens alone never make a contact engaged. If the user wants opens in the score, they stay minor and capped by the user's own rule, and the spec says why.
- Two axes: fit (from the gate) and engagement (from actions).
- Every weight, cap, decay and threshold: [User to set: ...], decided from the user's own past conversions or agreed with sales.
- A cap stated "per score" is per score, not a total; write which.

### 7. Lifecycle stages
The stage names, order and definitions are the user's own. Write them exactly as the user defines them. If two documents order them differently, show both and ask; never hard-code either and never state that one order is used everywhere.
| Stage (user's name) | Entry rule | Exit rule | Owner |
|---|---|---|---|

### 8. Early warning stage
A stage before hand-off that tells the account owner an account is warming, so sales is not surprised. Entry rule: [User to set]. What the account owner sees and does: [User to set].

### 9. Journeys
- Channels are timed, not sprayed: each journey names its channels and its order; timings are [User to set].
- Each journey is capped (a maximum number of touches, set by the user) and ends with a clear last message.
- Disqualification is a hard block, not a cool-down: disqualified contacts leave all journeys.
- Recycle with a reason and a date: every contact that leaves a journey without converting gets a recycle reason from a fixed list and a date to re-enter or to be reviewed. [User to set: the reason list and the dates.]
- Touch types in order, a starting shape the user changes: a thank you with a recap and one asset; a connection request with context and no link; an insight; a proof; a point of view; a meeting ask from sales only if the contact is engaged; a closing message. After the closing message a contact comes back in only on a fresh signal. The timing of every touch, including how soon the first touch goes after the event, is [User to set], decided before the event.
- No mailing into silence: when a contact has not engaged across the touches the user sets, the journey ends (with its closing message, if the user keeps one) and the contact is recycled instead of being mailed again.
- No-shows get their own journey [User to set: touches]. If a no-show engages, they merge into the attendee journey at the equivalent stage, so they are never double-mailed.
- The live event call to action ends when the event closes: no touch sent after the event asks people to visit the stand or join the session.
- One owner per contact: a contact who received a personal message from the person they met gets no generic journey mail on top of it, and two people never write to the same contact.
- The ask per signal: a table of which next step is asked for which signal, so the ask matches what the contact did.
| Signal (the user's) | Next step asked | Who asks |
|---|---|---|
| [User to set] | [User to set] | [User to set] |

### 10. One coordinated account play
When two or more people from the same account are active, stop treating them as separate leads and run one coordinated play for the account: one owner, one message plan, one hand-off. [User to set: what counts as "active" and how many people trigger it.]

### 11. Hygiene journeys
Separate journeys to clean the data: disqualified leads, dormant records, addresses from restricted regions, competitor addresses, bounced or unsubscribed contacts. Each with its rule [User to set] and its owner.

### 12. Prove it on one real account
Walk one real account from the user's last event through every gate, score, stage and journey in the spec, with the user's real data (or anonymised by the user). Every value used is the user's. The walk-through ends with a register: real, assumed, to confirm.

### 13. Close these before we build
The list of open items that block the build, each with an owner and a date.

### 14. Test list
Count first, then each test as name and what it checks in one or two lines; realistic tests only (see audit-mode.md section 9).

### 15. Build handoff
A paste-ready brief for the platform admin (handoff-brief.md). The skill does not build, import or change anything in a marketing platform or CRM.

## Discovery questions (ask in one message, only what the record does not answer)
- Which events and formats are in scope, and what each is meant to achieve?
- What happened in follow-up after recent events (before, during, after)?
- Which lead sources are out of the first phase, and why?
- The ideal customer and account definition, and the source of account data.
- The lifecycle stage definitions and who owns each hand-off.
- The pilot window and the team that will build and run it.
- Which platforms hold what (marketing automation, CRM, event platform), read only for this work.

## Sector notes (vocabulary only, no figures)
- Logistics tech events: shippers, carriers, brokers; buying roles in transportation, logistics and supply chain operations; accounts often have several sites.
- Fintech events: banks, lenders, issuers, merchants; buying roles in technology, risk, compliance and product; regulated communications rules may apply.
- Telecom events: operators and large enterprises; buying roles in network planning, operations and procurement; long programmes with tenders.
Ask the user to confirm the buying roles for their accounts; never add a statistic for the sector without a source.
