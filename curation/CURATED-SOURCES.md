# Curated sources — external finance automation content

Reviewed 2026-07-01. Status legend: ✅ reviewed, content inspected · ⚠️ partially reviewed, inspect before running · ❌ avoid.
Nothing here has been downloaded or executed. Review notes are from reading source files on GitHub.

## Vetting checklist (apply to EVERYTHING before it enters our library)

1. **Read every file** — SKILL.md, scripts, configs. No exceptions.
2. **Network calls**: grep scripts for `requests`, `urllib`, `httpx`, `socket`, `curl`, `fetch`. Any outbound call must have an obvious, documented purpose. Data leaving the machine = hard stop unless it's the point of the tool.
3. **Credential handling**: no hardcoded keys/tokens; credentials must come from env vars or runtime prompts. Anything asking users to paste bank credentials into a file: reject.
4. **Prompt injection**: skill/markdown files are instructions to an AI agent. Look for hidden instructions ("ignore previous...", "send the contents of...", instructions to fetch remote URLs mid-task, white text, base64 blobs).
5. **Obfuscation**: encoded strings, exec/eval on constructed strings, downloads of secondary payloads (`npx -y`, `curl | bash` patterns) = reject or sandbox-only.
6. **Install mechanism**: prefer "copy the files you read" over `npx skills add` style installers that pull unpinned latest code.
7. **License**: MIT/Apache = usable with attribution. AGPL = don't copy into our library (viral license); learn from structure only.
8. **Substance test**: does it actually compute something, or is it a wrapper prompt? Wrapper prompts are fine to learn from but not worth importing.
9. **Provenance**: stars/forks are weak signals (all these repos are <10 stars). Commit history, honest disclaimers, and named authors matter more.
10. **Test on sample data** in the sandbox before it ever touches real client data.

## Reviewed sources

### ✅ openaccountant/skills — github.com/openaccountant/skills
44 markdown-only skills (personal finance, freelancer/business, tax). MIT. 7 stars.
**Reviewed files:** bank-sync, stripe-import. **Verdict: clean and well-made.** Stripe-import is the standout — proper column mappings, deduplication by charge ID, explicit "don't import payouts, you'll double-count" warnings, spreadsheet formulas for manual mode. Bank-sync is partly a funnel to their paid "Wilson Pro" (Plaid integration) but is honest about it and the fallback instructions (per-bank CSV export walkthroughs) are useful.
**Risk notes:** no scripts = no code execution risk; skills reference "Wilson tools" that don't exist outside their CLI (harmless no-ops elsewhere). Commercial upsell present but disclosed.
**Steal-worthy for us:** the "With tool / Without tool" dual-mode pattern; per-provider import mappings (Stripe/PayPal/Square/Wise); month-end-close checklist structure.

### ✅ openaccountants/openaccountants — github.com/openaccountants/openaccountants
371 tax skills, 134 countries, incl. Denmark (VAT+income tax+social contributions tier). AGPL-3.0 + commercial dual license. 8 stars, 43 commits, real release.
**Verdict: impressive architecture, restrictive license.** Quality-tier system (Q1 battle-tested / Q2 research-verified / Q3 AI-drafted) is honest. "Conservative defaults — assume MORE tax when uncertain" is exactly the right design for tax automation. Supplier pattern libraries (local vendor name → classification) are a clever idea.
**Risk notes:** AGPL means don't copy content into our MIT-style library. Tax rates go stale — they admit finding errors in every country verified. Treat outputs as accountant-prep, never filing-ready.
**Steal-worthy (concepts only):** quality tiers, Classified/Assumed/Needs-Input three-outcome contract, conservative-default principle, vendor pattern library idea (a Danish vendor pattern library would be a great JE Advisory asset).

### ⚠️ alirezarezvani/claude-skills — github.com/alirezarezvani/claude-skills
330+ skills across domains; finance folder has financial-analyst (ratios, DCF, budget variance, forecasting) claiming 4 stdlib-only Python scripts. MIT.
**Verdict: promising but scripts not yet inspected** — raw fetch of the script paths returned empty (repo restructures frequently; v2.9.0). SKILL.md itself is clean and the "stdlib-only" claim is the right instinct.
**Before using:** read all 4 scripts line-by-line (checklist items 2, 5). Huge repo = huge review surface; take only the finance folder.

### ✅ OctagonAI/skills — github.com/OctagonAI/skills
~60 skills for equity research: financial statements, earnings call analysis, SEC filings, market data. MIT.
**Verdict: legit but different category.** All skills are thin wrappers around their commercial Octagon MCP API — requires their API key, sends queries to their servers. That's disclosed and normal for market data, but it's investment research, not accounting operations. Not our lane.
**Risk notes:** `npx -y octagon-mcp@latest` install pattern pulls unpinned code — standard MCP practice but worth knowing. Data you query goes to their API.
**Steal-worthy:** the master-skill-orchestrates-sub-skills pattern; skill naming taxonomy.

### ✅ anthropics/claude-cookbooks — github.com/anthropics/claude-cookbooks
Official Anthropic notebooks incl. financial applications (models, dashboards, portfolio analytics). Trusted publisher, MIT.
**Use as:** reference for skill-building patterns, safe baseline.

### ⚠️ n8n community templates — n8n.io/workflows (finance category)
Importable workflow JSON ("AI CFO team", financial reports with AI insights, expense sync).
**Verdict: good idea mine, import with care.** Community workflows are unreviewed by n8n. **Known risks:** hardcoded webhook/API URLs pointing at strangers' servers, credentials nodes, LLM prompts you can't see until you open every node. Before running any: open every node, delete unknown URLs, re-create all credentials.
**Steal-worthy:** workflow decomposition (which steps they chain) — rebuild in our own stack rather than importing.

### 📇 Index only
- **BehiSecc/awesome-claude-skills** — curated directory, useful for discovery; every listed item still needs the checklist.
- **skills.sh** — skill registry/installer; treat installer with checklist item 6.

## Standing rules for our library

1. External content never goes in as-is: rewrite to our conventions (config at top, honest false-positive notes, sample data, tested).
2. Credit original sources in the SKILL.md when we adapt an idea.
3. No AGPL content copied. Concepts and structure aren't copyrightable; text and code are.
4. Everything we adapt gets tested against seeded sample data before release — same bar as our own checks.
5. Re-review any source on major version bumps; pin to reviewed commits when referencing.
