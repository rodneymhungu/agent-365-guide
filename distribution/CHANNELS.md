# Distribution channels

Researched 22 September 2026. The question was: how to reach security,
identity, compliance and endpoint engineers who have not seen the guide,
without knocking on the same LinkedIn door every fortnight, and which of it
an agent can run unattended. Fit and effort are judgements; verify before
acting on anything marked "check".

## The principle

The guide has five reader segments, one per enforcing product: identity
(Entra), data and compliance (Purview), SecOps (Defender), endpoint
(Intune), network (Global Secure Access). Each segment has its own places.
Rotate the segment the release note leads with, and the section it links,
so the same audience is not asked to click twice in a row.

## Channels, ranked by fit for this guide

| Channel | Who it reaches | Automatable? | Effort | Notes |
|---|---|---|---|---|
| Search (Bing, Google) via IndexNow and sitemap | People typing "Agent 365 licensing", "Entra agent identity Conditional Access"; new readers every week, no door-knocking | Yes, fully: IndexNow ping on every deploy from GitHub Actions; sitemap already exists | One-off: verify the site in Bing Webmaster Tools and Google Search Console | The only channel that compounds without posting. The page split and the section pages exist for this. |
| LinkedIn newsletter (not just articles) | Your LinkedIn followers, plus anyone who subscribes; every issue is emailed and push-notified to subscribers by LinkedIn | No API for newsletters or articles; publishing is manual, the draft is generated | Ten minutes a fortnight | Any member can create one, no follower threshold. Turns the fortnightly release note into a subscription. |
| LinkedIn feed post | Your network | Yes, via the LinkedIn API with a verified app, "Share on LinkedIn" product and the w_member_social scope; tokens last 60 days | Half a day to set up, then unattended | Posts only, not articles. Useful for the short "new section" post between newsletters. |
| Bluesky and Mastodon (infosec.exchange) | The infosec crowd that left X; SecOps and identity people are there | Yes, fully: GitHub Actions post on article weeks with an app password | An hour to set up | Different audience from LinkedIn. Link goes in the post; no reach penalty. |
| dev.to cross-post with canonical_url | Developers and DevSecOps building agents, the SDK and MCP audience | Yes, fully: API with canonical_url back to the guide, so search credit stays with the guide | An hour to set up | Post the release note or one section as an article. |
| Community newsletters that curate links | Intune admins (Andrew Taylor's Intune Newsletter has a Community Content section of 20 or more links), Microsoft 365 admins (Practical 365, Office 365 for IT Pros), security (tl;dr sec) | No; one email to each curator with the guide and the section that fits their readers | An hour, once, then a line when something big changes | Highest leverage per minute. Curators want good links. Drafts can be written by the agent. |
| Microsoft Tech Community, Agent 365 blog | The product team's own audience; the team has featured community explainers and runs AMAs | No | Internal ask | You are inside; ask the Agent 365 blog owners to feature the guide or write a guest post. The Teams referrer shows internal sharing already works. |
| Reddit: r/Intune, r/entra, r/AZURE, r/microsoft365, r/sysadmin | Practitioners asking exact questions the guide answers | Posting: no, and do not try; self-promotion is policed and ratios near one in ten are expected. Finding threads: yes, the digest can list questions the guide answers (needs the Brave key) | Fifteen minutes a week answering two threads with a section link | Answer the question in the thread, link the section as the source. Never post the guide itself. |
| Microsoft Q&A and Learn comments | People stuck on a Learn page the guide cites | Finding: yes, same search. Answering: no | Same as Reddit | Same rule: answer, then cite. |
| GitHub awesome lists (awesome-microsoft-365, security lists) | Engineers who browse curated lists | Yes: one pull request each, done by the agent | Once | Small, permanent. |
| Dutch and EU user groups, Experts Live NL, workshop audiences | People you already meet | No | One follow-up message per session with the section that answers what came up | The session follow-up from the plan. Log each. |
| Hacker News, Product Hunt | Wrong audience for a Microsoft control-plane guide | No | Skip | |

## What to automate, in order

1. **IndexNow on every deploy.** Key file at the site root, one workflow
   step after each push to main. Bing, Yandex, Naver and Seznam get every
   changed URL within minutes. Verify the site once in Bing Webmaster Tools
   and Google Search Console and submit the sitemap; the agent cannot do
   the verification click.
2. **Bluesky and Mastodon on article weeks.** The digest already writes the
   release note; a workflow posts a three-line version with the section
   link. App passwords as repository secrets.
3. **dev.to cross-post on article weeks.** Same trigger, canonical_url set.
4. **"Questions you could answer this week" in the digest.** Brave Search
   for the guide's section titles and product terms on Reddit, Microsoft
   Q&A and Tech Community from the last seven days, listed with links. You
   answer two. Needs `BRAVE_API_KEY` (issue #10).
5. **LinkedIn feed post via API**, only if the manual newsletter publish
   turns out to be the thing that slips.

Everything else is one email, one pull request or one conversation, and
the agent drafts it.

## Sources

- IndexNow: https://www.bing.com/indexnow/getstarted and
  https://github.com/indexnowkit/indexnow-action
- LinkedIn Posts API and scopes:
  https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api
- LinkedIn newsletter access criteria:
  https://www.linkedin.com/help/linkedin/answer/a591266
- dev.to API cross-posting from GitHub Actions:
  https://dev.to/mrnoyy/publishing-to-devto-from-github-actions-with-zero-dependencies-4gj6
- Bluesky from GitHub Actions: https://github.com/zentered/bluesky-post-action
- Reddit self-promotion norms, 2026: https://www.soar.sh/blog/self-promotion-rules-by-subreddit-database
- Intune Newsletter, community content section:
  https://andrewstaylor.substack.com/p/intune-newsletter-5th-september-2025
- Agent 365 community all-stars, Tech Community:
  https://techcommunity.microsoft.com/blog/agent-365-blog/get-to-know-these-agent-365-community-all-stars/4501056
