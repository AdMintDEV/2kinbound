# TASK_QUEUE

Statuses: TODO | IN_PROGRESS | BLOCKED | VERIFIED | COMPLETE

Team queue also lives in `04_TASK_QUEUE.md`.

## T8 (ACTIVE — highest leverage)
Objective: Make TubeCheck able to collect $9 safely  
Status: IN_PROGRESS  
Owner: Builder  
Depends: Human Stripe Payment Link (`PAYMENT.md`) for full completion; gate fix can ship without it  
Success: (1) unpaid visitors cannot read pack assets when `paymentUrl` is set; (2) Buy CTA opens Payment Link; (3) paid redirect `?k=2k4130pack` unlocks pack; (4) `paymentUrl` committed when human pastes URL  
Evidence: `docs/pack.html`, `docs/config.js`, `docs/app.js` + Tester report  

## T9
Objective: Distribution plan for first TubeCheck buyers  
Status: TODO  
Owner: Research  
Success: 5–10 concrete channels with URLs + draft copy; marked needs-human-approval where posting required  
Evidence: `research/05_TUBECHECK_DISTRIBUTION.md`

## T3b / AC#0b
Objective: Measured Inbound Score engine COGS  
Status: BLOCKED (keys/spend)  
Depends: Human API keys + spend approval  
Evidence target: `product/` measured artifact

## TASK-101
Objective: Encode F.3.4 2026 minima and tube geometry with tests  
Status: VERIFIED

## TASK-102
Objective: TubeCheck static site  
Status: VERIFIED — public https://admintdev.github.io/2kinbound/

## TASK-103
Objective: $9 Team Pack files  
Status: VERIFIED (`docs/pack.html`, `docs/4130-catalog.csv`) — gate leak open (T8)

## TASK-104
Objective: Real checkout  
Status: BLOCKED — human Stripe Payment Link (`PAYMENT.md`)

## TASK-105
Objective: GitHub Pages public URL  
Status: COMPLETE — live
