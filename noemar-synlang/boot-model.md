# Boot Model — Identity-Driven Evaluation

How a Noemar instance (or any conforming atomspace runtime) starts up
and becomes a participant in the synome. The architectural shift this
captures: **the synart is the program, the runtime is the interpreter,
identity is the entry point.** There's no separate "instantiation" or
"install" step — booting Noemar against the synart with a given
identity runs the loop that identity is registered for.

Companion to `runtime.md` (the `(run-forever)` shape
in §10 is the concrete instantiation of this abstract model for the
synserv role), `topology.md` (where loops live structurally), and
`../synodoxics/noemar-substrate.md` (the three-tier substrate this boot model runs on; formerly `syn-tel-emb.md`).

---

## TL;DR

```
noemar boot --identity=X --key=path/to/key.pem --synart=endpoint
```

That command:

1. Mounts the synart (canonical or replicated copy).
2. Looks up `X` in `&core-registry-beacon` (and possibly elsewhere).
3. Resolves what loop `X` runs — a Space pointer in synart.
4. Evaluates `(run-forever)` with that Space as `&self`, with `X`'s
   identity bound from the boot args.

Everything else flows from there.

The deeper claim: **the same mechanism boots a synserv, a beacon, a
sentinel formation, an archive emb, a verifier emb.** Different
identities resolve to different loops. One runtime, one synart, many
roles — all parameterized by which identity boots.

---

## 1. The synart is the program

Three statements, equivalent in this model:

- "The synart contains the loops."
- "The synart **is** the program of the entire synome."
- "Spaces are the units of code; the runtime is the interpreter."

Compared to typical software architectures:

| Architecture | State | Code |
|---|---|---|
| Database + app | DB | Separate app code |
| Smart contracts | Chain state | Contract bytecode in chain state, off-chain workers separate |
| **Synome** | Synart | Loops, gates, recipes are atoms in synart; runtime evaluates them in place |

The synome goes one step further than smart contracts: even the
synserv that hosts the synart is described by code *in* the synart.
The runtime that interprets the synart has its source in the synart's
library layer (`&core-library-runtime-*`). It's self-hosting all the
way down.

**Implication:** there's no separate "code distribution" channel.
Replication of the synart is replication of the running program.
Subscribing to a synart slice means subscribing to the executable code
of whatever roles you might run.

---

## 2. The boot CLI

The minimal invocation:

```
noemar boot \
    --identity=spark-nfat-1 \
    --key=secrets/spark-nfat-1.pem \
    --synart=https://synserv.example.com \
    [--sync-policy=full|partial:<spec>]
```

That's the entire input contract. Off-synart inputs are kept to the
absolute minimum:

| Input | Why it's local-only |
|---|---|
| Identity name | Acts as the registry lookup key |
| Private key file | Replicated state can't hold secrets |
| Synart endpoint | Bootstrapping needs to know where to connect |
| Sync policy (optional) | Performance preference; affects which slices are replicated locally |

Everything else — what loop to run, what reads to subscribe to, what
auths apply, what call-outs to expect, what gate to use — comes from
the synart.

### What about hardware-specific config (GPU device, network interfaces)?

Goes in the runtime's local config (separate from the boot CLI). The
boot model treats hardware concerns as the runtime's responsibility,
not synart's. A telart-Space can have advisory atoms ("prefers GPU 0,"
"max memory 32GB") but enforcement is local.

---

## 3. The bootstrap procedure is itself a Space

Noemar starts knowing only how to do one thing: **read `&core-boot`
from synart and evaluate its contents.** Everything else is delegated
to that Space's content.

```metta
;; in &core-boot — the synart's own bootloader, run by every fresh runtime

(= (boot $identity)
   (let* (($keyfile     (runtime-arg key-file))
          ($synart-url  (runtime-arg synart-endpoint))
          ($_           (mount-synart $synart-url))
          ($_           (load-private-key $keyfile))
          ($role-pointer (resolve-identity-role $identity))
          ($loop-space   (resolve-loop-space $role-pointer)))
     (eval-in $loop-space (run-forever))))

(= (resolve-identity-role $identity)
   (match &core-registry-beacon
     (and (beacon-id $identity)
          (beacon-class $identity $class)
          (loop-pointer-for-class $class $pointer))
     $pointer))
```

So the bootstrap is itself synart content. Updating the bootstrap
procedure means updating an atom in `&core-boot`. There's nothing
"outside" that defines how to boot — even bootstrapping is data.

---

## 4. Identity → role lookup

The pivotal step is: given `--identity=X`, which loop does Noemar run?
The answer comes from `&core-registry-beacon`, which holds a row per
registered identity:

```metta
;; in &core-registry-beacon
(beacon-id          spark-nfat-1)
(beacon-pubkey      spark-nfat-1 "ab9c…")
(beacon-class       spark-nfat-1 lpha)
(beacon-status      spark-nfat-1 active)

(loop-pointer-for-class lpha             &core-loop-beacon-lpha)
(loop-pointer-for-class hpha-baseline    &core-loop-sentinel-baseline)
(loop-pointer-for-class hpha-warden      &core-loop-sentinel-warden)
(loop-pointer-for-class synserv          &core-loop-synserv)
(loop-pointer-for-class archive          &core-loop-archive)
(loop-pointer-for-class verifier         &core-loop-verifier)
(loop-pointer-for-class endoscraper-spark-pau  &core-loop-endoscraper-spark-pau)
```

The runtime resolves `spark-nfat-1` → class `lpha` → loop pointer
`&core-loop-beacon-lpha`. That's the universal template loop. For
entities with per-entity loop instances (Sentinel formations, certain
beacons), the resolved Space is the entity-specific one:

```metta
;; A Spark Sentinel-Baseline beacon's row points to the per-Prime instance:
(beacon-id            spark-baseline-1)
(beacon-class         hpha-baseline)
(beacon-entity        spark-baseline-1 spark-prime)
(loop-pointer-for     spark-baseline-1 &entity-prime-spark-sentinel-baseline)
```

So the resolution is: identity → class → either universal-template
pointer (for generic loops) or per-entity-instance pointer (for
loops specialized per entity).

### The two-step loop pattern

This is the loop-equivalent of the two-step rule pattern from
`topology.md` §16:

| Level | Where | Role |
|---|---|---|
| Universal template | `&core-loop-<class>` | portable loop body using `&self`; canonical, audited |
| Per-entity instance | `&entity-<type>-<id>-<sub-kind>` | entity-specific config + reference / context for the template |

When booting with a per-entity loop pointer, Noemar evaluates the loop
body (imported from the universal template) in the context of the
per-entity Space. Same code, different bindings. The universal template
lives once; entity-specific configurations are lightweight wrappers.

---

## 5. Shadow execution property

A consequence of identity-driven boot: **any embodiment can evaluate
any loop locally.** Everything's in synart; all loops are universally
readable. What changes between embs is *which writes count as
canonical.*

Three concrete uses:

**Verifier embs.** A verifier emb runs the same loop the canonical
emb runs, derives its own outputs, compares. Disagreement triggers
a `(verification-disagreement …)` atom in `&core-escalation`. This
is byzantine resistance through replicated computation — the verifier
needed no special access, just the ability to run the loop.

**Cross-warden formation.** Multiple Wardens of the same Sentinel
formation each independently re-derive what Baseline should propose
given the same inputs. Their disagreement among themselves (or with
Baseline) is the safety signal.

**Sandbox / dry-run testing.** A new tel can run any loop locally
without write authority, just to see what would happen. Fully isolated
from canonical state.

### Auth-bounded canonicality

What makes one emb's evaluation canonical and others' shadow? Auth.

```metta
;; in &core-skeleton or governance Space
(canonical-synserv-runner core-synserv-canonical)

;; in &core-registry-beacon
(beacon-id     core-synserv-canonical)
(beacon-class  synserv)

;; in the relevant entart Spaces — only the canonical synserv has write auth
(auth core-synserv-canonical write &core-settlement)
(auth core-synserv-canonical write &core-aggregation-*)
;; ... etc.
```

Other embs running the synserv loop produce the same logical outputs
but lack the auth atoms. Their writes don't gate through; their
in-memory results are local. The canonical instance is the one whose
identity has been blessed with the right auths — a governance fact,
not a runtime distinction.

**Failover is an atom write.** When a canonical synserv fails,
governance retracts `(canonical-synserv-runner core-synserv-canonical)`
and adds `(canonical-synserv-runner core-synserv-backup)`. The backup's
loop instance — which had been running shadow — becomes canonical from
the next tick.

---

## 6. Boot also resolves "which gate to run"

For roles that operate gates (synserv runs syngate; teleonomes run
telgate instances), the boot procedure also resolves which gate Space
to mount as part of role setup.

| Identity class | Gate it runs |
|---|---|
| `synserv` | `&core-syngate` (synart, universal — synserv is the canonical instance) |
| Teleonome identity | A telgate instance Space in own telart, running the universal `&core-telgate` spec from synart |
| Beacon identity | No gate of its own; it gates *out* through its parent tel's telgate (or directly to syngate for some operational beacons) |
| Endoscraper identity | No gate; it reads chain RPCs and writes through the parent synserv's normal write path |

Gate setup is part of the loop's `(boot)` step, not a separate concern
the runtime handles. Loops that need a gate include the gate
instantiation in their loop body.

---

## 7. Hot-swap and version transitions

Loop bodies in synart are atoms. Updating a loop is `add-atom` of the
new body + `remove-atom` of the old. Three modes for how running embs
pick up the change:

### Mode A — Tail-recursion picks up the new body (common case)

`(run-forever)` re-resolves `(heartbeat)` (and its sub-rules) every
tick by name. If the atoms backing those names get updated mid-tick,
the next tick uses the new versions.

This works for additive changes, parameter tweaks, and minor logic
adjustments. It's the lightest-touch upgrade.

### Mode B — Atomic restart with `(halt-heartbeat)`

For breaking changes (different signature, incompatible state shape),
governance writes `(halt-heartbeat)` into the relevant scope; running
embs notice and idle. Then the loop atoms get updated. Then `halt`
gets retracted; embs resume with the new loop.

Brief pause; clean cutover. Works for changes that need a coherent
swap.

### Mode C — Double-mesh / shadow synserv

For the deepest changes — synserv loop itself, gate semantics, core
auth model — the upgrade runs on a parallel grid:

```
1. Stand up shadow synserv with new loop atoms.
2. Replay current synart state into the shadow at last settlement
   boundary.
3. Run live + shadow in parallel; verify outputs agree under
   non-breaking inputs.
4. At a settlement boundary, retract `(canonical-synserv-runner old)`
   and add `(canonical-synserv-runner new)`. Live cuts to shadow.
5. Decommission old synserv after a soak period.
```

This is the double-mesh trick (see `scaling.md` §10) applied to
runtime upgrades. Heavy but safe.

### Choosing the mode

| Change | Mode |
|---|---|
| Add new external verb to whitelist | A |
| Adjust framework parameter values | A |
| Change internal loop sequencing (not external behavior) | A or B |
| Change a permission rule's body | B |
| Restructure auth model | C |
| Change synserv heartbeat shape | C |
| Migrate to a different atomspace runtime impl | C with extended soak |

The mode is governance's choice based on the change's semantics. The
boot model accommodates all three because loops, gates, and auth atoms
are all data — they can be updated in place by the same mechanisms
that update other state.

---

## 8. Failure modes

What goes wrong, and how the boot model handles it:

### Identity revocation mid-loop

Governance retracts a beacon's `(beacon-status … active)` atom. The
running emb's next gate-out attempt fails (gate refuses sigs from a
non-active beacon). Loop should detect the rejection and either:

- Halt cleanly (preferred for unexpected revocation)
- Re-resolve identity and retry with a new identity if available

The loop body specifies which behavior; runtime doesn't enforce one.

### Loop atom retraction during evaluation

If `(= (heartbeat) ...)` is retracted while a tick is in flight, the
in-flight tick continues with the version it captured at start (synlang
evaluation is generally tick-atomic). The *next* tick will re-resolve
`(heartbeat)` and find no body — it will idle (or error, depending on
the loop's `case` defaults).

This is intentional: loop retraction is a halt mechanism. Removing the
loop body stops new ticks from doing anything meaningful.

### Runtime crash recovery

Noemar process crashes. The atomspace flushes to disk on graceful
shutdown; on crash, recovery proceeds from last flush. Boot procedure:

```
1. Restart Noemar with same args.
2. Mount synart from disk-cache; reconcile with live synserv to fill
   any gap since crash.
3. Resolve identity → loop pointer (fresh lookup; identity may have
   been revoked during downtime).
4. Resume `(run-forever)` from the loop's persistent state if any
   (typically just resync gate-in queue position, restart from latest
   processed nonce).
```

Beacons rarely have meaningful loop-local persistent state because
their work is push-through (witness → sign → emit). Synserv has more
persistent state (settlement history, audit trail) but those are
synart writes that survive crashes by definition.

### Partial sync hard-fail

A loop reaches into a Space the emb hasn't synced. Per `topology.md`
§14 / `scaling.md` §5, default behavior is hard-fail (the rule refuses
to evaluate; emits an error atom; loop's error handler decides next
action). The boot procedure can declare which Spaces it expects to
have available; runtime can pre-check at boot and refuse to start if
required Spaces aren't synced.

---

## 9. The grounded fast-path

Some primitives can't be written in synlang for performance reasons —
ed25519 sig verification, atomspace pattern matching, network I/O.
These live as **grounded native code** in the runtime, not as synlang
atoms.

The boot model accommodates this by treating grounded primitives as
opaque function calls from synlang's perspective. The pattern:

| Aspect | Where it lives |
|---|---|
| Spec for the primitive's behavior | In synart as synlang (e.g., `&core-spec-gate-in` describes what the gate does in pseudocode) |
| Implementation | In Noemar's source as native code (e.g., Rust impl of ed25519 verification) |
| Conformance test | In synart as governance-vetted test atoms |
| Verifier check | A verifier loop reads the spec, executes the primitive, validates conformance |

So the *spec* is in synart and is the source of truth; the *impl* is
fast-path; the *verifier* checks they agree. This generalizes the
"functional core, imperative shell" pattern from
`runtime.md` §10.

For new grounded primitives added to the runtime, governance
obligations:

1. Publish the spec in synart.
2. Add conformance test atoms.
3. Verifier embs validate the impl on each new runtime version.
4. Cross-runtime test vectors guarantee impl-A and impl-B produce the
   same answers.

---

## 10. Connection to existing docs

| Doc | What it covers, relative to this one |
|---|---|
| `runtime.md` §10 | Concrete `(run-forever)` shape for the synserv role specifically — one application of the abstract boot model documented here |
| `runtime.md` §9 | Gate primitive details — boot resolves which gate to run via §6 above |
| `topology.md` §6 (executable layer) | Where loop and gate Spaces live structurally; `&core-loop-*`, `&core-syngate`, `&core-telgate` |
| `topology.md` §17 (two-step loop shape) | Universal template + per-entity instance pattern; expanded for loops here in §4 |
| `../synodoxics/noemar-substrate.md` "Atomspace Runtimes" | Atomspace runtimes — Noemar as one of multiple impls, runtime source in `&core-library-runtime-*` |
| `synlang-patterns.md` §5-§6 | Call-out primitive (for sentinel call-outs) and Sentinel formation patterns — running these uses this boot model |
| `telseed-bootstrap-example.md` | Worked trace of the boot procedure for a fresh telseed instantiation |

---

## 11. One-line summary

**Noemar boots with an identity argument, looks the identity up in
synart's beacon registry, resolves a loop Space pointer, and evaluates
`(run-forever)` with that Space as `&self` — making the running runtime
the embodiment of whatever role that identity is registered for.
Synart is the program; runtimes are interpreters; identity is the
entry point; auth atoms decide whose evaluations are canonical.**
