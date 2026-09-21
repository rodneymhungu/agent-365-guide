#!/usr/bin/env python3
"""
check_pages.py — a chapter published on its own page must match the guide.

licensing.html carries chapter 2 (<section class="block" id="s2">) of index.html
so that the chapter is indexable on its own. The markup must stay identical in
both files, or the two pages drift apart and one of them lies. This compares
the chapter block in each pair of files, ignoring whitespace and any element
marked data-page-only (the cross-links that only make sense on one page).

Exit 1 and print the first differing line when they diverge. No dependencies.
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


def main() -> int:
    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
        index = f.read()
    bad = 0
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
