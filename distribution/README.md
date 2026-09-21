# Distribution drafts

One file per post, named by date and channel. Written from that week's
`changes` entries in `a365-data.js`, one link per post pointing at the
section the post is about, so the referrer and the section both show in the
digest. When a post goes out, add the date and link to the log in `PLAN.md`.

Before posting, run the `ai-writing-review` skill on the draft and decide each
flag. The digest-generated drafts are assembled from changelog entries, which
were reviewed when they were merged, but the assembled article has not been
read as one piece until you do this. Log the review in the draft file.

Posts describe the product and what the guide says about it. They never
mention the guide's own workings: the drift workflow, documentation
discrepancies, label changes on Learn, or how a status was verified. That is
maintenance detail; readers are searching for what the product does.

## Release-note format (Rodney, 21 September 2026)

Every field-guide release note follows this shape. The fortnightly digest
draft is generated in it; edit, do not restructure.

1. Title: "What changed this week in the [product] field guide".
2. One sentence naming the guide and its audience: "Updated this week: the [product] field guide for [audience]."
3. "[Number] things moved on Microsoft Learn, and the guide moved with them:"
4. One bullet per material change: bold the product and, separately, the
   capability or outcome (two or three bold phrases, not one bold sentence), explain the practical change in plain English, give GA, Preview
   or other status where relevant, and end with a visible shortened section
   link such as `agent-365-guide/#s7-4`. The link is a navigation label; never
   hide it behind prose.
5. Structural guide improvements go in one final bullet beginning "Also new
   to the guide".
6. Then: "Every claim in the guide links to Learn. GA/Preview status badges
   follow Microsoft's release notes, checked every Monday."
7. End with "See what changed and what you can deploy today:" and the full visible link:
   https://rodneymhungu.github.io/agent-365-guide/#s10
8. Concise, factual, skimmable. British English, short paragraphs, no em dashes.

Changelog entries in `a365-data.js` feed the bullets, so write them to fit:
first sentence names the product and capability (it is bolded), then the
practical change. Entries about the guide itself carry `kind: "guide"` and
land in the "Also new to the guide" bullet.
