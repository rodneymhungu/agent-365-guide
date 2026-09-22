#!/usr/bin/env python3
"""
social_post.py — post the short release note to Bluesky and Mastodon.

Reads social-post.txt (written by feedback_collect.py on article weeks) and
posts it wherever credentials exist. Missing credentials skip that network
with a note; nothing fails the digest. Every post made is appended to
distribution-log.md so the digest issue records it.

Env
  BLUESKY_HANDLE, BLUESKY_APP_PASSWORD   app password from bsky.app, Settings, App passwords
  MASTODON_INSTANCE, MASTODON_TOKEN      e.g. infosec.exchange; token from Preferences,
                                          Development, New application, scope write:statuses
  DRY_RUN=1                              print what would be posted, post nothing
"""
import datetime as dt, json, os, re, sys, urllib.request
from urllib.error import HTTPError, URLError

TEXT_FILE, LOG = "social-post.txt", "distribution-log.md"


def call(url, data=None, headers=None, form=False):
    body = None
    h = {"User-Agent": "agent-365-guide-digest/1.0", **(headers or {})}
    if data is not None:
        if form:
            body = urllib.parse.urlencode(data).encode(); h["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            body = json.dumps(data).encode(); h["Content-Type"] = "application/json"
    with urllib.request.urlopen(urllib.request.Request(url, data=body, headers=h), timeout=30) as r:
        return json.loads(r.read().decode("utf-8", "replace") or "{}")


def link_facets(text):
    """Bluesky needs byte offsets for links to be clickable."""
    out, b = [], text.encode("utf-8")
    for m in re.finditer(r"https?://\S+", text):
        start = len(text[:m.start()].encode("utf-8")); end = start + len(m.group(0).encode("utf-8"))
        out.append({"index": {"byteStart": start, "byteEnd": end},
                    "features": [{"$type": "app.bsky.richtext.facet#link", "uri": m.group(0)}]})
    return out


def bluesky(text, log):
    handle, pw = os.environ.get("BLUESKY_HANDLE"), os.environ.get("BLUESKY_APP_PASSWORD")
    if not (handle and pw):
        return log.append("- Bluesky: skipped, BLUESKY_HANDLE or BLUESKY_APP_PASSWORD not set.")
    if os.environ.get("DRY_RUN"):
        return log.append(f"- Bluesky: dry run, would post {len(text)} characters as {handle}.")
    s = call("https://bsky.social/xrpc/com.atproto.server.createSession", {"identifier": handle, "password": pw})
    rec = {"$type": "app.bsky.feed.post", "text": text, "facets": link_facets(text),
           "createdAt": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")}
    r = call("https://bsky.social/xrpc/com.atproto.repo.createRecord",
             {"repo": s["did"], "collection": "app.bsky.feed.post", "record": rec},
             {"Authorization": f"Bearer {s['accessJwt']}"})
    rkey = r.get("uri", "").rsplit("/", 1)[-1]
    log.append(f"- Bluesky: posted https://bsky.app/profile/{handle}/post/{rkey}")


def mastodon(text, log):
    inst, tok = os.environ.get("MASTODON_INSTANCE"), os.environ.get("MASTODON_TOKEN")
    if not (inst and tok):
        return log.append("- Mastodon: skipped, MASTODON_INSTANCE or MASTODON_TOKEN not set.")
    if os.environ.get("DRY_RUN"):
        return log.append(f"- Mastodon: dry run, would post {len(text)} characters to {inst}.")
    r = call(f"https://{inst}/api/v1/statuses", {"status": text, "visibility": "public"},
             {"Authorization": f"Bearer {tok}"}, form=True)
    log.append(f"- Mastodon: posted {r.get('url', '(no url returned)')}")


def main():
    import urllib.parse  # noqa: F401  (used in call)
    globals()["urllib"].parse = urllib.parse
    if not os.path.exists(TEXT_FILE):
        print("social_post: no social-post.txt this week; nothing to post"); return 0
    text = open(TEXT_FILE, encoding="utf-8").read().strip()
    log = []
    for fn in (bluesky, mastodon):
        try:
            fn(text, log)
        except (HTTPError, URLError, KeyError, ValueError) as e:
            detail = e.read().decode("utf-8", "replace")[:200] if isinstance(e, HTTPError) else str(e)
            log.append(f"- {fn.__name__.title()}: failed, {detail}")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write("\n".join(log) + "\n")
    print("\n".join(log))
    return 0


if __name__ == "__main__":
    sys.exit(main())
