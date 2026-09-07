# Automation for agent-365-guide

Two weekly GitHub Actions workflows plus a GoatCounter snippet in `index.html`.
Everything here was verified against the live docs on 5 September 2026; the
"things to check" list at the bottom is what could still drift.

## What runs

| Workflow | When | What it does | Output |
|---|---|---|---|
| `learn-drift.yml` | Mon 05:00 UTC | `learn_watch.py` fetches the 51 Learn pages `index.html` cites, plus the Agent 365 and Security-for-AI docs tables of contents and the Windows 365 for Agents what's-new page, and diffs them against `.learn-cache/`. Only if something changed: Copilot CLI proposes minimal edits to `index.html` and the `window.A365` status block. | A pull request, never a push to `main` |
| `feedback-digest.yml` | Mon 05:30 UTC | `feedback_collect.py` pulls GoatCounter visitors and per-section views, GitHub issues and traffic referrers, and Brave Search mentions. Copilot CLI writes a ≤350-word digest. | An issue on this repo, which GitHub emails to watchers |

`.learn-cache/` is committed and already seeded, so the first scheduled run is a
real comparison. There is no Agent 365 "What's new" page on Learn; the docs
tables of contents stand in for it, so a page Microsoft adds shows up as a diff
line and the PR's "Needs a human decision" list will name it.

## Secrets to add (Settings → Secrets and variables → Actions)

No secret is required. Both workflows run on the automatic `GITHUB_TOKEN`.
The two below only add optional sources to the digest.

| Secret | Where to get it | Used by |
|---|---|---|
| `GOATCOUNTER_TOKEN` | rodneymhungu.goatcounter.com → Settings → API tokens (read-only, "statistics") | digest, visitor numbers |
| `BRAVE_API_KEY` | brave.com/search/api (free tier) | digest, public mentions |
| `COPILOT_PAT` | github.com/settings/personal-access-tokens/new → fine-grained PAT with **Copilot Requests** permission | not needed; the token fallback works |

`GITHUB_TOKEN` is provided automatically. Both workflows also request the
`copilot-requests: write` permission, and the 7 September run confirmed the CLI
falls back to `GITHUB_TOKEN` successfully on a personal account, so `COPILOT_PAT`
is not needed.

Any source whose secret is missing is reported as "unavailable" in the digest
rather than failing the run.

## Delivery

The digest is posted as an issue labelled `digest`, opened by the
`github-actions` bot. GitHub emails it to anyone watching the repository, so the
owner gets it without any mail credential stored here. It was an SMTP email to
Gmail until 7 September 2026; that needed a Google app password, which is a real
credential granting mailbox access, and the issue route removes it. The raw
signals are folded into a collapsed block at the bottom of the issue.

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

## Verified on the runner, 7 September 2026

The first scheduled `learn-drift` run compared all 55 cached pages, found no
drift and skipped the Copilot steps. Manual `feedback-digest` runs reached the
delivery step, and once the GoatCounter token existed, pulled real numbers.

- `copilot-requests: write` **does** work on a personal account with no
  `COPILOT_PAT`. The CLI authenticated with `GITHUB_TOKEN` and wrote a digest
  that followed the prompt. `COPILOT_PAT` is optional, not required.
- `--model claude-haiku-4.5` was accepted by the CLI on the runner.
- The GitHub traffic API returns **403 Forbidden** to `GITHUB_TOKEN`. Traffic
  needs push access, and workflow `permissions` has no `administration` key to
  grant it, so referrers cannot work without a personal access token. Either add
  one for that call or drop the referrer section from the digest.
- GoatCounter works, verified with a real token. Every API call must send
  `Content-Type: application/json`; without it the API answers **404** and an
  HTML error page rather than `{"error": ...}`. `start`/`end` as `YYYY-MM-DD`
  are accepted.
- Referrers are reduced to hostnames before they reach the digest, because the
  digest is a public issue and a full referrer can carry a reader's internal URL.
- The collector ignores issues labelled `digest`, so a digest never reports on
  the previous digests.
- Scheduled runs arrive late. On 7 September the 05:00 drift run started at
  09:59 and the 05:30 digest run at 10:39. That is normal for GitHub's cron on a
  quiet repository, not a fault.

## Still to check

- If a PR's diff is mostly boilerplate, extend the `CHROME` regex in
  `learn_watch.py`; the seed run was clean but Learn changes its chrome.

## Why it's split this way

The Learn watcher is deterministic so that most weeks cost nothing and the agent
only ever sees a bounded diff. The PR gate exists because the guide's value is
that every claim traces to Learn; a wrong GA/preview flip is worse than a stale
one. GitHub recommends Agentic Workflows (`gh-aw`) over raw `copilot` steps for
scheduled automation; if you move to that later, the two scripts stay the same
and only the YAML changes.
