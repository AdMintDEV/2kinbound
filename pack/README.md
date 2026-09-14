# 4130 Team Pack

This folder does not contain paid files. `pack/private/` is gitignored.

Generate the merchant upload bundle locally after clone:

```bash
python scripts/generate_team_pack.py
```

That writes `pack/private/4130-team-pack-catalog.csv`, `pack/private/PACK_NOTES.md`, and `pack/private/4130-team-pack.zip`. Upload those local paths in Payhip or Stripe. Do not commit them. Do not use a catalog from git history.

The public Pages site may show a short teaser (≤4 illustrative rows) so visitors know the checker works; that teaser is not the pack.

See `PAYMENT.md` for exact upload steps.
