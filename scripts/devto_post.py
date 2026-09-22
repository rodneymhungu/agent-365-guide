#!/usr/bin/env python3
"""
devto_post.py — cross-post the fortnightly release note to dev.to.

Reads linkedin-draft.md (the field-guide release note the collector writes on
article weeks), turns the short section labels into full links, and creates a
dev.to article with canonical_url pointing at the guide so search credit stays
with the guide. Created as a draft unless DEVTO_PUBLISH=true, so a person
presses publish. Appends the result to distribution-log.md.

Env
  DEVTO_API_KEY   dev.to, Settings, Extensions, DEV Community API Keys
  DEVTO_PUBLISH   "true" to publish immediately; anything else saves a draft
  DRY_RUN=1       print the article, create nothing
"""
import json, os, re, sys, urllib.request
from urllib.error import HTTPError, URLError

DRAFT, LOG = "linkedin-draft.md", "distribution-log.md"
GUIDE = "https://rodneymhungu.github.io/agent-365-guide/"
CANONICAL = GUIDE + "#s10"


def article_from_draft(md):
    title = re.search(r"^Headline:\s*(.+)$", md, re.M)
    title = title.group(1).strip() if title else "What changed in the Agent 365 field guide"
    start = md.find("Updated this week:")
    end = md.find("\nCover image:")
    body = md[start:end if end > 0 else None].strip()
    body = re.sub(r"(?<![\w/])agent-365-guide/(#s[\d-]+|[\w-]+\.html)", lambda m: f"[{m.group(0)}]({GUIDE}{m.group(1)})", body)
    body = body.replace("• ", "- ")
    body += f"\n\n*Originally published as part of the [Agent 365 field guide]({GUIDE}), which links every claim to Microsoft Learn.*"
    return title, body


def main():
    if not os.path.exists(DRAFT):
        print("devto_post: no draft this week; nothing to post"); return 0
    md = open(DRAFT, encoding="utf-8").read()
    title, body = article_from_draft(md)
    log = []
    key = os.environ.get("DEVTO_API_KEY")
    publish = os.environ.get("DEVTO_PUBLISH", "").lower() == "true"
    payload = {"article": {"title": title, "body_markdown": body, "published": publish,
                           "canonical_url": CANONICAL, "tags": ["microsoft", "security", "ai", "agents"]}}
    if os.environ.get("DRY_RUN"):
        print(json.dumps(payload, indent=2)); log.append(f"- dev.to: dry run, {'publish' if publish else 'draft'} of \"{title}\".")
    elif not key:
        log.append("- dev.to: skipped, DEVTO_API_KEY not set.")
    else:
        try:
            req = urllib.request.Request("https://dev.to/api/articles", data=json.dumps(payload).encode(),
                                         headers={"api-key": key, "Content-Type": "application/json",
                                                  "User-Agent": "agent-365-guide-digest/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.loads(r.read().decode())
            log.append(f"- dev.to: {'published' if publish else 'draft saved'} {d.get('url') or 'https://dev.to/dashboard'}")
        except (HTTPError, URLError) as e:
            detail = e.read().decode("utf-8", "replace")[:200] if isinstance(e, HTTPError) else str(e)
            log.append(f"- dev.to: failed, {detail}")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write("\n".join(log) + "\n")
    print("\n".join(log))
    return 0


if __name__ == "__main__":
    sys.exit(main())
