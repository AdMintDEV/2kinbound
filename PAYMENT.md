# PAYMENT

TubeCheck cannot collect money until a merchant link exists **and** paid files are not free on GitHub Pages.

**$0 to set up. No domain purchase.**

T8 removed the full catalog from public `docs/`. Pages publishes `docs/` only. Upload files from `pack_assets/`.

## Preferred: Payhip (digital delivery)

Static Pages cannot securely gate files. Payhip hosts the paid download.

1. Open [https://payhip.com](https://payhip.com) and create an account (or log in).
2. Create a digital product: `4130 Team Pack` — **$9.00 USD**.
3. Upload paid files from `pack_assets/` (not from `docs/`):
   - `4130-catalog.csv` (full catalog)
   - Optional: `PACK_NOTES.md`
4. Publish and copy the product checkout URL.
5. Paste the URL in chat (or into `docs/config.js` as `paymentUrl`).
6. Do not set a success URL that downloads files from GitHub Pages.

## Fallback: Stripe Payment Link

Only use if Payhip is blocked. Stripe Payment Link does **not** host files — you still need a delivery method (email the CSV after payment, or a private URL you rotate).

1. [Stripe register](https://dashboard.stripe.com/register) → identity + bank (US payout min $0.01).
2. Payment Links → New → `4130 Team Pack` → **$9.00** one time.
3. Success redirect (thank-you only, no assets):  
   `https://admintdev.github.io/2kinbound/pack.html`
4. Paste Payment Link URL (`https://buy.stripe.com/...`) into chat.
5. Delivery: email `pack_assets/4130-catalog.csv` manually for the first sales, or add a private host later.

## Do not

- Do not send API keys.
- Do not copy `pack_assets/4130-catalog.csv` back into `docs/`.
- Do not publish unlock tokens or `?k=` secrets in client JS.
- Do not treat `pack.html` as a download page. It is thank-you copy only.
