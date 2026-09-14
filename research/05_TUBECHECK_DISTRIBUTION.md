# T9 — TubeCheck distribution (first buyers @ $0 spend)

**Author:** Research Agent (2k)  
**Updated:** 2026-09-13  
**Product:** https://admintdev.github.io/2kinbound/  
**Constraint:** No outbound posts by agents. All draft copy = **NEEDS HUMAN APPROVAL**.  
**Policy (2026-09-14):** Soft-launch = **free checker only** (no Buy / no Team Pack / no sandbox Stripe). Pack leakage closed on tip (404). Live merchant still missing — do **not** advertise paid CTA. See `experiments/active/tubecheck_KILL.md` (T16).

## Ranking (expected time-to-first-buyer, $0 spend)

ASSUMPTION ranking — TubeCheck has no conversion history (UNKNOWN). Ordered for **speed to a chassis-lead conversation**.

| Rank | Channel | Est. days to first serious reply* | Spend |
|------|---------|-----------------------------------|-------|
| 1 | r/FSAE value post | 1–3 | $0 |
| 2 | FSAE.com Open Discussion | 2–7 | $0 |
| 3 | r/FSAE Discord | 1–5 | $0 |
| 4 | DesignJudges 2026 frame-rules engagement | 3–10 | $0 |
| 5 | FSAE.com Classifieds/tools (if rules allow) | 3–14 | $0 |
| 6 | Organic SEO on Size A–D queries | 14–60 | $0 |
| 7 | Facebook DesignIt.BuildIt.RaceIt engagement | 7–21 | $0 |
| 8 | Email 5–10 university chassis leads | 3–14 | $0 |
| 9 | LinkedIn personal post | 7–21 | $0 |
| 10 | YouTube comments on chassis tutorials | 7–30 | $0 |

\*ASSUMPTION. Kill channel after 2 failed attempts (anti-loop).

## Channels

### C1 — Reddit r/FSAE
- **URL:** https://www.reddit.com/r/FSAE/
- **Evidence:** Active sub; Discord reminder https://www.reddit.com/r/FSAE/comments/1qyggyv/we_have_a_discord/ (2026-02-07)
- **Access:** Reddit account; follow rules; no hard sell
- **Fit:** High
- **Risk:** Promo removal / ban
- **Human approval:** **YES — required**

### C2 — FSAE.com Open Discussion
- **URL:** https://www.fsae.com/forums/forumdisplay.php?45-Open-FSAE-Discussion
- **Hub:** https://www.fsae.com/forums/forum.php
- **Evidence:** Forum home reports ~12.5k threads / ~128k posts / ~15k members (site-reported)
- **Access:** Register; post Open Discussion (or Static Events if SES-specific)
- **Fit:** Highest historical intent
- **Risk:** Anti-commercial norms; unofficial-tool skepticism
- **Human approval:** **YES**

### C3 — r/FSAE Discord
- **Invite (from subreddit):** https://discord.gg/JHA3asr8xH
- **Evidence:** same Discord reminder post as C1
- **UNKNOWN:** invite may expire — re-check before use
- **Access:** Join; read rules; soft-share only
- **Fit:** Fast student feedback
- **Risk:** Spam channels / invite abuse
- **Human approval:** **YES** (D-policy: no personal posting without approval)

### C4 — DesignJudges.com 2026 frame rules
- **URL:** https://www.designjudges.com/articles/guide-to-2026-frame-rule-changes
- **Evidence:** Live article on 2026 frame/tubing changes for chassis designers
- **Access:** Comment/share if allowed; humble + “unofficial / not SES”
- **Fit:** High topical
- **Risk:** Spam under judge-facing content
- **Human approval:** **YES**

### C5 — FSAE.com Classifieds
- **URL:** https://www.fsae.com/forums/forum.php (Classifieds category)
- **Access:** Only if rules allow free tools listing
- **Fit:** Medium
- **Risk:** Wrong category → deleted
- **Human approval:** **YES** (read rules first — UNKNOWN without account)

### C6 — Organic SEO (owned)
- **URL:** https://admintdev.github.io/2kinbound/
- **Access:** Title/meta/H1 for “FSAE 2026 tubing size A B C D checker” + disclaimer via PR
- **Fit:** Compounds slowly
- **Risk:** Weak Pages SEO
- **Human approval:** Content PRs OK; no third-party posting

### C7 — Facebook page linked from FSAE.com
- **URL:** http://www.facebook.com/DesignIt.BuildIt.RaceIt (linked from fsae.com forum UI)
- **Access:** Human profile/page engagement
- **Fit:** Medium
- **Risk:** Low organic reach
- **Human approval:** **YES**

### C8 — University team contact (example)
- **Example public page:** https://www.utoledofsae.com/new (`fsae@utoledo.edu` listed)
- **Access:** Personalized human email to chassis/frame leads; do **not** spam team recruit Discords
- **Fit:** Direct ICP
- **Risk:** Cold-email fatigue
- **Human approval:** **YES always**; max ~10/day personalized

### C9 — LinkedIn (human personal)
- **Access:** Human posts #FormulaSAE #FSAE
- **Fit:** Advisors/alumni
- **Risk:** Low reach without network
- **Human approval:** **YES**

### C10 — YouTube comments
- **Access:** Human picks 3 “FSAE chassis 4130” videos (specific URLs UNKNOWN until chosen)
- **Fit:** Active learners
- **Risk:** Comment spam filters
- **Human approval:** **YES**

### Not primary
- **ApexSpeed** https://www.apexspeed.com/forums/forum.php — SCCA/amateur formula focus, weak FSAE ICP
- Roster scraping, Discord raids, paid ads before first sale — forbidden / deferred

## Draft posts — NEEDS HUMAN APPROVAL — DO NOT POST

### Draft A-free — r/FSAE soft-launch (CURRENT — free checker only)
**Status:** Ready for human approval under Goal Manager soft-launch policy. **No Buy. No Team Pack. No sandbox Stripe.**  
**Title:** Unofficial FSAE 2026 Size A/B/C/D tube checker (not SAE / not SES)  
**Body:**
> Built a free browser tool that checks steel tube OD/wall against the 2026 Size A–D tables and nests 4130 stick cuts.
>
> Important: **not SAE, not a substitute for the official SES.** Use the rulebook + SES for anything that matters in tech. Inch examples vs mm tables can disagree by tenths of a mm — we surface that (e.g. published 1.375×0.049 vs 35.0 mm Size D OD).
>
> Live: https://admintdev.github.io/2kinbound/
>
> Looking for chassis leads to break edge cases. If the checker disagrees with the rulebook, comment with the Size + dims — I’ll fix it.

### Draft A-paid — r/FSAE (HELD until live merchant)
**Status:** **HELD.** Do not post while `paymentUrl` is sandbox/`test_` or delivery unverified.  
**Title:** Unofficial FSAE 2026 Size A/B/C/D tube checker (not SAE / not SES)  
**Body:**
> Built a free browser tool that checks steel tube OD/wall against the 2026 Size A–D tables and nests 4130 stick cuts.
>
> Important: **not SAE, not a substitute for the official SES.** Inch examples vs mm tables can disagree by tenths of a mm — we surface that.
>
> Live: https://admintdev.github.io/2kinbound/
>
> Looking for chassis leads to break it. If something’s wrong vs the rulebook, tell me.
>
> (Optional Team Pack is separate; free checker stays free.) ← only after **live** Payhip/Stripe + delivery PASS

### Draft B — FSAE.com Open Discussion (Rank 2) — soft-launch OK (no Buy)
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
>
> (No paid product pitch in this soft-launch version.)

### Draft C — Discord (Rank 3) — soft-launch OK (no Buy)
> Free unofficial 2026 Size A–D tube checker + 4130 nest (not SAE/SES): https://admintdev.github.io/2kinbound/ — looking for chassis folks to break edge cases. Happy to move if wrong channel. (No pack/Buy link.)

## Prerequisites

### Soft-launch post (Draft A-free / B / C no-Buy)
1. Pack CSV still 404 on Pages (T8/T12).
2. Human approves exact text.
3. Human posts from a real account — agents do not post.
4. Log under `market/customer_signals/` (date, channel, URL, replies).
5. **Do not** mention Team Pack, $9, Stripe, Payhip, or sandbox checkout.

### Paid CTA post (Draft A-paid)
1. Soft-launch prerequisites, plus:
2. **Live** (non-`test_`) merchant URL in `docs/config.js`.
3. Paid file delivery verified (Payhip attach or equivalent).
4. Tester/Reviewer OK that Buy does not leak free assets.

## Next (Goal Manager / Human)
Approve **Draft A-free** when ready for soft-launch feedback. Keep **Draft A-paid** held until live merchant.
