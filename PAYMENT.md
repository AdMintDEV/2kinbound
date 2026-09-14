# PAYMENT

TubeCheck cannot collect money until a merchant link exists **and** paid files are not in this public repository (Pages, git tree, or raw GitHub URLs).

**$0 to set up. No domain purchase.**

Static Pages and a public git repo cannot securely gate files. `pack.html` is a post-pay / status landing only — it does not host or link paid files. The owner generates a **rotated** catalog locally and attaches those files privately in the merchant dashboard.

Do not commit the catalog, zip, or `PACK_NOTES.md` anywhere in this repo. Do not upload any file recovered from git history (old SHAs still serve the leaked public CSV).

## Generate the private upload bundle (after clone)

Paid files are **not** in git. After clone, build them on your machine:

```bash
python scripts/generate_team_pack.py
```

That writes **only** these local, gitignored paths (never add them):

| File | Path |
|------|------|
| Catalog CSV | `pack/private/4130-team-pack-catalog.csv` |
| Notes / disclaimer | `pack/private/PACK_NOTES.md` |
| Zip of both | `pack/private/4130-team-pack.zip` |

Confirm they stay untracked:

```bash
git check-ignore -v pack/private/*
git status
```

`git check-ignore` should match `pack/private/`. `git status` must not list those files as staged. If they appear, you force-added them — unstage and do not push.

## Preferred: Payhip (digital delivery)

Payhip hosts the paid download.

1. Open [https://payhip.com](https://payhip.com) and create an account (or log in).
2. Create a digital product: `4130 Team Pack` — **$9.00 USD**.
3. In the product file upload, attach **only** these local files (or the zip as a single attachment):
   - `pack/private/4130-team-pack-catalog.csv`
   - `pack/private/PACK_NOTES.md`
   - or `pack/private/4130-team-pack.zip`
4. Do **not** attach `docs/4130-catalog.csv` from any git SHA, raw GitHub URL, or gist.
5. Publish and copy the product checkout URL.
6. Paste the URL into `docs/config.js` as `paymentUrl`.
7. Confirm this repo still has no paid catalog file (`git ls-files '*catalog*' 'pack/private/*'` is empty of CSV/zip/notes).

## Fallback: Stripe Payment Link + file attachment

Only use if Payhip is blocked. A Payment Link alone does not host files — attach the catalog on the Stripe product from the same local `pack/private/` files (or email them after payment).

1. [Stripe register](https://dashboard.stripe.com/register) → identity + bank (US payout min $0.01).
2. Payment Links → New → `4130 Team Pack` → **$9.00** one time.
3. Attach `pack/private/4130-team-pack.zip` (or the CSV + `PACK_NOTES.md`) from your local clone. Not from git history.
4. Success redirect (thank-you only, **no assets**):
   `https://admintdev.github.io/2kinbound/pack.html?paid=1`
5. Paste Payment Link URL (`https://buy.stripe.com/...`) into `docs/config.js` as `paymentUrl`.

## Do not

- Do not send API keys.
- Do not put the paid catalog (or any paid exclusive) in `docs/`, `pack/` (except generating into ignored `pack/private/`), `data/`, or anywhere else in this git tree.
- Do not `git add -f` `pack/private/` or the CSV/zip/notes.
- Do not link a gist, raw GitHub URL, or other public stand-in for the file.
- Do not treat `?k=` / `?paid=1` / an empty `paymentUrl` as a paywall.
- Do not auto-unlock the pack when checkout is unconfigured.
- Do not sell the historically public `4130-catalog.csv` from an old commit.
