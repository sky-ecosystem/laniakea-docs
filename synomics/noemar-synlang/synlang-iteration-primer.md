# Synlang Iteration Primer — Deontic Skeleton

Self-contained context for an agent starting work on synlang patterns
that encode the Synome's deontic skeleton. Inline summaries of every
load-bearing concept; deep-dive file paths only when the inline
summary isn't enough.

---

## Architecture

**Five layers**, top to bottom:

1. **Synome** — Atlas (constitutional, human-readable), Language Intent (translator), Synomic Axioms (machine-readable rules), Synomic Library (canonical KB).
2. **Synomic Agents** — Sky Superagent (Sky Voters + Core Council), Effectors, agent types organized by rank.
3. **Teleonomes** — autonomous AI entities. "Private persons / private companies." Have their own Directive + Axioms + Library + Dreamarts + Embodiment Interface + Resource Register.
4. **Embodiment** — instance of a teleonome. Local Data, Orchestrator, Resources.
5. **Embodied Agent** — running thread + beacons + hardware.

**Three artifact scopes** (knowledge boundaries):

| Scope | = Layers | Visibility | Authority |
|---|---|---|---|
| **synart** | 1+2 | identical across all aligned entities | highest, slowest-changing |
| **telart** | synart + 3 | per teleonome, shared across embodiments | private to teleonome |
| **embart** | telart + 4 | per embodiment | local, fastest |

Authority flows downward: synart > telart > embart. Risk gates authority — high-risk decisions cannot rely on embart alone.

**Agent ranks** (the deontic chain we'll be encoding):

| Rank | Types | Governance Relationship |
|---|---|---|
| **0** | Core Council | Sovereign |
| **1** | Guardians, Core Controlled Agents, Recovery Agents | Directly regulated by Core Council |
| **2** | Primes, Generators | Accordant to a Guardian |
| **3** | Halos, Folio Agents | Administered by a Prime |

Below Halo: Class → Book → Unit (operational tags, not separate ranked agents).

**Beacon framework** — the only way private cognition affects the world:

|              | Low Authority (independent) | High Authority (Synomic Agent) |
|---|---|---|
| **Low Power**  | LPLA — reporting / data | LPHA — keepers / deterministic execution |
| **High Power** | HPLA — advanced trading | HPHA — sentinels / governance execution |

Sentinels are an HPHA subclass with Baseline (`stl-base`) / Stream (`stl-stream`) / Warden (`stl-warden`) formations. Phase 1 only uses LPHA/LPLA.

**Structural invariants** (cannot be violated by any pattern):

1. Teleonomes think; beacons act.
2. Beacons are apertures, not minds.
3. All enforcement bottoms out in embodiments.
4. Embodiments may host many agents and beacons.
5. Beacon sophistication is constrained by embodiment power.
6. Intelligence lives privately; power enters the world only through regulated apertures.

**Atlas / Synome separation** — Atlas is the human-readable constitutional doc (one node). Synome is the machine-readable graph database. Atlas is embedded in the Synome as the root node. Humans verify Atlas reflects values; machines verify Synome conforms to Atlas. All human directives at every layer pass through Language Intent — single trusted translator.

---

## Dual architecture

**Deontic skeleton** — sparse, deterministic, hard. Axioms, governance decisions, authority hierarchies, enforcement. Once set, holds unconditionally. This is what we're encoding.

**Probabilistic mesh** — dense, soft, weighted. Knowledge with `(strength, confidence)` truth values, evidence, RSI artifacts. Not in scope for skeleton work.

**Crystallization interface** — where mesh becomes skeleton. Governance consumes probabilistic evidence and produces deontic commitments. A pattern proven in mesh ossifies into a `(1, 1)` deontic rule via governance approval.

**Truth values** — every assertion carries `(strength, confidence)`. The deontic case is `(1, 1)`. Everything in this work is `(1, 1)` unless explicitly modeling probabilistic edges.

---

## Synlang language essentials

S-expressions grounded in the synomic library. Same notation Lisp pioneered.

```
(= (croaks Fritz) True)
(= (frog $x) (and (croaks $x) (eats_flies $x)))
(allocation Generator (to Spark 40) (to Grove 30) (to Keel 30))
```

Three load-bearing commitments:

- **Homoiconicity** — code = data = knowledge = reasoning traces. Self-modification operates on one data structure at every level.
- **Compositionality** — n-ary structures nest naturally. A multi-party allocation is one expression, not a triple-store workaround.
- **Library grounding** — symbols draw meaning from the shared synomic library.

**Atom kinds** (from AETHER/Noemar runtime):

- `Atom` — symbols, numbers, booleans, strings
- `Variable` — `$x`, `$_` wildcard
- `Expression` — `(head arg1 arg2 …)`, may carry an optional belief field
- `Rule` — `(= lhs rhs)` with canonical form
- Belief / Provenance — abstract belief interface

**Type annotations are atoms** (no rigid built-in type system):

```metta
(: Socrates Human)
(: mother (-> Human Human))
```

---

## AETHER runtime constraints (what actually bites)

The runtime is real but maturing. Patterns must respect these:

| Constraint | When it bites | Workaround |
|---|---|---|
| **Existentials only allowed under `and`/`or`/`not` heads** | `(if (and (foo $x $unbound)) …)` raises `StructuralValidationError` | Pre-bind every variable in the action LHS. Use flat capability facts. |
| **Bare `(and …)` body doesn't boolean-eval** | Rule body silently rewrites to the unevaluated conjunction; pipeline's `result == True` check passes everything | Wrap rule bodies in `(if (and …) True False)` |
| **Wildcard `$_` in flat fact inside `(and …)`** (QR-010) | `(attestation $book pre-deployment $_)` doesn't reduce to `True` | Write a separate flat 1-arg presence flag |
| **Recursive/transitive closure over bare facts** (QR-009) | `(reaches $a $b)` walking accordancy edges hangs or fails | Replace with append-only flat capability chain — write a 2-arg fact at construction time, check it at use time |
| **Protocol composition takes only `results[0]`** | Nested protocol calls don't cross-product | Not load-bearing for skeleton patterns yet |
| **Identical-intent retries produce identical sigs** | In-process loops can't rotate beacon nonces naturally | Driver appends `sn1, sn2, …` to each payload before signing |
| **Aggregation via `collapse`/`fold`** | Brittle; hits QR-009/010 territory | Avoid in skeleton patterns; do aggregation in Python effects |

---

## Established synlang patterns

### Pipeline shape

```
external submission
  → Stage 1: gate (ed25519 verify against (certified-beacon-key …) facts)
  → Stage 2: pipeline
       1. parse payload
       2. head ∈ effect-protocol allowlist
       3. query (permits $beacon $action) → True?
       4. dispatch Python effect
       5. write audit row
```

Authority lives **only** in step 3. Effect can fail for structural reasons (state, idempotency) but never decides authority.

### Atom layer convention

Every fact is flat — head + 2-3 atom args. No nested expressions inside facts. This is what the inverted index hits in O(1).

```metta
(prime spark-prime)
(administers phoenix-govops spark-prime)
(certified-beacon-key phoenix-govops "ab9c…")
(beacon-status phoenix-govops active)
(in-class phoenix-govops LPHA)
(beacon-role phoenix-govops govops)
```

### Permission rule template

```metta
(= (permits $beacon (VERB ARGS… $nonce))
   (if (and (in-class      $beacon LPHA)
            (beacon-role   $beacon ROLE)
            (beacon-status $beacon active)
            <flat membership checks…>)
       True
       False))
```

- `(if … True False)` forces a definite boolean
- Trailing `$nonce` ignored by body, present so retries get distinct sigs
- Every variable in body must trace to LHS — no existentials

### Flat capability-fact pattern (the central decision)

The natural design — `(can $caller $verb $target)` walking the accordancy graph — fails AETHER's QR-009 (closure over bare facts) and forces existentials. **Rewrite:** every constructor writes a flat 2-arg capability fact; every downstream rule checks it directly.

```
(administers $govops $prime)        ─┐  seed (Core Council writes)
                                     │
   create-halo writes ────────────►  (halo-admin $halo $govops)
                                     │
   create-book writes ────────────►  (book-admin $book $govops)
                                     │
   transition / attest rules check ──┘
```

Both args of every capability fact appear in the action LHS or `permits` head. Zero existentials. No closure. The chain is **append-only and one-directional** — you can't write a rule that bypasses an earlier link without contradicting an existing fact.

### Constructor (Python effect) shape

```python
def create_halo(space, action, *, beacon_id, clock):
    if len(action.args) != 3:
        raise EffectError(...)
    halo  = action.args[0].canonical()
    prime = action.args[1].canonical()
    if list(space.query(parse(f"(halo {halo})")[0])):
        raise EffectError(f"halo {halo} already exists")
    space.add(parse(f"(halo {halo})")[0])
    space.add(parse(f"(halo-prime {halo} {prime})")[0])
    space.add(parse(f"(halo-admin {halo} {beacon_id})")[0])  # ← chain link
```

Conventions:

- Trailing nonce arg → discarded
- Idempotency check before any `add`
- Capability fact writes happen here, not in the policy
- No authority decisions — `permits` already passed before this runs

### State machine as data

Transition table = set of permission rules. One rule per allowed `(src, dst)` pair. Each binds `$src` and `$dst` as ground atoms in its LHS:

```metta
(= (permits $beacon (transition-book $book offboarding deploying $nonce))
   (if (and (in-class $beacon LPHA)
            (beacon-role $beacon govops)
            (beacon-status $beacon active)
            (book-state $book offboarding)
            (has-pre-deployment-attestation $book)    ; ← gate flag
            (book-admin $book $beacon))
       True
       False))
```

Default-deny by absence: an untabled transition returns no `permits` results → policy denies.

### Attestation as positive flag

Policy can't reliably consume `(attestation $book pre-deployment $_)` inside `(and …)`. Effect writes **two** atoms — one structured for replay, one flat presence flag for policy:

```python
space.add(parse(f"(attestation {book} pre-deployment {att_id})")[0])  # audit
space.add(parse(f"(has-pre-deployment-attestation {book})")[0])       # policy
```

### Beacon identity (real ed25519)

Registration mints an ed25519 keypair, writes the pubkey as a fact:

```python
self.space.add(parse(f'(certified-beacon-key {beacon_id} "{pk_hex}")')[0])
self.space.add(parse(f"(beacon-status {beacon_id} active)")[0])
self.space.add(parse(f"(in-class {beacon_id} {beacon_class})")[0])
```

Submit signs with the private key. Gate verifies against the registered pubkey by querying the Space (no external cache). Revoke = retract `(certified-beacon-key …)`; gate slams shut on next message.

### Replay protection

Driver appends `sn{N}` to every payload before signing. Identical intent → distinct bytes → distinct sig. Permission rules pattern the trailing atom as `$nonce` and ignore it.

---

## Cross-Space conventions (Phase-1 commitments)

Even when running single-Space, write code as if multi-Space already:

1. **Space is always a parameter, never implicit.** `(add-atom &operational …)`, `(match &governance …)`.
2. **Append-only writes.** `add-atom` for creation; `remove-atom` only for explicit revocation. Required for replication, audit, fork/promote, content-addressing.
3. **Content-addressed names.** New entity IDs derive from creator + nonce + content (or content-determined symbol). Cross-Space references survive migration.
4. **Open verb dispatch via whitelist atoms.** `(external-verb $v ...)` registers a verb as externally callable.
5. **Gate as primitive at the trust boundary** even when trivially stubbed.
6. **`(can $caller $verb $target)` reads from a named auth Space**, even if that Space currently aliases to the same physical store.
7. **Idempotent constructors.** Calling twice with same args produces same atom or harmlessly no-ops.

The four conventional Spaces:

| Space | Contents | Read freq | Write freq |
|---|---|---|---|
| `&genesis` | Atlas, Axioms, Language Intent config | Constant | Near-immutable |
| `&governance` | Cert, auth, agent registry, beacon pubkeys | Constant | Slow |
| `&operational` | Books, units, settlement records | Constant | Fast |
| `&library` | Mesh knowledge, beliefs | Constant | Very fast |

Within one Synome runtime, cross-Space writes are direct `(add-atom &other-space …)`. The gate is for **trust** boundaries (external beacons, federated synomes), not Space boundaries.

---

## Pattern families to build (skeleton surface)

The GovOps demo covers two of these. Everything else is open.

| Pattern family | Scope | Status |
|---|---|---|
| Authority chain (Council → Guardian → Prime → Halo) | synart | Sketched; full hierarchy not built |
| Beacon lifecycle (cert / auth / revoke / status transitions) | synart `&governance` | Demo's registration is direct `space.add`; no constructor |
| Agent construction (Directive + Axioms + Resources = Agent) | synart | Not started |
| Accordancy / administration edges | synart | Demo uses `(administers …)`; full accordancy patterns not built |
| Governance proposals (vote / ratify / enact) | synart | Not started |
| State machines | synart | Demo covers Book lifecycle; broader pattern abstractable |
| Attestation gates / two-beacon patterns | synart | Demo covers single-actor; multi-beacon split not built |
| Crystallization commits (mesh → skeleton promotion) | synart | Not started |
| Rate limits & enforcement caps (LPLA/LPHA/HPLA/HPHA) | synart | Not started |
| Cross-Space atomic writes | multi-Space | Conventions defined, not exercised |
| Revocation cascades (Guardian collapse → propagation) | synart | Not started |
| Sentinel formations (Baseline / Stream / Warden) | synart + telart edge | Not started; HPHA only |

---

## Working file map (when inline summary isn't enough)

Source-of-truth docs (read selectively when a specific pattern needs depth):

| File | When to open it |
|---|---|
| `laniakea-docs/synomics/macrosynomics/synome-layers.md` | Full layer specs, artifact mapping, permanent design choices |
| `laniakea-docs/synomics/macrosynomics/synomic-agents.md` | Agent rank hierarchy, accordancy/admin semantics, Synomic Agent formula |
| `laniakea-docs/synomics/macrosynomics/beacon-framework.md` | Full LPLA/LPHA/HPLA/HPHA taxonomy, sentinel formations |
| `laniakea-docs/synomics/macrosynomics/atlas-synome-separation.md` | Atlas vs Synome boundary in detail |
| `laniakea-docs/synomics/synodoxics/synlang.md` | Synlang language reference |
| `laniakea-docs/synomics/core-concepts/*.md` | One-paragraph atomic concept definitions (~30 lines each) |

Working notes and code (already in `noemar-work/`):

| File | What it gives you |
|---|---|
| `noemar-work/synlang-context.md` | Halo/Class/Book/Unit conservation-network kernel; four-constructor MeTTa surface; sentinel decision rule with full code |
| `noemar-work/synart-access-and-runtime.md` | Auth domains, role/cert/auth model, gate primitive, in-synlang heartbeat, multi-Space scaling, 16 migration principles |
| `noemar-work/govops-synlang-patterns.md` | Working pattern catalog from the demo — pipeline, atom layer, full rule set, AETHER constraints table |
| `noemar-work/aether-notes-codex.md` | Honest review of AETHER capabilities — sharp edges section is the practical reference |
| `noemar-work/aether/examples/govops_demo/` | Runnable reference — `seed.synlang`, `policy.synlang`, `effects.py`, `run_demo.py`, `test_govops_demo.py` |
