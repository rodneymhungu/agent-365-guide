# Automation for agent-365-guide

Two weekly GitHub Actions workflows plus a GoatCounter snippet in `index.html`.
Everything here was verified against the live docs on 5 September 2026; the
"things to check" list at the bottom is what could still drift.

## What runs

| Workflow | When | What it does | Output |
|---|---|---|---|
| `learn-drift.yml` | Mon 05:00 UTC | `learn_watch.py` fetches the 51 Learn pages `index.html` cites, plus the Agent 365 and Security-for-AI docs tables of contents and the Windows 365 for Agents what's-new page, and diffs them against `.learn-cache/`. Only if something changed: Copilot CLI proposes minimal edits to `index.html` and the `window.A365` status block. | A pull request, never a push to `main` |
| `feedback-digest.yml` | Mon 05:30 UTC | `feedback_collect.py` pulls GoatCounter visitors and per-section views, GitHub issues and traffic referrers, and Brave Search mentions. Copilot CLI writes a ≤350-word digest. | Email to your Gmail |

`.learn-cache/` is committed and already seeded, so the first scheduled run is a
real comparison. There is no Agent 365 "What's new" page on Learn; the docs
tables of contents stand in for it, so a page Microsoft adds shows up as a diff
line and the PR's "Needs a human decision" list will name it.

## Secrets to add (Settings → Secrets and variables → Actions)

| Secret | Where to get it | Used by |
|---|---|---|
| `COPILOT_PAT` | github.com/settings/personal-access-tokens/new → fine-grained PAT with **Copilot Requests** permission | both |
| `GOATCOUNTER_TOKEN` | rodneymhungu.goatcounter.com → Settings → API tokens (read-only, "statistics") | digest |
| `BRAVE_API_KEY` | brave.com/search/api (free tier) | digest |
| `GMAIL_USERNAME` | your Gmail address | digest |
| `GMAIL_APP_PASSWORD` | Google Account → Security → 2-Step Verification → App passwords | digest |

`GITHUB_TOKEN` is provided automatically. Both workflows also request the
`copilot-requests: write` permission, so if `COPILOT_PAT` is left unset the CLI
falls back to `GITHUB_TOKEN`; GitHub documents that path as billed to an
organisation, so on a personal account expect to need the PAT.

Any source whose secret is missing is reported as "unavailable" in the digest
rather than failing the run.

## Analytics

Same GoatCounter site as data-security-art-of-the-possible; the two sites are
separated by path. The guide navigates by hash (`#s6-2`), which GoatCounter
ignores by default, so the second script in the snippet records each section a
reader opens as its own path (`/agent-365-guide/#s6-2`). The digest reports
those as "sections opened" and treats paths without a hash as page visits.

## Verified on 5 September 2026

- Copilot CLI: `-p`, `--allow-tool=write`, `--allow-tool='shell(cat:*)'`,
  `--allow-tool='<mcp-server-name>'`, `--model claude-haiku-4.5`, `--no-ask-user`,
  `-s`, and the `COPILOT_GITHUB_TOKEN` → `GITHUB_TOKEN` auth precedence, all per
  the programmatic reference on docs.github.com.
- MCP config path `~/.copilot/mcp-config.json` with `type: http` entries.
- GoatCounter API: `/api/v0/stats/hits` (limit ≤ 100, `count` is visitors, no
  path-prefix filter so the collector filters client-side) and
  `/api/v0/stats/toprefs` with `include_paths`. Shapes taken from
  goatcounter.com/api.json.
- Seed run: 54 pages fetched, none unreachable, no Learn chrome in the cache.

## Things to check after the first real run

- If a PR's diff is mostly boilerplate, extend the `CHROME` regex in
  `learn_watch.py`; the seed run was clean but Learn changes its chrome.
- `start`/`end` are sent to GoatCounter as `YYYY-MM-DD`; if the API rejects
  that, the digest will say "GoatCounter unavailable" with the error.
- Whether `copilot-requests: write` works on a personal account without the PAT.

## Why it's split this way

The Learn watcher is deterministic so that most weeks cost nothing and the agent
only ever sees a bounded diff. The PR gate exists because the guide's value is
that every claim traces to Learn; a wrong GA/preview flip is worse than a stale
one. GitHub recommends Agentic Workflows (`gh-aw`) over raw `copilot` steps for
scheduled automation; if you move to that later, the two scripts stay the same
and only the YAML changes.
