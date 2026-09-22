# Plan: 2,000 high-value weekly visitors

This file is the plan of record for growing the Agent 365 field guide. It is
written for three readers: Rodney, anyone who finds the repository, and any
agent that picks up the work. If you are an agent, read this file first, then
the section "How an agent picks this up" at the bottom.

Started 21 September 2026. Reviewed every Monday alongside the weekly digest.

## Where Rodney left off, 21 September 2026

Read this first when you come back. Everything below the line was done on
21 September; these are the things that were still open when you left.

1. **GoatCounter token: cleared, 21 September, 15:36.** The token created on
   7 September was fine; the copy saved as the GitHub secret was not. Tested
   with a direct API call, re-saved with `gh secret set`, digest re-run.
   Tokens live at rodneymhungu.goatcounter.com/user/api (user settings, not
   site settings) if it ever needs re-creating.
2. **Brave Search key (optional, issue #10).** Free key at
   brave.com/search/api, saved as `BRAVE_API_KEY` in the same place. The
   digest then reports public mentions.
3. **Field guide principles repository: pushed, 21 September, 16:10.** Commit
   893e6e2 carries the 9 September edits and the "one page per topic, one
   data file" amendment. The guide, the skill and the repo now agree.
4. **LinkedIn article posted, 22 September, 13:00.** Next one is due with the digest of 5 October.
   Everything is in `distribution/2026-09-21-linkedin.md`: three pickup
   steps, headline, body, and two cover images beside it. Format decided on
   21 September: a short weekly LinkedIn article on the latest update, guide
   link inside the article. When posted, add the URL to that file's "Posted"
   line and a row under focus 4 in the log below.
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
| 7 September 2026 | not measured | not measured | GoatCounter returned HTTP 404 to the digest: the secret held a bad copy of a good token. |
| 14 September 2026 | not measured | not measured | Drift pull request #16 sat unmerged for a week. Nothing shipped. |
| 14 September 2026 | 24 | LinkedIn 11, direct 9, Teams 3 | Measured on 21 September once the token was fixed. Eleven sections opened; 5.1, 2.2, 10, 3 and 2.1 most. |
| 21 September 2026 | measuring | measuring | Catch-up week: focus 1, 2 and 3 all shipped, see log. Analytics restored 15:36; the first live digest is the second one dated 21 September. |

## The weekly rotation

One focus a week, in this order, then repeat. Catch-up weeks may do more
than one. The digest names the current focus so nobody has to count.

| # | Focus | What "done" looks like |
|---|---|---|
| 1 | Split a section into its own indexable page | A new `*.html` at the repository root with its own title, description, canonical link and JSON-LD, listed in `sitemap.xml`, linked from the section it came from, rendering status from `a365-data.js`. |
| 2 | Build or extend a lookup table | A table a reader can scan in ten seconds: licence, preview against GA, control to scenario. Every row sourced at the point of use; status rendered from the data block, never typed. |
| 3 | Write the changed-this-week note | Merge the open `learn-drift` pull request, then add one entry to `changes` in `a365-data.js` that says what moved and links the Learn page. If nothing drifted, say so in the digest and skip. |
| 4 | Distribution | A short LinkedIn article every second week on the latest updates, with the guide link inside the article (decided 21 September 2026). The Monday digest carries a ready draft on article weeks (week 1, 3, 5 … of the rotation), built from the last fortnight's `changes` entries. Drafts live in `distribution/`, one file per post with its cover image. Plus, when there is one, a follow-up to a session audience or an account outreach. Record each in the log with the link and the referrer to expect. |

Every week, whatever the focus: check GoatCounter referrers, not just paths.
A path tells you what people read. A referrer tells you who sent them and
whether they are the reader this guide is for.

## Blockers that only Rodney can clear

1. **GoatCounter token: cleared on 21 September.** The 404 was a bad copy of
   a good token in the GitHub secret. If it recurs: tokens are at
   rodneymhungu.goatcounter.com/user/api; test one with a direct call to
   `/api/v0/me` before saving it with `gh secret set GOATCOUNTER_TOKEN`.
2. **Brave Search key.** Issue #10. Optional, but without it the digest
   never sees public mentions, which is the only distribution feedback loop
   that does not depend on the referrer.

## Out of scope

Decided by Rodney, with the date, so nobody re-opens these by accident.

| Since | Topic | Decision |
|---|---|---|
| 21 September 2026 | Microsoft 365 Government Community Cloud (GCC, G7) availability | Out of scope. GCC is a United States programme and this guide's readers are not in it. The service description's "GCC Availability" column is not tracked and chapter 2 carries no GCC caveat. Reopen only if a reader asks for it explicitly, through an issue. Drift pull requests that mention GCC changes can be merged without adding prose. |

## Log

Newest first. One line per item shipped, with the pull request.

| Date | Focus | Shipped | Evidence |
|---|---|---|---|
| 21 September 2026 | 3 | Merged the 21 September drift pull request after checking each claim on the live Learn page: Defender for Endpoint local agent discovery is GA (macOS still preview), Intune has a native Antivirus profile for agent-native runtime protection, Snowflake Cortex joins registry sync. Three changelog entries. Writing review: two "now/still" phrasings removed. | #25 |
| 22 September 2026 | 4 | First LinkedIn article, the 21 September release note, posted at 13:00 with the Defender local agents screenshot as cover. Expect the referrer www.linkedin.com in the 28 September digest, and section opens on 5.5, 7.4, 5.4 and 4.1. | [post](https://www.linkedin.com/posts/rodney-mhungu-18a26434_ive-updated-the-agent-365-field-guide-with-ugcPost-7507888290696491010-FqIJ) |
| 21 September 2026 | Images | Three Defender screenshots replaced with the Learn originals (CC BY 4.0, full resolution, no baked-in callouts): the local agents inventory in 5.5, the Claude Code block and toast and the prompt injection alert in 7.4. The other 27 deck slides stay because no Learn page shows the same view or the Learn version contradicts the prose. Rule: prefer the Learn original where it shows the same view. | #39 |
| 21 September 2026 | Plumbing | Tier changes are now human-only in code, not just in the prompt: `guard_tiers.py` reverts any tier the drift model moves and fails a pull request that moves a tier to GA without a release-notes link. The watcher tracks six product release-notes pages, filtered to lines about agents or MCP. | #36 |
| 21 September 2026 | Correction | Defender for Endpoint local agent discovery back to preview after Rodney caught it against the portal and the release notes. Drift prompt now requires a release-notes GA entry before any tier moves to ga. LinkedIn draft corrected. | #35 |
| 21 September 2026 | Plumbing | The Monday digest now carries a LinkedIn article draft every second week, built from the last fortnight's changelog entries without a model. First one lands 5 October. | #34 |
| 21 September 2026 | Writing review | `ai-writing-review` run over both pages: twelve flags, ten applied (changelog voice in 5.5 from the drift edit, "data block" in reader copy, a contrast rhythm in 4.1, closing verdicts for 6.7 and 7.5, small repetitions), two kept as note-only. | #24 |
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
7. A Learn page dropping "(Preview)" from its title is not a GA signal. Move a
   status to `ga` only when the product's release notes or What's new page say
   GA. Learnt on 21 September 2026: the drift run flipped Defender for Endpoint
   local agent discovery to GA on the title change; the release notes and the
   portal still said preview, and the LinkedIn draft repeated the error.
8. Every change to prose goes through the `ai-writing-review` skill before
   the pull request opens: report the flags, apply the ones the author
   approves, log the ones kept. This includes every distribution draft in
   `distribution/` before it is posted, the digest-generated ones included. Rodney's standing instruction from
   21 September 2026 is to run it on every prose update without being asked.
