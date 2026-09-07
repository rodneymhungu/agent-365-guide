#!/usr/bin/env python3
"""
feedback_collect.py — gathers every signal about the guide into one Markdown file
(feedback-input.md) for the digest step. Degrades gracefully: any source that
fails is reported as "unavailable" rather than crashing the run.

Sources
  1. GoatCounter  — visitors, per-section hash views, top referrers for the last 7 days
                    (same account as data-security-art-of-the-possible; filtered by path)
  2. GitHub       — stars delta, open issues/discussions, and the repo traffic API
                    (referrers and popular paths, last 14 days)
  3. Brave Search — public mentions of the guide URL or title

Env vars
  GOATCOUNTER_TOKEN   API token from https://rodneymhungu.goatcounter.com/user/api
  GOATCOUNTER_SITE    default rodneymhungu.goatcounter.com
  GITHUB_TOKEN        provided by Actions
  GITHUB_REPOSITORY   provided by Actions (owner/repo)
  BRAVE_API_KEY       https://brave.com/search/api/  (free tier is enough)
"""
import datetime as dt, json, os, re, sys, urllib.parse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

SITE_PATH = "/agent-365-guide"
SITE_URL = "https://rodneymhungu.github.io/agent-365-guide/"
TITLE = "Agent 365 for security and compliance engineers"
OUT = "feedback-input.md"

today = dt.date.today()
week_ago = today - dt.timedelta(days=7)


def get(url, headers=None, timeout=30):
    req = Request(url, headers={"User-Agent": "agent-365-guide-feedback/1.0", **(headers or {})})
    with urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def describe(e):
    """Turn an HTTPError into 'HTTP 404: <what the server said>' so the digest
    explains itself; other errors are returned as-is."""
    if isinstance(e, HTTPError):
        try:
            body = e.read().decode("utf-8", "replace").strip()
        except Exception:
            body = ""
        try:
            body = json.loads(body).get("error") or body
        except ValueError:
            body = re.sub(r"<[^>]+>", " ", body)
        body = re.sub(r"\s+", " ", body).strip()[:200]
        return f"HTTP {e.code} {e.reason}" + (f": {body}" if body else "")
    return str(e)


def section(title, body):
    return f"## {title}\n\n{body.strip()}\n\n"


# ---------- 1. GoatCounter ----------
# API shapes verified against https://www.goatcounter.com/api.json on 5 September 2026:
#   GET /api/v0/stats/hits?start&end&limit(<=100)   -> {"hits":[{"path","path_id","count","stats":[{"day","daily"}]}],"more"}
#   GET /api/v0/stats/toprefs?start&end&include_paths=<path_id>... -> {"stats":[{"name","count"}]}
# "count" is visitors (GoatCounter does not expose raw pageviews via the API). There is no
# path-prefix filter, so we pull the top 100 paths and filter client-side.
def referrer_host(name):
    """Reduce a referrer to its hostname. GoatCounter may return a full URL or a
    bare 'host/path'; both are trimmed so no path or query ever reaches the digest."""
    if not name:
        return "(direct)"
    name = name.strip()
    if "://" in name:
        name = urllib.parse.urlsplit(name).netloc or name
    return name.split("/", 1)[0].split("?", 1)[0].lower() or "(direct)"

def goatcounter():
    tok = os.environ.get("GOATCOUNTER_TOKEN")
    site = os.environ.get("GOATCOUNTER_SITE", "rodneymhungu.goatcounter.com")
    if not tok:
        return "GOATCOUNTER_TOKEN not set."
    # GoatCounter requires Content-Type: application/json on every API call; without
    # it errors come back as an HTML page instead of {"error": ...}.
    h = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}
    base = f"https://{site}/api/v0"
    rng = {"start": week_ago.isoformat(), "end": today.isoformat()}
    lines = []
    try:
        hits = get(f"{base}/stats/hits?" + urllib.parse.urlencode({**rng, "limit": 100}), h)
        rows = [r for r in hits.get("hits", []) if (r.get("path") or "").startswith(SITE_PATH)]
        pages = [r for r in rows if "#" not in r["path"]]
        sections = [r for r in rows if "#" in r["path"]]
        visitors = sum(r.get("count", 0) for r in pages)
        lines.append(f"Last 7 days: **{visitors} visitors** on `{SITE_PATH}` "
                     f"({len(sections)} distinct sections opened by hash).")
        if hits.get("more"):
            lines.append("_(GoatCounter returned more than 100 paths; totals may be incomplete.)_")
        by_day = {}
        for r in pages:
            for d in r.get("stats", []):
                by_day[d.get("day")] = by_day.get(d.get("day"), 0) + d.get("daily", 0)
        if by_day:
            lines.append("")
            lines.append("Visitors per day: " + ", ".join(f"{k[5:]}: {v}" for k, v in sorted(by_day.items())))
        if sections:
            lines.append("")
            lines.append("| Section (by hash) | Visitors |")
            lines.append("|---|---|")
            for r in sorted(sections, key=lambda r: -r.get("count", 0))[:15]:
                lines.append(f"| {r['path'].split('#', 1)[1]} | {r.get('count', 0)} |")
        ids = [r["path_id"] for r in rows if "path_id" in r]
        if ids:
            q = urllib.parse.urlencode({**rng, "limit": 10, "include_paths": ids}, doseq=True)
            refs = get(f"{base}/stats/toprefs?{q}", h).get("stats", [])
            if refs:
                # Hostnames only. The digest is posted as a public issue, and a full
                # referrer can carry a reader's internal wiki or intranet URL.
                by_host = {}
                for r in refs:
                    host = referrer_host(r.get("name"))
                    by_host[host] = by_host.get(host, 0) + int(r.get("count", 0) or 0)
                lines.append("")
                lines.append("Top referrers (hostnames only):")
                for host, n in sorted(by_host.items(), key=lambda kv: -kv[1])[:10]:
                    lines.append(f"- {host}: {n}")
    except (HTTPError, URLError, ValueError, KeyError) as e:
        lines.append(f"GoatCounter unavailable: {describe(e)}  (see https://www.goatcounter.com/help/api)")
    return "\n".join(lines)


# ---------- 2. GitHub ----------
def github():
    tok = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY", "rodneymhungu/agent-365-guide")
    if not tok:
        return "GITHUB_TOKEN not set."
    h = {"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json"}
    api = f"https://api.github.com/repos/{repo}"
    lines = []
    try:
        r = get(api, h)
        lines.append(f"Stars: {r.get('stargazers_count')} · Forks: {r.get('forks_count')} · Watchers: {r.get('subscribers_count')}")
    except (HTTPError, URLError) as e:
        lines.append(f"repo metadata unavailable: {e}")
    try:
        issues = get(f"{api}/issues?state=open&sort=updated&per_page=20", h)
        issues = [i for i in issues if "pull_request" not in i]
        lines.append(f"\nOpen issues: {len(issues)}")
        for i in issues[:10]:
            lines.append(f"- #{i['number']} {i['title']} (updated {i['updated_at'][:10]}, {i['comments']} comments)")
    except (HTTPError, URLError) as e:
        lines.append(f"issues unavailable: {e}")
    # Traffic API needs push access; GITHUB_TOKEN on your own repo has it.
    try:
        refs = get(f"{api}/traffic/popular/referrers", h)
        if refs:
            lines.append("\nGitHub traffic referrers (14 days):")
            for r in refs[:10]:
                lines.append(f"- {r['referrer']}: {r['count']} views, {r['uniques']} unique")
        views = get(f"{api}/traffic/views?per=week", h)
        lines.append(f"\nRepo page views (14 days): {views.get('count')} total, {views.get('uniques')} unique")
    except (HTTPError, URLError) as e:
        lines.append(f"\ntraffic API unavailable: {describe(e)}")
    return "\n".join(lines)


# ---------- 3. Brave web search ----------
def brave():
    key = os.environ.get("BRAVE_API_KEY")
    if not key:
        return "BRAVE_API_KEY not set — public mention search skipped."
    h = {"X-Subscription-Token": key, "Accept": "application/json"}
    queries = [
        f'"{SITE_URL}"',
        f'"{TITLE}"',
        '"agent-365-guide" mhungu',
        'Rodney Mhungu "Agent 365"',
    ]
    seen, lines = set(), []
    for q in queries:
        try:
            d = get("https://api.search.brave.com/res/v1/web/search?" +
                    urllib.parse.urlencode({"q": q, "count": 10, "freshness": "pw"}), h)
            for r in d.get("web", {}).get("results", []):
                u = r.get("url")
                if u and u not in seen and "rodneymhungu.github.io" not in u:
                    seen.add(u)
                    lines.append(f"- [{r.get('title','')}]({u}) — {r.get('description','')[:200]}")
        except (HTTPError, URLError, ValueError) as e:
            lines.append(f"- query `{q}` failed: {e}")
    return "\n".join(lines) if lines else "No new public mentions found in the past week."


def main():
    md = f"# Feedback inputs for {TITLE}\n\nWindow: {week_ago} to {today}. Site: {SITE_URL}\n\n"
    md += section("Visitors (GoatCounter)", goatcounter())
    md += section("Repository (GitHub)", github())
    md += section("Public mentions (Brave Search, past week)", brave())
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(md)
    print(md[:2000], file=sys.stderr)


if __name__ == "__main__":
    main()
