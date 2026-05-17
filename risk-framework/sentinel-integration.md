# Sentinel Integration

**Last Updated:** 2026-05-05

## Connection to Sentinel

The Risk Framework provides the calculations that Prime operating setups (baseline-relay + warden-relay + stream-sentinel) and other high-authority action beacons perform.

For full sentinel specification, see `sentinel/sentinel-network.md`.
For the broader beacon taxonomy (two-tier authority + I/O role), see [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md).

### Protocol-Level (Synserv-Run)

| Component | Uses Risk Framework For |
|-----------|-------------------------|
| **synserv verification (in-space calculation)** | Calculating CRR per position, TRRC, TRC, Encumbrance Ratio; settlement cycle processing; LCTS generation handling. Calculation runs as synart-resolved code inside synserv against current input atoms (chain reads / market-memory reducer outputs / attest-data). See [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) and [`../../noemar-synlang/listener-loops.md`](../../noemar-synlang/listener-loops.md). |

### Prime-Side Operating Setup

A Prime's operating setup is the bundle of three beacon classes deployed together: baseline-relay (config-driven execution), warden-relay (independent verification + halt), and stream-sentinel (latency-bounded reactive responses). They are distinct classes — not a single "sentinel formation."

| Component | Uses Risk Framework For |
|-----------|-------------------------|
| **baseline-{prime}** (relay class) | Risk monitoring during execution, deployment decisions |
| **warden-{prime}-{operator}** (relay class) | Independent risk verification, halt triggers |
| **stream-{prime}-{actor}** (sentinel class, stream variant) | Latency-bounded reactive responses operating the Prime |

### Folio-Side Operating Setup

| Component | Uses Risk Framework For |
|-----------|-------------------------|
| **baseline-{folio}** (relay) | Risk monitoring during execution, deployment decisions (automated folios) |
| **warden-{folio}-{operator}** (relay) | Independent risk verification, halt triggers (automated folios) |
| **principal-{owner}** (sentinel class, principal variant) | Direct control with structural protection only (principal-control folios) |

> **Note:** Automated folios inherit setup-level protection identical to Primes — TTS is defined by the warden set, and ORC is sized accordingly. Principal-control folios have no TTS (no wardens to shut them down) — risk is bounded by rate limits and PAU architecture alone, not by setup-level protections.

### Halo-Side Action Beacons

| Component | Uses Risk Framework For |
|-----------|-------------------------|
| **lcts-{halo}** (relay) | LCTS vault capacity management, redemption processing |
| **nfat-{halo}** (relay) | NFAT Facility operations, claim processing |

These are high-authority action beacons (deterministic keepers), not part of a Prime operating setup. Prime baseline/warden/stream beacons come later and operate Primes; Halo execution remains keeper-driven.

### Halo Reporting Beacons

| Component | Uses Risk Framework For |
|-----------|-------------------------|
| **relay-{halo}** + **attest-data-{class}** | Reporting risk metrics for Halo Units. On-chain reads use the chain-read grounded primitive directly inside synserv-run code; off-chain reports come in as `attest-data` beacon writes. |

### Key Metrics (from Sentinel doc)

| Metric | Definition | Risk Framework Connection |
|--------|------------|---------------------------|
| **CRR** | Capital Ratio Requirement per position | Per-position blended capital from sub-book routing per [`primebook-composition.md`](primebook-composition.md). For matched positions in `termbook`/`structbook`: risk weight only. For positions in `tradingbook`/unmatched: forced-loss envelope (`max(RW, forced-loss-capital)`). For positions in `hedgebook`: residual-risk after hedge per [`hedgebook.md`](hedgebook.md). For positions without matched category: CRR 100% (default-deny). |
| **TRRC** | Total Required Risk Capital | Sum of CRR × position size across portfolio |
| **TRC** | Total Risk Capital actually held | Actual safety capital |
| **Encumbrance Ratio** | TRRC / TRC | Capital utilization — target ≤90% |
| **Per-sub-book CRR** | CRR aggregated by sub-book within a Primebook | New metric; surfaces sub-book-level concentration and matched-portion shifts (see [`risk-monitoring.md`](risk-monitoring.md)) |
| **Equity proximity** | Distance to equity-tranche zero per book per [`book-primitive.md`](book-primitive.md) | Real-time alert when any book's equity approaches zero (unwind trigger) |

---

## PIV / Trading Execution Risk

Sentinel formations that operate Prime Intent Vaults (PIVs) face **trading execution risk** in addition to portfolio risk. Unlike portfolio risk — which is managed through CRR, hold-to-par matching, and risk capital — PIV risk is managed through on-chain enforcement mechanisms:

- **Delegated Intent Policy (DIP):** Per-vault policy defining allowed pairs, max slippage, per-intent notional caps, and per-window velocity limits. Enforced at fill time via a stateful vault hook.
- **Per-window caps:** Hourly and daily notional limits bound trading throughput, capping worst-case losses from a malfunctioning or compromised baseline-relay.
- **EIP-1271 validation:** Settlement contract validates maker authorization against the Prime Intent Vault, ensuring only authorized delegated signers can produce valid intents.
- **Vault balance isolation:** Only the PIV balance is exposed to settlement; the full Prime PAU is not at risk.

PIV trading execution risk is bounded by the vault balance and velocity limits rather than sized through ORC. For the full PIV specification, see `trading/sky-intents.md`. For the ORC/PIV boundary and how operational risk capital relates to formation-level protections, see `risk-framework/operational-risk-capital.md`.

---

## Category Caps (Correlation Framework) Outputs

If category caps are enabled (`correlation-framework.md`), synserv verification should additionally be able to report:

- Per category `c`: `cap_percent[c]`, `cap_amount[c]`, `exposure_total[c]`, `utilization[c]`
- Per Prime `p`, category `c`: `alloc[p][c]`, `E[p][c]`, `P[p][c]` (penalized amount)
- Portfolio-level: total over-cap exposure and resulting 100%-CRR-required capital
