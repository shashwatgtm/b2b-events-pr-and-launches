# Claim verification before writing

Run this before any release, post, teaser, forum post or award entry is drafted. The register goes to the user with the draft.

## 1. List every claim
Every statement that could be true or false: product capabilities, customer names and counts, partner names, figures (users, countries, transactions, growth, savings), awards, firsts and superlatives, dates, prices, quotes, and statements about competitors or the market. Every claim, not a sample.

## 2. The claims register
| # | Claim as written | Source | Source date | Status | Risk | Action |
|---|---|---|---|---|---|---|
Status is one of:
- Verified: a source opened in this session (a fetched page or a connector result) states it, in the same unit, region and period, and the source is one the user accepts.
- As pasted, not yet checked: the only source is text or a file the user pasted or attached; the claim matches it, but no source was opened in this session. Never called Verified.
- User to confirm: the user's own fact that no public source shows (internal numbers, unreleased features). Kept only after the user confirms, and phrased as the company's own statement.
- Unverified: no source found. Removed from the copy, or kept as "[User to add: source for ...]".
- Contradicted: a source says otherwise. Removed, and the conflict shown to the user.
Risk is High for superlatives, firsts, competitor statements, customer names, and figures in headlines; Medium for other figures; Low for descriptive statements the company's own page makes.

## 3. Source order
1. Sources the user names. They beat the skill's own search. If a named source cannot be opened, say so and leave the cell blank; never fill it from elsewhere without telling the user.
2. The company's own primary pages: its press releases, filings, investor relations pages, annual reports, product documentation.
3. Reputed news and business publications that report the fact directly.
Never use: anonymous posts, content farms, AI generated comparison pages, paid placements, or a search snippet as the source of a claim. When a page cannot be opened, a snippet from a search for its wording may be shown beside the claim, labelled "from a search result; the page itself was not opened", and the claim stays Unverified.

## 4. Rules for specific claim types
- Superlatives and firsts ("first", "only", "leading", "largest", "best"): High risk. Keep only with a source that states it in the same scope; otherwise rewrite to say what the product does.
- A claim is only as strong as its source: if two of three customers did something, say two of three, not "customers".
- A result needs a baseline: "three times more leads" with no starting point and period is not a claim; ask for the baseline or remove it.
- Prospects are not customers or partners. A pilot is not a deployment. Use the stage the user confirms.
- Inflated numbers: if a figure looks larger than the source supports, use the source's figure and tell the user why.
- Customer and partner names need their approval for a release; mark "[Customer approval needed]".
- Third party statistics: label region, sample and period; if they do not match the audience of the release, say so.
- Scale lines in boilerplate (countries, customers, users): check the date of the page they come from; if older than the user's own latest figures, ask.
- Tools and AI: say truthfully which tool does what; never claim a product does something a different tool does.

## 5. Date check on every output
- Run `scripts/text_check.py today` and `scripts/text_check.py date YYYY-MM-DD Weekday` for every dateline, embargo date, launch date and event date.
- Check the year: a release dated this year must not carry last year.
- Embargo times always carry a time zone.

## 6. Without web access
Say plainly that outside claims could not be checked in this session. Check only what the pasted material proves, and mark those claims "As pasted, not yet checked". Mark everything else "Unverified" in the register. Never write "verified" or "all links checked" unless each page was opened in this session.
