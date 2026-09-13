# AC#0 support — published list prices (NOT measured $/run)

**Updated:** 2026-09-13  
**Author:** Research Agent (2k)  
**Purpose:** Give Builder a sourced starting set of ≤3 engines. **AC#0 still requires measured $/run** from a real pilot — this file is list-price FACT only.

## Recommended engine set (≤3)

| # | Engine ID | How we’d call it | Why |
|---|-----------|------------------|-----|
| 1 | `openai-web-search` | OpenAI Responses/Chat + **Web search** tool | Official API; citations via search; controllable |
| 2 | `perplexity-sonar` | Perplexity **Sonar** (low context) | Grounded answers + citations; cheap request fee |
| 3 | `perplexity-agent-web` | Perplexity Agent API + `web_search` tool **or** omit if #1+#2 enough | Optional 3rd; prefer drop if COGS tight |

Do **not** scrape ChatGPT/Claude/Gemini UIs for production — ToS + brittle + unmeasurable.

## Published prices (FACT from vendor docs, fetched 2026-09-13)

### OpenAI
Source: https://developers.openai.com/api/docs/pricing

- **Web search tool:** **$10.00 / 1k calls** + search content tokens at model rates.  
- For `gpt-4o-mini` / `gpt-4.1-mini` non-preview web search: search content tokens billed as fixed **8,000 input tokens** per call (per same pricing page).  
- Current page emphasizes newer model families (e.g. gpt-5.6-luna short-context **$0.20 / $1.20** per 1M in/out). **Re-verify the exact model ID Builder pins** before treating token math as final.

**ASSUMPTION sketch (not measured):** 1 web-search call ≈ $0.01 request fee + token costs. If using mini + 8k search block: 8000 × (model input rate)/1e6 + output tokens. Builder must replace with invoice/usage export.

### Perplexity Sonar
Source: https://docs.perplexity.ai/docs/getting-started/pricing

| Model | Input $/1M | Output $/1M | Request fee low/med/high per 1k req |
|-------|------------|-------------|--------------------------------------|
| Sonar | $1 | $1 | $5 / $8 / $12 → **$0.005 / $0.008 / $0.012** each |
| Sonar Pro | $3 | $15 | $6 / $10 / $14 |

Docs sample (low context): ~**$0.00542** total for a small Sonar call (mostly request fee).

### Perplexity Agent tools (if used as engine #3)
Same pricing page: `web_search` **$0.0025**/invocation; `fetch_url` **$0.0005**/invocation; plus underlying model tokens.

## Starter margin gate (@ $29/mo)

Target COGS **&lt;30%** of $29 ⇒ **&lt;$8.70/mo** per paying seat.

If weekly monitoring = 20 prompts × 2 engines × 4 weeks = 160 engine-calls/mo:  
max average **~$0.054**/call.  
If daily = 20 × 2 × 30 = 1200 calls/mo: max **~$0.007**/call → need caching, fewer prompts, or weekly-only on Starter.

**UNKNOWN until AC#0 pilot:** actual $/run, answer stability, which 1–2 engines survive the budget.

## Builder checklist for `product/` AC#0 artifact

1. Name ≤3 engines (IDs above or replacements with sources).  
2. Run real calls; attach usage/cost evidence (dashboard export or API `usage` fields).  
3. Publish measured $/run (mean + p95).  
4. Set Starter limits (prompts/engines/frequency) so projected COGS &lt;30% at $29.  
5. Freeze that engine list for free audit (AC#2).
