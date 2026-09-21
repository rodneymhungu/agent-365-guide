# Plan: 2,000 high-value weekly visitors

This file is the plan of record for growing the Agent 365 field guide. It is
written for three readers: Rodney, anyone who finds the repository, and any
agent that picks up the work. If you are an agent, read this file first, then
the section "How an agent picks this up" at the bottom.

Started 21 September 2026. Reviewed every Monday alongside the weekly digest.

## Where Rodney left off, 21 September 2026

Read this first when you come back. Everything below the line was done on
21 September; these are the things that were still open when you left.

1. **GoatCounter token (blocks all measurement).** Sign in to
   rodneymhungu.goatcounter.com, Settings, API tokens, create a read-only
   "statistics" token. In this repository: Settings, Secrets and variables,
   Actions, update `GOATCOUNTER_TOKEN`. Then Actions, "Weekly feedback
   digest", Run workflow. The new digest should show visitors and referrers
   instead of "Action needed". About five minutes.
2. **Brave Search key (optional, issue #10).** Free key at
   brave.com/search/api, saved as `BRAVE_API_KEY` in the same place. The
   digest then reports public mentions.
3. **Field guide principles repository.** `Dev/field-guide-principles` has
   uncommitted edits from 9 September (field notes describe real events,
   distinct products stay distinct) plus today's amendment of "one HTML
   file" to "one page per topic, one data file". Review, commit, push.
4. **Next rotation focus is 4, distribution.** One LinkedIn post linking a
   section (`licensing.html` or `#s4-1`, not the home page), one session
   follow-up, one account outreach. Log each here with the link and the
   referrer to expect.
5. **Writing review.** The `ai-writing-review` skill is now installed for
   Claude Code; run it on the next prose change and decide each flag.

## Target

2,000 high-value visitors a week to
[rodneymhungu.github.io/agent-365-guide](https://rodneymhungu.github.io/agent-365-guide/).

High-value means the reader is a security, identity, compliance or endpoint
engineer who runs Entra, Purview, Defender or Intune, or the person who buys
Agent 365 for them. The proxy signals are the referrer (a Microsoft tenant,
Teams, LinkedIn, a search query that names Agent 365, Entra Agent ID, Purview
or Defender), the sections opened (anything in chapters 5 to 10 counts;
bouncing off the hero does not), and public mentions found by the digest.

Measured by GoatCounter, reported every Monday in the digest issue labelled
`digest`. The digest states visitors against this target and names the
week's focus.

## Where we are

| Week of | Visitors (7 days) | Top referrers | Notes |
|---|---|---|---|
| 31 August 2026 | 1 | direct | Baseline. Guide published 4 September. |
| 7 September 2026 | not measured | not measured | GoatCounter returned HTTP 404 to the digest. Token needs re-creating. |
| 14 September 2026 | not measured | not measured | Drift pull request #16 sat unmerged for a week. Nothing shipped. |
| 21 September 2026 | not measured | not measured | Catch-up week: focus 1, 2 and 3 all shipped, see log. Analytics still blocked on the token; the 21 September digest (#19) says so under Action needed. |

## The weekly rotation

One focus a week, in this order, then repeat. Catch-up weeks may do more
than one. The digest names the current focus so nobody has to count.

| # | Focus | What "done" looks like |
|---|---|---|
| 1 | Split a section into its own indexable page | A new `*.html` at the repository root with its own title, description, canonical link and JSON-LD, listed in `sitemap.xml`, linked from the section it came from, rendering status from `a365-data.js`. |
| 2 | Build or extend a lookup table | A table a reader can scan in ten seconds: licence, preview against GA, control to scenario. Every row sourced at the point of use; status rendered from the data block, never typed. |
| 3 | Write the changed-this-week note | Merge the open `learn-drift` pull request, then add one entry to `changes` in `a365-data.js` that says what moved and links the Learn page. If nothing drifted, say so in the digest and skip. |
| 4 | Distribution | One LinkedIn post that links a section, not the home page. One follow-up to a session or workshop audience. One account or partner outreach. Record each in the log with the link and the referrer to expect. |

Every week, whatever the focus: check GoatCounter referrers, not just paths.
A path tells you what people read. A referrer tells you who sent them and
whether they are the reader this guide is for.

## Blockers that only Rodney can clear

1. **GoatCounter token.** The digest on 14 September got HTTP 404 "not found".
   An unknown token returns 401 "unknown token", so this is not a missing
   secret. Re-create a read-only "statistics" token while signed in to
   rodneymhungu.goatcounter.com (Settings, API tokens), then update the
   `GOATCOUNTER_TOKEN` repository secret and run the digest workflow by
   hand from the Actions tab. If it still fails, check that the token was
   made on the site that serves `/agent-365-guide`, not a second site.
2. **Brave Search key.** Issue #10. Optional, but without it the digest
   never sees public mentions, which is the only distribution feedback loop
   that does not depend on the referrer.

## Log

Newest first. One line per item shipped, with the pull request.

| Date | Focus | Shipped | Evidence |
|---|---|---|---|
| 21 September 2026 | Skim pass | "In a hurry?" line under the hero actions pointing at 4.1, 9 and 10. Four dense paragraphs became tables or a list: purchase prerequisites (2.1), roles by task (2.3), the three Global Secure Access features (5.5), the four Entra Agent ID objects (7.1). Stale worktree copy removed. Brave key surfaced under Action needed in the digest. | #23 |
| 21 September 2026 | 2 | Chapter 4 gains a scenario-to-control table (4.1): fifteen scenarios, each landing on the control, the enforcing product, a status badge rendered from the data, and the section to read. GA only hides the rows you cannot deploy yet. | #22 |
| 21 September 2026 | 1 | Chapter 2 published as its own page, `licensing.html`, with its own title, description, canonical link, card and JSON-LD, listed in the sitemap. Data, styles and behaviour moved to shared files so both pages render from one data object. A build check keeps the two copies identical. | #20 |
| 21 September 2026 | Plan | Tracking issue #21 opened and pinned so the plan is the first thing on the repository page. | #21 |
| 21 September 2026 | 3 | Merged the 14 September drift pull request: Local agents page now detects twenty-three tools and can block some of them. Changelog entry rendered in chapter 10. | #16 |
| 21 September 2026 | Plumbing | Drift pull requests and digest issues are now assigned to Rodney and mention him, so GitHub emails and notifies on every one. The digest lists any drift pull request older than two days, states visitors against the target, and names the week's focus. The previous digest issue is closed when a new one opens. | this pull request |
| 21 September 2026 | Plumbing | This plan written. `.gitattributes` added so Windows and OneDrive stop turning every file into a line-ending diff. | this pull request |

## How an agent picks this up

1. Read this file. Then read the latest issue labelled `digest` and any open
   pull request labelled `learn-drift`.
2. If a drift pull request is open, review it first. The guide's value is
   that every claim traces to Learn; a stale page is worse than a quiet week.
   Merge it if the edit is verified against the Learn page it cites, then log
   the change under focus 3.
3. Take the focus the digest names, or the next one in the rotation table
   after the last logged entry. Do that one thing to "done" as defined above.
4. Add a row to the log with the pull request number. Update "Where we are"
   with the visitor count and referrers from the digest.
5. Never put a token or key in this repository. It is public. Secrets live
   in repository settings and are read by the workflows as environment
   variables; see `scripts/README.md`.
6. Prose follows the [field guide principles](https://github.com/rodneymhungu/field-guide-principles):
   UK spelling, no em or en dashes, status from data, source at the point of
   use, opinion only in numbered field notes.
