# Noemar / Synlang

**Status:** Mostly target architecture; topology + boot model + runtime kernel are design-of-record. Phase 1 builds single-Space, single-gate, single-heartbeat with the thirteen commitments from day 1.
**Canonical home:** `laniakea-docs/noemar-synlang/`

---

## TL;DR

Technical reference for the runtime + language layer. **Synlang** is S-expressions grounded in the synomic library (homoiconic, compositional, library-grounded). **The synart is the program**, runtimes (Noemar = one impl) are interpreters, **identity is the entry point**: `noemar boot --identity=X` resolves a loop Space pointer in `&core.registry.beacon` and evaluates `(run-forever)` with that Space as `&self`. Topology = tree of entarts under a six-layer synome root with four meta-patterns. Auth = role + sub-role; the **gate** is the trust boundary at network ingress; the **call-out primitive** is the only sanctioned synart→telart bridge. Loops, gates, recipes, runtime source, and the bootstrap procedure itself are all content in synart, replicated through the same channel as state.

## Section map

| § | Topic |
|---|---|
| 1 | Synlang the language |
| 2 | Topology — entarts, six-layer root, four meta-patterns |
| 3 | Two-step rule and two-step loop patterns |
| 4 | Runtime — auth, gate, heartbeat |
| 5 | Identity-driven boot, shadow execution, hot-swap |
| 6 | Call-out primitive |
| 7 | Sentinel formations as beacons-with-call-outs |
| 8 | Beacons (two-role) and in-space calculation |
| 9 | Risk-framework synlang shapes; worked examples |
| 10 | Scaling — synserv, replication, partitions |
| 11 | Phase 1 commitments and migration principles |

---

## §1. Synlang

S-expressions grounded in the synomic library. Three load-bearing commitments: **homoiconicity** (code = data = knowledge = reasoning traces), **compositionality** (n-ary heads as natural hyperedges; no triple-store reification), **library-grounded symbols**. Resolved: hypergraph as s-expressions; PLN truth values via delta method; inverted-index dispatch + one-way matching + Robinson unification; stochastic TV-weighted traversal. Open: surface conventions, schema/typing, versioning, macro/canonical-form. Runtime semantics: `synodoxics/noemar-substrate.md`.

## §2. Topology

The synart is a **tree of entarts plus universal Spaces**. Each Synomic Entity (Guardian, Generator, Prime, Halo) owns an **entart** rooted at one root Space.

### Six synome-root layers

| Layer | Representative Spaces |
|---|---|
| Constitutional | `&core.root`, `&core.telos`, `&core.skeleton`, `&core.governance`, `&core.protocol` |
| Framework | `&core.framework.risk`, `&core.framework.risk.forms`, `&core.framework.risk.scenarios`, `&core.framework.risk.concentration`, `&core.framework.distribution` |
| Registry | `&core.registry.entity`, `&core.registry.beacon`, `&core.registry.contract`, `&core.registry.exo-book` |
| Aggregation | `&core.settlement`, `&core.escalation` (note: `&core.endoscrapers` removed — endoscraper is a grounded runtime primitive; per-protocol metadata lives in `&core.protocol`) |
| Executable | `&core.syngate`, `&core.telgate`, `&core.loop.<class>`, `&core.recipe.*` |
| Library | `&core.library.runtime.<impl>`, `&core.library.telseed.<config>`, `&core.library.corpus.<domain>`, `&core.library.published.<topic>` |

### Four meta-patterns (prescriptive)

When proposing a universal Space, classify it: **framework** (universal shape + bounds, scatter-gathers to entarts), **registry** (flat identity index, push→pull onboarding), **aggregation** (collection at synserv), or **specification** (executable code, replicated to all). If none, push back.

### Naming convention

```
core-<kind>[-<topic>...]
entity-<entity-type>-<entity-id>-<sub-kind>[-<sub-id>]
```

Reserved keyword vocabulary is governance-paced. Names encode entity + sub-kind, *not* parent chain — registry atoms (`(sub-entart …)`, `(sub-space …)`) hold structural relationships, so a Space can move parents without renaming.

### Artifact tiers (full treatment in `synodoxics/noemar-substrate.md`)

| Tier | Replication | Privacy |
|---|---|---|
| **synart** | synserv → all participants | public |
| **entart** | inherits synart | scoped via auth |
| **telart** | within own emb fleet | private to that tel |
| **embart** | local only | private to that emb |

Authority gradient: synart > telart > embart. Crystallization promotes telart → synart; tel-internal review promotes embart → telart.

### Asymmetry rule, sharding, externals

Parent → child OK; child → parent and peer → peer avoided. Cross-sibling logic lives at common ancestor. **Policies cascade with monotonic tightening** (Halo can be stricter than parent Prime, never looser). Four sharding axes: authority / tenant / temperature / cadence. **Only Synomic Entities own entarts** — beacons are connective tissue (pubkey/class/loop pointer in registry, cert in certifier's entart, auth in entart owning the verb's target). Operators (companies, teleonomes, humans) are external.

## §3. Two-step rule and two-step loop patterns

Canonical synlang forms for portable cross-Space code.

### Two-step rule

A **portable local rule** uses `&self`; a **global declaration** specifies target set + local rule + combinator.

```metta
(= (book-exposure-here)
   (sum (collapse (match &self (unit $u) (unit-risk-weight $u)))))

(global-rule prime-exposure
   (targets via-registry sub-entart)
   (local-rule book-exposure-here)
   (combine sum))
```

Aggregator classes: trivial (sum/max/min/count), concat (top-K, list), sketch (t-digest, HLL — never for safety-critical math).

### Two-step loop

| Level | Where | Role |
|---|---|---|
| Universal template | `&core.loop.<class>` | portable loop body using `&self` |
| Per-entity instance | `&entity.<type>.<id>.<sub-kind>` | bindings (entity-bound-to, strategy-id, current-interval, import-loop) |

Booting against a per-entity Space evaluates the template body in that context. Same code, different bindings; verifier embs running the same Space derive the same expected behavior.

## §4. Runtime — auth, gate, heartbeat

**Two authorization domains** kept separate: Synome (atoms) and Chain (BEAM holdership in PAU stack). A GovOps team holds at least two credentials; a verifier emb reconciles. Synlang lives entirely in the Synome domain.

### Standardized vocabulary (deliberate tightening)

- **Governance accord** — synent ↔ synent mutual structural recognition.
- **Admin certification** — synent → beacon: "I carry liability."
- **Admin authorization** — certifier → beacon → scope: "may do verb V on target T."

"Accordant" reserved for governance accords; older docs' "GovOps becomes accordant to a PAU" usage moves under admin authorization.

### Three-level interaction model

- **Root** (Core Council on Guardian token-holder vote) — rare, governance-paced.
- **Cert** (any beacon with cert authority in tree) — operational.
- **Auth** (any certifier or delegate) — frequent, per-target scoped.

Underwriting frame: liability funnels up; blast radius bounded by auth.

### Synlang-native role definitions

Roles are first-class atoms (`role-def`, `role-grant`); kernel is ~10 atoms + one rule (`(can $principal $verb $target)`). **Genesis seed:** Core Council holds `root-authority` in `&core.governance` with verbs `define-role`/`grant-role`/`revoke-role`/`create-guardian`/`set-root`/`cert-beacon`/`auth-beacon`/`revoke-*`. Bootstrap: Core Council creates Ozone (single operational Guardian); on token-holder vote `set-root`s GovOps roots under Ozone (one per administered entity); GovOps roots cert + auth their operational beacons. Generator (USGE) is created accordant to Ozone, not as a separate Guardian.

### The gate primitive

Native-code grounded atom at network ingress. Per submission: parse → pubkey lookup → ed25519 verify (~50μs) → nonce dedup → rate-limit → route. Symmetric `gate-in`/`gate-out`. **Cross-Space ≠ trust boundary**: within one Synome runtime, cross-Space writes are direct `(add-atom &other-space …)`. The gate is for trust boundaries (external beacon → Synome, federation), not Space boundaries. Per-Space queues with single gate (routing-as-data via `(verb-target-space $verb $space)`).

### Heartbeat and dispatch

Synserv's `(run-forever)` lives in synlang; off-space is only the wall-clock metronome (grounded `delay`). Pause is `(halt-heartbeat)` atom write. **Open verb dispatch via whitelist**: `(external-verb $v (target-arg N))` atoms gate what's externally callable; one generic dispatch rule evaluates after sig + auth + whitelist.

### Full ingress pipeline — gate → policy → effect → audit

Sections 9 + 11 of `runtime.md` together describe one pipeline: gate-in (ed25519/dedup/rate-limit) → parse payload → whitelist check → **permits query** → dispatch effect → audit row. **Authority lives only in the permits step.** Crypto below it filters spam/replay; whitelist above it filters surface-area; effect below it does mechanical work; audit logs everything. None of those steps make policy decisions. Concentrating authority at one inspectable point is what makes the trust boundary auditable. Default-deny by absence: no `auth` atom → permits returns False → policy denies.

**Permission rule canonical successor (auth-only).** New code uses `(if (auth $beacon $verb $target) True False)` — flat 3-arg `auth` fact, lives in target-owning entart, granted by certifier rooted in genesis, removed on revocation. Trades roles/scope-shapes/conditions (the older `(can $principal $verb $target)` form) for a one-line audit answer to "can X do Y to Z." Legacy `govops_demo` preamble pattern (`in-class` + `beacon-role` + `beacon-status`) survives in older code; auth-only is canonical going forward.

**Failure / escalation modes** (4 named): beacon drops events (`event-gap-flagged` via on-chain comparison) / settlement disagrees with chain (flag into `&core.escalation`) / agent under-pays for resources (meter detects, escalation flag) / beacon misbehavior (cert/auth chain recourse — revoke `auth` atom, re-cert from above, ultimately legal liability up the chain). All flagging atoms append-only; pruned at next settlement unless promoted to settlement-tier or out-of-band archive.

### Space kinds — orthogonal to tier

Three Space kinds, orthogonal to the artifact tier (synart/telart/embart): **Beacon Spaces** (synart only — regulated comms apertures: gates, beacon loops, recipes), **Agent Spaces** (telart-proven / embart-speculative; never synart — agency is private by design; the seat of NN-in-the-loop pattern matching, RSI, risk reasoning), **Data Spaces** (all tiers — inert pattern-match environments). The agart is where Agent Spaces live with their supporting Data Spaces; Beacon Spaces sit in synart and consume from agarts via convention-named embart Space contracts.

### What multi-Space architecture actually buys

| Real wins | Not real wins |
|---|---|
| Replication topology granularity (per-entart subscription) | Raw query perf (indexes do that) |
| Lifecycle isolation (archive closed entities) | Trust separation within one runtime (cross-Space ≠ trust boundary) |
| Mobility / repartitioning unit | Failure isolation (operational discipline does this) |
| Fork-promote / staging (RSI, mesh) | Most "scaling" claims |
| Independent runtime versioning, conceptual/authority alignment, executable specs co-located with state | |

Each new Space proposal should answer: which left-column win does it deliver? If "none" — push back.

## §5. Identity-driven boot, shadow execution, hot-swap

**Canonical home:** `boot-model.md`. Concrete synserv shape: `runtime.md` §10.

```
noemar boot --identity=X --key=path/key.pem --synart=endpoint
   ↓ mount synart → look up X in &core.registry.beacon
   ↓ resolve loop pointer → evaluate (run-forever) with that Space as &self
```

Boot procedure is itself synart content (`&core.boot`). Off-synart inputs are minimal: identity, private key file, synart endpoint, optional sync policy.

**Shadow execution:** any embodiment can locally evaluate any loop. What changes is **which writes count canonical** — auth atoms decide. Uses: verifier embs (re-derive + flag disagreement to `&core.escalation`), cross-warden formations, sandbox/dry-run testing. **Failover is an atom write**.

**Hot-swap modes:** **A** — tail-recursion picks up (additive changes). **B** — atomic restart with `(halt-heartbeat)` (breaking changes; brief pause). **C** — double-mesh / shadow synserv (synserv loop, gate semantics, auth model; parallel grid + cut over at boundary).

**Failure modes:** identity revocation mid-loop; loop atom retraction; runtime crash (recovery from last flush); partial-sync (rule refuses to evaluate; pre-check at boot).

**Grounded fast-path:** ed25519, atomspace match, network I/O can't be synlang for performance. Pattern: spec in synart (truth) + native impl + conformance test atoms + verifier checks they agree.

## §6. The call-out primitive

The **only sanctioned mechanism** for synart-resolved code to consult local cognition. Direct telart access from synart loops is forbidden.

```metta
(call-out $service
   (inputs <input-atoms…>)
   (output-shape <expected-shape>))
```

Runtime resolves `$service` against the booting identity's telart call-out registry → marshals inputs → local service responds (typically external API) → response shape-validated → returned to surrounding synart code.

**Verifiability:** inputs verifiable (synart-derived); output not (LLM/cognition); output-shape conformance verifiable; what strategy does with output verifiable. **Properties:** service is a synart-known name (governance-paced catalog); output shape declared; provenance recorded; bounded latency; idempotent in synart effect. Different tels use different LLM providers/models at the same call-out point.

## §7. Sentinel formations as beacons-with-call-outs

Sentinels are **beacons whose strategy includes designated call-outs**.

| Formation | Synart share | Call-out share | Audit story |
|---|---|---|---|
| **Baseline** | ~95% | ~5% (ranking choice) | almost everything verifiable |
| **Stream** | ~10% (boundary check + comm) | ~90% (the proposal) | bounds verifiable; proposal is local cognition |
| **Warden** | ~95% | ~5% (own LLM at same call-out site) | re-runs Baseline; halts on divergence past tolerance |

Inter-formation communication via synart channels (`gate-out (emit-to-baseline …)`, `gate-out (halt-baseline …)`); no out-of-band.

**TTS bound** = Warden tick interval + call-out latency + halt propagation. ORC = Rate Limit × TTS. **Expected disagreement among Wardens** (each runs its own LLM) is normal; threshold tuning per recipe is governance's responsibility. Architecture is continuous: pure-spec deterministic beacons at one end, mostly-cognitive Streams at the other.

## §8. Beacons (two-role taxonomy) and in-space calculation

After moving calculation into synart-resolved code that synserv runs, beacons become pure I/O.

**Input beacons** (push data atoms into book Spaces):
- **Endoscraper** — on-chain protocol state; deterministic, verifiable by re-scraping
- **Oracle** — off-chain market data; provider trust + redundancy/dispute
- **Attestor** — off-chain claims (custody, contract terms, compliance); signed claims with attestor liability via slashing

**Action beacons** (emit chain txs from synart state):
- **`relay`** — narrow per-target, deterministic (relayers + executors collapsed into this single class)
- **`sentinel`** — call-out density into operator telart (variants: `stream`, `principal`) (Phase 9-10+)
- **Sentinel formation** — operating-setup bundle pairing `baseline-{prime}` (relay) + `warden-{prime}-{op}` (relay) + `stream-{prime}-{actor}` (sentinel) (Phase 9-10+)

Old → new: `lpla-checker` disappears; `lpla-verify` → verifier emb; `lpha-relay` → `relay-{x}` (relay class); `lpha-nfat`/`-lcts`/`-council` → `nfat-{halo}`/`lcts-{x}`/`council-{x}` (relay class, executors); `lpha-halo` → chain-read primitive (chain reads) or `attest-data-{class}` (attestations); `stl-base-{prime}` → `baseline-{prime}` (relay); `stl-warden-{prime}-{op}` → `warden-{prime}-{op}` (relay); `stl-stream-{prime}-{actor}` → `stream-{prime}-{actor}` (sentinel). The LPLA/LPHA/HPLA/HPHA matrix (`macrosynomics/beacon-framework.md`) is **orthogonal**: matrix = authority profile, two-role = work shape.

**In-space calculation** (mechanism deferred to Phase 1): synserv runs synart-resolved calculation that keeps each book's derived state (equity, CRR, matching, breach flags, ER) consistent with current input atoms. Three consequences: full verifiability (wardens re-derive), beacons stay pure I/O, no lag.

**Endoscraper vs exoscraper:** the `(chain-read $contract $slot)` runtime primitive (in scope; replaces the retired endoscraper beacon class) reads internal protocol contract state on public blockchains directly from any rule in any Space; verifier embs independently re-evaluate rules over chain reads, with reconciliation atoms triggering escalation on disagreement. Exoscrapers (deferred): external APIs / proprietary feeds delivered through `market-data-beacon` / `attest-data-beacon` channels; insurance + governance review needed.

## §9. Risk-framework synlang shapes; worked examples

`risk-framework.md` is the synlang complement to `risk-framework/` (canonical conceptual home). Atom shapes for Primebook / Halobook / Riskbook / Exobook (book-type, book-category, parent-*, sub-*, holds, issues, book-frame). Risk forms live in `&core.framework.risk.forms` at three levels (exo-asset / exobook / riskbook) declaring variables, M2M and HTM equations, resolution-tier, optional composition-constraints. Stress scenarios in `&core.framework.risk.scenarios`; simulation maps loss-fn over scenarios and combines (`take-worst`, `probability-weighted-mean`).

**Four-tier resolution**: math → simulation → heuristic → max-risk. Heuristic tier applies depth/cycle/repeat penalties. Tier 4 returns full notional ⇒ CRR 100%. **Default-deny CRR 100%** triggers in three places: Riskbook without matching risk form, Exobook beyond max recursion depth, Exobook without matching risk form. Composition constraints are synlang predicates over Riskbook contents (multiple matches = governance-priority risk-form-design error). Patterns also cover **rule-bearing tranches** (callable, step-up, triggered subordination) and **projection-model declarations** (Black-Scholes, Monte Carlo, lattice, parametric credit) with `(model-uncertainty-haircut …)`.

**`settlement-cycle-example.md`** walks one Spark Prime cycle demonstrating: entart subtree seed state, **uniform permission rule template** `(if (auth $beacon $verb $target) True False)`, local-by-default risk-weight rule, **ER as derived rule (not stored)** via scatter-gather, real-time event samples, two-phase settlement closure (per-Prime → mirror to `&core.settlement`). §3.5 shows the content-based CRR version: lifecycle phases (filling/deploying/at-rest) become *different exo units pointing to different exo books with different risk forms*, not state attributes on a single unit.

**`telseed-bootstrap-example.md`** traces "Mira's research tel" first 24 hours: t=0 boot, t=2min sync (~600MB compressed), t=5min telart instantiation, t=10min identity registration via syngate with sponsor vouching cert, t=30min second emb spawn + telart inter-emb replication, t=4h first verifier carry, t=24h steady state. Demonstrates: telseed minimalism, identity-driven boot uniformly across embs, three-tier replication, two-step loop pattern, recipe marketplace economics.

## §10. Scaling — synserv, replication, partitions

Three flow paths: beacon write (beacons → gate → synserv → atomspace), replication (synserv → subscribers), scatter-gather (synserv ⇄ entart Spaces).

**Risk classes:**

1. **Synserv as single sequencer** — bottleneck/SPOF. Phase 1 single-leader + hot standby; consensus needed when settlements faster (Phase 2+) or events exceed ~10k/sec.
2. **Partial sync correctness** — *empty-match is the trap*; default must be **hard-fail**. Lazy-fetch is opt-in. Every rule declares `(rule-reads $rule $space)`.
3. **Rule propagation skew** — version mismatches during in-flight scatter-gather. Synserv stamps eval with target version. Same discipline applies to call-out propagation across Wardens.
4. **Hot-spotting** — `&core.skeleton`, `&core.framework.*`, `&core.registry.*` are Zipfian hubs. Mitigation: hub replication, aggressive caching, partial sync for non-universal Spaces.
5. **Storage growth** — temperature axis becomes physical. Compaction: ER-samples → epoch summaries; audit history → per-day rollups; closed books → snapshot.
6. **Network partitions** — beacon ↔ synserv (queue locally, replay; cap queue size); subscriber ↔ synserv (resume from last-ack); replicas split (consensus / deterministic election).
7. **Trust model fragility** — operational beacon → its auth ceiling; Guardian root cert → whole subtree; synserv → total compromise; replication channel → subscribers see corrupted view but synserv truth still good.

**Telart spread** is a separate channel within one tel's emb fleet (telgate instances, not syngate). Distinct authority + bandwidth budget.

**Goertzel hardware locality:** PIM grid of cubes; intra-cube fast, inter-cube slow; **repartitioning requires freezing the grid** (double-mesh). Hub replication is natural for cert/auth/pubkey. Slowly-changing append-only graphs are the sweet spot. Migration tolerance: cognitive (μs–ms, fatal) → operational → settlement → governance → constitutional.

## §11. Phase 1 commitments and migration principles

**Thirteen Phase 1 commitments** — design hygiene that incidentally makes scaling free.

Original seven (`runtime.md` §17): (1) Space always a parameter; (2) append-only writes; (3) content-addressed names; (4) open verb dispatch via whitelist; (5) gate as real primitive at trust boundary; (6) `(can …)` reads from a named auth Space; (7) idempotent constructors.

Added by structural design (`topology.md` §19): (8) every rule declares its reads; (9) cross-Space refs go through registries; (10) cross-Space rules are scatter-gather; (11) global rules carry publication metadata; (12) synart is a tree of entarts (parent → child only; only synents own entarts).

Added by self-hosting: (13) loops, gates, recipes are first-class synart content.

**16 migration principles (P1–P16):** Locality (Space is unit; most ops single-Space; co-locate edges with dominant access). Naming (logical names; content-addressing; routing-as-data). Causality (append-only; idempotent; no global ordering). Visibility (cross-Space deps explicit; provenance first-class). Migration (partition layout foundational but not eternal; per-Space runtime version; split/merge without breaking refs; major restructuring uses fork-promote).

---

## Key vocabulary

| Term | Meaning |
|---|---|
| synent | Synomic Entity — owns an entart (Guardian, Generator, Prime, Halo, Folio) |
| entart | A synent's subtree of synart, rooted at one root Space |
| synart / telart / embart | Replication tiers — public / per-tel / per-emb |
| synserv | Canonical instance running the synome; sole sequencer of synart writes |
| Noemar | One implementation of the synlang atomspace runtime contract |
| synlang | The language — S-expressions grounded in the synomic library |
| gate | Trust-boundary primitive (`gate-in`/`gate-out`) at network ingress |
| call-out | `(call-out $service (inputs …) (output-shape …))` — only synart→telart bridge |
| two-step rule | Portable local rule using `&self` + global declaration with target set + combinator |
| two-step loop | Universal template in `&core.loop.<class>` + per-entity instance in `&entity.…` |
| shadow execution | Any emb runs any loop locally; auth atoms decide canonical writes |
| scatter-gather | Cross-Space rule: ship local rule to targets, run against `&self`, aggregate |
| hub atom | Small, ubiquitously-read atom replicated to every cube/node |
| role-def / role-grant | First-class atoms defining a role's verbs/scope-shape and instantiating it |
| endoscraper | (Retired beacon class) replaced by `(chain-read $contract $slot)` grounded runtime primitive accessible from any rule |
| exoscraper | (Deferred) External-API scraper with insurance overhead; future `market-data-beacon` / `attest-data-beacon` channel |
| `attest-data-beacon` | Input beacon class for off-chain claim attestation with slashing liability (replaces retired `attestor`) |
| double-mesh | Two-grid migration: live + shadow; swap at boundary |
| `&core.boot` | Synart's own bootloader; runtimes start knowing only how to read this Space |

## Cross-references

- `noemar-synlang/topology.md` §8 — five levels of self-reference (canonical home)
- `synodoxics/noemar-substrate.md` — artifact tiers full treatment
- `synoteleonomics/recipe-marketplace.md` — recipe marketplace canonical home
- `macrosynomics/beacon-framework.md` — LPLA/LPHA/HPLA/HPHA authority matrix
- `macrosynomics/topology-layers.md` — population/probmesh meta-layering
- `risk-framework/` — risk framework conceptual home
- `roadmap/phase-1-spaces.md` — Phase 1 reality
- `accounting/settlement-cycle.md` — five-step closure heartbeat
- `accounting/entity-fees.md` — Entity Upkeep (50 bps/yr) and fee structure
- `trading/` — Sentinel formation conceptual spec

## File map

| File | What's in it the summary doesn't have |
|---|---|
| `synlang.md` | Resolved/open table for language design questions |
| `topology.md` | All 21 sections: Hyperon-Spaces basics; full per-Space contents tables; full Ozone entart family example; registry pattern atom shapes; full two-step rule + loop code with worked Sentinel-Baseline; pattern-families-to-build matrix |
| `runtime.md` | ACL/RBAC/capability framing; three-level interaction asymmetry; full `(can …)` rule details; per-Space-queue routing diagram; 16 migration principles with rationale; full bootstrap sequence with metta; kernel implementation order |
| `boot-model.md` | Boot CLI with all flags; bootstrap-procedure-as-Space metta (`&core.boot`); identity→role lookup with registry rows; auth-bounded canonicality metta; hot-swap mode taxonomy mapping; per-failure-kind handling |
| `synlang-patterns.md` | Platonic-kernel framings; cross-book duality metta; full four-constructor MeTTa surface (Halo/Class/Book/Unit); Sentinel decision rule with RAR + worked arithmetic; full Baseline/Stream/Warden code; tranche-rule and projection-model patterns (BS, Monte Carlo, lattice, parametric credit) |
| `scaling.md` | All 15 sections: networked-architecture diagram; beacon throughput arithmetic (~75μs/op); replication-staleness profile; partial-sync semantics table; full rule-propagation CDC; storage tiering + compaction; partition matrix; Goertzel temporal calibration; aggregator pitfalls; trust blast-radius; testing strategy; open questions a–k |
| `risk-framework.md` | Synlang-flavored complement (Trimmed, Phase 5). Full atom shapes for all four book types; three risk-form bodies with examples; default-deny in all three locations; stress-scenario param vectors; four-tier resolution code; loop-and-recursion with cycle detection; five worked examples with arithmetic (pure-ETH, Morpho recursion, ABF+CDS, multi-Riskbook, looped exposure) |
| `settlement-cycle-example.md` | Worked end-to-end settlement cycle (updated to content-based CRR framing). Full seed state metta; permission rule template; ER scatter-gather metta; deployment timeline arithmetic (t₀ ER 0.20 → t₂ 0.95 breach); penalty arithmetic; §3.5 content-based CRR version |
| `telseed-bootstrap-example.md` | Mira endowment table; full Space enumeration; sync byte sizes; t=5min telart instantiation metta; t=10min vouching cert; t=4h first verifier carry; t=24h steady state |
| `beacons.md` | Full old → new mapping table; open Phase 1 questions on classes / oracle vs attestor / authority scope / verifier-emb collapse |
| `listener-loops.md` | Data-flow diagram; comparison table (heartbeat / in-space calc / beacon); open questions on mechanism choice |
