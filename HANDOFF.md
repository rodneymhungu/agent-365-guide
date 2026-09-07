# Handoff: finish the weekly automation setup

Written 5 September 2026 by Claude Code on Rodney's Mac. Read this first if you are
picking the work up on another machine. Delete this file once everything below is done.

## Where things stand, updated 7 September 2026

The Windows laptop is now signed in to the GitHub CLI, and both workflows have
been exercised.

- **Learn drift works.** It ran on schedule on 7 September, compared the 55
  cached Learn pages, found no drift and skipped the Copilot steps. The Copilot
  and pull-request path is still unproven, because nothing had changed to
  propose.
- **The digest now arrives as an issue.** A manual run on 7 September collected
  signals, installed the CLI and wrote the digest, then failed at the old Gmail
  step. Rather than store a Google app password, the delivery was changed to open
  an issue labelled `digest`, which GitHub emails to the repository owner.
- **The repository has no secrets, and no longer needs any.** Both workflows run
  on the automatic `GITHUB_TOKEN`.
- **`COPILOT_PAT` turned out to be optional.** Copilot CLI authenticated with the
  automatic `GITHUB_TOKEN` on a personal account and accepted the
  `claude-haiku-4.5` model id. See `scripts/README.md` for the full findings.

## What Rodney has to do himself

Nothing is required. Two optional secrets at
https://github.com/rodneymhungu/agent-365-guide/settings/secrets/actions
would enrich the digest:

| Secret | Where it comes from | Adds |
|---|---|---|
| `GOATCOUNTER_TOKEN` | rodneymhungu.goatcounter.com, Settings, API tokens, read-only statistics | visitor numbers and sections opened |
| `BRAVE_API_KEY` | brave.com/search/api, free tier | public mentions |

Without them the digest still arrives and says those sources were unavailable.

## What is left for the agent

1. Confirm the issue-based digest reads sensibly, and that GitHub emailed it:

   ```
   gh workflow run feedback-digest.yml
   gh run watch
   ```

2. Prove the drift workflow's Copilot and pull-request path. Drift is rare, so
   force it: on a branch, delete one file from `.learn-cache/`, run the workflow,
   check the pull request it opens, then revert.

3. Decide what to do about the traffic API 403. Referrers need a personal access
   token with push access, or the section comes out of the digest.

4. Confirm `feedback-digest.yml` fires on its own schedule next Monday. It did
   not on 7 September.

5. Review any Learn drift pull request with Rodney. The rule for this guide:
   every factual claim must trace to a Microsoft Learn page, and a wrong
   GA/preview flip is worse than a stale one. Never merge a status change
   without checking the cited page.

6. Delete this file once all of the above is done.

## How the pieces fit

- `learn-drift.yml` (Mondays 05:00 UTC): `scripts/learn_watch.py` diffs the 51 cited
  Learn pages plus the Agent 365 and Security-for-AI docs tables of contents. Only when
  something changed does it install Copilot CLI, ask for the minimal edit, and open a
  pull request on branch `auto/learn-drift`. It never pushes content to `main`.
- `feedback-digest.yml` (Mondays 05:30 UTC): `scripts/feedback_collect.py` gathers
  GoatCounter, GitHub traffic and issues, and Brave Search mentions into
  `feedback-input.md`; Copilot writes `digest.md`; an SMTP action emails it via Gmail.
- Everything runs on GitHub's hosted runners. No laptop needs to be on.

## Style rules for any edit to the guide

British spelling. Keep the author's voice. Status lives in the `window.A365` data block
at the top of `index.html`, never in the prose. Do not touch "Rodney's field note"
callouts. See `README.md` and the field guide principles it links to.
