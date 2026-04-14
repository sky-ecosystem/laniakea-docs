---
id: remove-duration-matching-from-rate-hedging-methods
author: CloakyAD
date: 2026-04-15
status: pending
targets:
  - risk-framework/matching.md
---

## Summary

The "Methods of Rate Hedging" table in `risk-framework/matching.md` lists **Duration matching** as a valid rate hedging method. This directly contradicts the document's own argument: the preceding sections explain at length that ALDM (Asset-Liability Duration Matching) does *not* protect against interest rate risk — only against credit spread risk. Including it in a table of rate hedging methods creates a factual contradiction visible to any reader who reads the table alongside the prose. The row should be removed. The other three methods in the table (floating-rate assets, interest rate swaps, rate hedging capital) are all legitimate rate hedges consistent with the rest of the document.

## Changes

### CHANGE-001
- **Status:** pending
- **Type:** replacement
- **File:** `risk-framework/matching.md`
- **Section:** `## Rate Risk vs Credit Spread Risk > ### Rate Hedging Requirement > #### Methods of Rate Hedging`
- **Rationale:** The Duration matching row contradicts the document's explicit statement that "rate risk is NOT manageable with duration matching" (see the "Why rate risk is NOT manageable with duration matching" subsection). A table listing rate hedging methods must not include a technique that the document rules out as ineffective for rate risk. Removing the row eliminates the contradiction cleanly; the surrounding prose already explains why duration matching is not a rate hedge.

**Before** (must appear verbatim in the target file, ≥3 lines, unique within the file):
```
| **Interest rate swaps** | Swap fixed receipts for floating | Convert fixed-rate bonds to floating exposure |
| **Duration matching** | Match asset duration to liability duration | When liabilities have predictable duration |
| **Rate hedging capital** | Hold extra capital to cover expected rate loss | When hedging instruments unavailable or costly |
```

**After:**
```
| **Interest rate swaps** | Swap fixed receipts for floating | Convert fixed-rate bonds to floating exposure |
| **Rate hedging capital** | Hold extra capital to cover expected rate loss | When hedging instruments unavailable or costly |
```
