# Comprehension gate and handoff brief

## A. Yes or No comprehension gate (before any build brief or spec draft)
Restate the job in three to five lines: the events in scope, the goal, the mode (audit or spec), what the output will be, and what it will not include. Keep the user's own words in the restatement; anything you add (the goal, what the output will include) goes inside [Draft for you to confirm: ...]. Then ask exactly:

"Have I understood the requirement? Please reply Yes or No. If No, tell me what to change."

Do not start the build brief until the user says Yes. If the user already said Yes earlier in the conversation for the same job, show the restatement and continue. A rushed or frustrated user still gets this one line; it is the only question asked.

The spec, the audit and the nurture emails the user asked for (1.0.5) come in the same answer, in full, under the gate line and marked "draft; depends on your Yes; redone if No", in every case: never hold them back until the user replies, because a gate with nothing under it leaves the user with nothing to react to. Every weight, threshold and timing in them stays the user's or a [User to set: ...] placeholder. The build brief for a platform admin always waits for an explicit Yes, in every case.

## B. Paste-ready handoff brief
Use when the conversation is long, when the user asks to continue elsewhere, or when the spec goes to a platform admin or another person.

Format (plain text the user can paste):
1. Job: one line.
2. Mode: audit or spec.
3. Locked decisions: numbered, in the user's words.
4. The user's own edits so far: every change the user made, by section.
5. Current state: which sections are done, which are drafts.
6. Open items: each with owner and date.
7. Values still to set: every "[User to set: ...]" placeholder listed.
8. Next step: one line.
9. Rules for whoever continues: structure only, no invented values; the lifecycle order is the user's; never write to a marketing platform without the user's admin; ask before assuming a system is broken.

Keep it short enough to paste in one message. Do not lose any locked decision or user edit; if something must be cut for length, cut explanation, never decisions.

## C. Build checklist for the platform admin (when the user asks)
A list the admin works through in the user's own platform: each item names the section of the spec it comes from, what to configure, and the test from the test list that proves it. The skill never configures, imports or changes anything itself.
