# Tranching

**Status:** Draft (Phase 2 conceptual core, 2026-05-05)

How loss propagates through seniority structures. Defines the exoasset/exoliab vocabulary, the senior/junior/equity tranche pattern, and the waterfall semantics. The unification mechanism that lets Sparklend loans, NFAT facilities, JAAA holdings, and ABF deals all express as the same primitive.

Companion to:
- `book-primitive.md` — the 6-tuple where tranches live as one component
- `risk-decomposition.md` — the risk types whose forced-loss math runs through tranche waterfalls
- `currency-frame.md` — frames apply to tranche denominations

---

## TL;DR

Tranches are ordered claims on a book's assets, with **seniority** defining loss-absorption order. Loss waterfalls absorb to the most-junior (equity) tranche first, eat through it, then move up to the next tranche.

Two flavors of "exo" (external-to-the-synome):
- **Exoasset** — terminal asset held but not controlled (ETH, USDC, T-bills)
- **Exoliab** — tranche held by an external party (borrower equity, third-party debt) [NEW vocabulary]

Anything overcollateralized — Sparklend loans, NFAT facilities, CLO tranches, ABF deals — expresses as a tranched exobook. The holder's risk = asset-stress propagated through the tranche structure. **Gap risk disappears as a separate concept**; what remains is the same forced-loss math applied uniformly.

---

## Section map

| § | Topic |
|---|---|
| 1 | Tranches as ordered claims |
| 2 | Exoassets and exoliabs |
| 3 | Loss propagation through the waterfall |
| 4 | Tranche rights schema (P + T) |
| 5 | Re-framing of overcollateralized lending |
| 6 | Why gap risk disappears |
| 7 | One-line summary |

---

## 1. Tranches as ordered claims

A tranche is a claim on a book's assets, with four load-bearing properties:

| Property | What it specifies |
|---|---|
| **Seniority** | Position in the loss-absorption order. Lower number = more junior = absorbs first. |
| **Holder** | Who owns the claim. May be internal (another synome book) or external (exoliab). |
| **Notional** | Claim amount. May be static or rule-determined (per `book-primitive.md` §3). |
| **Denomination** | The instrument the claim is paid in (USD, USDC, ETH, etc.). |

Tranches are ordered. There's always exactly one **equity tranche** (most-junior, seniority 0). Senior tranches sit above it. Some books have only two tranches (senior + equity); structured products may have many.

```metta
(exo-book sparklend-eth-pool-001
   (category overcollateralized-eth-lending))

(exo-book-asset sparklend-eth-pool-001 eth 1000)         ; 1000 ETH

(exo-book-tranche sparklend-eth-pool-001
   (seniority 0)
   (holder borrower-XYZ)                                  ; exoliab
   (notional 750000)
   (denom usd))                                           ; equity tranche

(exo-book-tranche sparklend-eth-pool-001
   (seniority 1)
   (holder spark-halo-A)                                  ; internal
   (notional 1750000)
   (denom usd))                                           ; senior tranche
```

---

## 2. Exoassets and exoliabs

Two kinds of "exo" — both refer to entities outside synome control:

| Term | What it is | Examples |
|---|---|---|
| **Exoasset** | Terminal asset held but not controlled by synome | ETH, BTC, USDC, T-bills, real-world cash |
| **Exoliab** | Tranche claim held by an external party | Borrower equity in an overcollateralized loan; third-party debt; equity tranche of an external structured product; sponsor retention in a CLO |

Why exoliabs matter: many useful financial structures involve a **junior cushion held by someone outside synome**. The synome doesn't track that party's full state — but it does track the cushion size, because that's what protects the synome's senior claim.

Example: in a Sparklend ETH loan, the borrower holds the junior (equity) tranche. The synome doesn't model the borrower's other assets, balance sheet, or personal financial state. It just records the cushion size: how much loss the junior tranche can absorb before the senior is at risk.

---

## 3. Loss propagation through the waterfall

When a book's assets lose value under stress, loss waterfalls down the seniority order:

```
Loss = max(0, original_assets - stressed_assets)

For each tranche, junior to senior:
   tranche_loss = min(tranche_notional, remaining_loss)
   remaining_loss -= tranche_loss
   if remaining_loss == 0: break
```

The most-junior (equity) tranche absorbs first, up to its full notional. If the loss exceeds the equity tranche, the next-most-junior absorbs whatever remains. And so on up the stack.

### Worked example

Sparklend ETH loan from §1: 1000 ETH at $4000/ETH = $4M assets. Junior tranche $1.5M (borrower equity), senior tranche $1.75M (Spark's claim). Total liabilities $3.25M; remaining $0.75M is "borrower's gain" if assets are unwound at peak.

ETH crashes 50% → assets = $2M:
- Loss = $4M − $2M = $2M
- Junior absorbs first: borrower equity $1.5M wiped out (junior_loss = $1.5M)
- Remaining loss = $0.5M
- Senior absorbs next: Spark loses $0.5M of its $1.75M claim (senior_loss = $0.5M)
- Spark recovers $1.25M of its $1.75M senior claim

Spark's risk on this position:
- Asset stress: ETH down 50% (read from canonical liquidity profile)
- Junior cushion: $1.5M
- Net loss to senior: max(0, asset_drop − junior_cushion) = max(0, $2M − $1.5M) = $0.5M
- Loss fraction: 0.5 / 1.75 ≈ 28.6%

This is the standard structured-product capital model. **No special "gap risk" treatment is needed** — gap risk has unified into asset-liquidity stress through the tranche waterfall.

### Cushion revaluation under stress

The junior cushion's *size in stress* may be smaller than its size now. If the borrower's equity is denominated in USD but pledged in ETH, an ETH crash that reduces the asset value also reduces the cushion's USD value (because the cushion *is* a portion of the same ETH). Category equations must apply scenario-conditional cushion sizing — stress both the asset side AND the cushion sizes consistently in each scenario.

For positions where the cushion is held in a different asset (e.g., USDC sponsor retention against a credit pool), the cushion stress profile differs from the asset stress profile and must be modeled separately.

---

## 4. Tranche rights schema (P + T)

Tranche claims often carry rights beyond the bare amount:

| Right | What it is | Maps to |
|---|---|---|
| **Redemption rights** | Holder can redeem at specified times / conditions | Permitted unwind (P) per `risk-decomposition.md` §4 |
| **Liquidation acceleration** | Holder can force unwind on specified triggers | Permitted unwind (P) |
| **Transfer rights** | Tranche can be sold to a different holder | Transfer market (T) per `risk-decomposition.md` §4 |
| **Governance rights** | Holder participates in book-level governance | Out of scope for risk math; relevant for operational governance |
| **Conversion rights** | Tranche can be converted to a different security | Affects notional rule (per `book-primitive.md` §3) |

The U/P/T liquidity decomposition from `risk-decomposition.md` cashes out at the tranche level: redemption + liquidation rights are **P** (whether the unwind is permitted at all), transferability is **T** (whether the tranche can be sold). Default is no rights (lockup until maturity, no transferability) — applicable to many fixed-term structures.

```metta
(tranche-rights spark-halo-senior-tranche
   (redemption-rights (only-at-maturity))
   (transfer-rights none)
   (liquidation-acceleration (on-health-factor-breach)))
```

For v1 crypto-collateralized NFATs: redemption only at maturity OR on health-factor breach, no transferability. So P and T are both restrictive; the position routes to `structbook` (no-liquidity-needed) sub-book.

---

## 5. Re-framing of overcollateralized lending

The new framework collapses several historically-distinct position types into one primitive: **a senior tranche of a tranched exobook**.

| Position | Old framing | New framing |
|---|---|---|
| Sparklend USD loan vs ETH | Crypto lending; no SPTP; gap risk applies | Senior tranche of perpetual ETH-collateralized exobook; senior's risk = ETH liquidity stress through junior cushion |
| Crypto-collateralized NFAT (v1 test) | Riskbook does its own gap-risk stress sim | Senior tranche of fixed-term BTC/ETH/stETH exobook; standard asset-liquidity stress through tranche waterfall |
| JAAA (CLO AAA) | RW + FRTB drawdown | Senior tranche of CLO exobook with deep junior cushion. RW = waterfall protection; FRTB drawdown = secondary-market price volatility (separate liquidity-loss source). Deferred for v1 (recursive complexity). |
| Real ABF deal | Credit-claim with attestor-verified properties | Senior tranche of ABF exobook (asset = real cash flows, junior = sponsor retention or equity tranche) |
| Pure ETH holding | Terminal exo asset | Same — no tranche structure |

**Pattern:** anything overcollateralized is a tranched exobook; the holder's risk is asset-stress propagated through the tranche structure of the exobook the holder owns.

This is the substrate-level unification. The exo asset's stress profile is read once from canonical data (per `asset-classification.md`), and the propagation math is identical regardless of what the structure is called in colloquial finance. Sparklend loans, NFAT facilities, CLO tranches, ABF claims — all the same math, parameterized by the structure.

---

## 6. Why gap risk disappears

**Gap risk** in the old framework was the bad debt from collateral prices crashing faster than liquidations execute (per the legacy `collateralized-lending-risk.md`). The old math treated this as a special concept distinct from FRTB drawdown (for liquid tradeables).

In the new framework, both are the same thing: **liquidity stress on the underlying asset**. The difference between "gap risk" and "FRTB drawdown" was just *which asset class the math was applied to*, not what the math actually was.

What unifies them: the asset's canonical liquidity profile (per `asset-classification.md`) gives the stress drop at the relevant horizon. The math:

- For a **direct holding** (no tranche structure): forced-loss = asset_value × stress_drop
- For a **senior tranche** of an exobook: forced-loss = max(0, asset_drop − junior_cushion)
- For a **junior tranche** of an exobook: forced-loss = junior_notional (worst case — wiped out before senior)

Gap risk and FRTB drawdown both fall out of these three cases. The "extra math" each used to require was just structure-specific arithmetic dressed up as a separate concept.

What survives in `risk-framework/`:
- `asset-classification.md` — canonical asset-level liquidity profiles
- `tranching.md` (this doc) — the waterfall propagation
- The `forced-loss-capital(asset-type)` term in `capital-formula.md`

What gets archived (per `clean-up-plan.md` Phase 2):
- `collateralized-lending-risk.md` — folded into `tranching.md`; "gap risk" no longer a separate concept
- `market-risk-frtb.md` — folded into `tranching.md` / `asset-type-treatment.md`; "FRTB drawdown" no longer a separate concept (still appropriate for un-tranched holdings — direct positions in liquid assets — handled via the same machinery)

---

## 7. One-line summary

**Tranches are ordered claims; seniority defines loss-absorption order; the most-junior tranche is the equity tranche (universal invariant per `book-primitive.md`); exoliabs (NEW) are external-party tranches like borrower equity; loss waterfalls down the order, eating each tranche before moving up; anything overcollateralized — Sparklend, NFAT, CLO tranche, ABF — expresses as a senior tranche of a tranched exobook with the same stress-propagation math; gap risk disappears as a separate concept (it was always asset-liquidity stress through tranche structure).**

---

## File map

| Doc | Relationship |
|---|---|
| `book-primitive.md` | The 6-tuple where tranches live; the equity invariant tranches implement |
| `risk-decomposition.md` | The forced-loss-capital risk type whose math runs through tranche waterfalls |
| `currency-frame.md` | Tranche denominations — frame vs instrument |
| `asset-classification.md` | Canonical asset-level stress profiles consumed by tranche math |
| `capital-formula.md` | Where tranche math contributes to per-position capital computation |
| `riskbook-layer.md` | Riskbook categories whose composition constraints reference tranche structures |
