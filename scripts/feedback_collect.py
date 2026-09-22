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
  3. Web search   — public mentions of the guide URL or title (Google Programmable
                    Search, free, or Brave, metered)
  4. Plan         — the target and this week's rotation focus from PLAN.md
  5. Article      — every second week, a LinkedIn article draft built from the
                    last fortnight's changes entries in a365-data.js, written to
                    linkedin-draft.md and appended to the digest issue verbatim
  6. Social       — same weeks, a 300-character version in social-post.txt for
                    scripts/social_post.py (Bluesky, Mastodon)
  7. Questions    — threads from the last week on Reddit, Microsoft Q&A and Tech
                    Community that a guide section answers (Brave Search)

Anything that needs a human (analytics down, a drift pull request left open)
is collected into an "Action needed" section at the top of the file, and the
digest prompt repeats it first.

Env vars
  GOATCOUNTER_TOKEN   API token from https://rodneymhungu.goatcounter.com/user/api
  GOATCOUNTER_SITE    default rodneymhungu.goatcounter.com
  GITHUB_TOKEN        provided by Actions
  GITHUB_REPOSITORY   provided by Actions (owner/repo)
  GOOGLE_CSE_KEY, GOOGLE_CSE_ID   Google Programmable Search (free, 100 queries a day)
  BRAVE_API_KEY       https://brave.com/search/api/  (card on file, metered; alternative)
"""
import datetime as dt, json, os, re, sys, time, urllib.parse
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


def get(url, headers=None, timeout=30, retries=3):
    """GET JSON. GoatCounter's API answers an occasional 404 or 429 to a request that
    succeeds seconds later (seen 21 and 22 September 2026), so transient codes are
    retried with a short back-off before the source is reported as unavailable."""
    req = Request(url, headers={"User-Agent": "agent-365-guide-feedback/1.0", **(headers or {})})
    for attempt in range(retries + 1):
        try:
            with urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except HTTPError as e:
            if e.code in (404, 429, 500, 502, 503, 504) and attempt < retries:
                time.sleep((3, 8, 15)[attempt])
                continue
            raise


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
    # GoatCounter's end date is exclusive: "end=today" returns nothing for today
    # (found 22 September 2026). Ask up to tomorrow so the run day is included.
    rng = {"start": week_ago.isoformat(), "end": (today + dt.timedelta(days=1)).isoformat()}
    lines = []
    try:
        hits = get(f"{base}/stats/hits?" + urllib.parse.urlencode({**rng, "limit": 100}), h)
        # Only the guide's real pages count as visits: the root and any *.html beside it.
        # Anything else under the prefix (a stray test path, a typo) is ignored.
        def is_page(path):
            rest = path[len(SITE_PATH):].split("#", 1)[0].strip("/")
            return rest == "" or rest.endswith(".html")
        rows = [r for r in hits.get("hits", []) if (r.get("path") or "").startswith(SITE_PATH) and is_page(r["path"])]
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


# ---------- 3. Web search (Google Programmable Search, or Brave) ----------
# Google's Custom Search JSON API: 100 queries a day free, no card, needs an API key
# and a Programmable Search Engine id set to search the whole web. Brave dropped its
# free tier in February 2026 (card on file, metered). Either works; Google is tried first.
def search_provider():
    if os.environ.get("GOOGLE_CSE_KEY") and os.environ.get("GOOGLE_CSE_ID"):
        return "google"
    if os.environ.get("BRAVE_API_KEY"):
        return "brave"
    return None


def web_search(q, past_week=True):
    """Return [(title, url, snippet)] for q, restricted to the past week."""
    prov = search_provider()
    if prov == "google":
        d = get("https://www.googleapis.com/customsearch/v1?" + urllib.parse.urlencode(
            {"key": os.environ["GOOGLE_CSE_KEY"], "cx": os.environ["GOOGLE_CSE_ID"], "q": q, "num": 10,
             **({"dateRestrict": "w1"} if past_week else {})}))
        return [(r.get("title", ""), r.get("link", ""), r.get("snippet", "")) for r in d.get("items", [])]
    if prov == "brave":
        d = get("https://api.search.brave.com/res/v1/web/search?" + urllib.parse.urlencode(
            {"q": q, "count": 10, **({"freshness": "pw"} if past_week else {})}),
            {"X-Subscription-Token": os.environ["BRAVE_API_KEY"], "Accept": "application/json"})
        return [(r.get("title", ""), r.get("url", ""), r.get("description", "")) for r in d.get("web", {}).get("results", [])]
    return []


NO_SEARCH = ("No web search key set; skipped. Add GOOGLE_CSE_KEY and GOOGLE_CSE_ID (free, 100 queries a day) "
             "or BRAVE_API_KEY (card on file). See scripts/README.md and issue #10.")


def mentions():
    if not search_provider():
        problems.append("Public mentions and the questions list are not being searched. " + NO_SEARCH)
        return NO_SEARCH
    queries = [f'"{SITE_URL}"', f'"{TITLE}"', '"agent-365-guide" mhungu', 'Rodney Mhungu "Agent 365"']
    seen, lines = set(), []
    for q in queries:
        try:
            for t, u, desc in web_search(q):
                if u and u not in seen and "rodneymhungu.github.io" not in u:
                    seen.add(u)
                    lines.append(f"- [{t}]({u}): {desc[:200]}")
        except (HTTPError, URLError, ValueError) as e:
            lines.append(f"- query `{q}` failed: {describe(e) if isinstance(e, HTTPError) else e}")
    return "\n".join(lines) if lines else "No new public mentions found in the past week."


# ---------- 5. LinkedIn article draft ----------
SHORT = "agent-365-guide/"   # visible shortened section link, a navigation label (format rule 4)


def article_draft(weeks):
    """Every second week, write a LinkedIn article draft in the field-guide
    release-note format (distribution/README.md) from the changes entries in
    a365-data.js dated within the last two weeks. Deterministic on purpose:
    no model touches it. Returns the draft text, or None on an off week."""
    if weeks % ARTICLE_EVERY_WEEKS:
        return None
    try:
        with open("a365-data.js", encoding="utf-8") as f:
            js = f.read()
    except OSError:
        return None
    since = today - dt.timedelta(days=14)
    learn, guide = [], []
    pat = re.compile(r'\{\s*date:\s*"([^"]+)"(?:,\s*section:\s*"([^"]+)")?(?:,\s*kind:\s*"([^"]+)")?,\s*text:\s*"((?:[^"\\]|\\.)*)"')
    for m in pat.finditer(js):
        try:
            d = dt.datetime.strptime(m.group(1), "%d %B %Y").date()
        except ValueError:
            continue
        if d < since:
            continue
        item = (d, m.group(2), m.group(4).replace('\\"', '"'))
        (guide if m.group(3) == "guide" else learn).append(item)
    learn.sort(reverse=True); guide.sort(reverse=True)

    def bullet(text, sec):
        # Bold the first sentence: it names the product and the capability.
        m = re.match(r"(.+?[.:])\s+(.*)", text)
        head, rest = (m.group(1), m.group(2)) if m else (text, "")
        link = f" {SHORT}#{sec}" if sec else ""
        return f"• **{head.rstrip('.:')}.** {rest}{link}".rstrip()

    learn = learn[:6]
    n = len(learn)
    words = {0: "No", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six"}
    lines = ["# LinkedIn article draft (every second week; copy, edit, post from the computer)", "",
             "Before posting: run ai-writing-review on this draft and decide each flag.", "",
             "Headline: What changed this week in the Agent 365 field guide", "",
             "Updated this week: the Agent 365 field guide for security and compliance engineers.", ""]
    if learn:
        lines.append(f"{words.get(n, str(n))} thing{'s' if n != 1 else ''} moved on Microsoft Learn, and the guide moved with {'them' if n != 1 else 'it'}:")
        lines.append("")
        for d, sec, text in learn:
            lines.append(bullet(text, sec))
        lines.append("")
    else:
        lines.append("No cited Learn page changed in the last two weeks. Write this one about a single section instead; the most-opened sections are listed under Visitors above.")
        lines.append("")
    if guide:
        parts = []
        for d, sec, text in guide[:3]:
            parts.append(f"{text.rstrip('.')} ({SHORT}#{sec})" if sec else text.rstrip('.'))
        lines.append("• Also new to the guide: " + "; ".join(parts) + ".")
        lines.append("")
    lines += ["Every claim in this guide links to Learn. GA/Preview status badges follow Microsoft's release notes, checked every Monday.", "",
              "See what changed and what you can deploy today: " + ARTICLE_LINK, "",
              "Cover image: a Learn screenshot or the figure the article is about; see distribution/README.md.",
              "When posted, save the article as distribution/<date>-linkedin.md with the URL on its Posted line and log it under focus 4 in PLAN.md."]
    return "\n".join(lines)


SOCIAL_OUT = "social-post.txt"
BLUESKY_LIMIT = 300


def social_text(weeks):
    """A three-line version of the release note for Bluesky and Mastodon, under
    300 characters, only on article weeks with at least one Learn change."""
    if weeks % ARTICLE_EVERY_WEEKS:
        return None
    try:
        js = open("a365-data.js", encoding="utf-8").read()
    except OSError:
        return None
    since = today - dt.timedelta(days=14)
    firsts = []
    for m in re.finditer(r'\{\s*date:\s*"([^"]+)"(?:,\s*section:\s*"([^"]+)")?(?:,\s*kind:\s*"([^"]+)")?,\s*text:\s*"((?:[^"\\]|\\.)*)"', js):
        try:
            d = dt.datetime.strptime(m.group(1), "%d %B %Y").date()
        except ValueError:
            continue
        if d >= since and m.group(3) != "guide":
            first = re.match(r"(.+?[.:])(\s|$)", m.group(4))
            firsts.append((first.group(1) if first else m.group(4)).rstrip(".:"))
    if not firsts:
        return None
    head = "Agent 365 field guide, updated. What moved on Microsoft Learn:"
    tail = f"What you can deploy today: {ARTICLE_LINK}"
    def short(t, n=72):
        return t if len(t) <= n else t[:n - 1].rstrip() + "…"
    bullets = [f"• {short(f)}" for f in firsts[:2]]
    text = head + "\n" + "\n".join(bullets) + "\n" + tail
    if len(text) > BLUESKY_LIMIT:
        text = head + "\n" + bullets[0] + "\n" + tail
    return text


# ---------- 6. Questions the guide could answer ----------
# Threads from the last week on Reddit, Microsoft Q&A and Tech Community that ask
# what a guide section explains. The owner answers two a week and cites the
# section; the guide itself is never posted. Needs BRAVE_API_KEY.
SECTION_HINTS = [
    (r"licen[cs]|e7|add-on|pricing", "2.1 What the licence unlocks", "s2-1"),
    (r"conditional access|agent id|agent identit|blueprint", "7.1 Identity", "s7-1"),
    (r"dlp|sensitivity label|purview|insider risk", "7.2 Data", "s7-2"),
    (r"real-time protection|prompt injection|defender xdr|security for ai", "7.3 Threats", "s7-3"),
    (r"local agent|claude code|openclaw|runtime protection|intune", "7.4 Local agents on the endpoint", "s7-4"),
    (r"mcp|global secure access|prompt shield", "7.5 Network controls on agent traffic", "s7-5"),
    (r"access package|sponsor|lifecycle workflow", "6.6 Identity governance in Entra", "s6-6"),
    (r"policy template", "6.2 Policy templates", "s6-2"),
    (r"shadow ai", "5.5 Shadow AI and local agents on endpoints", "s5-5"),
    (r"registry|inventory|agent map", "5.1 The registry and the overview page", "s5-1"),
    (r"audit|ediscovery|retention|communication compliance", "6.7 Compliance in Purview", "s6-7"),
]


def questions():
    if not search_provider():
        return NO_SEARCH
    queries = [
        '"Agent 365" (site:reddit.com OR site:learn.microsoft.com/answers OR site:techcommunity.microsoft.com)',
        '"Entra Agent ID" OR "agent identity" conditional access site:reddit.com',
        '"MCP" Defender OR Purview OR "Global Secure Access" agents site:reddit.com',
        '"local AI agents" OR "Claude Code" Defender Intune site:reddit.com',
        '"Agent 365" licensing OR "E7" site:reddit.com',
    ]
    seen, lines = set(), []
    for q in queries:
        try:
            results = web_search(q)
        except (HTTPError, URLError, ValueError) as e:
            lines.append(f"- query `{q[:50]}` failed: {describe(e) if isinstance(e, HTTPError) else e}"); continue
        for t, u, desc in results:
            if not u or u in seen or "rodneymhungu" in u:
                continue
            seen.add(u)
            blob = (t + " " + desc).lower()
            hint = next(((name, sid) for pat, name, sid in SECTION_HINTS if re.search(pat, blob)), None)
            where = "Reddit" if "reddit.com" in u else "Microsoft Q&A" if "learn.microsoft.com" in u else "Tech Community" if "techcommunity" in u else "web"
            lines.append(f"- [{t[:90]}]({u}) ({where})" + (f": answer with {hint[0]}, `{SITE_URL}#{hint[1]}`" if hint else ""))
    lines = lines[:8]
    return "\n".join(lines) if lines else "No new threads found this week."


def main():
    md = f"# Feedback inputs for {TITLE}\n\nWindow: {week_ago} to {today}. Site: {SITE_URL}\n\n"
    body = section("Plan", plan())
    body += section("Visitors (GoatCounter)", goatcounter())
    body += section("Repository (GitHub)", github())
    body += section("Public mentions (web search, past week)", mentions())
    body += section("Questions the guide could answer (past week)", questions())
    if problems:
        md += section("Action needed", "\n".join(f"- {p}" for p in problems))
    md += body
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(md)
    draft = article_draft(rotation_week())
    if draft:
        with open(DRAFT_OUT, "w", encoding="utf-8") as f:
            f.write(draft + "\n")
    social = social_text(rotation_week())
    if social:
        with open(SOCIAL_OUT, "w", encoding="utf-8") as f:
            f.write(social + "\n")
    print(md[:2000], file=sys.stderr)


if __name__ == "__main__":
    main()
