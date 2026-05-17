# Matching — P1 Lean

Lean P1 view of [`../risk-framework/matching.md`](../risk-framework/matching.md). Canonical full body there; this file carries only what P1 binds to.

How positions consume SDR capacity. P1's only active matched sub-book is `structbook`; `termbook` / `tradingbook` / `ascbook` / `hedgebook` have schema slots but are inactive.

## TL;DR

Hold-to-par matching makes a position's spread and rate risks "covered by structure" rather than capital — the Prime holds to maturity against structural demand, avoiding forced-sale losses.

- **Credit spread risk** is mean-reverting → matching protects (Prime can wait it out).
- **Rate risk** can be permanent (regime shift) → matching alone doesn't protect; the SDR mechanism is what makes rate-CRR non-binding for matched portions.

Matching is **continuous, not binary**. Smooth blend as capacity utilization shifts.

## 1. Credit-spread vs rate distinction

| Risk | Behavior | Why matching works (or doesn't) |
|---|---|---|
| **Credit spread widening** | Mean-reverting, cyclical | Temporary MTM; SSR doesn't rise with spreads; Prime can wait for recovery |
| **General rate rise** | Can be permanent (regime shift) | Ongoing cash flow mismatch; matching alone doesn't help — needs floating-rate, swap, rate-CRR capital, or SDR coverage |

Empirical anchor: credit spreads modeled as Ornstein-Uhlenbeck (mean-reverting); 2008 GFC recovered in ~6 months, COVID-19 2020 in ~3 weeks. Rate regime shifts (Volcker-era 15% → 2010s 0%) are decades-long, not mean-reversion.

## 2. Eligibility (P1)

```
structbook-eligible = (Has SPTP ≤ liability bucket tenor) AND (SDR allocation available)
```

The risk form always outputs rate-CRR. `structbook` doesn't delete it; for SDR-matched portions in P1 it becomes non-binding. Unmatched portions still carry rate-CRR.

## 3. Smooth blend (the P1-binding formula)

The structbook position CRR is continuous:

```text
structbook position CRR
  = matched_portion   × default-CRR
  + unmatched_portion × max(default-CRR, forced-loss-capital)
  + unmatched_portion × rate-CRR
```

When SDR capacity shrinks (other Primes' allocations, redemption pressure):
- `matched_portion` shrinks; `unmatched_portion` grows
- Blended CRR rises smoothly — no binary cliff, no transition event

### Cumulative capacity matching

An asset can match against its required bucket AND all higher buckets.

**Worked example** — hold $500M asset with SPTP requiring bucket 42 (1,260 days); cumulative capacity at bucket 42+: $300M:

| Portion | Amount | Treatment | CRR | Capital |
|---|---|---|---|---|
| Matched | $300M | structbook (default only) | 5% | $15M |
| Unmatched | $200M | forced-loss | 10% | $20M |
| **Total** | $500M | — | — | **$35M** |

As structural-demand stickiness grows, more of each position matches → lower capital. Natural incentive alignment.

## 4. P1 SDR allocation source

Total SDR capacity is produced in `&entity.generator.usge.structural-demand`: lot-age surface → Lindy SDR bucket capacity → SDR policy overlay → effective SDR bucket capacity. `structbook` does not read those total-capacity atoms directly.

`structbook` reads current-epoch Prime SDR allocation atoms from `&entity.generator.usge.sdr-auction`:

```metta
(sdr-allocation $prime $bucket $amount $epoch)
```

Atom shape is the stable contract. P1's ownership-weighted temporary SDR auction and future real-auction/tug systems write the same shape; `structbook` matching logic doesn't depend on allocation provenance. No P1 carry-forward or durable reservation rights.

## 5. termbook vs structbook (concept reference)

- **`termbook`** — matched against tUSDS-issued YT (Yield Tokens). Covers credit-spread AND rate (fixed/fixed match), AND liquidity (held to par). Default capital still required. **Phase 2+; tUSDS market doesn't exist yet in P1.**
- **`structbook`** — matched against structural USDS demand. SDR match in P1 covers rate, liquidity, credit-spread MTM for the matched portion. Default capital still required. **Active P1 sub-book.**
