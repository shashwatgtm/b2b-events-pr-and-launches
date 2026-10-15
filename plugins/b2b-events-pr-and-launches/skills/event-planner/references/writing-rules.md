# Writing rules for any text written for a reader

Apply these to everything this skill drafts for someone else to read: releases, posts, articles, emails, speaker lines, briefs. Working material for the user (a claims register, a run of show table, a specification) may use tables and bullets; the word and dash rules still apply.

## Voice
- Plain spoken English, peer to peer. Written from inside the problem by someone who has done the work, not from above it.
- Calm and grounded. No guru tone, no hype, no sudden excitement or despair.
- Anchor in a specific moment, decision, test or tension that the user's material supports. Never invent a scene, a dialogue, an anecdote or a feeling to supply one.
- Set the reading level by the audience and ask when it is unclear. Default: understandable by a reader with secondary school education or more, without talking down to a graduate reader.
- Keep the user's own raw lines when they carry the point. Edit for accuracy and these rules, not to polish away their voice.

## Format for reader-facing prose
- Prose paragraphs of one to four sentences. In posts, no bullets, no bold, no headers, no Unicode bold, no emoji numbers, no arrows, no checkmarks.
- No emoji anywhere unless the user asks for them in their own text, and then only theirs.
- No exclamation marks in published text.
- On LinkedIn, no links in the post body: links go in a comment. Two to three hashtags mixing one broad and the rest niche, never more than five. Tag a person or company only when the post is about them or quotes them.
- Count characters by script, never by estimate.
- Names in public copy: an internal code name, working label or draft name never appears in a launch asset. One product, tool or method keeps one name across every asset. A named method or framework is explained in one plain sentence where it first appears, or replaced by plain words.

## Punctuation
- No long dashes (em dashes) and no short dashes (en dashes). No spaced hyphen or double hyphen used as a dash. Hyphens inside words are fine. Use a comma, a colon, a full stop or the word "to" for ranges.
- Run `scripts/text_check.py dashes -f FILE` on every draft before showing it (save the draft to a file first; a file name given without -f is refused as bad input). If the script cannot run, say so and check by eye, line by line.

## Banned words and phrases
game-changer, game-changing, leverage, dive in, dive deep, delve, landscape (allowed only as a domain modifier, such as "competitive landscape"), tapestry, elevate, elevated, unlock, seamless, seamlessly, landed hard, resonated, struck a chord, genuine unlock, genuinely, honestly, straightforward, revolutionize, supercharge, harness, empower, navigate (for abstract things), in today's world, in the ever-evolving landscape, take your X to the next level, it's important to note, testament to, the rise of, keep coming back to, sat with me, rubric (say "scoring method"), move the needle, here's the thing, groundbreaking, revolutionary, transformative, comprehensive, robust, dynamic, holistic, synergy, paradigm shift, next-level, mechanics, "just" used as filler, and "thought leader" applied to oneself.

Stock openers are banned: "Humbled to share", "Thrilled to announce", "Excited to share", "We are delighted", "Big news".

A word on this list may appear only when it is part of a quote, a product name or a proper noun the user supplied.

## Banned patterns
- Staccato fragments of one to three words ("No code. No fuss. Shipped.").
- Label fragments used as sentences ("Short runs.").
- "First... Second... Third..." enumeration inside prose.
- The contrast formula "It was not X. It was Y." or "That's not X. That's Y."
- Neat punchlines, aphorisms and invented coined labels.
- Hyperbole and superlatives without a source ("first", "only", "leading", "best").
- Lazy "start on Monday" closing lines.
- Essay-style openers that begin with context, news, a trend or an abstract principle.
- Claims written in the first person for someone who has not said them.

## Final check before showing any draft
1. Every fact traces to the user's material, a fetched page or a named source, or it is a placeholder.
2. The dash script found nothing (or each hit is inside a quoted source and marked).
3. No banned word or pattern.
4. Counts were run by script for every line that has a limit.
5. Dates and weekdays were checked by script.
