# Growth Staking

**Status:** Draft concept
**Date:** February 2026

---

## Overview

Growth Staking aligns SKY governance token holders with ecosystem innovation. Under Growth Staking, SKY stakers must also hold other Sky Ecosystem tokens — called **growth assets** — to unlock staking rewards. The more directly a growth asset contributes to ecosystem innovation, the higher its **Growth Factor** — the multiplier that amplifies its contribution to the staking requirement.

Eligible growth assets are deliberately limited to instruments that require an individual investment decision and carry meaningful risk: Agent governance tokens (Generator, Guardian, Prime, Halo) and Prime junior risk capital (TEJRC). Passive yield wrappers — savings tokens, senior risk capital, and Halo Units — are excluded. This keeps Growth Staking pointed at the live edge of innovation rather than at safe carry.

This creates a direct economic link between governance participation (staking SKY) and investment in the ecosystem's equity-like growth layer.

---

## The Growth Factor

Each eligible growth asset has a **Growth Factor (GF)** — a multiplier on the asset's Reference Value that determines how much it counts toward unlocking staking rewards.

| Category | Assets | Growth Factor | Effect |
|---|---|---|---|
| **Agent governance tokens** | Generator, Guardian, Prime, Halo | 2.5× | $1 counts as $2.50 |
| **Junior risk capital** | TEJRC (per-Prime) | ~1.67× | $1 counts as $1.67 |

**Excluded assets:** Senior risk capital (srSGA, TISRC, ESRC), savings tokens (sSGA, fixed-rate sSGA), Halo Units (Portfolio, Term, Trading shares), stSCST, LCTS queue positions, DAI, MKR. These are passive holdings that don't require an active investment thesis — Growth Staking is reserved for capital that flows into innovation through individual judgment.

### Reward Scaling

Rewards scale linearly from 0% to 100% based on how much of the staking requirement is satisfied. All values use **Reference Values** — fundamentals-based prices that filter out speculative swings (see [Reference Valuation](#reference-valuation) below).

```
Staking Factor = min(1, Σ(Asset Reference Value_i × Growth Factor_i) / SKY Reference Value)

Staking Rewards = Base Staking Yield × Staked SKY × Staking Factor
```

**Example** — SKY Reference Value implies $100k staked position, with Prime tokens at GF 2.5×:

| Prime tokens held (at Reference Value) | Growth-Factor-adjusted value | Staking Factor |
|---|---|---|
| $0 | $0 | 0% |
| $20k | $50k ($20k × 2.5) | 50% |
| $40k | $100k ($40k × 2.5) | 100% |

When multiple growth assets are held, each is converted to its GF-adjusted Reference Value and the contributions are summed:

```
Total GF Reference Value = Σ (Asset Reference Value_i × GF_i)

Staking Factor = min(1, Total GF Reference Value / Staked SKY Reference Value)
```

**Example** — $100k staked SKY (at Reference Value), holding $20k SPK (at Reference Value, GF 2.5×) + $18k Spark TEJRC (GF ~1.67×):

```
GF Value = ($20k × 2.5) + ($18k × 1.67) = $50k + $30k = $80k
Staking Factor = min(1, $80k / $100k) = 80%
```

If SKY's market price then doubles on speculation while protocol revenue stays flat, the Reference Value is unchanged — this staker still earns 80%, not 40%.

---

## Reference Valuation

All values in the staking factor calculation — both the growth asset numerator and the staked SKY denominator — use **Reference Values** derived from fundamentals rather than spot market prices. This makes the entire Growth Staking system immune to speculative price swings in any token, including SKY itself.

The core principle: if nothing changes about the actual economics of the ecosystem, nothing should change about a staker's reward percentage.

```
Staking Factor = min(1, Total GF Reference Value / Staked SKY Reference Value)
```

Every token enters this formula at its Reference Value, never its spot market price.

### Global P/E Model

Reference Values for revenue-generating assets are derived from a **global P/E model** with three governance-set parameters per income stream:

**Global parameter (governance-set):** Base P/E (e.g., 15)

**Per-income-stream parameters:**
- **Modifier** — multiplier on Base P/E to get the center P/E for this income stream
- **Variance** — fractional range around the center P/E
- **Growth rate** — trailing revenue growth, converted to a score (0–100) that positions the actual P/E within the variance window

```
Center P/E = Global Base P/E × Modifier
Band = Center P/E × Variance
Actual P/E = Center - Band + (score / 100) × (2 × Band)
```

**Example** — Base P/E = 15, Modifier = 1.0, Variance = 0.3, Growth score = 75:

```
Center P/E = 15 × 1.0 = 15
Band = 15 × 0.3 = 4.5
Actual P/E = 15 - 4.5 + (75/100) × (2 × 4.5) = 10.5 + 6.75 = 17.25
```

This model allows governance to express views on income quality (via Modifier), uncertainty (via Variance), and growth momentum (via the growth rate → score mapping), all anchored to a single global Base P/E that can be adjusted for market conditions.

### SKY Reference Value

SKY is valued using the global P/E model applied to Sky Core's revenue streams:

```
SKY Reference Value = (SKY Core Revenue × Actual P/E + SKY Special Revenue × Special P/E) / SKY Circulating Supply
```

**SKY Core revenue (standard P/E — Modifier, Variance, growth score as above):**
- SCST spread (interest rate margin on stablecoin credit)
- SCST risk capital fees (fees on SRC, TISRC, TEJRC, stSCST)
- Agent upkeep (25 bps/year on agent token supply)
- Guardian accord fees
- SCST duration income (duration matching revenue)
- 5% share of Generator revenue

**SKY special revenue (separate Modifier/Variance — typically discounted):**
- Agent creation fee token sales (5% of newly issued agent tokens)

Special revenue receives a separate Modifier (typically < 1.0) because token sale income is lumpy and non-recurring. Governance sets the special Modifier and Variance independently.

Updated at each daily settlement based on trailing revenue figures.

**Effect:** If SKY market price doubles on speculation but protocol revenue hasn't changed, the Reference Value stays the same — stakers' staking factors are unchanged. Conversely, if protocol revenue doubles, the Reference Value rises to reflect genuine growth, and stakers naturally need more growth assets to maintain 100%.

### Generator Reference Value

Generators are valued as a combination of standard P/E on operating revenue plus book value on stability capital:

```
Generator Reference Value = (Generator Revenue × Actual P/E + ISRC Book Value) / Tokens Outstanding
```

**Generator revenue (standard P/E — keeps 95% of gross, 5% to Sky Core):**
- SGA fees (on USDS and other SGA transactions)
- SGA spread (interest rate margin on generated assets)
- SGA risk capital fees (fees on ESRC, TISRC, TEJRC)
- SGA duration income (duration matching revenue)

**Generator book value:**
- ISRC holdings (stability capital overflow, SBE dry powder)

ISRC (Internal Senior Risk Capital) is valued at par — no P/E applied to capital reserves.

### Guardian Reference Value

Guardians are valued using P/E on operating income plus book value on SKY holdings:

```
Guardian Reference Value = (Accord Fee Income × Actual P/E + SKY Holdings Book Value) / Tokens Outstanding
```

- **Accord fees** — recurring revenue from Guardian Accord relationships with Primes and other agents. Valued via the global P/E model.
- **SKY holdings** — SKY tokens held by the Guardian, valued at SKY Reference Value (book value, no P/E multiplier on holdings).
- **sUSDS** — Used as operational collateral. The sUSDS income feeds the P/E component (as part of accord fee income), but the sUSDS balance itself is not counted as book value to avoid double-counting.

### Prime Reference Value

Primes are valued at net capital reserves — no P/E component:

```
Prime Reference Value = Net Capital Reserves / Tokens Outstanding
```

Net capital reserves include look-through to Reference Value for any Halo Agent tokens the Prime holds.

A Prime holding $500M in capital reserves with 10B tokens outstanding has a Reference Value of $0.05 per token. If the market price is $0.08, the staking factor calculation uses $0.05. If the market price is $0.03, the staking factor calculation uses $0.03.

### Halo Reference Value

Halos are valued using capital reserves plus earnings:

```
Halo Reference Value = (Capital Reserves + Annual Earnings × Actual P/E) / Tokens Outstanding
```

Earnings are valued via the global P/E model. Capital reserves are valued at par.

**Early-stage Halos:** A newly capitalized Halo with no earnings history can still count toward the favorable Agent token Growth Factor — provided its synomic artifacts demonstrate that the capital is being actively spent on genuine growth (building technology, deploying infrastructure, etc.). This is a qualitative assessment based on observable synomic activity, not just capital sitting idle. Once earnings materialize, the P/E component takes over as the primary value driver.

### Agent Token Floor

Agent tokens are valued at the **lower of Reference Value or market value**. The min() floor ensures that if an Agent token's market price collapses below fundamentals (distressed sale, illiquidity), the staking factor calculation reflects the worse reality.

```
Effective Value = min(Reference Value, Market Value)
```

The asymmetry is deliberate: you can't inflate growth asset values by pumping, but genuine impairment does reduce your staking factor credit. SKY uses Reference Value directly (not min) because the denominator should be stable — a SKY dump shouldn't make it trivially easy to earn full rewards.

### TEJRC

TEJRC is valued at its on-chain redemption value — no Reference Value adjustment needed, since the token is directly backed by underlying capital at a known ratio.

### Tokenized vs Tokenless

Not all agents participate in Growth Staking as growth assets:

| Agent | Tokenized | Growth Asset |
|---|---|---|
| **Guardian** | Yes | Yes (governance token GF 2.5×) |
| **Prime** | Yes; also issues TISRC, TEJRC | Yes (governance token GF 2.5×, TEJRC GF ~1.67×; TISRC excluded) |
| **Generator** | Yes; also issues ESRC, sSGA, fixed-rate sSGA, stSCST | Yes (governance token GF 2.5×; all other issued tokens excluded) |
| **Halo** | Yes; also issues Halo Units | Yes (governance token GF 2.5×; Halo Units excluded) |
| **Core Controlled** | No | No |
| **Recovery** | No | No |
| **Folio** | No | No (is the staking vehicle) |

### Why Reference Values Throughout

Using fundamental values on both sides of the staking factor formula creates a system where the staking relationship reflects real economic reality:

| Scenario | Market price effect | Staking factor effect |
|---|---|---|
| SKY pumps speculatively | SKY market price rises | No change — SKY Reference Value unchanged |
| Agent token pumps speculatively | Agent market price rises | No change — Agent Reference Value unchanged |
| Protocol revenue grows | SKY Reference Value rises | Stakers need more growth assets — correct, the ecosystem is bigger |
| Prime deploys more capital | Prime Reference Value rises | Staker gets more GF credit — correct, real capital at work |
| SKY dumps on panic selling | SKY market price falls | No change — SKY Reference Value unchanged |
| Agent token dumps | Agent market price falls below Reference | Staking factor uses market price — correct, reflects real impairment |

---

## The Folio Agent

To participate in Growth Staking, a SKY holder creates a **Folio Agent** — a standardized holding structure (rank 3) that serves as a self-contained staking and investment vehicle. See [`sky-agents/folio-agents/agent-type-folios.md`](../sky-agents/folio-agents/agent-type-folios.md) for the full specification.

Key properties:
- **Instant creation** — any SKY holder
- **Not a Halo** — tokenless, single owner (the principal), no Halo Units
- **PAU-based** — holds staked SKY + growth asset portfolio
- **Two operating modes** — automated (sentinel formation) or principal control (principal sentinel)
- **Type 1 Restructure** — graduate to Standard Halo or Prime when ready

---

## Agent-Internal Growth Staking

Primes and Halos that hold SKY in their treasuries automatically earn Growth Staking rewards — the Agent's own book value counts as its growth asset portfolio at GF 2.5×. No separate Folio Agent is needed; the Agent itself functions as one.

A Prime effectively counts as a SKY staker with all of its own tokens in its Folio Agent. Same for a Halo holding SKY.

**Example** — A Prime with $500M Reference Value holding SKY worth $10M at SKY Reference Value:

```
GF Reference Value = $500M × 2.5 = $1.25B effective
Staking Factor on $10M SKY (at Reference Value) = min(1, $1.25B / $10M) = 100%
```

Any Agent with meaningful book value trivially satisfies the growth requirement, making SKY holdings essentially free yield for Agents. This creates a structural incentive for Primes and Halos to accumulate SKY in their treasuries — aligning Agent operations with protocol governance and creating natural demand for SKY from the innovation layer itself.

### Double-counting

This creates an accepted paradox: an Agent's book value is used twice for staking factor purposes — once by the Agent itself (to unlock staking rewards on its own SKY holdings), and a second time by external token holders (who hold the Agent's tokens as growth assets in their Folio Agents). The same underlying book value supports both claims. This is by design — the double-counting amplifies the incentive to build genuine book value within Agents, and the protocol accepts this as a worthwhile tradeoff for the alignment it creates.

---

## Incentive Effects

### Capital flow from passive to active

Growth Staking creates a direct incentive to convert passive holdings into active innovation investment:

```
$100k sSGA (or other passive holding) → GF value: $0 (excluded)
    ↓ invest into a Prime
$100k in Prime tokens → GF value: $100k × 2.5 = $250k effective
```

Holding savings tokens, senior risk capital, or Halo Units earns no staking factor. Stakers who want rewards must take a position on a specific Agent — picking which Prime, Halo, Generator, or Guardian to back, or which Prime's first-loss tranche (TEJRC) to underwrite.

### Ecosystem alignment

- **SKY whales** must become active ecosystem participants — passive governance holders earn nothing
- **Agent token demand** is structurally supported by stakers seeking efficient GF
- **Junior risk capital supply** increases as stakers underwrite specific Primes via TEJRC for GF credit
- **Mercenary staking** is eliminated — holding SKY alone earns nothing, and neither does parking capital in passive yield wrappers

### Natural segmentation

- Concentrated stakers → hold Agent governance tokens (GF 2.5×) → maximum capital efficiency, full equity exposure to a chosen Agent
- Underwriters → hold one or more Primes' TEJRC (GF ~1.67×) → first-loss exposure to a specific Prime's book without governance responsibility
- Mixed → blend governance tokens and TEJRC across Agents to express a portfolio thesis

There is no passive tier. Earning Growth Staking rewards requires picking specific Agents to back.

---

## Anti-Gaming

The primary defense against manipulation is the **Reference Valuation framework** — market price movements don't affect the staking factor calculation in either direction. You cannot inflate staking factor value by pumping Agent token prices, and you cannot reduce your staking factor requirement by pumping SKY.

A secondary concern is **hollow agents** — Primes or Halos created solely to warehouse capital and claim favorable GF without genuine innovation activity. Defenses:

1. **Mechanical (day one):** Reference Values are based on actual capital reserves (Primes) or earnings (Halos), so capital must be genuinely deployed or revenue genuinely earned.
2. **Synomic monitoring (when needed):** Governance can monitor the synomic artifacts of Primes and Halos. A real level of intelligent synomic activity must be observed for an Agent's tokens to maintain GF eligibility. This monitoring layer is deferred — implemented only when manipulation attempts actually occur.

The same monitoring applies to potentially hollow TEJRC positions.

---

## Open Design Questions

- **GF governance** — Are Growth Factors set by governance vote, or derived from on-chain metrics?
- **P/E revision cadence** — How often is the global Base P/E updated? Quarterly governance vote?
- **Revenue trailing period** — What lookback window for trailing revenue? Trailing 12 months? Trailing 6 months annualized? Shorter windows are more responsive but more volatile.
- **Growth score mapping** — What formula converts trailing revenue growth rate to a 0–100 score? Linear? Sigmoid? Capped?
- **New Agents with no history** — A new Prime with zero capital reserves or a new Halo with zero earnings would have zero Reference Value. Intended? (Likely yes — prove value before getting GF credit.)
- **Measurement timing** — Snapshot at daily settlement, or time-weighted average to prevent flash-positioning?
- **Forfeited rewards** — Where do unclaimed rewards (from stakers below 100% staking factor) flow? Back to TMF waterfall? Redistributed to fully-qualifying stakers?
- **Reference Value divergence** — What happens if SKY market price diverges extremely from Reference Value (e.g., 10× above or below)? Is this purely informational, or should there be a governance-triggered recalibration mechanism?
