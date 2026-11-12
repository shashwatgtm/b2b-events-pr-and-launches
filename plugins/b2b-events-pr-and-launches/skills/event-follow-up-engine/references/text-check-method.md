# Text check: the method

This file sets out four fixed checks for drafts: "count" (characters, UTF-16 units, words and UTF-8 bytes), "date" (the weekday of a date, and whether the weekday in the text matches it), "dashes" (long dashes, short dashes and hyphens used as dashes) and "today" (today's date and weekday). Follow the rules exactly. When code execution is available, write your own calculation from these rules and run it; otherwise work it out by hand and say "counted by hand per the method". Either way the printed lines must match the shapes below character for character.

Counts are counted, never estimated. Nothing here is a platform limit: the limit always comes from the user, the outlet or the platform.

## Inputs

| Input | Used by | Meaning |
|---|---|---|
| mode | all | One of count, date, dashes, today. Any other mode is refused (rule T1). |
| text | count, dashes | The text to check, given directly (a headline, a subject line, a short post). |
| file | count, dashes | A saved draft to check instead of text, named after the file flag `-f` or `--file`. Use a file for anything longer than one line. |
| date | date | The date to check. |
| weekday | date | Optional. The weekday the text says for that date. |
| today | date, today | The current date on the machine where the check runs (the local calendar date). |

Give text or a file, never both. When the text and the file flag are both missing, the input is refused (rule C4).

## White space and line breaks

These two definitions are used throughout.

**White space** is any of these characters: tab (U+0009), line feed (U+000A), line tabulation (U+000B), form feed (U+000C), carriage return (U+000D), the four separators U+001C, U+001D, U+001E and U+001F, space (U+0020), next line (U+0085), no break space (U+00A0), Ogham space mark (U+1680), the spaces U+2000 to U+200A, line separator (U+2028), paragraph separator (U+2029), narrow no break space (U+202F), medium mathematical space (U+205F) and ideographic space (U+3000). The byte order mark (U+FEFF) and the zero width space (U+200B) are not white space.

**Line breaks** split a text into lines. A line break is any of: line feed (U+000A), carriage return (U+000D), carriage return followed by line feed (one break, not two), line tabulation (U+000B), form feed (U+000C), U+001C, U+001D, U+001E, next line (U+0085), line separator (U+2028) and paragraph separator (U+2029). A line break at the very end of the text does not start an extra empty line. Lines are numbered from 1, blank lines included. An empty text has no lines.

## Reading a file

1. Read the file as UTF-8. Each sequence of bytes that is not valid UTF-8 becomes one replacement character (U+FFFD). A byte order mark at the start is kept as a character (U+FEFF).
2. While reading, every carriage return followed by a line feed, and every lone carriage return, becomes a single line feed. So a file saved with Windows line ends is counted as if it had plain line feeds.
3. Anything after the file name is ignored.

## Rules for count and dashes, in this order

Stop at the first rule that refuses. A refusal is printed as one line that starts "bad input: " and nothing else is printed. The check then ends with result code 2.

| Rule | When | Printed line |
|---|---|---|
| C1. A lone file name given as text | The text was given as one single argument (one quoted string), and either it names a file or folder that exists (relative to the working folder, or as a full path), or it looks like a file name: it has no white space, has at least one character before its last dot, and ends in one of these extensions in any letter case: .txt .text .md .markdown .csv .htm .html .json .doc .docx .rtf .tex .odt .pdf (one line break at the very end is ignored for this test) | `bad input: '<text>' looks like a file name; to check a file use -f <text> (a string is checked as text only)` |
| C2. A file flag with no path | The first argument is `-f` or `--file` and nothing follows it | `bad input: give a path after <the flag as typed>` |
| C3. A file that cannot be read | The file does not exist or cannot be opened | `bad input: cannot read '<path>' (<reason>)` where the reason is the system's own text, for example "No such file or directory" for a missing file |
| C4. Nothing given | No text and no file flag | `bad input: give a string or -f PATH` |

In C1 and C3 the text or path inside the single quotes is written the way Python writes a quoted string: in single quotes, or in double quotes when it holds a single quote and no double quote, with each backslash doubled. In C1 the second copy, after "-f", is written as typed.

When the text is given as several separate arguments, they are joined with one space between each, and C1 does not apply. An empty text (an empty quoted string) is not refused: it is counted or checked as an empty text.

## Count

For a piece of text, four numbers:

| Number | How it is counted |
|---|---|
| characters | Unicode code points. A letter with a separate combining accent is 2; an emoji is 1; a flag made of two regional indicator letters is 2. |
| utf16_units | UTF-16 code units: 1 for every code point up to U+FFFF, 2 for every code point above U+FFFF (most emoji). |
| words | The number of pieces left when the text is split at every run of white space; white space at both ends is ignored. An empty text, or one of only white space, is 0 words. Punctuation stays with its word. |
| utf8_bytes | UTF-8 bytes: 1 for U+0000 to U+007F, 2 for U+0080 to U+07FF, 3 for U+0800 to U+FFFF (this includes U+FFFD and U+FEFF), 4 above U+FFFF. |

Each counted piece is printed on one line in this exact shape:

`<label>: characters=<n> utf16_units=<n> words=<n> utf8_bytes=<n>`

When characters and utf16_units differ, this is added to the end of the same line, starting with one space:

` NOTE: some platforms count UTF-16 units; use the higher number when unsure`

**Text given directly:** one line with the label `text`. Result code 0.

**A file:** after reading the file, split it into lines. For each line that has at least one character that is not white space, print one count line with the label `line <n>` (the line's number counting every line, blank ones included), counting the line without its line break. Blank lines are skipped but still numbered. Then print one count line with the label `whole file`, counting the whole text as read (line feeds included, after step 2 of reading). Result code 0.

## Dashes

Split the text (or the file as read) into lines. On each line, find every instance of the following. Columns count characters from 1 at the start of the line.

| Problem name (printed exactly) | What is found | Column reported |
|---|---|---|
| long dash (em dash) | every U+2014 | the character |
| short dash (en dash) | every U+2013 | the character |
| figure dash | every U+2012 | the character |
| horizontal bar | every U+2015 | the character |
| minus sign used as dash | every U+2212 | the character |
| spaced hyphen used as a dash | a plain space (U+0020), a hyphen (U+002D), a plain space, where the character before the first space is not white space and the character after the second space is not white space. Pattern: `(?<=\S) [-] (?=\S)` | the first space |
| double hyphen used as a dash | exactly two hyphens in a row, with no hyphen directly before them and no hyphen directly after them. Pattern: `(?<!-)-{2}(?!-)` | the first hyphen |

Notes on the spaced hyphen: only the plain space counts as the space on either side (a tab or a no break space next to the hyphen is not a match), so a hyphen at the start of a line ("- item") or after indentation ("  - item") is never a match, and nor is a hyphen at the end of a line. Matches do not overlap: the search moves on after the three characters it matched, so in "a - - b" only the first hyphen is found, at column 2. A hyphen inside a word ("follow-up") is fine. Three or more hyphens in a row are not reported.

Sort all problems by line, then by column, and print one line each:

`line <line> column <column>: <problem name>`

Then, as the last line:

| Result | Last line | Result code |
|---|---|---|
| no problems | `dashes: none found` (the only line printed) | 0 |
| one or more | `dashes: <number of problems> found` | 1 |

## Date

| Rule | When | Printed |
|---|---|---|
| D1 | No date given | `bad input: give YYYY-MM-DD and optionally a weekday` (code 2) |
| D2 | The date is not one of the accepted forms below, or is not a real calendar date | `bad input: <date as typed> is not a valid YYYY-MM-DD date` (code 2) |

Accepted forms, exactly as written, with no spaces and nothing before or after: `YYYY-MM-DD` (2026-10-28), `YYYYMMDD` (20261028), ISO week with day `YYYY-Www-D` or `YYYYWwwD` (2026-W44-3, where D is 1 for Monday to 7 for Sunday), and ISO week without a day `YYYY-Www` or `YYYYWww` (the Monday of that week). The W is a capital letter. The year runs from 0001 to 9999; the week must exist in that ISO year (2026 has a week 53, 2025 does not). So 2026-10 (no day), 2026-1-5 (one digit), 28/10/2026, 2026-02-30 and 2026-13-01 are all refused.

When the date is valid, the first line is always printed:

`<date as YYYY-MM-DD> is a <Weekday> (<when>; today is <today as YYYY-MM-DD>)`

The weekday is written with a capital first letter (Monday ... Sunday). <when> is:

`today` when the date is today, `in the past` when it is before today, `in the future` when it is after today.

Then, only when a weekday was given:

| Rule | When | Printed after the first line | Result code |
|---|---|---|---|
| D3 | The given weekday, with white space at both ends removed and in lower case, is not one of monday, tuesday, wednesday, thursday, friday, saturday, sunday (abbreviations such as "Wed" are refused) | `bad input: <weekday as typed> is not a weekday name` | 2 |
| D4 | It is the date's weekday | `MATCH` | 0 |
| D5 | It is another weekday | `MISMATCH: the text says <Given weekday>, the date is a <Actual weekday>` (both with a capital first letter) | 1 |

With no weekday, only the first line is printed and the result code is 0. Anything given after the weekday is ignored.

## Today

Print two lines, then result code 0:

| Line | Exact shape |
|---|---|
| 1 | `UTC: <today's date in UTC as YYYY-MM-DD> <Weekday>` |
| 2 | `local (<the machine's local time zone name>): <today's local date as YYYY-MM-DD> <Weekday>` |

The two dates differ when it is already the next day in one of them. Without code execution, write today's date as the conversation gives it and say it was not checked by a clock.

## Any other mode

`bad input: unknown command <mode as typed>` (code 2). With no mode at all, nothing is checked: ask which check is wanted.

## Worked examples

Each was run against these rules; the printed lines are exact.

**Count, text given directly.** Text: `Launch day`, a space, then two rocket emoji (U+1F680 twice). 13 characters ("Launch" 6, space 1, "day" 3, space 1, emoji 2), 15 UTF-16 units (each emoji is 2), 3 words ("Launch", "day" and the two emoji together), 19 UTF-8 bytes (11 plus 4 for each emoji).

`text: characters=13 utf16_units=15 words=3 utf8_bytes=19 NOTE: some platforms count UTF-16 units; use the higher number when unsure`

**Count, a file with Windows line ends.** The file holds "Headline one", "Subheadline two words here", an empty line and "Last line with a tab<TAB>here", each ended by a carriage return and line feed:

| Line | Text |
|---|---|
| 1 | `line 1: characters=12 utf16_units=12 words=2 utf8_bytes=12` |
| 2 | `line 2: characters=26 utf16_units=26 words=4 utf8_bytes=26` |
| 3 | `line 4: characters=25 utf16_units=25 words=6 utf8_bytes=25` |
| 4 | `whole file: characters=67 utf16_units=67 words=12 utf8_bytes=67` |

The whole file is 67 characters because each of the 4 line ends counts as one line feed (63 characters of text plus 4).

**Dashes, a file.** Line 1 is `Event plan <U+2013> Q4`, line 6 is `Spaced - hyphen and another - one`, line 7 is `Double--hyphen, triple---hyphen, quad----hyphen`, line 8 is `a - - b and x -- y`. The printed lines for those four lines are:

| Text |
|---|
| `line 1 column 12: short dash (en dash)` |
| `line 6 column 7: spaced hyphen used as a dash` |
| `line 6 column 28: spaced hyphen used as a dash` |
| `line 7 column 7: double hyphen used as a dash` |
| `line 8 column 2: spaced hyphen used as a dash` |
| `line 8 column 15: double hyphen used as a dash` |
| `dashes: 6 found` |

In line 8, " -- " is a double hyphen only (the character after the first hyphen is a hyphen, not a space), and the second hyphen of "a - - b" is not found because the first match used the space before it.

**Date.** Today 2026-11-12, date 2026-10-28, weekday Tuesday:

| Line | Text |
|---|---|
| 1 | `2026-10-28 is a Wednesday (in the past; today is 2026-11-12)` |
| 2 | `MISMATCH: the text says Tuesday, the date is a Wednesday` |

Result code 1. With the weekday Wednesday the second line is `MATCH` and the code is 0; with the weekday "Wed" it is `bad input: Wed is not a weekday name` and the code is 2.

**Refusal.** Text `draft.txt` given directly: `bad input: 'draft.txt' looks like a file name; to check a file use -f draft.txt (a string is checked as text only)`.

## Results in short

| Mode | Result code | Meaning |
|---|---|---|
| any | 2, a "bad input: " line | The input was refused; pass the line on as written and ask for what is missing (for a draft, check the saved file with -f). |
| count | 0 | Counts printed; compare them with the limit the user, outlet or platform gives. |
| date | 0 | MATCH, or no weekday given. |
| date | 1 | MISMATCH: correct the weekday or the date, never both by guess; ask. |
| dashes | 0 | No dashes found. |
| dashes | 1 | Fix every line listed and check again. |
| today | 0 | Today's date in UTC and locally. |
