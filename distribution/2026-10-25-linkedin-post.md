# LinkedIn feed post, 25 October 2026

**Status: draft, not posted.** Replaces the 19 October article that was never
sent. This is the native-post test from the 6 October review: one post, under
1,300 characters, one change led, three more named, the guide linked once.
The comparison is the LinkedIn referrer count in the 2 November digest against
the article weeks (13 on the week of the 6 October article, 3 to 4 on the weeks
without one).

## Pick this up in three steps

1. LinkedIn, Start a post. Paste the body below as it is. No article, no
   headline field.
2. Add the image `distribution/2026-10-25-linkedin-cover.png`: the chapter 4
   map rendered from the live page at 1920 by 1169, light theme. The post
   says "the map below", so the image is not optional.
3. When it is live, add the post URL to the Posted line below and tell Claude
   "posted, <url>", which also fills the focus 4 row in `PLAN.md`.

Posted:

Built 25 October 2026 from the `changes` entries dated 12 to 25 October, curated
by hand to four product changes plus the map. Left out as guide maintenance
or too small for a feed post: the first-party ownership rule, the duplicate
registry rows, the MCP server options page, the CLI onboarding walkthroughs,
the Users-assignment exclusion (already in the 19 October digest draft, which
was never posted, and a 7.1 detail rather than a lead), and the dropped
enforcement claim.

Characters: 1262.

---

## Body

Updated: the Agent 365 field guide for security and compliance engineers. Four things moved on Microsoft Learn in the last fortnight.

Conditional Access policies that use the Agent risk condition need Entra ID P2 or Microsoft 365 E5 beside the Agent 365 licence. It is the one policy in the guide's identity sequence that an E3 base plan does not cover.

Defender for Endpoint has a support matrix for local agents. Claude Desktop in code mode and the GitHub Copilot and Claude Code extensions for VS Code gain agent hooks; ChatGPT Desktop and Ollama Desktop come under network inspection. Preview.

Every Connected platforms connection has a Collect agent observability data switch, on by default. It queries the provider's own logs, BigQuery or S3, and the provider bills those queries.

Creating, syncing or deleting a connection is not guaranteed to reach the Purview audit log. If you need that trail, keep it in your change process.

Also new to the guide: the map below. Where agents run, what Agent 365 reaches by each route, and which product enforces.

Every claim links to Learn. Status badges follow Microsoft's release notes, checked every Monday.

See what changed and what you can deploy today: https://rodneymhungu.github.io/agent-365-guide/#s10

---

## Writing review, 25 October 2026

Checklist T1 to T19. Verdict: reads as human. The opening and closing lines
are the release-note format and exempt; "has a support matrix" and "come
under" state the current fact rather than the change (T19 clear).

1. Note only. "Preview." as a one-word sentence after the Defender paragraph.
   Status precision, kept.
2. Note only. "the map below" assumes the image is attached; step 2 above
   makes it so.
3. Checked, no flag. Four product paragraphs of 31 to 44 words, then two short
   closers: enough variation (T2).
