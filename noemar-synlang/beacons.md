# Beacons — Roles and Catalog

**Status:** Sketch. Old beacon classes have been collapsed into the
six-class taxonomy in `../macrosynomics/beacon-framework.md` now that
calculation has moved into synart-resolved in-space computation, and
endoscraping has moved from a beacon class to a grounded runtime
primitive. This file gives the role-shape overview; the canonical
class catalog lives in `beacon-framework.md`.

Companion to `listener-loops.md` (where the calculation now lives),
`runtime.md` (auth + identity), `boot-model.md`
(identity-driven boot), `topology.md` §6 (executable layer), and
`../sentinel/sentinel-network.md` (baseline-relay + warden-relay +
stream-sentinel operating setup).

---

## The two roles

After moving calculation out of beacons and into the synart (per
`listener-loops.md`), beacons become pure I/O:

### Input beacons — push data into book spaces

| Class | Reads from | Writes |
|---|---|---|
| **market-data-beacon** | Off-chain market data (price feeds, indices, FX rates) | Price atoms, index updates |
| **attest-data-beacon** | Off-chain claims (custody balances, contract terms, compliance facts) | Signed attestation atoms |
| **patch-beacon** | External (govops attestation, sudoed) | Direct atom writes into a target Space; Guardian-sudoed, designed to sunset |

Endoscraping (deterministic on-chain reads) is **not** a beacon class
in the current taxonomy — it's a grounded runtime primitive
(`(chain-read $contract $slot)`) that any rule in any Space can call.
Per-protocol metadata lives in `&core.protocol`. See
`../macrosynomics/beacon-framework.md` for the full class catalog and
trust-model treatment.

### Action beacons — emit chain txs based on synart state

| Class | Acts on | Authority |
|---|---|---|
| **relay** | Reads synart state, submits the corresponding tx (nfat / lcts / amm / baseline / warden / council / auction / identity / rate / gov / nfat issuance, etc.) — single class with many stems | Scoped per verb and target |
| **sentinel** | Stream-sentinels (in-entart per Prime/Halo) and principal-sentinels (per owner) — emergency-action, formation-internal checks | Broader; with formation-internal checks; Phase 9-10+ |

Action beacons read synart state to decide what to do; they don't
calculate it themselves. The earlier `lpha-*` / `hpha-*` four-letter
prefixes are retired; instance identifiers are bare stem + owner
(e.g., `nfat-spark-term`, `baseline-spark`, `stream-spark-{actor}`).
Only legacy peer-to-peer trade beacons retain the `hpla-` prefix as a
stable identifier handle.

### Both roles share

- Registered identity in `&core.registry.beacon` per `boot-model.md` §4
- Gate-mediated submissions per `runtime.md` §9
- Auth scoped narrowly per the cert/auth chain (`runtime.md` §3–§7)
- Replay protection via nonces per `../inactive/archive/govops-synlang-patterns.md` (historical demo)

---

## Old → new mapping

The old beacon catalog mixed I/O with calculation. The new taxonomy
splits these and drops the power-as-axis. Approximate mapping (see
`../macrosynomics/beacon-framework.md` for the canonical list):

| Old class | New name / role | Notes |
|---|---|---|
| `lpla-checker` | **Retired** | Calculation moves to in-space per `listener-loops.md` |
| `lpla-verify` | **Retired** (verifier emb, not a beacon class) | Re-derivation via shadow execution per `boot-model.md` §5 |
| `lpha-relay-{x}` | `relay-{x}` (class **relay**) | Pure I/O |
| `lpha-nfat-{halo}` | `nfat-{halo}` (class **relay**) | Submits NFAT txs based on synart state |
| `lpha-lcts-{halo}` | `lcts-{halo}` (class **relay**) | Same |
| `lpha-council` | `council-{x}` (class **relay**) | Council ops |
| `lpha-halo-{name}` | On-chain reads → `chain-read` primitive; off-chain claims → `attest-data-{class-id}` (class **attest-data-beacon**) | Split by data source |
| `endoscraper-{protocol}` | **Retired as beacon class** | Grounded runtime primitive `(chain-read $contract $slot)`; per-protocol metadata in `&core.protocol` |
| `oracle-exsyn-{class}` | `patch-{target}` (class **patch-beacon**, Guardian-sudoed) | exsyn-TRRC writes relocated to per-primebook patch-beacons |
| `stl-base-{prime}` | `baseline-{prime}` (class **relay**) | Deterministic synart code post-noemar |
| `stl-warden-{prime}-{op}` | `warden-{prime}-{op}` (class **relay**) | Deterministic halt monitor |
| `stl-stream-{prime}-{actor}` | `stream-{prime}-{actor}` (class **sentinel**, variant stream) | Lives in entart, not a universal template |
| `stl-principal-{owner}` | `principal-{owner}` (class **sentinel**, variant principal-sentinel) | |
| `hpla-trade-*` / `hpla-arb-*` / `hpla-coop-*` | Retained as legacy peer-to-peer identifiers | The `hpla-` prefix survives only on these |

The power-as-axis (LPLA / LPHA / HPLA / HPHA) is retired. The six-class
system (relay / sentinel / market-data / attest-data / patch / synserv-ish)
plus per-stem identifiers replaces it. See
`../macrosynomics/beacon-framework.md`.

---

## Open questions

Deferred to Phase 1:

1. **Concrete class implementations** — per-protocol metadata in
   `&core.protocol` for `chain-read` calls, market-data providers
   (Chronicle, Chainlink, etc.), attest-data templates and slashing
   terms.
2. **market-data vs attest-data boundary** — they differ in trust
   model (push vs pull, who signs, what the slashing surface looks
   like). Some data sources blur the line; need clear per-class
   definitions.
3. **Action-beacon authority scope** — Phase 1 has narrow,
   manually-authed beacons; later phases give Sentinel formations
   broader scope. The auth grant/revocation mechanics are settled
   (`runtime.md` §4-§7); the per-class scope
   policies aren't.
4. **Beacon-to-listener interaction** — does an input beacon's
   write trigger a listener loop directly, or always through synserv
   write processing? Resolved by `listener-loops.md` §"How synserv
   does it" once that's picked.
5. **Verifier embs vs verifier beacons** — verifier embs (per
   `boot-model.md` §5) shadow-execute loops; do we still need a
   separate verifier beacon class, or does shadow execution cover
   it entirely?
6. **attest-data atom schema + reconciliation cycle.** Atom shape
   for off-chain attestation claims, plus the reconciliation cycle
   for cases where `chain-read` calls can't independently verify the
   claim (off-chain custody, off-chain contract terms, compliance
   facts). The cert/auth/beacon-class machinery already exists per
   `runtime.md`; the genuinely new design is the attestation atom
   schema and the reconciliation flow. Forcing trigger: building
   the v1 crypto-collateralized lending test attest-data beacon —
   the first concrete instance that will shape the schema.
