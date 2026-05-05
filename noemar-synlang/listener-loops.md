# In-Space Calculation — Notes

**Status:** Sketch. Captures the concept; implementation deferred to
Phase 1.

Companion to `synart-access-and-runtime.md` (auth + runtime),
`boot-model.md` (identity-driven boot), and the in-progress beacon
rethink.

---

## The pattern

Three classes of input beacon push data atoms into book spaces:

- **Endoscrapers** — read on-chain protocol state
- **Oracles** — price feeds, market data
- **Attestors** — off-chain claims (custody balances, off-chain
  contract terms)

Each writes signed atoms into the relevant book space (Riskbook,
Halobook, Primebook, Genbook, or the Generator's structural-demand
space).

For each book, synserv runs whatever calculation is needed to keep
its derived state (equity, CRR, matching status, breach flags,
encumbrance ratio, etc.) consistent with current input atoms, in
real time. The calculation logic is synart-resolved code; synserv
executes it.

```
endoscraper write ────┐
                      │
oracle write ─────────┼──→ atom lands in book space
                      │
attestor write ───────┘
                          │
                          ▼
                    synserv re-derives the book's derived state
                    from current input atoms (somehow)
                          │
                          ▼
                    derived atoms updated in the book space;
                    replicated to subscribers
```

---

## Why this matters

The old beacon model (`lpla-checker` and similar) had calculation
happening in beacon processes off-loop. The new model moves all
calculation into synart-resolved code that synserv runs. Three
consequences:

1. **Full verifiability.** Wardens can re-derive everything because
   the calculation is synart code, not opaque off-loop compute.
2. **Beacons become pure I/O.** Input beacons (scrapers / oracles /
   attestors) push data; action beacons emit chain txs based on
   synart state. No calculation in either.
3. **No lag.** Derived state always reflects current input atoms.

---

## How synserv does it

Open. Several plausible mechanisms:

- Event-driven (synserv fires per-book calculation when matching
  atoms arrive)
- Heartbeat poll (per-book loop ticks fast, recomputes from current
  state)
- Hybrid (hot books event-driven, cold books polled)
- Something else

To be decided during Phase 1 implementation when concrete latency,
throughput, and operational concerns force the choice. The invariant
that needs to hold regardless of mechanism: **derived state in any
book is a deterministic function of its current input atoms, and
synserv is responsible for keeping it current.**

---

## Comparison

| | Heartbeat loop | In-space calculation | Beacon |
|---|---|---|---|
| **Triggered by** | Internal clock | Input atom changes (mechanism TBD) | External event |
| **Runs in** | Process at boot identity | Synserv (or wherever Phase 1 puts it) | External process |
| **Purpose** | Periodic work (settlement, cleanup) | Derive book state from inputs | Witness / sign / submit |
| **Verifiability** | Re-runnable by wardens | Re-runnable by wardens | Re-derivable from chain |

Beacons are I/O. Heartbeat loops are scheduled work. In-space
calculation is reactive derivation. Three roles, three mechanisms;
see `beacons.md` for how old mixed-role beacons collapse into clean
instances of these categories.

---

## Open questions

Deferred to Phase 1:

1. Implementation mechanism (see "How synserv does it")
2. Same-book writes vs paired derived sub-space for derived atoms
3. Failure mode when a calculation errors (halt vs log-and-continue)
4. Whether call-outs to local cognition are admitted at this layer
   (`synlang-patterns.md` §5), or strictly pure synlang
