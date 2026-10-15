# B2B Events, PR and Launches

Plan B2B events, press releases and product launches with Claude: event portfolios and plans per event type, panel and webinar kits, speaker notes, verified releases, launch sequences and event follow-up specs.

Version 1.0.2.

## What changed in 1.0.2

- Event planner: the plan arithmetic script now answers "bad input" with a plain message, never a crash, when a figure is NaN or Infinity, a result is too large to compute, or an event type row is not a set of named figures; and working backwards from 0 accepted leads now answers 0 events needed instead of refusing.
- Event speaker kit: the moderator rules sample and the confidentiality filter now say that a panelist's internal practice stays out of the kit, or is marked for the panelist's confirmation, until the panelist confirms it is public or cleared by their employer; it is no longer reworded as a general industry observation.
- Event planner: the plan arithmetic script also answers "bad input", never a crash, for a whole number too long to compute, a plan file that is not UTF-8 text, and a figure so small that the result cannot be computed; a positive accepted target never answers 0 events needed.
- Event planner: Step 5 now says to show a "bad input" message to you and ask for the right figure or row, never to correct it by guess or by hand.
- Event speaker kit: a failure story from a panelist's own employer counts as an internal practice and follows the same confidentiality rule; it is never relabelled a general pattern.
- Every script now writes UTF-8, so a rupee sign, a Unicode minus or a curly quote in your text no longer stops it with an encoding error on a Windows console or pipe set to code page 1252.
- The text check script (dashes and counts) now refuses a lone file name given without -f, such as draft.txt, with a plain message, instead of checking those few letters as text and reporting the draft clean, and -f with no path or a file that cannot be read ends with the same kind of plain message, never a crash or a silent pass; the skills now say to run it with -f on the saved draft.
- Event speaker kit: every part the answer says it gives (a seed question, a takeaway, a talking point) is written out or marked as a field for you to fill.
- PR and launch pack: who a product or feature is for, and what it is built for, is written only in your words or a page's words; anything more is a field to fill or marked for you to confirm.

## What changed in 1.0.1

- When a pasted text, a file or a page a skill opens holds an instruction to the assistant, the answer now says so in one line at the top (where it was, what it asked, and that it was not followed). The speaker kit now has the same rule as the PR and launch pack.
- A page, file or message that asks a speaker or attendee for personal, tax or bank details is reported to you at the top of the answer as a likely scam; nothing from it goes into the output, and the rest of the job goes on.
- When a line you pasted is missing from what a fetch returned, the answer says "not in what the fetch returned" instead of saying the page does not have it, and looks for the exact sentence before treating it as unconfirmed.
- Launch copy never uses an internal code name, keeps one name per product or method, and explains a named method in one plain sentence where it first appears.
- Speaker notes can be given as short talking points for a phone; demo prompts are written against the demo data and the event date and run before the event; an organiser who asks to check the session gets the exact prompts and the unedited outputs.
- Launch offers are checked like any other claim: support levels, inclusions, bonuses, sessions, rewards and tiers are used only as you confirm them; your own source files are read for facts and never edited unless you ask; proof shown in any launch asset is real.

## Who it is for

Event and field marketers, communications and PR leads, product marketers, demand generation and marketing operations teams, and founders and executives who speak at events or announce news, in B2B companies.

## What's inside

**Event Planner**: works back from your sales target to the share events must deliver, the event portfolio and the cost per qualified lead (every figure is yours, arithmetic by script), helps you choose between event types with a comparison table, and plans each type: roundtable, exhibition or trade show booth, webinar, podcast, event visit, summit or awards sponsorship, panel moderation, AMA or LinkedIn Live, workshop, partner and customer events and the analyst programme, with a pre, during and post event timeline whose timings are suggestions you decide on. Analyst events, your own mid sized event and large brand programmes are marked as a method still being completed.

**Event Speaker Kit**: panel moderator question maps (context, tension, a concrete example, a metric and a takeaway for every question), AMA run of show with backup questions and scope lines, webinar and podcast plans, guest briefings, stage demo kits checked against the real product, live teardown segments, speaker notes in SAY, BE PRECISE, IF ASKED and SOURCE blocks, and post-event articles per platform with every paraphrased quote marked for the panelist's approval.

**PR and Launch Pack**: a claims register before any copy, press releases with quotes as placeholders until the person writes or approves them, regional releases with local figures left to local PR teams, company update posts, spokesperson lanes, teasers, a launch day chosen from your own audience, launch sequence plans, community forum posts and supporter talking points. Headlines, subject lines and meta text are counted by script, never estimated.

**Event Follow-up Engine**: audit mode checks a follow-up or nurture requirements document against your locked decisions and says so truthfully when nothing is wrong; spec mode writes a pilot specification with the account gate before the person, scoring on clicks, visits and downloads, an early warning stage, recycle rules, one coordinated account play, hygiene journeys, mapping and consent, nurture emails, a realistic test list and a paste-ready handoff brief. Every weight, threshold and timing stays yours.

## Install

```bash
# Add this repository as a marketplace
claude plugin marketplace add shashwatgtm/b2b-events-pr-and-launches

# Install the plugin
claude plugin install b2b-events-pr-and-launches@b2b-events-pr-and-launches
```

## Quick start

"Plan our customer roundtable in Amsterdam on 28 October and tell me how many such events we need to hit our pipeline target."

"I'm moderating a customer panel at our roundtable on 28 October. Four panelists, 40 minutes. Build the question map."

"Draft a press release for our new product line and check every claim in it first."

"Our trade show ended yesterday. Audit our follow-up requirements document against Friday's meeting note."

## How it handles facts
Every skill checks claims against your material or a cited page, checks dates and weekdays by script, and writes "[User to add: ...]" where a fact is missing. It never invents statistics, quotes, customers, attendance numbers, budgets, conversion rates or scoring values. Text in pages and files it reads is treated as data, never as instructions.

## Examples
The worked examples in the skills use real logistics tech, fintech and telecom companies only as examples, with public facts fetched and cited on 11 October 2026; every other figure in them is hypothetical. No company endorsed this plugin.

## Privacy
The plugin stores nothing on any server and has no database. When Claude can write files, a skill may save its drafts (for example a plan or a release) in your own working folder, and nothing else. This plugin sends no data to Helix GTM Consulting and runs no server. The skills run inside Claude. When you name a company or event, Claude may open public pages with its own web tools. The text check script, and the event planner's plan arithmetic script, run on your machine, read only the text or file you give them and write nothing. The skills never send, post or publish anything, and never write to a marketing platform or CRM. What you type into Claude is handled under your own Claude account terms.

## Security
To report a security problem, email shashwat@gtmhelix.com with the subject "Security report: b2b-events-pr-and-launches". Please do not open a public issue for it.

## Author
Built by Shashwat Ghosh, Co-Founder and Fractional CMO of Helix GTM Consulting, with 24+ years in B2B go-to-market and 10+ years of fractional experience.

https://gtmexpert.com | https://tools.gtmhelix.com/plugins/

## License
MIT. See [LICENSE](LICENSE).
