# PAYMENT

TubeCheck cannot collect money until a merchant link exists **and** paid files are not in this public repository (Pages, git tree, or raw GitHub URLs).

**$0 to set up. No domain purchase.**

Static Pages and a public git repo cannot securely gate files. `pack.html` is a post-pay / status landing only — it does not host or link paid files. The owner attaches the catalog privately in the merchant dashboard. Do not commit the catalog anywhere in this repo.

## Preferred: Payhip (digital delivery)

Payhip hosts the paid download.

1. Open [https://payhip.com](https://payhip.com) and create an account (or log in).
2. Create a digital product: `4130 Team Pack` — **$9.00 USD**.
3. Attach the catalog from a **private** copy (not from this repo).
4. Publish and copy the product checkout URL.
5. Paste the URL into `docs/config.js` as `paymentUrl`.
6. Confirm this repo still has no paid catalog file.

## Fallback: Stripe Payment Link + file attachment

Only use if Payhip is blocked. A Payment Link alone does not host files — attach the catalog on the Stripe product from a private copy (or email it after payment).

1. [Stripe register](https://dashboard.stripe.com/register) → identity + bank (US payout min $0.01).
2. Payment Links → New → `4130 Team Pack` → **$9.00** one time.
3. Attach the catalog as the product file from a private copy (or deliver by email).
4. Success redirect (thank-you only, **no assets**):
   `https://admintdev.github.io/2kinbound/pack.html?paid=1`
5. Paste Payment Link URL (`https://buy.stripe.com/...`) into `docs/config.js` as `paymentUrl`.

## Do not

- Do not send API keys.
- Do not put the paid catalog (or any paid exclusive) in `docs/`, `pack/`, `data/`, or anywhere else in this git tree.
- Do not link a gist, raw GitHub URL, or other public stand-in for the file.
- Do not treat `?k=` / `?paid=1` / an empty `paymentUrl` as a paywall.
- Do not auto-unlock the pack when checkout is unconfigured.
