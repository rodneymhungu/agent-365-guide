/*
  ==========================================================================
  HOW TO UPDATE THE GUIDE
  --------------------------------------------------------------------------
  Every fact that goes stale lives in this one object: the review date, GA
  and transition dates, prices, the trial offer, the changelog, and the
  status of each capability. Both pages (index.html and licensing.html) load
  this file. Status badges, the "in preview" phrases in the prose, the
  "What you can deploy today" table and the changelog all render from it.
  Change a tier from "preview" to "ga" and every page updates. Do not edit
  statuses in the prose by hand.

  Tiers: ga | preview | frontier | roadmap

  When you change "reviewed", add a line to "changes" (newest first), then
  run  python3 scripts/check_pages.py --fix  from the repository root. That
  rewrites the static copies of these values: the text inside every element
  carrying data-val on both pages (crawlers, link previews and plain text
  fetches read those, because guide.js only fills them after the page loads),
  dateModified in each page's JSON-LD block and lastmod in sitemap.xml.
  The same script without --fix runs on every push and fails when a copy
  disagrees with this file. Readers read the changelog in chapter 10.
  ==========================================================================
*/
window.A365 = {
  reviewed: "18 October 2026",
  gaDate: "1 May 2026",
  transitionDate: "1 July 2026",
  trial: "25 seats for 30 days",
  assets: "images/manifest.json",
  price: { addon: "13 euro", e7: "91.92 euro", note: "per user per month, annual commitment, Dutch-localised pricing page" },
  tiers: {
    ga:       { label: "GA",               phrase: "generally available" },
    preview:  { label: "Preview",          phrase: "in preview" },
    frontier: { label: "Frontier preview", phrase: "a Frontier preview" },
    roadmap:  { label: "Early preview",    phrase: "in early preview" }
  },
  changes: [
    { date: "18 October 2026", section: "s5-5", text: "The Defender for Endpoint AI agent support matrix is now the source for both Defender columns of the lookup table: Claude Desktop in Code mode and the GitHub Copilot and Claude Code extensions for Visual Studio Code gain agent hooks, ChatGPT Desktop and Ollama Desktop gain network inspection, Antigravity Desktop and Microsoft Scout are discovered, and Codex CLI is named by the runtime protection overview but absent from the matrix. Sixty tools on Windows, fifty-one on macOS. AI agent support matrix page cited." },
    { date: "18 October 2026", section: "s7-4", text: "Runtime protection's supported agents come from the support matrix: six agents with hooks, four under network inspection. AI agent support matrix page cited." },
    { date: "18 October 2026", section: "s5-4", text: "Observability on Connected platforms now covers five platforms, Salesforce Agentforce and Databricks Genie joining Bedrock, Vertex AI and Anthropic, and each connection has a Collect agent observability data switch, on by default, whose queries the provider bills. The two Learn pages disagree about older connections. Connected platforms and Third-party agent observability pages cited." },
    { date: "18 October 2026", section: "s5-4", text: "Two onboarding walkthroughs for agents you build: a single agent with the Agent 365 CLI, and bulk onboarding from one CSV with PowerShell. Both pages cited." },
    { date: "18 October 2026", section: "s5-6", text: "Observability data for Foundry and Copilot Studio agents includes prompts and responses, stored in the tenant's default geography whatever the Azure region, and each platform has a control to stop sending it. Data handling for Azure agents page cited." },
    { date: "18 October 2026", section: "s2-1", text: "Agent risk-based Conditional Access needs Entra ID P2 or Microsoft 365 E5 beside Agent 365, the one policy in 7.1 that E3 does not cover. Secure autonomous agents with Conditional Access page cited." },
    { date: "12 October 2026", section: "s7-1", text: "Policies in the Users assignment exclude agent user accounts whether they target all users, selected users, groups, roles or external users; scope agent users with the Agents assignment instead. Conditional Access for agents page cited." },
    { date: "12 October 2026", section: "s5-6", text: "Observability collection starting only once a trial or licence is active now applies to third-party agents and to tenants in ten listed countries, including Austria, Denmark and Spain. Data handling, data residency, and compliance page cited." },
    { date: "12 October 2026", section: "s6-6", text: "Access packages for agents grant OAuth API permissions, delegated and application, for Microsoft Graph and applications. Governing agent identities page cited." },
    { date: "12 October 2026", section: "s5-5", text: "Defender for Endpoint lists a local agent only after it observes activity, so discovery is not a full software inventory. Local AI agent discovery page cited." },
    { date: "12 October 2026", section: "s2-1", text: "Dropped the claim that Agent 365 licence enforcement for Conditional Access is coming: the autonomous agents policy page now lists the licence plans without that notice. Secure autonomous agents with Conditional Access page cited." },
    { date: "11 October 2026", section: "s6-3", text: "Management rules number five: Apply a template joins the four bulk actions, each rule takes conditions that select the agent instances it runs on, and the template rule is a one-off run limited to registry agents with an identity. Microsoft's September What's new post calls custom rules a public preview and lists more conditions than Learn does. Agent settings page and the post cited." },
    { date: "11 October 2026", section: "s5-3", text: "AI mode, a natural-language search of the registry for ownerless, inactive or review-worthy agents, announced as a public preview in Microsoft's September What's new post. No Learn page yet, so it carries the early preview label." },
    { date: "11 October 2026", section: "s5-4", text: "Azure API Management integration: agents, tools, models and MCP servers onboarded there appear in Agent 365 without manual registration, rolling out from 30 September per Microsoft's September What's new post. No Learn page yet, so it carries the early preview label." },
    { date: "11 October 2026", kind: "guide", text: "Chapter buttons under the 6.7 and 7.5 videos jump to their chapters. The review date, prices and key dates sit in the page text for crawlers and link previews. Each part of the page script runs on its own, so one missing element no longer stops the rest." },
    { date: "6 October 2026", section: "s5-4", text: "Connected platforms is the current name for what Microsoft announced as Registry sync in April 2026, and several Learn pages still use the old name; observability differs by platform: the hub lists it for Amazon Bedrock, Google Vertex AI and Anthropic, with the other four coming soon, and third-party agent observability is a Frontier preview whose page also lists Salesforce Agentforce. Connected platforms and Third-party agent observability pages cited." },
    { date: "6 October 2026", section: "s6-8", text: "Admins can create an agent instance on behalf of a manager: a Global Administrator or AI Administrator starts it from the agent's details in the registry, a wizard checks licences first, and the manager owns the instance in Entra and Teams. Create agentic user instances page cited." },
    { date: "6 October 2026", kind: "guide", text: "Writing and structure pass: 5.5 and 7.2 open on their verdict, 2.1 and 7.4 split into one claim per sentence, the hero names all five enforcing products, 4.1 lists all seven synced platforms, and cross-references use bare section numbers." },
    { date: "6 October 2026", section: "s6-4", text: "The Allowed agent types setting is now Agent and plugin access and also governs plugins, meaning tools, MCP servers, connectors and skills; Microsoft-built ones stay visible when disabled but cannot be installed. Agent settings page cited." },
    { date: "6 October 2026", section: "s5-4", text: "Each registry sync platform now has its own setup page, and the permission scope varies: Amazon Bedrock and Oracle need only read access, with delete rights optional, while Google Vertex AI requires the delete permission. A delete in Agent 365 reaches the source platform. All seven setup pages cited." },
    { date: "5 October 2026", section: "s5-4", text: "The Agent 365 SDK no longer bundles observability: Microsoft deprecated the SDK's observability packages in favour of the separate Microsoft OpenTelemetry Distro, keeping identity, tooling and notifications in the SDK. Agent 365 SDK overview page cited." },
    { date: "5 October 2026", section: "s5-4", text: "Dropped the claim that registry sync scheduling is promised: the connected platforms page no longer states a scheduled-sync roadmap, only that synchronisation is manual. Connected platforms page cited." },
    { date: "5 October 2026", section: "s2-1", text: "Conditional Access for agents now states its licensing as Microsoft 365 E7, or an Agent 365 licence paired with at least Entra ID P1 or Microsoft 365 E3; the companion autonomous agents policy page confirms Agent 365 licence enforcement is still coming. Conditional Access for agents page cited." },
    { date: "28 September 2026", section: "s7-4", text: "Runtime protection can now be deployed from the Microsoft Defender portal as well as Intune, reaching devices under Defender for Endpoint security settings management; public preview also requires the Beta Channel for platform and engine updates. Runtime protection setup page cited." },
    { date: "28 September 2026", section: "s6-3", text: "Deleting an agent is now a soft delete with a thirty-day recovery window and a restore option, for any agent type, not an irreversible Agent Builder-only removal. Agent actions page cited." },
    { date: "28 September 2026", section: "s5-3", text: "The Risks column and Risk details pane now cover high, medium and low severity signals, not high alone; a zero means no active signal at any severity. Agent registry page cited." },
    { date: "28 September 2026", section: "s6-8", text: "AI administrators, not only administrators, can activate templates and delete agent instances. Manage agent instances page cited." },
    { date: "27 September 2026", kind: "guide", text: "Structure pass: 5.4 and 6.1 open on their answer, 6.2 custom templates and 7.3 real-time protection coverage are tables, 5.5 names each tool once, 7.4 says which admin-centre page blocks what." },
    { date: "27 September 2026", section: "s5-5", kind: "guide", text: "5.5 gains a lookup table of which surface detects which local AI tool and which can block it, joined from the Shadow AI, Local agents, Defender discovery and runtime protection pages." },
    { date: "21 September 2026", section: "s5-5", text: "Defender for Endpoint local agent discovery stays in preview. Learn's page dropped its preview label, but the Defender for Endpoint release notes and the portal still say preview, and there is no GA entry." },
    { date: "21 September 2026", section: "s7-4", text: "Intune now has a native Antivirus policy for agent-native event inspection; network inspection still needs a PowerShell platform script. Runtime protection setup page cited." },
    { date: "21 September 2026", section: "s5-4", text: "Snowflake Cortex joins registry sync's supported platforms. Connected platforms page cited." },
    { date: "21 September 2026", section: "s4-1", kind: "guide", text: "Chapter 4 gains a scenario-to-control table: start from what you need to stop, land on the control, the enforcing product and its status." },
    { date: "21 September 2026", section: "s2", kind: "guide", text: "Chapter 2 is also published on its own page, licensing.html, so the licensing question can be found on its own." },
    { date: "14 September 2026", section: "s5-5", text: "Local agents page: the detected developer-tool list has grown substantially and blocking now covers Gemini CLI, VS Code extensions and OpenClaw's Node.js siblings. Learn page cited." },
    { date: "9 September 2026", section: "s2-1", text: "Licensing prerequisites corrected after Microsoft product marketing feedback: Entra ID P1 comes with every plan that qualifies for Agent 365. Licensing FAQ cited." },
    { date: "8 September 2026", kind: "guide", text: "Link preview card for LinkedIn and Teams." },
    { date: "7 September 2026", kind: "guide", text: "Weekly check of every cited Learn page, with a pull request when one moves. Sections panel scrolls on phones." },
    { date: "5 September 2026", section: "s7-1", text: "Noted that licence enforcement for Conditional Access and Identity Protection for agents is still pending." },
    { date: "4 September 2026", kind: "guide", text: "First published." }
  ],
  capabilities: [
    { key: "control-plane",      name: "Agent 365 licence and admin centre control plane", tier: "ga", note: "GA since 1 May 2026", where: "Microsoft 365 admin centre" },
    { key: "registry",           name: "Registry, overview, requests, actions, management rules, settings, policy templates", tier: "ga", where: "Microsoft 365 admin centre" },
    { key: "registry-ai-mode",   name: "AI mode: natural-language search of the registry", tier: "roadmap", note: "Blog announcement of 30 September 2026; no Learn page yet", where: "Microsoft 365 admin centre" },
    { key: "agent-map",          name: "Agent map", tier: "ga", where: "Microsoft 365 admin centre" },
    { key: "single-agent-map",   name: "Single Agent Map", tier: "preview", where: "Microsoft 365 admin centre" },
    { key: "graph-api",          name: "Graph API for registry and details", tier: "preview", where: "Graph" },
    { key: "registry-sync",      name: "Connected platforms (Bedrock, Vertex, Agentforce, Genie, Oracle, Snowflake Cortex)", tier: "ga", where: "Microsoft 365 admin centre" },
    { key: "registry-sync-anthropic", name: "Connected platforms: Anthropic Claude Managed Agents", tier: "preview", where: "Microsoft 365 admin centre" },
    { key: "apim-discovery",     name: "Azure API Management integration: agents, tools, models and MCP servers discovered from the gateway", tier: "roadmap", note: "Blog announcement of 30 September 2026, rolling out from that date; no Learn page yet", where: "Azure API Management; Microsoft 365 admin centre" },
    { key: "third-party-observability", name: "Third-party agent observability (Bedrock, Vertex AI, Anthropic, Agentforce, Genie)", tier: "frontier", where: "Microsoft 365 admin centre" },
    { key: "byo-mcp",            name: "Bring your own MCP server", tier: "preview", where: "Admin centre and CLI" },
    { key: "shadow-ai-page",     name: "Shadow AI page", tier: "frontier", where: "Microsoft 365 admin centre" },
    { key: "local-agents-page",  name: "Local agents page", tier: "frontier", where: "Microsoft 365 admin centre" },
    { key: "own-identity",       name: "Agents with their own identity, AI teammate templates", tier: "frontier", where: "Microsoft 365 admin centre" },
    { key: "agent-id",           name: "Entra Agent ID, blueprints, identities, agent users", tier: "ga", note: "GA for all Entra customers", where: "Entra" },
    { key: "conditional-access", name: "Conditional Access for agents", tier: "ga", note: "Agent risk and Agent execution environments conditions in preview", where: "Entra" },
    { key: "ca-agent-risk",      name: "Conditional Access: Agent risk condition", tier: "preview", note: "Needs Entra ID P2 or Microsoft 365 E5 beside Agent 365", where: "Entra", hidden: true },
    { key: "ca-exec-env",        name: "Conditional Access: Agent execution environments condition", tier: "preview", where: "Entra", hidden: true },
    { key: "id-protection",      name: "Identity Protection for agents", tier: "ga", note: "All detections offline; licence enforcement coming", where: "Entra" },
    { key: "id-governance",      name: "Access packages and sponsor lifecycle workflows for agents", tier: "ga", note: "With licence", where: "Entra ID Governance" },
    { key: "purview",            name: "Purview audit, DLP, labels, IRM, Communication Compliance, eDiscovery, DLM, Compliance Manager for agents", tier: "ga", where: "Purview" },
    { key: "defender-core",      name: "Defender agent inventory and real-time protection for Agent 365 tool invocations", tier: "ga", where: "Defender XDR" },
    { key: "defender-posture",   name: "Defender posture risk assessment", tier: "preview", where: "Defender XDR" },
    { key: "defender-nrt",       name: "Defender near-real-time detection", tier: "preview", where: "Defender XDR" },
    { key: "defender-rtp-mcs",   name: "Defender real-time protection for Copilot Studio agents", tier: "preview", where: "Defender XDR" },
    { key: "defender-rtp-foundry", name: "Defender real-time protection for Foundry agents", tier: "preview", where: "Defender XDR" },
    { key: "mde-discovery",      name: "Defender for Endpoint local agent discovery", tier: "preview", note: "Learn's page dropped its preview label on 21 September 2026; the release notes and the portal still say preview", where: "Defender for Endpoint" },
    { key: "mde-runtime",        name: "Defender for Endpoint runtime protection", tier: "preview", where: "Defender for Endpoint" },
    { key: "gsa-copilot-studio", name: "Global Secure Access for Copilot Studio agents, prompt injection protection", tier: "ga", note: "Device and prompt-injection paths need Entra Internet Access", where: "Global Secure Access" },
    { key: "gsa-shadow-ai",      name: "Global Secure Access Shadow AI discovery", tier: "ga", where: "Global Secure Access" },
    { key: "gsa-mcp-firewall",   name: "MCP firewall", tier: "preview", where: "Global Secure Access" },
    { key: "gsa-genai-insights", name: "Generative AI Insights", tier: "preview", where: "Global Secure Access" },
    { key: "gsa-agent-discovery", name: "AI agent discovery", tier: "preview", where: "Global Secure Access" },
    { key: "w365-agents",        name: "Windows 365 for Agents", tier: "ga", where: "Intune" },
    { key: "mxc",                name: "Microsoft Execution Containers", tier: "roadmap", note: "Windows Insider builds; not in Learn docs", where: "Windows" }
  ]
};
