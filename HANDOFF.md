# Handoff: finish the weekly automation setup

Written 5 September 2026 by Claude Code on Rodney's Mac. Read this first if you are
picking the work up on another machine. Delete this file once everything below is done.

## Where things stand

- The repo `rodneymhungu/agent-365-guide` has two GitHub Actions workflows, two Python
  scripts, a seeded Learn cache, and a GoatCounter snippet in `index.html`. All of it is
  committed and pushed to `main` (commit `a55e992`), and the live site already carries
  the analytics snippet.
- Nothing has run yet. Both workflows are inert until the repository secrets below exist.
- Full technical notes, including what was verified against the docs and what could
  still drift, are in `scripts/README.md`. Read that before changing anything.

## If you are on the Windows laptop

The Mac clone lives inside OneDrive. Do not rely on OneDrive to sync a `.git` folder;
clone fresh instead:

```
git clone https://github.com/rodneymhungu/agent-365-guide.git
```

## What Rodney has to do himself (an agent cannot do these)

Add five repository secrets at
https://github.com/rodneymhungu/agent-365-guide/settings/secrets/actions

| Secret | Where it comes from | Needed for |
|---|---|---|
| `COPILOT_PAT` | github.com/settings/personal-access-tokens/new, fine-grained, permission **Copilot Requests** | both workflows |
| `GMAIL_USERNAME` | Rodney's Gmail address | digest email |
| `GMAIL_APP_PASSWORD` | Google Account, Security, 2-Step Verification, App passwords | digest email |
| `GOATCOUNTER_TOKEN` | rodneymhungu.goatcounter.com, Settings, API tokens, read-only statistics | visitor numbers (optional) |
| `BRAVE_API_KEY` | brave.com/search/api, free tier | public mentions (optional) |

Without the optional two, the digest still sends and just says those sources were
unavailable.

## What the agent should do once secrets exist

1. Trigger both workflows by hand and watch them:

   ```
   gh workflow run learn-drift.yml
   gh workflow run feedback-digest.yml
   gh run list --limit 5
   gh run view --log-failed
   ```

2. Things the Mac session could not test and that may need a fix on first run:
   - Copilot CLI auth via `COPILOT_PAT`. If it fails, check the PAT has the Copilot
     Requests permission and has not expired.
   - The `--model claude-haiku-4.5` id in `feedback-digest.yml`. If rejected, run
     `copilot help` on the runner (or locally) and pick the current cheap model.
   - GoatCounter `start`/`end` sent as `YYYY-MM-DD`. If the digest says "GoatCounter
     unavailable", the error text will say what format it wanted; fix it in
     `scripts/feedback_collect.py`.
   - Whether the Learn drift PR diff is mostly boilerplate. If so, extend the `CHROME`
     regex in `scripts/learn_watch.py` and re-seed the cache with
     `rm -rf .learn-cache && python3 scripts/learn_watch.py`, then commit.

3. Confirm the digest email arrived in Rodney's Gmail and reads sensibly.

4. If a Learn drift PR was opened, review it with Rodney. The rule for this guide:
   every factual claim must trace to a Microsoft Learn page, and a wrong GA/preview
   flip is worse than a stale one. Never merge a status change without checking the
   cited page.

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
