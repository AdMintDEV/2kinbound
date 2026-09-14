# T17 — TubeCheck soft-launch drafts (free checker only)

**Author:** Research Agent (2k)  
**Updated:** 2026-09-14  
**Live tool:** https://admintdev.github.io/2kinbound/  
**Policy:** Goal Manager soft-launch — free checker feedback only.  
**Hard rules:** No Buy · No $9 · No Team Pack · No Stripe · No payment CTA · Agents do **not** post.

Every draft below = **NEEDS HUMAN APPROVAL — DO NOT POST.**

Related: `research/05_TUBECHECK_DISTRIBUTION.md`, `experiments/active/tubecheck_KILL.md` (T16).

## Channel rank (soft-launch order)

| Order | Channel | Why first | Human approval |
|-------|---------|-----------|----------------|
| 1 | r/FSAE | Fastest serious chassis feedback @ $0 | **Required** |
| 2 | FSAE.com Open Discussion | Highest-intent historical forum | **Required** |
| 3 | r/FSAE Discord | Fast iterate; invite may expire | **Required** |

Do **not** run paid Draft A / pack CTAs until live (non-`test_`) merchant + delivery PASS.

---

## Draft A — r/FSAE (RECOMMENDED FIRST)

**NEEDS HUMAN APPROVAL — DO NOT POST**

**Title:** Unofficial FSAE 2026 Size A/B/C/D tube checker (not SAE / not SES)

**Body:**
> Built a free browser tool that checks steel tube OD/wall against the 2026 Size A–D tables and nests 4130 stick cuts.
>
> Important: **not SAE, not a substitute for the official SES.** Use the rulebook + SES for anything that matters in tech. Inch examples vs mm tables can disagree by tenths of a mm — we surface that (e.g. published 1.375×0.049 vs 35.0 mm Size D OD).
>
> Live: https://admintdev.github.io/2kinbound/
>
> Looking for chassis leads to break edge cases. If the checker disagrees with the rulebook, comment with the Size + dims — I’ll fix it.

**Must omit:** Buy, $9, Team Pack, Stripe, Payhip, payment, checkout, sandbox.

---

## Draft B — FSAE.com Open Discussion

**NEEDS HUMAN APPROVAL — DO NOT POST**

**Forum:** https://www.fsae.com/forums/forumdisplay.php?45-Open-FSAE-Discussion

**Subject:** Browser Size A–D / 4130 nest helper for 2026 (unofficial)

**Body:**
> Posting a small free tool for tube-frame teams working 2026 Size A/B/C/D:
> https://admintdev.github.io/2kinbound/
>
> Disclaimers: unofficial, not SAE, not SES, not tech. Use the official rulebook + SES.
>
> Why it exists: testing caught the published 1.375×0.049 vs 35.0 mm Size D OD mismatch (~0.075 mm).
>
> Feedback welcome from anyone deep in frame/SES this season.

**Must omit:** any paid product / checkout language.

---

## Draft C — r/FSAE Discord (short)

**NEEDS HUMAN APPROVAL — DO NOT POST**

**Invite evidence (may expire):** https://discord.gg/JHA3asr8xH — from https://www.reddit.com/r/FSAE/comments/1qyggyv/we_have_a_discord/

**Message:**
> Free unofficial 2026 Size A–D tube checker + 4130 nest (not SAE / not SES): https://admintdev.github.io/2kinbound/ — looking for chassis folks to break edge cases. Happy to move if wrong channel.

**Must omit:** Buy / pack / payment.

---

## Before human posts
1. Confirm live CSV still 404: `https://admintdev.github.io/2kinbound/4130-catalog.csv`
2. Approve exact text (edit freely).
3. Post from a real human account.
4. Log date/channel/URL/replies in `market/customer_signals/`.

## After soft-launch
Keep Draft A-paid held until live merchant (see `research/05_TUBECHECK_DISTRIBUTION.md`). Sandbox Stripe must not appear in community posts.
