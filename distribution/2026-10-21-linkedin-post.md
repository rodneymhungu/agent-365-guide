# LinkedIn feed post, week of 19 October 2026

**Status: draft.** The native-post test the plan has asked for since
6 October: one change led, three more named, the guide linked once, under
1,300 characters. Compare the LinkedIn referrer count in the 26 October digest
against the 6 October article (13 visitors, 986 impressions, 39 article
views) before deciding the weekly format.

## Pick this up in three steps

1. LinkedIn, Start a post. Paste the text below as it stands. No cover image
   is needed for a feed post; the link preview card carries the route plate.
2. Post on a weekday morning. The 6 October article went out around
   11 October and its best day was 9 October, a Thursday.
3. When it is live, add the URL to the Posted line below and to the log in
   `PLAN.md` under focus 4, or tell Claude "posted, <url>" and it will do both.

Posted:

Built 21 October 2026 from the `changes` entries dated 12 and 18 October.
Length: 1300 characters. Link: the new changes page, so the referrer and the
landing page both show in the digest.

---

Your "All users" Conditional Access policies do not touch agent user accounts.

Microsoft's Conditional Access for agents page says it plainly: any policy scoped through the Users assignment, whether all users, selected users, groups, roles or external users, skips agent users. To cover them you need a policy that targets Agent users. If you have AI teammates with their own accounts, check the Agents assignment this week.

Three more changes in the Agent 365 field guide since 11 October:

• Defender for Endpoint published its AI agent support matrix. Six agents get runtime hooks, including Claude Desktop and the GitHub Copilot and Claude Code extensions for VS Code. OpenClaw, Ollama Desktop and the ChatGPT apps get network inspection. Codex CLI is named in the overview but missing from the matrix.

• Connected platforms has a Collect agent observability data switch, on by default for new connections. It queries the provider's own logging services, BigQuery or S3 for example, and the provider bills those queries.

• Agent risk-based Conditional Access needs Entra ID P2 or Microsoft 365 E5 beside Agent 365. The rest of the recommended policy set runs on P1 or E3.

Every change, dated and linked to the Learn page behind it: https://rodneymhungu.github.io/agent-365-guide/changes.html

---

## Writing review, 21 October 2026

Run with the `ai-writing-review` checklist (T1 to T19).

Verdict: reads as human. Flags considered:

1. Kept. "says it plainly" (T11, editorialising): one plain-English reading
   of a Learn boundary statement, which is the point of the post.
2. Kept. Three bullets (T6, the triad): the plan's native-post shape is one
   change led and two or three named, so the count is structural.
3. Applied. The support matrix bullet ran to one 40-word sentence with two
   semicolons; now three sentences.
4. Kept. "this week" in the opening (T19, changelog voice): it is an
   instruction to the reader, not a release note.

Also checked: no em or en dashes, British spelling throughout, nothing about
the guide's own workings.
