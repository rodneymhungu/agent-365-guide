#!/usr/bin/env python3
"""
guard_tiers.py — status tiers in a365-data.js change only by human decision.

The guide's value is that every GA badge is true. A Learn page dropping
"(Preview)" from its title is not a release; on 21 September 2026 the drift
run flipped a capability to GA on exactly that signal while the product's
release notes and portal still said preview. So:

  --restore   (drift workflow, after the model edits) compare the working-tree
              a365-data.js with the base revision; put every changed tier back;
              append the proposed changes to CHANGES.md under "Needs a human
              decision". Prose and note edits pass through untouched. Exit 0.

  --check     (pages-check workflow, on pull requests) exit 1 if any tier
              changed unless the pull request body (PR_BODY env var, or a file
              named by PR_BODY_FILE) cites a release-notes or What's new page on
              learn.microsoft.com. Exit 0 otherwise.

  --base REV  git revision to compare against (default HEAD).

No dependencies. Tiers are read line by line from the capabilities array:
  { key: "...", ..., tier: "ga", ... }
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = "a365-data.js"
CHANGES = os.path.join(ROOT, "CHANGES.md")
LINE = re.compile(r'\{\s*key:\s*"([^"]+)".*?tier:\s*"([a-z]+)"')
EVIDENCE = re.compile(r'https://learn\.microsoft\.com/\S*(whats-new|what-s-new|release-notes|release_notes)\S*', re.I)


def tiers(text: str) -> dict:
    return {m.group(1): m.group(2) for m in map(LINE.search, text.splitlines()) if m}


def base_text(rev: str) -> str:
    return subprocess.run(["git", "show", f"{rev}:{DATA}"], cwd=ROOT, check=True,
                          capture_output=True, text=True).stdout


def main() -> int:
    args = sys.argv[1:]
    rev = args[args.index("--base") + 1] if "--base" in args else "HEAD"
    with open(os.path.join(ROOT, DATA), encoding="utf-8") as f:
        now_text = f.read()
    before, now = tiers(base_text(rev)), tiers(now_text)
    moved = [(k, before[k], now[k]) for k in now if k in before and before[k] != now[k]]
    added = [k for k in now if k not in before]

    if "--restore" in args:
        if not moved:
            print("guard_tiers: no tier changed")
            return 0
        out = []
        for line in now_text.splitlines(keepends=True):
            m = LINE.search(line)
            if m and m.group(1) in dict((k, (b, n)) for k, b, n in moved):
                b = before[m.group(1)]
                line = re.sub(r'tier:\s*"[a-z]+"', f'tier: "{b}"', line, count=1)
            out.append(line)
        with open(os.path.join(ROOT, DATA), "w", encoding="utf-8") as f:
            f.write("".join(out))
        with open(CHANGES, "a", encoding="utf-8") as f:
            f.write("\n## Needs a human decision: status tier changes (reverted by guard_tiers.py)\n\n")
            for k, b, n in moved:
                f.write(f"- `{k}`: proposed {b} → {n}. Tiers change only by a human, in their own pull request, "
                        "with a GA entry from the product's release notes or What's new page in the commit message. "
                        "A Learn page losing its (Preview) label is not evidence.\n")
        for k, b, n in moved:
            print(f"guard_tiers: reverted {k} {n} -> {b}")
        return 0

    if "--check" in args:
        if not moved and not added:
            print("guard_tiers: no tier changed")
            return 0
        body = os.environ.get("PR_BODY", "")
        bf = os.environ.get("PR_BODY_FILE")
        if bf and os.path.exists(bf):
            with open(bf, encoding="utf-8") as f:
                body += f.read()
        for k, b, n in moved:
            print(f"guard_tiers: tier change {k}: {b} -> {n}")
        for k in added:
            print(f"guard_tiers: new capability {k}: {now[k]}")
        if any(n == "ga" for _, _, n in moved) or any(now[k] == "ga" for k in added):
            if EVIDENCE.search(body):
                print("guard_tiers: GA change carries a release-notes link in the pull request body")
                return 0
            print("guard_tiers: FAIL. A tier moved to ga and the pull request body cites no release-notes "
                  "or What's new page on learn.microsoft.com. Add the link that announces GA, or keep the tier.")
            return 1
        print("guard_tiers: tier change is not to ga; allowed")
        return 0

    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
