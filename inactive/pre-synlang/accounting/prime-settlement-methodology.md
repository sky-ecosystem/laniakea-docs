# Prime Settlement Methodology (Current)

**Status:** Draft
**Last Updated:** 2026-02-12

---

## Overview

This document describes the current methodology for calculating what each Prime owes (or is owed) at each settlement cycle. The settlement reconciles a Prime's borrowing costs against credits earned from holding assets productively across the ecosystem.

The core question settlement answers: **After accounting for interest owed, idle asset credits, savings spread profits, and Sky Direct performance — what does each Prime actually owe?**

Currently this calculation is performed manually on a monthly basis (see `current-accounting.md` for settlement cycle timing). The long-term target is automated daily settlement (Phase 3+).

---

## The Five-Step Calculation

### Step 1: Calculate Maximum Debt Fees

The starting point is the maximum interest a Prime would owe if there were no reimbursements.

```
Maximum Debt Fees = Average Ilk Debt × Monthly Rate

Where:
- Average Ilk Debt = time-weighted average of the Prime's outstanding borrowed amount over the measurement period
- Rate = Annual Base Rate ÷ 12 (monthly) or ÷ 365 (daily)
```

Time-weighting accounts for debt fluctuations during the period. If a Prime's debt was $10M for half the month and $15M for the other half, the average is $12.5M — not $15M.

**Example (monthly settlement — current):**

```
Prime's ilk debt over a monthly measurement period:
- Days 0–15: $10M debt
- Days 15–25: $15M debt (increased)
- Days 25–30: $12M debt (decreased)

Average Ilk Debt = ($10M × 15 + $15M × 10 + $12M × 5) ÷ 30 = $12M

Base Rate: 5% APR
Monthly Rate = 5% ÷ 12 = 0.4167%

Maximum Debt Fees = $12M × 0.4167% = $50,000
```

This is the maximum the Prime would pay if there were no reimbursements.

---

### Step 2: Calculate Reimbursements for Idle USDS/DAI

Primes hold idle USDS/DAI across multiple locations in the ecosystem. These idle assets earn the Base Rate, and the Prime receives reimbursement.

```
Idle USDS/DAI Reimbursement = Average Idle Balance × Rate (same as Step 1)
```

**Idle asset locations:**

- USDS in PSM3 (Peg Stability Module 3)
- USDS in ALM Proxy (Asset Liability Management Proxy)
- Idle USDS/DAI in lending protocols (Aave, SparkLend, Compound, etc.)
- Idle USDS/DAI in AMM pools (Curve, Uniswap, Balancer, etc.)

**Example:**

```
Time-weighted average idle balances:
- USDS in PSM3:         $2.0M
- USDS in ALM Proxy:    $1.5M
- USDS in Aave:         $3.0M
- USDS in Curve pools:  $0.5M

Total Average Idle USDS/DAI = $7.0M

Base Rate: 5% APR → Monthly Rate: 0.4167%

Idle USDS/DAI Reimbursement = $7.0M × 0.4167% = $29,167
```

---

### Step 3: Calculate Profits for Idle sUSDS

Primes also hold sUSDS (savings USDS) across similar locations. sUSDS earns the Savings Rate, which is the Base Rate plus a spread (currently 0.3% above the Base Rate).

Since the Base Rate portion is already accounted for in Step 1 (the Prime has already "paid for" that portion via debt fees), the Prime's profit here is **only the spread**.

```
sUSDS Profit = Average Idle sUSDS Balance × Spread Rate

Where:
- Spread Rate = Savings Rate - Base Rate (currently 0.3% APR)
```

**Idle sUSDS locations** (same as USDS locations):

- sUSDS in PSM3
- sUSDS in ALM Proxy
- sUSDS in lending protocols (Aave, SparkLend, Compound, etc.)
- sUSDS in AMM pools (Curve, Uniswap, Balancer, etc.)

**Example:**

```
Time-weighted average idle sUSDS balances:
- sUSDS in PSM3:       $5.0M
- sUSDS in ALM Proxy:  $2.0M
- sUSDS in SparkLend:  $4.0M
- sUSDS in Curve pools: $1.0M

Total Average Idle sUSDS = $12.0M

Spread: 0.3% APR → Monthly Rate: 0.3% ÷ 12 = 0.025%

sUSDS Profit = $12.0M × 0.025% = $3,000
```

---

### Step 4: Handle Sky Direct Exposure Reimbursements

Sky Direct allocations are specific capital deployments mandated by governance. For each allocation, the settlement compares actual performance against the Base Rate.

```
Sky Direct Reimbursement = MAX(0, Base Rate Profit − Actual Profit)
```

**Rules:**

| Allocation Performance | Result |
|------------------------|--------|
| Actual Profit < Base Rate Profit | Prime receives reimbursement for the shortfall |
| Actual Profit ≥ Base Rate Profit | No reimbursement; Sky gets all profits |

This provides **underperformance protection** for Primes: if a Sky Direct allocation earns less than the Base Rate, the Prime is made whole. If it earns more, Sky captures all the profits (including excess above Base Rate) as compensation for providing capital and taking allocation risk.

**Example:**

```
Sky Direct Allocation #1 (underperforming):
- Exposure: $8M average balance
- Actual yield: 3% APR
- Base Rate: 5% APR

Base Rate Profit = $8M × 0.4167% = $33,333
Actual Profit    = $8M × 0.25%   = $20,000

Reimbursement = $33,333 − $20,000 = $13,333


Sky Direct Allocation #2 (outperforming):
- Exposure: $5M average balance
- Actual yield: 7% APR
- Base Rate: 5% APR

Base Rate Profit = $5M × 0.4167% = $20,833
Actual Profit    = $5M × 0.5833% = $29,167

Reimbursement = MAX(0, $20,833 − $29,167) = $0
Sky gets all $29,167.


Total Sky Direct Reimbursements = $13,333 + $0 = $13,333
```

---

### Step 5: Compute Net Amount

```
Net Amount = Maximum Debt Fees − Total Reimbursements

Where:
Total Reimbursements = Idle USDS/DAI Reimbursement + sUSDS Profit + Sky Direct Reimbursements
```

**Interpretation:**

| Net Amount | Meaning |
|------------|---------|
| Positive | Prime owes this amount; increases debt on the Prime's ilk |
| Negative | Prime has net profit; decreases debt on the Prime's ilk |

**Complete example:**

| Step | Component | Amount |
|------|-----------|--------|
| 1 | Maximum Debt Fees | $50,000 |
| 2 | Idle USDS/DAI Reimbursement | −$29,167 |
| 3 | sUSDS Profit | −$3,000 |
| 4 | Sky Direct Reimbursements | −$13,333 |
| | **Total Reimbursements** | **$45,500** |
| 5 | **Net Amount** | **$4,500** |

Result: The Prime owes $4,500 for the period. This amount increases the Prime's ilk debt.

---

## Key Properties

**Time-weighted averages** — All balance calculations use time-weighted averages over the measurement period, accounting for positions that change during the period.

**Base Rate netting** — The system avoids double-counting by having the Prime pay the full Base Rate on debt (Step 1), then crediting back the Base Rate earned on idle assets (Step 2). sUSDS profit (Step 3) only captures the spread above Base Rate.

**Underperformance protection** — Sky Direct reimbursements ensure Primes are never worse off for accepting governance-mandated allocations. This makes Primes willing to take on Sky Direct exposure without fear of opportunity cost.

**Asymmetric Sky Direct returns** — Sky captures all upside from outperforming allocations (including the portion above Base Rate), while Primes are protected from downside. This compensates Sky for the risk of making allocation decisions.

---

## Transition Path

| Roadmap Phase | Settlement | Change |
|---------------|-----------|--------|
| Phase 1 (current) | Monthly, manual | Slow, processed toward end of following month |
| Phase 2 | Monthly, formalized | Beacon-monitored calculation with GovOps-coordinated execution; settles faster (early in following month) |
| Phase 3 | Daily, automated | Settlement each day at 4pm UTC; expenses flow continuously |
| Phase 9+ | Daily, beacon-operated | Full `stl-base` automation with auction-based allocation |

The five-step methodology remains the same regardless of settlement frequency — only the measurement period and automation level change.

---

## Connections

- Books and units (the accounting primitives settlement updates): `books-and-units.md`
- Settlement cycle and timing: `current-accounting.md`
- Future daily settlement cycle: `daily-settlement-cycle.md`
- TMF waterfall (what happens with protocol-level profit): `../whitepaper/appendix-c-treasury-management-function.md`
- Risk Framework capital requirements: `../risk-framework/README.md`
