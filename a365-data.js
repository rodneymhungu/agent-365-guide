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

  When you change "reviewed", add a line to "changes" (newest first) and
  update dateModified in each page's JSON-LD block and lastmod in
  sitemap.xml. Search engines read those; readers read the changelog in
  chapter 10.
  ==========================================================================
*/
window.A365 = {
  reviewed: "21 September 2026",
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
    { date: "21 September 2026", section: "s5-5", text: "Defender for Endpoint local agent discovery is now GA (macOS discovery remains preview); the Learn page dropped its preview banner." },
    { date: "21 September 2026", section: "s7-4", text: "Intune now has a native Antivirus policy for agent-native event inspection; network inspection still needs a PowerShell platform script. Runtime protection setup page cited." },
    { date: "21 September 2026", section: "s5-4", text: "Snowflake Cortex joins registry sync's supported platforms. Connected platforms page cited." },
    { date: "21 September 2026", section: "s4-1", text: "Chapter 4 gains a scenario-to-control table: start from what you need to stop, land on the control, the enforcing product and its status." },
    { date: "21 September 2026", section: "s2", text: "Chapter 2 is also published on its own page, licensing.html, so the licensing question can be found on its own." },
    { date: "14 September 2026", section: "s5-5", text: "Local agents page: the detected developer-tool list has grown substantially and blocking now covers Gemini CLI, VS Code extensions and OpenClaw's Node.js siblings. Learn page cited." },
    { date: "9 September 2026", section: "s2-1", text: "Licensing prerequisites corrected after Microsoft product marketing feedback: Entra ID P1 comes with every plan that qualifies for Agent 365. Licensing FAQ cited." },
    { date: "8 September 2026", text: "Link preview card for LinkedIn and Teams." },
    { date: "7 September 2026", text: "Weekly check of every cited Learn page, with a pull request when one moves. Sections panel scrolls on phones." },
    { date: "5 September 2026", section: "s7-1", text: "Noted that licence enforcement for Conditional Access and Identity Protection for agents is still pending." },
    { date: "4 September 2026", text: "First published." }
  ],
  capabilities: [
    { key: "control-plane",      name: "Agent 365 licence and admin centre control plane", tier: "ga", note: "GA since 1 May 2026", where: "Microsoft 365 admin centre" },
    { key: "registry",           name: "Registry, overview, requests, actions, management rules, settings, policy templates", tier: "ga", where: "Microsoft 365 admin centre" },
    { key: "agent-map",          name: "Agent map", tier: "ga", where: "Microsoft 365 admin centre" },
    { key: "single-agent-map",   name: "Single Agent Map", tier: "preview", where: "Microsoft 365 admin centre" },
    { key: "graph-api",          name: "Graph API for registry and details", tier: "preview", where: "Graph" },
    { key: "registry-sync",      name: "Registry sync (Bedrock, Vertex, Agentforce, Genie, Oracle, Snowflake Cortex)", tier: "ga", where: "Microsoft 365 admin centre" },
    { key: "registry-sync-anthropic", name: "Registry sync for Anthropic Claude Managed Agents", tier: "preview", where: "Microsoft 365 admin centre" },
    { key: "byo-mcp",            name: "Bring your own MCP server", tier: "preview", where: "Admin centre and CLI" },
    { key: "shadow-ai-page",     name: "Shadow AI page", tier: "frontier", where: "Microsoft 365 admin centre" },
    { key: "local-agents-page",  name: "Local agents page", tier: "frontier", where: "Microsoft 365 admin centre" },
    { key: "own-identity",       name: "Agents with their own identity, AI teammate templates", tier: "frontier", where: "Microsoft 365 admin centre" },
    { key: "agent-id",           name: "Entra Agent ID, blueprints, identities, agent users", tier: "ga", note: "GA for all Entra customers", where: "Entra" },
    { key: "conditional-access", name: "Conditional Access for agents", tier: "ga", note: "Agent risk and Agent execution environments conditions in preview", where: "Entra" },
    { key: "ca-agent-risk",      name: "Conditional Access: Agent risk condition", tier: "preview", where: "Entra", hidden: true },
    { key: "ca-exec-env",        name: "Conditional Access: Agent execution environments condition", tier: "preview", where: "Entra", hidden: true },
    { key: "id-protection",      name: "Identity Protection for agents", tier: "ga", note: "All detections offline; licence enforcement coming", where: "Entra" },
    { key: "id-governance",      name: "Access packages and sponsor lifecycle workflows for agents", tier: "ga", note: "With licence", where: "Entra ID Governance" },
    { key: "purview",            name: "Purview audit, DLP, labels, IRM, Communication Compliance, eDiscovery, DLM, Compliance Manager for agents", tier: "ga", where: "Purview" },
    { key: "defender-core",      name: "Defender agent inventory and real-time protection for Agent 365 tool invocations", tier: "ga", where: "Defender XDR" },
    { key: "defender-posture",   name: "Defender posture risk assessment", tier: "preview", where: "Defender XDR" },
    { key: "defender-nrt",       name: "Defender near-real-time detection", tier: "preview", where: "Defender XDR" },
    { key: "defender-rtp-mcs",   name: "Defender real-time protection for Copilot Studio agents", tier: "preview", where: "Defender XDR" },
    { key: "defender-rtp-foundry", name: "Defender real-time protection for Foundry agents", tier: "preview", where: "Defender XDR" },
    { key: "mde-discovery",      name: "Defender for Endpoint local agent discovery", tier: "ga", note: "macOS discovery still in preview", where: "Defender for Endpoint" },
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
