#!/usr/bin/env python3
"""
check_pages.py — a chapter published on its own page must match the guide,
and every video chapter button must jump somewhere real.

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


def main() -> int:
    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
        index = f.read()
    bad = check_chapters(index, "index.html")
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
