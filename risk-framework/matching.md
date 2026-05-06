# Matching

**Status:** Draft (Phase 3 update, 2026-05-05)

How positions consume duration capacity from `structbook` and `termbook`. Preserves the load-bearing insight from prior versions: **duration matching protects against credit spread risk, not interest rate risk**. Reframed as smooth optimization across sub-book treatment, not binary matched/unmatched flags.

Companion to:
- [`primebook-composition.md`](primebook-composition.md) — `termbook` and `structbook` are the optimization-shaped sub-books that consume matching
- [`duration-model.md`](duration-model.md) — bucket capacity that matching draws from
- [`asset-classification.md`](asset-classification.md) — SPTP split into credit-spread vs rate duration
- [`risk-decomposition.md`](risk-decomposition.md) — coverage matrix; what each sub-book covers

---

## TL;DR

Duration matching is the mechanism by which a position's spread and rate risks become "covered by structure" rather than capital. The architectural placement:

| Sub-book | Covers credit-spread? | Covers rate? | Liability matched against |
|---|---|---|---|
| `termbook` | Yes (held to par) | Yes (matched fixed/fixed) | tUSDS-issued YT (Yield Tokens) |
| `structbook` | Yes (held to par) | No (rate-hedge or v1 carve-out) | Structural USDS demand (Lindy + caps) |
| `tradingbook` | No (forced-loss applies) | No (rate-hedge or capital) | None — held for trading |

The **credit-spread vs rate distinction** is foundational. Credit spreads are mean-reverting; rate shifts can be permanent. Matching protects against the first; the second requires hedging or rate-hedge capital.

Matching itself is **continuous**, not binary. The optimization-shaped sub-books (`structbook`, `termbook`, `hedgebook`) blend matched and unmatched portions smoothly as capacity shifts.

---

## Section map

| § | Topic |
|---|---|
| 1 | Rate risk vs credit spread risk (the foundational distinction) |
| 2 | Duration matching eligibility |
| 3 | Rate hedging requirement |
| 4 | Smooth optimization (matched + unmatched blend) |
| 5 | Termbook vs Structbook |
| 6 | What this means for asset types |

---

## 1. Rate risk vs credit spread risk

Duration matching protects against **credit spread risk**, not **interest rate risk**. This distinction is fundamental.

### Why the distinction matters

| Risk Type | Behavior | SSR Response | Matching Applicability |
|---|---|---|---|
| **Credit spread widening** | Mean-reverting; cyclical | SSR stays flat or falls (flight to quality) | Matching protects — temporary MTM loss, no cash flow mismatch |
| **General rate rise** | Can be permanent (regime shift) | SSR rises | Matching does NOT protect — ongoing cash flow mismatch |

### The mechanism

**Why credit spread risk is manageable with matching:**

1. Credit spread widening causes asset prices to fall temporarily
2. But SSR (Sky Savings Rate) doesn't rise — it tracks general rate levels, not credit spreads
3. During credit stress, USDS often benefits from flight-to-quality
4. The Prime has no cash flow mismatch — it can afford to wait
5. As credit spreads compress (empirically mean-reverting), asset prices recover
6. Matching ensures the Prime has time to wait for recovery

**Why rate risk is NOT manageable with matching:**

1. General rate rise (e.g., Fed hikes) causes SSR to rise permanently
2. If the Prime holds fixed-rate assets, it earns the old lower rate
3. This creates ongoing negative carry: pays SSR + margin, earns old rate
4. This isn't a temporary MTM shock — it's permanent cash flow drag
5. Matching doesn't help because there's no "pull to par" on the rate differential itself
6. The Prime will bleed continuously until the asset matures or rates fall

### Empirical support

**Credit spreads are mean-reverting:**
- Significant evidence of mean reversion, especially for higher-rated spreads
- Credit spread indices are modeled using Ornstein-Uhlenbeck processes (mean-reverting systems)
- 2008 GFC: ~6+ months to recover; COVID-19 2020: ~3 weeks after Fed intervention
- Counter-cyclical: widen during contractions, narrow during expansions

**Interest rates can shift permanently:**
- Monetary policy regime changes are documented (e.g., Volcker era)
- The move from ~15% (1980s) to ~0% (2010s) wasn't mean reversion — it was a multi-decade regime shift
- Recent research challenges the assumption that monetary policy is "neutral" in the long run

---

## 2. Duration matching eligibility

For an asset to be eligible for matched treatment in `termbook` or `structbook`, it must satisfy **both** conditions:

1. **Has stressed pull-to-par** (per [`asset-classification.md`](asset-classification.md) §3) ≤ matched liability tier duration
2. **Is rate-neutral relative to SSR** (only required for `termbook`):
   - Asset is floating-rate (natural hedge), OR
   - Asset is hedged via swap/derivative, OR
   - Prime holds rate-hedging capital for unhedged fixed-rate portion

```
termbook-eligible = (Has SPTP) AND (Rate Neutral OR Rate Hedge Capital Held)
structbook-eligible = (Has SPTP) AND (rate-hedge capital held OR v1 carve-out applies)
```

`structbook` doesn't require rate neutrality (it's matched against variable-rate structural demand), so positions go there with rate-hedge capital separately accounted. V1 carves out the rate-hedge capital requirement for the test (resumed in v2+).

---

## 3. Rate hedging requirement

All Prime fixed-rate exposure must be rate-hedged for `termbook` placement.

### Methods

| Method | Description | When to Use |
|---|---|---|
| **Floating-rate assets** | Asset yield tracks market rates naturally | Preferred for CLOs (most are floating-rate) |
| **Interest rate swaps** | Swap fixed receipts for floating | Convert fixed-rate bonds to floating exposure |
| **Duration matching** | Match asset duration to liability duration (only works for `termbook` with tUSDS YT counterparty) | When tUSDS market exists |
| **Rate hedging capital** | Hold extra capital to cover expected rate loss | When hedging instruments unavailable or costly |

### Rate hedging capital calculation

If a Prime holds unhedged fixed-rate exposure, it must hold capital to cover the expected loss from rate movements:

```
Rate Hedge Capital = Fixed Rate Exposure × Duration × Expected Rate Volatility × Confidence Multiplier
```

**Example:**
- $100M fixed-rate bonds, 3-year duration
- Expected rate volatility: 200bps at 95% confidence
- Rate Hedge Capital = $100M × 3 × 2% × 1.65 = $9.9M

This capital is **in addition to** credit risk capital, not a substitute for it.

---

## 4. Smooth optimization (matched + unmatched blend)

Earlier framing treated matching as **binary**: a position was either matched (risk weight only) or unmatched (forced-loss treatment). The new framework treats it as **continuous**.

The optimization-shaped sub-books (per [`primebook-composition.md`](primebook-composition.md) §4) blend matched and unmatched portions smoothly:

```
structbook position CRR = matched_portion × RW
                        + unmatched_portion × max(RW, forced-loss-capital)
```

When duration capacity shrinks (e.g., bucket capacity allocated elsewhere, Lindy shifts, redemptions surge):
- `matched_portion` shrinks
- `unmatched_portion` grows
- Blended CRR rises smoothly

No binary "transition" event. Capital requirement updates continuously. This dissolves the old "treatment-coverage-failure" problem (binary coverage flips that were predicated on hard match/unmatch boundaries).

### Cumulative capacity matching

An asset can match against its required bucket AND all higher buckets (per [`duration-model.md`](duration-model.md)).

**Example:**
- Hold $500M JAAA (SPTP = 1,260 days, requires bucket 84)
- Cumulative duration capacity at bucket 84+: $300M

| Portion | Amount | Treatment | CRR | Capital |
|---|---|---|---|---|
| Matched | $300M | structbook (risk weight) | 5% | $15M |
| Unmatched | $200M | unmatched / tradingbook (forced-loss) | 10% | $20M |
| **Total** | $500M | — | — | **$35M** |

As duration capacity grows (longer-duration liabilities accumulate or redemption pressure eases), more of each position can be matched, reducing overall capital requirements. Natural incentive alignment — sticky liabilities enable more efficient capital deployment.

---

## 5. Termbook vs Structbook

The two matched sub-books differ in what they're matched against and what they cover:

### `termbook` — tUSDS-matched

- Matched against tUSDS-issued YT (Yield Tokens), with the Prime holding the YT side
- Matched fixed/fixed → covers credit-spread MTM AND rate
- Held to par → covers liquidity (no forced sale)
- Default capital still required

**Note:** tUSDS / YT split market is a Phase 2+ feature — fixed-rate USDS holders on one side, variable-rate (YT) on the other. The market doesn't exist yet; the v1 risk framework has the schema and category but `termbook` is empty in practice.

### `structbook` — structural-demand matched

- Matched against structural USDS demand (per [`duration-model.md`](duration-model.md))
- Variable-rate liability → does NOT cover rate risk
- Held to par → covers liquidity and credit-spread MTM
- Default capital still required
- Rate-hedge capital required for fixed-rate positions (carved out for v1)

`structbook` is the active sub-book for v1's crypto-collateralized lending test. `termbook`, `tradingbook`, `ascbook`, `hedgebook` have schema slots but hold nothing in v1.

---

## 6. What this means for asset types

| Asset | Rate Exposure | Typical Handling | Matching Eligibility |
|---|---|---|---|
| **JAAA (CLO AAA)** | Floating-rate (SOFR + spread) | Natural hedge | Eligible for both `termbook` and `structbook` |
| **Fixed-rate corporate bonds** | Fixed-rate | Must swap to floating or hold rate capital | Conditional |
| **T-bills (short duration)** | Fixed but short | Minimal rate risk due to short duration | Eligible (small rate-hedge capital) |
| **Long-duration treasuries** | Fixed, long duration | Must hedge or hold significant rate capital | Conditional |
| **Sparklend** | Floating-rate (typically) | N/A — no SPTP regardless | Not eligible (no SPTP); routes to `tradingbook` if liquid, otherwise unmatched |
| **NFAT (crypto-collateralized)** | Fixed-term | V1 carve-out — no rate-hedge capital required for matched portion | Eligible for `structbook` |

### The value proposition of duration matching

With rate risk properly hedged, duration matching allows Primes to:
- **Avoid hedging credit spread risk** on long-duration variable-rate assets
- **Take credit spread exposure** for yield while managing capital efficiently
- **Wait out temporary credit dislocations** without forced sales

This is the core value: matching lets Primes capture credit spread (compensated, mean-reverting) while requiring them to hedge rate risk (potentially permanent, catastrophic if unhedged).

---

## File map

| Doc | Relationship |
|---|---|
| [`primebook-composition.md`](primebook-composition.md) | `termbook` and `structbook` are the matched sub-books |
| [`duration-model.md`](duration-model.md) | Bucket capacity feeds matching |
| [`asset-classification.md`](asset-classification.md) | SPTP split into credit-spread vs rate duration |
| [`risk-decomposition.md`](risk-decomposition.md) | Coverage matrix shows what each sub-book covers |
| [`hedgebook.md`](hedgebook.md) | Rate-hedging at portfolio level (alternative to per-position rate-hedge capital) |
| [`capital-formula.md`](capital-formula.md) | Per-position capital integrates matched + unmatched blend |
| [`asset-type-treatment.md`](asset-type-treatment.md) | Asset-class-specific matching applicability |
