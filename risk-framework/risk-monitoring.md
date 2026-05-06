# Risk Monitoring

**Status:** Draft
**Last Updated:** 2026-02-07

---

## Purpose

Monitoring provides early warning, situational awareness, and accountability. This document defines the metric categories, stress testing approaches, anomaly detection, and escalation procedures that complement the quantitative risk framework.

For which beacons compute which metrics, see `sentinel-integration.md`.
For sentinel formation architecture, see `trading/sentinel-network.md`.

---

## Key Metrics

### Solvency Metrics

**System Collateral Ratio**
```
Total Collateral Value / Total USDS Outstanding
```
Fundamental measure of system health. Must remain well above 100%.

**Collateral Coverage by Tier**
Distribution across quality tiers. Higher Tier 1 concentration = more robust.

**Surplus Buffer**
Accumulated surplus available to absorb losses before affecting USDS holders. The TMF targets Aggregate Backstop Capital at 1.5% of total USDS supply post-Genesis (see [Appendix C](../whitepaper/appendix-c-treasury-management-function.md)). During the Genesis phase, the interim target is $125M.

### Liquidity Metrics

**USDS Liquidity**
Redeemability and tradability across venues.

**Collateral Liquidity**
Depth and spread data for liquidation scenarios.

**Redemption Capacity**
Maximum stress redemption before stability impact.

### Concentration Metrics

**Single Asset Exposure**
Maximum exposure to any single collateral asset. Governed by category caps (`correlation-framework.md`).

**Counterparty Concentration**
Exposure to any single counterparty (custodian, issuer, protocol).

**Correlated Asset Exposure**
Exposure to assets that move together. See `correlation-framework.md`.

### Stress Metrics

**Value at Risk (VaR)**
Loss at various confidence levels.

**Liquidation Cascade Risk**
Probability of liquidations triggering further liquidations.

**Oracle Failure Impact**
Consequences of price feed failure or manipulation.

### Operational Metrics

**Liquidator Activity**
Active, well-capitalized liquidators available.

**Keeper Health**
Operational keepers performing their functions.

**Oracle Freshness**
Price feeds current and accurate.

### Sub-book and Equity Metrics

**Per-sub-book CRR**
CRR aggregated by sub-book within each Primebook (`ascbook`, `tradingbook`, `termbook`, `structbook`, `hedgebook`, unmatched). Surfaces:
- Concentration shifts (e.g., `tradingbook` growing as a fraction of total)
- Matched-portion erosion (e.g., `structbook` matched-portion shrinking due to bucket capacity changes)
- Hedge effectiveness drift (e.g., `hedgebook` residual rising as basis loosens)

See [`primebook-composition.md`](primebook-composition.md) for the sub-book taxonomy.

**Equity proximity**
Distance to equity-tranche zero per book, per [`book-primitive.md`](book-primitive.md). Real-time alerting when any book (Riskbook, Halobook, Primebook, Genbook, Exobook) has equity approaching zero — the unwind trigger. Each book class must have a documented equity-feed mechanism (endoscraper / attestor / synserv computation).

**Treatment-switch frequency**
Rate of sub-book reclassifications per Prime per epoch. Sudden spikes may indicate gaming attempts (especially mid-stress); the crash-oracle (Phase 2+, per [`primebook-composition.md`](primebook-composition.md) §7) suspends switches during declared crash windows.

---

## Monitoring Infrastructure

| Layer | Components |
|-------|-----------|
| **Collection** | On-chain state, oracle data, external market data, sentinel reports |
| **Processing** | Real-time aggregation, historical comparison, anomaly detection, alert generation |
| **Visualization** | Role-specific dashboards, real-time status, historical trends, drill-down |
| **Alerting** | Threshold-based, anomaly-based, escalation triggers |

---

## Stress Testing

### Scenario Analysis

Test against specific scenarios:
- 50% price drop in major collateral
- Liquidity crisis (no buyers)
- Oracle failure or manipulation
- Mass redemption event
- Coordinated attack

### Historical Stress Tests

Apply historical crisis conditions:
- March 2020 COVID crash
- May 2021 crypto crash
- Terra/Luna collapse
- FTX contagion

### Monte Carlo Simulation

- Random price paths with varying correlations
- Tail event modeling
- Distribution of outcomes

### Reverse Stress Testing

Work backwards from failure:
- What conditions cause insolvency?
- How likely are those conditions?
- What is the margin of safety?

---

## Anomaly Detection

Not all risks surface as threshold breaches.

| Type | Examples |
|------|----------|
| **Statistical** | Deviations from historical patterns, unusual distributions, unexpected correlations |
| **Behavioral** | Unusual transaction patterns, new actors behaving anomalously, coordination signatures |
| **Structural** | Changes in market structure, new risk concentrations, emerging dependencies |

---

## Escalation Procedures

### Severity Levels

| Level | Condition | Response |
|-------|-----------|----------|
| Info | Notable but not concerning | Log, track |
| Warning | Approaching thresholds | Increase monitoring, prepare |
| Alert | Threshold breach or anomaly | Active response, notifications |
| Critical | Immediate threat | Emergency procedures |

### Escalation Path

1. Automated detection (synserv verification, warden sentinels)
2. Sentinel formation review
3. Human operator notification (if needed)
4. Governance notification (if needed)
5. Emergency powers (if needed)

---

## Continuous Improvement

### Post-Event Analysis

After every significant event: what happened, what monitoring caught, what it missed, how to improve.

### Metric Evolution

Add new metrics as risks evolve. Retire metrics that aren't useful. Refine thresholds based on experience.

---

## Encumbrance Ratio Enforcement

**[Future — governance proposal required]**

The target encumbrance ratio is ≤90% (TRRC / TRC). Agents exceeding this threshold face restrictions until compliance is restored. The specific penalty schedule requires a governance proposal; likely mechanics include:

- **Rate limit reduction** — automatic scaling of PAU rate limits proportional to overshoot
- **New deployment freeze** — no new positions until ratio returns below threshold
- **Mandatory deleveraging timeline** — escalating timeline to restore compliance (e.g., 7 days for minor breach, 48 hours for severe)
- **Governance notification** — automatic escalation via synserv verification alerts

The enforcement mechanism should be calibrated to avoid pro-cyclical forced selling while maintaining capital discipline.

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| `sentinel-integration.md` | Which beacons compute which risk metrics |
| `capital-formula.md` | Capital requirements that monitoring tracks |
| `correlation-framework.md` | Category caps feeding concentration metrics |
| `operational-risk-capital.md` | ORC and TTS — warden monitoring economics |
| `trading/sentinel-network.md` | Sentinel formation architecture |
