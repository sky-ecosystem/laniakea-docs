# Synlang Context — Starter Document

This is a self-contained context document for iterating on the foundational synomic structures in synlang (MeTTa-style S-expressions, runnable in AETHER).

**How to use:** Paste the **Priming Prompt** section into a fresh conversation. The reference sections below are inlined so the conversation can draw on them without reading external files.

---

# Part 1 — Priming Prompt (paste this)

```text
We're going to iteratively build foundational synomic structures from
scratch in synlang (MeTTa-style S-expressions, runnable in AETHER).
This is the second pass — the first conversation reached a synthesis I
want to keep and refine.

The reference material you need is below in this same doc. Don't go
read external files unless you find a gap. The CLAUDE.md project
context is auto-loaded.

──── The metaphysical kernel we landed on ────
The whole architecture is a conservation network on a directed weighted
multigraph. Books are nodes. Units are edges. Internal nodes conserve
flow (assets = liabilities). External nodes (USDS holders at the top,
real-world borrowers at the bottom) are sources/sinks. Halo and Class
are operational tags grouping books — they're metadata on the graph,
not separate entities.

In one sentence: BOOKS BALANCE, UNITS BRIDGE, EVERYTHING ELSE IS METADATA.

──── The four-constructor surface (engineering version) ────
We narrowed the API to exactly enough degrees of freedom that any
buildable state is a legal state. The typed MeTTa version we ended at:

(: Halo Type)  (: Class Type)  (: Book Type)  (: Unit Type)
(: BookState Type)  (: created BookState) (: filling BookState) ...
(: ClassType Type) (: AssetKind Type) (: Result Type)
(: Created (-> Symbol Symbol Result))
(: Issued  (-> Unit Result))
(: Error   (-> Symbol Atom Result))

(: create-halo  (-> Symbol Symbol Result))
(: create-class (-> Symbol Halo ClassType Number Number Result))
(: create-book  (-> Symbol Class Result))
(: issue-unit   (-> Symbol Book Symbol Number AssetKind Result))

;; Each constructor: add-atom the typed atom + relation atoms, atomically.
;; issue-unit additionally records the asset that came in, so balance is
;; preserved by construction. Liability is *derived* via bridging rules:

(= (liabilities-of $book)
   (match &self (unit $u (issuer $book) (holder $_) $a) ($u $a)))
(= (assets-held-by $holder)
   (match &self (unit $u (issuer $_) (holder $holder) $a) ($u $a)))

The previous conversation also worked through CRR factors per book state,
encumbrance ratio for Primes, and a sentinel example computing
risk-adjusted return as a strategy living in the Synome.

──── What I want from this session ────
Start a foundation-problem-statement.md that establishes the criteria
the foundational primitives have to meet before we begin constructing
them. Then we iterate code: refine the four constructors, add state
transitions and redemptions in the same shape, build out the deontic
core and the deontic/probabilistic interface (PLN belief annotations
on primitives without contaminating their axiomatic status).

──── Style preferences ────
- MeTTa-correct synlang. Use proper (: …) types, (-> …) function
  signatures, case/Empty for guards, let* with $_ for sequencing
  add-atoms, &self for the current space.
- Atomicity in constructors: every constructor is "add a typed atom
  + the relation atoms + any derived effects" or it errors. Never
  partial.
- Type-level guards beat runtime guards when expressible. Runtime
  guards are honest about why they're not types.
- Be concrete with code blocks; trust me to read them. Don't
  re-explain what the code obviously does.
- When you flag a tradeoff, name both sides explicitly. When
  something doesn't pencil, say "this doesn't pencil."
- Avoid restating what's in CLAUDE.md or the docs unless it's
  load-bearing for what you're saying.
- Length: medium responses by default; long when there's actual
  code or a real argument; short when the answer is short.
- Take MeTTa parity issues seriously — flag where synlang we write
  today would actually not run cleanly in AETHER (collapse/fold
  semantics, transitive closure gaps, QR-009/010), and propose
  alternatives.

──── First task ────
Read the reference material in this doc. Then propose a draft outline
for foundation-problem-statement.md — sections, what each section
commits to, what would make it falsifiable. Don't write the content
yet; we'll iterate on the outline first.
```

---

# Part 2 — Reference Material (already inlined below)

Below are the load-bearing extracts from the synomics docs, the AETHER runtime, and the prior conversation's synthesis. The conversation can quote them directly.

---

## Reference 2.1 — The Synome architecture (distilled macrosynomics)

### The core idea
> Intelligence lives privately; power enters the world only through regulated apertures.

The Synome architecture separates **private cognition** from **public action**. Teleonomes (autonomous AI systems) think privately and accumulate knowledge in the dark. To affect the external world, they must act through **beacons**: registered, observable, revocable interfaces governed by the Synome.

### The five layers (top → bottom)

1. **Synome** — the foundational data layer. Atlas (constitutional doc, ~10-20 pages, human-readable) + Language Intent (translates human directives to machine logic) + Synomic Axioms (machine-readable rules, hard (1,1) truth values) + Synomic Library (canonical knowledge base with truth values).
2. **Synomic Agents** — Sky Superagent (governance), Effectors, Synomic Agent Types (Guardians, Generators, Primes, Halos).
3. **Teleonomes** — aligned autonomous entities with their own missions. Best understood as private persons or private companies.
4. **Embodiment** — a specific instance of a teleonome — an "emb." Local data, orchestrator, scoped resources.
5. **Embodied Agent** — the actual running agent, interacting with the world through beacons.

### Atlas / Synome separation
- **Atlas (human layer):** constitutional doc. Plain language. WHAT must be true.
- **Synome (machine layer):** graph database. ALL operational data. Unlimited size.
- The Atlas is embedded in the Synome as the root node.
- **Verification:** humans verify Atlas reflects their values. Machines verify Synome conforms to Atlas constraints.

### Dual architecture
- **Deontic skeleton:** sparse, hard, deterministic — axioms, governance, authority.
- **Probabilistic mesh:** dense, soft, weighted — knowledge, evidence, learning.
- Governance sits at the **crystallization interface** — consuming probabilistic evidence, producing deontic commitments.

### Beacon framework (2x2)

|              | Low Authority (independent)        | High Authority (Synomic Agent)         |
|---           |---                                  |---                                      |
| **Low Power**  | LPLA — reporting, data            | LPHA — keepers: deterministic execution |
| **High Power** | HPLA — advanced trading, arbitrage | HPHA — sentinels, governance execution  |

**Sentinels** are a distinguished HPHA subclass operating as coordinated formations: **Baseline** (stl-base, primary execution), **Stream** (stl-stream, intent streaming), **Warden** (stl-warden, independent monitoring + halt).

### Structural invariants
1. Teleonomes think; beacons act.
2. Beacons are apertures, not minds.
3. All enforcement bottoms out in embodiments.
4. Embodiments may host many agents and beacons.
5. Beacon sophistication is constrained by embodiment power.
6. Intelligence lives privately; power enters the world only through regulated apertures.

### Permanent design choices
1. Directives as universal human interface.
2. Core loop: Atlas → Language Intent → Axioms → Library → Language Intent.
3. 5-layer model with clear containment.
4. Content addressing (identity = hash of content).
5. (strength, confidence) truth model on all assertions.
6. Probabilistic-deontic dual architecture.
7. Language Intent as single translation layer.

---

## Reference 2.2 — Synlang and AETHER (distilled synodoxics + AETHER readme)

### What is synlang? What is AETHER?
- **Synlang** is the language: S-expressions grounded in the synomic library. The whole system thinks in synlang — symbolic side, neural nets, mesh.
- **AETHER** is the runtime: stores synlang expressions, matches patterns, propagates beliefs, dispatches multi-modal reasoning.
- AETHER's `Space` plays the role MeTTa/Hyperon's Atomspace plays — built from scratch with architectural choices targeting performance limitations that block civilizational scale.

### Atom kinds (same as MeTTa)
- **Atom** — symbols, numbers, booleans, strings.
- **Variable** — `$x`, `$_` wildcard.
- **Expression** — `(head arg1 arg2 …)`, can carry an optional `belief` field directly.
- **Rule** — `(= lhs rhs)` with canonical form.
- **Belief / Provenance** — abstract belief interface.

S-expressions are *homoiconic* (code = data) but typed. The system can rewrite its own rules with the same machinery it uses on external data.

### Pattern matching
- **One-way matching:** pattern variables bind against ground expressions.
- **Robinson unification:** symmetric matching, finds MGU; both sides can have variables.
- **Compound patterns:** `and` (intersect binding sets), `or` (union), `not` (complement, NAF/CWA).

### Equality rules drive evaluation
```metta
(= (double $x) (+ $x $x))
! (double 5)   ; → 10
```
1. AETHER sees `(double 5)`.
2. Looks for `(= (double 5) $r)`.
3. Finds `(= (double $x) (+ $x $x))` with `$x = 5`.
4. Rewrites to `(+ 5 5)`.
5. `+` is grounded → `10`.

### The Space (AETHER's central object)
Three-layer query resolution:
1. **Direct fact match** — index lookup (head, arity, position) — O(1) candidates.
2. **Rewriting** — apply rules, evaluate special forms (`if`, `let`, `let*`, `cond`, `quote`, `quasiquote`, `map`, `fold`, `filter`).
3. **Compound resolution** — set ops over the index for `and` (intersect), `or` (union), `not` (complement).

Both OWA (`query`) and CWA (`query_closed` / `ClosedResult`) supported.

### Protocols (grounded extension)
Pluggable inference backends. Each owns a head-symbol prefix.

| Protocol | Heads | Backend |
|---|---|---|
| **PLN** | `pln-*` (21 operators) | scipy + Beta dist (delta-method confidence propagation) |
| **Graph** | `graph-*` | NetworkX |
| **SMT** | `smt-*` | Z3 |
| **SymbolicMath** | `sym-*` | SymPy |
| **Validation** | type-check, schema-validate | built-in |
| **Temporal** | Allen interval | built-in |

Note: ordinary `+ - * /` and comparisons are core rewriter builtins — *not* the SymPy protocol.

### PLN belief = (strength, confidence)
- `strength s` — probability estimate (mean of Beta).
- `confidence c` — pseudo-count via `count = k * c / (1 - c)`.
- `variance = s * (1 - s) / (count + 2)`.
- **Delta-method propagation** — first-order partial derivatives, not heuristic confidence multipliers. This fixes MeTTa's "confidence collapse after 2-3 steps."

### Types are atoms
```metta
(: Socrates Human)
(: mother (-> Human Human))
(: Vec (-> Type Nat Type))
(: Cons (-> $t (Vec $t $n) (Vec $t (S $n))))
```
MeTTa does not have a rigid built-in type system. Types are themselves represented in the Atomspace and can be queried like any other atom.

### RSI (in AETHER)
| Level | What updates | Status |
|---|---|---|
| L1 | Belief calibration | Planned |
| L2 | Prediction calibration | Planned |
| L3 | Rule discovery (regression-tested in staging) | **Implemented** |
| L4 | Source rewriting | Future |

L3 today: agent forks Space → proposes rules → runs regression → diff bindings → promote (additively) or discard.

### MeTTa / AETHER divergences (load-bearing)
- AETHER decouples variable resolution (index lookup) from evaluation (memoized rewriting). Fibonacci becomes O(n), not O(2^n).
- Compound resolution is set-theoretic (intersect/union/complement) like a SQL query planner.
- Space mutation invalidates the memo cache via versioning.
- Promotion in RSI is **additive only** (never removes existing rules).
- Documented divergences: eager evaluation, quote handling, nested nondeterminism, multiset cardinality, nil syntax (see `METTA_PARITY_DIVERGENCES.md`).

### Sharp edges in AETHER (per Codex's notes)
- Recursive/transitive closure over bare facts is weak (QR-009).
- Bare conjunction queries can be variable-name-sensitive and may hang (QR-010).
- Aggregation via `collapse`/`fold` over `match` results works but is the brittlest part.
- Protocol composition takes only `results[0]` of nested protocol args (no cross-product yet).
- RSI protocol-author imports candidate code in-process — not a sandbox.
- Atlas docs ship explicit workarounds for the closure/conjunction issues.

---

## Reference 2.3 — Halo Class / Book / Unit (canonical, full)

### Overview

Halos organize capital into three layers: **Class**, **Book**, and **Unit**. Classes share infrastructure, Books balance assets against liabilities, Units connect one agent's book to another's.

```
Halo Class (shared smart contract infra + default terms)
    |
    +-- Halo Book (balanced ledger)
    |     Assets:      Loan X + Loan Y
    |     Liabilities: Unit 1, Unit 2
    |
    +-- Halo Book (balanced ledger)
          Assets:      Loan Z
          Liabilities: Unit 3
```

### The Book pattern

A Book is a **balanced ledger**: assets on one side, liabilities on the other. Every agent in the Laniakea capital stack maintains books, and they chain together through Units — a Unit is simultaneously an asset in the book above and a liability in the book below.

```
Generator
  Book:
    Liabilities: USDS in circulation
    Assets:      Prime Units
                    │
                    ▼  Unit = connecting tissue
Prime
  Book:
    Liabilities: Units held by Generator
    Assets:      Halo Units
                    │
                    ▼  Unit = connecting tissue
Halo
  Book:
    Liabilities: Units held by Primes
    Assets:      Real-world loans, bonds, positions
```

The recursive structure means the entire capital stack is connected through a uniform pattern of books linked by units. **Phase 1 scope:** only Halo books are implemented. Prime/Generator level book pattern is target architecture but not yet built.

### Halo Class

A Halo Class is the **unit of smart contract infrastructure and default terms**. It defines the product family.

| Component | Purpose |
|---|---|
| **PAU** | Single Controller + ALMProxy + RateLimits shared by all Units in the Class |
| **LPHA Beacon(s)** | `lpha-lcts` for Portfolio; `lpha-nfat` + `lpha-attest` for Term |
| **Legal Buybox** | Acceptable parameter ranges — duration, size, APY, asset types |
| **Queue Contract** | Where capital enters (Primes deposit here) |
| **Redeem Contract** | Where capital exits (Halo deposits returned funds here) |
| **Factory Template** | All Units deployed from the same pre-audited template |

Anything within the buybox can be executed autonomously by the LPHA beacon. Anything outside requires governance intervention. One Class supports many Books and Units.

### Halo Book

A Halo Book is a **balanced ledger** — bankruptcy-remote boundary where the asset side holds real-world positions and the liability side records the Units that claim on those assets.

| Property | Description |
|---|---|
| **Balanced** | Assets = liabilities. |
| **Bankruptcy-remote** | Each book is its own isolation boundary. |
| **Pari passu within** | All Units in same book share losses equally. |
| **Fully isolated across** | Units in different books have zero exposure to each other. |
| **Blended for privacy** | Multiple assets blended in a single book. |
| **Whole assets** | Each asset sits entirely in one book. |
| **Recursive** | A book's assets can include Units from other books. |

> **Phase 1 constraint:** Each Halo book holds a single asset (or multiple assets that must all be in the same state). Multi-asset books with independent asset states are a future extension.

### Book Lifecycle

```
Created --> Filling --> Deploying --> At Rest --> Unwinding --> Closed
```

| Phase | Synome Visibility | CRR Impact |
|---|---|---|
| **Created** | Full | None |
| **Filling** | Full transparency | Low |
| **Deploying** | Obfuscated (Schrodinger's risk) | **High** |
| **At Rest** | Attested risk profile | Medium |
| **Unwinding** | Transitional | -- |
| **Closed** | Archived | -- |

The high CRR during deploying creates economic incentive to minimize the obfuscated period.

### Two-Beacon Deployment Gate

Neither beacon can trigger deployment alone:
1. **lpha-attest** (independent Attestor) posts a risk attestation into the Synome.
2. Only then can **lpha-nfat** transition the book from filling to deploying.

### Halo Unit

A Halo Unit is the **connecting tissue between books**. Within a Halo book, it appears as a liability — what the Halo owes. In the Prime's book above, the same Unit appears as an asset.

Every NFAT maps to a Unit. The Unit maps to a liability in the Halo book. The book holds assets equivalent to its liabilities.

### Two Token Standards

| | Portfolio (LCTS) | Term (NFAT) |
|---|---|---|
| **What the Unit is** | Shares in pooled position | Individual ERC-721 token |
| **Fungibility** | Fungible within pool | Non-fungible — each NFAT has unique terms |
| **Terms** | Same for all participants | Bespoke per deal (within buybox) |
| **Transferability** | Non-transferable | Transferable |

### Unit-to-Book Mapping

| Pattern | Use Case |
|---|---|
| **1 Unit : 1 Book** | Simple bilateral arrangement |
| **Many Units : 1 Book** | Privacy protection — terms can't be inferred |
| **Recursive** | Structured products, tranching across books |

### What Each Layer Controls

| Decision | Layer |
|---|---|
| What contracts are used? | **Class** |
| What parameter ranges are acceptable? | **Class** (buybox) |
| What rate limits apply? | **Class** (PAU) |
| Which beacon operates? | **Class** |
| Where is the bankruptcy-remote boundary? | **Book** |
| Who bears losses if assets fail? | **Book** (pari passu across Units in same book) |
| What blended risk profile do assets have? | **Book** (via attestor) |
| What specific terms does the investor have? | **Unit** |
| Who holds the claim? | **Unit** |
| What can be transferred or traded? | **Unit** |

### Boundaries Summary

```
CLASS boundary = infrastructure sharing
                 (same contracts, same beacon, same legal framework)

BOOK boundary  = risk isolation + balance
                 (bankruptcy remoteness, loss containment, privacy,
                  assets = liabilities)

UNIT boundary  = individual claim + cross-book link
                 (specific terms, specific holder, transferable position,
                  asset in one book ↔ liability in another)
```

### Legal Mapping
| Halo Concept | BVI SPC Equivalent | Delaware Equivalent |
|---|---|---|
| **Halo Class** | The SPC entity itself | The Series LLC parent |
| **Halo Book** | Segregated portfolio (BVI BCA s.146) | Individual series (untested in bankruptcy) |
| **Halo Unit** | Share/interest within a portfolio | Membership interest in a series |

BVI SPCs provide materially stronger book-level isolation than Delaware Series LLCs — BVI statutory segregation has been court-tested.

---

## Reference 2.4 — Phase 1 Halo Book Lifecycle (deep-dive selective)

### Identity and linkage

```
ON-CHAIN                              SYNOME-MVP
─────────                             ──────────
NFAT (ERC-721)                        Halo Unit record
  tokenId: 42          ◄── same ID ──►  unitId: 42
  facility: 0xABC...                    bookId: "book-7"
  principal: 25M                        dealTerms: { ... }
  depositor: 0xPrime...                 state: ACTIVE

                                      Halo Book record
                                        bookId: "book-7"
                                        haloClass: "facility-A"
                                        state: FILLING
                                        assets: [ ... ]
                                        linkedUnits: [42, 43, 44]
                                        attestations: [ ... ]
```

A book has no on-chain representation. It is a Synome record. The NFAT's `tokenId` is the join key.

### Book states and transitions

```
CREATED ──► FILLING ──► OFFBOARDING ──► DEPLOYING ──► AT REST ──► UNWINDING ──► CLOSED
```

### Attestation principle
**Attestation is required before any state change that makes assets not visible on-chain.**

1. Sending assets off-chain (within OFFBOARDING, before external transfer) — pre-deployment attestation.
2. Entering obfuscated deployment (OFFBOARDING → DEPLOYING) — same gate.
3. Entering at-rest (DEPLOYING → AT REST) — at-rest attestation.

Any state where assets are on-chain and transparent (CREATED, FILLING, UNWINDING, CLOSED) does not require attestation to enter.

### Write Access Matrix

| Operation | Who Writes | Preconditions |
|---|---|---|
| Create book | lpha-nfat | — |
| Add unit to book (sweep) | lpha-nfat | Book is in FILLING state |
| Update book assets (offboarding sub-steps) | lpha-nfat | Book is in OFFBOARDING state |
| Transition FILLING → OFFBOARDING | lpha-nfat | — (no attestation required) |
| Convert USDS → USDC (offboarding step 1) | lpha-nfat | Book is in OFFBOARDING state |
| Post pre-deployment attestation | lpha-attest | Book is in OFFBOARDING state, USDC conversion complete |
| Send USDC externally (offboarding step 2) | lpha-nfat | Pre-deployment attestation exists from lpha-attest |
| Transition OFFBOARDING → DEPLOYING | lpha-nfat | Pre-deployment attestation exists; all funds confirmed received |
| Post at-rest attestation | lpha-attest | Book is in DEPLOYING state |
| Transition DEPLOYING → AT REST | lpha-nfat | At-rest attestation exists from lpha-attest |
| Write aggregate risk data to book | lpha-nfat | At-rest attestation provides the data |
| Post periodic attestation | lpha-attest | Book is in AT_REST state |
| Update book with periodic attestation | lpha-nfat | New periodic attestation exists |
| Transition AT REST → UNWINDING | lpha-nfat | Assets returning |
| Update book assets (unwinding sub-steps) | lpha-nfat | Book is in UNWINDING state |
| Transition UNWINDING → CLOSED | lpha-nfat | All linked units redeemed |

**Read access:** lpla-verify reads everything. lpha-attest reads book state to know when attestation is needed.

### Loss distribution

If a book returns less than expected (partial default), proceeds distribute **pro rata by principal** across linked units. Phase 1 uses bullet loans only; default scenarios handled via legal recourse, but Synome should track pro-rata entitlements.

---

## Reference 2.5 — Sentinel formations (compact summary)

### The four sentinel types
- **stl-base** (Baseline) — public/open-source, holds Execution Engine and pBEAMs, runs the Base Strategy from the Prime Artifact. Three parallel processes: counterfactual simulation, streaming-monitor, active-management fail-safe.
- **stl-stream** (Stream) — proprietary, operated by Ecosystem Actors. Streams *intent* only, never holds keys. Earns carry only when outperforming simulated Base Strategy.
- **stl-warden** (Warden) — independent third-party safety. Continuous monitoring, halt authority over the Execution Engine. Multiple wardens per formation.
- **stl-principal** — owner-operated direct control, no formation, no guardian, no warden.

### TTS economics
- `Maximum Damage = Rate Limit × TTS`
- `Required Risk Capital ≥ Rate Limit × TTS`
- Better wardens → lower TTS → either less risk capital required or higher rate limits permitted.

### Where sentinels apply
- Both Primes and Halos with PAUs *can* be sentinel-operated.
- Currently **Halos run on LPHA beacons** (lpha-lcts, lpha-nfat, lpha-amm, lpha-attest), not sentinels. Sentinels for Halos is future capability.
- **lpla-checker** is the protocol-wide beacon that calculates CRR, TRRC, TRC, Encumbrance Ratio (target ≤ 90%).

---

# Part 3 — Prior Synthesis (the code progression we already worked through)

## 3.1 The simplest possible halo book in synlang (v0)

```synlang
; --- Facts about book-7 ---
(book book-7)
(asset      book-7  cash  75000000)
(liability  book-7  nfat-42  75000000)

; --- The defining rule of a book: balance ---
(= (balanced $book)
   (==
     (match &self (asset     $book $_ $a) $a)
     (match &self (liability $book $_ $l) $l)))

! (balanced book-7)        ; -> True
```

## 3.2 Multi-entry version with aggregation (v1)

```synlang
(book book-7)

(asset book-7  loan-A  30000000)
(asset book-7  loan-B  25000000)
(asset book-7  loan-C  20000000)

(liability book-7  nfat-42  30000000)
(liability book-7  nfat-43  25000000)
(liability book-7  nfat-44  20000000)

(= (sum-assets $book)
   (fold + 0
     (collapse
       (match &self (asset $book $_ $a) $a))))

(= (sum-liabilities $book)
   (fold + 0
     (collapse
       (match &self (liability $book $_ $l) $l))))

(= (balanced $book)
   (== (sum-assets $book) (sum-liabilities $book)))
```

**⚠ AETHER caveat:** the `collapse`/`fold` aggregation is the brittlest part — exactly the QR-009/010 territory. A truly runnable version may need explicit recursive sum rules or a dedicated aggregation protocol.

## 3.3 The cross-book duality — the key insight (v2)

```synlang
; A unit appears as a liability in the issuing book ($issuer)
; and as an asset in the holding book ($holder).
(unit nfat-42 (issuer book-7) (holder spark-prime-book) 30000000)

; --- Bridging rule: project units into both sides ---
(= (liability $issuer $unit $amt)
   (match &self
     (unit $unit (issuer $issuer) (holder $_) $amt)
     True))

(= (asset $holder $unit $amt)
   (match &self
     (unit $unit (issuer $_) (holder $holder) $amt)
     True))
```

**One atom populates two views.** The recursive Generator → Prime → Halo stack falls out automatically.

## 3.4 CRR, encumbrance, state-dependence

```synlang
(crr-factor filling      0.05)   ; USDS, fully transparent
(crr-factor offboarding  0.30)   ; transitional
(crr-factor deploying    1.00)   ; Schrödinger's risk
(crr-factor at-rest      0.40)   ; attested but deployed
(crr-factor unwinding    0.20)   ; assets returning
(crr-factor closed       0.00)

(unit nfat-42 (issuer book-7) (holder spark) 30000000)
(book-state book-7 filling)
(prime-capital spark 500000000)

(= (unit-risk-weight $unit)
   (match &self
     (and (unit $unit (issuer $book) (holder $_) $principal)
          (book-state $book $state)
          (crr-factor $state $factor))
     (* $principal $factor)))

(= (encumbered $prime)
   (fold + 0 (collapse
     (match &self (unit $u (issuer $_) (holder $prime) $_)
       (unit-risk-weight $u)))))

(= (capital-of $prime)
   (match &self (prime-capital $prime $c) $c))

(= (encumbrance-ratio $prime)
   (/ (encumbered $prime) (capital-of $prime)))
```

| `(book-state book-7 …)` | `(unit-risk-weight nfat-42)` | `(encumbrance-ratio spark)` |
|---|---:|---:|
| `filling`     |  1,500,000 | 0.003 |
| `offboarding` |  9,000,000 | 0.018 |
| `deploying`   | 30,000,000 | **0.060** |
| `at-rest`     | 12,000,000 | 0.024 |
| `unwinding`   |  6,000,000 | 0.012 |
| `closed`      |          0 | 0.000 |

20× swing between filling and deploying — same dollar of principal, just a different state on a single fact.

## 3.5 Sentinel decision rule with risk-adjusted return

The Base Strategy is rules in the Synome. The same rules are read by stl-base (decide), stl-warden (verify), stl-stream (propose intent within), and used for counterfactual carry simulation.

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

; --- Risk-adjusted return — Spark's theory of how to weigh trade-offs ---
;     RAR = yield_rate − λ × encumbrance_ratio
(= (risk-adjusted-return $prime)
   (match &self (risk-aversion $prime $lambda)
     (- (yield-rate $prime)
        (* $lambda (encumbrance-ratio $prime)))))

; --- The decision rule: hypothetical RAR for a reallocation ---
(= (hypothetical-rar $prime $from $to $delta)
   (let* (($cap     (capital-of $prime))
          ($lambda  (match &self (risk-aversion $prime $l) $l))
          ($f-from  (match &self (and (book-state $from $s)
                                       (crr-factor $s $f)) $f))
          ($f-to    (match &self (and (book-state $to   $s)
                                       (crr-factor $s $f)) $f))
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
         ($f-from (match &self (and (book-state $from $s) (crr-factor $s $f)) $f))
         ($f-to   (match &self (and (book-state $to   $s) (crr-factor $s $f)) $f))
         ($limit  (match &self (encumbrance-limit $prime $l) $l)))
     (<= (/ (+ (encumbered $prime) (* $delta (- $f-to $f-from))) $cap)
         $limit)))

(= (propose-reallocation $prime $from $to $delta)
   (and (> (rar-improvement $prime $from $to $delta) 0)
        (within-limit $prime $from $to $delta)))
```

Worked example: Spark moves 50M from book-11 (deploying, λ=1.00, yield 14%) → book-9 (at-rest, λ=0.40, yield 8%):
- Δ encumbered = 50M × (0.40 − 1.00) = −30M
- Δ yield = 50M × (0.08 − 0.14) = −3M
- New RAR = 0.030 − 0.15 × 0.123 = **0.01155** (up from 0.0085)
- `propose-reallocation` returns **True**.

The same trade with risk-aversion λ = 0.05 would return False.

**Why this composition matters:** "all execution flows through public Baseline code" translated literally — the strategy is rules in the Space; wardens read the same rules and halt when their evaluation disagrees with baseline's actions; counterfactual simulation = same rules on a forked Space; TTS bounds the damage window between rogue baseline and warden halt.

## 3.6 The four-constructor surface (untyped)

```synlang
;; Each constructor: add-atom a typed atom + the relation atoms.
;; Each constructor's only DOF is what it needs at its layer.
;; By construction, no buildable state can be invalid.

(create-halo  spark-halo  (operator spark-team))

(create-class facility-A
  (in-halo  spark-halo)
  (type     term)
  (buybox   (duration 6m 24m) (size 5M 100M) (apy 0.08 0.15)))

(create-book book-7 (in-class facility-A))

(issue-unit  nfat-42
  (from-book   book-7)
  (to-holder   spark)
  (amount      30000000)
  (asset-kind  usds))
```

## 3.7 The four constructors with proper MeTTa types

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

## 3.8 The Platonic kernel (the absolute simplest framing)

> **A book is a node. A unit is a directed weighted edge. Balance means every internal node conserves flow.**

Kirchhoff's current law applied to claims. The architecture is a **conservation network**. Capital is the conserved quantity, units are wires, books are junctions. USDS holders and real-world borrowers are the unconserved boundaries.

| Framing | Books are… | Units are… | Balance is… |
|---|---|---|---|
| **Flow network** | junctions | wires | Kirchhoff: in = out |
| **Double-entry bookkeeping** | accounts | transactions | every Tx posts to two ledgers |
| **Category theory** | objects | morphisms | composition preserves identity |
| **Promise graph** | bundles of promises | promises | promises made = promises held |
| **Type theory** | types | values bridging types | type preservation under composition |
| **Physics** | reservoirs | pipes | mass conservation |

Same shape, different vocabulary.

## 3.9 The minimum constructor — Platonic version

```
Start: empty universe.
Step:  mint(issuer, holder, amount, policy)
Inv:   for every internal node, Σ(incoming amounts) = Σ(outgoing amounts).
End:   the architecture is whatever set of mints satisfies the invariant.
```

Any compliant Laniakea state is reachable from `{}` by some sequence of valid mints. Any state with a balance violation is unreachable.

The *engineering* version (the four constructors) is this Platonic kernel + a curated lens that exposes only the moves the architecture admits. Anything you can build with `create-halo / create-class / create-book / issue-unit` is correct by construction; anything you can't build with them is something the system shouldn't allow.

---

# Part 4 — What's intentionally NOT in this doc

- The full Phase 1 halo-book deep-dive (state machine sub-steps, exact attestation payload schemas)
- AETHER's RSI roadmap details (Phases 0-6)
- Sentinel formation lifecycle, Streaming Accord, carry math
- The full beacon framework taxonomy
- The Hearth / teleology layer
- Specific halo types (Portfolio/Term/Trading) — these are downstream applications

If a session needs them, it should read the source docs in `laniakea-docs/` directly. The point of this doc is to be a tight foundation context, not a complete reference.
