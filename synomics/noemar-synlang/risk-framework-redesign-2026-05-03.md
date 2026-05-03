# Risk Framework Redesign — Comprehensive Notes

**Date:** 2026-05-03
**Status:** Working notes / design conversation summary
**Scope:** Foundational redesign of the risk framework (laniakea-docs/risk-framework + noemar-synlang/risk-framework.md). Captures every architectural insight from the design conversation so context can be reconstructed if lost.

---

## Quick reference (read first)

The redesigned framework rests on these primitives:

1. **Books** as nodes in a conservation network — a 6-tuple: `(assets, tranches, equity-tranche, rules, state, frame)`
2. **Tranches** as ordered claims with seniority — generalized to "rule-bearing claims" (claim amount can depend on state)
3. **Equity invariant** — every book has a designated equity tranche (most-junior, first-loss); when equity hits zero, unwind triggers
4. **Rules** attached to books — deterministic state-transition functions making books into financial state machines
5. **Currency frame vs instrument** — frame is the unit-of-account (set top-down by Generator); instruments are concrete realizations (USDS, USDC, ETH, etc.)
6. **Three-level layered risk computation** — Riskbook (fundamental + currency translation), Halobook (liquidity adjustments), Primebook (composition of typed sub-books for TTM/rates/hedging)
7. **Risk decomposition into 5 basic types** — default, credit-spread MTM, rate cash-flow drag, liquidity/fire-sale, concentration amplification
8. **Sub-books as risk-coverage contracts** — ascbook, tradingbook, termbook, structbook, hedgebook
9. **Projection pattern** — non-trivially-tranchable structures (options, derivatives) use category-specific projection models (Black-Scholes etc.) to produce stress-loss numbers that flow through the substrate normally
10. **Asset-level liquidity profile** as the foundational risk primitive — each terminal asset declares its canonical stress profile

The core teleological grounding: **the framework's purpose is to answer one question — "could we liquidate everything we need to right now if a worst-case crash happened?" — to drive the binary decision: continue Prime / step in and liquidate.**

The complete pragmatic statement:
> **Books + tranches + rules + stress scenarios + projection models = the complete framework for structural risk under stress.**

---

## Part 1: New conceptual primitives (architectural insights)

### 1.1 Currency frame vs instrument (foundational distinction)

Two distinct concepts that had been collapsed:

| Concept | What it is | Examples |
|---|---|---|
| **Frame** | Abstract unit of account in which value is measured. Set top-down by the Generator. | USD, EUR, BTC |
| **Instrument** | Concrete realization with its own stress profile relative to its frame | USDS, USDC, USDT (USD-proxies); EURC (EUR-proxy); BTC (its own native frame); ETH (volatile asset) |

**Frame inheritance:** Genbook → Primebook → Halobook → Riskbook all inherit the Generator's frame. USDS Generator → USD frame all the way down.

**Instrument flexibility:** A Prime can deploy USDT (or USDC, or anything) into a Halo unit. The Halo holds USDT positions, but its Halobook is still in USD frame because the Generator is USD-frame.

**Currency taxonomy** (kinds):
- `unit-of-account` (USD, EUR — abstract, not held)
- `stablecoin-proxy` (USDS, USDC, USDT — proxies for a unit-of-account, with depeg stress)
- `native-volatile-asset` (BTC, ETH — their own native frame, USD-equivalent via oracle with volatility stress)

Each currency declares: depeg-stress profile (for proxies), volatility profile (for natives), correlation with other currencies, FX stress profile (per-pair).

### 1.2 Books with rules (the 6-tuple)

A book is now:

```
Book = (assets, tranches, equity-tranche, rules, state, frame)
```

- **Assets** — exo assets and units of other books on the asset side
- **Tranches** — ordered claims with seniority (loss-absorption order); claim amount can be rule-determined (not just fixed notional)
- **Equity tranche** — the residual / first-loss absorber; universal invariant
- **Rules** — deterministic state-transition functions (when X, do Y; at time T, do Z; if oracle V, evaluate W)
- **State** — temporal, path-dependent, or oracle-dependent values rules read and update
- **Frame** — the unit of account in which the book's numbers are measured

**Rules give us:** conditional payoffs (options, CDS, insurance), time evolution (interest accrual, expiry, liquidation triggers), path dependence (barrier options, Asian averaging, accumulators).

**Tranches generalize** from "fixed claim with seniority" to "rule-bearing claim with seniority." Seniority still defines loss absorption order; the *amount* of each claim can be rule-determined.

**Books become financial state machines** — structurally identical to smart contracts (state + rules + transitions) but with the additional financial structure (asset/liability/seniority/equity invariant) that makes risk reasoning natural.

### 1.3 Tranching as first-class primitive (with non-pegged assets and exoliabs)

**Key insight:** Tranching + non-pegged assets + exoliabs together collapse "gap risk" into a special case of liquidity risk + tranche-waterfall propagation. Gap risk disappears as a separate concept.

**Vocabulary additions:**
- `exoasset`: terminal asset held but not controlled (ETH, BTC, USDC, T-bills) — already existed
- `exoliab`: tranche held by an external party (borrower equity, third-party debt, equity of an external structured product) — NEW

**Exobook schema with first-class tranching:**

```metta
;; in &core-registry-exo-book
(exo-book sparklend-eth-pool-001
   (category overcollateralized-eth-lending))

(exo-book-asset sparklend-eth-pool-001 eth 1000)              ; 1000 ETH

;; liability side — tranched, ordered by seniority (0 = junior absorbs first)
(exo-book-tranche sparklend-eth-pool-001
   (seniority 0)
   (holder borrower-XYZ)                                       ; exoliab
   (notional 750000)
   (denom usd))

(exo-book-tranche sparklend-eth-pool-001
   (seniority 1)
   (holder spark-halo-A)                                       ; the lender
   (notional 1750000)
   (denom usd))
```

**Re-framing of all overcollateralized lending:**

| Position | Old framing | New framing |
|---|---|---|
| Sparklend USD loan vs ETH | Crypto lending; no SPTP; gap risk applies | Senior tranche of perpetual ETH-collateralized exobook; senior's risk = ETH liquidity stress through junior cushion |
| Crypto-collateralized NFAT (the test) | Riskbook does its own gap-risk stress sim | Senior tranche of fixed-term BTC/ETH/stETH exobook; equation = standard asset-liquidity stress through tranche waterfall |
| JAAA (CLO AAA) | RW + FRTB drawdown | Senior tranche of CLO exobook with deep junior cushion. RW = waterfall protection; FRTB drawdown = secondary-market price volatility (separate liquidity-loss source). DEFERRED for v1 (recursive complexity) |
| Real ABF deal | Credit-claim with attestor-verified properties | Senior tranche of ABF exobook (asset = real cash flows, junior = sponsor retention or equity tranche) |
| Pure ETH holding | Terminal exo asset | Same — no tranche structure |

**Pattern:** anything overcollateralized is a tranched exobook; the holder's risk is asset-stress propagated through the tranche structure.

### 1.4 The equity invariant (universal book-level structural rule)

> **Every book has a designated equity tranche (always the most-junior, first-loss). The book is solvent iff equity > 0. When equity hits zero, an unwind procedure triggers.**

| Book type | Equity holder | Unwind mechanism |
|---|---|---|
| Exobook (overcollateralized loan) | External borrower | Protocol-level liquidation |
| Exobook (CLO etc.) | Equity tranche holder | Per the structure's contractual mechanics — synome observes |
| Riskbook | The Halo (operator) | Governance/operational wind-down |
| Halobook | The Halo | Same |
| Primebook | The Prime | Same |
| Genbook | Sky (protocol surplus) | Drawdown of Sky reserves before USDS itself is at risk |

**Real-time equity computation** is the load-bearing invariant. Assets fluctuate (especially non-pegged), liabilities accrue, equity = (assets − liabilities). When equity hits floor → unwind.

This is the universal balance-sheet identity made *structurally enforced* rather than derived. It also gives precise meaning to bankruptcy remoteness: an unwind of one book can't propagate loss upward past its equity holder. Independent equity = independent unwind boundary.

**Data infrastructure implication:** every book must always know its current equity in real-time. Drives:
- Internal books: computable from synart state
- On-chain exobooks: endoscrapers compute equity from chain reads
- Off-chain exobooks: attestor-published numbers
- Each new asset class brought into the system requires a documented equity-feed mechanism at onboarding

### 1.5 Risk decomposition into basic types

Five atomic kinds of loss, each with different time signatures and stress responses:

| Risk type | What it is | Time signature | Capital approach |
|---|---|---|---|
| **Default / fundamental** | Pure default — credit default, smart contract failure, counterparty failure, regulatory seizure. NOT collateralization shortfall. | Permanent | Always required (Risk Weight) |
| **Credit spread MTM** | Mark-to-market loss from spread widening | Mean-reverting (months) | Avoidable if hold-to-par possible |
| **Rate cash-flow drag** | Permanent carry loss from rate regime shift | Permanent until rates revert or asset matures | Hedge or hold rate-hedge capital |
| **Liquidity / fire-sale** | Realized loss from forced execution (slippage, depth, oracle latency). UNIFIED with what was "gap risk" — they're the same thing. | Crystallizes only on forced sale | Avoidable if not forced to sell |
| **Concentration amplification** | Correlated stress hits multiple positions simultaneously | Portfolio-level | Category caps (100% CRR on excess) |

**Critical observation:** "FRTB drawdown" (for tradeables) and "gap risk" (for collateralized lending) were the same thing measured differently for different asset classes. Now unified as `forced-loss-capital(asset-type)` — liquidity stress on the underlying asset, propagated through the tranche structure (or directly for un-tranched holdings).

**Separate parallel tracks (NOT folded into CRR computation):**
- ASC (Actively Stabilizing Collateral) — peg-defense operational liquidity
- ORC (Operational Risk Capital) — guardian-posted, covers operator compromise

### 1.6 The three-level layered risk computation

| Layer | Computes | Outputs |
|---|---|---|
| **Exobook** | Recursive infrastructure for external structures | Risk profile of external structures |
| **Riskbook** | Default risk + intrinsic asset characteristics + **instrument-to-frame translation with stress** | Per-position tuple: (RW, CS-sensitivity, intrinsic liquidity profile, SPTP/TTM, denomination → frame stress) |
| **Halobook** | Bundle adjustments to liquidity profile — **bundling can downgrade liquidity but not upgrade**. Aggregates Riskbook units into Halobook unit with declared liquidity tier and TTM | Halobook unit with: aggregated RW, declared liquidity tier, declared TTM/SPTP |
| **Primebook (composition)** | Routes Halobook units to typed sub-books based on treatment classification. Each sub-book is a *risk-coverage contract* | Per-sub-book: matched portion (covered risks dropped) + unmatched portion (capital for uncovered risks) |
| **Genbook / system** | Concentration / correlation caps; system-wide stability constraints | Cap-excess penalties |

**The Riskbook is special** — it's the layer that:
- Accepts external assets in their native denominations
- Applies depeg/FX stress for cross-currency equivalences
- Translates to the Generator's frame
- Issues Riskbook units that upstream books can consume as frame-pure
- Also captures lots of capital efficiency through composition (CDS-protected ABF, delta-neutral spot/perp, etc.)

The Riskbook is where messy reality enters the synomic accounting frame. Below it: arbitrary denominations. Above it: everything is in the generator's frame (with declared stress).

### 1.7 Primebook as composition of typed sub-books

The Primebook is no longer a flat aggregator. It's a composition of typed sub-books:

| Sub-book | Role | Default | Credit Spread MTM | Rate | Liquidity |
|---|---|---|---|---|---|
| `ascbook` | ASC-eligible holdings (peg-defense readiness) | Capital | Capital | n/a (cash-equivalent) | Liquidity is the product (must hold) |
| `tradingbook` | Liquid holdings (FRTB-style) | Capital | Forced-loss (FRTB drawdown) | Hedged or rate-hedge capital | Forced-loss (FRTB captures it) |
| `termbook` | TTM units matched against tUSDS (Prime holds YT) | Capital | **Covered** (held to par; matched fixed/fixed) | **Covered** (matched fixed/fixed via tUSDS YT) | **Covered** (no forced sale) |
| `structbook` | TTM units matched against structural demand | Capital | **Covered** (held to par) | Capital required (rate-hedge or v1 carve-out) | **Covered** (no forced sale) |
| **`hedgebook`** (NEW) | Cross-position hedge groups | Capital | Capital adjusted for hedge | Capital adjusted for hedge | Capital adjusted for hedge |
| (unmatched leftover) | What didn't fit anywhere | Capital | Forced-loss | Forced-loss | Forced-loss |

**Primebook still issues a single Primeunit upward** to Genbook — the sub-books are internal composition for risk treatment, not external products.

**Each sub-book has its own category catalog** with composition constraints + equations + projection models. Default-deny preserved: holdings without a matching category get CRR 100%.

### 1.8 Hedgebook — portfolio-level hedging

The Hedgebook is the new sub-book where well-defined hedge pairs/groups get composed across the Prime's portfolio. Its category equation rewards anti-correlation: residual basis risk after the hedge is what gets capital-charged, not either leg's standalone risk.

**Two distinct levels of hedging:**

| Level | Scope | Examples |
|---|---|---|
| **Riskbook** | Within one coherent strategy / single composition | `abf-with-cds-cover` (ABF claim + matching CDS in same Riskbook); `delta-neutral-eth-spot-perp` (long spot + short perp) |
| **Hedgebook (Primebook)** | Across the Prime's diverse portfolio | Long credit via Halobook A + index-CDS hedge via Halobook B; USDC concentration across Riskbooks + Circle-CDS hedge separately |

Riskbook hedges are tactical (specific vs specific within one strategy). Hedgebook hedges are portfolio-level (broad hedges across diverse positions). Hedgebook can only meaningfully evaluate hedges between cleanly-defined positions — Riskbook output. Messy exobooks can't be hedged in the Hedgebook because the hedge math depends on knowing what you're hedging precisely.

**Hedgebook category equations explicitly model hedge failure modes:**
- Counterparty risk on hedge leg (CDS issuer fails)
- Basis risk (hedge instrument doesn't track specific exposure)
- Liquidity risk on closing the hedge under stress

So the Hedgebook doesn't hand out "hedge magic" — it's a quantified residual-risk computation. Clean hedge → near-zero residual; sloppy hedge → mostly capitalized.

**Currency hedges in the Hedgebook:** A Prime hedging system-wide USDC depeg risk with a Circle-CDS or USDC/USDT FX hedge — the hedge lives in the Hedgebook, providing CRR reduction across the Prime's USDC exposure across many Riskbooks. Powerful pattern.

### 1.9 Projection pattern (handling complex/non-tranched positions)

The substrate doesn't need to natively model every weird position type. Each category brings a **projection function** that converts the position into a stress-loss number under each scenario. Sophisticated finance lives in the projection layer; the substrate stays clean.

| Position type | Projection model |
|---|---|
| Senior loan tranche | Direct (tranche waterfall) |
| ETH holding | Direct (asset stress profile) |
| Vanilla call option | Black-Scholes (or Heston, local-vol) → stress P&L |
| Callable bond | OAS / lattice / prepayment model → stress price |
| MBS with prepayment | Prepayment model → stress cashflows |
| CDS | Default probability × LGD → stress payoff |
| Asian/lookback option | Monte Carlo or analytic → stress price |
| Cat bond | Probability of trigger × payoff → stress |

**Architecture:** each category in `&core-framework-risk-categories` declares a `projection-model` along with its composition constraints:

```metta
(risk-category-def vanilla-european-call
   (level position-instrument)
   (projection-model black-scholes
      (variables strike expiry notional underlying-price implied-vol risk-free-rate)
      (under-scenario $s
         (let* (($u-stressed (apply-scenario $s underlying-price))
                ($v-stressed (apply-scenario $s implied-vol)))
           (compute-bs-pnl $u-stressed $v-stressed strike expiry notional)))))
```

Vanilla holdings → trivial projection (linear pass-through). Sophisticated structures → sophisticated projections. Categories without declared projection → CRR 100% (default-deny).

**Rules + projection models are complementary:**
- **Rules** express what the contract DOES — the truth of the obligation
- **Projection models** are analytical tools for computing risk under stress when the rule is too computationally heavy to inline

A vanilla call can be projected via Black-Scholes (analytic) OR by simulating the rule across stress paths (Monte Carlo). The rule is the same; the projection method varies.

### 1.10 Projection-model risk as own capital dimension

Worth naming **projection-model risk** as its own (small) capital adjustment. Categories with weaker projection models — newer instruments, less-tested math, more degrees of freedom in calibration — could carry an explicit "model uncertainty haircut" on top of the projected number. Makes the framework's epistemics first-class: it admits when it's less sure and reserves accordingly.

### 1.11 Asset-level liquidity profile (foundational primitive)

For the framework to compose correctly, each terminal exo asset needs **one canonical risk profile** that downstream structures inherit:

```metta
(asset-category eth
   (drawdown-distribution
      (scenario severe-correlated-crash  (drop 0.55) ...)
      (scenario credit-crisis            (drop 0.20) ...)
      (scenario stable                   (drop 0.05) ...))
   (slippage-model
      (depth-fn (impact-bp-per-million ...)))
   (correlation-with btc 0.85)
   (correlation-with stETH 0.95))
```

Any category equation that touches ETH (a tranched exobook with ETH collateral, an ETH-only Riskbook, a structured product with ETH exposure) reads this profile and stresses against it. No category re-derives ETH's risk from scratch.

**Without this**, every category equation re-implements asset stress with potentially different assumptions, and consistency falls apart. This is the load-bearing primitive that makes everything above compose correctly.

### 1.12 Sky-issued tranched products = LCTS

`srUSDS`, `TEJRC`, `TISRC` (referenced in risk-framework README as risk capital instruments) are tranches of a Prime's (or Sky's) risk-capital book. The new tranching primitive supports this natively. Worth a future doc mapping the full LCTS catalog into the tranched-book model — should drop out cleanly.

### 1.13 Structural demand scraping (architectural addition)

Real-time scraping of structural demand:
- Scrape USDS, DAI, sUSDS holder data (DAI included because of DAI→USDS migration, sUSDS for savings tier)
- Scrapers as **grounded atoms** (native code outputs into a synart space)
- Processing as **synlang** (rules consume scraper outputs and produce per-bucket capacity facts)
- Lives inside Generator's entart in a `structural-demand-scraping` sub-space

```
&entity-generator-usge-structural-demand
  ├── &entity-generator-usge-structural-demand-scrapers   ← grounded scraper outputs
  └── &entity-generator-usge-structural-demand-auction    ← fake-then-real auction logic
```

Separating scrapers from processed facts keeps raw data isolatable for compaction/replication and lets processing logic be rebuilt without re-scraping.

### 1.14 Fake auction (built for real later)

Build the auction interface and have all Primes submit a 0-cost bid for an equal share. Same interface as the real auction will use; only the strategy changes later.

```metta
(= (run-auction $bucket)
   (let* (($capacity (match &self (structural-demand-capacity $bucket $c) $c))
          ($bidders  (collapse (match &self (auction-bidder $bucket $b) $b)))
          ($n        (length $bidders))
          ($per-bid  (/ $capacity $n)))
     (map (lambda ($b)
            (add-atom &self (allocated-to $b $bucket $per-bid))) $bidders)))
```

Later: replace `(run-auction)` body with real bid evaluation. Data flow unchanged.

---

## Part 2: Generator entity addition

New entity type `generator` (named USGE — USDS Generator), accordant to
the single operational guardian Ozone alongside the Primes:

```
&core-root
  └── &entity-guardian-ozone-root                            ← single operational guardian
        ├── &entity-generator-usge-root                      ← new entity type
        │     ├── &entity-generator-usge-genbook             ← Primeunits in, USDS out
        │     └── &entity-generator-usge-structural-demand   ← capacity + distribution
        │
        ├── &entity-prime-spark-root
        │     ├── &entity-prime-spark-primebook              ← matching computation here
        │     └── &entity-halo-spark-crypto-lending-root
        │           ├── halobook
        │           └── riskbook (crypto-collateralized-USD-lending category)
        │
        ├── &entity-prime-grove-root                         (same shape)
        └── &entity-prime-obex-root                          (same shape)
```

**Topology vocabulary additions** (topology.md §9):
- New entity-type keyword: `generator`
- New sub-kind keywords: `genbook`, `structural-demand`, `structural-demand-scrapers`, `structural-demand-auction`

**Authority chain note:** Ozone is the single operational guardian (see
synome-extra-info.md Q17 resolution). USGE and all Primes are direct
children of Ozone, not of separate per-Prime guardians.

---

## Part 3: The crypto-collateralized lending v1 test

### 3.1 Overall scope

**Three near-identical Halos** doing institutional borrowers custodial crypto-collateralized stablecoin lending. NFATs (fixed-term Halo units). Risk decomposes through: per-loan exobooks → Riskbook → Halobook → Primebook → Genbook.

**Topology:**
- 3 Star Primes (Spark, Grove, Keel), each running one of the 3 Halos
- USDS Generator with Genbook + structural demand registry
- Equal split of structural demand among the 3 Stars (1/3 each per bucket)

### 3.2 Position structure (each NFAT = senior tranche of per-loan exobook)

Each NFAT loan position is structurally:

```
exobook (per-loan):
   asset side:   BTC/ETH/stETH collateral (custodial)
   liability side (tranched):
      junior:    borrower equity (~20-40% of asset value)            [exoliab — held by borrower]
      senior:    loan principal (USDC/USDT-denominated)              [endo — held by Halo's Riskbook]
   rules:
      continuous: compute health factor from oracle prices
      if health < threshold: trigger liquidation
      at maturity: borrower repays in cash, recovers collateral
   state: current collateral value, current health factor
   frame: USD (inherited from USDS Generator)
```

### 3.3 Riskbook category for the test

Provisional name: `crypto-collateralized-USD-lending`

```metta
(book-category-def crypto-collateralized-USD-lending
   (frame usd)
   (composition-constraints
     (and (single-senior-tranche-positions)
          (asset-class-in (eth btc stETH))
          (denom-in (usdc usdt))))
   (equation-m2m
     (sum-over (held-senior-tranches)
       (lambda ($pos)
         (let* (($asset-stress-profile (asset-stress-profile (collateral-of $pos)))
                ($denom-depeg (depeg-stress-profile (denom-of $pos)))
                ($junior-cushion (junior-tranche-size (exobook-of $pos))))
           (simulate-across-scenarios m2m-scenarios
             (lambda ($s)
               (let* (($asset-drop (apply-scenario $s $asset-stress-profile))
                      ($depeg-loss (apply-scenario $s $denom-depeg))
                      ($effective-loss (max 0 (- $asset-drop $junior-cushion))))
                 (+ $effective-loss $depeg-loss)))))))))
```

This is the standard structured-product capital model — no special "gap risk" treatment needed, because gap risk has been unified into asset-liquidity stress through the tranche waterfall.

### 3.4 Test attestor mechanism

Attestor = special beacon class (similar to govops beacon), certed and authed by govops root to attest for a particular Halo class:
- Registered beacon class: `attestor`
- Cert chain rooted in the responsible Halo's govops
- Writes attestation atoms (signed)
- Slashing surface for proven-false attestations
- Off-chain attestor + on-chain endoscraper reconciliation cycle

The cert/auth/beacon-class machinery already exists. Genuine new design is the **attestation atom schema** + reconciliation cycle for off-chain claims.

### 3.5 Privacy approach for v1

**Aggregate buckets in synart, full deal terms in telart:**
- Synart records: LTV bucket, term bucket, jurisdiction code, custodian ID, denom, asset class
- Telart (visible to attestor + Halo govops): full deal terms, contract details, parties
- Riskbook category equation reads buckets, not specifics

The bucket categories ARE the regulatory surface — what governance is approving.

**Hash-commitments and encrypted-at-rest deferred** — too much complexity for marginal v1 benefit.

### 3.6 Stress scenarios for v1

Hand-tuned library covering:
- `severe-crypto-correlated-crash` (BTC/ETH magnitude over liquidation window)
- `stETH-ETH-peg-break`
- `USDC-depeg`
- `USDT-depeg`
- `custodian-failure` (binary)
- `combined-coordinated-case`

Lives in `&core-framework-stress-scenarios`. Full library curation is governance work for later.

### 3.7 TTM / structural demand integration

**TTM cap: 0-12 months** for the test. Buckets 0-24 from duration-model.md (15 days each, up to 360 days).

**Simplified SPTP** (will be renamed): for crypto-collateralized NFATs, SPTP = remaining contractual term, no stress modifier. Bucket = `ceil(ttm_days / 15)`.

**Structural demand source:** real-time scraping of USDS, DAI, sUSDS holder data (data team will build prototype). Output: `(structural-demand-capacity bucket-N <amount>)` atoms in `&entity-generator-usge-structural-demand`.

**Distribution:** "fake auction" — equal split among 3 Stars per bucket. `(allocated-to spark-prime bucket-12 33.3M)` etc.

**Match algorithm** (in synlang): partial matching with cumulative capacity per matching.md. Greedy descending — longest-SPTP positions claim highest bucket first, cumulative downward.

**v1 carve-out: matched positions don't need rate-hedge capital.** Temporary suspension of the rate-hedging requirement from matching.md for these positions. v2+ will reinstate.

### 3.8 v1 simplifications log (deliberate carve-outs)

1. Manual governance-set capacity initially (Lindy + structural caps from existing duration-model.md parameters; data-team scraper will replace later)
2. Equal-split distribution (no auctions, no tug-of-war)
3. No rate-hedge capital for matched positions (carve-out from matching.md)
4. TTM range 0-12 months only
5. SPTP = remaining nominal term (no stress modifier)
6. One Genbook (USDS) only
7. Three Halos under three Star Primes (one Halo per Prime)
8. Super-senior tranches only (mezzanine/equity-tranche holdings get CRR 100% by default-deny)
9. Phase 1 manual structural demand allocations (not Lindy-driven dynamically yet)
10. Halobook category as placeholder (`crypto-lending-bundle` with no liquidity adjustment)
11. Active sub-books: only `structbook` for the test. `ascbook`, `tradingbook`, `termbook`, `hedgebook` exist as schema placeholders but hold nothing
12. Tranche rights schema present but not exercised
13. JAAA / CLO modeling deferred (recursive complexity)

Each has a clear later-phase replacement.

---

## Part 4: Plan for editing risk-framework (laniakea-docs/risk-framework/)

### 4.1 New files to create

**`risk-decomposition.md`** (NEW) — the conceptual root the other docs specialize from. Contains:
- The 5 basic risk types (default, credit-spread MTM, rate, liquidity, concentration)
- The teleological grounding (decision: continue Prime / liquidate)
- The risk-types × layer × sub-book-coverage matrix
- Why "gap risk" and "FRTB drawdown" are unified as `forced-loss-capital`

**`book-primitive.md`** (NEW) — the substrate definition. Contains:
- The 6-tuple book primitive (assets, tranches, equity-tranche, rules, state, frame)
- The equity invariant (universal book-level structural rule)
- Tranching as first-class with seniority
- Rules attached to books — books as financial state machines
- Real-time equity recomputation requirement

**`currency-frame.md`** (NEW) — frame vs instrument. Contains:
- Currency taxonomy (unit-of-account, stablecoin-proxy, native-volatile-asset)
- Frame inheritance from Generator down through book hierarchy
- The Riskbook as instrument-to-frame translation layer
- Multi-generator architectural readiness (single-generator v1)

**`tranching.md`** (NEW) — first-class tranching. Contains:
- Exoassets vs exoliabs vocabulary
- Senior/junior/equity tranches
- Loss propagation through waterfall
- Tranche rights schema
- Re-framing of overcollateralized lending (Sparklend, NFAT loan, ABF) as tranched exobooks
- Why gap risk disappears as separate concept

**`projection-models.md`** (NEW) — the projection pattern. Contains:
- Categories declare projection-model per position type
- Black-Scholes, Monte Carlo, lattice models, etc. as projection examples
- Rules vs projections — complementary
- Projection-model risk as own capital adjustment dimension

**`hedgebook.md`** (NEW) — Hedgebook sub-book at Primebook level. Contains:
- Two levels of hedging (Riskbook tactical vs Hedgebook portfolio)
- Hedgebook categories with explicit hedge-failure modeling
- Currency hedges via Hedgebook
- Hedge declaration mechanism (Prime declares hedge groups)
- Cross-Halobook flow without breaking bankruptcy-remoteness

**`primebook-composition.md`** (NEW) — Primebook as composition of typed sub-books. Contains:
- The 5 sub-book types (ascbook, tradingbook, termbook, structbook, hedgebook) + unmatched
- Sub-books as risk-coverage contracts (which risks each covers)
- Routing Halobook units to sub-books (recommend declarative via composition constraints)
- Each sub-book has its own category catalog
- Default-deny preserved at sub-book level

### 4.2 Files to substantially revise

**`README.md`** — update module index to reflect new files, add the foundational primitives at the top, update Open Items to reflect new design (concentration L3 still open, etc.)

**`asset-classification.md`** — extend the three properties (fundamental risk, drawdown, SPTP) into the full risk-type tuple. Asset registers all components needed by downstream consumers. SPTP probably should split into "credit-spread duration" and "rate duration."

**`asset-type-treatment.md`** — re-write each asset class treatment to use the new framework: tranched exobook structure where applicable, projection model where applicable, sub-book routing.

**`capital-formula.md`** — becomes a downstream consumer of risk-decomposition.md. Per-position computation flow becomes:
1. Look up position's Riskbook category equation
2. Project asset stress through tranche waterfall (or projection model for non-tranched)
3. Apply Halobook liquidity adjustment if any
4. Route to Primebook sub-book
5. Sub-book determines which risks are covered vs require capital
6. Sum to position capital

**`collateralized-lending-risk.md`** — substantial rewrite. Gap risk is no longer a separate concept; reframe as asset-liquidity stress through tranche waterfall. May fold this doc into tranching.md with a redirect.

**`market-risk-frtb.md`** — also reframe: FRTB drawdown is the unified `forced-loss-capital` term for liquid tradeable assets, computed via the asset's liquidity profile. Still appropriate for un-tranched holdings (direct positions in liquid assets). May merge into a unified `forced-loss-capital.md`.

**`matching.md`** — preserve the credit-spread vs rate distinction insight (foundational). Update to reflect:
- Sub-book treatment as "risk-coverage contract" framing
- Termbook (covers spread + rate + liquidity) vs Structbook (covers spread + liquidity, rate carve-out for v1)
- Cumulative capacity computation
- Relation to the new layered architecture

**`duration-model.md`** — preserve the Lindy + structural caps math; update to reflect:
- Lives in Generator's entart (structural-demand sub-space)
- Phase 1 manual allocation is the simplification
- Real-time scraping replaces manual eventually
- Equal-split is the v1 distribution; auctions are the eventual pattern

**`correlation-framework.md`** — reframe concentration as living at two levels (Primebook for own categories; Genbook for system-wide). The 100% CRR penalty mechanism stays.

**`asc.md`** — explicitly note ASC is a separate parallel track (not a sub-book in the new sense), but ASC-eligible holdings live in the `ascbook` sub-book. ASC requirement is operational; ascbook risk treatment is structural.

**`operational-risk-capital.md`** — note ORC is also a separate parallel track. No change to mechanics.

**`risk-monitoring.md`** — extend metrics list to include new framework outputs (per-sub-book CRR, hedge-residual exposure, equity-invariant proximity-to-zero alerts, etc.).

**`sentinel-integration.md`** — update beacon metric outputs to reflect new computation flow.

**`examples.md`** — replace examples with worked computations showing the new framework end-to-end (start with the 3-Halo crypto-lending test, then a JAAA example for v2+).

### 4.3 Suggested new sequencing for risk-framework reading

1. `risk-decomposition.md` — the conceptual root (start here)
2. `book-primitive.md` — the substrate
3. `tranching.md` — first-class tranching mechanics
4. `currency-frame.md` — frame vs instrument
5. `projection-models.md` — handling non-tranchable structures
6. `asset-classification.md` — asset risk profile schema
7. `primebook-composition.md` — sub-book overview
8. `matching.md` — termbook / structbook matching mechanics
9. `hedgebook.md` — Hedgebook details
10. `correlation-framework.md` — concentration caps
11. `asset-type-treatment.md` — worked examples per asset class
12. `capital-formula.md` — final computation flow
13. `asc.md`, `operational-risk-capital.md` — parallel tracks
14. `examples.md`, `risk-monitoring.md`, `sentinel-integration.md` — operational

---

## Part 5: Plan for editing noemar-synlang/ (synomic-architecture docs)

### 5.1 Files to substantially revise

**`risk-framework.md`** — major rewrite to reflect:
- The 6-tuple book primitive (currently described as 4-book taxonomy)
- New three-level architecture: Riskbook (fundamental + frame translation), Halobook (liquidity adjustments), Primebook (composition of sub-books)
- Tranching as first-class (currently absent)
- Currency frame vs instrument distinction
- Equity invariant as foundational
- Risk-type decomposition (default / spread / rate / liquidity / concentration)
- Sub-book-as-risk-coverage-contract framing
- Projection pattern
- Hedgebook
- Asset-level liquidity profile primitive
- Removal of "gap risk" as separate concept

This is the biggest synlang doc rewrite. Probably wants to be split into:
- `risk-framework.md` — top-level overview with cross-references
- `book-primitive-and-tranching.md` — substrate
- `riskbook-halobook-primebook.md` — three-level layering
- `projection-and-rules.md` — how complex positions get into the framework
- `hedgebook.md` — Hedgebook sub-book

**`topology.md`** —
- Add `generator` to entity-type keyword vocabulary in §9
- Add `genbook`, `structural-demand`, `structural-demand-scrapers`, `structural-demand-auction`, `hedgebook`, `ascbook`, `tradingbook`, `termbook`, `structbook` to sub-kind vocabulary
- Update entity-tree examples to show Generator at top
- Update §6 (synome root layers) to add `&core-framework-currency`, `&core-framework-stress-scenarios` (already there), and per-asset-category stress profile location
- Update Phase 1 commitments if any new ones emerged (probably equity invariant deserves to be foundational alongside append-only writes)

**`syn-overview.md`** —
- Update §6 (Halo / Class / Book / Unit) to reflect new four-book + sub-book taxonomy
- Update §7 (risk framework) to reference the new risk-decomposition doc
- Update §8 (settlement) to reflect Genbook role
- Update §10 (replicated synart) entity tree examples

**`synlang-patterns.md`** —
- §1 (Platonic kernel) extends with rules + tranches + frame as part of the book primitive
- New section on tranche-rule patterns
- New section on projection-model declaration patterns
- New section on Hedgebook composition patterns

**`syn-tel-emb.md`** — minor updates for Generator entity, structural demand scraping context

**`settlement-cycle-example.md`** — replace the example with one that includes the Generator → Prime → Halo flow with sub-book routing and tranche waterfall (probably the 3-Halo crypto-lending test as the canonical example)

**`synart-access-and-runtime.md`** — note attestor as new beacon class with cert/auth shape

**`scaling.md`** — note scrapers as grounded atoms in structural-demand-scrapers space; per-pair FX stress profile load implications

### 5.2 New files to create

**`books-with-rules.md`** (NEW in noemar-synlang/) — synlang patterns for rule-bearing tranches and book state machines. Worked examples: option, overcollateralized loan, barrier knockout, CDS.

**`generator-entity.md`** (NEW in noemar-synlang/) — Generator entity type, Genbook structure, structural demand sub-spaces, distribution mechanism (fake-then-real auction).

---

## Part 6: Open design questions

### 6.1 Substrate-level

1. **Halobook downgrade semantics.** Multiplicative liquidity factor? Liquidity-tier override? "Max bucket" constraint? Schema needs definition.

2. **The credit-spread-vs-rate split inside SPTP.** Existing matching.md lumps them. Should SPTP split into "credit-spread duration" and "rate duration" for separate treatment in different sub-books?

3. **Tranche-cushion revaluation under stress.** Under correlated stress the junior cushion may be effectively smaller (e.g., borrower equity drops faster than loan principal). Equations should allow scenario-conditional cushion sizing.

4. **Multi-tranche holdings.** A Riskbook might hold both senior and junior of the same exobook. Category composition rules need to support this. Deferred for v1 (super-senior only).

5. **Tranche-frame mismatches.** Can a tranche be denominated in a frame different from its book? E.g., a USD-frame book with a tranche that has a EUR-denominated claim? Real (cross-currency tranches exist in structured finance) but adds complexity. Worth flagging as v2+.

6. **Treatment-coverage-failure semantics.** What happens when a position is in `structbook` but bucket capacity gets withdrawn mid-cycle (Lindy shifts, redemptions surge)? Position transitions from "covered" to "uncovered" — needs a transition mechanism (forced rebalance, capital top-up window, etc.).

7. **Hedge breakdown transitions.** If hedge counterparty defaults mid-cycle or basis blows out beyond category tolerance, Hedgebook composition fails the category check. Need clean transition (positions fall back to default-deny CRR 100% or natural sub-book treatment).

### 6.2 Routing and composition

8. **Routing Halobook units to Primebook sub-books.** Two shapes:
   - (a) Halo declares per-unit treatment classification: `(treatment-for $hb-unit structbook)`
   - (b) Primebook routes declaratively by reading unit properties against sub-book composition constraints (default-deny pattern)
   - Recommend (b) — structurally consistent with rest of model.

9. **Hedge declaration mechanism.** Does the Prime declare hedge groups operationally? `(hedge-group H units (a b c))`. Probably yes — explicit declaration with category match validation.

10. **Cross-Halobook flow into Hedgebook.** First place cross-Halobook composition happens. Need to handle without breaking bankruptcy-remoteness — probably the Hedgebook is read-only at the Halobook level (observes and composes for capital purposes; doesn't actually merge bankruptcy estates).

11. **Hedgebook unit issuance.** Does the Hedgebook issue its own unit upward (uniform with other sub-books) or modify underlying sub-books' contributions? Recommend: issues a unit; halobook units that participate get "claimed" by Hedgebook composition; their natural-sub-book contribution is replaced.

12. **Concentration interaction with hedges.** A Prime could be concentrated in a hedged position. Concentration limits should still bite on net-of-hedge exposure — hedges reduce capital but don't eliminate concentration concerns.

### 6.3 Currency / multi-generator

13. **Currency identifier registry.** Need `&core-registry-currency`. Every currency (unit-of-account or instrument) registered with properties. Adding new currency is governance-paced.

14. **Cross-frame conversion rules.** Where do FX stress profiles live? Per-pair atoms in `&core-framework-fx-stress`? Probably per-pair because FX correlations matter.

15. **Multi-generator Primes.** Phase 1 is single-generator. Architecture should not preclude later multi-generator Primes (one Primebook per generator served).

16. **The "1:1 lock" stale-calibration risk.** When a Riskbook accepts USDC at "1.0 × USD with X% depeg stress," X% is a model assumption. If realized depeg approaches X, the assumption is breaking. Needs governance discipline (cadence for recalibration, alarms when realized approaches modeled limits).

### 6.4 Generator / structural demand

17. **Generator's place in the authority chain.** New entity type. Where does it root? (a) under Core Council directly (peer of all Guardians); (b) under a dedicated "USDS Guardian"; (c) under Core Council's own root structure as a special class. (a) is cleanest minimal addition; (b) lets it be governed by token holders.

18. **Equal-split semantics with bucket-specific caps.** Two readings:
   - (a) Equal per-bucket: each Star gets 1/3 of bucket 0, 1/3 of bucket 1, etc.
   - (b) Equal cumulative pool: each Star gets 1/3 of total ≤12-month capacity, freely allocated across buckets
   - Recommend (a) — preserves structural shape per Star.

19. **Unused allocations.** If Spark uses all of its allocation but Grove uses none, what happens to Grove's idle capacity? v1: sits idle (document inefficiency). v2: redistribution / secondary market.

20. **Genbook's risk computation role.** Pure aggregation (consistent with Halobook/Primebook), or also a stress simulation for USDS depeg pressure? v1 pure-aggregation is the obvious starting point.

### 6.5 Externally-held positions

21. **Externally-held junior tranches modeling.** Borrower's junior tranche held by external party. Exobook records `(holder borrower-XYZ)` but synome doesn't track borrower's full state — just the cushion size as a haircut for the senior. Schema sufficient?

22. **Sky-issued tranched products.** Architecture supports this (LCTS = srUSDS, TEJRC, TISRC). Worth a future doc mapping the full LCTS catalog into the tranched-book model.

23. **Tranche rights.** Schema needs per-tranche rights atoms — at minimum: redemption rights, liquidation acceleration, governance voting (for governance tranches), conversion rights. v1 doesn't model in detail; just leave room.

### 6.6 Test-specific

24. **Test attestor schema.** Atom shape for attestation claims, reconciliation cycle for off-chain claims (where on-chain endoscraper isn't sufficient).

25. **NFAT match-eligibility decision (resolved):** YES match-eligible, SPTP = remaining nominal term. But need to confirm this lands in synlang correctly.

26. **Privacy bucket choice.** LTV bucket boundaries, term bucket boundaries, jurisdiction code list, custodian ID schema. Deal with at the Riskbook category specification.

27. **Stress scenario calibration for crypto.** What magnitude of crypto crash is "severe-correlated"? What's the right liquidation window? Hand-tuned for v1 but needs discussion.

### 6.7 Outside-the-substrate (genuinely meta)

28. **Multi-agent strategic equilibrium / game theory.** Rules express what one party will do; can't natively model what counterparties will do. Captured imperfectly via behavioral scenarios. Real limit.

29. **Subjective contracts.** "Best efforts," "commercially reasonable," "in good faith." Have legal meaning, aren't deterministic. Handled by attestor-based legal review for off-chain contracts. Real limit.

30. **Genuinely novel risk modes.** Stress libraries are backward-looking. Can't see modes we haven't conceived of. Mitigated by scenario-library-curation discipline + conservative defaults + willingness to declare CRR 100%.

31. **Input correctness.** If attestor lied, oracle manipulated, calibration stale — projection executes against wrong inputs. Reality problem, not framework problem. Mitigated by attestor-redundancy, multi-source pricing, etc.

32. **Projection-model error.** Black-Scholes is wrong about jumps, vol smile. Each projection model has known limits. Mitigation: explicit model-uncertainty haircut as separate capital dimension.

33. **Our own market impact at scale.** When we liquidate, we move the market. Slippage models capture for current depth but not "the depth disappears when other large holders are doing the same thing." Recursive — we're part of the crash we're modeling.

---

## Part 7: Future work / Phase 2+ items

1. **Termbook + tUSDS / YT mechanism.** Needs tUSDS/YT split market — fixed-rate USDS holders on one side, variable-rate (YT) on the other. That market doesn't exist yet. Has its own design surface.

2. **Real auction system replacing fake auction.** Same interface, real bid evaluation. Tug-of-war for redistribution.

3. **Lindy measurement replacing manual structural demand allocation.** Real-time measurement of holder durations from chain data (USDS, DAI, sUSDS).

4. **Concentration L3.** Halobook category constraints + Primebook category constraints + system-wide concentration tracking.

5. **JAAA / CLO modeling.** Recursive exobook modeling for structured credit. Deferred from v1.

6. **Multi-tranche holdings.** Riskbooks holding senior + junior of same exobook. Mezzanine treatment.

7. **Multi-generator architecture.** Per-generator Genbook, Primebook serving multiple generators, cross-frame conversions at higher levels.

8. **Tranche rights / governance modeling.** Voting tranches, callable tranches, convertible tranches.

9. **Reinstating rate-hedging requirement** for matched positions (currently carved out for v1).

10. **TTM > 12 months matching.** Buckets 25-100 from duration-model.md become live.

11. **Sky-issued tranched products formalization.** Full LCTS catalog mapped into the tranched-book model.

12. **Sentinel formations integration with risk framework.** stl-base, stl-warden, stl-stream consuming the new risk computation outputs (Phase 9-10).

13. **Currency hedges in Hedgebook.** Cross-stablecoin depeg hedging at the portfolio level.

14. **Off-chain attestor reconciliation mechanism formalization.** Beyond the test attestor mechanism.

---

## Part 8: Key insights worth repeating

(Verbatim from the conversation, in case anything was missed above.)

**On the substrate:**
> Books + tranches + rules + stress scenarios + projection models = the genuinely complete pragmatic framework. The rules primitive is what makes the substrate Turing-complete-enough for financial contracts; projection models give us computational efficiency when rules are too heavy to inline.

**On gap risk:**
> Tranching + non-pegged assets + exoliabs together collapses gap risk into a special case of liquidity risk + tranche-waterfall propagation. Gap risk disappears as a separate concept. What remains: liquidity stress on the underlying asset, propagated through the tranche structure of the exobook the holder owns.

**On the equity invariant:**
> Every book has a designated equity tranche (always the most-junior, first-loss). The book is solvent iff equity > 0. When equity hits zero, an unwind procedure triggers. Real-time equity computation is the load-bearing invariant. This is the universal balance-sheet identity made structurally enforced rather than just a derived bookkeeping property.

**On the teleological grounding:**
> The framework's purpose is to answer one question — "could we liquidate everything we need to right now if a worst-case crash happened?" — to drive the binary decision: continue Prime / step in and liquidate. Most "limitations" of the substrate dissolve once you accept that any complex position can be projected into stress-loss numbers via best-available models.

**On currency:**
> The Riskbook is where external value enters the synomic accounting frame. Below the Riskbook, the world has its own denominations. At the Riskbook, you accept "this thing in frame X is worth Y in my frame, with stress profile Z." Above the Riskbook, everything is in the generator's frame.

**On layering:**
> Riskbook level: instrument→frame translation; tight hedges within single strategy. Halobook level: bundle liquidity adjustment (downgrade only). Primebook level: route into sub-book; Hedgebook captures portfolio-level hedges. Genbook level: concentration caps; system-wide aggregation. Each level has a specific role; each can adjust CRR via its own category catalog; default-deny everywhere preserves discipline.

**On sub-book risk-coverage contracts:**
> Each Primebook sub-book is a contract about which risks it covers. When a position lands in `termbook`, three of the four non-default risks become non-issues. In `structbook`, two are covered. In `tradingbook`, only default is intrinsic; the other three need capital. Default capital is always required because it's the irreducible loss.

**On hedgebook:**
> Hedgebook hedges are portfolio-level (broad-market hedges across diverse positions). Riskbook hedges are tactical and tight. The Hedgebook can only meaningfully evaluate hedges between positions that are already cleanly defined upstream — which is exactly what Riskbooks produce. The Hedgebook doesn't hand out hedge magic; it's a quantified residual-risk computation that explicitly models hedge failure modes.

**On asset-level liquidity profile:**
> For the framework to compose correctly, each terminal exo asset needs ONE canonical risk profile that downstream structures inherit. Without this, every category equation re-implements asset stress with potentially different assumptions, and consistency falls apart. This is the load-bearing primitive.

**On the platonic statement:**
> Books + tranches is genuinely close to a Platonic primitive — comparable to what double-entry accounting was for bookkeeping in the 14th century. It's the universal grammar of structural financial risk. The wisdom of the framework comes from knowing exactly where structure ends and other primitives begin.

---

## Appendix A: The complete updated entart tree (test scenario)

```
&core-root
  │
  └── &entity-guardian-ozone-root                              ← single operational guardian
        │
        ├── &entity-generator-usge-root                        ← USDS Generator
        │     ├── &entity-generator-usge-genbook
        │     └── &entity-generator-usge-structural-demand
        │           ├── &entity-generator-usge-structural-demand-scrapers
        │           └── &entity-generator-usge-structural-demand-auction
        │
        ├── &entity-prime-spark-root
        │     ├── &entity-prime-spark-primebook
        │     │     ├── &entity-prime-spark-primebook-ascbook
        │     │     ├── &entity-prime-spark-primebook-tradingbook
        │     │     ├── &entity-prime-spark-primebook-termbook
        │     │     ├── &entity-prime-spark-primebook-structbook        ← active in test
        │     │     ├── &entity-prime-spark-primebook-hedgebook
        │     │     └── &entity-prime-spark-primebook-unmatched
        │     └── &entity-halo-spark-crypto-lending-root
        │           ├── &entity-halo-spark-crypto-lending-halobook
        │           └── &entity-halo-spark-crypto-lending-riskbook-A   ← per-loan exobooks below
        │
        ├── &entity-prime-grove-root  → ...                            (similar structure)
        └── &entity-prime-obex-root   → ...                            (similar structure)

Per-loan exobooks (one per NFAT loan, registered in &core-registry-exo-book):
  exo-book spark-loan-001
    asset: eth N (custodial)
    tranches:
      - junior (exoliab, holder=borrower, denom=usd)
      - senior (held by spark riskbook, denom=usdc)
    rules:
      - liquidation trigger on health factor
      - maturity settlement
```

---

## Appendix B: Universal &core-* additions

Add to topology.md §6:
- `&core-framework-currency` — currency definitions (proxies, depeg profiles, FX stress)
- `&core-framework-asset-stress-profile` — per-asset canonical stress profiles
- (existing) `&core-framework-stress-scenarios` — scenario library
- (existing) `&core-framework-risk-categories` — category catalog (now richer with frame, projection-model, etc.)
- `&core-registry-currency` — currency identifier registry

---

## Appendix C: Reading order for someone catching up

If someone needs to understand this redesign cold, recommended order:

1. This document (`risk-framework-redesign-2026-05-03.md`) — the summary
2. Then in laniakea-docs/risk-framework/ (after edits land): risk-decomposition.md → book-primitive.md → tranching.md → currency-frame.md → primebook-composition.md → hedgebook.md → projection-models.md → matching.md → capital-formula.md → asset-type-treatment.md → examples.md
3. In noemar-synlang/ (after edits land): topology.md → risk-framework.md → settlement-cycle-example.md (with new test as example)

The conceptual heart is in the first 4 redesign docs (decomposition, book primitive, tranching, currency frame). Everything else specializes from those.
