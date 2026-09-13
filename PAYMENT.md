# PAYMENT

TubeCheck cannot collect money until a merchant link exists. This is the only required human step. **$0 to set up. No domain purchase.**

## Do this (about 5 minutes if Stripe already verifies ID)

1. Open [https://dashboard.stripe.com/register](https://dashboard.stripe.com/register) and create an account (or log in).
2. Complete identity + bank so payouts can actually leave Stripe. US payout minimum is $0.01.
3. Go to **Payment Links** → **New**.
4. Product name: `4130 Team Pack`
5. Price: **$9.00 USD** one time
6. After payment, redirect customers to:

```
https://AdMintDEV.github.io/2kinbound/pack.html?k=2k4130pack
```

(If GitHub Pages uses a different URL, use that origin + `/pack.html?k=2k4130pack`.)

7. Copy the Payment Link URL (starts with `https://buy.stripe.com/`).
8. Paste it into `docs/config.js` as `paymentUrl`, or reply in chat with the URL and I will paste it and push.

Payhip is the fallback if Stripe KYC is stuck: create a $9 digital product, upload `docs/pack.html` contents / the CSV, and send me that checkout URL instead.

Do **not** send API keys. The public Payment Link is enough.
