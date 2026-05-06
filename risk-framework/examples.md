# Examples

**Status:** Draft (Phase 3 update, 2026-05-05)

Worked end-to-end example of the new framework: the v1 crypto-collateralized lending test. Three near-identical Halos, three Star Primes, one Generator, one active sub-book (`structbook`). Demonstrates how the substrate primitives compose into a complete capital computation.

Companion to:
- [`risk-decomposition.md`](risk-decomposition.md), [`book-primitive.md`](book-primitive.md), [`tranching.md`](tranching.md), [`currency-frame.md`](currency-frame.md) — substrate primitives in use
- [`riskbook-layer.md`](riskbook-layer.md), [`primebook-composition.md`](primebook-composition.md) — layer architecture
- [`asset-type-treatment.md`](asset-type-treatment.md) — per-class treatment behind the math here
- [`capital-formula.md`](capital-formula.md) — the per-position computation flow this example exercises

---

## V1 test scenario: crypto-collateralized lending

### Setup

- **Three near-identical Halos** doing institutional borrowers custodial crypto-collateralized stablecoin lending
- **NFATs** (fixed-term Halo units) per loan
- **Three Star Primes** (Spark, Grove, Keel), each running one of the three Halos
- **USDS Generator** (USGE) with Genbook + structural-demand registry
- **Equal split** of structural demand among the 3 Stars (1/3 each per bucket)
- **Active sub-book**: `structbook` only — `ascbook`/`tradingbook`/`termbook`/`hedgebook` exist as schema placeholders but hold nothing in v1

### Position structure (each NFAT loan)

Each NFAT loan position is structurally a **senior tranche of a per-loan exobook**:

```
exo-book (per-loan):
   asset side:   BTC/ETH/stETH collateral (custodial)
   liability side (tranched):
      junior:    borrower equity (~20-40% of asset value)        [exoliab]
      senior:    loan principal (USDC/USDT-denominated)          [endo, held by Halo]
   rules:
      continuous: compute health factor from oracle prices
      if health < threshold: trigger liquidation
      at maturity: borrower repays in cash, recovers collateral
   state: current collateral value, current health factor
   frame: USD (inherited from USDS Generator)
```

The Halo's Riskbook holds the senior tranche as an exo unit, paired with the per-loan Riskbook category match.

### V1 carve-outs (deliberate simplifications)

1. Manual governance-set capacity initially (Lindy + structural caps from existing parameters)
2. Equal-split distribution (no auctions, no tug-of-war)
3. No rate-hedge capital for matched positions (carve-out from `matching.md`)
4. TTM range 0-12 months only
5. SPTP = remaining nominal term (no stress modifier)
6. One Genbook (USDS) only
7. Three Halos under three Star Primes (one Halo per Prime)
8. Super-senior tranches only (mezzanine/equity-tranche holdings get CRR 100% by default-deny)
9. Phase 1 manual structural demand allocations
10. Halobook category as passthrough (`nfat-crypto-lending-fixed-term`)
11. Active sub-books: only `structbook`
12. Tranche rights schema present but not exercised
13. JAAA / CLO modeling deferred (recursive complexity)

Each carve-out has a clear later-phase replacement.

---

## Walking through one position

A 6-month NFAT loan: Spark Halo lends $750K USDC against 1 BTC of collateral.

### Step 1: Per-loan exobook setup

```
exo-book spark-loan-001
   asset: btc 1                                      ; collateral
   tranches:
      seniority 0: borrower equity, $250K usd        ; ~25% cushion
      seniority 1: spark senior, $750K usdc          ; loan principal
   rules:
      health-factor-trigger (liquidate at HF < 1.05)
      maturity 180 days
   state:
      btc-value-usd $80000
      current-hf 1.07
   frame: usd
```

### Step 2: Riskbook category match

Spark Halo's Riskbook (`&entity-halo-spark-crypto-lending-riskbook-A`) holds the senior tranche of `spark-loan-001`. The Riskbook matches `crypto-collateralized-USD-lending` (per [`asset-type-treatment.md`](asset-type-treatment.md) §NFAT).

### Step 3: Asset stress projection

Under the `severe-correlated-crash` scenario (from `&core-framework-stress-scenarios`):
- BTC drops 45% → asset value falls from $80K to $44K
- USDC depeg stress: ~5% → Spark's claim is worth 95% of nominal
- Junior cushion: $250K (intact at peak; reduces under stress)

Loss math:
- Asset value post-stress: $44K
- Junior cushion (in stressed BTC value): $44K × ($250K / $80K) = ~$13.75K
- Effective senior loss = max(0, asset_drop − junior_cushion) = max(0, $36K − $13.75K) = $22.25K
- USDC depeg loss on $750K notional: $750K × 0.05 = $37.5K
- Total stress loss: $59.75K
- Loss fraction: $59.75K / $750K ≈ 7.97%

### Step 4: Halobook P/T declarations

Halobook category `nfat-crypto-lending-fixed-term` declares:
- P (permitted unwind): only at maturity OR on health-factor breach
- T (transfer market): not transferable

### Step 5: Sub-book routing

Eligibility check:
- `ascbook`: NO (not deep peg-defense liquid)
- `tradingbook`: NO (P AND T both restrictive — no exit path)
- `termbook`: NO (no tUSDS-matched liability)
- `structbook`: YES (has SPTP = 180 days, structural-demand capacity available)
- `hedgebook`: NO (no hedge instruments in v1 test)

→ Routes to `structbook`.

### Step 6: structbook capital math

Assume Spark has been allocated $200M of bucket 12 (180 days) capacity by the equal-split distribution.

For this single loan:
- Position size: $750K
- Available capacity at bucket 12: $200M minus already-matched
- Assume $190M already matched, so $10M capacity remaining
- Matched portion: min($750K, $10M) = $750K (fully matched)
- Unmatched portion: $0

`structbook` capital:
- Matched: $750K × RW (default + counterparty) ≈ $750K × 5% = $37.5K
- Rate-hedge capital: 0 (v1 carve-out)
- Unmatched: $0
- **Position capital: ~$37.5K** (default risk only; structural matching covers credit-spread and liquidity)

If capacity were exhausted before this loan landed:
- Matched portion: $0 (capacity full)
- Unmatched portion: $750K
- Unmatched capital: $750K × max(RW, Forced-Loss) ≈ $750K × max(5%, 7.97%) = $750K × 7.97% = $59.8K
- **Position capital: ~$59.8K**

The smooth blend (per [`matching.md`](matching.md) §4) means capital scales continuously with capacity utilization — no binary cliff.

### Step 7: Concentration check

If Spark's total ETH-backed lending exposure (across all loans, USDC and USDT denominated) exceeds the governance-set Genbook cap on "ETH-collateralized lending" category, the excess gets 100% CRR. V1 manual caps; the math is the same.

---

## Scaling up: full-Prime computation

For Spark's entire crypto-lending book (say, 1000 loans summing to $500M):

```
Total Position Capital = Σ_loan (Matched × RW + Unmatched × Forced-Loss)
Concentration Excess   = applicable category penalties
Total ASC + ORC         = parallel tracks (not in TRRC, but additive operational obligations)

Spark TRRC = Total Position Capital + Concentration Excess
```

Each Prime computes its own TRRC; the Genbook aggregates across all Primes for system-wide concentration enforcement.

### Encumbrance ratio

```
ER = TRRC / TRC
```

Where TRC is Total Risk Capital (JRC + EJRC + SRC). Target: ER ≤ 0.90. Breach drives penalties at settlement.

---

## Summary of principles

1. **Liability duration determines duration capacity.** The Lindy Duration Model measures how much of the liability base is short-term vs long-term.

2. **Use Stressed Pull-to-Par (SPTP) for asset duration.** Stress modifier reflects historical worst-case prepayment/amortization slowdowns.

3. **Duration matching protects against credit spread risk, not rate risk.** Credit spreads are mean-reverting; rate shifts can be permanent. Matching covers the first; the second requires hedging.

4. **All fixed-rate exposure must be rate-hedged** (or hold rate-hedge capital) for matched treatment.

5. **SPTP determines duration matching eligibility.** Only assets with SPTP ≤ liability tier duration AND rate-neutral exposure can be duration-matched.

6. **Matched positions get risk-weight treatment.** Capital only for fundamental risk.

7. **Unmatched positions get forced-loss treatment.** Capital for `max(RW, forced-loss-capital)`.

8. **Crypto lending is structurally tranched.** The senior tranche's risk = asset stress through junior cushion. Gap risk has unified into the standard tranche math.

9. **Concentration limits prevent diversification illusions.** Capital must survive each stress scenario applied to its correlated asset group.

10. **Default-deny is the discipline.** Anything the framework can't model adequately gets CRR 100%.

11. **Sub-book composition is continuous, not binary.** The optimization-shaped sub-books blend matched and unmatched portions smoothly as capacity shifts.

12. **Currency frame ≠ instrument.** Frame is the unit of account (USD); instruments (USDC, USDT, ETH) translate to the frame with declared stress.

13. **Real-time equity recomputation is the operational invariant.** Every book's equity must be computable continuously; this drives endoscraper / attestor / synserv-computation infrastructure requirements.

---

## File map

| Doc | Relationship |
|---|---|
| [`risk-decomposition.md`](risk-decomposition.md), [`book-primitive.md`](book-primitive.md), [`tranching.md`](tranching.md), [`currency-frame.md`](currency-frame.md) | Substrate primitives in use |
| [`riskbook-layer.md`](riskbook-layer.md), [`halobook-layer.md`](halobook-layer.md), [`primebook-composition.md`](primebook-composition.md) | Layer architecture exercised here |
| [`asset-classification.md`](asset-classification.md), [`asset-type-treatment.md`](asset-type-treatment.md) | Per-asset data and treatment behind the math |
| [`matching.md`](matching.md) | Smooth optimization between matched / unmatched portions |
| [`duration-model.md`](duration-model.md) | Bucket capacity that the matched portion consumes |
| [`capital-formula.md`](capital-formula.md) | Per-position capital flow exercised in §"Walking through one position" |
| [`correlation-framework.md`](correlation-framework.md) | Concentration limits that gate scaling up |
| [`asc.md`](asc.md), [`operational-risk-capital.md`](operational-risk-capital.md) | Parallel-track operational obligations not in TRRC |
| [`open-questions.md`](open-questions.md) | Open items including v1 stress calibration, attestor schema, privacy buckets |
