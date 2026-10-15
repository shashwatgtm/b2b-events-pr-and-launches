# The shared event process (applies to every event type)

Every figure in this file is a field the user fills ("[User to add: ...]"). Timings are suggested defaults, written as "a common choice is ..., you decide"; they are never rules. Stage names (for example marketing qualified lead, sales accepted lead, opportunity) are the user's own: ask for them and use them exactly.

## 1. Plan backwards from the sales target
Events exist to deliver a share of the sales target, so the plan starts there and works back.

| Step | Field | How it is decided |
|---|---|---|
| 1 | Sales target for the period, in the user's own stage (for example qualified leads accepted by sales, opportunities or pipeline value) | [User to add: target, period, region] |
| 2 | Accounts needed to reach it | [User to add: from the user's own win and conversion history] |
| 3 | Share of the target events must deliver | [User to add: agreed with sales] |
| 4 | Split between new accounts and existing accounts | [User to add] |
| 5 | Contacts needed per event type | Worked back from step 3 and the user's own conversion rates (step 6), by script |
| 6 | Conversion from contact to the first qualified stage, and from that stage to the stage sales accepts | [User to add: from the user's past events; if there is no history, say so and mark the plan as a first test] |
| 7 | Cost per qualified lead the user can accept | [User to add: agreed with finance or sales] |

Run `scripts/plan_math.py` on the user's figures; never do the arithmetic by estimate. If a figure is missing, the script names it and leaves every value that depends on it out.

## 2. The event portfolio table
One row per event type the user is considering. All values start blank.

| Type of event | Total events | Contacts per event | Total contacts reached | Relevant target group (share of contacts in the target group) | Old accounts | New accounts | Cost per event | Total cost |
|---|---|---|---|---|---|---|---|---|
| [User to add] | [User to add] | [User to add] | by script | [User to add] | [User to add] | [User to add] | [User to add] | by script |

A second table runs each type through the funnel:

| Type of event | Contacts | Conversion to first qualified stage | Total at first qualified stage | Conversion to sales accepted stage | Total sales accepted | Cost per sales accepted lead |
|---|---|---|---|---|---|---|
| [User to add] | by script | [User to add] | by script | [User to add] | by script | by script |

The method's portfolio used four broad kinds of event: large format events run by others, a custom national event the company hosts, custom regional breakfast or evening events, and webinars. In that experience, large format events had the lowest share of relevant attendees and the lowest conversion, and small custom regional formats had a fully relevant audience and the highest conversion. Treat this as a pattern to test against the user's own history, not as a fact about their market.

## 3. The core group and roles
- A marketing owner, a lead generation owner and inside sales own each contact from the event to the first qualified stage, and follow up with sales until it is accepted. Once sales accepts it, it passes to the lead generation or sales owner for closure, and the core group's responsibility for that lead ends. The lead generation owner updates the core group on closures at a cadence the user sets [User to add].
- Leaders attend as speaker, panelist or visitor, for networking.
- Sales members attend for high quality networking and say which contacts have the potential to become accepted leads.
- Roles are named by role, never by a person the user has not named.

## 4. The timeline (pre, during, post)
Every timing below is a suggested default. Write each one as "a common choice is ..., you decide" and put the user's decision in the plan. Check every resulting date and weekday with `scripts/text_check.py date YYYY-MM-DD Weekday`.

### Pre event
| Task | Owner | Suggested default (you decide) |
|---|---|---|
| Target list: segmented by enterprise or mid market, and existing or new target companies; refreshed every quarter | Marketing owner | a common choice is to refresh it each quarter, you decide |
| Invite emails, web banners, content synopsis and the post event drip, all written | Marketing owner | a common choice is three to four weeks before the event, you decide |
| Presentation and panel content final | Speaker and marketing owner | a common choice is one week before, you decide |
| Session material to the organiser for their check, when they ask for it: what will actually be shown (the exact prompts or inputs and the unedited outputs), with no scores or summaries of the speaker's own | Speaker | [User to add: the date it goes to them] |
| Meetings fixed in advance with target contacts | Core group | a common choice is to have them fixed two days before, you decide |
| Mock run of the presentation or panel | Speakers | a common choice is a mock run two to three days before; you decide whether and when |
| Account based outreach on LinkedIn to the final invitee list | Marketing owner | a common choice is to start three days before and continue for three working days after, you decide |

### During the event
- Debrief: collect every meeting note against a fixed set of debrief questions about the buyer's current process [User to add: the debrief questions]. A common choice is the same day; you decide.
- Marketing writes personalised notes on the panel discussion so that people can be tagged in a meaningful way later (only people the post is about).
- Live social: real posts, the right people tagged, the user's hashtags. The number of posts per person is the user's choice [User to add].

### Post event
| Task | Owner | Suggested default (you decide) |
|---|---|---|
| Personal email to everyone met, drafted before the event | The person who met them | a common choice is to have drafts ready a week before and send within 48 hours of the event, you decide |
| First call | The contact's owner | a common choice is within 72 hours, you decide |
| Drip to registrants or the organiser's list who were not met | Marketing owner | a common choice is within four working days, you decide |
| Meetings held | Core group and sales | a common choice is within ten working days, you decide; the number of meetings is [User to add] |
| Pipeline review with sales | Core group and sales | a common choice is fifteen working days after, you decide |
| Hand over to nurture | Marketing owner | a common choice is thirty days after, with the nurture drip from forty five days, you decide |

From the hand over, the follow-up journeys, scoring, consent and nurture emails belong to the event-follow-up-engine skill. Hand off with the event name, date, the list source and the owners; do not design the journeys here.

## 5. Event type by sales stage
| Sales stage or job | Event types | What it is for | Measure (fields) |
|---|---|---|---|
| Discovery, before qualification | Webinar, own event, industry event | New contacts in prospect companies, or new companies; a wider industry audience | [User to add: new contacts, new accounts] |
| Early opportunity | Breakfast or workshop | Deeper engagement with senior buyers | [User to add: senior buyers with a workshop or deep discussion] |
| Educating the people who advise the buyer | Event, webinar, PR | Reach the advisers one level below the decision maker | [User to add: audience reached, meetings arranged, accepted leads after a quarter] |
| Stalled deals or lapsed relationships | Event, webinar | Revive existing relationships | [User to add: share of the funnel revived] |
| Customer education and training | Sales webinar | Teach users and buyers | [User to add] |

## 6. The post event audit: one owner per contact
- Log every event contact with its owner, lead stage, last activity and flags.
- One owner per contact. If two people from the company contact the same person, flag it as a conflict: it damages the company's image.
- No generic lead generation mail after a personal one. If a contact received a personal note from the person they met, the generic follow-up for the list is stopped for that contact, so the personal note is taken seriously.
- Report the conflicts to the core group with the fix (who keeps the contact, what the other person stops).

## 7. Common mistakes (from the method)
- Planning events from the calendar of shows instead of from the sales target.
- Debriefs collected days later, so meeting notes are lost.
- Two people writing to the same contact, or a generic mail landing after a personal one.
- Follow-up emails written after the event instead of before it.
- No mock run before a panel or presentation.
