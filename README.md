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

One HTML file, no build step. Everything that goes stale lives in the `A365` object in the first script block: the review date, GA and transition dates, prices, the trial offer, and the status of every capability. Status badges, the "in preview" phrases in the prose, and the deploy-today table all render from that object. To update a status, change the tier in the data block. Do not edit it in the prose.

Tiers are `ga`, `preview`, `frontier` and `roadmap`.

Screenshots live in `images/`. [images/README.md](images/README.md) and `images/manifest.json` record where each one came from (deck slide or Learn page), how it was cropped, and which section uses it. Update both when a screenshot is replaced.

Diagrams are hand-built SVG in the page. The two sketches use a hand-drawn face and a slight wobble filter on purpose.

## Why it looks and reads the way it does

This guide is the first built on my [field guide principles](https://github.com/rodneymhungu/field-guide-principles): name the enforcing product, keep status as data, source every claim where it is made, quarantine opinion, order by dependency, lead with the verdict, say what the source does not say, and end in action. The visual identity, the routed field manual, is described there too.

## Checking a change

Before publishing, confirm that both scripts parse, every local image and internal anchor resolves, every image has width and height, nothing overflows at 390px or 1440px, and the page reads correctly in light and dark. Then run an AI-writing review on any prose that changed.

## Keeping it current

Two GitHub Actions run every Monday. One re-fetches every Learn page the guide cites, and when a page has changed asks Copilot CLI for the minimal edit and opens a pull request for review. The other collects visitor numbers, referrers, issues and public mentions and posts a short digest as an issue labelled `digest`, which GitHub emails to anyone watching the repository. Both are described in [scripts/README.md](scripts/README.md). Neither needs a secret. Two optional tokens add visitor numbers and public mentions to the digest.

## Licence and attribution

Screenshots from Microsoft Learn are CC BY 4.0. Workshop deck screenshots show demo-tenant data approved for publication. Structure and diagrams are adapted from a September 2026 Agent 365 workshop. Text and drawings by Rodney Mhungu.
