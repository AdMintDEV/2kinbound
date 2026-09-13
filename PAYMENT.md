# PAYMENT

TubeCheck cannot collect money until a merchant link exists **and** paid files are not free on GitHub Pages.

**$0 to set up. No domain purchase.**

Static Pages cannot securely gate files. The full catalog lives in `pack/4130-catalog.csv` (repo source for the owner). It must **not** be copied into `docs/` (the Pages publish root). `pack.html` is a post-pay / status landing only — it does not host or link the file.

## Preferred: Payhip (digital delivery)

Payhip hosts the paid download.

1. Open [https://payhip.com](https://payhip.com) and create an account (or log in).
2. Create a digital product: `4130 Team Pack` — **$9.00 USD**.
3. Upload paid files from this repo:
   - `pack/4130-catalog.csv` (full catalog)
   - Optional: a short README / pack notes
4. Publish and copy the product checkout URL.
5. Paste the URL into `docs/config.js` as `paymentUrl`.
6. Confirm `docs/` still has no `4130-catalog.csv`.

## Fallback: Stripe Payment Link + file attachment

Only use if Payhip is blocked. A Payment Link alone does not host files — attach the catalog on the Stripe product (or email it after payment).

1. [Stripe register](https://dashboard.stripe.com/register) → identity + bank (US payout min $0.01).
2. Payment Links → New → `4130 Team Pack` → **$9.00** one time.
3. Attach `pack/4130-catalog.csv` as the product file (or deliver by email).
4. Success redirect (thank-you only, **no assets**):
   `https://admintdev.github.io/2kinbound/pack.html?paid=1`
5. Paste Payment Link URL (`https://buy.stripe.com/...`) into `docs/config.js` as `paymentUrl`.

## Do not

- Do not send API keys.
- Do not put `4130-catalog.csv` (or any paid exclusive) in `docs/`.
- Do not treat `?k=` / `?paid=1` / an empty `paymentUrl` as a paywall.
- Do not auto-unlock the pack when checkout is unconfigured.
