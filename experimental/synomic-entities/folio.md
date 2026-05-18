# Folio

A folio is the standardized supply-side holding structure in the Sky ecosystem — simultaneously an on-chain agent (PAU-based, with its own teleonome) and a principal-controlled vehicle linked to legal entities the principal holds. Folios are rank-3 agents administered by a Prime and transitively accordant to that Prime's Guardian.

For Synomic Entity theory, see [`../macrosynomics/synomic-entities.md`](../macrosynomics/synomic-entities.md). For the sentinel-formation patterns folios share with Primes / Halos (Baseline / Stream / Warden / Principal), see [`../sentinel/sentinel-network.md`](../sentinel/sentinel-network.md).

---

## Properties

| Property | Description |
|---|---|
| **Rank** | 3 — administered by a Prime, transitively accordant to that Prime's Guardian |
| **Creation** | Instant; auto-accord (any SKY holder can create one) |
| **Contains** | PAU holding staked SKY + growth assets + strategy positions |
| **Token issuance** | None — folios are tokenless |
| **Halo Units** | None — not a Halo, does not issue Units or shares |
| **Governance tokens** | None — single owner (the principal) |
| **Control** | Automated (operating setup — baseline-relay + warden-relay + stream-sentinel — via Guardian Accord) or Principal Control (principal-sentinel, direct) |
| **Restructuring** | Type 1 only (create new Halo or Prime from assets) — see [`creation-restructuring.md`](creation-restructuring.md) |

---

## The Principal and the Directive

Every folio has a **principal** — the person or entity whose folio it is. The principal's primary instrument of control is the **directive** — human-language instructions that define the folio's investment philosophy, risk appetite, strategic priorities, and constraints.

In an automated folio, the directive is what GovOps and the baseline-relay follow. In a principal-control folio, the principal executes on their own directive directly.

---

## Two Operating Modes

### Automated Folio

Hands-off path. Reuses the same operating setup that operates Primes and Halos: baseline-relay + warden-relay + stream-sentinel, deployed together.

| Component | Role |
|---|---|
| **baseline-{folio}** (relay) | Baseline — public, auditable execution rules; config in `&entity.folio.{owner}.relay.baseline` |
| **stream-{folio}-{actor}** (stream-sentinel) | Stream — proprietary intelligence streaming intent; config in `&entity.folio.{owner}.sentinel.{actor}` |
| **warden-{folio}-{operator}** (relay) | Warden(s) — independent monitoring with halt authority; config in `&entity.folio.{owner}.relay.warden.{operator}` |

The principal enters a Guardian Accord. The Guardian operates the baseline-relay on the principal's behalf, and a Stream operator runs the stream-sentinel for active capital deployment. Wardens defend against the baseline-relay going rogue.

The principal's only active responsibility is writing and maintaining the directive. The setup executes within the directive's bounds.

**Protection:** Same state-of-the-art security as institutional-scale Prime capital — public baseline rules, intent-only stream-sentinel, independent warden-relays, rate-limited PAU bounds, TTS-priced ORC. See [`../sentinel/sentinel-network.md`](../sentinel/sentinel-network.md) for the operating-setup spec.

### Principal Control Folio

Hands-on path. The principal operates a **principal-sentinel** — directly controlling the folio's PAU without any Guardian Accord, baseline-relay service, or GovOps intermediary.

| Identifier | Role |
|---|---|
| **principal-{owner}** (principal-sentinel) | Standalone principal-sentinel (no operating setup) |

The principal deploys their own algorithms, makes their own trading decisions, and manages their own positions through the folio's PAU. Rate limits still apply, but the principal can modify them through whatever governance mechanism they set up.

**Trade-off:** More power, less protection. The PAU still provides structural protection (rate limits, audited contracts), but setup-level protections (baseline-relay fail-safe, stream-sentinel / warden-relay monitoring, Guardian collateral) are absent.

**Expected users:** Companies that already run stream-sentinels for other Primes / Halos / Folios — they have the infrastructure, expertise, and algorithms to operate autonomously.

---

## Shared Capabilities

Both modes share core capabilities through their operating interface:

- **Monitor** — real-time visibility into positions, exposures, P&L, risk metrics
- **Trade** — enter and exit Prime strategies, allocate to Halo products, rebalance
- **Alert** — threshold breaches, counterparty events, performance deviations

The difference is who exercises these: in an automated folio, the operating setup does it on the principal's behalf according to the directive; in a principal-control folio, the principal does it themselves.

---

## How Folios Differ from Halos

Folios are **not** a type of Halo. The structural difference is fundamental — the entity relationship is inverted:

| Property | Halo | Folio |
|---|---|---|
| **Relationship to legal entity** | Halo wraps around a legal entity — Halo is the outer shell | Folio is controlled BY the principal through legal entities — the principal's legal structure is the governance surface |
| **Token issuance** | Can issue governance tokens | None |
| **Halo Units** | Issues Units (liability-side claims) | None |
| **Governance** | Token-holder governance via Root Edit | Single-owner principal control via directive |
| **Creation** | Requires Guardian Accord + governance | Instant via auto-accord |
| **Operation** | Relay beacons + sentinels (operating setup) | Automated operating setup or principal-sentinel |

A Halo is an autonomous institutional entity that wraps value and gives it agency. A folio is a personal holding structure — a PAU controlled by its principal, used for capital deployment, staking, and portfolio management.

---

## Legal Structure

The folio inverts the usual agent-entity relationship. For Primes and Halos, the agent controls its legal entities — the entity structure serves the agent. For folios, the principal controls the folio agent *through* legal entities — the entity structure is the principal's governance surface.

The ecosystem develops standardized best-practice legal structures principals can adopt as-is (cheapest, fastest), or principals can use their own (more flexibility, more cost). Either way, the on-chain layer works the same.

---

## Growth Staking

Folios are the required vehicle for Growth Staking participation. The folio's PAU holds both staked SKY and a portfolio of growth assets. For the full mechanism (growth-factor values, reward scaling, agent-token valuation, compounding mechanics), see [`../growth-staking/growth-staking.md`](../growth-staking/growth-staking.md).

The folio can reinvest rewards automatically:

1. **When SF capacity exists** — use rewards to acquire more SKY and stake it
2. **When at SF capacity** — use rewards to acquire growth assets, expanding capacity for future SKY compounding

A baseline-relay can automate this cycle, optimizing the SKY/growth-assets balance based on current SF utilization.

---

## Architecture

```
┌─────────────────────────────────────┐
│              Folio                   │
│                                      │
│  ┌───────────────────────────────┐   │
│  │             PAU               │   │
│  │                               │   │
│  │  Staked SKY:    100,000 SKY   │   │
│  │                               │   │
│  │  Growth Assets:               │   │
│  │    SPK:         $30,000       │   │
│  │    GROVE:       $10,000       │   │
│  │    Spark TEJRC: $15,000       │   │
│  │                               │   │
│  │  Pending Rewards: ...         │   │
│  └───────────────────────────────┘   │
│                                      │
│  Control: principal-sentinel or      │
│           operating setup            │
│  Directive: principal's intent       │
└──────────────────────────────────────┘
```

- **Creation** — Instant. Any SKY holder can create a folio.
- **PAU** — The folio's internal Parallelized Allocation Unit holds staked SKY, growth assets, and strategy positions.
- **Reward distribution** — At each daily settlement, the system measures the total staking factor of assets inside the PAU and airdrops the corresponding staking reward.
- **Control** — Automated: operating setup (baseline-relay + warden-relay + stream-sentinel) according to directive. Principal control: principal operates directly via principal-sentinel.

---

## Related

- [`README.md`](lani/synomic-entities/README.md) — Rank hierarchy
- [`prime.md`](prime.md) — Type 1 Restructure target (folio → Prime)
- [`halo-classes.md`](halo-classes.md) — Halos that folios allocate to
- [`creation-restructuring.md`](creation-restructuring.md) — Folio auto-accord; Type 1 Restructure
- [`../sentinel/sentinel-network.md`](../sentinel/sentinel-network.md) — Operating-setup pattern (baseline-relay / warden-relay / stream-sentinel / principal-sentinel)
- [`../noemar-synlang/synlang-patterns.md`](../noemar-synlang/synlang-patterns.md) §6 — Synlang substrate of operating-setup patterns
- [`../synoteleonomics/recipe-marketplace.md`](../synoteleonomics/recipe-marketplace.md) — Streaming Accord as recipe instance
- [`../growth-staking/growth-staking.md`](../growth-staking/growth-staking.md) — Growth Staking mechanism
