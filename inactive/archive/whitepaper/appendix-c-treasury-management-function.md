# Appendix C: Treasury Management Function

The Sky Treasury Management Function (TMF) is a single, linear waterfall mechanism that manages all protocol net revenue. All calculations and transfers are denominated in USDS.

---

## Overview

Protocol net revenue (Revenue minus Expenses) enters the top of the waterfall and flows sequentially through five steps:

| Step | Name | Purpose |
|------|------|---------|
| 1 | Security & Maintenance | Fund core teams, security, risk management |
| 2 | Aggregate Backstop Capital | Build solvency buffer against bad debt |
| 3 | Fortification Conserver | Legal defense, resilience, unquantifiable risk |
| 4 | Smart Burn Engine | SKY buybacks |
| 5 | Staking Rewards | Distribution to SKY stakers |

Each step calculates its allocation based on the **Step Result** passed down from the previous step, ensuring capital flows through every layer before reaching staking rewards.

---

## Net Revenue Ratio

The Net Revenue Ratio determines how aggressively the protocol funds stability buffers and token burn based on total protocol net revenue. It scales allocations so that at low revenue, most surplus flows to staking rewards, while at higher revenue, more flows to burn and fortification.

### Constants

| Parameter | Value |
|-----------|-------|
| Target Constant | 3 Billion USDS |
| Cap Threshold | 1 Trillion USDS |

### Formula (Piecewise Hyperbolic)

```python
TARGET_CONSTANT = 3_000_000_000    # 3 Billion
CAP_THRESHOLD   = 1_000_000_000_000  # 1 Trillion

if current_yearly_net_revenue < CAP_THRESHOLD:
    # Hyperbolic curve to prevent quadratic drag
    net_revenue_ratio = current_yearly_net_revenue / (current_yearly_net_revenue + TARGET_CONSTANT)
else:
    # Snaps to 1.0 at 1 Trillion
    net_revenue_ratio = 1.0
```

### Ratio Examples

| Yearly Net Revenue | Net Revenue Ratio |
|--------------------|-------------------|
| 200 Million | 0.0625 |
| 500 Million | 0.143 |
| 1 Billion | 0.25 |
| 2 Billion | 0.40 |
| 3 Billion | 0.50 |
| 5 Billion | 0.625 |
| 10 Billion | 0.77 |
| 20 Billion | 0.87 |
| 100 Billion | 0.97 |
| 1 Trillion+ | 1.0 |

The hyperbolic curve prevents "quadratic drag" (rewards decreasing proportionally) as revenue grows. It smoothly approaches 0.997 at 1 Trillion, then snaps to exactly 1.0.

---

## Step 1: Security and Maintenance

The first allocation funds core teams responsible for governance security, protocol security, risk management, and ongoing maintenance and development of critical infrastructure.

### Allocation

| Phase | Allocation |
|-------|------------|
| Genesis Phase | 21% of Total Net Revenue |
| Post-Genesis | 4–10% of Total Net Revenue (governance determined) |

### Calculation

```python
step_1_allocation = net_revenue * security_rate  # 0.21 genesis, 0.04-0.10 post-genesis
step_1_result = net_revenue - step_1_allocation
```

### Destination

Core Budget & Operational Multisigs

---

## Step 2: Aggregate Backstop Capital

This step builds the protocol's solvency buffer (denominated in USDS) to protect against bad debt or insolvency events.

### Target Size

1.5% of Total Supply (Liabilities)

### Allocation Rate Formula

```python
# Calculate how much space is left in the buffer (1.0 = Empty, 0.0 = Full)
fill_factor = 1.0 - (current_buffer_size / target_buffer_size)

# Apply 10% floor to the Net Revenue Ratio
effective_ratio = max(net_revenue_ratio, 0.10)

# Calculate dynamic rate (Max 50% when empty)
step_2_rate = fill_factor * 0.50 * effective_ratio
```

### Three Phases

| Phase | Condition | Allocation |
|-------|-----------|------------|
| **Phase 1: Safety Floor & Turbo Fill** | Buffer < 125M USDS | `max(0.25, step_2_rate) × step_1_result` |
| **Phase 2: Filling** | 125M ≤ Buffer < Target | `step_2_rate × step_1_result` |
| **Phase 3: Hard Cap** | Buffer ≥ Target | 0% |

**Phase 1** ensures aggressive buffer building when reserves are critically low, with a 25% floor allocation regardless of the calculated rate.

**Phase 2** uses the dynamic rate formula, filling faster when the buffer is emptier and slowing as it approaches target.

**Phase 3** stops all allocation once the buffer reaches target, allowing full flow-through to subsequent steps.

### Calculation

```python
if current_buffer < 125_000_000:
    # Phase 1: Safety Floor
    step_2_allocation = max(0.25, step_2_rate) * step_1_result
elif current_buffer < target_buffer_size:
    # Phase 2: Filling
    step_2_allocation = step_2_rate * step_1_result
else:
    # Phase 3: Full
    step_2_allocation = 0

step_2_result = step_1_result - step_2_allocation
```

---

## Step 3: Fortification Conserver Account

This step funds the Fortification Conserver, currently the Fortification Foundation. The Fortification Conserver is an Alignment Conserver responsible for:

- Legal defense
- Resilience infrastructure
- Unquantifiable risk management
- Triggering SKY emissions backstop in case of insolvency (currently disabled, future upgrade)

### Scaling Rationale

At small scale, Sky can depend on established legal infrastructure built by larger entities. As Sky grows, it increasingly cannot rely on external protection mechanisms, making the Fortification Conserver more critical. Hence the allocation grows with Net Revenue.

### Allocation Formula

```python
step_3_allocation = (0.20 * net_revenue_ratio) * step_2_result
step_3_result = step_2_result - step_3_allocation
```

### Effective Rates by Scale

| Net Revenue Ratio | Effective Rate (of Step 2 Result) |
|-------------------|-----------------------------------|
| 0.0625 | 1.25% |
| 0.25 | 5% |
| 0.40 | 8% |
| 0.625 | 12.5% |
| 0.87 | 17.4% |
| 1.0 | 20% |

---

## Step 4: Smart Burn Engine

This step captures value for token holders by buying SKY from the market. Purchased SKY is distributed to stakers as additional yield.

### Allocation Formula

```python
step_4_allocation = (0.20 * net_revenue_ratio) * step_3_result
step_4_result = step_3_result - step_4_allocation
```

### Effective Rates by Scale

| Net Revenue Ratio | Effective Rate (of Step 3 Result) |
|-------------------|-----------------------------------|
| 0.0625 | 1.25% |
| 0.25 | 5% |
| 0.40 | 8% |
| 0.625 | 12.5% |
| 0.87 | 17.4% |
| 1.0 | 20% |

### Properties

- **Programmatic execution** — Operates automatically based on protocol parameters
- **Scaling allocation** — Receives larger share as protocol revenue grows
- **Transparent** — All transactions visible on-chain

---

## Step 5: Staking Rewards

All remaining USDS after Steps 1–4 flows to staking rewards. This is the primary destination for surplus, especially during the Genesis Phase when the Net Revenue Ratio is low.

### Allocation

```python
step_5_allocation = step_4_result  # 100% of remainder
```

### Destination

Distributed to SKY stakers

---

## Example Scenarios

The following scenarios illustrate waterfall distribution under different conditions. These are **calculation examples only, not financial forecasts**.

### Summary

| Scenario | Net Revenue | Net Revenue Ratio | Smart Burn | Staking Rewards |
|----------|-------------|-------------------|------------|-----------------|
| Early Stage (Genesis) | 200M | 0.0625 | ~1.5M | ~115.6M |
| Growth Stage (Post-Genesis) | 2B | 0.40 | ~114.8M | ~1.32B |
| Mature Stage (Post-Genesis) | 5B | 0.625 | ~503.1M | ~3.52B |
| Massive Scale (Post-Genesis) | 20B | 0.87 | ~2.64B | ~12.55B |

---

### Scenario 1: Early Stage / Low Profit (Genesis Phase)

**Conditions:**
- Total Net Revenue: 200 Million USDS
- Net Revenue Ratio: 0.0625
- Buffer Status: 50M (Target 150M) → Phase 1 (Safety Floor)

```python
net_revenue = 200_000_000

# Step 1: Security (21% - Genesis Phase)
step_1_allocation = net_revenue * 0.21              # 42,000,000
step_1_result     = net_revenue - step_1_allocation # 158,000,000

# Step 2: Backstop (Phase 1: Safety Floor)
# Formula: (1 - 50/150) * 50% * max(0.0625, 0.10) = 0.66 * 0.5 * 0.10 = 3.3%
# Floor of 25% applies because 25% > 3.3%
step_2_allocation = step_1_result * 0.25            # 39,500,000
step_2_result     = step_1_result - step_2_allocation # 118,500,000

# Step 3: Fortification (0.0625 * 20% = 1.25%)
step_3_allocation = step_2_result * 0.0125          # 1,481,250
step_3_result     = step_2_result - step_3_allocation # 117,018,750

# Step 4: Burn (0.0625 * 20% = 1.25%)
step_4_allocation = step_3_result * 0.0125          # 1,462,734
step_4_result     = step_3_result - step_4_allocation # 115,556,016

# Step 5: Staking Rewards
final_staking_rewards = 115_556_016                 # ~115.6 Million
```

| Step | Allocation | Cumulative |
|------|------------|------------|
| Security | 42.0M | 42.0M |
| Backstop | 39.5M | 81.5M |
| Fortification | 1.5M | 83.0M |
| Burn | 1.5M | 84.5M |
| **Staking** | **115.6M** | 200.0M |

---

### Scenario 2: Growth Stage / Medium Profit (Post-Genesis)

**Conditions:**
- Total Net Revenue: 2 Billion USDS
- Net Revenue Ratio: 0.40
- Buffer Status: 500M (Target 1.5B) → Phase 2 (Filling)

```python
net_revenue = 2_000_000_000

# Step 1: Security (10% - Post-Genesis)
step_1_allocation = net_revenue * 0.10              # 200,000,000
step_1_result     = net_revenue - step_1_allocation # 1,800,000,000

# Step 2: Backstop (Phase 2: Filling)
# Fill Factor = (1.5B - 500M) / 1.5B = 0.666
# Rate = 0.666 * 50% * 0.40 = 13.33%
step_2_allocation = step_1_result * 0.1333          # 240,000,000
step_2_result     = step_1_result - step_2_allocation # 1,560,000,000

# Step 3: Fortification (0.40 * 20% = 8%)
step_3_allocation = step_2_result * 0.08            # 124,800,000
step_3_result     = step_2_result - step_3_allocation # 1,435,200,000

# Step 4: Burn (0.40 * 20% = 8%)
step_4_allocation = step_3_result * 0.08            # 114,816,000
step_4_result     = step_3_result - step_4_allocation # 1,320,384,000

# Step 5: Staking Rewards
final_staking_rewards = 1_320_384_000               # ~1.32 Billion
```

| Step | Allocation | Cumulative |
|------|------------|------------|
| Security | 200M | 200M |
| Backstop | 240M | 440M |
| Fortification | 124.8M | 564.8M |
| Burn | 114.8M | 679.6M |
| **Staking** | **1.32B** | 2.0B |

---

### Scenario 3: Mature Stage / High Profit (Post-Genesis)

**Conditions:**
- Total Net Revenue: 5 Billion USDS
- Net Revenue Ratio: 0.625
- Buffer Status: 10B (Target 7.5B) → Phase 3 (Full)

```python
net_revenue = 5_000_000_000

# Step 1: Security (8% - Post-Genesis)
step_1_allocation = net_revenue * 0.08              # 400,000,000
step_1_result     = net_revenue - step_1_allocation # 4,600,000,000

# Step 2: Backstop (Phase 3: Full - buffer exceeds target)
step_2_allocation = 0
step_2_result     = step_1_result                   # 4,600,000,000

# Step 3: Fortification (0.625 * 20% = 12.5%)
step_3_allocation = step_2_result * 0.125           # 575,000,000
step_3_result     = step_2_result - step_3_allocation # 4,025,000,000

# Step 4: Burn (0.625 * 20% = 12.5%)
step_4_allocation = step_3_result * 0.125           # 503,125,000
step_4_result     = step_3_result - step_4_allocation # 3,521,875,000

# Step 5: Staking Rewards
final_staking_rewards = 3_521_875_000               # ~3.52 Billion
```

| Step | Allocation | Cumulative |
|------|------------|------------|
| Security | 400M | 400M |
| Backstop | 0 | 400M |
| Fortification | 575M | 975M |
| Burn | 503.1M | 1.48B |
| **Staking** | **3.52B** | 5.0B |

---

### Scenario 4: Massive Scale (Post-Genesis)

**Conditions:**
- Total Net Revenue: 20 Billion USDS
- Net Revenue Ratio: 0.87
- Buffer Status: 20B (Target 15B) → Phase 3 (Full)

```python
net_revenue = 20_000_000_000

# Step 1: Security (8% - Post-Genesis)
step_1_allocation = net_revenue * 0.08              # 1,600,000,000
step_1_result     = net_revenue - step_1_allocation # 18,400,000,000

# Step 2: Backstop (Phase 3: Full - buffer exceeds target)
step_2_allocation = 0
step_2_result     = step_1_result                   # 18,400,000,000

# Step 3: Fortification (0.87 * 20% = 17.4%)
step_3_allocation = step_2_result * 0.174           # 3,201,600,000
step_3_result     = step_2_result - step_3_allocation # 15,198,400,000

# Step 4: Burn (0.87 * 20% = 17.4%)
step_4_allocation = step_3_result * 0.174           # 2,644,521,600
step_4_result     = step_3_result - step_4_allocation # 12,553,878,400

# Step 5: Staking Rewards
final_staking_rewards = 12_553_878_400              # ~12.55 Billion
```

| Step | Allocation | Cumulative |
|------|------------|------------|
| Security | 1.6B | 1.6B |
| Backstop | 0 | 1.6B |
| Fortification | 3.2B | 4.8B |
| Burn | 2.64B | 7.45B |
| **Staking** | **12.55B** | 20.0B |

---

## Key Properties

### Sequential Deduction
Each step operates on what remains after previous steps, ensuring all priorities are funded before surplus flows to staking.

### Scale-Responsive
The Net Revenue Ratio causes Fortification and Burn allocations to grow with protocol scale, reflecting increased need for legal infrastructure and value capture at larger sizes.

### Buffer Dynamics
The Backstop buffer fills aggressively when empty (up to 50% allocation at maximum Net Revenue Ratio; the effective rate scales with the Net Revenue Ratio) and stops entirely when full, creating a self-regulating solvency mechanism.

### Genesis vs Post-Genesis
Higher Security allocation during Genesis (21% vs 4-10%) reflects the intensive development and infrastructure buildout required in early phases.

---

*Parameters subject to change through decentralized governance. This appendix describes the TMF design as of December 2025.*
