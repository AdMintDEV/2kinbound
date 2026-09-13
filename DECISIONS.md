# DECISIONS

## Team SELECT — Inbound Score (ACCEPTED)

See `decisions/SELECT_inbound_score.md`. ICP: B2B SaaS &lt;50 employees. Free audit → $29/mo. AC#0 engine COGS is the gate.

## D-TubeCheck — Zero-COGS parallel F-path

Ship TubeCheck without waiting for GEO engines. Reason: AC#0 list prices imply paid OpenAI/Perplexity calls; that needs keys and can become meaningful spend. TubeCheck COGS is $0 until a sale (then Stripe 2.9%+$0.30).

Does **not** cancel SELECT. It is the F2 “if GEO is blocked on auth/spend” path, executed early so the first dollar is not gated on LLM invoices.

## D-price $9

Inside the band of an existing $8.49 FSAE Excel pack. Stripe US payout minimum $0.01.

## D-not Gumroad for penny-one

Standard Gumroad payout floor is typically $100.

## D-no personal posting without approval

GitHub Pages indexing first. Reddit/Discord from Jimmy’s accounts needs explicit OK.

## D-no domain/ads yet

Spend $0 until a paying customer exists.
| 2026-09-13 | Split AC#0 into 0a ESTIMATE (PASS) / 0b measured (pre-LAUNCH) | ACCEPTED | `reviews/REVIEW_2026-09-13_AC0_PR1.md`; SELECT amended |

## D-kill static paywall (2026-09-13)

Tester proved `4130-catalog.csv` is free on Pages; `?k=` unlock is obscurity.  
**Decision:** Kill client-side paywall. First-dollar rail = merchant that delivers the file (Payhip preferred). Builder T8 removes public paid assets.
