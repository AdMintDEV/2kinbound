# DISCOVER → VALIDATE

**Status:** COMPLETE (v1)  
**Author:** Research Agent (2k)  
**Updated:** 2026-09-13  
**Confidence overall:** MEDIUM (precedents verified; our wedge not yet customer-validated)

## OBJECTIVE

Find an internet business path to **~$2,000/month profit** with **minimal human involvement**, matching mission favors (async/digital/subscription/automated distribution/low OpEx) and avoids (no client work, no spam, no fabricated claims).

## FINDINGS

Ranked candidates (higher = better fit for this team right now):

### 1. Niche completed-sales / comps **data API** (SoldComps pattern) — PRIMARY PATTERN
- **What:** Paid REST API returning structured market comps from a hard-to-access source; freemium → $9/$29/$79 tiers.
- **Why it fits:** Subscription + API = asynchronous revenue; set-and-forget ops; digital; no calls; distribution via docs/SEO/dev communities.
- **Evidence:** TrustMRR (Stripe-verified) lists SoldComps at **~$15k MRR**, **400+** active subscriptions, pricing Free/$9/$29/$79 — https://trustmrr.com/startup/soldcomps and https://sold-comps.com/
- **FACT:** SoldComps exists and publishes that pricing; TrustMRR claims Stripe verification.
- **ASSUMPTION:** A *different* legal public/licensed dataset can reach similar economics.
- **UNKNOWN:** Which alternate dataset we can legally productize without ToS/scraping risk.
- **Fit score intuition:** High autonomy, proven $2k+ path exists in category; legal/data sourcing is the hard part.

### 2. **Inbound free tool → paid monitoring** (fits repo name `2kinbound`) — PRIMARY BUILD WEDGE
- **What:** Free URL checker for “inbound readiness” (technical SEO basics + AI-answer / citation readiness) → Stripe paywall for full report history + weekly monitors + alerts.
- **Why it fits:** Automated distribution (the free tool is the funnel); subscription for monitoring; low touch; brand-aligned.
- **Evidence of demand / willingness to pay:**
  - Enterprise SEO priced high (Ahrefs/Semrush commonly cited ~$99–$140+/mo on competitor landing pages such as https://jackpotkeywords.web.app/ and https://sealseo.com/).
  - Indie alternatives already charge: SealSEO **$20/mo** (Pro) / **$49/mo** (Agency) per https://sealseo.com/; JackpotKeywords **$9.99/mo**.
  - Organic-only indie SaaS reaching ~$2k: MediaFa.st founder report **$2k MRR** (Oct 6, 2025) https://www.indiehackers.com/post/building-a-reddit-marketing-saas-to-2k-mrr-in-a-don-t-get-banned-world-683f8af49c ; SupaBird story ~**$2,057**/30d organic https://www.mrrstory.com/stories/from-0-to-2057month-using-only-organic-traffic
- **Counter-evidence (important):** Several SEO micro-SaaS on TrustMRR show **tiny** verified MRR (e.g. SeoLoupe ~$72 MRR, Seozast ~$36 MRR) — category is crowded and many products do not clear $2k.
- **FACT:** Cheap SEO tools exist and charge; $2k MRR indie stories exist; many SEO micros fail to scale.
- **ASSUMPTION:** A sharper wedge (AI-search / answer-engine visibility + inbound checklist) can differentiate from generic “SEO audit.”
- **UNKNOWN:** Conversion rate free→paid; LLM/API cost per free check; whether ICP will pay for monitoring vs one-shot audits.

### 3. Set-and-forget **database backup automation**
- **Evidence:** SimpleBackups public pricing Lite **$49/mo**, Plus **$99/mo**, Max **$299/mo** — https://www.simplebackups.com/pricing ; MicroGaps narrative cites category validation (secondary source).
- **Fit:** High autonomy once live.
- **Risk:** Trust, security, compliance, and onboarding friction; slower first dollar for a new brand; support spikes on restore failures.
- **Verdict:** Strong long-term pattern; weaker as *first* ship for this team.

### 4. Social/content planning SaaS (MediaFa.st class)
- **Evidence:** MediaFa.st **$2k MRR** self-report (Indie Hackers, 2025-10-06).
- **Risk vs mission:** Easy to drift into spammy growth tactics; platform ToS/ban risk; ongoing content labor.
- **Verdict:** Validated revenue, poor mission fit as primary.

### 5. Generic AI PDF chat tool
- **Evidence:** Crowded (ChatPDF, Smallpdf Chat PDF, PDF.ai, NotebookLM, etc.) with free tiers and $5–$20 entry pricing (roundups e.g. https://paperguide.ai/blog/ai-tools-to-chat-with-pdf/).
- **Verdict:** Reject for v1 — commoditized, high LLM OpEx, weak wedge.

### 6. Vertical compliance / certification trackers
- **Evidence:** Idea-list literature (e.g. emergent.sh micro-SaaS roundup) claims buyers exist; **no primary revenue verification pulled in this pass**.
- **Verdict:** PARK — needs customer interviews / competitor pricing pages before SELECT.

## EVIDENCE (URL index)

| URL | Supports |
|-----|----------|
| https://trustmrr.com/startup/soldcomps | Stripe-verified ~$15k MRR data-API precedent; pricing tiers |
| https://sold-comps.com/ | Product shape: freemium comps API |
| https://www.simplebackups.com/pricing | Backup SaaS price anchors $49–$299 |
| https://sealseo.com/ | Indie SEO suite pricing $20 / $49 |
| https://jackpotkeywords.web.app/ | Keyword tool $9.99 vs Ahrefs/SEMrush price claims |
| https://www.indiehackers.com/post/building-a-reddit-marketing-saas-to-2k-mrr-in-a-don-t-get-banned-world-683f8af49c | Self-reported $2k MRR organic SaaS |
| https://www.mrrstory.com/stories/from-0-to-2057month-using-only-organic-traffic | Organic ~$2k/mo story (SupaBird) |
| https://trustmrr.com/startup/seoloupe | Counter: SEO micro at ~$72 MRR |
| https://trustmrr.com/startup/seozast | Counter: SEO micro at ~$36 MRR |
| https://www.indiehackers.com/post/2k-mrr-after-228-days-this-is-what-building-a-saas-really-looks-like-435b69c112 | Ferndesk $2k MRR but high founder labor (autonomy warning) |

## RECOMMENDATION

**Select for BUILD (v1):** **Inbound Readiness Checker** — free single-URL inbound/AEO audit + paid **$19/mo** monitoring (working name: *Inbound Score* / fits `2kinbound`).

**Rationale:**
1. Aligns with project name and automated distribution (free tool is the funnel).
2. Subscription monitoring matches async revenue + low touch better than one-off client SEO.
3. Price envelope supported by live indie SEO products ($9.99–$49).
4. Avoids spam-adjacent social automation and avoids high-trust backup/compliance on day one.
5. Unit economics controllable if free tier is rate-limited and paid tier caps crawl/LLM spend.

**Parallel research track (T2b):** Identify **one legal dataset** for a SoldComps-style API as Plan B / Scale path — do not scrape ToS-hostile sources.

**Confidence:** MEDIUM on pattern; LOW-MEDIUM on this exact wedge until 10–20 waitlist emails or first paid conversion.

## RISKS

| Risk | Severity | Mitigation |
|------|----------|------------|
| SEO tool graveyard (many <$100 MRR) | High | Narrow wedge to AI-answer visibility + inbound checklist; kill if no paid conversion in 30 days post-launch |
| LLM / crawl cost eats margin | High | Hard rate limits; cache; paid-only deep scans |
| Commodity perception vs Ahrefs | Med | Do not compete on backlinks index; compete on “inbound score + weekly delta” |
| Data-API Plan B legal risk | High | Only public/licensed APIs; counsel/ToS review before scrape |
| Founder-labor trap (Ferndesk lesson) | Med | No sales calls; self-serve Stripe only |

## UNKNOWN INFORMATION

- Exact search volume for target keywords (need keyword tool run) — **UNKNOWN**
- Our CAC via organic for this brand — **UNKNOWN**
- Legal dataset shortlist for Plan B — **UNKNOWN**
- Hosting + LLM cost per free audit — **UNKNOWN** (must measure in BUILD)
- Whether users pay for *monitoring* vs one-shot PDF report — **UNKNOWN**

## NEXT ACTION

1. **Research (T2):** Write `decisions/SELECT_inbound_score.md` with acceptance criteria for MVP (below) and mark SELECT done unless Reviewer objects within one cycle.
2. **Builder (T3):** Implement MVP per AC.
3. **User:** Sign in to GitHub on the box (or `gh auth login`) so the initial commit can be pushed — empty remote still blocks Cursor cloud agents.

### Draft MVP acceptance criteria (for Builder)

1. Public landing page explaining Inbound Score + pricing.
2. Free: submit URL → receive score breakdown (technical inbound basics + AI-visibility heuristics) without human review.
3. Paid: Stripe Checkout **$19/mo**; authenticated dashboard with score history + weekly re-check job.
4. Hard free-tier rate limit (e.g. 3 audits / IP / day) documented.
5. Automated test suite covering: valid URL, invalid URL, rate limit, checkout session creation (test mode), webhook marks subscription active.
6. No spam features; no outbound messaging to third parties.
