# Risk Framework — Books, Categories, Simulations

How risk is computed across the synome. The four-book taxonomy
(Primebook / Halobook / Riskbook / Exobook) gives each level a specific
job; the category framework provides the equations; stress simulation
is the canonical mechanism for evaluating those equations against real
worst-case scenarios; loop and recursion handling provides a graceful
fallback when math can't resolve the structure cleanly.

Companion to:
- `topology.md` (Space layout — `&core-framework-risk-*` and `&core-registry-exo-book` live here)
- `syn-tel-emb.md` §1 (synart commons — categories and stress scenarios are open-source SOTA)
- `synlang-patterns.md` §1-§3 (the conservation-network framing — books as nodes, units as edges)
- `settlement-cycle-example.md` (worked settlement; uses old state-based CRR; pending update — see §9)
- `synart-access-and-runtime.md` (how exo book state gets pushed through the gate)

---

## TL;DR

The model rests on a few decisions:

**Books come in four kinds, each with a specific job.**

| Book type | Job | Issues units to | Holds (asset side) |
|---|---|---|---|
| **Primebook** | Aggregate across Halos; clean face to Generator | Generator | Halobook units |
| **Halobook** | Aggregate across Riskbooks; clean face to Prime | Primebook | Riskbook units |
| **Riskbook** | Resolve risk to finality (load-bearing computation lives here) | Halobook | Exo units + raw exo assets + (rarely) endo units from other Riskbooks |
| **Exobook** | Map external financial engineering into categorizable structures | Riskbook (entry into synome) | Other exo units (recursive) + exo assets |

(Generatorbook implicitly sits above Primebook — receives Primebook units, issues USDS. Out of scope for this doc.)

**Risk is content-derived via three category types.**

| Category type | Applies to | What the equation does |
|---|---|---|
| **Exo asset category** | Terminal exo assets (ETH, USDC, etc.) | Returns base risk weight (degenerate equation) |
| **Exobook category** | Exobooks — infrastructure pattern | Returns risk weight for the Exobook's exo units, walking its asset side recursively |
| **Riskbook category** | Riskbooks — *load-bearing economic citizens* | Returns finality CRR for the Riskbook's endo units, evaluating the composition under stress |

**Riskbook categories are the unit of regulation.** A Riskbook MUST
match a registered Riskbook category. Riskbooks not matching get CRR
100% (default-deny). The category catalog is governance's primary
risk-shaping lever.

**Equations are stress simulations, not static formulas.** Each
category equation evaluates the Riskbook composition (or Exobook
state) under a library of stress scenarios, computing expected loss.
Risk weights reflect worst-case real claim to real assets after
correlated crash.

**Four-tier resolution hierarchy.** When computing risk, the framework
attempts:

1. **Mathematical resolution** — closed-form analytic where possible
2. **Stress simulation** — forward-propagate scenarios through the structure
3. **Heuristic estimation** — overestimating fallback when structure is opaque
4. **Max-risk default** — CRR 100% when nothing else works

**Dual M2M and HTM propagation.** Every level always computes both
M2M and HTM risk weights. The Prime book picks per-position which
treatment applies based on liquidity strategy.

**State maintenance: govops live, endoscrapers verify.** The Halo's
accordant govops pushes exo book state continuously. Synserv-run
endoscrapers read chain directly and reconcile. Disagreements escalate.

**State-based CRR is gone.** The original `(crr filling 5)` /
`(crr deploying 100)` table doesn't exist. Lifecycle phases now
manifest as different exo units pointing to different exo books with
different categories.

---

## Section map

| § | Topic |
|---|---|
| 1 | Books and units — the four-book taxonomy |
| 2 | Recursive composition of exo books — infrastructure for Riskbook categories |
| 3 | The category framework — three category types |
| 4 | Riskbook categories as the unit of regulation |
| 5 | The unit-risk-weight calculation — per-book-type computation flow |
| 6 | Stress simulation as the canonical equation type |
| 7 | The four-tier resolution hierarchy |
| 8 | Loop and recursion handling |
| 9 | What state-based CRR was and why it's gone |
| 10 | The govops / endoscraper division of state responsibility |
| 11 | The CRR-100% default mechanism |
| 12 | Worked examples |
| 13 | Open design questions |
| 14 | One-line summary |

---

## 1. Books and units — the four-book taxonomy

### Each level has a specific job

The four book types form a stack from external messy reality to clean
aggregate exposure at the top:

```
       Generator (USDS holders)
           ↑ holds USDS (= claims against Generatorbook, out of scope here)
       Generatorbook
           ↑ holds Primebook units; issues USDS
       Primebook
           ↑ holds Halobook units; issues units to Generator
       Halobook
           ↑ holds Riskbook units; issues units to Prime
       Riskbook       ← finality CRR computed here
           ↑ holds exo units + raw exo assets; issues units to Halo
       Exobook        ← recursive composition lives here
           ↑ holds other exo units + exo assets; issues units recursively
       Exo asset      ← terminal, irreducible
```

**Bankruptcy remoteness lies above the Riskbook level.** A Riskbook is
the unit of linked fate — positions inside it share bankruptcy and can
hedge each other. Across Riskbooks, fates are unlinked, so no netting
across boundaries. This gives a precise operational meaning to "books
are bankruptcy-remote ledgers" — the boundary is at the Riskbook level.

### Book types in detail

**Primebook** (`&entity-prime-<id>-primebook`)

- Aggregates Halobook units from all Halos governed by this Prime
- Issues endo units up to Generatorbook
- No risk transformation, just aggregation
- Concentration tracking eventually lives here (deferred — see §13)

**Halobook** (`&entity-halo-<id>-halobook`)

- Aggregates Riskbook units from all Riskbooks owned by this Halo
- Issues endo units up to Primebook
- No hedging at this level — bankruptcy-remoteness across Riskbooks
  forbids it
- Pure aggregation

**Riskbook** (`&entity-halo-<id>-riskbook-<rb-id>`)

- The unit of regulation. Each Riskbook matches a registered Riskbook
  category that constrains its composition
- Holds exo units, raw exo assets, occasionally endo units from other
  Riskbooks
- Issues endo units (with finality CRR) up to Halobook
- This is where hedge-shaped risk reductions can be earned (via
  Riskbook categories whose equations recognize offsetting positions)
- A Halo typically has multiple Riskbooks, each fitting a coherent
  strategy

**Exobook** (`&core-registry-exo-book` entries — universal)

- Synome doesn't control these; only monitors them
- Each Exobook matches an Exobook category that supplies an equation
  for computing the risk weight of its issued exo units
- Composition can be recursive — Exobooks holding exo units pointing
  to other Exobooks
- Bottoms out at exo assets (terminal categories)

### Units mirror the book taxonomy

| Unit type | Issuer | Where held |
|---|---|---|
| Endo unit | Primebook / Halobook / Riskbook (any synome-controlled book) | Held as asset by upstream book or by USDS holders (for Generator-issued USDS) |
| Exo unit | Exobook | Held as asset by Riskbooks or by other Exobooks (recursive) |
| Exo asset | (no issuer — terminal) | Held as asset by any book that holds raw assets directly |

Books hold units (and possibly exo assets) on their **asset side** and
issue units on their **liability side**. The conservation-network
framing from `synlang-patterns.md` §1 is preserved — books balance,
units bridge — just with richer typing.

### What lives in each book's atoms

```metta
;; ──── &entity-halo-spark-credit-riskbook-A ────
(book-type riskbook)
(book-category abf-with-cds-cover)                       ; the Riskbook category
(parent-halobook spark-credit-halobook)
(holds (exo-unit u-001) abf-deal-X 1000000)              ; ABF claim, $1M notional
(holds (exo-unit u-002) cds-on-abf-deal-X 950000)        ; CDS coverage, $950k notional
(issues (endo-unit u-rb-a-bond) (notional 1000000))      ; the finality unit going up

;; ──── &entity-halo-spark-credit-halobook ────
(book-type halobook)
(parent-primebook spark-primebook)
(sub-riskbook spark-credit-riskbook-A &entity-halo-spark-credit-riskbook-A)
(sub-riskbook spark-credit-riskbook-B &entity-halo-spark-credit-riskbook-B)
(holds (endo-unit u-rb-a-bond) 1000000)                  ; from Riskbook A
(holds (endo-unit u-rb-b-bond) 2000000)                  ; from Riskbook B
(issues (endo-unit u-hb-bond) (notional 3000000))

;; ──── &entity-prime-spark-primebook ────
(book-type primebook)
(parent-generator spark-generator-interface)
(sub-halobook spark-credit-halobook ...)
(sub-halobook spark-trade-halobook  ...)
(holds (endo-unit u-hb-bond) 3000000)
(holds ...)
```

Registries connect levels: `(sub-riskbook ...)` in a Halobook lists
all Riskbooks under it; `(sub-halobook ...)` in a Primebook lists all
Halobooks. Same registry pattern as the entart tree per
`topology.md` §12.

---

## 2. Recursive composition of exo books — infrastructure for Riskbook categories

Exobooks are reusable infrastructure components. They don't carry
economic meaning on their own — a Morpho market exobook doesn't "mean"
anything until a Riskbook category invokes it. Their job is to give
Riskbook categories well-formed, categorizable references to external
structures.

### Exobook recursion in practice

Consider a Morpho vault holding positions in multiple Morpho markets,
each backed by collateral assets:

```
Halo's Riskbook (category: morpho-lending)
   asset side:
      exo unit → morpho-eth-vault                            ; 1.0M USDS notional

&core-registry-exo-book entries (recursive):
   morpho-eth-vault      (category morpho-vault, depth 0)
      exo-book-holds morpho-market-X 0.40                    ; 40% allocation
      exo-book-holds morpho-market-Y 0.60                    ; 60% allocation
   
   morpho-market-X       (category morpho-market, depth 1)
      exo-book-holds (borrower-position-1) ...
      exo-book-holds (borrower-position-2) ...
   
   morpho-market-Y       (category morpho-market, depth 1)
      ...
   
   borrower-position-1   (category morpho-borrow-position, depth 2)
      exo-book-asset eth 150                                  ; 150 ETH collateral
      exo-book-liability owed-to-morpho-X 100                 ; 100 ETH-equiv debt
   
   ...further borrower positions...
   
   eth                   (category eth, depth 3, TERMINAL)
   wbtc                  (category wbtc, depth 3, TERMINAL)
```

Each Exobook in the chain has a category. The category provides the
equation for computing that Exobook's risk weight, which usually
involves recursing into the Exobook's children.

### Recursion termination

Recursion ends at exo assets — registered Exobook entries whose
category is **terminal** (e.g., `eth`, `usdc`, `wbtc`, `treasury-bill-direct`).
Terminal categories have a base risk weight and no children to recurse
into.

### Why this is "infrastructure"

Exobook categories are useful but not *economically* meaningful in
isolation. The economic meaning lives one level up — in the Riskbook
category that *invokes* an Exobook. A Riskbook of category `morpho-
lending` says "I'm a Riskbook that holds a morpho-vault exo unit and
that's all I do." The Riskbook category equation is what matters
economically; the Exobook is just structured reference data the
equation reads.

This is why Exobook design is purely structural and why Exobook
categories are about pattern recognition for external structures
rather than risk strategy. The strategy lives at the Riskbook level.

### Loops and depth

The recursion can encounter cycles (Vault A holds Vault B holds Vault A)
or deep nesting. Section 8 details how the framework handles these via
the four-tier resolution hierarchy (§7) — when math can't resolve,
heuristics overestimate.

---

## 3. The category framework — three category types

All categories live in `&core-framework-risk-categories`. They share
a common shape (parameterized equations with input requirements) but
apply at different levels.

### Common shape

Every category atom contains:

```metta
(risk-category-def $name
   (level <exo-asset | exobook | riskbook>)
   (variables [<named inputs needed at evaluation>])
   (equation-m2m  <synlang form taking variables → CRR>)
   (equation-htm  <synlang form taking variables → CRR>)
   (resolution-tier <math | simulation | heuristic | max-risk>)
   (composition-constraints <only for riskbook level>)
   (description "...")
)
```

The `equation-m2m` and `equation-htm` may be:

- **Static formulas** (rare; only for simple categories like
  `pure-stablecoin-holding`)
- **Stress simulations** that propagate scenarios through the
  structure (typical)
- **References to mathematical solvers** for closed-form-resolvable
  structures (Morpho-shaped lending, where the rules are deterministic)

### Type 1: Exo asset categories (terminal)

Simplest case. Fixed risk weights for irreducible holdings.

```metta
(risk-category-def eth
   (level exo-asset)
   (variables [])
   (equation-m2m (constant 0.25))
   (equation-htm (constant 0.20))
   (resolution-tier math)
   (description "Native ETH on Ethereum; market liquidation recourse"))

(risk-category-def usdc
   (level exo-asset)
   (variables [])
   (equation-m2m (constant 0.05))
   (equation-htm (constant 0.04))
   (resolution-tier math)
   (description "USDC stablecoin; Circle redemption recourse"))

(risk-category-def treasury-bill-direct
   (level exo-asset)
   (variables [])
   (equation-m2m (constant 0.02))
   (equation-htm (constant 0.005))
   (resolution-tier math)
   (description "Direct US Treasury bill holding"))
```

M2M is higher than HTM for nearly all assets — mark-to-market
sensitivity exposes more volatility than buying-and-holding.

### Type 2: Exobook categories (infrastructure)

These categories represent *external structures* the synome monitors.
The equation walks into the Exobook's own assets/liabilities and
computes risk based on observed state.

```metta
(risk-category-def morpho-market
   (level exobook)
   (variables [(state $book) (collateralization-data $cdata) (liquidation-rules $rules)])
   (equation-m2m
      (simulate-loss-under-scenarios m2m-scenarios
         (lambda ($scenario)
            (let* (($collateral-after (apply-stress $cdata $scenario))
                   ($debt-survives (apply-debt-stress $book $scenario))
                   ($recovery (compute-recovery $collateral-after $debt-survives $rules)))
              (- 1.0 (/ $recovery (debt-of $book)))))
         (combiner take-worst)))
   (equation-htm
      ;; over-time perspective; uses different scenario set with longer horizons
      (simulate-loss-under-scenarios htm-scenarios ...))
   (resolution-tier simulation)
   (description "Morpho lending market; deterministic liquidation rules; simulation-resolvable"))

(risk-category-def morpho-vault
   (level exobook)
   (variables [(state $book) (allocations $allocs)])
   (equation-m2m
      ;; iterate child markets, compute their risks under same scenario, weighted by allocation
      ...)
   (resolution-tier simulation)
   (description "Morpho vault layered on top of markets"))

(risk-category-def custody-major
   (level exobook)
   (variables [(custodian $c) (counterparty-rating $cr) (jurisdiction $j)])
   (equation-m2m ...)
   (resolution-tier simulation)
   (description "Major custody counterparty (BNY, State Street, Coinbase Custody, etc.)"))
```

Exobook categories are *structural patterns*. They exist in the
catalog because Riskbook categories want to reference well-known
structures — when a Riskbook category equation says "consult the
underlying Morpho market's risk," it's invoking an Exobook category to
get a structured answer.

### Type 3: Riskbook categories (the load-bearing economic citizens)

This is where actual financial economics is encoded. A Riskbook
category specifies:

- **Composition constraints** — what units may be in this Riskbook,
  with what relationships, what proportions
- **Equation per treatment** — typically stress simulation
- **Variables** — economic parameters needed at evaluation

```metta
(risk-category-def abf-with-cds-cover
   (level riskbook)
   (variables [(coverage-ratio $cr) (cds-counterparty-rating $cprat)])
   (composition-constraints
      (and (count-of (units-where (asset-class abf-claim)) = 1)
           (count-of (units-where (asset-class cds-cover)) = 1)
           (forall $cds (units-where (asset-class cds-cover))
                       (cds-references-credit-asset-in-same-book $cds))
           (>= (cds-notional / abf-notional) 0.90)))
   (equation-m2m
      (simulate-across-scenarios m2m-scenarios
         (lambda ($scenario)
            (let* (($abf-default-prob (apply-credit-stress $scenario))
                   ($cds-payout-effective
                      (* (cds-notional)
                         (cds-counterparty-survival-prob $cprat $scenario)))
                   ($expected-loss
                      (* $abf-default-prob
                         (max 0 (- (abf-notional) $cds-payout-effective)))))
              (/ $expected-loss (abf-notional))))
         (combiner take-worst)))
   (equation-htm
      ;; HTM treatment less M2M-sensitive; uses different scenarios + horizons
      ...)
   (resolution-tier simulation)
   (description "Asset-backed finance claim with tokenized CDS coverage from approved counterparty"))

(risk-category-def delta-neutral-eth-spot-perp
   (level riskbook)
   (variables [(basis-tolerance-bps $bt) (perp-counterparty $pc)])
   (composition-constraints
      (and (exists $u (units-where (asset-class eth-spot)))
           (exists $u (units-where (asset-class eth-perp-short)))
           (within-balance (long-eth-notional) (short-eth-notional) $bt)))
   (equation-m2m ...)
   (equation-htm ...)
   (resolution-tier simulation))

(risk-category-def pure-eth-holding
   (level riskbook)
   (variables [])
   (composition-constraints
      (and (count-of (asset-class eth) >= 1)
           (count-of (asset-class != eth) = 0)))
   (equation-m2m
      (* (sum-of-notionals) (lookup-rw eth m2m)))            ; just the eth RW
   (equation-htm
      (* (sum-of-notionals) (lookup-rw eth htm)))
   (resolution-tier math)                                    ; closed-form
   (description "Riskbook holding only direct ETH"))

(risk-category-def morpho-lending
   (level riskbook)
   (variables [])
   (composition-constraints
      (and (count-of (units-pointing-to-exobook (category morpho-market or morpho-vault)) >= 1)
           (count-of (other-asset-classes) = 0)))
   (equation-m2m
      ;; recurse into the Morpho structure via the Exobook category equations
      (sum-over (held-units)
         (lambda ($u)
            (* (notional $u) (exobook-risk-rate (issuer-of $u) m2m))))))
   (resolution-tier simulation)
   (description "Riskbook holding only Morpho lending positions"))
```

Riskbook categories define what kinds of strategies the synome
recognizes and prices. Halos compete on selecting + composing
categories well; governance owns the catalog.

---

## 4. Riskbook categories as the unit of regulation

The Riskbook is the regulatory unit. This deserves explicit treatment
because it's structurally different from how risk works in most
systems.

### Composition constraints are precise

A Riskbook category isn't a label — it's a precise specification of
what the Riskbook is allowed to hold. The `composition-constraints`
clause is a synlang predicate over the Riskbook's contents that must
evaluate to True.

Example constraints from the categories above:

| Category | Constraint |
|---|---|
| `pure-eth-holding` | Exactly ETH, nothing else |
| `delta-neutral-eth-spot-perp` | Long ETH spot AND short ETH perp, balanced within tolerance |
| `abf-with-cds-cover` | Exactly one ABF unit + one CDS-on-same-ABF + ≥ 90% coverage |
| `morpho-lending` | Only exo units pointing to Morpho-shape Exobooks |
| `tranched-credit-senior` | Only senior tranche units of a single underlying credit pool |

These aren't just sanity checks — they're **type constraints**. A
Riskbook with the wrong composition fails category match.

### Default-deny: no match → CRR 100%

This is the load-bearing pattern. If a Riskbook's contents don't
match any registered category, the Riskbook gets CRR 100% on its
issued units. The Halo is free to compose anything they want, but the
synome only gives favorable risk treatment to compositions that fit a
governance-vetted category.

```metta
(= (riskbook-finality-crr $book)
   (let (($matched-cat (find-matching-category $book)))
     (case $matched-cat
       ((no-match  1.0)                                    ; CRR 100%
        ($cat (eval-category-equation $cat $book))))))
```

This forces:

- **Halos** to either work within categories or lobby governance
- **Governance** to keep the catalog comprehensive enough to cover
  legitimate strategies
- **Innovation** to flow through the proposal-and-crystallization gate
  rather than ad-hoc

This is the same default-deny pattern as elsewhere in the synome
(verb whitelists, recipe catalogs, runtime registry, telseed catalog).
Risk follows it.

### Halo strategy as Riskbook composition

A Halo's strategy decomposes into:

1. Which Riskbook categories does this Halo's strategy fit into?
2. How many Riskbooks of each category does the Halo run?
3. What's the allocation across Riskbooks?

The Halobook just aggregates — no creative work. The strategic work
is at the Riskbook level (selecting categories, composing within them)
and at the sourcing level (finding good Exobooks to invoke).

### Halo competition

Halos compete on three skills:

- **Sourcing** — finding well-categorized Exobooks (good Morpho
  markets, well-rated ABF deals, reliable CDS counterparties)
- **Composing** — fitting holdings into Riskbook categories with
  favorable equations (CDS-covered credit instead of naked credit;
  delta-neutral hedged instead of directional)
- **Innovating** — proposing new Riskbook categories through governance
  when their strategy doesn't fit existing ones

The first two are operational competence; the third creates new market
structures and is governance-paced (slow but durable when accepted).

---

## 5. The unit-risk-weight calculation — per-book-type computation flow

The risk computation cleanly decomposes by book type. Each level has
its own role.

### Top-down view

```
Primebook risk-weight = sum-of-asset-side(Halobook units × their RW)
                         (pure aggregation)

Halobook risk-weight  = sum-of-asset-side(Riskbook units × their RW)
                         (pure aggregation)

Riskbook RW (M2M)     = if matched-category:
                            evaluate category.equation-m2m against composition
                        else:
                            CRR = 100%

Riskbook RW (HTM)     = if matched-category:
                            evaluate category.equation-htm against composition
                        else:
                            CRR = 100%

Exobook RW (M2M)      = evaluate category.equation-m2m against state
                        (typically recursive into child exo units)

Exobook RW (HTM)      = evaluate category.equation-htm against state

Exo asset RW          = look up category in catalog → base RW
                        (terminal; no recursion)
```

Two levels do real work:

- **Riskbook level** — category match + equation evaluation produces
  finality CRR
- **Exobook level** — category equation evaluates the Exobook's state,
  often recursively walking into child Exobooks

Halobook and Primebook are pure aggregators.

### Synlang form

```metta
(= (book-risk-weight $book $treatment)              ; treatment ∈ {m2m, htm}
   (case (book-type-of $book)
     ((primebook  (aggregate-children $book sub-halobook $treatment))
      (halobook   (aggregate-children $book sub-riskbook $treatment))
      (riskbook   (riskbook-finality-rw $book $treatment))
      (exobook    (exobook-rw $book $treatment)))))

(= (aggregate-children $book $relation $treatment)
   (sum-over (children-via $book $relation)
      (lambda ($child)
         (* (notional-held $book $child)
            (book-risk-weight $child $treatment)))))

(= (riskbook-finality-rw $book $treatment)
   (let (($cat (find-matching-category $book)))
     (case $cat
       ((no-match  (notional-of-issued-units $book))           ; CRR = 100%, RW = full notional
        ($c (* (notional-of-issued-units $book)
               (eval-equation $c $book $treatment)))))))

(= (exobook-rw $book $treatment)
   (let (($cat (exobook-category $book)))
     (eval-equation $cat $book $treatment)))
```

### M2M and HTM both always

Every level always computes both. The Prime book picks per-position
which to use based on liquidity treatment. The exo book itself doesn't
know whether a given holder is treating it M2M or HTM — it propagates
both upward continuously.

### Where the M2M/HTM decision actually happens

At the Primebook level, when the Prime decides how to treat each
incoming Halobook unit:

```metta
;; in &entity-prime-spark-primebook
(treatment-for spark-credit-halobook-unit-001 m2m)
(treatment-for spark-trade-halobook-unit-002 htm)

(= (primebook-rw $primebook $treatment-mode)
   (sum-over (held-halobook-units $primebook)
      (lambda ($u)
         (let (($treatment-for-u (treatment-for $u)))
           (* (notional-held $primebook $u)
              (book-risk-weight (issuer-of $u) $treatment-for-u))))))
```

The `treatment-for` decision is governance and operational (Prime
decides per-position based on liquidity strategy). Both numbers always
flow up; the Prime selects.

---

## 6. Stress simulation as the canonical equation type

Most category equations are **stress simulations**, not static
formulas. This means a category equation, given a Riskbook's
composition or an Exobook's state, runs forward simulations across a
library of stress scenarios and computes expected loss.

### Why simulation over formulas

The fundamental risk question:

> In a correlated crash where lots of bad things happen at once,
> what real claim do I have to real assets that survive?

A static formula can't answer this — it doesn't know about
correlations, cascading failures, counterparty defaults under stress.
A simulation can:

- Apply a coordinated stress scenario across all dimensions
- Propagate the stress through the structure (downstream effects)
- Compute what's left of the original claim
- Repeat across multiple scenarios; take worst-case (or
  probability-weighted)

The output is a CRR that reflects "expected loss in the worst plausible
real-world failure mode."

### Stress scenario library

Lives in `&core-framework-stress-scenarios` (universal, replicated).
Each scenario is a parameter vector:

```metta
(stress-scenario-def severe-correlated-crash
   (description "2008-style coordinated crash across crypto + traditional")
   (params
      (eth-drop -0.55)
      (btc-drop -0.45)
      (stable-major-depeg-prob 0.05)
      (credit-spreads-widen-bps 800)
      (correlation-uplift 1.6)
      (defi-protocol-risk-uplift 1.8)
      (custody-counterparty-default-prob 0.02)
      (real-estate-residential-drop -0.30)
      ;; ... full vector
      ))

(stress-scenario-def credit-crisis
   (description "Credit-cycle-led downturn; less crypto-correlated")
   (params ...))

(stress-scenario-def liquidity-crisis
   (description "Sudden liquidity withdrawal; M2M stress without solvency stress")
   (params ...))

(stress-scenario-def stable-conditions
   (description "Base case; no major stress")
   (params (all-stress-uplift 0.0)))

;; ... library of 10-20 scenarios covering different failure modes
```

Categories declare which scenarios their equations apply:

```metta
(risk-category-def abf-with-cds-cover
   ...
   (m2m-scenarios [severe-correlated-crash credit-crisis liquidity-crisis])
   (htm-scenarios [severe-correlated-crash credit-crisis])
   ...)
```

The category's M2M equation evaluates against the M2M scenario set;
the HTM equation against the HTM set. Different scenario sets per
treatment because M2M cares about volatility/liquidity stress while
HTM cares more about ultimate solvency.

### Simulation propagation

A category equation's simulation typically does:

```
for each scenario S in this category's scenarios:
   for each held unit u in this Riskbook:
      // recursively get u's expected loss under S
      // by invoking u's issuer's category equation under S
      losses[u] = recurse-into-child-exo-or-asset(u, S)
   
   // apply this category's specific composition logic
   // (offsetting positions, subordination, hedging, etc.)
   composed-loss[S] = compose-losses-per-category-rules(losses, S)

// take worst case (or probability-weighted, depending on category)
final-rw = max-or-weighted(composed-loss across S)
```

The "compose-losses-per-category-rules" is where each Riskbook
category's specific economic logic lives. For `abf-with-cds-cover`:
the CDS payoff is conditional on the CDS counterparty surviving the
scenario; the net loss is `max(0, ABF-loss - CDS-effective-payout)`.
For `tranched-credit-senior`: losses absorb to junior tranches first.
For `delta-neutral-spot-perp`: long and short ETH offset directly,
with residual basis risk applied as a small haircut.

### Real-time updates

Risk weights aren't snapshots — they recompute as inputs change. The
data flow:

```
endoscrapers (live chain reads)        ┐
                                        ├─→ &core-registry-exo-book state updates
halo govops (state pushes through gate)┘             ↓
                                              triggers re-evaluation of
                                              affected category equations
                                                     ↓
                                              updated risk weights propagate
                                              up through Halobook → Primebook
                                                     ↓
                                              consumers (Sentinels, settlement)
                                              read current weights
```

State changes can come from many sources:

- Endoscraper detects collateralization change in a Morpho market
- Halo govops pushes new Riskbook composition (added a new unit)
- New stress scenario crystallized into the library
- Category equation updated through governance crystallization

Each triggers cascading recomputation upward through the stack.

### Push vs pull evaluation

Category equations can be either:

- **Push-evaluated** — recompute on every input change; cache result
  in synart (e.g., `(current-rw $book m2m 0.43)`)
- **Pull-evaluated** — only compute when a consumer asks; expensive
  categories may use this
- **Hybrid** — hot risk weights pushed; cold ones pulled

This is a per-category configuration. The framework supports both.

### Computational cost

Stress simulation is more expensive than static formulas. Categories
mark their `resolution-tier`; runtime can use cheaper tiers when
simulation is unnecessary, or budget computation per-category. See
`scaling.md` for the operational implications.

---

## 7. The four-tier resolution hierarchy

Risk computation for any structure proceeds through tiers, falling
through when each fails:

| Tier | What | When it works | Example |
|---|---|---|---|
| **1. Mathematical resolution** | Closed-form analytic | Structure is simple and tractable | `pure-eth-holding`: just `notional × eth-rw` |
| **2. Stress simulation** | Forward-propagate scenarios | Structure is well-modeled but no closed form | `morpho-lending`: simulation walks the borrower positions |
| **3. Heuristic estimation** | Loop / depth / repetition penalties biased to overestimate | Structure is opaque, cyclic, or too deep | A vault-of-vaults with circular references |
| **4. Max-risk default** | CRR = 100% | Structure can't be reasoned about at all | Riskbook with no matching category; Exobook beyond MAX_RECURSION_DEPTH |

Each category equation declares the tiers it supports via
`resolution-tier`. The framework attempts the highest tier first;
falls through on failure.

### Per-category tier preferences

```metta
(risk-category-def pure-eth-holding
   ...
   (resolution-tier math))                                    ; tier 1 always

(risk-category-def morpho-market
   ...
   (resolution-tier simulation))                              ; tier 2; falls to 3 on failure

(risk-category-def opaque-structured-product
   ...
   (resolution-tier heuristic))                               ; tier 3; max-risk on failure
```

### Tier-1 (math) sketch

Used for categories whose equations are linear or have closed-form
fixed-point solutions:

```metta
(= (eval-equation-tier1 $cat $book $treatment)
   (case (analytic-form-of $cat $treatment)
     ((closed-form (apply-formula $cat $book))
      (linear-system (solve-linear-system $cat $book))
      (none Error))))
```

Loops in a linear system can sometimes be solved as fixed-point
equations — `X = AX + B` solves to `X = (I - A)^{-1} B` if `(I - A)`
is invertible. This works for some compounding structures.

### Tier-2 (simulation) sketch

The default for most non-trivial categories:

```metta
(= (eval-equation-tier2 $cat $book $treatment)
   (let (($scenarios (m2m-or-htm-scenarios $cat $treatment))
         ($combiner (combiner-of $cat))
         ($losses (collapse
                    (map (lambda ($s) (simulate-loss $cat $book $s))
                         $scenarios))))
     (apply-combiner $combiner $losses)))
```

Where `combiner-of` is per-category — `take-worst` is conservative,
`probability-weighted-mean` averages.

### Tier-3 (heuristic) sketch

For genuinely opaque structures. Conservative biases:

```metta
(= (eval-equation-tier3 $cat $book $treatment)
   (let* (($best-effort-rw (best-effort-estimate $cat $book $treatment))
          ($depth (recursion-depth-of $book))
          ($depth-penalty (* $depth (depth-penalty-per-level)))
          ($cycle-penalty (case (cycle-detected $book)
                            ((True (loop-penalty-multiplier))
                             (False 1.0))))
          ($repeat-penalty (case (repeated-terminals $book)
                             ((True (repeated-terminal-penalty))
                              (False 1.0)))))
     (min 1.0
          (* $best-effort-rw $cycle-penalty $repeat-penalty
             (+ 1.0 $depth-penalty)))))
```

Key heuristic parameters live in `&core-framework-risk` (governance-
tunable):

```metta
(loop-penalty-multiplier 1.5)
(depth-penalty-per-level 0.05)
(max-recursion-depth 8)
(repeated-terminal-penalty 1.3)
```

### Tier-4 (max-risk) — the final fallback

Anywhere the prior tiers fail, return CRR 100%. This guarantees the
calculation always terminates and never produces unsafely-low risk
weights.

---

## 8. Loop and recursion handling

Loops happen in real DeFi composability — vaults of vaults, circular
hypothecation, mutually-referencing structures. The framework handles
them via the four-tier hierarchy.

### Mathematical resolution where possible

Some loops are solvable analytically:

- **Linear claim systems** — A owes B owes C owes A; the equilibrium
  values are a fixed-point solution of a linear system
- **Geometric series** — compounding interest in a closed loop
  converges to a geometric sum
- **Fixed-point existence** — Banach contraction mapping etc.

For such structures, the category equation's tier-1 path handles
them. The doc captures this as a *capability* that some categories
have.

### Iterative simulation under stress

When the structure is well-defined but no closed form, simulate
iteratively:

```metta
(= (iterative-simulate $book $scenario $iters $damping)
   (let-loop ($state (initial-state $book) (i 0))
      (case (>= $i $iters)
        ((True $state)
         (False
            (let* (($next (one-step-update $state $scenario))
                   ($damped (interpolate $state $next $damping)))
              (if (converged? $state $damped)
                  $damped
                  (iter $damped (+ $i 1)))))))))
```

Damping prevents oscillation. Iteration cap prevents runaway. If
convergence isn't achieved, fall through to tier 3.

### Heuristic fallback

When neither analytic resolution nor convergent simulation works:

**Cycle detection.** Track visited Exobooks during recursion. On
encountering a previously-visited book, apply `loop-penalty-multiplier`
and return.

**Depth penalty.** Each level of recursion adds `depth-penalty-per-level`
additively to the multiplier. Discourages deep nesting.

**Repeated-terminal detection.** If the same exo asset is reached via
multiple paths, that's the same recourse asset claimed by multiple
positions — re-hypothecation. Apply `repeated-terminal-penalty`.

**Bounded recursion.** Beyond `max-recursion-depth`, return max-risk.

```metta
(= (exobook-rw-with-loop-handling $book $treatment $depth $visited)
   (cond
     ((> $depth (max-recursion-depth))
        (notional-of-issued-units $book))                      ; CRR 100%
     ((in-set $book $visited)
        (* (loop-penalty-multiplier) (best-effort-rw $book $treatment)))
     (True
        (let* (($visited' (add-to-set $book $visited))
               ($cat (exobook-category $book))
               ($child-rws (recurse-children $book $cat $treatment (+ $depth 1) $visited'))
               ($raw-rw (eval-category-equation $cat $book $child-rws))
               ($depth-mult (+ 1.0 (* $depth (depth-penalty-per-level))))
               ($repeat-mult (case (repeated-terminals-across-paths $book)
                                ((True (repeated-terminal-penalty))
                                 (False 1.0)))))
          (min 1.0 (* $raw-rw $depth-mult $repeat-mult))))))
```

### The "real claim to real stuff" principle

The deeper goal of all this machinery is answering one question:

> In the worst plausible scenario, what real claim do I have to real
> assets that will still exist and be accessible?

Loops obscure this. A position whose backing is a loop (X owes Y owes
X) ultimately has no real-world claim — the loop nets to zero in the
worst case. The heuristic penalty discourages such structures
economically. The simulation tier tries to model what happens when
someone in the loop fails. The math tier solves the linear algebra
when it's clean.

What survives all the math, simulation, and heuristics: **hard
recourse to terminal exo assets that exist independently of any
particular protocol or counterparty.** The framework's job is to
trace claims down to that bedrock and quantify how much of it the
holder actually has after stress.

---

## 9. What state-based CRR was and why it's gone

### The original model

Earlier iterations of `&core-framework-risk` had a state-based CRR
table:

```metta
(crr filling      5)
(crr deploying  100)
(crr at-rest     40)
(crr unwinding   60)
(crr offboarding 80)
(crr closed       0)

;; book had a state
(book-state book-A1 at-rest)

;; risk weight was: notional × CRR-for-current-state
(unit-risk-weight $u) = (* (notional-of $u) (crr-for-state (book-state-of $u)))
```

The idea was that a book's lifecycle phase was a proxy for content
uncertainty — `filling` is mostly empty, `deploying` is committing,
`at-rest` is stable.

### Why it existed

State-based CRR was a **proxy for content uncertainty**. Without
machinery to monitor exo books recursively, recognize complex
strategies, run stress simulations — state was a simple stand-in.
Crude but workable.

### What replaces it

**Different unit, different exo book.** A claim against an ABF deal
that's still being negotiated and funded is a *different exo book*
than the same deal once it's closed and seasoned. They go in different
categories with different equations; they're held as different exo
units.

When a deal moves through its lifecycle, the Halo's Riskbook
substitutes one exo unit for another:

```metta
;; before: Riskbook holds the "in-deployment" version
(holds spark-credit-rb-A (exo-unit deal-D-deploying 1.0M))
(exo-book deal-D-deploying (category abf-deploying))           ; high-risk category

;; after closing: Riskbook swaps for the "at-rest" version
(holds spark-credit-rb-A (exo-unit deal-D-at-rest 1.0M))
(exo-book deal-D-at-rest (category abf-at-rest))               ; lower-risk category
```

Lifecycle phases still happen — deals still move from negotiation to
seasoned — but they manifest as **different exo units in different
exo books**, not as a state attribute on a single unit.

### Implications for existing material

- `&core-framework-risk` no longer holds `(crr <state> <value>)` atoms.
  Replaced by the full category catalog in
  `&core-framework-risk-categories`.
- `(book-state $b $s)` atoms may persist as **operational/governance
  metadata** for tracking which phase a deal is in, but they don't
  drive risk computation. Risk is purely a function of which units
  the book holds.
- The four-constructor MeTTa surface in `synlang-patterns.md` §3 with
  its `BookState` enum may evolve — `BookState` is now an operational
  label, not a risk input.
- `settlement-cycle-example.md` uses the old model and needs an update
  pass. The shape of the calculation (ER, breach, penalty) survives;
  the inputs (CRR table, state transitions) get replaced.

---

## 10. The govops / endoscraper division of state responsibility

Risk simulations are only as good as the input data. Two parties
maintain that data, with verification between them.

### Halo govops keeps state real-time

The Halo's accordant govops team is responsible for pushing exo book
state and Riskbook composition updates through the gate continuously.
Whenever a new position is taken, an old one closed, a parameter
changes — the govops pushes a signed update to synserv via syngate.

For exo books the Halo invests in, the govops is responsible for:

- Atomically pushing state changes (`(exo-book-asset ...)`,
  `(exo-book-liability ...)`, etc.)
- Pushing parameter updates (collateralization ratios, counterparty
  identifiers, etc.)
- Handling lifecycle transitions (which exo unit replaces which)

This is the Halo's accountability. Stale or wrong state means stale
or wrong risk weights, which means the Halo earns inaccurate carry
and is subject to settlement penalties when the accuracy gets
verified.

### Endoscrapers verify

Synserv-run **endoscrapers** independently read the underlying chain
state and reconcile against what the Halo govops claimed. The pattern
is the verification cycle from `topology.md` §6:

```
1. Halo govops pushes state update through telgate / syngate
2. Synart-side state atoms updated
3. Endoscraper independently scrapes the same chain state
4. Reconciler compares (Halo's claim vs scraped reality)
5. Match → continue
6. Disagreement → flag into &core-escalation
```

Disagreement triggers governance review. Repeated discrepancies have
slashing implications for the responsible Halo's beacon network.

### Off-chain exo books

For exo books that aren't fully on-chain (custody, real-world claims,
ISDA-shaped derivatives), the verification model needs a different
mechanism — exoscrapers, attestation, oracles. These are out of scope
for now (`topology.md` §6 notes exoscraper as deferred). For Phase 1+
on-chain-heavy operation, endoscrapers cover the majority of cases.

### Why this division

- **Halo has the live information.** They're the ones placing the
  positions; they know first what changed.
- **Synserv has the impartial verifier.** Endoscrapers are
  governance-blessed; they don't have a stake in any Halo's positions.
- **Symmetric obligation.** If Halo lies, endoscraper catches it. If
  endoscraper is wrong (chain reorg, etc.), Halo can dispute via
  governance.

This is the same baseline-and-warden pattern from sentinel formations:
claim + independent verification + escalation on disagreement.

---

## 11. The CRR-100% default mechanism

The framework treats "default-deny" as a first-class principle. Three
places it manifests:

### Riskbook without matching category → CRR 100%

Already covered in §4. The single most important application of the
default-deny pattern. A Halo can compose any Riskbook they want; only
ones matching a registered category get favorable risk treatment.

### Exobook beyond MAX_RECURSION_DEPTH → CRR 100%

Covered in §8. If recursion goes too deep, the framework can't
adequately model what's at the bottom; treat as max risk. This forces
exo book structures to be reasonably shallow.

### Exobook without matching category → CRR 100%

Same logic as Riskbook. Every exo book must have a category. Adding
a new exo book to `&core-registry-exo-book` is a small governance act
that includes assigning it a category.

### Why this is structurally important

- **Forces governance to keep up.** New asset classes / structures
  / strategies require new categories. If governance lags, Halos pay
  in CRR.
- **Limits opacity.** Halos can't sneak unmodeled structures into
  the system at favorable rates. Anything novel either has a category
  (and was vetted) or pays max risk.
- **Aligns incentives.** Halos that propose new categories with
  governance get rewarded with both faster turnaround on their own
  needs and ecosystem standing for contributing to the catalog.

This is the same pattern as elsewhere in the synome: regulated
activity flows where governance has built infrastructure for it;
un-regulated activity is treated as worst-case.

---

## 12. Worked examples

Five examples covering the model's expressive range.

### Example A — Pure ETH Riskbook (terminal, math tier)

Simplest case. A Halo holds raw ETH in a Riskbook of category
`pure-eth-holding`.

**Setup:**

```metta
;; in &core-framework-risk-categories
(risk-category-def eth (level exo-asset) (m2m 0.25) (htm 0.20))

(risk-category-def pure-eth-holding
   (level riskbook)
   (composition-constraints (only-asset-class eth))
   (equation-m2m (* (sum-of-notionals) (lookup-rw eth m2m)))
   (equation-htm (* (sum-of-notionals) (lookup-rw eth htm)))
   (resolution-tier math))

;; in &entity-halo-spark-eth-riskbook-A
(book-type riskbook)
(book-category pure-eth-holding)
(holds eth-asset 1000)                                       ; 1000 ETH held
(issues (endo-unit u-rb-A-bond) (notional 1000))             ; 1000 ETH equiv
```

**Computation:**

```
riskbook-finality-rw(spark-eth-rb-A, m2m):
   matched-category = pure-eth-holding
   resolution-tier = math
   apply equation: 1000 × 0.25 = 250 ETH-equiv risk weight
   ⇒ M2M CRR = 250/1000 = 0.25 = 25%

riskbook-finality-rw(spark-eth-rb-A, htm):
   apply equation: 1000 × 0.20 = 200
   ⇒ HTM CRR = 0.20 = 20%
```

Both numbers propagate up to the Halobook unchanged (Halobook
aggregates without transformation).

### Example B — Morpho lending Riskbook (Exobook recursion, simulation tier)

A Halo holds a Morpho-vault exo unit. The Riskbook category invokes
recursion through Morpho's structure.

**Setup:**

```metta
;; categories
(risk-category-def eth (level exo-asset) (m2m 0.25))
(risk-category-def morpho-borrow-position
   (level exobook)
   (variables [(coll-value $cv) (debt $d) (liq-thresh $lt)])
   (equation-m2m (simulate-borrow-position-loss $cv $d $lt))
   (resolution-tier simulation))
(risk-category-def morpho-market
   (level exobook)
   (equation-m2m (sum-children-weighted) (then-floor 0.30))
   (resolution-tier simulation))
(risk-category-def morpho-vault
   (level exobook)
   (equation-m2m (allocation-weighted-sum) (then-floor 0.35))
   (resolution-tier simulation))
(risk-category-def morpho-lending
   (level riskbook)
   (composition-constraints (units-pointing-to-morpho-vault-or-market))
   (equation-m2m (sum-over-units (lambda ($u) (* (notional $u) (exobook-rw (issuer $u) m2m)))))
   (resolution-tier simulation))

;; exo book registry
(exo-book morpho-eth-vault       (category morpho-vault))
(exo-book morpho-market-X        (category morpho-market))
(exo-book borrower-pos-1         (category morpho-borrow-position))
(exo-book eth                    (category eth))

(exo-book-holds morpho-eth-vault morpho-market-X 1.0)         ; 100% in market X
(exo-book-holds morpho-market-X borrower-pos-1 1.0)
(exo-book-asset borrower-pos-1 eth 150)
(exo-book-liability borrower-pos-1 owed-to-morpho-X 100)

;; Halo's Riskbook
(book-type riskbook)
(book-category morpho-lending)
(holds (exo-unit u-001) morpho-eth-vault 1000000)
```

**Computation (simulation under severe-correlated-crash):**

```
exobook-rw(borrower-pos-1, m2m, scenario=severe-correlated-crash):
   coll-value (current) = 150 ETH × 4000 USD/ETH = 600,000 USD
   coll-value (post-stress) = 600,000 × (1 - 0.55) = 270,000 USD
   debt = 100 ETH × 4000 = 400,000 USD
   debt-after-stress (debt is in USD-equiv) = 400,000 × interest-accrual ≈ 400,000
   recovery = min(coll-value-post, debt) = 270,000
   loss-fraction = 1 - 270,000/400,000 = 0.325
   ⇒ borrower-pos-1 RW (M2M, severe-correlated-crash) = 0.325

;; (other scenarios computed similarly; take max for conservative)
;; assume severe-correlated-crash is the worst, so borrower-pos-1 M2M RW = 0.325

exobook-rw(morpho-market-X, m2m):
   weighted-sum-of-children = 1.0 × 0.325 = 0.325
   floor = 0.30
   ⇒ morpho-market-X M2M RW = max(0.30, 0.325) = 0.325

exobook-rw(morpho-eth-vault, m2m):
   allocation-weighted-sum = 1.0 × 0.325 = 0.325
   floor = 0.35                                              ; vault adds protocol risk
   ⇒ morpho-eth-vault M2M RW = max(0.35, 0.325) = 0.35

riskbook-finality-rw(spark-defi-rb-B, m2m):
   sum-over-units: 1,000,000 × 0.35 = 350,000
   ⇒ M2M CRR = 350,000/1,000,000 = 0.35 = 35%
```

The vault's protocol risk floor (0.35) ends up dominating in this
scenario. HTM would compute differently — typically lower, since HTM
treatment cares about ultimate solvency rather than mark-to-market
volatility.

### Example C — ABF + CDS Riskbook (Riskbook category with offsetting positions)

The most interesting case: a Riskbook combining a credit asset with
its protective CDS.

**Setup:**

```metta
(risk-category-def abf-with-cds-cover
   (level riskbook)
   (composition-constraints
      (and (count-of (asset-class abf-claim)) = 1)
           (count-of (asset-class cds-cover)) = 1)
           (cds-references-credit-asset-in-same-book ...)
           (>= (cds-notional / abf-notional) 0.90)))
   (equation-m2m
      (simulate-across-scenarios m2m-scenarios
         (lambda ($scenario)
            (let* (($abf-default-prob (apply-credit-stress $scenario abf-deal))
                   ($abf-loss-on-default (- 1.0 (abf-recovery-rate $scenario)))
                   ($cds-counterparty-survival (cds-counterparty-survival-prob $scenario))
                   ($cds-effective-payout
                      (* (cds-notional)
                         $cds-counterparty-survival
                         (cds-payout-ratio $scenario)))
                   ($expected-loss
                      (* $abf-default-prob
                         (max 0 (- (abf-notional) $cds-effective-payout)))))
              (/ $expected-loss (abf-notional))))
         (combiner take-worst)))
   (resolution-tier simulation))

;; Halo's Riskbook
(book-type riskbook)
(book-category abf-with-cds-cover)
(holds (exo-unit u-001) abf-deal-D 1000000)
(holds (exo-unit u-002) cds-on-abf-deal-D 950000)            ; 95% coverage
```

**Computation under severe-correlated-crash:**

```
abf-default-prob (under crash) = 0.20                        ; high in stress
abf-recovery-rate (under crash) = 0.40                       ; some recovery from collateral
abf-loss-on-default = 0.60

cds-counterparty (e.g., a major dealer):
   cds-counterparty-survival-prob (under crash) = 0.75       ; counterparty is themselves stressed
   cds-payout-ratio (if they survive) = 1.0                   ; full coverage if they pay

cds-effective-payout = 950,000 × 0.75 × 1.0 = 712,500

if ABF defaults (probability 0.20):
   gross loss = 1,000,000 × 0.60 = 600,000
   net loss (after CDS) = max(0, 600,000 - 712,500) = 0      ; CDS covers fully
   
if ABF doesn't default (probability 0.80):
   no loss

expected-loss = 0.20 × 0 + 0.80 × 0 = 0
                                ↑
              CDS provides full coverage in this scenario

;; under credit-crisis scenario where counterparty fails harder:
   cds-counterparty-survival-prob = 0.40
   cds-effective-payout = 950,000 × 0.40 × 1.0 = 380,000
   if ABF defaults:
      gross loss = 600,000
      net loss = max(0, 600,000 - 380,000) = 220,000
   expected-loss = 0.20 × 220,000 = 44,000
   loss-fraction = 0.044

;; take worst case across scenarios
final M2M CRR = 0.044 (or higher if worse scenario found)
```

The CDS effectively transforms a high-risk credit position (would be
~12% RW unhedged) into a much lower risk position (~4-5% RW). The
remaining risk is **counterparty residual** — the risk that the CDS
issuer fails to pay.

This is what hedge-categorization buys: substantial RW reduction in
exchange for accepting a different (much smaller) risk in the form of
counterparty residual.

### Example D — Multi-Riskbook Halo composition (your example)

A Halo wants exposure to ABF (with CDS protection) AND Morpho lending.
Each gets its own Riskbook with appropriate category. Halobook
aggregates.

**Setup:**

```metta
;; Two Riskbooks under one Halo
(book-type riskbook (book-category abf-with-cds-cover) ...)        ; spark-credit-rb-A
   ;; contents from Example C
(book-type riskbook (book-category morpho-lending) ...)            ; spark-credit-rb-B
   ;; contents from Example B

;; Halobook aggregating both
(book-type halobook)
(sub-riskbook spark-credit-rb-A)
(sub-riskbook spark-credit-rb-B)
(holds (endo-unit u-rb-a-bond) 1000000)                            ; finality unit from rb-A
(holds (endo-unit u-rb-b-bond) 2000000)                            ; finality unit from rb-B
(issues (endo-unit u-hb-bond) (notional 3000000))
```

**Computation:**

```
Halobook RW (M2M)  = (1,000,000 × 0.044) + (2,000,000 × 0.35)
                  = 44,000 + 700,000
                  = 744,000
   ⇒ M2M CRR = 744,000 / 3,000,000 = 0.248 ≈ 25%

(Halobook is just aggregation; no further computation. Pari passu
across the two Riskbook units' bond claims.)
```

Note: cross-Riskbook correlation isn't credited. If both Riskbooks
suffer in the same crash (likely — both have credit-cycle exposure),
the Halobook RW reflects worst-case aggregate of independent
calculations. The Halo doesn't get a netting benefit across Riskbooks
because bankruptcy-remoteness forbids it.

### Example E — Looped exposure (heuristic tier fallback)

A Halo holds an exo unit pointing to Vault-Alpha, which holds positions
in Vault-Beta, which holds positions back in Vault-Alpha (a loop).

**Setup:**

```metta
(exo-book vault-alpha (category opaque-vault))
(exo-book vault-beta  (category opaque-vault))
(exo-book-holds vault-alpha vault-beta 1.0)                  ; alpha 100% allocated to beta
(exo-book-holds vault-beta vault-alpha 1.0)                  ; beta 100% allocated to alpha
(exo-book-asset ... eth 100)                                  ; some real ETH somewhere

;; Halo's Riskbook holds vault-alpha
(book-category vault-of-vaults)
(holds (exo-unit u-001) vault-alpha 1000000)
```

**Computation walks down with cycle detection:**

```
exobook-rw-with-loop-handling(vault-alpha, m2m, depth=0, visited=∅):
   not over depth, not in visited
   recurse into children with visited = {vault-alpha}
   
   exobook-rw-with-loop-handling(vault-beta, m2m, depth=1, visited={vault-alpha}):
      not over depth, not in visited
      recurse into children with visited = {vault-alpha, vault-beta}
      
      exobook-rw-with-loop-handling(vault-alpha, m2m, depth=2, visited={vault-alpha, vault-beta}):
         vault-alpha IS in visited!
         → cycle detected
         → return (loop-penalty-multiplier × best-effort-rw(vault-alpha))
                = 1.5 × 0.5 (best guess)
                = 0.75

      vault-beta's RW = (1.0 weight × 0.75) = 0.75
      depth-multiplier = 1.0 + (1 × 0.05) = 1.05
      vault-beta's adjusted RW = 0.75 × 1.05 = 0.7875

   vault-alpha's RW = (1.0 weight × 0.7875) = 0.7875
   depth-multiplier = 1.0 + (0 × 0.05) = 1.0
   vault-alpha's adjusted RW = 0.7875 × 1.0 = 0.7875
   capped at 1.0 → 0.7875

⇒ Riskbook M2M CRR ≈ 79%
```

The looped structure ends up with very high CRR (~79%) due to the
cycle penalty. Compare to a clean linear structure where the same
underlying ETH might give a CRR of ~30%. The loop costs the Halo
nearly 50 percentage points of capital efficiency.

This is the intended outcome: **looped structures are still possible
but economically discouraged.** A Halo that wants to use them pays
real capital cost; a Halo that doesn't can avoid them.

---

## 13. Open design questions

**1. Cross-Riskbook correlation friction.**
Bankruptcy-remoteness across Riskbooks means correlated returns aren't
credited at the Halobook level (Example D shows this). Is this the
right tradeoff? Probably yes — the legal/economic structure mirrors
the risk-calculation structure — but Halos pay real cost for the
benefit. Worth being explicit in governance discussions.

**2. Provisional category mechanism.**
Halos with novel strategies face a wait while a new category goes
through governance crystallization. Should there be a provisional
mechanism — higher CRR than mature categories but lower than the
default-deny 100% — for strategies under sandbox testing? Tradeoff:
faster innovation vs more risk surface for governance to manage.

**3. Stress scenario library curation.**
Who proposes new stress scenarios? How are they parameterized? Some
scenarios are obvious (2008-style crash), others are speculative
(novel coordinated attack vectors). The library is a major governance
artifact — needs its own design pass on proposal flow, sandbox
testing, and crystallization criteria.

**4. Real-time recomputation cadence.**
Push-evaluation on every input change is expensive at scale.
Pull-evaluation may produce stale risk weights when consumers haven't
asked. Hybrid is right but needs configuration. Per-category default
plus per-context overrides? See `scaling.md` for cost implications.

**5. Cross-chain exo books.**
Examples assume Ethereum. Real exo books span chains: a Spark deal
might span an Ethereum custody vault, a Solana DeFi position, and a
real-world receivable. The recursion needs to handle heterogeneous
chain composition, including bridging risk.

**6. Halobook category constraints.**
Should Halobooks themselves have categories that constrain what mix
of Riskbook units they can hold? E.g., "diversified-credit-halobook"
requires at least 3 Riskbook categories, no single category > 50%.
Concentration limits at the Halobook level? This is a sketch direction
for the deferred Level-3 (concentration) design.

**7. Primebook category constraints.**
Same question, one level higher. Primebook categories that constrain
Halobook mix. This is naturally where concentration tracking sits
because it's a system-wide decision (the Prime sees across its
Halos).

**8. Concentration L3 — full design.**
Deferred. Once tackled: concentration categories, global limits,
competition between Primes, scatter-gather aggregation across
Primebooks. Intersects with mechanism design (how to handle
displacement) and information design (Primes need to know global
state).

**9. Lifecycle metadata persistence.**
If `(book-state $b $s)` atoms persist as operational metadata (per
§9), who writes them, who reads them? Settlement coordination? Audit?
Or do they fully disappear with deal phase encoded entirely in unit
identity? Minimal answer: drop them; richer answer: keep for human-
readability.

**10. Counterparty risk modeling depth.**
CDS counterparty risk in Example C is computed via a per-counterparty
survival probability. How is that probability sourced? From the CDS
counterparty's own categorization (custody-major, etc.)? From a
separate counterparty-rating framework? Worth designing explicitly.

---

## 14. One-line summary

**Books come in four kinds (Primebook / Halobook / Riskbook /
Exobook), each with a specific job; Riskbook is the unit of regulation
(must match a registered category or get CRR 100%); categories are
parameterized stress simulations evaluating Riskbook composition or
Exobook state under a library of governance-curated crash scenarios;
the four-tier resolution hierarchy (math → simulation → heuristics →
max-risk) gracefully degrades on opaque structures; both M2M and HTM
risk weights propagate continuously up the stack with the Primebook
selecting per-position; state-based CRR is gone, replaced by content-
derived risk that asks the right question — "what real claim do I
have to real assets in the worst plausible correlated crash?"**

---

## File map

| Doc | What it covers, relative to this one |
|---|---|
| `topology.md` §6 | Where `&core-framework-risk-categories`, `&core-framework-stress-scenarios`, `&core-registry-exo-book` live structurally; the four-book taxonomy reflected in `entity <sub-kind>` keywords |
| `syn-tel-emb.md` §1 | Framework layer of synart — categories and scenarios as commons content |
| `syn-tel-emb.md` §8 | Recipe marketplace — proposing new categories and scenarios is recipe-shaped governance work |
| `synlang-patterns.md` §1-§3 | The conservation-network framing (books-as-nodes, units-as-edges) that this framework operates on |
| `synlang-patterns.md` §4 | Sentinel decision rule with risk-adjusted return — uses the unit-risk-weight outputs from this framework |
| `settlement-cycle-example.md` | Worked settlement; uses the old state-based CRR; pending update to new model |
| `synart-access-and-runtime.md` §9-§14 | Auth, gates, telgate / syngate — how Halo govops pushes state through, how endoscrapers verify |
| `boot-model.md` | How endoscraper loops boot to populate exo book registry |
| `scaling.md` | Hot-spotting on `&core-registry-exo-book`; endoscraper bandwidth; simulation computation cost |
