# Plan: 2,000 high-value weekly visitors

This file is the plan of record for growing the Agent 365 field guide. It is
written for three readers: Rodney, anyone who finds the repository, and any
agent that picks up the work. If you are an agent, read this file first, then
the section "How an agent picks this up" at the bottom.

Started 21 September 2026. Reviewed every Monday alongside the weekly digest.

## Where Rodney left off, 10 November 2026

Read this first when you come back. One pull request carries everything from
10 November; merging it also closes the 9 November drift pull request (#79)
and the article pull request (#78), because their commits are in it.

- **Drift, 9 November.** Both edits checked on the live pages and kept: fixed
  outbound IP addresses for Connected platforms (5.4), and Defender for
  Endpoint finding Visual Studio Code extensions from installed-extension
  data without a run (5.5). Added on review: an inventory entry is not proof
  of use (5.5) and Agent 365 SDK 2.0 with its migration page (5.4). Review
  date 10 November.
- **Chapter 10 is a status board.** The digests of 26 October, 2 November and
  9 November put 44, 94 and 73 per cent of visitors on chapter 10, which was
  a flat table that clipped on a phone. It now has a status meter that
  filters, product chips, a find box, a link from every row to the section
  that explains it, and cards on a phone. The hero carries the same meter
  and the three newest changes; sections changed in the last fortnight carry
  an Updated marker. See the log.
- **`changes.html` is live with this merge.** Built on 21 October and never
  merged; now brought up to date.
- **The drift workflow syncs its own static copies.** It runs
  `check_pages.py --fix` before the check and commits `changes.html` and
  `sitemap.xml`, so drift pull requests stop arriving with a stale sitemap
  and the false "chapter 2 differs" line.
- **The article for the week of 9 November is updated and ready** in
  `distribution/2026-11-09-linkedin.md`: eight bullets, the discovery
  sentence corrected against the 9 November Learn change, a second cover
  showing the status board. Three Low writing-review flags wait on Rodney;
  the default is keep.
- **Use case classification is in 6.4** (10 November, added in the
  pre-merge review). Agent Map classifies every eligible agent session into
  a predefined business use case, on by default, with an opt-out under
  Agents, Settings. The setting, who can change it and what happens to
  earlier results are in the guide as a Frontier preview control. The value
  and return-on-investment reporting built on it stays out, by the
  11 October decision on the Consumption Dashboard; see Out of scope. Take
  the paragraph out if you would sooner not cover it.
- **The week of 26 October is explained, and the native-post test is run.**
  Rodney posted the 25 October feed post with the chapter 4 map, from the
  draft on the closed pull request #73, and said so on 10 November. It drew
  3,605 impressions, 74 per cent out of network, 30 saves, 5 reposts, 19
  followers and 40 clicks; the article of 6 October drew 986 impressions, 2
  saves and no followers. Numbers side by side in
  `distribution/2026-10-25-linkedin-post.md`.
- **Format: Rodney is leaning post-first** (10 November). A feed post in the
  same shape is drafted for today in `distribution/2026-11-10-linkedin-post.md`
  with the status board as its image, beside the article draft; post one, not
  both. The feed post format is written down in `distribution/README.md`.
  Not done until Rodney confirms: changing `article_draft` in
  `scripts/feedback_collect.py` so the digest generates the feed post shape.
- **The 21 October native post draft was dropped** unmerged; the 25 October
  one superseded it.

## Where Rodney left off, 6 November 2026

The older handoff, kept because most of its list is still open.

The 2 November drift pull request (#74)
was reviewed and extended on 6 November: every proposed edit checked against
the live page, Defender for Endpoint local agent discovery moved to GA on its
October what's new entry, the two status conflicts (`defender-posture`,
`mde-runtime`) kept at preview with dated notes, and the November
announcements (Execution Containers GA, Project Perception direction, the
Manage agents page) folded in. Merged on 6 November, together with #77, which
adds announcement-feed discovery to the drift watcher (new posts arrive as
coverage candidates, feed failures are reported, never passed as "no
changes"). The Agent 365 Action Center (3 November Gartner MQ post) has no Learn
page yet and is deferred; see the pull request body. Rodney skipped the
25 October native feed post (PR #73, closed unposted) and will post one
article in the week of 9 November instead, drafted in
`distribution/2026-11-09-linkedin.md` with the chapter 4 map as its cover:
seven product changes from 11 October to 6 November, led by Defender for
Endpoint discovery reaching GA. The older list below is kept because most of
it is still open.

1. **The 6 October article is live and logged** (18 October, focus 4 row in
   the log). Still only Rodney can edit the live copy: the registry sync
   bullet wants "and" after "Connected platforms".
2. **Decide the weekly format: native post or article.** A second review
   (6 October) argues for a native feed post each week, under about 1,300
   characters, one change led, two or three more named, the guide linked
   once in the body, and the article kept for a quarterly piece. The
   21 September decision was the article, with the LinkedIn referrer as the
   test. Evidence so far: article week 1 brought 10 LinkedIn visitors, the
   week with no article brought 4, article week 2 brought 13 (986
   impressions, 39 article views; see the log row of 18 October), and a
   native post was tried on 26 October: 49 LinkedIn visitors, 3,605
   impressions, 30 saves, 19 followers (see the log row of 10 November and
   `distribution/2026-10-25-linkedin-post.md`). That is the 45 LinkedIn
   visitors the 2 November digest could not explain.
   Recommendation, 10 November: a feed post with an image every time there
   is something to say, the article kept for a quarterly piece. One caveat:
   the post differed from the article in format and in carrying a new
   diagram, so every feed post needs a real visual. Rodney is leaning this
   way and has not confirmed; when he does, `article_draft` in
   `scripts/feedback_collect.py` changes to the feed post shape in
   `distribution/README.md`.
3. **Candidate for the next focus 2 week: a permissions table in 5.4.**
   One row per Connected platforms provider: credential type, the read
   permission set, whether delete is required, optional or absent, and the
   extra grant observability needs. Bedrock (two sets, Classic and
   AgentCore; delete opt-in; S3 or CloudWatch for activity) and Vertex AI
   (service account key; delete in the base set; four BigQuery, Monitoring
   and Trace roles for observability) are documented in enough detail; the
   other five pages are thinner. Source each cell from its setup page.
4. **Two claims from that review not to repeat.** The Learn hub was not
   renamed on 28 September; that is the page's ms.date. The guide's
   5 September cache already carried the Connected platforms title, so the
   rename sits between the April announcement and 5 September. And the
   graphic point stands: Foundry integrates automatically and is not a
   Connected platforms provider, so it should not sit under that label.
5. **Credentials to add, in any order, one at a time:** `GOOGLE_CSE_KEY`
   and `GOOGLE_CSE_ID` (Google Programmable Search, free, no card; Brave
   needs a card, so `BRAVE_API_KEY` is the fallback), `BLUESKY_HANDLE` and
   `BLUESKY_APP_PASSWORD` (bsky.app, Settings, App passwords),
   `MASTODON_INSTANCE` and `MASTODON_TOKEN` (your instance, Preferences,
   Development, scope write:statuses), `DEVTO_API_KEY` (dev.to, Settings,
   Extensions). All go in Settings, Secrets and variables, Actions. Plus the
   Bing Webmaster Tools and Google Search Console meta-tag codes, which
   Claude puts in both page heads. Steps in `scripts/README.md`. Nothing
   breaks while any are missing.
6. **Two drafts still unsent:** the curator email in
   `distribution/2026-09-27-curator-intune-newsletter.md` (from Rodney's own
   address, recipient to confirm) and the feed post in
   `distribution/2026-09-30-linkedin-post.md`, which now carries the 5.5
   table on its own since the article dropped that bullet.
7. **The claude.ai copy of `ai-writing-review`** still has the 17-tell
   checklist. The 19-tell version is in the local skill; upload the zip
   Claude packaged on 6 October, or ask for it again.
8. **Four pull requests from the 11 October site review, merge in order:**
   #61 video chapter buttons, #62 static copies of the data values, #63
   guide.js parts, then the September announcements pull request. Each is
   stacked on the one before, so its diff shrinks as the earlier ones merge.
   After the last one merges, the live page shows the 11 October review
   date.
9. **Candidate for a later focus 2 week: spending policies in chapter 6.**
   Microsoft's September What's new post describes cost management in
   Agent 365: spending policies that cap credits per group and restrict
   which models and effort levels a group may use, across Copilot Cowork,
   WorkIQ, Code and Copilot Managed Runtime, with Copilot Studio agents in
   October. Decision of 11 October: in scope for the spending policy, as a
   guardrail on a runaway agent and an allow-list of models, as one section
   in chapter 6 plus a 4.1 row; out of scope for the Consumption Dashboard's
   value reporting. Wait for a Learn page before writing it; the post is
   blog-only today.

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
| 28 September 2026 | 26 | direct 18, LinkedIn 4, static.microsoft.com 3 | From the 6 October digest, re-run by hand after the 5 October crash. Most opened: 4.1, 10, 9, 2.1. |
| 5 October 2026 | 53 | direct 30, LinkedIn 13 (web 9, app 4), Teams 6 | From the 12 October digest. Busiest day 9 October with 11. Most opened: 4.1 and 7.2 (7 each), 2.1, 6.4, 5.3. The 6 October article was posted this week. |
| 12 October 2026 | 25 | direct 15, Teams 4, LinkedIn 3, Bing 1 | From the 19 October digest. No post. Most opened: 7.2 (5), 2.2 (4). |
| 19 October 2026 | 34 | direct 15, LinkedIn 9, Teams 2 | From the 26 October digest. No post. Most opened: 10 (15), 4.1 and 2.1 (7 each). |
| 26 October 2026 | 66 | LinkedIn 49 (web 45, app 4), direct 8, Teams 3, Substack 1 | From the 2 November digest. The best week so far: 36 visitors on 26 October alone, 62 of the 66 on chapter 10. Source: the 25 October feed post with the chapter 4 map, posted about 26 October and logged on 10 November. |
| 2 November 2026 | 15 | direct 10, LinkedIn 3 | From the 9 November digest. No post. Chapter 10 took 11 of the 15. |

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
| 10 November 2026 | Business use cases for agents (Frontier) | Partly. The Use case classification setting is in 6.4: it is on by default, classifies agent sessions, and an administrator can turn it off, which a compliance engineer needs to know. The adoption, duplication and return-on-investment reporting built on the classifications is out of scope, for the same reason as the Consumption Dashboard. Added by Claude in a pre-merge review; Rodney to confirm or remove. |
| 11 October 2026 | Cost management and the Consumption Dashboard | Partly. Spending policies (credit caps and model allow-lists per group) are in scope as a chapter 6 section once a Learn page exists; see item 9 above. The Consumption Dashboard's credits-to-value reporting is out of scope: a finance report, not a control a security or compliance engineer deploys. Reopen only if a reader asks. |
| 6 October 2026 | FedRAMP and other US federal authorisations | Out of scope, for the same reason as GCC: the guide is for commercial customers in Europe and worldwide, and no European buyer decides on FedRAMP. The 5 October drift run added a FedRAMP High sentence to 2.1; it was taken out before merging. The drift prompt now names GCC and FedRAMP as out of scope, so future runs note them in CHANGES.md without editing prose. Data residency and the EU Data Boundary stay in 5.6. |

## Log

Newest first. One line per item shipped, with the pull request.

| Date | Focus | Shipped | Evidence |
|---|---|---|---|
| 10 November 2026 | Structure | Pre-merge review of the status board against how the guide is used: shared in Teams and LinkedIn, steered by the Monday digest. Four additions. A Clear filters control whenever a filter is on (before, a status filter could only be undone by pressing the same segment again). The address bar follows the status and product filters and a Copy link to this view control copies it, so a filtered view can be sent to a customer. Each status or product filter a reader uses is counted once per visit and listed in the digest under "Status board filters used"; what is typed in the find box is never recorded. The hero's latest changes are cut to two lines each. Thirty-four controls with the new 6.4 row. | this pull request |
| 10 November 2026 | Structure | Chapter 10 rebuilt as a status board, on the evidence that it is the landing section (44, 94 and 73 per cent of visitors in the last three digests) and that its table clipped two columns on a phone. A meter counts the controls by status and filters on click; product chips and a find box narrow the list; each row carries a status stripe and a link to the section that explains it, from a new `sec` field on every capability; at 760px and below each row is a card. The same meter sits under the hero with the three newest product changes, the end of chapter 10 lists the five newest and three ways onward, and sections a product change touched in the fortnight before the review date carry an Updated marker and a dot in the contents panel. The board's rows are a static copy written by `check_pages.py --fix`, so crawlers and readers without JavaScript see the statuses; a link can open the board filtered (`?status=preview&product=defender#s10`). Identity unchanged: same type, palette, borders and offset shadows. Rendered at 390, 768 and 1440 in light and dark: no overflow, no script errors, filters, GA only switch and deep link exercised. | this pull request |
| 10 November 2026 | 1 | `changes.html`, the changelog on its own page, built on 21 October and merged now: own title, description, canonical link and JSON-LD, in the sitemap, entries grouped by month and date with an anchor per date. Static copy of the `changes` array, regenerated and checked by `check_pages.py`. | this pull request |
| 10 November 2026 | 3 | Reviewed the 9 November drift pull request against the live pages and merged it into this one. Kept: Connected platforms connect from a fixed set of outbound IP addresses, and a blocked connection can show an authentication error (5.4); Defender for Endpoint finds Visual Studio Code extensions from installed-extension data without a run (5.5). Added: an inventory entry is not proof of use (5.5); Agent 365 SDK 2.0 and the .NET `authToken` change, from the new migration page (5.4). Added in the pre-merge review: use case classification (Frontier), on by default with an opt-out, as a paragraph in 6.4 and a row on the board; its value reporting stays out of scope. Review date 10 November. Writing review on the new prose: two flags in my own sentences reworded before commit (a staged "One does not:" in 5.4, a repeated "Every" opening chapter 10). | #79 and this pull request |
| 10 November 2026 | Plumbing | The drift workflow runs `check_pages.py --fix` before its check, commits `changes.html` and `sitemap.xml`, and reports what still fails in the check's own words. Before, every drift pull request arrived with a stale sitemap and a fixed "chapter 2 differs" line whatever had failed. The prompt tells the model to give a new capability a `sec` and to leave the static copies alone. | this pull request |
| 10 November 2026 | 4 | The 25 October feed post logged as posted, about 26 October, with the chapter 4 map: 3,605 impressions (74% out of network), 2,181 members reached, 43 reactions, 7 comments, 5 reposts, 30 saves, 19 followers gained, 40 clicks to the guide; GoatCounter counted 49 LinkedIn visitors that week, 62 of 66 visitors on chapter 10. Against the 6 October article: 3.7 times the impressions, 3.8 times the visitors, 15 times the saves. The native-post test from 6 October is therefore run and the post won, with the caveat that it also carried a new diagram. Draft and cover restored from the closed pull request #73. A feed post in the same shape drafted for 10 November with the status board as its image; the feed post format added to `distribution/README.md`. | [post](https://lnkd.in/p/eSvCrqWR) |
| 10 November 2026 | 4 | The article for the week of 9 November updated for the 9 November drift and the redesign: discovery sentence corrected, a bullet for the outbound IP addresses (eight bullets), the "Also new" bullet leads with the status board, a second cover rendered from the board. Writing review of the changed passages logged in the file: three Low flags, none applied. | this pull request |
| 6 November 2026 | 4 | LinkedIn article for the week of 9 November drafted in `distribution/2026-11-09-linkedin.md`, replacing the unsent 19 October article and the 25 October native post (#73, closed unposted at Rodney's call). Seven product changes from 11 October to 6 November, curated by hand because the 2 November digest draft covered only its fortnight: Defender for Endpoint discovery GA leads (endpoint, after two identity-led drafts), then runtime protection's supported agents and Intune template, agent-risk Conditional Access needing P2 or E5, Connected platforms observability and its billed queries and audit gap, prompts and responses in Azure agent observability data, duplicate registry entries, and the three kinds of MCP server; the chapter 4 map as the "Also new" bullet and the cover, re-rendered so the discovery badge reads GA. Execution Containers offered as an optional bullet, since it is not on Learn. Not yet posted. Writing review: three low flags; Rodney applied flag 1 (the Researcher and Analyst sentence now names the Manage agents page) and kept 2 and 3. | this pull request |
| 6 November 2026 | 3 | Reviewed and extended the 2 November drift pull request, each edit checked against its live source. Verified and kept: activity metrics scoped to third-party agents (first-party agents report without the licence), the Databricks-managed service principal for Genie, Prompt Shields block events for Copilot Studio recorded as behaviours (7.3 needed no edit). Moved on release-notes evidence: Defender for Endpoint local agent discovery to GA for Windows and macOS (October what's new; WSL and macOS VS Code extension entries stay preview; matrix now 62 Windows, 59 macOS tools). Kept at preview with dated notes: posture risk (XDR what's new still says preview) and runtime protection (Intune's template is GA with a new AI agent runtime inspection setting, the Defender feature is not). Added: the Manage agents page to 6.1 and 6.4 with the creator-shared against organisation-published distinction, Execution Containers GA on Windows with Agent 365 integration still upcoming (7.4), and a two-sentence direction note on Dynamic Permissions, Dynamic Agent Risk, Dynamic Conditional Access and Project Perception (7.1). Deferred: the Action Center, blog-only, no Learn page. Seven changelog entries; review date 6 November. Merged the same day with #77, which adds announcement-feed discovery to the watcher. Writing review: three flags, all applied (a duplication, a narrowed claim, a wrong attribution). | #74, #77 |
| 25 October 2026 | Structure | Chapter 4's Figure 3 rebuilt as a three-band map: the four routes an agent takes into Agent 365 (built in, with the SDK, Connected platforms, on the device), the control plane, and the products that enforce, with status badges on the routes from the data file. The idea came from a community architecture overview by Russell Hockley; the content comes from Learn's Choose an Agent 365 integration option page, now cited in chapter 4. The old hover-pillar SVG and its script and styles are gone. Built as an HTML grid, not SVG, so the text wraps at 390px and the badges use the same spans as the rest of the page; README says so. The top bar carries one name on both pages (the "Agent control atlas" label is gone) and fits a phone in two balanced rows, one row from 621px up. Writing review: one flag applied, "data block" in reader copy. | this pull request |
| 25 October 2026 | 3 | Merged the 19 October drift pull request after checking each edit against the Learn page it cites. Brought up to main first: #71 had changed chapter 2 and 5.4 after it branched, so its 5.4 observability edit was already in and was dropped. Kept: first-party agents cannot be reassigned (6.3). Decisions closed on Learn: 5.1 says one Copilot Studio agent can appear twice; 5.4 gains the read-only model, key-based credentials, deletion reconciliation and the Purview audit log gap for connection actions; 6.5 cites the new MCP server options page and the CLI evaluate step. Work IQ MCP keeps its name, the options page still uses it. Four changelog entries. | #69 |
| 18 October 2026 | 3 | Closed every open decision from the 12 October drift report, each checked on Learn first. 5.4: observability on Connected platforms now covers five platforms (Agentforce and Databricks Genie joined), each connection has a Collect agent observability data switch that is on by default and whose provider queries are billed, and the two Learn pages disagree about older connections, which the guide says; two onboarding walkthroughs (single agent with the Agent 365 CLI, bulk from one CSV with PowerShell) cited. 5.5 and 7.4: the Defender AI agent support matrix is now the source for both Defender columns of the lookup table, with Claude Desktop and two VS Code extensions gaining hooks, ChatGPT and Ollama Desktop gaining network inspection, Antigravity Desktop and Microsoft Scout discovered, and Codex CLI named by the overview but absent from the matrix. 5.6: the Azure agents data-residency page, prompts and responses included, per-platform switch-off. 2.1 and 7.1: agent risk-based Conditional Access needs Entra ID P2 or E5. Review date 18 October. Legibility pass: 5.4 split into shorter paragraphs, two long onboarding sentences split; rendered at 390 and 1440 in light and dark with no overflow and no script errors; no dashes, no US spellings, no broken anchors. Writing review: no flags beyond the two splits. | this branch |
| 18 October 2026 | 3 | Merged the 12 October drift pull request after checking each of its five edits against the live Learn page it cites: the Conditional Access licence notice ("Agent 365 licence will soon be required") is gone from the autonomous agents page, so 2.1 drops the "enforcement is coming" sentence; 5.5 says Defender lists a local agent only after it sees it run and that the list is not a software inventory; 5.6 scopes collection starting at trial or licence to third-party agents and ten named countries; 6.6 access packages grant delegated as well as application permissions; 7.1 says every policy in the Users assignment excludes agent users, and the widget note in guide.js now says the same. Also checked: the Identity Protection page still says its licence requirement is starting soon, so the chapter 7 sentence stands. Sitemap date synced with `check_pages.py --fix`. Writing review: one 5.5 sentence reworded ("observes it active"); changelog entries kept as changelog voice. Open from the drift report, not yet decided: the Connected platforms "Collect agent observability data" setting and its provider charges for 5.4, the new AI agent support matrix page for 7.4 and 5.5, agent risk-based Conditional Access needing P2 or E5 for 2.1 and 7.1, the Azure agents data-residency page for 5.6, and two uncited onboarding pages (CLI and bulk PowerShell). | #67 |
| 18 October 2026 | 4 | Second LinkedIn article, the 28 September and 5 October release note, posted about 11 October from `distribution/2026-10-06-linkedin.md` with an illustrated cover. Logged on 18 October with one week of LinkedIn analytics: 986 impressions (43% out-of-network), 661 reached, 39 article views, 19 reactions, 3 comments, 2 saves, no reposts. The 12 October digest shows the referrer: LinkedIn 13 against 4 the week before, so about one article reader in three reached the guide. This is the baseline for the native-post comparison; do not change the article generator before it. | [post](https://lnkd.in/p/exg_rJiH) |
| 11 October 2026 | 3 | Microsoft's September What's new post (30 September, Tech Community) checked against the guide. Three gaps closed: 6.3 lists the fifth management rule, Apply a template, and the conditions the post adds; 5.3 gains AI mode and 5.4 gains the Azure API Management integration, both as blog-only announcements at the early preview tier until Learn documents them, with a 4.1 row for the gateway. Cost management recorded as a scope decision above. Review date 11 October. | this pull request |
| 11 October 2026 | Plumbing | Three fixes from an outside site review: the eight chapter buttons under the 6.7 and 7.5 videos no longer all jump to the start; the review date, prices and key dates sit in the page text for crawlers and link previews, with `check_pages.py --fix` to rewrite them and a check that fails when they drift; `guide.js` runs each part on its own so one missing element cannot stop the rest. The first run of the new check also caught `dateModified` a day behind and the sitemap two weeks behind. | #61, #62, #63 |
| 6 October 2026 | 3 | Gaps raised by Rodney from a review elsewhere, each checked on Learn first. The guide now uses the current name, Connected platforms, in 2.1, 2.2, 4.1, 5.1, 5.4 and the chapter 10 rows. Corrected the same evening: Microsoft announced the feature as Registry sync (Message Center RM559615, 23 April 2026) and the Learn hub carried that title before being renamed by 5 September; five cited Learn pages still use the old name. 5.4 now says so in one sentence, with the announcement linked, so readers searching for the April name find it. 5.4 gains the observability split: the hub lists Bedrock, Vertex AI and Anthropic, with four coming soon, and the Frontier third-party observability page also lists Agentforce, which the hub does not. New Frontier capability row for third-party agent observability. Writing review: three wording fixes, observability moved to its own paragraph. | this pull request |
| 6 October 2026 | 3 | Closed the two open decisions from the 5 October drift report. 5.4 links all seven registry sync setup pages and says the permission scope varies (Vertex AI requires delete; Bedrock and Oracle are read-only with delete optional), correcting an overgeneralisation added in #51. 6.8 cites the new Create agentic user instances page: admins can create an instance on behalf of a manager. Status left at Frontier; the new page carries no preview notice, but tiers move only on release notes. Writing review: no flags. | #55 and this pull request |
| 6 October 2026 | Writing review | Whole-guide sweep with `pyramid-edit` and `ai-writing-review`, fifteen flags, all applied: 5.5 and 7.2 open on their verdict; 2.1 and 7.4 split into one claim per sentence; the hero names all five enforcing products; 4.1 lists all seven synced platforms; 3 points at 7.1, not 7; GSA spelled out; bare section numbers; "now" and three "matters" removed; the guard analogy in 3 cut. The `ai-writing-review` checklist was refreshed first with current-model tells ("this matters", copula avoidance, changelog voice). Kept as note-only: the short verdict that closes most sections. | this pull request |
| 6 October 2026 | 3 | Merged the 5 October drift pull request after checking each edit against the Learn text it cites: Conditional Access for agents licensing (E7, or Agent 365 with Entra ID P1 or Microsoft 365 E3), the SDK's observability packages deprecated in favour of the Microsoft OpenTelemetry Distro, registry sync scheduling no longer promised. Taken out: the FedRAMP High sentence, now out of scope. Added in review: 5.4 delete rights are optional, from the new per-platform setup pages, and 6.4's setting is now Agent and plugin access. Open decisions from the drift report: link the per-platform pages from 5.4 more fully, the new Create agentic user instances page for 6.8. | #51 |
| 6 October 2026 | Plumbing | The 5 October digest crashed before opening its issue: two guide changelog entries dated 27 September, one without a section, could not be sorted. The article draft now sorts on the date alone. FedRAMP and US government clouds added to Out of scope and to the drift prompt. | this pull request |
| 28 September 2026 | 3 | Merged the 28 September drift pull request after checking each edit against the Learn text it cites: the Risks column covers high, medium and low severity; agent deletion is a soft delete with a thirty-day window for any agent type; AI administrators can activate templates and delete instances; runtime protection deploys from the Defender portal as well as Intune and needs the Beta Channel in preview. Four changelog entries. Writing review: three changelog-voice phrasings removed from 5.3 and 7.4, one rhythm note on the changelog entries kept. Open decisions from the drift report: the 5.3 risk-type table left Learn, a new Activate governance action, and a new third-party agent observability page. | #48 and this pull request |
| 21 September 2026 | 3 | Merged the 21 September drift pull request after checking each claim on the live Learn page: Defender for Endpoint local agent discovery is GA (macOS still preview), Intune has a native Antivirus profile for agent-native runtime protection, Snowflake Cortex joins registry sync. Three changelog entries. Writing review: two "now/still" phrasings removed. | #25 |
| 27 September 2026 | Structure | Pyramid pass over the whole guide, seven flags applied: 5.4 and 6.1 open on their answer; 6.2 custom templates and 7.3 real-time coverage became tables; 5.5 names each tool once and points at the new table; 7.4 says which admin-centre page blocks what; 5.2 closes on a verdict. Writing review: no new flags. | #47 |
| 27 September 2026 | 2 | 5.5 gains "Which surface sees which tool, and which can block it": 13 rows joining the Shadow AI page, the Local agents page, Defender for Endpoint discovery and runtime protection, every cell from its Learn page, closing on two verdicts. Curator email and a mid-week feed post drafted in `distribution/`. | #46 |
| 22 September 2026 | Plumbing | Distribution automation built: IndexNow on every deploy; Bluesky and Mastodon post and dev.to draft on article weeks; "Questions the guide could answer" in the digest. Each needs its credential added as a secret; none added yet except the IndexNow key, which is public. | #43 |
| 22 September 2026 | 4 | Distribution channels researched and ranked in `distribution/CHANNELS.md`: search via IndexNow, a LinkedIn newsletter, Bluesky and Mastodon, dev.to, curator newsletters, Tech Community, Reddit and Q&A answering, awesome lists, user groups. Automation order proposed; nothing built yet. | CHANNELS.md |
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
9. The Learn cache starts on 5 September 2026. Before saying a name or
   feature was never Microsoft's, check the Message Center archive at
   mc.merill.net and the page's earlier title. Learnt on 6 October 2026:
   "registry sync" was called the guide's own term for a day; Microsoft had
   announced the feature under that name in April, and five cited Learn
   pages still use it.
