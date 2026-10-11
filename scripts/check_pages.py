#!/usr/bin/env python3
"""
check_pages.py — a chapter published on its own page must match the guide,
every video chapter button must jump somewhere real, and the static copies of
the data values must match a365-data.js.

licensing.html carries chapter 2 (<section class="block" id="s2">) of index.html
so that the chapter is indexable on its own. The markup must stay identical in
both files, or the two pages drift apart and one of them lies. This compares
the chapter block in each pair of files, ignoring whitespace and any element
marked data-page-only (the cross-links that only make sense on one page).

Exit 1 and print the first differing line when they diverge. No dependencies.

Video chapters: each <div class="yt"> carries chapter buttons with data-t, the
start in seconds, and a label that opens with the same time as mm:ss. A button
with data-t="0" sends every chapter to the start of the video, which is how the
6.7 and 7.5 chapters shipped broken in October 2026. Each button must have a
non-zero start that matches its label, and starts must increase down the list.

Static values: guide.js fills every element carrying data-val from a365-data.js
after the page loads, so a crawler, a LinkedIn preview or a plain text fetch
would otherwise see an empty review date and empty prices. Each such element
therefore also carries the current value as its text, the JSON-LD dateModified
in each page's head carries the review date in ISO form, and sitemap.xml
carries the same date as lastmod. This script fails when any copy disagrees
with the data file. Run it with --fix to rewrite every copy from the data file
instead of editing them by hand.
"""
import difflib, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (standalone page, section id it carries). Add a row when a chapter is split out.
PAIRS = [
    ("licensing.html", "s2"),
]


def block(html: str, sec_id: str) -> str:
    m = re.search(rf'<section class="block" id="{sec_id}">.*?\n</section>\n', html, re.S)
    if not m:
        raise SystemExit(f"section #{sec_id} not found")
    text = m.group(0)
    text = re.sub(r'<(\w+)[^>]*\bdata-page-only\b[^>]*>.*?</\1>\s*', '', text, flags=re.S)
    return re.sub(r"\s+", " ", text).strip()


def check_chapters(html: str, page: str) -> int:
    bad = 0
    for box in re.finditer(r'<div class="yt" data-id="([^"]+)"[^>]*>.*?<div class="chapters">(.*?)</div>', html, re.S):
        vid, chapters = box.group(1), box.group(2)
        buttons = re.findall(r'<button type="button" data-t="(\d*)">\s*(?:(\d+):(\d\d))?', chapters)
        last = 0
        for t, mm, ss in buttons:
            start = int(t) if t else 0
            if start <= 0:
                print(f"BAD CHAPTER: {page} video {vid}: a chapter starts at 0, so it jumps to the start of the video")
                bad += 1
            elif mm is None:
                print(f"BAD CHAPTER: {page} video {vid}: chapter at {start}s has no mm:ss in its label")
                bad += 1
            elif int(mm) * 60 + int(ss) != start:
                print(f"BAD CHAPTER: {page} video {vid}: label says {mm}:{ss} but data-t is {start}")
                bad += 1
            elif start <= last:
                print(f"BAD CHAPTER: {page} video {vid}: chapter at {start}s does not come after {last}s")
                bad += 1
            last = max(last, start)
        if not bad:
            print(f"ok: {page} video {vid} has {len(buttons)} chapters with real starts")
    return bad


MONTHS = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"], 1)}


def read_data() -> dict:
    """The scalar values of window.A365 that the pages carry as text. A small
    regex read, so this script needs no JavaScript runtime."""
    with open(os.path.join(ROOT, "a365-data.js"), encoding="utf-8") as f:
        js = f.read()
    head = js.split("capabilities:", 1)[0]
    values = {}
    for key in ("reviewed", "gaDate", "transitionDate", "trial"):
        m = re.search(rf'^\s*{key}:\s*"([^"]*)"', head, re.M)
        if not m:
            raise SystemExit(f"a365-data.js: {key} not found")
        values[key] = m.group(1)
    m = re.search(r'price:\s*\{([^}]*)\}', head)
    if not m:
        raise SystemExit("a365-data.js: price block not found")
    for sub, val in re.findall(r'(\w+):\s*"([^"]*)"', m.group(1)):
        values[f"price.{sub}"] = val
    return values


def iso(day: str) -> str:
    """'6 October 2026' -> '2026-10-06'."""
    d, mon, y = day.split()
    return f"{y}-{MONTHS[mon]:02d}-{int(d):02d}"


VAL_RE = re.compile(r'(<(\w+)\b[^>]*\bdata-val="([^"]+)"[^>]*>)(.*?)(</\2>)', re.S)


def check_static(html: str, page: str, data: dict, fix: bool):
    """Returns (bad count, html with every copy rewritten when fix is set)."""
    bad = 0
    def sub(m):
        nonlocal bad
        want = data.get(m.group(3))
        have = re.sub(r"\s+", " ", m.group(4)).strip()
        if want is None:
            print(f"BAD VALUE: {page}: data-val=\"{m.group(3)}\" is not in a365-data.js")
            bad += 1
            return m.group(0)
        if have != want:
            bad += 1
            print(f"BAD VALUE: {page}: data-val=\"{m.group(3)}\" reads \"{have}\", data says \"{want}\"")
        return m.group(1) + want + m.group(5) if fix else m.group(0)
    html = VAL_RE.sub(sub, html)
    want = iso(data["reviewed"])
    m = re.search(r'"dateModified":"([^"]*)"', html)
    if not m:
        print(f"BAD VALUE: {page}: no dateModified in the JSON-LD block"); bad += 1
    elif m.group(1) != want:
        print(f"BAD VALUE: {page}: dateModified is {m.group(1)}, the review date is {want}"); bad += 1
        if fix:
            html = html.replace(m.group(0), f'"dateModified":"{want}"')
    if not bad:
        print(f"ok: {page} carries the data values and dateModified {want}")
    return bad, html


def check_sitemap(data: dict, fix: bool) -> int:
    path = os.path.join(ROOT, "sitemap.xml")
    with open(path, encoding="utf-8") as f:
        xml = f.read()
    want = iso(data["reviewed"])
    stale = [d for d in re.findall(r"<lastmod>([^<]*)</lastmod>", xml) if d != want]
    if not stale:
        print(f"ok: sitemap.xml lastmod is {want}")
        return 0
    print(f"BAD VALUE: sitemap.xml lastmod {', '.join(sorted(set(stale)))} should be {want}")
    if fix:
        with open(path, "w", encoding="utf-8") as f:
            f.write(re.sub(r"<lastmod>[^<]*</lastmod>", f"<lastmod>{want}</lastmod>", xml))
    return 1


def main() -> int:
    fix = "--fix" in sys.argv
    data = read_data()
    bad = 0
    for page in sorted(p for p in os.listdir(ROOT) if p.endswith(".html")):
        path = os.path.join(ROOT, page)
        with open(path, encoding="utf-8") as f:
            html = f.read()
        n, fixed = check_static(html, page, data, fix)
        bad += n
        if fix and fixed != html:
            with open(path, "w", encoding="utf-8") as f:
                f.write(fixed)
            print(f"fixed: {page} rewritten from a365-data.js")
    bad += check_sitemap(data, fix)
    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
        index = f.read()
    bad += check_chapters(index, "index.html")
    for page, sec_id in PAIRS:
        with open(os.path.join(ROOT, page), encoding="utf-8") as f:
            other = f.read()
        a, b = block(index, sec_id), block(other, sec_id)
        if a == b:
            print(f"ok: #{sec_id} is identical in index.html and {page}")
            continue
        bad += 1
        print(f"DIFFERS: #{sec_id} in index.html and {page}")
        shown = 0
        for line in difflib.unified_diff(a.split("> <"), b.split("> <"), "index.html", page, lineterm="", n=0):
            print("  " + line[:160])
            shown += 1
            if shown >= 8:
                break
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
