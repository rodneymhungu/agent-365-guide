# LinkedIn feed post, 10 November 2026

**Status: draft, not posted.** The same shape as the 26 October feed post,
which outperformed the 6 October article on every measure (see
`2026-10-25-linkedin-post.md`). It carries the four strongest changes from
the article drafted in `2026-11-09-linkedin.md`; post one or the other, not
both.

## Pick this up in three steps

1. Merge the 10 November pull request first and wait for the site to deploy.
   The post says "the status board below" and its link lands on chapter 10,
   which is only a board once that merge is live.
2. LinkedIn, Start a post. Paste the body below as it is. Add the image
   `distribution/2026-11-09-linkedin-cover-board.png`: the status board
   rendered from the page at 1920 by 1080, light theme. The image is not
   optional; the 26 October post's diagram is the likeliest reason it
   travelled.
3. When it is live, tell Claude "posted, <url>", which fills the Posted line
   below and the focus 4 row in `PLAN.md`.

Posted:

Built 10 November 2026 from the `changes` entries dated 6 to 10 November.
Left for the article or the changelog: the provider-billed observability
switch and the Purview audit gap (both in the 26 October post), the agent-risk
licence (same), Execution Containers and the Dynamic announcements (not on
Learn), the Manage agents page, the Databricks Genie service principal, the
activity-metrics scope and SDK 2.0.

Characters: 1276.

---

## Body

Updated: the Agent 365 field guide for security and compliance engineers. Four things moved on Microsoft Learn in the last fortnight.

Defender for Endpoint local agent discovery is generally available on Windows and macOS. Its support matrix lists sixty-two tools on Windows and fifty-nine on macOS. The WSL and macOS VS Code extension entries stay in preview.

An inventory entry is not proof of use. Most tools are listed once their process runs, and VS Code extensions are found from installed-extension data even if they never run.

Intune's policy template for Defender runtime protection is generally available. The feature it deploys is still in preview.

Connected platforms reach each source platform from a fixed set of outbound IP addresses. If the platform restricts network access and you have not allowed them, the connection fails with an authentication error, even when the credentials are correct.

Also new to the guide: the status board below. Every control with its status today, filtered by status or product, each linked to the section that explains it.

Every claim links to Learn. Status badges follow Microsoft's release notes, checked every Monday.

See what changed and what you can deploy today: https://rodneymhungu.github.io/agent-365-guide/#s10

---

## Writing review, 10 November 2026

Checklist T1 to T19. Verdict: reads as human. The opening and the two closing
lines are the format and exempt. No dashes, no US spellings. None applied;
the default is keep.

1. Note only. "An inventory entry is not proof of use." A negation as an
   opener (T4 cousin, Low). It is the finding, and the next sentence gives
   the reason, so it reads as a claim, not a flourish.
2. Note only. "is still in preview" and "stay in preview" in adjacent
   paragraphs (T19, T13, Low). In a release note the status is the point.
3. Checked, no flag. Paragraphs run 16 to 39 words with one 8-word sentence;
   enough variation (T2).
