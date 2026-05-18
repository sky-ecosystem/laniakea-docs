# Treasury Management Function (TMF)

**Status:** Live (Genesis phase parameters); transitions to post-Genesis parameters as the Aggregate Backstop Capital target is hit and the Genesis Phase ends
**Last Updated:** 2026-05-08

---

## TL;DR

The TMF is a **5-step sequential waterfall** that distributes all protocol net revenue (Revenue − Expenses, denominated in USDS). Each step calculates its allocation based on the **Step Result** — what remains after the previous step — ensuring all priorities are funded in order before surplus flows to staking rewards.

```
Net Revenue
   ↓
Step 1 — Security & Maintenance        21% Genesis / 4-10% post-Genesis
   ↓
Step 2 — Aggregate Backstop Capital    Variable (target: 1.5% of USDS supply)
   ↓
Step 3 — Fortification Conserver       20% × Net Revenue Ratio
   ↓
Step 4 — Smart Burn Engine             20% × Net Revenue Ratio
   ↓
Step 5 — Staking Rewards               100% of remainder (SKY stakers)
```

The **Net Revenue Ratio (NRR)** is a hyperbolic scaling factor that grows with revenue, causing Steps 3 and 4 to take a larger share at scale and leaving more for staking when revenue is small.

---

## Section map

| § | Topic |
|---|---|
| 1 | Net Revenue Ratio |
| 2 | Step 1 — Security & Maintenance |
| 3 | Step 2 — Aggregate Backstop Capital |
| 4 | Step 3 — Fortification Conserver |
| 5 | Step 4 — Smart Burn Engine |
| 6 | Step 5 — Staking Rewards |
| 7 | Worked examples |
| 8 | Phase 1 vs target behavior |

---

## 1. Net Revenue Ratio

The NRR scales Steps 3 and 4 so that at low revenue most surplus flows to staking rewards, while at higher revenue more flows to fortification and burn.

```
TARGET_CONSTANT = 3 Billion USDS
CAP_THRESHOLD   = 1 Trillion USDS

if current_yearly_net_revenue < CAP_THRESHOLD:
    nrr = current_yearly_net_revenue / (current_yearly_net_revenue + TARGET_CONSTANT)
else:
    nrr = 1.0
```

| Yearly Net Revenue | NRR |
|---|---|
| 200M | 0.0625 |
| 500M | 0.143 |
| 1B | 0.25 |
| 2B | 0.40 |
| 3B | 0.50 |
| 5B | 0.625 |
| 10B | 0.77 |
| 20B | 0.87 |
| 100B | 0.97 |
| 1T+ | 1.0 |

The hyperbolic curve prevents quadratic drag on staking rewards as revenue grows; it smoothly approaches 0.997 at 1T then snaps to 1.0.

---

## 2. Step 1 — Security & Maintenance

Funds core teams responsible for governance security, protocol security, risk management, and ongoing maintenance and development of critical infrastructure.

| Phase | Allocation |
|---|---|
| Genesis Phase | 21% of Total Net Revenue |
| Post-Genesis | 4–10% (governance-determined within the cap) |

```
step_1_allocation = net_revenue × security_rate
step_1_result     = net_revenue − step_1_allocation
```

The 10% upper limit is **permanent and cannot be increased** post-Genesis — a hard structural commitment to long-term cost control. (Genesis → post-Genesis transition timeline is out-of-band during transition; not currently documented in the corpus.)

---

## 3. Step 2 — Aggregate Backstop Capital

Builds the protocol's solvency buffer (denominated in USDS) to protect against bad debt or insolvency events.

**Target:** 1.5% of total USDS supply (the long-term post-Genesis target). **Phase 1 floor:** $125M. See [`capital-stack.md`](capital-stack.md) §8 for ABC's role in the insolvency-defense hierarchy and how Aggregate Backstop Capital relates to Allocated Genesis Capital.

### Three-phase allocation

```
fill_factor      = 1.0 − (current_buffer_size / target_buffer_size)
effective_ratio  = max(nrr, 0.10)
step_2_rate      = fill_factor × 0.50 × effective_ratio
```

| Phase | Condition | Allocation |
|---|---|---|
| **Phase 1: Safety Floor & Turbo Fill** | Buffer < $125M | `max(0.25, step_2_rate) × step_1_result` |
| **Phase 2: Filling** | $125M ≤ Buffer < target | `step_2_rate × step_1_result` |
| **Phase 3: Hard Cap** | Buffer ≥ target | 0% |

**Phase 1** ensures aggressive buffer building when reserves are critically low; the 25% floor applies regardless of the calculated rate.

**Phase 2** uses the dynamic rate, filling faster when emptier and slowing as the buffer approaches target.

**Phase 3** stops all allocation once the buffer reaches target, allowing full flow-through to subsequent steps.

```
step_2_result = step_1_result − step_2_allocation
```

---

## 4. Step 3 — Fortification Conserver

Funds the Fortification Conserver (currently the Fortification Foundation) — an Alignment Conserver responsible for legal defense, resilience infrastructure, unquantifiable risk management, and triggering SKY emissions backstop in case of insolvency (the SKY emissions trigger is currently disabled; future upgrade).

```
step_3_allocation = (0.20 × nrr) × step_2_result
step_3_result     = step_2_result − step_3_allocation
```

Allocation grows with NRR because at small scale Sky depends on established legal infrastructure built by larger entities; as Sky grows, it increasingly cannot rely on external protection mechanisms, making the Fortification Conserver more critical.

| NRR | Effective Rate (of Step 2 Result) |
|---|---|
| 0.0625 | 1.25% |
| 0.25 | 5% |
| 0.40 | 8% |
| 0.625 | 12.5% |
| 0.87 | 17.4% |
| 1.0 | 20% |

---

## 5. Step 4 — Smart Burn Engine

Captures value for token holders by buying SKY from the market. Purchased SKY is distributed to stakers as additional yield.

```
step_4_allocation = (0.20 × nrr) × step_3_result
step_4_result     = step_3_result − step_4_allocation
```

Same NRR scaling as Step 3.

### Current vs target behavior

**Current (temporary):** Steps 4 and 5 are unified — all funds from both steps execute fixed-amount SKY buybacks (~$300K/day) and distribute purchased SKY to stakers as yield.

**Target (post SBE BEAM deployment):** Step 4 implements the dynamic burn rate formula:

```
Burn Rate = (1 − MC / TMC) × 50%
```

Where MC is current market capitalization and TMC is a target derived from growth rate and annual profits. Buys more when undervalued, retains capital when overvalued.

The transition activates once the SBE BEAM ships (Phase 2+). (Current fixed-buyback configuration is out-of-band during transition; not currently documented in the corpus.)

---

## 6. Step 5 — Staking Rewards

All remaining USDS after Steps 1–4 flows to staking rewards. This is the primary destination for surplus during the Genesis Phase when NRR is low.

```
step_5_allocation = step_4_result   # 100% of remainder
```

Distribution: SKY stakers via the Smart Burn Engine buyback mechanism.

---

## 7. Worked examples

### Genesis early stage (low revenue)

```
Net Revenue:          200M
NRR:                  0.0625
Buffer Status:        $50M (target $150M) → Phase 1 (Safety Floor)
S&M Rate:             21% (Genesis)

Step 1 (S&M):         42.0M           → 158.0M remaining
Step 2 (ABC):         39.5M (25%)     → 118.5M remaining
Step 3 (Fortif):       1.5M (1.25%)   → 117.0M remaining
Step 4 (Burn):         1.5M (1.25%)   → 115.6M remaining
Step 5 (Staking):    115.6M
```

### Post-Genesis mature (high revenue, full ABC)

```
Net Revenue:           5B
NRR:                   0.625
Buffer Status:         Buffer ≥ target → Phase 3 (Full)
S&M Rate:              8% (post-Genesis)

Step 1 (S&M):        400.0M           → 4.60B remaining
Step 2 (ABC):          0   (0%)       → 4.60B remaining
Step 3 (Fortif):     575.0M (12.5%)   → 4.03B remaining
Step 4 (Burn):       503.1M (12.5%)   → 3.52B remaining
Step 5 (Staking):    3.52B
```

### Key properties

| Property | Mechanism |
|---|---|
| **Sequential deduction** | Each step operates on what remains; all priorities funded before surplus flows to staking |
| **Scale-responsive** | Fortification and Burn allocations grow with NRR, reflecting greater need for legal infra and value capture at scale |
| **Buffer dynamics** | ABC fills aggressively when empty (up to 50% allocation at maximum NRR), stops entirely when full — self-regulating solvency mechanism |
| **Genesis vs Post-Genesis** | Higher S&M during Genesis reflects intensive development and infrastructure buildout |

---

## 8. Phase 1 vs target behavior

| Aspect | Phase 1 reality | Target |
|---|---|---|
| Settlement cadence | Monthly (manual processing, end of following month) | Daily (Phase 3+) |
| Smart Burn | Fixed $300K/day buyback; Steps 4+5 unified | Dynamic burn rate via SBE BEAM |
| S&M cap | 21% Genesis | 4–10% (10% permanent ceiling) |
| ABC target | $125M Phase 1 floor | 1.5% of USDS supply |
| Settlement closure | Synserv-run synlang code; settlement actions manual in Phase 1 | Beacon-operated execution from Phase 2+ |

For the synserv heartbeat that runs the per-Prime computations, see [`settlement-cycle.md`](settlement-cycle.md). The five-step per-Prime calculation feeds the protocol-level **Sky Net** that this TMF then distributes.

---

## File map

| Doc | Relationship |
|---|---|
| [`README.md`](lani/accounting/README.md) | Accounting directory index |
| [`settlement-cycle.md`](settlement-cycle.md) | Per-Prime closure produces the Sky Net that the TMF distributes |
| [`capital-stack.md`](capital-stack.md) | ABC's role in insolvency defense; Genesis Capital structure |
| [`entity-fees.md`](entity-fees.md) | Synomic Entity fees (creation, upkeep, rebate) — feed Sky's gross revenue before it enters the TMF |
| [`distribution-rewards.md`](distribution-rewards.md) | Distribution Rewards and Structural Demand Resource Rewards — paid to Primes from Sky's revenue |
| [`../growth-staking/growth-staking.md`](../growth-staking/growth-staking.md) | Forfeited Growth Staking rewards re-enter the TMF aggregation in `&core.settlement` |
| [`../inactive/pre-synlang/forecast_model/`](../inactive/pre-synlang/forecast_model/) | Forecast model implements a simplified 3-step waterfall version |

---

## One-line summary

**The TMF is a five-step sequential waterfall (Security & Maintenance → Aggregate Backstop Capital → Fortification Conserver → Smart Burn → Staking Rewards) that distributes all protocol net revenue, with the Net Revenue Ratio scaling Steps 3–4 to grow with protocol revenue and the ABC step self-regulating around its 1.5%-of-supply target via three fill phases.**
