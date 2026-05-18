# Folio Agents

**Status:** Draft
**Date:** February 2026

---

## Overview

A folio is the standardized supply-side holding structure in the Sky ecosystem. It is simultaneously:

- **An on-chain agent** — a smart contract stack built on the PAU pattern (Controller + ALMProxy + RateLimits), with its own teleonome, operating within the same audited architecture as every other agent in the ecosystem
- **Connected to legal entities** — linked to one or more legal entities that the principal controls, usually following standardized best-practice patterns developed by the ecosystem
- **A risk-managed position** — inheriting structural risk protection from the Laniakea infrastructure (rate limits, beacon framework, break-glass provisions) and, for automated folios, the full sentinel formation stack

Folio Agents are rank 3 agents, administered by a Prime and transitively accordant to that Prime's Guardian.

---

## The Principal

Every folio has a **principal** — the person or entity whose folio it is. The principal is the end user, the owner, the one whose capital is at stake and whose strategic intent the folio serves.

The principal's primary instrument of control is the **directive** — human language instructions that define the folio's investment philosophy, risk appetite, strategic priorities, and constraints. In an automated folio, the directive is what GovOps and the baseline sentinel follow. In a principal control folio, the principal executes on their own directive directly.

---

## Two Operating Modes

There are two fundamentally different modes of folio operation — **automated** and **principal control** — distinguished by who operates the folio agent day-to-day.

### Automated Folio

The automated folio is the hands-off path. It reuses exactly the same sentinel formation pattern that operates Primes and Halos.

The principal enters a guardian accord. The guardian operates a **folio baseline sentinel** on the principal's behalf, and a stream operator runs a **folio stream sentinel** that actively manages capital deployment. One or more independent **warden sentinels** provide defense against the baseline going rogue. The result is the same baseline/stream/warden formation that protects Primes — now protecting the folio.

The principal's only active responsibility is writing and maintaining the **directive**. The sentinel formation executes within the boundaries the directive sets.

**Protection:** An automated folio principal receives the same state-of-the-art security as institutional-scale Prime capital. The baseline sentinel runs public, auditable code. The stream can influence strategy but cannot execute directly. The wardens independently monitor for rogue behavior and can halt operations. Rate limits bound worst-case damage.

### Principal Control Folio

The principal control folio is the hands-on path. The principal themselves operates a **principal sentinel** — directly controlling their folio agent without any guardian accord, baseline service, or GovOps intermediary.

The principal deploys their own algorithms, makes their own trading decisions, and manages their own positions directly through the folio agent's PAU. They still operate within rate limits — but they also have the freedom to change those rate limits through whatever governance mechanism they choose to set up.

**Who does this:** This mode is for highly competent operators. In practice, the primary users of principal control folios are expected to be companies that themselves run stream sentinels for other primes, halos, and folios. They have the infrastructure, the expertise, and the algorithms to operate autonomously.

**Trade-off:** More power, less protection. No baseline fail-safe, no stream/warden formation, no guardian collateral backing. The principal is responsible for their own security and risk management. The PAU architecture still provides structural protection (rate limits, standardized interfaces, audited contracts), but the formation-level protections are absent.

### Shared Capabilities

Both automated and principal control folios share core capabilities through their sentinel interface:

- **Monitor** — real-time visibility into positions, exposures, P&L, risk metrics across every strategy the folio participates in
- **Trade** — enter and exit Prime strategies, allocate to Halo products, rebalance across positions. All through a unified interface, all within rate limits
- **Alert** — threshold breaches, counterparty events, strategy performance deviations — surfaced before they become problems

The difference is who exercises these capabilities: in an automated folio, the sentinel formation does it on the principal's behalf according to the directive. In a principal control folio, the principal does it themselves through their principal sentinel.

---

## Key Properties

| Property | Description |
|---|---|
| **Rank** | 3 — administered by a Prime, transitively accordant to that Prime's Guardian |
| **Creation** | Instant; any SKY holder can create one |
| **Contains** | PAU holding staked SKY + growth assets + strategy positions |
| **Token issuance** | None — Folio Agents are tokenless |
| **Halo Units** | None — not a Halo, does not issue Units or shares |
| **Governance tokens** | None — single owner (the principal), not governed by token holders |
| **Control** | Automated (sentinel formation via guardian accord) or Principal Control (principal sentinel, direct) |
| **Restructuring** | Can perform Type 1 Restructure only (create new Halo or Prime from assets) |

---

## How Folio Agents Differ from Halos

Folio Agents are **not** a type of Halo. The structural difference is fundamental — the entity relationship is inverted:

| Property | Halo | Folio Agent |
|---|---|---|
| **Relationship to legal entity** | Halo wraps around a legal entity — Halo is the outer shell | Folio is controlled BY the principal through legal entities — the principal's legal structure is the governance surface |
| **Token issuance** | Can issue governance tokens | No token issuance |
| **Halo Units** | Issues Units (liability-side claims) | No Units |
| **Governance** | Token holder governance via Root Edit | Single owner (principal) control via directive |
| **Creation** | Requires Guardian Accord + governance process | Instant creation |
| **Rank** | 3 (same rank, different type) | 3 |
| **Operation** | LPHA beacons or sentinel formations | Automated (sentinel formation) or principal sentinel |

A Halo is an autonomous institutional entity that wraps value and gives it agency. A folio is a personal holding structure — a PAU controlled by its principal, used for capital deployment, staking, and portfolio management.

---

## Legal Structure: The Principal's Governance Surface

The folio inverts the usual agent-entity relationship. For Primes and Halos, the agent controls its legal entities — the entity structure serves the agent's operations. For folios, the principal controls the folio agent *through* legal entities — the entity structure is the principal's governance surface.

The ecosystem develops standardized best-practice legal structures that principals can adopt. Principals can adopt the ecosystem's standardized legal structures as-is (cheapest, fastest) or use their own structures (more flexibility, more cost). Either way, the on-chain layer works the same.

---

## Growth Staking

Folio Agents are the required vehicle for Growth Staking participation. The folio's PAU holds both staked SKY and a portfolio of growth assets. For the complete Growth Staking mechanism — including growth factor values, reward scaling, agent token valuation, and compounding mechanics — see [Growth Staking](../../growth-staking/growth-staking.md).

The folio can reinvest rewards automatically:

1. **When SF capacity exists** (growth assets support more SKY than currently staked) — use rewards to acquire more SKY and stake it inside the folio
2. **When at SF capacity** (no room for additional SKY without more growth assets) — use rewards to acquire growth assets, expanding capacity for future SKY compounding

A sentinel can automate this cycle, optimizing the balance between SKY accumulation and growth asset acquisition based on current SF utilization.

---

## Architecture

```
┌─────────────────────────────────────┐
│           Folio Agent               │
│                                     │
│  ┌───────────────────────────────┐  │
│  │             PAU               │  │
│  │                               │  │
│  │  Staked SKY: 100,000 SKY     │  │
│  │                               │  │
│  │  Growth Assets:               │  │
│  │    SPK:         $30,000       │  │
│  │    GROVE:       $10,000       │  │
│  │    Spark TEJRC: $15,000       │  │
│  │                               │  │
│  │  Pending Rewards: ...         │  │
│  └───────────────────────────────┘  │
│                                     │
│  Control: Principal Sentinel or     │
│           Sentinel Formation        │
│  Directive: Principal's intent      │
└─────────────────────────────────────┘
```

- **Creation** — Instant. Any SKY holder can create a Folio Agent at any time.
- **PAU** — The folio's internal Parallelized Allocation Unit holds staked SKY, growth assets, and strategy positions.
- **Reward distribution** — At each daily settlement, the system measures the total staking factor of assets inside the PAU and airdrops the corresponding staking reward.
- **Control** — Automated folio: sentinel formation operates on behalf of the principal according to the directive. Principal control folio: the principal operates directly via their principal sentinel.
