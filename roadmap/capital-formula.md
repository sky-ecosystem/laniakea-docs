# Capital Formula — P1 Lean

Lean P1 view of [`../risk-framework/capital-formula.md`](../risk-framework/capital-formula.md). Canonical full body there; this file carries only what P1 binds to.

P1 has one active sub-book (`structbook`); deferred sub-book formulas (ascbook, tradingbook, termbook, hedgebook, unmatched-leftover) live in the canonical.

## 1. Per-position computation flow

```
Step 1: Riskbook risk-form match
  → If matched: equation produces per-position CRR components
  → If no match: CRR = 100% (default-deny)

Step 2: Project asset stress through structure
  → Tranched-exobook: waterfall propagation (see custodial-crypto-risk-form.md §3)

Step 3: Halobook exposure structure adjustment
  → Apply rollover, lockup, embedded-option effects → U/P/T declarations

Step 4: Sub-book routing
  → P1: always structbook (others are deferred schema slots)

Step 5: Sub-book capital math (see §2 below)

Step 6: Concentration excess (computed, deferred enforcement in P1)
  → 100% CRR on over-cap portion when activated

Step 7: Position capital = sum × position size
```

## 2. `structbook` formula (the only P1-active sub-book)

```
Matched Portion   = min(Position Size, Available Structural-Demand Capacity)
Unmatched Portion = Position Size - Matched Portion

Position Capital = Matched   × default-CRR
                 + Unmatched × max(default-CRR, Forced-Loss Capital)
                 + Unmatched × rate-CRR
```

Spread / rate / liquidity covered on the SDR-matched portion in P1 (risk form still calculates them; they become non-binding only to the extent matched). **default-CRR is always required.**

See [`matching.md`](matching.md) §3 for the cumulative capacity matching that determines available capacity.

## 3. Concentration excess (P1: computed, not enforced)

Mechanism deferred to Phase 3+. When activated:

```
excess[p][c] = max(0, exposure[p][c] - cap_allocation[p][c])
Excess Capital[p][c] = excess[p][c] × 1.0   ; 100% CRR
```

No-stacking rule: max binding category penalty, not the sum.

## 4. TRRC aggregation

```
insynTRRC[p] = Σ Position Capital[position] + Σ Excess Capital (deferred in P1)
TRRC[p]      = insynTRRC[p] + exsynTRRC[p]    ; exsyn from patch-{prime} writing into primebook
ER[p]        = TRRC[p] / TRC[p]               ; target ≤ 0.90
```

`TRC[p]` = Total Risk Capital held (JRC + EJRC + SRC tiers; tier mechanics deferred-out-of-P1 in the canonical, but the TRC scalar is sudo-set in `&entity.prime.{id}.root` for P1).

P1 ER emission cadence: per heartbeat, via `(prime-er $prime $value $T)` written by synserv into the primebook.
