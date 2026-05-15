# Synomic Entity Fees

**Status:** Live (rates and mechanics current)
**Last Updated:** 2026-05-10

---

## TL;DR

Sky Core captures revenue from every Synomic Entity that issues a governance token through a single unified rule:

| Component | Rate | Trigger |
|---|---|---|
| **Entity Creation Fee** | 5% of issued tokens to Sky Core | Any token issuance — genesis, distribution, fundraising, ecosystem incentives |
| **Entity Upkeep Fee** | 50 bps/yr of entity token market cap | Continuous accrual; settled at each settlement boundary |
| **Cross-Entity Upkeep Rebate** | Reduces upkeep owed | Continuous, proportional to other entities' tokens held |

**Tokenless entities pay neither fee.** Whether an entity type is tokenized determines fee exposure; rate and structure are uniform across all tokenized types.

---

## Section map

| § | Topic |
|---|---|
| 1 | Unified rule |
| 2 | Which entities have tokens |
| 3 | Cross-Entity Upkeep Rebate |
| 4 | Mechanics |
| 5 | Open questions |

---

## 1. Unified rule

**Any Synomic Entity with active governance tokens pays:**

- **5% Entity Creation Fee** — 5% of all governance tokens issued flow to Sky Core, paid in the entity's own tokens. Applies to every issuance event (genesis, team allocation, ecosystem incentives, fundraising rounds, restructuring), not just initial creation. For Type 1 Restructure (creator transfers assets into a new entity and receives tokens), the 5% is deducted from the creator's allocation: creator gets 95%, Sky Core gets 5%. See [`../synomic-entities/creation-restructuring.md`](../synomic-entities/creation-restructuring.md).
- **50 bps/yr Entity Upkeep Fee** — 50 basis points per year of the entity's governance-token market cap, accruing continuously and settled at each settlement boundary. Paid in the entity's own tokens.

**Tokenless entities pay neither fee.** No governance token, no fee exposure — by construction.

The rule is uniform: same rate, same mechanics, same denomination across every tokenized entity type. Sky Core's revenue from Entity Upkeep flows into Sky Core's gross revenue alongside USDS interest and Generator pass-through, ultimately feeding the [TMF waterfall](treasury-management.md). Reference Value calculations in growth-staking treat Entity Upkeep as a Sky Core revenue line — see [`../growth-staking/growth-staking.md`](../growth-staking/growth-staking.md) §4.2.

---

## 2. Which entities have tokens

Fee exposure is fully determined by whether an entity type is tokenized. The canonical mapping (see [`../synomic-entities/README.md`](../synomic-entities/README.md)):

| Entity type | Tokenized? | Notes |
|---|---|---|
| **Generator** | Yes | Foundational; USDS Generator and any future Generators issue governance tokens |
| **Prime** | Yes | Heavyweight capital allocators (Spark, Grove, Keel, Obex, etc.) |
| **Guardian** | Yes | Accountable, collateral-backed entities (Ozone is the operational Guardian) |
| **Pylon Entity** | Yes | Rank-2 broker-dealer analog with capital-weighted governance token; per-Ring pledge contributions to Ring assurance funds are accounted separately at the Pylon's primebook layer — see [`../synomic-entities/pylon-entity.md`](../synomic-entities/pylon-entity.md) |
| **Halo (governed)** | Yes | Halos with their own governance token |
| **Halo (minimal/simple)** | No | Halos that wrap value without issuing a separate governance token |
| **Folio** | No | Single principal owner; tokenless by definition |
| **Core Entity** | No | Direct Core Council operational vehicle — legacy-asset management and crisis-wrapper roles; no separate token |
| **Oracle Entity** | No | Domain-specific data provider; tokenless Core-Council operational vehicle |
| **Sequencer Entity** | No | Orderbook sequencer / matcher and Ring host; no collateral and no governance token; trust enforced by revocability rather than slashing |

Tokenless entities do not appear in Growth Staking valuations and generate no Entity Creation or Upkeep revenue for Sky Core. Where a tokenless entity earns its keep through other channels (e.g. usage fees from data consumers, maker-taker spreads), those are specified per-type in the entity's own document and are independent of the fee rule above.

---

## 3. Cross-Entity Upkeep Rebate

Tokenized entities that hold other entities' tokens receive a rebate on their own upkeep fee, incentivizing cross-entity investment and ecosystem cohesion.

| Property | Value |
|---|---|
| Mechanism | Proportional discount based on token holdings |
| Pricing | Conservative estimate of current market price (spread favors Sky) |
| Cap | Rebates cannot exceed 100% — best case is zero upkeep, never negative |
| Purpose | Drive cross-entity investment; align ecosystem economics |

### How rebates work

When an entity holds tokens of another entity, the value of those holdings (priced conservatively) offsets the entity's own upkeep liability:

```
holdings_value (conservative)
   = sum over (held_token i) of:
       quantity_held_i × conservative_price_i

rebate_credit = holdings_value × upkeep_rate
              = holdings_value × 0.005

upkeep_after_rebate = max(0, gross_upkeep − rebate_credit)
```

The conservative pricing means the rebate value is calibrated below live market mid, with the spread accruing to Sky as additional protocol revenue. An entity with sufficient holdings can reduce upkeep to zero; it cannot earn negative upkeep (rebates do not become income).

### Why this matters

The rebate pulls tokenized entities toward holding each other's tokens, which:

- **Increases ecosystem cohesion** — every entity has economic interest in the success of others
- **Supports cross-entity capital flows** — Primes holding Halo tokens, Guardians holding Prime tokens, and so on
- **Aligns with Growth Staking** — entities with deep cross-holdings are simultaneously more capital-efficient (zero upkeep) and serve as growth-asset holders that improve their own staking factor (per [`../growth-staking/growth-staking.md`](../growth-staking/growth-staking.md))
- **Captures spread for Sky** — conservative pricing makes the rebate game-theoretically generate revenue even as it incentivizes the desired behavior

### Worked example

A Star Prime with the following profile:

```
Token market cap:       $X (10B PRIME × PRIME conservative price)
Annual gross upkeep:    market_cap × 0.005 (paid in PRIME tokens)

Holdings:
  - 200M GROVE tokens (conservative price: $0.04)
  - 50M HALO-X tokens (conservative price: $0.10)

Holdings value (conservative):
  = 200M × $0.04 + 50M × $0.10
  = $8M + $5M
  = $13M USD-equivalent

Rebate credit:
  = $13M × 0.005
  = $65,000 USD-equivalent

Net upkeep:
  Gross    = market_cap × 0.005, paid in PRIME
  Rebate   = subtract $65K equivalent
  Owed     = remaining (in PRIME)
```

The Prime's effective upkeep load drops by the dollar-value of the rebate credit.

---

## 4. Mechanics

**Denomination.** Both the Creation Fee and the Upkeep Fee are paid in the entity's own governance tokens, not in USDS. Sky Core receives entity tokens directly, which it can hold, stake, use to claim Cross-Entity Upkeep Rebates, or sell over time.

**Market-cap valuation for upkeep.** Upkeep is assessed against the entity's governance-token market cap using the same conservative-pricing methodology that governs the rebate (mid-of-window, oracle-attested where available, with anti-manipulation windowing). Conservative pricing protects Sky Core against settlement-window manipulation in either direction: the spread between conservative and live mid accrues to Sky as additional revenue on the upkeep side, mirroring the rebate side.

**Cadence.** Upkeep accrues continuously and is realized at each settlement boundary (currently monthly in Phase 1; daily once Phase 2 LCTS settlement is live). Creation Fees are realized at the issuance event itself — the 5% slice mints alongside the rest of the issuance and routes to Sky Core in the same transaction.

**Revenue routing.** Upkeep, the spread captured via conservative pricing, and Creation Fee token receipts all flow into Sky Core's gross revenue and feed the [TMF waterfall](treasury-management.md). Creation Fee tokens are tracked separately in growth-staking accounting as Sky Special revenue (per [`../growth-staking/growth-staking.md`](../growth-staking/growth-staking.md) §4.2).

---

## 5. Open questions

- **Conservative-pricing oracle source and window.** The exact oracle, lookback window, and aggregation rule for "conservative price" is finalized at the framework level but not yet pinned to a specific implementation. Tracked in the rate-limit / oracle technical specs.
- **Rebate eligibility for tokenless holders.** A tokenless entity (e.g. Core Entity holding Prime tokens during a busted-prime wrap) has no upkeep liability against which to apply a rebate; whether holdings should generate any other credit is unspecified.

---

## File map

| Doc | Relationship |
|---|---|
| [`README.md`](README.md) | Accounting directory index |
| [`treasury-management.md`](treasury-management.md) | Entity fees feed Sky Core gross revenue, which enters the TMF waterfall |
| [`distribution-rewards.md`](distribution-rewards.md) | Sky's payments to Primes (opposite-direction flow) |
| [`../growth-staking/growth-staking.md`](../growth-staking/growth-staking.md) | Reference Value calculations include entity upkeep as revenue; cross-entity holdings double as growth assets |
| [`../synomic-entities/creation-restructuring.md`](../synomic-entities/creation-restructuring.md) | Type 1 / Type 2 Restructure events trigger the Creation Fee |
| [`../synomic-entities/README.md`](../synomic-entities/README.md) | Tokenized vs tokenless entity types |
| [`../synomic-entities/pylon-entity.md`](../synomic-entities/pylon-entity.md) | Pylon Entity spec (tokenized; falls under unified rule) |
| [`../synomic-entities/oracle-entity.md`](../synomic-entities/oracle-entity.md) | Oracle Entity spec (tokenless; pays no fee) |
| [`../synomic-entities/sequencer-entity.md`](../synomic-entities/sequencer-entity.md) | Sequencer Entity spec (tokenless; pays no fee) |
| [`../synomic-entities/core-controlled.md`](../synomic-entities/core-controlled.md) | Core Entity — legacy management role (tokenless) |
| [`../synomic-entities/recovery.md`](../synomic-entities/recovery.md) | Core Entity — crisis-wrapper role (tokenless) |

---

## One-line summary

**Any Synomic Entity with active governance tokens pays a 5% Entity Creation Fee at issuance and a 50 bps/yr Entity Upkeep Fee on token market cap, both denominated in the entity's own tokens, with a Cross-Entity Upkeep Rebate that incentivizes mutual holdings and captures spread for Sky via conservative pricing; tokenless entities pay neither.**
