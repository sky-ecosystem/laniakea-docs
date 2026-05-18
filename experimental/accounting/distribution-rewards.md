# Distribution Rewards, Structural Demand Resource Rewards, Pioneer Star System

**Status:** Target incentive system; DR/SDRR/tagging are not P1 synome functionality. SDRR activates with real SDR auctions that pay reservation fees.
**Last Updated:** 2026-05-17

---

## TL;DR

Three Sky-funded incentive mechanisms drive USDS adoption and route value to Primes that source demand:

| Mechanism | What it pays for | How |
|---|---|---|
| **Distribution Rewards (DR)** | Driving USDS / sUSDS adoption | Tiered token rewards (0/10/20/50 bps) routed to Primes based on tagged USDS balances and product branding |
| **Structural Demand Resource Rewards (SDRR)** | Sourcing sticky USDS demand that produces SDR for matched asset deployment | 2/3 of SDR bucket fees to the tagging Prime, 1/3 to Sky |
| **Pioneer Star System** | Star Primes leading USDS expansion to new chains | 3-year exclusive Pioneer Phase per chain — auto-tagging, Pioneer Rewards, Unbalanced Supply Fee authority |

In the target system, DR and SDRR are paid out at each settlement cycle. The Pioneer Star System is a separate set of privileges available only to **Star Primes** (the five genesis-named Primes: Spark, Grove, Keel, skybase, launch6). The Institutional Prime (Obex) does not participate in the Pioneer System.

---

## Section map

| § | Topic |
|---|---|
| 1 | Distribution Rewards — the four-tier system |
| 2 | Tagging mechanism and ownership |
| 3 | Structural Demand Resource Rewards |
| 4 | Pioneer Star System |
| 5 | Pioneer Star — Unbalanced Supply Fee |

---

## 1. Distribution Rewards — the four-tier system

DR rewards Primes for sourcing USDS / sUSDS adoption. Rewards are tiered by how strongly the distribution channel builds long-term demand-side moat — direct branded holding earns the most; opaque integrations earn nothing.

| Tier | Rate | Criteria |
|---|---|---|
| **0** | No DR | Excluded / ineligible addresses |
| **1** | 0 bps | Untagged addresses (tracked but unpaid; can still earn SDRR) |
| **2** | 10 bps | Unbranded complex products with <90% sUSDS backing |
| **3** | 20 bps | Branded USDS products **OR** unbranded with ≥90% sUSDS backing |
| **4** | 50 bps | Direct USDS / sUSDS holding with clear Sky branding (Boosted DR) |

Rates are annualized and accrue continuously based on the tagged balance.

### Tier 2 — Unbranded complex products

A wrapper or composed product that:

- Does **not** use "USDS" in its name
- Is backed by mixed collateral with **<90% sUSDS** content

Example: a "StarUSD" containing various stablecoins as collateral, including some sUSDS but mostly other assets.

### Tier 3 — Branded or high-backing products

Two paths qualify for Tier 3:

| Path | Requirements | Example |
|---|---|---|
| **3a (branded)** | Uses "USDS" in product name **AND** subscribe/redeem currency is USDS | "StarUSDS" |
| **3b (high backing)** | Unbranded but **≥90% backed by sUSDS** | "StarUSDT" with 90%+ sUSDS backing |

### Tier 4 — Boosted Distribution Rewards

- Direct holding of USDS or sUSDS (no wrapper)
- Clear Sky branding on the frontend or product surface

This creates the strongest demand-side moat — users see "USDS" and choose it directly. Highest reward rate.

### Distribution to Primes

**Primes receive DR; how they share with integrators is each Prime's own choice.** There is no enforced split between Prime and the front-end / integration partner — each Prime determines its own integrator economics. This means a Prime can keep all DR or pass most of it through, depending on how they structure partnerships.

---

## 2. Tagging mechanism and ownership

Tagging associates a USDS / sUSDS balance with a Prime for DR purposes.

### Tag types

| Method | How |
|---|---|
| **On-chain** | Codes embedded in transactions by frontends or smart contracts |
| **Off-chain** | Verified by a Guardian and accordant GovOps |

### Ownership rules

| Property | Value |
|---|---|
| Tagging term | 10 years from tagging |
| Retagging | Last tagger owns the entire account (replaces prior tag) |
| Transferability | Tags are non-transferable; cannot be sold |

Tag ownership rules — particularly last-tagger-wins — are subject to refinement; this is the working specification. When a tagged address is retagged by a different Prime, the new Prime captures all subsequent DR for the 10-year period from the retag.

---

## 3. Structural Demand Resource Rewards

SDRR rewards Primes that source **tagged USDS demand feeding into the SDR system**. Where DR rewards adoption (any USDS held by an end user), SDRR rewards adoption that produces sticky structural demand that matches against long-maturity assets.

| Property | Value |
|---|---|
| Purpose | Compensate Primes for sourcing SDR capacity (sticky USDS demand) |
| Eligibility | Tagged USDS that sits in SDR Buckets |
| Distribution split | **2/3 to tagging Prime, 1/3 to Sky** (initial setting, subject to governance) |

### How it works

1. USDS accounts accrue lot age over time and land in [SDR Buckets](../risk-framework/sdr-model.md) based on their measured holding age and Lindy SDR treatment.
2. Primes that have tagged those USDS accounts earn a proportional share of the bucket's underlying demand.
3. When a Prime pays fees to reserve SDR capacity, their reservation **tugs** on buckets to match their need (the tug-of-war mechanism in [`sdr-auction.md`](sdr-auction.md)).
4. Fees flow back to whoever tagged the USDS that actually got tugged — not just the bucket the reservation initially targeted.

### Dynamic matching

Bucket contents change over time as USDS accounts accrue or lose lot age. When a Prime reserves capacity:

- They may tug on **nearby buckets** if their target lacks sufficient capacity
- Fee distribution follows the **actual tugging**, not the original reservation target
- This ensures rewards always flow to Primes whose tagged demand is actually being matched

### Worked example

```
Setup:
  Prime B reserves capacity targeting Bucket 42
  Bucket 42 has $100M USDS; Prime A has tagged $30M (30% of bucket)
  Prime B pays $1M in capacity fees, of which $400K is attributed to Bucket 42

Distribution:
  Prime A's share = 30% × (2/3) × $400K = $80K
  (Plus any share from adjacent buckets if Prime A tagged demand there)
  Sky's share    = 1/3 × $400K = $133K
  Other 2/3 distributed across all tagging Primes pro-rata to their bucket share
```

### Tier 1 + SDRR

Even **Tier 1 (0 bps DR)** tagged addresses can earn SDRR. This lets Primes benefit from demand-side contributions without requiring full branding or composition requirements — a generic USDS holder that happens to be sticky still produces value when matched against long-maturity assets.

---

## 4. Pioneer Star System

The Pioneer Star System enables **Star Primes only** to gain exclusive advantages when expanding USDS to new blockchains. This is not available to the Institutional Prime.

| Property | Value |
|---|---|
| Eligibility | Star Primes (Spark, Grove, Keel, skybase, launch6) |
| Purpose | Incentivize cross-chain expansion with first-mover advantages |
| Phase term | 3-year Pioneer Phase per Pioneer Chain |
| Exclusivity | One Pioneer Star per chain; Stars can have multiple Pioneer Chains |

### Pioneer Chains and Pioneer Stars

A **Pioneer Chain** is any blockchain integrating USDS for the first time. A **Pioneer Star** is the Star Prime designated by the chain's official team or foundation to lead the USDS rollout.

### Designation process

1. Written confirmation from the Pioneer Chain's official team / foundation
2. The Star's governance verifies intention to accept Pioneer Status
3. Core Council reviews strategic alignment with Sky Ecosystem growth
4. If approved, the 3-year Pioneer Phase begins

### Pioneer Phase benefits

#### (a) Distribution Reward auto-tagging

| Property | Value |
|---|---|
| During Pioneer Phase | Pioneer Star auto-tags all untagged USDS / sUSDS accounts on the chain |
| At Phase end | One-time permanent tag of remaining untagged balances |
| Tagging term | 10 years (unless retagged by another Star) |
| Boosted DR | Not available on auto-tags; only on explicitly tagged + branded addresses |

The auto-tag is a "default" Tier 1 or Tier 3 tag depending on context; Boosted DR (Tier 4) requires the explicit branded direct-holding criteria, not just auto-tagging.

#### (b) Pioneer Rewards

| Property | Value |
|---|---|
| Source | SSR × Unrewarded USDS balance on Pioneer Chain |
| Cadence | Paid at each settlement cycle |
| Recipient | Pioneer Star's SubProxy (as income) |

"Unrewarded USDS" = bridged USDS that is **not** earning SSR through sUSDS, Integration mechanisms, or holdings in other Synomic Entities. The Pioneer Star earns SSR-equivalent on this otherwise-idle balance for the Pioneer Phase term.

#### (c) Unbalanced Supply Fee Authority

The Pioneer Star can charge fees to other Stars that allocate supply to the Pioneer Chain without contributing to demand on it — see §5 below.

### De-designation

If a Pioneer Star fails to meet expectations recorded in an Ecosystem Accord, the Pioneer Chain team / foundation can:

- De-designate the current Pioneer Star, **or**
- Transfer designation to a different Star Prime

When de-designated, the 3-year clock pauses. A future Pioneer Star continues from where the previous one stopped, not from zero.

---

## 5. Pioneer Star — Unbalanced Supply Fee

A Pioneer Star can charge other Stars that deploy capital into the Pioneer Chain without contributing matching demand.

| Property | Value |
|---|---|
| Fee rate | 20 bps per year |
| Applies to | Unbalanced supply (USDS-backed collateral / liquidity not matched by demand) |
| Purpose | Protect supply / demand balance on the Pioneer Chain |

### Balancing mechanisms

To avoid the fee, an allocating Star can balance their supply through:

| Mechanism | Offset Ratio |
|---|---|
| **Tagging Demand** | 1:1 — every $1 of tagged USDS demand offsets $1 of supply |
| **ASC Liquidity** | 3× average daily trading volume counts as demand |

Direct demand (tagged USDS holdings) is most efficient; ASC contributions count too because they support the local market.

### Exemptions

The Pioneer Star or Pioneer Chain team can grant **exemptions** to specific Stars via an Ecosystem Accord. Once granted, exemption terms cannot be revoked if the exempted Star made significant investments based on them — this prevents bait-and-switch.

---

## File map

| Doc | Relationship |
|---|---|
| [`README.md`](lani/accounting/README.md) | Accounting directory index |
| [`entity-fees.md`](entity-fees.md) | Sky → Entity revenue (opposite direction from DR/SDRR/Pioneer Rewards) |
| [`treasury-management.md`](treasury-management.md) | DR / SDRR / Pioneer Rewards are paid from Sky's gross revenue before it enters the TMF waterfall |
| [`sdr-auction.md`](sdr-auction.md) | SDR Bucket reservation and tug-of-war that SDRR distributes fees from |
| [`../risk-framework/sdr-model.md`](../risk-framework/sdr-model.md) | Lindy SDR algorithm and SDR Buckets that house tagged USDS |
| [`../synomic-entities/prime.md`](../synomic-entities/prime.md) | Star Primes (Spark, Grove, Keel, skybase, launch6) and Institutional Prime (Obex) |
| [`../synomic-entities/generator.md`](../synomic-entities/generator.md) | USDS Generator that issues the assets DR/SDRR rewards adoption of |
| [`../risk-framework/asc.md`](../risk-framework/asc.md) | ASC liquidity that counts toward Pioneer Chain supply balancing |

---

## One-line summary

**Distribution Rewards pay Primes for USDS adoption in tiers from 0 to 50 bps based on branding and sUSDS backing; Structural Demand Resource Rewards split SDR bucket fees 2/3 to the Prime that tagged the sticky USDS demand and 1/3 to Sky; the Pioneer Star System gives the 5 Star Primes 3-year exclusive privileges per chain they lead USDS expansion onto, including auto-tagging, SSR-equivalent rewards on unrewarded USDS, and authority to charge other Stars 20 bps/year on unbalanced supply to protect chain-level supply/demand balance.**
