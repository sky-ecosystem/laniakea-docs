# Sentinel Integration

**Last Updated:** 2026-01-27

## Connection to Sentinel

The Risk Framework provides the calculations that sentinel formations and LPHA beacons perform.

For full sentinel specification, see `legal-and-trading/sentinel-network.md`.
For the broader beacon taxonomy, see `synomics/beacon-framework.md`.

### Protocol-Level Beacons

| Component | Uses Risk Framework For |
|-----------|-------------------------|
| **lpla-checker** | Calculating CRR per position, TRRC, TRC, Encumbrance Ratio; Settlement cycle processing, LCTS generation handling |

### Prime-Side Sentinels

| Component | Uses Risk Framework For |
|-----------|-------------------------|
| **stl-base** | Risk monitoring during execution, deployment decisions |
| **stl-warden** | Independent risk verification, halt triggers |

### Halo-Side Sentinels (Temporary)

| Component | Uses Risk Framework For |
|-----------|-------------------------|
| **lpha-lcts** | LCTS vault capacity management, redemption processing |
| **lpha-nfat** | NFAT Facility operations, claim processing |

> **Note:** lpha-lcts and lpha-nfat are temporary sentinel types for Phase 1. Long-term, these operations migrate to standard stl-base/stl-stream/stl-warden formations.

### LPHA Beacons

| Component | Uses Risk Framework For |
|-----------|-------------------------|
| **lpha-halo** | Reporting risk metrics for Halo Units |

### Key Metrics (from Sentinel doc)

| Metric | Definition | Risk Framework Connection |
|--------|------------|---------------------------|
| **CRR** | Capital Ratio Requirement per position | Risk weight (if matched) or FRTB drawdown (if unmatched) |
| **TRRC** | Total Required Risk Capital | Sum of CRR × position size across portfolio |
| **TRC** | Total Risk Capital actually held | Actual safety capital |
| **Encumbrance Ratio** | TRRC / TRC | Capital utilization — target ≤90% |

---

## Category Caps (Correlation Framework) Outputs

If category caps are enabled (`correlation-framework.md`), Sentinel should additionally be able to report:

- Per category `c`: `cap_percent[c]`, `cap_amount[c]`, `exposure_total[c]`, `utilization[c]`
- Per Prime `p`, category `c`: `alloc[p][c]`, `E[p][c]`, `P[p][c]` (penalized amount)
- Portfolio-level: total over-cap exposure and resulting 100%-CRR-required capital
