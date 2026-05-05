# Scaling — Networked Synart, Failure Modes, and Testing

Operational concerns when turning the topology defined in `topology.md`
into a real networked system: synserv as the canonical sequencer,
beacons writing through gates, replication to subscribers, partial sync,
rule propagation across the wire, hot-spotting on universal Spaces,
storage growth, network partitions, and what needs to be tested before
this goes live.

The structural decisions in `topology.md` are sound on paper. This
document is about the operational reality of running them on real
machines, real networks, and real adversaries.

---

## TL;DR — what breaks and what to test

**The networked architecture has three flow paths**, each with distinct
failure modes:

```
1. Beacon write path:    beacons → gate → synserv → atomspace
2. Replication path:     synserv → subscribers (full or partial)
3. Scatter-gather path:  synserv ⇄ entart Spaces (project rules + collect results)
```

**The dominant risk classes:**

1. **Synserv as single sequencer** — bottleneck, SPOF, replication-lag source.
2. **Partial sync correctness** — rules with unsatisfied reads must hard-fail, never silently underestimate.
3. **Rule propagation skew** — version mismatches during in-flight scatter-gather.
4. **Hot-spotting on universal Spaces** — `&core-*` read by everyone; framework projections fan out to many entarts.
5. **Storage growth** — synart accumulates; needs tiering and compaction discipline.
6. **Network partitions** — beacons cut off can't write; subscribers cut off run stale.
7. **Trust-model fragility** — beacon key compromise, synserv compromise, replication-channel compromise have different blast radii.

**The testing imperatives:**

- Chaos: synserv crash, partition, replication delay
- Load: beacon write throughput, gate sig-verification, scatter-gather fan-out
- Correctness: every rule's `rule-reads` must be enumerable; partial-sync hard-fail; rule-update during in-flight aggregation
- Long-running: consistency drift over weeks; storage growth profile
- Migration: per-tier repartitioning at settlement boundaries

---

## Section map

| § | Topic | Core idea |
|---|---|---|
| 1 | Networked architecture | Three flow paths; synserv at the center |
| 2 | Synserv as canonical sequencer | Single-writer model; SPOF; consensus options |
| 3 | Beacon write throughput | Gate ingress; concurrent submissions; sig cost |
| 4 | Replication and staleness | Eventual consistency; staleness bounds; versioning |
| 5 | Partial sync correctness | The dangerous case; declarative reads |
| 6 | Rule propagation correctness | Publication as CDC; version skew; transitive deps |
| 7 | Hot-spotting on universal Spaces | Hub replication; caching; tiering |
| 8 | Storage growth and tiering | Hot/warm/cold; compaction; pruning |
| 9 | Network partitions | Beacons cut off; subscribers cut off; reconvergence |
| 10 | Migration and repartitioning | Goertzel locality; settlement-paced migrations |
| 11 | Aggregator robustness | Order-dependence; sketch merge errors |
| 12 | Trust model fragility | Compromise classes and blast radii |
| 13 | Testing strategy | Unit / integration / chaos / load / long-running / migration |
| 14 | Open scaling questions | Things we'll need answers to before scale matters |
| 15 | One-line summary | The whole concern set compressed |

---

## 1. The networked architecture

Once distributed, the synome has three flow paths:

```
                                   external operators
                                         │
                                         │ run
                                         ▼
                                       beacons
                                         │
                                         │ signed submissions
                                         ▼
                                  ┌─────────────┐
                                  │    GATE     │  sig verification, rate limits, nonce
                                  └──────┬──────┘
                                         │ verified messages
                                         ▼
                                  ┌─────────────┐
                                  │   SYNSERV   │  sole sequencer, ordered writes
                                  └──────┬──────┘
                                         │
                ┌────────────────────────┼────────────────────────┐
                │                        │                        │
                ▼                        ▼                        ▼
         atomspace writes        rule projections        replication stream
                │                        │                        │
                ▼                        ▼                        ▼
         entart Spaces        scatter-gather targets        subscribers
                                                            (full and partial)
```

Synserv is the center of gravity for **synart replication**. Every
concern about synart replication below is, in one form or another,
about synserv being the single sequencer that the whole system funnels
through.

### Telart spread — a separate channel

There's also a **second replication channel**: telart spread within a
single teleonome's emb fleet. When a tel runs multiple embs (for
resilience per `syn-tel-emb.md` §7), its telart contents must replicate
across them. This channel is:

| Property | Synart replication | Telart spread |
|---|---|---|
| Direction | synserv → all participants | one tel's authoritative emb → that tel's other embs |
| Authority | governance-controlled | per-tel internal |
| Bandwidth budget | global, governance-set | per-tel, paid by that tel |
| Visibility | public | private to the tel |
| Trust profile | gate-mediated | tel's own pubkey ring |

A tel running 3-5 embs has roughly tel-internal-fanout × telart-update-
rate of bandwidth obligation on its private channel. This is separate
from the bandwidth this tel pays for synart replication-out (per the
pricing in `syn-overview.md` §19).

The two channels can use the same physical network but have distinct
authority models. Tel-internal traffic doesn't go through syngate; it
goes through telgates (each tel's own gate instance, running the
universal `&core-telgate` spec).

---

## 2. Synserv as the canonical sequencer

Synserv runs the gate, runs constructors, writes to atomspace,
projects rule updates to entart targets, aggregates settlement, and
pushes replication. It's the single source of truth for write order.

### What this gives us

- **Linear write order** — no conflict resolution needed; the synserv's
  log is the canonical history.
- **Atomic constructors** — a constructor that writes to multiple Spaces
  (e.g., auth grant in `&entity-prime-spark-root` + capability fact in
  `&entity-halo-spark-term-book-usds`) is atomic because synserv is the
  sole writer.
- **Single point for sig verification, rate limits, and audit.**

### What can go wrong

| Failure | Effect | Mitigation |
|---|---|---|
| Synserv crashes | Whole synome stops accepting writes | Hot standby, leader election |
| Synserv slow | Beacons back up at the gate; settlements miss SLO | Horizontal scaling of read replicas (writes still single-leader); aggressive batching |
| Synserv partitioned | Half the network can't write | Single-writer model — partition resolution must be deterministic |
| Synserv compromised | Total system compromise (sig'ed canonical history corrupted) | Replication consensus with multiple validators; cryptographic commits |

### Phase 1: single-leader is fine

For Phase 1 with monthly settlement and modest beacon throughput, a
single synserv instance with a hot standby is enough. The constraint
that pushes toward consensus is *settlement frequency* and *cross-Prime
coordination volume* — once those grow (Phase 2+ daily settlement,
factory stack), single-leader becomes a real bottleneck.

### What needs validation

- **Failover time** under realistic load. Hot standby with crash-recover
  from atomspace flush. SLO: < 30 seconds for Phase 1.
- **Determinism** of synserv's write log. Same input, same output, same
  hash — required for any future consensus story.
- **Backpressure** from gate to beacons when synserv is slow. Beacons
  must retry-with-backoff, not flood the gate.

---

## 3. Beacon write throughput

The gate is the trust boundary. Every external write passes through it
for sig verification, nonce check, rate limit, and routing.

### The cost profile

For a single submission:

- ed25519 verify: ~50μs on commodity hardware
- Nonce dedup against recent window: ~10μs (in-memory hash)
- Rate-limit token check: ~5μs
- Routing decision (`(verb-target-space …)` lookup): ~10μs
- Total: ~75μs hot-path → ~13k submissions/sec single-threaded

For a 100-Prime / 1000-Halo system at 2-second event cadence
(`er-sample` from each Halo every 2 sec): ~500 events/sec. Well within
budget single-threaded.

For settlement spikes (every Halo flushes at epoch close): up to 1000
submissions in a few seconds. Still within single-thread budget; multi-
core scales linearly because sig verification is embarrassingly parallel.

### What can go wrong

- **Spam:** beacon spamming until rate-limit kicks in costs sig
  verification cycles. Mitigation: per-pubkey rate limit *before* sig
  check (cheap pubkey lookup; reject if rate exceeded; only then verify).
- **Burst at epoch close:** thundering herd of settlement submissions.
  Mitigation: jittered close times; gate-level batching.
- **Sig spam from unknown pubkeys:** attacker submits with random
  pubkeys to force gate lookups. Mitigation: pubkey lookup is O(1) hash;
  unknown-pubkey sigs drop without verification.

### What needs validation

- **Load test the gate** at 10x expected sustained rate, 100x burst.
- **Verify rate limits** hold under DDoS-shaped load.
- **Verify nonce dedup** works across synserv restart (nonces persist
  through some recent window).

---

## 4. Replication and staleness

Subscribers (teleonomes, embodiments, light bots) replicate from
synserv. Replication is **eventually consistent** — subscribers always
trail the canonical history by some delay.

### Staleness profile

| Subscriber type | Acceptable staleness | Mechanism |
|---|---|---|
| Pure governance auditor | minutes | poll-based, low frequency |
| Settlement aggregator | seconds | push subscription, near-realtime |
| Risk monitor | sub-second on critical Spaces | streaming subscription |
| Light embodiment (USDS-only bot) | seconds-minutes for its slice | per-Space subscription |

### What can go wrong

- **Replication lag** during high write volume. Subscribers see stale
  ER, may make stale decisions. Mitigation: subscribers stamp queries
  with a freshness token; refuse to act if behind threshold.
- **Subscriber falls catastrophically behind** (network slow, machine
  slow). Mitigation: subscriber resumes from last-acked atom; synserv
  can serve historical chunks.
- **Subscriber forks** (somehow gets a divergent view). Mitigation:
  every replicated batch is hash-chained; subscriber detects mismatch
  and triggers full re-sync.

### What needs validation

- **Worst-case replication lag** under sustained write load.
- **Hash chain integrity** end-to-end.
- **Resume from last-ack** correctness after subscriber crash.
- **Full re-sync** time for a fresh subscriber as synart grows.

---

## 5. Partial sync correctness

Rules and data co-locate (per `topology.md` §15-16): if you don't sync
a Space, you don't get its rules. The common case is clean — partial
sync gives partial *capabilities*, missing capabilities just aren't
there to call.

### The dangerous case

You have a rule but not all the Spaces it reaches into. Concretely:
sync `&entity-prime-spark-root` (for policy) but skip
`&entity-halo-spark-trade-root`. Now `prime-exposure` walks the registry
and tries to match against an unbound Space.

| Semantic | Behavior | Use when |
|---|---|---|
| **Hard fail** | throws; rule refuses to answer | safety-critical (covenant checks) |
| **Lazy fetch** | runtime pulls missing Space from canonical synart | DAS pattern; one-shot queries |
| **Empty match** | treats unbound as no atoms; silently underestimates | **never** — silent wrong answers |

Empty-match is the trap. Default must be hard-fail; lazy-fetch is opt-in.

### Declarative reads — capability introspection

Every rule declares its reads:

```metta
(rule-reads prime-exposure &entity-prime-spark-root)
(rule-reads prime-exposure &core-skeleton)
(rule-reads prime-exposure via-registry sub-entart)

(= (can-evaluate $rule)
   (forall $s (rule-reads $rule $s) (have-synced $s)))
```

The runtime refuses to evaluate a rule whose reads aren't satisfied.

### What needs validation

- **Every projected rule** has correct `rule-reads` declarations
  (lint at publish time).
- **Hard-fail by default** — fuzz a partial-sync teleonome by running
  rules with random Space-omissions; verify it never silently produces
  a result.
- **Lazy fetch opt-in** behavior tested: one-shot fetch happens, result
  is correct, fetch is logged.

---

## 6. Rule propagation correctness

When a global rule's master version updates, synserv projects it out
to every target Space via the same replication channel as data writes.
This is **publish-subscribe via CDC**.

### The mechanism

```metta
;; master in &entity-prime-spark-root
(global-rule book-exposure-here
   (version 7)
   (targets via-registry sub-entart)
   (rule-deps unit-risk-weight crr-of)
   (space-reads &self &core-skeleton))

(= (book-exposure-here) <body-v7>)
(rule-version book-exposure-here 7)
```

On v7→v8:

1. Synserv writes new body + version atoms in master, retracts old.
2. Walks the registry → list of target Spaces.
3. For each target: retracts old projection, adds new projection plus
   provenance: `(rule-source book-exposure-here &entity-prime-spark-root)`.
4. Replication carries new atoms to subscribers.

### What can go wrong

**Version skew during scatter-gather.** `eval-global` runs across five
books while v7→v8 rollout is in flight; three may run v7 and two run v8.
For sum-shaped aggregations rarely matters; for safety-critical paths
(covenant pre-flights), synserv stamps the eval with a target version
and any target running an older copy refuses or upgrades first.

**Transitive dependency closure.** If `book-exposure-here` calls
`unit-risk-weight`, both must ship together. Publication step closes
over rule deps and projects the package. The runner refuses to project
unless every dep is itself either projected or universally replicated.

**Retraction cascade.** Retracting a master must cascade to every
projection. If a projection is reached by a rule before retraction
propagates, the rule may run with stale code.

### What needs validation

- **Rule update during in-flight aggregation:** trigger v7→v8 mid-eval,
  verify either (a) all targets ran v7 or (b) all ran v8 — never mixed
  for safety-critical rules.
- **Transitive closure:** publish a rule whose dep isn't universally
  replicated → publication should refuse.
- **Retraction propagation:** retract master, verify every projection
  retracted before any reader can touch them.

### Call-out propagation across wardens

The same rule-propagation discipline applies to loops that contain
call-outs (`(call-out $service ...)` per `synlang-patterns.md` §5).
When a Sentinel-Baseline strategy is updated, every Warden running
the same strategy must also pick up the update — they re-derive
against the same code with their own LLM call-outs.

Mixed-version Wardens are particularly dangerous: an old-version
Warden checking against new-version Baseline outputs will see false
disagreement and may halt a healthy Baseline. Mitigation: per-formation
loops project synchronously, with version atoms that Wardens check
against Baseline before halting.

Also: **expected disagreement** between Wardens (because each has its
own LLM at the same call-out site) is normal. Threshold tuning per
recipe is governance's responsibility — too tight and false halts
fire; too loose and rogue Baselines escape detection. This tuning is
itself a recipe parameter, not a fixed constant.

---

## 7. Hot-spotting on universal Spaces

The four-layer factoring puts a lot of read traffic on a small number
of universal Spaces:

- `&core-skeleton` — read on every rule that touches CRR, ER formulas, etc.
- `&core-framework-*` — read whenever a framework parameter is consulted
- `&core-registry-*` — read whenever an entart, beacon, or contract is looked up
- `&core-root` — read whenever the synome tree is walked from the top

These are exactly the Zipfian hub-atoms that DAS handles via hub
replication. But replication has costs and bounds.

### Mitigations

- **Hub replication.** Every cube/node carries a copy of `&core-*`
  Spaces. Updates propagate to all replicas at governance pace
  (rare). Reads are always local.
- **Aggressive caching at subscribers.** `&core-skeleton` doesn't change
  except at constitutional rewrites; aggressive caching is safe.
- **Partial sync for non-universal-Spaces.** Light embodiments that
  only need their slice + skeleton don't pull the whole synart.

### What needs validation

- **Update propagation time** to all replicas of `&core-skeleton`
  during a rare constitutional change. Should be governance-tolerable
  (minutes, not hours).
- **Cache invalidation** on framework updates: every subscriber
  invalidates its cache when a framework's version atom changes.
- **Hot-spot resilience:** simulate every entart simultaneously
  reading `&core-framework-risk` during settlement; verify reads stay
  local.

---

## 8. Storage growth and tiering

The synart accumulates atoms over time. Some grow without bound by
default; others have natural retention boundaries.

### Growth profile

| Atom class | Retention | Volume profile |
|---|---|---|
| `&core-skeleton` | Permanent | small, bounded |
| `&core-framework-*` | Permanent | small, bounded |
| `&core-registry-*` | Permanent | linear in entities/beacons/contracts |
| Entart roots | Permanent | bounded per entity |
| Book leaf operational atoms | Bounded by lifecycle | big when active, prunable when book closes |
| ER samples | Two-epoch rolling | large during epoch, small after settlement |
| Settlement records | Permanent | linear in epochs, compactible |
| Audit history | Permanent | linear in submissions, compactible |

### Tiering

The temperature axis (axis C from `topology.md` §4) becomes a real
physical decision:

- **Hot:** active-epoch er-samples; current submission window
- **Warm:** last-settled epoch; recent audit history (within governance
  window, e.g., 90 days)
- **Cold:** older settlement records, audit history, closed-book leaves;
  archived to slower/cheaper storage

### Compaction

Append-only with structured compaction:
- ER-sample atoms after settlement: compact to `(epoch-max-er …)` and
  `(epoch-min-er …)` summary atoms; drop individual samples.
- Audit history: compact to per-day rollups beyond the warm window.
- Closed-book leaves: snapshot final state to cold; retain only the
  snapshot atom.

### What needs validation

- **Storage growth** projection over 1, 3, 10 years at projected event
  rates. If unbounded, find what's missing in compaction.
- **Compaction correctness:** never lose semantically important atoms
  (auth grants, governance decisions, settlement obligations).
- **Cold restoration:** how long to read a 5-year-old settlement record?
  SLO matters for disputes.

---

## 9. Network partitions

In a real network, partitions happen. The synome's response depends on
which side of the partition each role is on.

### Partition scenarios

| Scenario | Effect | Recovery |
|---|---|---|
| Beacon ↔ synserv | Beacon can't submit; queues writes locally | Reconnect, replay queued writes (nonce-protected); synserv accepts in order |
| Subscriber ↔ synserv | Subscriber falls behind; runs stale | Reconnect, resume from last-ack |
| Synserv replicas split | Both halves try to be leader | Consensus protocol decides; one half goes read-only |
| Cross-region replication delay | Distant subscribers more stale | Local-region read replicas |

### What can go wrong

- **Beacon's local queue grows unbounded** during long partitions.
  Mitigation: cap queue size; beacon refuses new operations when full.
- **Stale subscribers acting on stale state** — risk monitor sees ER
  pre-deployment, doesn't notice the breach for minutes. Mitigation:
  freshness tokens on safety-critical reads.
- **Split-brain at synserv replicas.** Mitigation: single-writer
  invariant must hold even under partition; deterministic election or
  fence-based protocol.

### What needs validation

- **Partition tolerance test:** kill the network between beacons and
  synserv for 5 minutes; verify clean reconvergence.
- **Subscriber catch-up time** after extended partition.
- **Split-brain prevention:** force a synserv-replica partition; verify
  no double-leader.

---

## 10. Migration and repartitioning

From `synart-access-and-runtime.md` §15: Goertzel hardware locality is
physics; repartitioning requires freezing the grid; the sweet spot is
slowly-changing graphs. Repartitioning at *cognitive* timescales is
fatal; at *governance* timescales it's a scheduled migration.

### When repartitioning happens

| Scale | Trigger | Tolerance |
|---|---|---|
| Cognitive (μs–ms) | Cross-cube query routing | Cannot freeze; double-mesh |
| Operational (sec–min) | Hot Space splitting | Tolerate seconds |
| Settlement (hours–days) | Per-Prime / per-Halo rebalance | Tolerate maintenance windows |
| Governance (days–months) | New Space layouts | Hours of downtime fine |
| Constitutional (years) | Whole-synome reorganization | Multi-day reorganizations fine |

### The double-mesh trick

For settlement-paced repartitioning of large operational Spaces:

1. Stand up new layout on shadow grid.
2. Copy current state from live to shadow at last settlement boundary.
3. Replay any post-settlement writes from live to shadow.
4. At next settlement, freeze briefly, switch reads to shadow.
5. Decommission old layout.

Only works because the synart is append-only and content-addressed —
copying preserves identity.

### What needs validation

- **Migration rehearsal** at small scale: split a leaf Space into two,
  verify subscribers see no inconsistency.
- **Settlement-paced migration** under live load: full repartitioning
  during a synthetic settlement window.
- **Migration with failures:** kill the migration mid-flight; verify
  rollback works.

---

## 11. Aggregator robustness

Scatter-gather aggregations have their own correctness landmines.

### Trivial combiners (sum, max, min, count)

Mostly fine, but watch:

- **Floating-point sum order-dependence.** If targets return floats and
  the synserv sums in arrival order, results are non-deterministic.
  Mitigation: integer/bp arithmetic for safety-critical math; explicit
  sort before sum if floats are unavoidable.
- **Empty target set.** What's `sum []`? Define explicitly: 0 for sum,
  -∞ for max, ∞ for min, false for any, true for all.

### Sketch combiners

Percentiles, distinct-counts, quantiles use sketches (t-digest, HLL).
These are *approximate* and have known error bounds.

- **Don't use sketches for safety-critical math.** Penalty calculations
  must be exact; sketch error compounds.
- **Document sketch error bounds** alongside any rule that uses them.
- **Validate merge correctness** under target failures (one target
  returns nothing, the merged sketch must be valid for the rest).

### What needs validation

- **Determinism** of aggregations under reordering of target responses.
- **Sketch correctness** under partial-failure scenarios.
- **Empty-set semantics** defined and tested for every aggregator.

---

## 12. Trust model fragility

Different compromises have different blast radii. Worth mapping them
explicitly.

| Compromise | Blast radius | Mitigation |
|---|---|---|
| One operational beacon's key | Whatever that beacon was authed for; bounded by auth ceiling | Auth scope, revocation via retract `(beacon-status … active)` |
| Guardian's root cert authority | Whole subtree under that Guardian; can re-cert/re-auth at will | Guardian-level governance recourse; Core Council can revoke |
| Synserv (single) | Total — corrupted canonical history | Replication consensus; cryptographic commits; multi-validator |
| Replication channel | Subscribers see corrupted view (but synserv truth is still good) | Hash-chain replication; subscribers reject bad chains |
| Goertzel cube physical | Locality of the cube's atoms; possible silent corruption | Hub-replication of universal Spaces; subscriber-side hash checks |

### What needs validation

- **Beacon revocation propagation time:** retract a beacon, measure
  time until gate refuses its sigs.
- **Synserv tamper detection:** introduce an inconsistent atom into
  synserv's log; verify replication consensus rejects.
- **Replication chain integrity** under hostile network conditions.

---

## 13. Testing strategy

Five categories, each with concrete deliverables before Phase 1 launch.

### Unit (per-rule)

- Every `permits` rule has positive and negative test cases (auth granted, auth absent).
- Every constructor has idempotency tests (call twice, second is no-op or error).
- Every `rule-reads` declaration is exhaustive (lint: rule body's `match` calls vs declared reads).

### Integration (end-to-end)

- Beacon sends submission → gate verifies → synserv constructs → atomspace updates → subscriber sees update.
- Cross-Space writes within a constructor are atomic.
- Two-phase settlement closes correctly: per-Prime → `&core-settlement`.

### Chaos

- Synserv crash mid-write; recovery from last-acked.
- Network partition between beacons and synserv; reconvergence.
- Subscriber falls behind; catch-up correctness.
- Synserv replica failover; no double-leader.

### Load

- Gate sustained throughput at 10x expected.
- Burst handling at 100x expected.
- Scatter-gather fan-out across 1000 targets.
- Replication lag under sustained writes.

### Long-running

- 30-day continuous-operation test on staging.
- Monitor: storage growth, replication lag drift, atomspace fragmentation.
- Compaction kicks in on schedule; no atom loss.

### Migration

- Per-Space split rehearsal on staging.
- Settlement-paced repartition under synthetic load.
- Kill mid-migration; rollback correctness.

---

## 14. Open scaling questions

Worth flagging now, defer answers until decisions are forced:

**a) Synserv consensus protocol.** Single-leader for Phase 1; what's the
upgrade path? Raft or Paxos for ordered log; Tendermint-style for full
BFT; or something cryptographically-anchored (zk-rollup-shaped). Each
has different latency, throughput, and trust profiles.

**b) Cross-shard transactions when DAS partitions across cubes.** A
constructor that writes to two cubes' Spaces — atomic? Two-phase
commit? Probably not; instead, design constructors to be local to one
cube + idempotent retries.

**c) DAS query routing under load.** For complex multi-Space queries,
the routing layer's cost matters. May need query-planning layer above
the runtime.

**d) Probmesh update cadence.** When the canonical probmesh becomes
real, what's its acceptable update rate? Faster than governance, slower
than events. May need its own propagation channel separate from
deontic-skeleton updates.

**e) When does single-leader synserv become unviable?** Probably when
event rates exceed ~10k/sec sustained or when settlements need
sub-second close. Before then, single-leader + standby is fine.

**f) Telart and embart sync semantics.** Telart spread within a tel's
emb fleet runs on a separate channel (§1) but shares physical
substrate with synart replication. Bandwidth contention,
prioritization, and per-tel quotas need design. Embart never
replicates so doesn't need a sync story, just locality optimization.

**g) Telseed onboarding load.** When many telseeds spawn simultaneously
(e.g., a popular telseed configuration drops, dozens of researchers
fire it up), each new tel pulls a substantial synart slice on first
sync. Spike load profile: peak 50-200MB×N parallel transfers for a few
minutes, falling to steady-state per-tel sync rates after. Mitigations:
synart slices delta-cacheable at gateway; telseed configs declare
sync set so synserv can predict; per-tel sync-rate limits during
high-spawn windows.

**h) Endoscraper bandwidth.** Endoscrapers (`topology.md` §6 executable
layer) poll chain RPC endpoints at protocol-specific rates. Each
endoscraper writes parsed events into `&core-endoscrapers` and forwards
verified facts to entart leaves. Load profile: chain-protocol-bound
inflow, with reconciliation cost when matched against beacon
submissions. Per-protocol endoscraper independence allows horizontal
scaling.

**i) Cross-tel telgate-to-telgate traffic.** Tels coordinating
peer-to-peer (e.g., negotiating call-out service contracts, sharing
proposals before publication) generate inter-tel traffic that doesn't
pass through synserv. Distributed; growing with tel population;
needs its own routing/discovery story analogous to DNS or peer
discovery in P2P systems.

---

## 15. The one-line summary

**Synart's topology is sound; its operational reality is gated by
synserv's single-writer model, replication staleness, partial-sync
correctness, hot-spotting on universal Spaces, storage growth,
partition tolerance, and the testing discipline that proves all of the
above hold under real load and adversarial conditions.**
