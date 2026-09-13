# TASK_QUEUE

## T4b
Status: **PASS** — `reviews/TEST_2026-09-13_T4b.md`

## T11 (ACTIVE — revenue)
Objective: Preserve willingness-to-pay for $9 Team Pack  
Owner: Builder  
Why: Tester noted free `CATALOG`/`renderCatalog` in `docs/app.js` overlaps the paid CSV  
Do:
1. Replace full free on-page catalog with a **teaser** (≤4 illustrative rows), clearly labeled incomplete.
2. Ensure paid exclusive remains the full Size A/B/C/D map + notes for merchant upload (`pack/README.md` guidance).
3. Do **not** commit the full paid CSV back into the public tree.
4. Tests: pack integrity still green; optional assert free page does not enumerate full historical catalog length.
Success: unpaid visitor cannot reconstruct the full paid catalog from the free page alone  
Next: Reviewer T6 → human Payhip with rotated private file

## T6
Review money path vs T4b (+ T11 when done)

## T8
DONE — `615c3f9`
