# Genesis Capital: How Sky's Backstop Mechanism Works

This document explains the Genesis Capital system — a temporary mechanism designed to bootstrap Sky's agent ecosystem while providing a safety net for USDS holders.

---

## Glossary of Key Terms

**Allocated Genesis Capital:** The specific funds deployed from Sky Core to Genesis Agents. Its primary purpose is to bootstrap innovation and diversity. It is subtracted when calculating the protocol's safety margin.

**Aggregate Backstop Capital:** The "safety net." Defined as:
```
Total Genesis Capital - Allocated Genesis Capital
```
This represents the excess capital backing USDS beyond standard collateral. (The Core Council Buffer was previously included in this formula but has been reclassified as operational capital — see `current-accounting.md` for details.)

**Genesis Capital Backstop Mechanism:** The specific portion of capital held by agents that Sky can "reclaim" as a last line of defense during a crisis (after SKY token inflation fails but before a USDS haircut).

**Genesis Agents:** The broad category of autonomous entities within the Sky Ecosystem that receive capital to foster growth.

**Star Primes:** The main type of Sky Agents that allocate USDS collateral on behalf of Sky (e.g., Spark, Grove, Keel).

**Institutional Primes:** Sky Agents optimized for institutional participants (e.g., Obex).

**Guardian Agents:** Sky Agents tasked with operationalizing and buffering risk related to governance operations and governance security (distinct from governance Guardians who vote in SpellGuard — see Glossary: Guardian Role Mapping). They negotiate paid Guardian Accords with Star Primes and Institutional Primes.

---

## The Role of Allocated Genesis Capital

Allocated Genesis Capital represents the resources deployed by Sky into Genesis Agents, specifically designed to bootstrap diversity and foster innovation within the Sky Ecosystem.

When this capital is allocated from Sky Core, it serves as a foundational source of stability for Sky, USDS, and the broader ecosystem.

**Key insight:** Genesis Capital allocation is NOT an expense. It's a capital deployment that remains as backstop capital within the system.

An upcoming Atlas Edit Proposal will specify the Genesis Capital Backstop Mechanism and define the Aggregate Backstop Capital formula. This figure represents the total pool of excess capital backing USDS beyond its standard collateral portfolio — available to backstop insolvency losses in the worst-case scenario.

---

## Insolvency Defenses: The Hierarchy

The protocol has established a specific hierarchy of defenses to handle bad liquidations or significant losses:

### Defense Level 1: Aggregate Backstop Capital
If a Star Prime experiences losses beyond its collateral, the Aggregate Backstop Capital absorbs the loss first.

### Defense Level 2: SKY Token Inflation
If Aggregate Backstop Capital goes negative after one or more Sky Agents are fully liquidated, the system will inflate SKY tokens to cover the shortfall.

### Defense Level 3: Genesis Capital Backstop Mechanism
In the extreme scenario where the SKY token price fully collapses to 0 and cannot generate further funding, Sky enacts its last line of defense by reclaiming capital through the Genesis Capital Backstop Mechanism from the Genesis Agents.

**If reclaimed capital is sufficient:**
- Genesis Agent Token holders (who effectively covered the loss after SKY was diluted to zero) receive an airdrop of the new SKY supply

### Defense Level 4: USDS Haircut (Final Resort)
If the Genesis Capital Backstop Mechanism is insufficient to recapitalize the system, the final loss is socialized among USDS holders via a haircut.

**In this outcome:**
- USDS holders receive the airdrop of the new SKY token supply
- This allows them to configure the system to utilize future returns to recover the original 1:1 USDS peg

**Relationship to the 7-step loss absorption waterfall:** This 4-level view is a simplified Genesis Capital perspective. The whitepaper's detailed 7-step waterfall maps as follows: steps 1-4 (FLC, JRC, Agent Token Inflation, SRC Pool) are collectively captured by Level 1 (Aggregate Backstop Capital), step 5 (SKY Token Inflation) maps to Level 2, step 6 (Genesis Capital Haircut) maps to Level 3, and step 7 (USDS Peg Adjustment) maps to Level 4. See the [whitepaper Part 6](../whitepaper/sky-whitepaper.md) for the complete waterfall.

---

## Capital Targets and Revenue Retention

To strengthen these defenses, an upcoming Atlas edit proposal includes:

### New Aggregate Backstop Capital Target: $125M (Phase 1 Safety Floor)
(Increased from the current $37M. The long-term target is 1.5% of total USDS supply, per the TMF — see `whitepaper/appendix-c-treasury-management-function.md`.)

### Revenue Retention Requirement
Sky will retain a minimum of **25% of net revenue after Security and Maintenance allocation** every Monthly Settlement to grow the Aggregate Backstop Capital.

### What Happens When Target Is Met
Once the $125M target is reached:
- The minimum retention requirement ceases
- TMF allocations shift primarily toward staking rewards
- Smart Burn Engine can operate at full capacity

**Relationship to TMF target:** The $125M target applies during the Genesis Phase. Post-Genesis, the TMF's dynamic target of 1.5% of total USDS supply governs backstop sizing (see [Appendix C](../whitepaper/appendix-c-treasury-management-function.md)).

---

## Genesis Capital Phase-out

The Genesis Capital Mechanism is **temporary** — only intended to be in place during 2026 and 2027.

It applies ONLY to an amount of capital equivalent to the original Genesis Capital provided by Sky to seed the Genesis Agent.

### While Active
- Genesis Capital counts towards Aggregate Backstop Capital
- Genesis Capital remains available to be reclaimed in an extreme SKY insolvency event

### Phase-out Logic

Genesis Capital is phased out over time by Genesis Agents that have launched liquid tokens with at least $10M in average daily volume.

**Phase-out calculation (at each Monthly Settlement):**

```
IF a Genesis Agent has had an actively launched token
   with average daily volume >= $10M during the past month
AND IF Aggregate Backstop Capital >= $50M
THEN the Genesis Agent phases out $1M of Genesis Capital

ADDITIONAL: +$1M phased out for every $10M of Aggregate Backstop Capital above $50M
```

**Example:**
- Two Genesis Agents with fully liquid tokens
- Aggregate Backstop Capital is $58M at Settlement
- Each phases out $1M (accounted for in Settlement)
- This reduces Aggregate Backstop Capital to $56M
- Next month: if ABC grows to $64M, each phases out $2M
- Following month: if ABC stays above $60M but below $70M, each phases out $2M again

**Key principle:** Total Genesis Capital can only go DOWN over time, eventually reaching full phase-out and removal of the mechanism.

---

## The Nine Genesis Agents

The planned number of Genesis Agents has been consolidated to simplify and accelerate the Genesis phase.

### Five Genesis Star Primes
1. **Spark** — Already capitalized
2. **Grove** — DeFi credit infrastructure
3. **Keel** — Ecosystem development
4. **Star 4** — Unannounced (Q1 2026)
5. **Star 5** — Unannounced (Q1 2026)

### One Genesis Institutional Prime
- **Obex** — Already capitalized

### Three Genesis Guardian Agents
Each slated to receive $25M in Genesis Capital (Guardian Agents are a Genesis Capital class, distinct from governance Guardians — see Glossary: Guardian Role Mapping)

**No other agents beyond this limited group will receive Genesis Capital.**

---

## Guardian Agent Capital Structure

Each of the three Guardian Agents receives $25M in Genesis Capital.

### Ring-fenced Buffers
Under the planned Ecosystem Accords:
- **$20M per agent** is ring-fenced as a Core Council and GovOps Support Buffer

### Spending Priority
The Core Council and GovOps Support Buffer must be spent entirely in support of general Sky Ecosystem development before Guardians may use internal capital for:
- Token buybacks
- Staking rewards

### Dual Use Before Spending
Before it is spent, the buffer can still be applied as Operational Risk Capital by the Guardian for its Guardian Accords.

### Two Goals of the Buffers

**1. Core Council Transition**
Provide resources for the Core Council to transition away from the current Genesis Phase Security and Maintenance Budget of 21%, without needing much financial support from Sky Frontier Foundation.

This enables SFF to invest more in longer-term revenue generating and cost reducing assets and technology.

**2. Bootstrap GovOps**
Bootstrap Operational GovOps capabilities without charging Guardian Accord Fees from Primes during the early Genesis Phase.

This gives GovOps teams and Guardians time to build service capabilities before negotiating medium-term Guardian Accords.

---

## The Path to 10% Maintenance Budget

### Current State
Genesis Phase Security and Maintenance Budget: **21% of Net Revenue**

### Target State
Post-genesis Security and Maintenance upper limit: **10%**

### Timeline
Transition expected before the end of 2026.

### Permanence
Once established, the 10% Security and Maintenance upper limit becomes **permanent and cannot be increased**.

### Impact
This promises a substantial boost to:
- Long-term profitability of Sky Ecosystem
- Immutability of the cost structure

---

## Current Estimates (Q1 2026)

| Metric | Estimate |
|--------|----------|
| Current Allocated Genesis Capital | Spark + Obex |
| Remaining to allocate | 7 agents |
| Projected total Allocated Genesis Capital | ~$120M |
| Projected Aggregate Backstop Capital (Q1) | $50-60M range |

---

## Summary

1. **Genesis Capital** is temporary capital deployed to bootstrap the agent ecosystem
2. **Aggregate Backstop Capital** is the safety net: Total Genesis Capital - Allocated Genesis Capital
3. **Insolvency defense hierarchy:** Backstop → SKY inflation → Genesis reclaim → USDS haircut
4. **Target:** $125M Aggregate Backstop Capital, achieved through 25% revenue retention
5. **Phase-out:** Genesis Capital decreases over time as agents launch liquid tokens
6. **Nine Genesis Agents:** 5 Star Primes + 1 Institutional Prime + 3 Guardians
7. **Guardian buffers:** $20M ring-fenced per Guardian for Core Council and GovOps support
8. **Maintenance budget:** Transitioning from 21% to permanent 10% cap by end of 2026

---

## Related Documents

| Document | Relationship |
|----------|--------------|
| [Whitepaper Part 6](../whitepaper/sky-whitepaper.md) | 7-step loss absorption waterfall (this doc's 4-level view is a simplified Genesis perspective) |
| [Appendix C — TMF](../whitepaper/appendix-c-treasury-management-function.md) | TMF mechanics — backstop target of 1.5% post-Genesis, revenue allocation waterfall |
| [`current-accounting.md`](current-accounting.md) | Core Council Buffer reclassification and current settlement cycle |
| [`../roadmap/roadmap-overview.md`](../roadmap/roadmap-overview.md) | Implementation phasing — Genesis Capital spans Phases 1–4 |
