"""20-prompt B2B SaaS GEO / AI-visibility set for the AC#0 pilot.

Templates only. The harness never invents citation rows from these strings.
"""

from __future__ import annotations

from dataclasses import dataclass


SYSTEM_PROMPT = """You are answering a buyer question about B2B software.
Return ONLY JSON with keys:
  mentioned_brand (boolean),
  mentioned_url (boolean),
  other_vendors (array of strings),
  sources_named (array of strings the model itself stated; empty if none),
  snippet (string, <= 80 words).
Do not invent URLs, rankings, or citations that you cannot support from
your own answer text. If you are unsure whether the brand appears, set
mentioned_brand to false. This is a visibility probe, not advice to buy.
"""


@dataclass(frozen=True)
class BrandContext:
    brand: str
    url: str
    category: str
    competitor: str


# Neutral fixture — not a real audit of this domain, only token-shaped input.
DEFAULT_BRAND = BrandContext(
    brand="Northwind Analytics",
    url="https://www.example.com",
    category="B2B product analytics for SaaS teams under 50 employees",
    competitor="Mixpanel",
)


PILOT_PROMPTS: tuple[str, ...] = (
    "What are the best {category} tools for a B2B SaaS company with fewer than 50 employees?",
    "Recommend {category} software for an early-stage B2B SaaS marketing or growth team.",
    "Which vendors would you shortlist for {category} in 2026, and why?",
    "Is {brand} ({url}) a reasonable {category} option for a 20-person SaaS company?",
    "What tools are like {brand}?",
    "Best alternatives to {brand} for small B2B SaaS teams.",
    "{brand} vs {competitor}: which should a startup pick first?",
    "Who are the top competitors to {brand} in {category}?",
    "Does anyone recommend {brand} for inbound pipeline or product-led growth?",
    "What {category} product do small B2B SaaS teams mention most often?",
    "How should a founder choose a {category} vendor with a budget under $100/month?",
    "Which {category} tools integrate well with Stripe, HubSpot, or Slack?",
    "List GTM or SEO tools a B2B SaaS under 50 employees should consider; include {brand} only if relevant.",
    "For AI-visibility or GEO monitoring aimed at small B2B SaaS, which product names come up?",
    "Would you mention {url} when answering questions about {category}?",
    "What pages or claims from {brand} would you actually quote, if any?",
    "Summarize {brand}'s positioning in {category} and name similar products.",
    "For the query 'best {category} for B2B startups', which brands belong on a five-name list?",
    "Is {brand} a leader, challenger, or niche player in {category}? Say if you cannot tell.",
    "Write a one-paragraph buyer recommendation for {category} aimed at a 15-person B2B SaaS.",
)


assert len(PILOT_PROMPTS) == 20


def render_prompt(template: str, brand: BrandContext = DEFAULT_BRAND) -> str:
    return template.format(
        brand=brand.brand,
        url=brand.url,
        category=brand.category,
        competitor=brand.competitor,
    )


def brand_block(brand: BrandContext = DEFAULT_BRAND) -> str:
    return (
        f"Brand name: {brand.brand}\n"
        f"Brand URL: {brand.url}\n"
        f"Category: {brand.category}\n"
        f"Named competitor (for comparison prompts): {brand.competitor}\n"
    )
