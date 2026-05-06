# Riskbook Layer

**Status:** Draft (Phase 2 layer doc, 2026-05-05)

The Riskbook is the unit of regulation in the risk framework. It's the layer where matched categories produce CRR (Capital Ratio Requirement), where default risk is set entirely, where instrument-to-frame translation happens, and where tactical hedging within a single coherent strategy can earn capital relief.

Companion to:
- `book-primitive.md` — Riskbook is one specialization of the 6-tuple book
- `risk-decomposition.md` — default risk and cross-default → Riskbook constraint
- `currency-frame.md` — Riskbook as translation layer
- `tranching.md` — Riskbook holds tranche claims as its asset side
- `halobook-layer.md` — what sits above; pure aggregation across Riskbooks

---

## TL;DR

A Riskbook is:
- A book matching a registered category in `&core-framework-risk-categories`
- The unit at which **default risk** is fully determined
- The layer where **currency translation** to the Generator's frame happens
- The boundary at which **bankruptcy remoteness** sits in the Sky stack
- The natural home for **tactical hedging** within a single coherent strategy (e.g., ABF + CDS-on-same-ABF in one Riskbook)

Riskbooks without a matching category get CRR 100% (default-deny). Halobooks above never modify the Riskbook's default risk; that's structurally enforced (cross-default → Riskbook constraint per `risk-decomposition.md` §5).

---

## Section map

| § | Topic |
|---|---|
| 1 | Why the Riskbook is the unit of regulation |
| 2 | Composition constraints define what a Riskbook can hold |
| 3 | Default risk lives here entirely |
| 4 | Currency translation |
| 5 | Tactical hedging within a single Riskbook |
| 6 | Bankruptcy remoteness as the Riskbook boundary |
| 7 | The Riskbook category catalog as governance lever |
| 8 | Examples |
| 9 | One-line summary |

---

## 1. Why the Riskbook is the unit of regulation

Of the four book types in the synome stack (Riskbook, Halobook, Primebook, Genbook), only the Riskbook is **regulated by category match**. The others aggregate; the Riskbook is where governance writes the actual capital math.

Why this layer specifically:
- **Composability requires a unit.** Halos can compose anything they want. The Riskbook is the granularity at which "what is this composition, and how risky is it?" gets answered.
- **Categories require constraints.** A Riskbook category specifies what may be in the Riskbook, with what relationships and proportions. Without a category boundary, "this composition is recognized" has no meaning.
- **Bankruptcy remoteness needs a unit.** Cross-Riskbook netting is forbidden (per §6 below). That makes sense only if the Riskbook is the unit at which fates are linked.
- **Hedging needs a unit.** Tactical hedges (CDS protecting an ABF claim, perp shorting an ETH spot exposure) only get capital relief when the offsetting positions are in the same Riskbook with a category that recognizes the hedge.

Halos compete on three skills, all rooted in Riskbook composition: **sourcing** (finding good Exobooks to invoke), **composing** (fitting holdings into Riskbook categories with favorable equations), and **innovating** (proposing new Riskbook categories through governance when their strategy doesn't fit existing ones).

---

## 2. Composition constraints define what a Riskbook can hold

A Riskbook category isn't a label — it's a precise specification of what the Riskbook is allowed to hold. The `composition-constraints` clause is a synlang predicate over the Riskbook's contents that must evaluate to True.

Examples:

| Category | Constraint |
|---|---|
| `pure-eth-holding` | Exactly ETH, nothing else |
| `delta-neutral-eth-spot-perp` | Long ETH spot AND short ETH perp, balanced within tolerance |
| `abf-with-cds-cover` | Exactly one ABF claim + one CDS-on-same-ABF + ≥ 90% coverage |
| `morpho-lending` | Only exo units pointing to Morpho-shape Exobooks |
| `crypto-collateralized-USD-lending` | Senior tranches of BTC/ETH/stETH-collateralized exobooks; denoms in (USDC, USDT) |

These aren't sanity checks — they're **type constraints**. A Riskbook with the wrong composition fails category match and falls through to CRR 100%.

```metta
(risk-category-def abf-with-cds-cover
   (level riskbook)
   (composition-constraints
      (and (count-of (units-where (asset-class abf-claim)) = 1)
           (count-of (units-where (asset-class cds-cover)) = 1)
           (forall $cds (units-where (asset-class cds-cover))
                       (cds-references-credit-asset-in-same-book $cds))
           (>= (cds-notional / abf-notional) 0.90)))
   (variables [(coverage-ratio $cr) (cds-counterparty-rating $cprat)])
   (equation-m2m  ...stress-simulation...)
   (equation-htm  ...stress-simulation...)
   (resolution-tier simulation))
```

Default-deny is enforced by absence of match: if no category's `composition-constraints` evaluates True over the Riskbook's contents, no equation runs, and the Riskbook gets CRR 100%.

---

## 3. Default risk lives here entirely

> **The Halobook never modifies default risk. Default is set entirely at the Riskbook level.**

This is the architectural invariant from `risk-decomposition.md` §5. Any structural feature that would change joint-default behavior (cross-default clauses, joint-and-several obligations, mutual subordination) must be captured by composing the relevant positions in **a single Riskbook** with a category that understands their joint behavior.

Cross-Halobook default linkages are forbidden. Allowing them would mean Halobook category equations have to model joint-default behavior. Cleaner: force structurally-linked positions into one Riskbook.

This drives a clean operational alignment:
- Legal/operational ownership = Riskbook boundary = unit of joint-default modeling
- Cross-Halo cross-default would require a single Riskbook spanning both Halos → same Halo operationally owns the Riskbook (so it's not really cross-Halo anymore)

The default-risk constraint is what makes the four-book stack tractable. Without it, default math would have to thread through every layer; with it, default is computed once at the Riskbook and propagates as a fixed input upward.

---

## 4. Currency translation

The Riskbook is where messy reality enters the synomic accounting frame (per `currency-frame.md` §4):

> Below the Riskbook, the world has its own denominations (USDC positions, ETH collateral, real-world cash flows). At the Riskbook, you accept "this thing in frame X is worth Y in my frame, with stress profile Z." Above the Riskbook, everything is in the Generator's frame.

What the Riskbook does:
1. Accepts external assets in their native denominations (exo units pointing to USDC, ETH, real-world receivables, etc.)
2. Applies depeg/FX stress for cross-currency equivalences (USDC at 1.0 × USD with X% depeg stress at the severe scenario)
3. Translates to the Generator's frame
4. Issues Riskbook units that upstream books consume as frame-pure

The Riskbook also captures lots of capital efficiency through composition (CDS-protected ABF, delta-neutral spot/perp, etc.) — see §5.

---

## 5. Tactical hedging within a single Riskbook

Tactical hedges sit at the Riskbook level: specific-vs-specific within one coherent strategy. The hedge math is expressed by the Riskbook category equation, which knows the relationship between the two legs.

Examples:
- **ABF + CDS-on-same-ABF** — credit asset and its CDS coverage in one Riskbook. Equation: net loss = max(0, ABF default × loss − CDS counterparty-survival × CDS notional). Capital reflects counterparty residual, not naked credit.
- **Delta-neutral ETH spot/perp** — long spot, short perp, balanced. Equation: net exposure = residual basis × notional. Capital reflects basis risk, not directional ETH.
- **Convertible bond + short common stock** — bond and short hedge in one book. Equation: covers stock-leg movement; capital is for credit + residual.

The Halo's strategy is what it composes. A Halo that puts ABF in one Riskbook and CDS-on-same-ABF in a different Riskbook gets no hedge benefit; the synome can only recognize the offset when it's structurally captured in one category.

**Distinct from Hedgebook.** Riskbook hedges are tactical (one strategy, two legs). Hedgebook hedges are portfolio-level (broad-market hedges across diverse positions). See `hedgebook.md` for the latter.

---

## 6. Bankruptcy remoteness as the Riskbook boundary

Bankruptcy remoteness sits at the Riskbook level in the Sky stack. **A Riskbook is the unit of linked fate — positions inside it share bankruptcy and can hedge each other. Across Riskbooks, fates are unlinked, so no netting across boundaries.**

This gives a precise operational meaning to the often-vague "books are bankruptcy-remote ledgers" claim:
- The boundary is at the Riskbook level
- The Halobook holds Riskbook units and aggregates them, but doesn't merge their fates
- Halo-level capital adjustments via netting are not allowed

Cross-Riskbook correlation isn't credited at the Halobook level. If two Riskbooks suffer in the same crash (likely — both have credit-cycle exposure), the Halobook's composite RW reflects worst-case aggregate of independent calculations. The Halo doesn't get a netting benefit across Riskbooks because bankruptcy-remoteness forbids it.

This is intentional. Halos pay a real capital cost for the structural protection; the trade-off mirrors the legal/economic structure.

---

## 7. The Riskbook category catalog as governance lever

The catalog of registered Riskbook categories is **governance's primary risk-shaping tool**. It defines what kinds of strategies the synome recognizes and prices.

What governance can do via the catalog:
- **Add categories** to recognize new strategies (e.g., a new hedge structure becomes available; governance adds the category)
- **Tune equations** to reflect updated stress assumptions
- **Update composition constraints** as strategies evolve
- **Deprecate categories** that are no longer aligned with risk appetite
- **Adjust resolution tier** (math / simulation / heuristic) per category

Halos that want a new strategy either:
- Compose within an existing category
- Lobby governance to add a new category (governance-paced; slow but durable)
- Operate without category match (CRR 100%; high capital cost)

The catalog is itself a synart artifact in `&core-framework-risk-categories`. Updates flow through governance crystallization (per the `crystallization-interface` concept). This makes the catalog a governance-paced resource: high-stakes, low-velocity, durable.

---

## 8. Examples

### Pure ETH holding (math tier)

```metta
(risk-category-def pure-eth-holding
   (level riskbook)
   (composition-constraints
      (and (count-of (asset-class eth) >= 1)
           (count-of (asset-class != eth) = 0)))
   (equation-m2m (* (sum-of-notionals) (lookup-rw eth m2m)))
   (equation-htm (* (sum-of-notionals) (lookup-rw eth htm)))
   (resolution-tier math))
```

A Riskbook holding only ETH. The math tier resolves trivially: notional × ETH risk weight. No simulation required.

### ABF with CDS cover (simulation tier)

```metta
(risk-category-def abf-with-cds-cover
   (level riskbook)
   (composition-constraints ...)
   (equation-m2m
      (simulate-across-scenarios m2m-scenarios
         (lambda ($scenario)
            (let* (($abf-default-prob (apply-credit-stress $scenario))
                   ($cds-effective-payout
                      (* (cds-notional)
                         (cds-counterparty-survival-prob $cprat $scenario))))
              (/ (* $abf-default-prob
                    (max 0 (- (abf-notional) $cds-effective-payout)))
                 (abf-notional))))
         (combiner take-worst)))
   (resolution-tier simulation))
```

The CDS effectively transforms a high-risk credit position (would be ~12% RW unhedged) into a much lower risk position (~4-5% RW). The remaining risk is **counterparty residual** — the risk that the CDS issuer fails to pay. This is what hedge-categorization buys: substantial RW reduction in exchange for accepting a different (much smaller) risk in the form of counterparty residual.

### Crypto-collateralized USD lending (v1 test category)

```metta
(risk-category-def crypto-collateralized-USD-lending
   (level riskbook)
   (frame usd)
   (composition-constraints
     (and (single-senior-tranche-positions)
          (asset-class-in (eth btc stETH))
          (denom-in (usdc usdt))))
   (equation-m2m
     (sum-over (held-senior-tranches)
       (lambda ($pos)
         (let* (($asset-stress-profile (asset-stress-profile (collateral-of $pos)))
                ($denom-depeg          (depeg-stress-profile (denom-of $pos)))
                ($junior-cushion       (junior-tranche-size (exobook-of $pos))))
           (simulate-across-scenarios m2m-scenarios
             (lambda ($s)
               (let* (($asset-drop      (apply-scenario $s $asset-stress-profile))
                      ($depeg-loss      (apply-scenario $s $denom-depeg))
                      ($effective-loss  (max 0 (- $asset-drop $junior-cushion))))
                 (+ $effective-loss $depeg-loss))))))))
   (resolution-tier simulation))
```

The standard structured-product capital model — no special "gap risk" treatment needed, because gap risk has unified into asset-liquidity stress through the tranche waterfall (per `tranching.md` §6).

---

## 9. One-line summary

**The Riskbook is the unit of regulation: it must match a registered category or get CRR 100% (default-deny); default risk and currency translation live here entirely; tactical hedging within a single coherent strategy earns capital relief through category-aware equations; bankruptcy remoteness sits at the Riskbook boundary, so cross-Riskbook netting is forbidden; the category catalog is governance's primary risk-shaping lever.**

---

## File map

| Doc | Relationship |
|---|---|
| `book-primitive.md` | Riskbook is a specialization of the 6-tuple book |
| `risk-decomposition.md` | Default risk lives at Riskbook layer; cross-default constraint |
| `tranching.md` | Riskbook holds tranche claims as its asset side |
| `currency-frame.md` | Riskbook is the translation layer |
| `halobook-layer.md` | What sits above; pure aggregation; bundle exposure structure |
| `correlation-framework.md` | Concentration limits sit one level higher (Primebook + Genbook) |
| `capital-formula.md` | Riskbook RW propagates upward through the stack |
| `examples.md` | Worked v1 test scenario uses the categories sketched in §8 |
