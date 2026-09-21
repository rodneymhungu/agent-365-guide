#!/usr/bin/env python3
"""
feedback_collect.py — gathers every signal about the guide into one Markdown file
(feedback-input.md) for the digest step. Degrades gracefully: any source that
fails is reported as "unavailable" rather than crashing the run.

Sources
  1. GoatCounter  — visitors, per-section hash views, top referrers for the last 7 days
                    (same account as data-security-art-of-the-possible; filtered by path)
  2. GitHub       — stars, forks, watchers, open issues and open learn-drift pull
                    requests with their age (the traffic API is deliberately not
                    used: it needs push access, so a PAT, and GoatCounter already
                    covers referrers)
  3. Brave Search — public mentions of the guide URL or title
  4. Plan         — the target and this week's rotation focus from PLAN.md
  5. Article      — every second week, a LinkedIn article draft built from the
                    last fortnight's changes entries in a365-data.js, written to
                    linkedin-draft.md and appended to the digest issue verbatim

Anything that needs a human (analytics down, a drift pull request left open)
is collected into an "Action needed" section at the top of the file, and the
digest prompt repeats it first.

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

# The growth plan (PLAN.md). The digest reports visitors against the target and
# names the week's focus so nobody has to count weeks by hand.
TARGET = 2000
ROTATION_START = dt.date(2026, 9, 21)   # a Monday; focus 1 that week
ROTATION = [
    "1. Split a section into its own indexable page",
    "2. Build or extend a lookup table (licence, preview against GA, control to scenario)",
    "3. Write the changed-this-week note from the drift pull request",
    "4. Distribution: LinkedIn post, session follow-up, account outreach",
]
STALE_PR_DAYS = 2   # a learn-drift pull request older than this is called out
ARTICLE_EVERY_WEEKS = 2   # a LinkedIn article draft lands in the digest every second week
ARTICLE_LINK = SITE_URL + "#s10"
DRAFT_OUT = "linkedin-draft.md"

today = dt.date.today()
week_ago = today - dt.timedelta(days=7)
problems = []   # anything that needs a human, surfaced at the top of the digest


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
        problems.append("GOATCOUNTER_TOKEN is not set, so visitors and referrers are not being measured. "
                        "Add it under Settings, Secrets and variables, Actions.")
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
        lines.append(f"Last 7 days: **{visitors} visitors** on `{SITE_PATH}` against a target of {TARGET} "
                     f"({len(sections)} distinct sections opened by hash).")
        if hits.get("more"):
            lines.append("_(GoatCounter returned more than 100 paths; totals may be incomplete.)_")
        if len(pages) > 1:
            lines.append("")
            lines.append("Visitors per page:")
            for r in sorted(pages, key=lambda r: -r.get("count", 0)):
                lines.append(f"- `{r['path']}`: {r.get('count', 0)}")
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
        hint = ("Re-create a read-only 'statistics' API token while signed in to "
                f"https://{site}/ (Settings, API tokens), update the GOATCOUNTER_TOKEN "
                "repository secret, then run this workflow by hand.")
        if isinstance(e, HTTPError) and e.code == 404:
            # An unknown token answers 401 "unknown token", so a 404 means the token was
            # accepted but the site or data it points at was not found. Seen 14 Sep 2026.
            hint = ("The API answered 404 to a token it accepted, so the token is probably "
                    "bound to a different GoatCounter site. " + hint)
        problems.append("Visitor numbers and referrers are not being collected. " + hint)
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
        # Skip pull requests and the digests themselves, so the digest never reports on itself.
        issues = [i for i in issues if "pull_request" not in i
                  and not any(l.get("name") == "digest" for l in i.get("labels", []))]
        lines.append(f"\nOpen issues: {len(issues)}")
        for i in issues[:10]:
            lines.append(f"- #{i['number']} {i['title']} (updated {i['updated_at'][:10]}, {i['comments']} comments)")
    except (HTTPError, URLError) as e:
        lines.append(f"issues unavailable: {e}")
    # Open drift pull requests are the "changed this week" note waiting to be written.
    # One that sits for days is the ball being dropped, so it goes to the top.
    try:
        prs = get(f"{api}/pulls?state=open&per_page=20", h)
        drift = [p for p in prs if any(l.get("name") == "learn-drift" for l in p.get("labels", []))]
        lines.append(f"\nOpen learn-drift pull requests: {len(drift)}")
        for p in drift:
            opened = dt.date.fromisoformat(p["created_at"][:10])
            age = (today - opened).days
            lines.append(f"- #{p['number']} {p['title']} (open {age} days) {p['html_url']}")
            if age >= STALE_PR_DAYS:
                problems.append(f"Drift pull request #{p['number']} has been open {age} days: {p['html_url']}. "
                                "Review it, merge it, then log the change in PLAN.md.")
    except (HTTPError, URLError, ValueError, KeyError) as e:
        lines.append(f"pull requests unavailable: {e}")
    return "\n".join(lines)


# ---------- 4. Plan ----------
def rotation_week():
    return max(0, (today - ROTATION_START).days // 7)


def plan():
    weeks = rotation_week()
    focus = ROTATION[weeks % len(ROTATION)]
    draft = "This digest carries a LinkedIn article draft." if weeks % ARTICLE_EVERY_WEEKS == 0 else "No article draft this week; the next one comes with next week's digest."
    return (f"Target: {TARGET} high-value visitors a week (PLAN.md).\n"
            f"Week {weeks + 1} of the rotation. This week's focus: {focus}\n"
            f"Every week: check referrers, not just paths. {draft}")


# ---------- 3. Brave web search ----------
def brave():
    key = os.environ.get("BRAVE_API_KEY")
    if not key:
        problems.append("BRAVE_API_KEY is not set, so public mentions are never searched (issue #10). "
                        "Free tier at brave.com/search/api; add it under Settings, Secrets and variables, Actions.")
        return "BRAVE_API_KEY not set; public mention search skipped (issue #10)."
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


# ---------- 5. LinkedIn article draft ----------
def article_draft(weeks):
    """Every second week, write a LinkedIn article draft from the changes entries
    in a365-data.js dated within the last two weeks. Deterministic on purpose:
    no model touches it, so the wording is the guide's own. Returns the draft
    text, or None on a week without a draft."""
    if weeks % ARTICLE_EVERY_WEEKS:
        return None
    try:
        with open("a365-data.js", encoding="utf-8") as f:
            js = f.read()
    except OSError:
        return None
    since = today - dt.timedelta(days=14)
    items = []
    for m in re.finditer(r'\{\s*date:\s*"([^"]+)"(?:,\s*section:\s*"([^"]+)")?,\s*text:\s*"((?:[^"\\]|\\.)*)"', js):
        try:
            d = dt.datetime.strptime(m.group(1), "%d %B %Y").date()
        except ValueError:
            continue
        if d >= since:
            items.append((d, m.group(2), m.group(3).replace('\\"', '"')))
    items.sort(reverse=True)
    lines = ["# LinkedIn article draft (every second week; copy, edit, post from the computer)", "",
             "Before posting: run ai-writing-review on this draft and decide each flag.", "",
             "Headline: What changed in the last two weeks in the Agent 365 field guide", "",
             "Updated this fortnight: the Agent 365 field guide for security and compliance engineers.", ""]
    if items:
        lines.append("What moved:")
        lines.append("")
        for d, sec, text in items[:6]:
            lines.append(f"\u2022 {text}")
        lines.append("")
    else:
        lines.append("No cited Learn page changed in the last two weeks. Write this one about a single section instead; the most-opened sections are listed under Visitors above.")
        lines.append("")
    lines += ["Every claim links to Learn. Status badges change the week Microsoft changes a page.", "",
              "See what changed and what you can deploy today:", ARTICLE_LINK, "",
              "Cover image: crop the table or figure the article is about; see distribution/README.md.",
              "When posted, save the article as distribution/<date>-linkedin.md with the URL on its Posted line and log it under focus 4 in PLAN.md."]
    return "\n".join(lines)


def main():
    md = f"# Feedback inputs for {TITLE}\n\nWindow: {week_ago} to {today}. Site: {SITE_URL}\n\n"
    body = section("Plan", plan())
    body += section("Visitors (GoatCounter)", goatcounter())
    body += section("Repository (GitHub)", github())
    body += section("Public mentions (Brave Search, past week)", brave())
    if problems:
        md += section("Action needed", "\n".join(f"- {p}" for p in problems))
    md += body
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(md)
    draft = article_draft(rotation_week())
    if draft:
        with open(DRAFT_OUT, "w", encoding="utf-8") as f:
            f.write(draft + "\n")
    print(md[:2000], file=sys.stderr)


if __name__ == "__main__":
    main()
