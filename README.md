# Agent 365 for security and compliance engineers

Field guide 01. Live at [rodneymhungu.github.io/agent-365-guide](https://rodneymhungu.github.io/agent-365-guide/).

Agent 365 is Microsoft's unified control plane for AI agents. It finds every agent in the tenant, gives it an owner, attaches policy and watches what it does. It enforces nothing itself; Entra, Purview, Defender and Intune do that. This guide shows security and compliance engineers which product enforces each control, what it needs, and what works today.

## Who it is for

Engineers who already run Entra, Purview, Defender or Intune and have been asked to bring agents under the same controls. It assumes you know those products and want to know what changes when the subject is an agent instead of a user.

## How it is organised

The chapters follow Microsoft's three pillars in the order the work has to happen, because each depends on the one before it:

1. The control plane does not enforce anything
2. What you need before the controls appear
3. Agents do not behave like applications
4. Five products share the enforcement path
5. Observe. First, find what is running
6. Govern. Then give every agent an owner
7. Secure. Last, stop the action itself
8. A twelve-week evaluation you can actually run
9. The first ten moves
10. What you can deploy today

Facts come from Microsoft Learn and are linked in the sentence that makes the claim. Opinions live in numbered field notes and are mine.

## How it is built

Plain HTML, no build step, no framework. Four files at the root do the work:

- `index.html` is the full guide.
- `licensing.html` is chapter 2 published on its own page so that it can be found on its own. Its chapter block is a copy of the one in `index.html`; `scripts/check_pages.py` fails the build if the two differ.
- `changes.html` is the changelog published on its own page, grouped by month and date, so each week's changes have an address to link to. Its list is a static copy of the `changes` array in `a365-data.js`; `scripts/check_pages.py --fix` regenerates it and the build fails when it drifts.
- Chapter 10 of `index.html` is the status board, the section most readers land on. A meter counts the controls by status and filters the list on click, product chips and a find box narrow it, and each row links to the section that explains it through the capability's `sec` field in `a365-data.js`. On a phone each row is a card. Its rows are a static copy of the `capabilities` array, written by `scripts/check_pages.py --fix` like the changelog, so the board reads without JavaScript. A link can open it filtered: `index.html?status=preview&product=defender#s10` (status is `ga`, `preview`, `frontier` or `roadmap`). The address bar follows the filters and the board has a Copy link to this view control, so a filtered view can be shared. Each status or product filter a reader uses is sent to GoatCounter once per visit as `#filter-preview` or `#filter-defender`, and the Monday digest lists them; text typed in the find box is never recorded.
- A section a product change touched in the fortnight before the review date carries an Updated marker under its heading and a dot in the contents panel. `guide.js` works that out from the `changes` array; nothing is typed.
- `a365-data.js` holds everything that goes stale: the review date, GA and transition dates, prices, the trial offer, the changelog, and the status of every capability. Status badges, the "in preview" phrases in the prose, and the deploy-today table all render from that object on every page. To update a status, change the tier there. Do not edit it in the prose.
- `guide.css` and `guide.js` are the shared tokens, layout and behaviour.

Tiers are `ga`, `preview`, `frontier` and `roadmap`.

Screenshots live in `images/`. [images/README.md](images/README.md) and `images/manifest.json` record where each one came from (deck slide or Learn page), how it was cropped, and which section uses it. Update both when a screenshot is replaced.

Diagrams are built in the page from its tokens: SVG for drawings and flows, a plain HTML grid for the chapter 4 map, whose text has to wrap on a phone and whose badges render from the data file. The two sketches use a hand-drawn face and a slight wobble filter on purpose.

## Why it looks and reads the way it does

This guide is the first built on my [field guide principles](https://github.com/rodneymhungu/field-guide-principles): name the enforcing product, keep status as data, source every claim where it is made, quarantine opinion, order by dependency, lead with the verdict, say what the source does not say, and end in action. The visual identity, the routed field manual, is described there too.

## Checking a change

Before publishing, confirm that both scripts parse, every local image and internal anchor resolves, every image has width and height, nothing overflows at 390px or 1440px, and the page reads correctly in light and dark. Then run an AI-writing review on any prose that changed.

## Keeping it current

Two GitHub Actions run every Monday. One re-fetches every Learn page the guide cites, and when a page has changed asks Copilot CLI for the minimal edit and opens a pull request for review. The other collects visitor numbers, referrers, issues, open drift pull requests and public mentions and posts a short digest as an issue labelled `digest`. Both the pull request and the issue are assigned to the author and mention him, so GitHub notifies and emails on every one. Both are described in [scripts/README.md](scripts/README.md). Neither needs a secret. Two optional tokens add visitor numbers and public mentions to the digest.

## Where this is going

[PLAN.md](PLAN.md) is the plan of record: the visitor target, the weekly rotation of work, the blockers, and a log of what shipped. Read it first if you are picking the work up.

A changelog lives in the `changes` array of the same data block. Readers get it on `changes.html`; the five newest product changes also show at the end of chapter 10 and the three newest under the hero. `sitemap.xml`, `robots.txt`, the canonical link and the JSON-LD block in the head exist for search engines. The review date, prices and key dates also sit as static text inside the elements that `guide.js` fills, so crawlers and link previews see them without JavaScript. When the review date or a price changes, run `python3 scripts/check_pages.py --fix` to rewrite those copies, `dateModified` and `lastmod` from the data file; the Pages check fails when they disagree.

## Licence and attribution

Screenshots from Microsoft Learn are CC BY 4.0. Workshop deck screenshots show demo-tenant data approved for publication. Structure and diagrams are adapted from a September 2026 Agent 365 workshop. Text and drawings by Rodney Mhungu.
