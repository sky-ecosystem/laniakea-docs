# Synlang Patterns — Code Library

Working synlang code for the Synome's deontic skeleton. Code-heavy
reference; cross-cuts conceptual material in `topology.md` and
`runtime.md`.

What's in this doc:

| § | Pattern | Why |
|---|---|---|
| 1 | The Platonic kernel | The conservation-network framing |
| 2 | Cross-book duality | One atom, two views |
| 3 | Four-constructor MeTTa surface | Typed `create-halo / create-class / create-book / issue-unit` |
| 4 | Sentinel decision rule (RAR) | Risk-adjusted return as strategy in synlang |
| 5 | The call-out primitive | The synart→telart bridge — how loops consult local cognition |
| 6 | Relay and sentinel patterns | Two action classes by cognitive density; the formerly-formation roles collapse into relay (baseline / warden) + sentinel (stream / principal) |
| 7 | Tranche-rule patterns | Rule-bearing tranches (callable, conversion, step-up, triggered subordination) |
| 8 | Projection-model declaration patterns | How risk forms declare projection models for complex positions |

Working examples elsewhere:

- `settlement-cycle-example.md` — full ER → penalty cycle (covers CRR / encumbrance / settlement)
- `telseed-bootstrap-example.md` — first-24-hours trace of a new teleonome
- `../inactive/archive/govops-synlang-patterns.md` — runnable demo's pattern catalog (gate, pipeline, attestation, beacon identity); archived as historical demo
- `topology.md` §16 — the two-step rule shape with `&self` portability
- `topology.md` §17 — the two-step loop shape (universal template + per-entity instance)
- `boot-model.md` — identity-driven boot mechanics for any loop
- `../synoteleonomics/recipe-marketplace.md` — the recipe marketplace context for sentinel formations (canonical home; formerly `syn-tel-emb.md` §8)

---

## 1. The Platonic kernel

> **A book is a node. A unit is a directed weighted edge. Balance means every internal node conserves flow.**

Kirchhoff's current law applied to claims. The architecture is a
**conservation network**. Capital is the conserved quantity, units are
wires, books are junctions. USDS holders and real-world borrowers are
the unconserved boundaries.

| Framing | Books are… | Units are… | Balance is… |
|---|---|---|---|
| **Flow network** | junctions | wires | Kirchhoff: in = out |
| **Double-entry bookkeeping** | accounts | transactions | every Tx posts to two ledgers |
| **Category theory** | objects | morphisms | composition preserves identity |
| **Promise graph** | bundles of promises | promises | promises made = promises held |
| **Type theory** | types | values bridging types | type preservation under composition |
| **Physics** | reservoirs | pipes | mass conservation |

Same shape, different vocabulary.

### The minimum constructor

```
Start: empty universe.
Step:  mint(issuer, holder, amount, policy)
Inv:   for every internal node, Σ(incoming amounts) = Σ(outgoing amounts).
End:   the architecture is whatever set of mints satisfies the invariant.
```

Any compliant Laniakea state is reachable from `{}` by some sequence
of valid mints. Any state with a balance violation is unreachable.

The engineering version (the four constructors below) is this Platonic
kernel + a curated lens exposing only the moves the architecture
admits. Anything buildable with `create-halo` / `create-class` /
`create-book` / `issue-unit` is correct by construction; anything not
buildable with them is something the system shouldn't allow.

---

## 2. Cross-book duality — one atom, two views

```synlang
;; A unit appears as a liability in the issuing book ($issuer)
;; and as an asset in the holding book ($holder).
(unit nfat-42 (issuer book-7) (holder spark-prime-book) 30000000)

;; Bridging rules — project the unit into both sides.
(= (liability $issuer $unit $amt)
   (match &self
     (unit $unit (issuer $issuer) (holder $_) $amt)
     True))

(= (asset $holder $unit $amt)
   (match &self
     (unit $unit (issuer $_) (holder $holder) $amt)
     True))
```

**One atom populates two views.** The recursive Generator → Prime →
Halo stack falls out automatically: each layer's units are
simultaneously liabilities below and assets above.

This is also why the canonical `&entity.halo.<id>.book.<bookid>` leaf Space
is the right home for a unit atom: the same atom is read as "what this
book owes" by the issuing-side bridging rule and "what some other book
holds" by the holding-side rule — different reads at different points
in the entart tree, one fact in storage.

---

## 3. Four-constructor MeTTa surface

The narrowed API: exactly enough degrees of freedom that any buildable
state is a legal state. By construction, no buildable state can be
invalid.

```metta
;; ════════════════════════════════════════════════════════════════
;;  Type universe
;; ════════════════════════════════════════════════════════════════

(: Halo  Type)
(: Class Type)
(: Book  Type)
(: Unit  Type)

(: BookState Type)
(: created     BookState)
(: filling     BookState)
(: offboarding BookState)
(: deploying   BookState)
(: at-rest     BookState)
(: unwinding   BookState)
(: closed      BookState)

(: ClassType Type)
(: portfolio ClassType)
(: term      ClassType)
(: trading   ClassType)

(: AssetKind Type)
(: usds AssetKind)
(: usdc AssetKind)
(: usd  AssetKind)
(: loan AssetKind)

(: Result Type)
(: Created (-> Symbol Symbol Result))
(: Issued  (-> Unit Result))
(: Error   (-> Symbol Atom Result))

;; ════════════════════════════════════════════════════════════════
;;  Bridging rules — units project automatically into both books
;; ════════════════════════════════════════════════════════════════

(: liabilities-of (-> Book Expression))
(= (liabilities-of $book)
   (match &self (unit $u (issuer $book) (holder $_) $a) ($u $a)))

(: assets-held-by (-> Symbol Expression))
(= (assets-held-by $holder)
   (match &self (unit $u (issuer $_) (holder $holder) $a) ($u $a)))

;; ════════════════════════════════════════════════════════════════
;;  1. create-halo
;; ════════════════════════════════════════════════════════════════

(: create-halo (-> Symbol Symbol Result))
(= (create-halo $halo $operator)
   (let* (($_ (add-atom &self (: $halo Halo)))
          ($_ (add-atom &self (halo-operator $halo $operator))))
     (Created halo $halo)))

;; ════════════════════════════════════════════════════════════════
;;  2. create-class      type checker enforces $halo : Halo
;; ════════════════════════════════════════════════════════════════

(: create-class (-> Symbol Halo ClassType Number Number Result))
(= (create-class $class $halo $type $min $max)
   (let* (($_ (add-atom &self (: $class Class)))
          ($_ (add-atom &self (class-halo   $class $halo)))
          ($_ (add-atom &self (class-type   $class $type)))
          ($_ (add-atom &self (class-buybox $class $min $max))))
     (Created class $class)))

;; ════════════════════════════════════════════════════════════════
;;  3. create-book       type checker enforces $class : Class
;; ════════════════════════════════════════════════════════════════

(: create-book (-> Symbol Class Result))
(= (create-book $book $class)
   (let* (($_ (add-atom &self (: $book Book)))
          ($_ (add-atom &self (book-class $book $class)))
          ($_ (add-atom &self (book-state $book created))))
     (Created book $book)))

;; ════════════════════════════════════════════════════════════════
;;  4. issue-unit        type-level: $book : Book, $kind : AssetKind
;;                       runtime:    state ∈ {created, filling}
;;                                   amount within buybox
;; ════════════════════════════════════════════════════════════════

(: issue-allowed? (-> Book Number Bool))
(= (issue-allowed? $book $amount)
   (case (match &self
           (, (book-state $book $s)
              (book-class $book $class)
              (class-buybox $class $min $max))
           (and (or (== $s created) (== $s filling))
                (and (>= $amount $min) (<= $amount $max))))
     ((True  True)
      (False False)
      (Empty False))))

(: ensure-filling (-> Book Atom))
(= (ensure-filling $book)
   (case (match &self (book-state $book created) yes)
     ((yes
        (let* (($_ (remove-atom &self (book-state $book created)))
               ($_ (add-atom    &self (book-state $book filling))))
          ok))
      (Empty ok))))

(: issue-unit (-> Symbol Book Symbol Number AssetKind Result))
(= (issue-unit $unit $book $holder $amount $kind)
   (if (issue-allowed? $book $amount)
       (let* (($_ (add-atom &self (: $unit Unit)))
              ($_ (add-atom &self
                    (unit $unit (issuer $book) (holder $holder) $amount)))
              ($_ (add-atom &self (asset $book $kind $amount)))
              ($_ (ensure-filling $book)))
         (Issued $unit))
       (Error issuance-denied $book)))
```

### Where the type system earns its keep

| Property | How it's enforced |
|---|---|
| Halo must exist before a Class can reference it | **Type:** `create-class` requires a `Halo` |
| Class must exist before a Book can reference it | **Type:** `create-book` requires a `Class` |
| Book must exist before a Unit can be issued from it | **Type:** `issue-unit` requires a `Book` |
| Class type is one of {portfolio, term, trading} | **Type:** `ClassType` enum |
| Book state is one of the seven valid states | **Type:** `BookState` enum |
| Asset kind is approved | **Type:** `AssetKind` enum |
| Amount falls within buybox | **Runtime guard** |
| Book state allows issuance | **Runtime guard** |

### Type errors caught BEFORE evaluation

```metta
! (create-class evil grunt term 1 1000)
;; ⇒ BadType                          ;; grunt is not a Halo

! (create-book book-7 spark-halo)
;; ⇒ BadType                          ;; spark-halo is a Halo, not a Class

! (issue-unit nfat-1 facility-A spark 30000000 usds)
;; ⇒ BadType                          ;; facility-A is a Class, not a Book

! (issue-unit nfat-1 book-7 spark 30000000 yen)
;; ⇒ BadType                          ;; yen is not an AssetKind
```

### Where these run in the entart tree

The `&self` in the constructors above is whichever entart Space the
constructor runs against. In production layout (per `topology.md` §11):

- `create-halo` — writes identity atoms into a new `&entity.halo.<id>.root`, plus a `(sub-entart …)` registry atom into the parent Prime's root.
- `create-class` — writes class atoms into the halo's root Space.
- `create-book` — writes book identity into a new book leaf Space, plus a `(sub-space …)` registry atom into the halo's root.
- `issue-unit` — writes unit atoms into the book's leaf Space.

See `topology.md` §12 for the registry pattern that connects these.

---

## 4. Sentinel decision rule with risk-adjusted return

The Base Strategy is **rules in the synome**, not opaque code in a
process. The same rules are read by `baseline-{prime}` relay (decide),
`warden-{prime}-{op}` relay (verify), `stream-{prime}-{actor}` sentinel
(propose intent within bounds), and used for
counterfactual carry simulation.

```synlang
(prime-capital spark 500000000)
(unit nfat-A (issuer book-7)  (holder spark)  30000000)
(unit nfat-B (issuer book-9)  (holder spark) 100000000)
(unit nfat-C (issuer book-11) (holder spark)  50000000)

(book-state book-7  filling)
(book-state book-9  at-rest)
(book-state book-11 deploying)

(book-yield book-7  0.10)
(book-yield book-9  0.08)
(book-yield book-11 0.14)

(encumbrance-limit spark 0.90)
(risk-aversion     spark 0.15)   ; λ — Spark's published risk preference

;; Risk-adjusted return — Spark's theory of how to weigh trade-offs.
;;     RAR = yield_rate − λ × encumbrance_ratio
(= (risk-adjusted-return $prime)
   (match &self (risk-aversion $prime $lambda)
     (- (yield-rate $prime)
        (* $lambda (encumbrance-ratio $prime)))))

;; The decision rule: hypothetical RAR for a reallocation.
(= (hypothetical-rar $prime $from $to $delta)
   (let* (($cap     (capital-of $prime))
          ($lambda  (match &self (risk-aversion $prime $l) $l))
          ($f-from  (match &core.framework.risk
                      (and (book-state $from $s) (crr $s $f)) $f))
          ($f-to    (match &core.framework.risk
                      (and (book-state $to   $s) (crr $s $f)) $f))
          ($y-from  (match &self (book-yield $from $y) $y))
          ($y-to    (match &self (book-yield $to   $y) $y))
          ($new-enc   (+ (encumbered $prime)
                         (* $delta (- $f-to $f-from))))
          ($new-yield (+ (expected-yield $prime)
                         (* $delta (- $y-to $y-from)))))
     (- (/ $new-yield $cap)
        (* $lambda (/ $new-enc $cap)))))

(= (rar-improvement $prime $from $to $delta)
   (- (hypothetical-rar $prime $from $to $delta)
      (risk-adjusted-return $prime)))

(= (within-limit $prime $from $to $delta)
   (let (($cap (capital-of $prime))
         ($f-from (match &core.framework.risk
                    (and (book-state $from $s) (crr $s $f)) $f))
         ($f-to   (match &core.framework.risk
                    (and (book-state $to   $s) (crr $s $f)) $f))
         ($limit  (match &self (encumbrance-limit $prime $l) $l)))
     (<= (/ (+ (encumbered $prime) (* $delta (- $f-to $f-from))) $cap)
         $limit)))

(= (propose-reallocation $prime $from $to $delta)
   (and (> (rar-improvement $prime $from $to $delta) 0)
        (within-limit $prime $from $to $delta)))
```

### Worked example

Spark moves 50M from `book-11` (deploying, CRR 1.00, yield 14%) →
`book-9` (at-rest, CRR 0.40, yield 8%):

- Δ encumbered = 50M × (0.40 − 1.00) = −30M
- Δ yield = 50M × (0.08 − 0.14) = −3M
- New RAR = 0.030 − 0.15 × 0.123 = **0.01155** (up from 0.0085)
- `propose-reallocation` returns **True**.

The same trade with risk-aversion λ = 0.05 would return False.

### Why this composition matters

"All execution flows through public Baseline code" translates literally
into synlang — the strategy is rules in the Space; wardens read the
same rules and halt when their evaluation disagrees with baseline's
actions; counterfactual simulation = same rules on a forked Space; TTS
bounds the damage window between rogue baseline and warden halt.

This is the pattern that makes sentinel formations possible: a
public-readable strategy that produces the same answer regardless of
who's running it, with role-specific *actions* (decide / verify /
propose) all rooted in the same rule set.

---

## 5. The call-out primitive

The synart→telart bridge. A synlang form that lets synart-resolved
loops consult local cognition at strategy-designated points without
giving up the synart envelope's verifiability.

### The form

```metta
(call-out $service
   (inputs <input-atoms…>)
   (output-shape <expected-shape>))
```

Reads as: "at this point in the strategy I need a value of shape
`<expected-shape>` derived from `<input-atoms…>` by service `$service`;
the running embodiment must provide it via a registered service in its
local telart."

### Mechanism

When a synart-resolved loop hits a `(call-out …)`:

1. Runtime resolves `$service` against the booting identity's telart
   call-out registry (e.g.,
   `&telart-mira-research-tel-001-callout (callout-service llm-rank …)`).
2. Inputs get marshalled across the synart→telart boundary.
3. The local service responds — typically by invoking an external API
   (LLM provider, classifier, scorer) or running a local ML model.
4. The response is shape-validated against `<expected-shape>`. Malformed
   responses raise an error.
5. The validated response becomes the value of the `(call-out …)` form
   in the surrounding synart code.

### Code shape

```metta
;; in &core.loop.relay.baseline (synart, universal)
(= (decide-allocation $market-state $entity)
   (let* (($candidates    (enumerate-rebalances $market-state))
          ($scored        (score-with-strategy $candidates))
          ;; ── designated call-out: synart asks local cognition ──
          ($selected      (call-out llm-rank
                            (inputs $scored $market-state)
                            (output-shape (allocation-id))))
          ($within-rar?   (check-rar-improvement $selected))
          ($within-limit? (check-encumbrance-limit $selected)))
     (case (and $within-rar? $within-limit?)
       ((True  $selected)
        (False (fall-back-baseline-allocation))))))

;; in &telart-<tel-id>-callout (per-tel local cognition)
(callout-service llm-rank
   (provider anthropic)
   (model claude-haiku-4.5)
   (max-tokens 2000)
   (api-key-ref endowment-api-keys/anthropic))
```

The synart code doesn't know or care which LLM the tel uses — it just
asks for a ranking. Different tels use different LLMs at the same
`llm-rank` call-out point.

### What's audit-able and what's not

| Property | Verifiability |
|---|---|
| Inputs to the call-out (`$scored`, `$market-state`) | Fully verifiable — derived from synart state |
| Call-out output (the ranked result) | NOT verifiable — non-deterministic LLM response |
| Output-shape conformance | Verifiable — synart code checks shape |
| What the strategy does *with* the output | Fully verifiable — synart code from there onward |

Wardens running the same strategy with their own LLM at the same
call-out site will produce different outputs but identical strategy
structure. **Disagreement on the LLM output is expected; disagreement
on what the strategy did with the output is a halt-the-baseline signal.**
This is how the call-out primitive preserves alignment despite
non-determinism.

### Why this isn't a generic foreign function call

Three properties distinguish it:

1. **Service is a synart-known name.** `llm-rank`, `classifier-spam`,
   `scorer-credit-risk` — these are catalog entries that all tels can
   register implementations for. Adding a new call-out service is
   governance-paced.
2. **Output shape is declared.** Synart can validate; rogue cognition
   can't return arbitrary structures that confuse the strategy.
3. **Provenance is recorded.** Each call-out invocation writes an audit
   atom: which service was called, what inputs, what output, how long
   it took. This is what wardens read to compare.

### Constraints

- Call-outs are the **only** sanctioned way for synart-resolved code to
  consult local cognition. Direct telart access from synart loops is
  forbidden (would break the audit story).
- Call-outs SHOULD have bounded latency (seconds, not minutes). Long
  call-outs starve the loop's heartbeat.
- Call-outs MUST be idempotent in their effect on synart — the same
  inputs at the same loop tick should produce the same write to synart,
  even if the call-out response varies.

---

## 6. Relay and sentinel patterns

The action-beacon taxonomy splits into two classes by cognitive
density:

- **Relay** — pure synart-resolved I/O, no call-outs. Deterministic strategy. Universal templates at `&core.loop.relay.<stem>`.
- **Sentinel** — call-out density into operator telart. Per-operator strategy. Loop body lives in the operated entity's entart (no universal template).

This collapses the legacy "Baseline / Stream / Warden formation" into
three different classes:

| Legacy role | New class | Why |
|---|---|---|
| Baseline | relay (stem `baseline-`) | Strategy is deterministic synart code post-noemar; no real cognitive density |
| Warden | relay (stem `warden-`) | Verify+halt is deterministic synart re-derivation against chain state via grounded primitive |
| Stream | sentinel (variant stream) | Genuinely requires local cognition for intent proposal |
| Principal | sentinel (variant principal-sentinel) | Direct PAU control with discretionary cognition |

The "formation" is no longer a beacon subclass — it's a deployment
pattern: a `baseline-{prime}` relay + zero-or-more `stream-{prime}-{actor}`
sentinels + ≥1 `warden-{prime}-{op}` relays all wired to one PAU. P1
omits sentinels entirely — only deterministic relays, govops-controlled.

### baseline-relay — fully deterministic

```metta
;; in &core.loop.relay.baseline (universal template)
(= (heartbeat)
   (let* (($entity     (match &self (entity-bound-to $e) $e))
          ($chain-state (chain-read (target-pau $entity)))   ; grounded primitive
          ($candidates (enumerate-allocations $chain-state $entity))
          ;; deterministic ranking — no call-out
          ($selected   (deterministic-rank $candidates $entity))
          ($safe?      (within-baseline-envelope $selected $entity)))
     (case $safe?
       ((True  (gate-out (sign-and-emit $selected)))
        (False (audit-rejected $selected))))))
```

| Property | Value |
|---|---|
| Synart-determined share | 100% |
| Call-out share | 0% |
| Audit story | Fully verifiable — any warden re-runs the same synart |
| Warden re-derivation | Identical answer expected (deterministic) |

The deterministic ranking is a synart-resolved function — could be
priority-table lookup, RAR-optimization, governance-set bias, whatever
the strategy specifies. The point is that it's verifiable.

### stream-sentinel — cognitive proposal

```metta
;; in &entity.prime.spark.sentinel.{actor} (per-operator, NOT a universal template)
(= (heartbeat)
   (let* (($entity     (match &self (entity-bound-to $e) $e))
          ;; cognitive call-out into operator telart
          ($proposal   (call-out cognitive-propose
                         (inputs (current-context $entity))
                         (output-shape proposal-record)))
          ;; synart-side boundary check
          ($bounds     (match &self (rti-bounds $b) $b))
          ($within?    (proposal-within-bounds $proposal $bounds))
          ($formatted  (format-for-baseline $proposal)))
     (case $within?
       ((True  (emit-to-baseline $formatted))
        (False (audit-out-of-bounds $proposal))))))
```

| Property | Value |
|---|---|
| Synart-determined share | ~10% (bounds + comm protocol) |
| Call-out share | ~90% (proposal cognition) |
| Audit story | Bounds enforcement verifiable; proposal content is private cognition |
| Holds PAU keys? | No — emits intent for baseline-relay to consume |

The sentinel loop lives in the entity's entart, not in `&core.loop.*` —
strategy is per-operator and the cognitive substance lives in the
operator's telart agart, off-corpus.

### warden-relay — deterministic re-derivation

```metta
;; in &core.loop.relay.warden (universal template)
(= (heartbeat)
   (let* (($entity         (match &self (entity-bound-to $e) $e))
          ($chain-state     (chain-read (target-pau $entity)))
          ($candidates     (enumerate-allocations $chain-state $entity))
          ($expected       (deterministic-rank $candidates $entity))
          ;; what did the baseline-relay actually do?
          ($baseline-action (latest-baseline-action $entity))
          ($agreement (action-agrees-with $baseline-action $expected
                                          (tolerance loose))))
     (case $agreement
       ((agree            audit-clean)
        (disagree-minor   (audit-flag-soft))
        (disagree-major   (gate-out (freeze-beam $entity)))))))
```

| Property | Value |
|---|---|
| Synart-determined share | 100% |
| Call-out share | 0% |
| Audit story | Re-runs baseline's strategy deterministically; divergence is unambiguous |
| Triggers halt | When baseline output diverges from expected past tolerance |

Halt mechanism: a warden with freeze authority emits a BEAM freeze
through gate-out. On chain, the baseline-relay's pBEAM stops working
until governance review.

### Operating-setup interactions

```
stream-sentinel (optional, cognitive, off-corpus)
   │
   │ intent within RTI
   ▼
baseline-relay (deterministic, holds PAU keys)
   │
   │ chain tx
   ▼
chain state (readable by anyone via (chain-read …))
   ▲
   │ re-derive
   │
warden-relay × N (independent, deterministic)
   │
   ▼
agree → continue / disagree → freeze BEAM
```

All inter-component communication goes through synart-defined channels
(`gate-out (emit-to-baseline …)`, `gate-out (freeze-beam …)`). No
out-of-band coordination — every interaction is auditable.

### The TTS bound

Time-to-stop (TTS) is the window between baseline-relay doing something
wrong and a warden-relay halting it. Because both are deterministic
relays operating against the grounded chain-read primitive, TTS drops
the call-out-latency term that the legacy formation model carried:

```
TTS = (warden tick interval) + (warden synart re-derive latency) + (halt propagation)
```

Each component has a bound; the sum is a per-setup structural constant.
Designing setups with low TTS is governance's lever for how dangerous
baselines are allowed to be.

### Per-entity instantiation

Relay loops follow the two-step loop pattern (`topology.md` §17) —
universal template at `&core.loop.relay.<stem>`, per-entity config in
the entity's entart:

```
&core.loop.relay.baseline                       ← universal template
&entity.prime.spark.relay.baseline              ← Spark's per-Prime config
&entity.prime.grove.relay.baseline              ← Grove's per-Prime config

&core.loop.relay.warden                         ← universal template
&entity.prime.spark.relay.warden.sentinelco     ← per-Prime per-operator config

&core.loop.relay.nfat                           ← universal template
&entity.halo.spark-term.relay.nfat              ← per-Halo config
```

Sentinel loops have **no universal template** — strategy is
per-operator. Per-entity sentinel Space holds bounds + envelope-check +
gate-out shape + call-out registry pointers:

```
&entity.prime.spark.sentinel.horizonlabs        ← stream-sentinel for Spark (operator: HorizonLabs)
&entity.folio.{owner}.sentinel-principal        ← principal-sentinel for a folio
```

### The architecture is continuous, not binary

A relay with zero call-outs and a sentinel with massive call-out are
endpoints of a continuum: any beacon could be designed with anywhere
between 0% and 100% call-out density. The class split (relay = 0%,
sentinel > 0%) is a useful regulatory cut, not a structural barrier.
Most useful beacons sit at one of the two endpoints because the
governance + audit + ORC machinery is calibrated for them.

This is the structural realization of "intelligence private, power
regulated" — synart envelope enforces bounds; call-outs admit cognition
at designated points; the ratio between them is a per-recipe choice
governance makes when defining a new beacon class.

---

## 7. Tranche-rule patterns

Per [`../risk-framework/book-primitive.md`](../risk-framework/book-primitive.md) §3, tranches generalize from "fixed claim" to "rule-bearing claim" — the seniority order is fixed at book creation but the *amount* of the claim can be rule-determined. The synlang patterns:

### Static tranche (most common)

```metta
(book-tranche my-bond
   (seniority 1)
   (holder spark-halo)
   (notional 1000000)                                    ; static
   (denom usd))
```

### Rule-determined notional (callable bond, conversion option)

```metta
(book-tranche callable-tranche
   (seniority 1)
   (holder some-investor)
   (notional-rule (callable-payoff $strike $expiry))     ; rule-determined
   (denom usd))

(= (callable-payoff $strike $expiry)
   (case (>= now $expiry)
     ((True (max 0 (- (book-state-of-issuer underlying-price) $strike)))
      (False (par-value)))))
```

### Step-up coupon tranche

```metta
(book-tranche step-up-tranche
   (seniority 2)
   (holder some-investor)
   (notional-rule (step-up-schedule $base-notional $step-table))
   (denom usd))

(= (step-up-schedule $base $schedule)
   (let (($months-elapsed (months-since (book-creation-date))))
     (* $base (lookup-rate $schedule $months-elapsed))))
```

### Triggered subordination

```metta
(book-tranche triggered-tranche
   (seniority-rule (subordination-trigger $health-factor-threshold))
   (holder some-investor)
   (notional 5000000)
   (denom usd))

(= (subordination-trigger $threshold)
   (case (< (book-health-factor) $threshold)
     ((True 0)                                           ; becomes most-junior
      (False 2))))                                       ; otherwise stays in original position
```

### Tranche rights (P + T declarations)

Per [`../risk-framework/tranching.md`](../risk-framework/tranching.md) §4:

```metta
(tranche-rights spark-halo-senior-tranche
   (redemption-rights (only-at-maturity))                ; P
   (transfer-rights none)                                ; T
   (liquidation-acceleration (on-health-factor-breach))) ; P
```

P and T declarations feed the Primebook sub-book router per [`../risk-framework/primebook-composition.md`](../risk-framework/primebook-composition.md).

---

## 8. Projection-model declaration patterns

Per [`../risk-framework/projection-models.md`](../risk-framework/projection-models.md), risk forms declare projection models for complex positions that don't fit direct-tranche math. The synlang patterns:

### Vanilla European call (Black-Scholes)

```metta
(risk-form-def vanilla-european-call
   (level position-instrument)
   (projection-model black-scholes
      (variables strike expiry notional underlying-price implied-vol risk-free-rate)
      (under-scenario $s
         (let* (($u-stressed (apply-scenario $s underlying-price))
                ($v-stressed (apply-scenario $s implied-vol)))
           (compute-bs-pnl $u-stressed $v-stressed strike expiry notional))))
   (model-uncertainty-haircut 0.0))                      ; well-validated
```

### Path-dependent option (Monte Carlo)

```metta
(risk-form-def asian-option
   (level position-instrument)
   (projection-model monte-carlo
      (variables strike expiry notional underlying-process averaging-window)
      (under-scenario $s
         (let* (($paths (generate-stressed-paths $s underlying-process averaging-window 10000)))
           (mean (map (lambda ($path) (asian-payoff $path strike notional)) $paths))))
      (sample-size 10000))
   (model-uncertainty-haircut 0.10))                     ; Monte Carlo error + path-dependency
```

### Callable bond (lattice)

```metta
(risk-form-def callable-bond
   (level position-instrument)
   (projection-model binomial-lattice
      (variables coupon maturity call-schedule rate-process)
      (under-scenario $s
         (let* (($lattice (build-lattice $s rate-process maturity))
                ($value (backward-induct $lattice coupon call-schedule)))
           (- (par-value) $value))))
   (model-uncertainty-haircut 0.05))                     ; well-established
```

### CDS (parametric)

```metta
(risk-form-def cds-position
   (level position-instrument)
   (projection-model parametric-credit
      (variables reference-entity notional protection-period counterparty-rating)
      (under-scenario $s
         (let* (($default-prob (apply-credit-stress $s reference-entity))
                ($lgd          (lgd-for-reference-entity reference-entity))
                ($cp-survival  (counterparty-survival-prob $counterparty-rating $s))
                ($expected-payoff (* $default-prob $lgd notional $cp-survival)))
           (- (premium-paid) $expected-payoff))))
   (model-uncertainty-haircut 0.05))
```

### Novel instrument (high uncertainty)

```metta
(risk-form-def some-novel-derivative
   (level position-instrument)
   (projection-model novel-stochastic-model
      (variables ...)
      (under-scenario $s ...))
   (model-uncertainty-haircut 0.30))                     ; bleeding-edge → conservative
```

### Composing projection into Riskbook risk form

A Riskbook risk form that holds projection-using positions invokes the model:

```metta
(risk-form-def options-portfolio
   (level riskbook)
   (composition-constraints (only-vanilla-options))
   (equation-m2m
      (sum-over (held-positions)
         (lambda ($pos)
            (let* (($form (form-of $pos))
                   ($projected-loss (project-with-model
                                       (projection-model-of $form)
                                       $pos
                                       (current-scenario))))
              (* $projected-loss (+ 1.0 (model-uncertainty-haircut-of $form)))))))
   (resolution-tier simulation))
```

Categories without declared projections fall through to CRR 100% per default-deny.
