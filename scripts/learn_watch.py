#!/usr/bin/env python3
"""
learn_watch.py — deterministic drift detector for the Agent 365 guide.

1. Pulls every learn.microsoft.com URL that index.html links to (plus EXTRA_URLS).
2. Fetches each page, keeps the <main> content, normalises it to plain text.
3. Compares against .learn-cache/<id>.txt from the last run.
4. Writes learn-diff.md (a unified diff per changed page, with the guide
   sections that cite that page) and refreshes the cache.
5. Exits 0 always; prints `changed=true|false` for the workflow to read.

No LLM, no third-party packages. Runs in about a minute for ~50 pages.
"""
import difflib, hashlib, html, json, os, re, sys, time
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")
CACHE = os.path.join(ROOT, ".learn-cache")
REPORT = os.path.join(ROOT, "learn-diff.md")
UA = "agent-365-guide-watch/1.0 (+https://rodneymhungu.github.io/agent-365-guide/)"

# Pages the guide should track but does not (yet) link to.
# There is no Agent 365 "What's new" page on Learn (checked 5 September 2026), so the
# docs-set tables of contents stand in for it: a new or renamed page shows up as a
# diff line here before any prose page changes.
EXTRA_URLS = [
    "https://learn.microsoft.com/en-us/microsoft-agent-365/toc.json",
    "https://learn.microsoft.com/en-us/security/security-for-ai/toc.json",
    "https://learn.microsoft.com/en-us/windows-365/agents/whats-new",
    # Licensing prerequisites live here, not on Learn. The page serves a 4 KB
    # JavaScript shell to unknown user agents and full HTML to a browser UA,
    # so fetch() switches UA for hosts other than learn.microsoft.com.
    "https://www.microsoft.com/licensing/faqs/122",
]
BROWSER_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

MAX_DIFF_LINES = 160   # per page; keeps the agent prompt bounded


class MainText(HTMLParser):
    """Collects text inside <main>, skipping script/style/nav/aside."""
    SKIP = {"script", "style", "nav", "aside", "header", "footer", "noscript", "svg"}
    BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "tr", "td", "th", "pre", "div"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_main = False
        self.skip_depth = 0
        self.out = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "main" or a.get("id") in ("main", "main-content"):
            self.in_main = True
        if self.in_main and tag in self.SKIP:
            self.skip_depth += 1
        if self.in_main and tag in self.BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if self.in_main and tag in self.SKIP and self.skip_depth:
            self.skip_depth -= 1
        if tag == "main":
            self.in_main = False

    def handle_data(self, data):
        if self.in_main and not self.skip_depth:
            self.out.append(data)


# Learn page chrome that lands inside <main>; seen in the seed run on 5 September 2026.
CHROME = re.compile(r"(Feedback|Was this page helpful\?|Yes|No|Table of contents|Read in English|Save|Print|Share|Edit|"
                    r"Skip to main content|Exit editor mode|Ask Learn|Reading mode|Add|Add to Plans|Copy Markdown|Note|"
                    r"Summarize this article for me|Need help with this topic\?|Suggest a fix\?|Additional resources|"
                    r"Want to try using Ask Learn to clarify or guide you through this topic\?|"
                    r"Access to this page requires authorization\. You can try (signing in or )?changing directories\.|"
                    r"Last updated on|\d{4}-\d{2}-\d{2})")


def toc_lines(raw_json: str) -> str:
    """Render a Learn toc.json as one 'title -> href' line per entry, indented by depth."""
    out = []

    def walk(items, depth=0):
        for it in items or []:
            title = (it.get("toc_title") or "").strip()
            href = (it.get("href") or "").split("?")[0]
            out.append(f"{'  ' * depth}{title} -> {href}".rstrip())
            walk(it.get("children"), depth + 1)

    walk(json.loads(raw_json).get("items", []))
    return "\n".join(out)


def normalise(raw_html: str, url: str = "") -> str:
    if url.endswith(".json"):
        try:
            return toc_lines(raw_html)
        except (ValueError, AttributeError):
            pass
    p = MainText()
    p.feed(raw_html)
    text = "".join(p.out) if p.out else re.sub(r"<[^>]+>", " ", raw_html)
    text = html.unescape(text)
    lines = []
    for ln in text.splitlines():
        ln = re.sub(r"[ \t]+", " ", ln).strip()
        if ln and not CHROME.fullmatch(ln):
            lines.append(ln)
    return "\n".join(lines)


def fetch(url: str, retries: int = 3):
    for i in range(retries):
        try:
            ua = UA if "learn.microsoft.com" in url else BROWSER_UA
            req = Request(url, headers={"User-Agent": ua, "Accept-Language": "en-US,en;q=0.9"})
            with urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(2 * (i + 1))
        except URLError:
            time.sleep(2 * (i + 1))
    return None


def url_id(url: str) -> str:
    return hashlib.sha1(url.encode()).hexdigest()[:16]


def sections_citing(index_html: str, url: str):
    """Guide section ids (e.g. s6-2) whose HTML contains this URL."""
    ids = []
    heads = list(re.finditer(r'<section[^>]+id="(s\d+(?:-\d+)?)"', index_html))
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(index_html)
        if url in index_html[m.start():end]:
            ids.append(m.group(1))
    return ids


def main() -> int:
    with open(INDEX, encoding="utf-8") as f:
        index_html = f.read()

    found = {u.rstrip(".,") for u in re.findall(r'https://learn\.microsoft\.com/[^"\'<>\s)]+', index_html)}
    urls = sorted(found | set(EXTRA_URLS))
    os.makedirs(CACHE, exist_ok=True)

    changed, new, gone, unchanged = [], [], [], 0
    for url in urls:
        path = os.path.join(CACHE, f"{url_id(url)}.txt")
        raw = fetch(url)
        if raw is None:
            gone.append(url)
            continue
        now = normalise(raw, url)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                before = f.read()
            if before == now:
                unchanged += 1
            else:
                diff = list(difflib.unified_diff(
                    before.splitlines(), now.splitlines(),
                    fromfile="previous", tofile="current", lineterm="", n=2))
                changed.append((url, diff))
        else:
            new.append(url)
        with open(path, "w", encoding="utf-8") as f:
            f.write(now)
        time.sleep(0.5)  # be polite to Learn

    with open(os.path.join(CACHE, "index.json"), "w", encoding="utf-8") as f:
        json.dump({url_id(u): u for u in urls}, f, indent=2)

    any_change = bool(changed or gone)
    with open(REPORT, "w", encoding="utf-8") as f:
        f.write("# Learn drift report\n\n")
        f.write(f"Checked {len(urls)} pages · {len(changed)} changed · {len(new)} newly cached · "
                f"{len(gone)} unreachable · {unchanged} unchanged\n\n")
        if gone:
            f.write("## Unreachable (404 or repeated failure)\n\n")
            for u in gone:
                f.write(f"- {u} — cited in: {', '.join(sections_citing(index_html, u)) or 'sources list only'}\n")
            f.write("\n")
        for url, diff in changed:
            secs = sections_citing(index_html, url)
            f.write(f"## {url}\n\nCited in guide sections: {', '.join(secs) if secs else 'sources list only'}\n\n")
            f.write("```diff\n" + "\n".join(diff[:MAX_DIFF_LINES]) + "\n```\n")
            if len(diff) > MAX_DIFF_LINES:
                f.write(f"\n_…{len(diff) - MAX_DIFF_LINES} more diff lines truncated._\n")
            f.write("\n")
        if new and not changed:
            f.write("## First run\n\nCache seeded; nothing to compare yet.\n")

    print(f"changed={'true' if any_change else 'false'}")
    print(f"pages={len(urls)} changed={len(changed)} new={len(new)} gone={len(gone)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
