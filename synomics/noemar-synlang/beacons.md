# Beacons — Roles and Catalog

**Status:** Sketch. Old beacon classes are being collapsed into a
two-role taxonomy now that calculation has moved into synart-resolved
in-space computation. Phase 1 implementation will fill in concrete
classes and per-protocol details.

Companion to `listener-loops.md` (where the calculation now lives),
`synart-access-and-runtime.md` (auth + identity), `boot-model.md`
(identity-driven boot), `topology.md` §6 (executable layer), and
`synlang-patterns.md` §6 (Sentinel formations as the high-power
extreme of the action role).

---

## The two roles

After moving calculation out of beacons and into the synart (per
`listener-loops.md`), beacons become pure I/O:

### Input beacons — push data into book spaces

| Class | Reads from | Writes |
|---|---|---|
| **Endoscraper** | On-chain protocol state (deterministic, public) | Chain events, contract state deltas, redemption flows |
| **Oracle** | Off-chain market data (price feeds, indices, FX rates) | Price atoms, index updates |
| **Attestor** | Off-chain claims (custody balances, contract terms, compliance facts) | Signed attestation atoms |

Differences in trust model:
- Endoscrapers are deterministic (chain reads); verifiable by re-scraping
- Oracles are pushed data with provider trust; verifiable by oracle
  redundancy / dispute mechanisms
- Attestors are signed off-chain claims with attestor liability;
  verified at slashing time, not at write time

### Action beacons — emit chain txs based on synart state

| Class | Acts on | Authority |
|---|---|---|
| **Relayer** | Submits governance-initiated or user-initiated txs to chain | Narrow, per-target |
| **Executor** | Executes strategies derived in synart (settlement, rebalance, etc.) | Scoped to specific verbs and targets |
| **Sentinel formation** (HPHA) | Baseline/Stream/Warden patterns operating Primes or Halos | Broader; with formation-internal checks; Phase 9-10+ |

Action beacons read synart state to decide what to do; they don't
calculate it themselves.

### Both roles share

- Registered identity in `&core-registry-beacon` per `boot-model.md` §4
- Gate-mediated submissions per `synart-access-and-runtime.md` §9
- Auth scoped narrowly per the cert/auth chain (`syn-overview.md` §5)
- Replay protection via nonces per `govops-synlang-patterns.md`

---

## Old → new mapping

The old beacon catalog mixed I/O with calculation. The new taxonomy
splits these. Approximate mapping:

| Old class | New role | Notes |
|---|---|---|
| `lpla-checker` | **Disappears** | Calculation moves to in-space per `listener-loops.md` |
| `lpla-verify` | **Verifier emb** (not a beacon class) | Re-derivation via shadow execution per `boot-model.md` §5 |
| `lpha-relay` | **Action beacon (relayer)** | Already pure I/O |
| `lpha-nfat` | **Action beacon (executor)** | Submits NFAT txs based on synart state |
| `lpha-lcts` | **Action beacon (executor)** | Same |
| `lpha-council` | **Action beacon (executor)** | Council ops |
| `lpha-halo` | **Endoscraper or attestor** depending on data source | Reporting role; on-chain → endoscraper, off-chain → attestor |
| `endoscraper-<protocol>` | **Input beacon (endoscraper)** | Already in the new shape |
| `stl-base` / `stl-stream` / `stl-warden` | **Sentinel formation (HPHA action)** | Per `synlang-patterns.md` §6 |

The Beacon Framework (LPLA / LPHA / HPLA / HPHA) from the
power-by-authority matrix is orthogonal to the two-role taxonomy —
it describes the *authority profile*; input vs action describes the
*work shape*.

---

## Open questions

Deferred to Phase 1:

1. **Concrete class implementations** — per-protocol endoscrapers,
   oracle providers (Chronicle, Chainlink, etc.), attestor
   templates and slashing terms.
2. **Oracle vs attestor boundary** — they differ in trust model
   (push vs pull, who signs, what the slashing surface looks like).
   Some data sources blur the line; need clear per-class definitions.
3. **Action-beacon authority scope** — Phase 1 has narrow,
   manually-authed beacons; later phases give Sentinel formations
   broader scope. The auth grant/revocation mechanics are settled
   (`synart-access-and-runtime.md` §4-§7); the per-class scope
   policies aren't.
4. **Beacon-to-listener interaction** — does an input beacon's
   write trigger a listener loop directly, or always through synserv
   write processing? Resolved by `listener-loops.md` §"How synserv
   does it" once that's picked.
5. **Verifier embs vs verifier beacons** — verifier embs (per
   `boot-model.md` §5) shadow-execute loops; do we still need a
   separate verifier beacon class, or does shadow execution cover
   it entirely?
