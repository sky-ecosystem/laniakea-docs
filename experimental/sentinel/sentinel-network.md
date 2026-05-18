# Sentinel Network

**Status:** Forward-looking — sentinels are not in Phase 1 scope. P1 has only relays (deterministic, govops-controlled). This doc describes the architecture for when ecosystem actors with proprietary intelligence and folios under principal control come online.

Sentinels are the **action class with cognitive call-out density** in the Laniakea beacon taxonomy. They split into two variants — **stream-sentinels** (ecosystem actors proposing intent into a Prime's relay) and **principal-sentinels** (folio owners with direct PAU control + bundled relay + local govops). The synlang substrate of the patterns lives in [`../noemar-synlang/synlang-patterns.md`](../noemar-synlang/synlang-patterns.md) §6; the marketplace surface that prices the work lives in [`../synoteleonomics/recipe-marketplace.md`](../synoteleonomics/recipe-marketplace.md).

For the broader beacon taxonomy (six classes plus synserv; relay vs sentinel split), see [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md).

---

## What Sentinels Are

A sentinel is a **high-authority action beacon with call-out density into operator telart**. Specifically:

- Strategy involves designated cognitive call-outs (LLM, classifier, scorer) that resolve to services in the operator's telart agart
- Strategy bounds and envelope-check code live in synart (in the entity's entart) — auditable
- Cognitive content is non-deterministic and private — verifiable only by output-shape conformance and provenance

This is what distinguishes sentinels from **relays** (no cognition, fully deterministic synart-resolved I/O) and from input-class beacons. Cognition is the load-bearing property — without call-outs, a beacon doing the same work would be a relay.

### Relay vs sentinel — the key separation

Earlier framings grouped Baseline / Stream / Warden / Principal under a unified "sentinel formation." The post-noemar architecture splits these:

| Old framing | Class | Why |
|---|---|---|
| Baseline (~95% synart, 5% call-out) | **relay** (stem `baseline-`) | Deterministic strategy is fully synart-resolvable post-noemar; no real cognitive density |
| Warden (~95% synart, 5% call-out) | **relay** (stem `warden-`) | Verify+halt is also deterministic synart re-derivation; the "call-out" was incidental |
| Stream (~10% synart, 90% call-out) | **sentinel** (variant stream) | Genuinely requires local cognition for intent proposal |
| Principal (varies) | **sentinel** (variant principal-sentinel) | Direct PAU control by single operator with discretionary cognition |

So "sentinel formation" as a term retires; what replaces it is "Prime operating setup" — a baseline-relay + warden-relay(s) + optional stream-sentinel(s) all wired to one PAU, plus the Streaming Accord between any stream-sentinel and the baseline-relay.

### Where sentinels live

Sentinels are not in Phase 1 scope. When they come online, they apply wherever there's a PAU with proprietary-cognition demand:

- **Prime stream-sentinels:** Ecosystem actors stream intent into a Prime's baseline-relay
- **Folio principal-sentinels:** Folio owners operate their PAU directly with cognitive discretion

What makes sentinels operationally distinct from relays is **cognitive density** — relays run deterministic synart-resolved code; sentinels run a synart envelope around per-tick call-outs into operator telart.

---

## Stream Sentinel

A stream-sentinel is an ecosystem actor (typically a proprietary trading firm or research tel) that proposes intent into a Prime's baseline-relay. The stream-sentinel does the cognitive heavy lifting; the baseline-relay executes within RTI bounds.

### Structure

| Component | Class | Role |
|---|---|---|
| **stream-{prime}-{actor}** | sentinel (variant stream) | Cognitive intent proposal; gate-out into baseline within bounds |
| **baseline-{prime}** | relay | Deterministic execution; accepts intent within RTI, signs PAU txs, falls back to Base Strategy on disconnect |
| **warden-{prime}-{op}** × ≥1 | relay | Independent re-derivation of baseline output; halt authority on divergence |

### Synart / call-out split per component

| Role | Synart share | Call-out share | Authority |
|---|---|---|---|
| stream-sentinel | ~10% (bounds + comm) | ~90% (proposal cognition) | Streams intent; no PAU keys |
| baseline-relay | 100% | 0% | Holds pBEAMs; signs PAU txs; no cognition |
| warden-relay | 100% | 0% | Halt authority via BEAM freeze; re-derives via grounded primitives |

### Why the separation

- **baseline-relay ensures all execution flows through public, auditable code.** No private actor directly moves Synomic Entity capital.
- **stream-sentinel lets proprietary intelligence influence execution without exposing strategies or holding keys.** The teleonome's alpha stays private; only proposals cross the boundary into synart-defined bounds.
- **warden-relays provide independent re-derivation.** Each warden re-runs the baseline-relay's deterministic strategy against current state via `(chain-read …)` and synart-resolved code; divergence beyond tolerance triggers halt.

### Inter-component channels

All communication goes through synart-defined channels (`gate-out (emit-to-baseline …)`, `gate-out (halt-baseline …)`). No out-of-band coordination — every interaction is auditable.

```
                                  stream-sentinel
                                  (cognition; private)
                                          │
                                          │ intent within RTI
                                          ▼
                                   baseline-relay
                                  (deterministic; PAU keys)
                                          │
                          ┌──────────────┼──────────────┐
                          │              │              │
                  warden-relay A   warden-relay B   warden-relay C
                  (independent operators; re-derive + halt)
```

---

## Time to Shutdown (TTS)

TTS is the structural constant that prices safety in the operating setup. It is the worst-case window between baseline-relay doing something wrong (whether from rogue stream intent or compromised key) and a warden-relay halting it.

```
TTS = (warden-relay tick interval) + (warden synart re-derive latency) + (halt propagation)
```

Note: call-out latency drops out compared to the legacy formation model, because warden-relays don't do call-outs — they're deterministic. The only call-out in the operating setup is in stream-sentinels' intent proposal, which doesn't affect TTS (the baseline-relay's RTI check enforces bounds regardless).

Each TTS component has a measurable bound; the sum is per-formation. TTS is what governance tunes when deciding how dangerous a setup is allowed to be.

### TTS → ORC

During the [0, TTS] window, a compromised baseline can damage at most:

```
Maximum Damage = Rate Limit × TTS
```

The Guardian (Ozone) accordant to the Synomic Entity posts operational risk capital covering that bound:

```
Required ORC ≥ Rate Limit × TTS
```

For the full ORC parameter calibration (including IRL/SORL interaction with Type 1 / Type 2 attacks), see [`../risk-framework/operational-risk-capital.md`](../risk-framework/operational-risk-capital.md) and [`../smart-contracts/rate-limit-attacks.md`](../smart-contracts/rate-limit-attacks.md).

### Two ways to read TTS

```
For Primes:     Better wardens → Lower TTS → Less ORC required (fixed rate limits)
For Primes:     Better wardens → Lower TTS → Higher rate limits allowed (fixed ORC)
For wardens:    Reliable, certified service has measurable price
For the system: Safety is priced in, not externalized
```

### TTS determinants

| Factor | Effect |
|---|---|
| Number of independent warden-relays | More → lower TTS |
| Operator diversity (geographic, organizational) | Diverse → lower TTS |
| Monitoring latency | Faster detection → lower TTS |
| Halt propagation speed | Faster BEAM freeze → lower TTS |
| Warden certification | Audited + SLAs → more reliable TTS |

### Independence requirement

Warden-relays **must** be operated by independent parties — distinct from the baseline-relay operator and from each other. If a baseline goes rogue, a warden run by the same operator may also be compromised. Independence is what makes "multiple wardens" multiplicative rather than additive.

---

## Streaming Accord

The Streaming Accord is the synomic contract governing the **stream-sentinel ↔ baseline-relay** relationship. It is a **recipe instance** in the marketplace — see [`../synoteleonomics/recipe-marketplace.md`](../synoteleonomics/recipe-marketplace.md) for the canonical recipe shape (loop body, call-out points, auth requirements, payment terms, slashing conditions, framework dependencies, library dependencies).

### Accord components

| Component | Purpose |
|---|---|
| **Risk Tolerance Interval (RTI)** | Bounds on what intent the baseline-relay will accept. Position limits, velocity limits, concentration limits, prohibited actions. |
| **Performance Fee Ratio** | Stream's share of outperformance vs Base Strategy. |
| **Termination conditions** | When the accord can be dissolved — accord expiration, breach, governance intervention, warden-triggered halt. |
| **Dispute resolution** | Synomic-governance-defined arbitration path. |

### Carry math

```
Carry = (Actual PnL − Counterfactual Baseline PnL) × Performance Fee Ratio
```

- If stream-sentinel underperforms the deterministic baseline: zero carry.
- If stream-sentinel outperforms: proportional share of alpha.
- The counterfactual is computed by the baseline-relay running its Base Strategy in simulation in parallel with live operation, uploaded to Synome.

### The compounding loop

Carry is private; it accrues to the operating teleonome behind the stream-sentinel. That carry can be reinvested into proprietary AGI capability (compute, training, data, additional embodiments). This is the steepest known compounding path:

```
Public capital → Private intelligence → Better streams → More carry → More intelligence
```

The loop is bounded by:

1. **Synomic constraints** — execution flows through the public deterministic baseline-relay.
2. **Warden-relays** — independent monitoring with halt authority.
3. **Rate limits + ORC** — maximum damage is bounded and collateralized.
4. **Revocability** — beacons can be revoked by governance.

The teleonome gains private intelligence without gaining unchecked power. Streams are the highest-leverage activity available to a teleonome.

---

## Principal Sentinel

Principal-sentinels are direct-control sentinels without a separate stream operator. Used primarily for folios under principal control, where a single competent operator wants direct PAU control combined with their own cognition.

### Structure

A principal-sentinel bundles three things into one identity:

1. **Cognitive control** — call-outs into principal's telart for discretionary intent
2. **Bundled relay** — direct PAU operation (pBEAM holdership, tx signing)
3. **Local govops** — folio-scoped governance (which the principal naturally has)

This makes principal-sentinels structurally distinct from stream-sentinels (which propose to a separately-operated baseline-relay) — the principal IS the relay operator AND the cognitive source AND the local governance.

### What Principal control gives up vs the stream-sentinel + relay setup

| Setup property | Principal-sentinel equivalent |
|---|---|
| Independent baseline-relay with deterministic execution | Principal directly operates PAU; cognitive decisions become PAU txs |
| Independent warden-relays with halt authority | No wardens; principal is self-accountable |
| Guardian posts ORC covering Rate Limit × TTS | No formation-level ORC; principal bears own risk |
| TTS-based capital efficiency | Rate limits are the sole on-chain constraint |
| Public deterministic baseline; private stream | Cognitive control throughout |
| SORL-constrained rate limit increases | Principal can modify via chosen governance mechanism |

### Expected users

Companies that already run stream-sentinels for other Primes / Halos — they have the infrastructure, expertise, and algorithms to operate autonomously. The PAU still provides structural protection (rate limits, audited contracts) but formation-level protections are absent.

For folio integration patterns (principal control vs automated), see [`../synomic-entities/folio.md`](../synomic-entities/folio.md).

### Open: internal structure

The exact internal structure of principal-sentinel (how the cognition + relay + local-govops bundle is wired) is deferred. The class is positioned in the taxonomy; concrete bundling pattern TBD.

---

## Folio Integration

Folios are the user-facing capital-deployment surface in the Laniakea stack. Each folio is a PAU operated by either an automated setup (baseline-relay + optional stream-sentinel) or a principal-sentinel.

| Mode | Operator | Pattern |
|---|---|---|
| **Automated folio** | baseline-relay (`baseline-{folio}`) + optional stream-sentinel (`stream-{folio}-{actor}`) + warden-relay(s) | Principal writes directive → setup executes within directive bounds |
| **Principal control folio** | principal-sentinel (`principal-{owner}`) | Principal operates PAU directly with cognitive call-outs |

The directive bounds for an automated folio are the folio's analogue of the RTI in a Streaming Accord. See [`../synomic-entities/folio.md`](../synomic-entities/folio.md) for the folio entity spec.

---

## Where sentinel Spaces live

Because sentinel strategy is per-operator (not standardized), there is **no universal synart template** for the sentinel class. Sentinel loop bodies live in the entart of the entity they operate on:

| Sentinel | Entart Space |
|---|---|
| stream-sentinel for Spark | `&entity.prime.spark.sentinel.{actor}` |
| principal-sentinel for a folio | `&entity.folio.{owner}.sentinel-principal` |

The entart-resident Space holds bounds, gate-out shape, call-out registry pointers, and envelope-check synart code. The cognitive call-outs resolve to services in the operator's telart agart, off-corpus and private.

Contrast with relays, which have universal synart templates at `&core.loop.relay.<stem>` and per-entity config in entarts. Relays standardize; sentinels are per-operator.

---

## Naming Conventions

Beacon identifiers follow the dash-separated `<stem>-<owner>-<disambiguator>` pattern (see [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) §9).

### Prime operating setup (forward-looking)

```
baseline-{prime}                    # relay class — deterministic baseline strategy
warden-{prime}-{operator}           # relay class — deterministic halt monitor
stream-{prime}-{actor}              # sentinel class, stream variant
```

Examples:
```
baseline-spark                      # Spark Prime's baseline-relay
stream-spark-horizonlabs            # Horizon Labs streaming for Spark (sentinel)
warden-spark-sentinelco             # SentinelCo warden for Spark (relay)
warden-spark-riskwatch              # RiskWatch warden for Spark (relay)
```

### Folio operating setup

```
baseline-{folio}                    # automated folio baseline-relay
stream-{folio}-{actor}              # stream-sentinel for automated folio
warden-{folio}-{operator}           # automated folio warden-relay
principal-{owner}                   # principal-sentinel (no separate stream/baseline)
```

### Halo action beacons (relays, not sentinels)

LCTS, NFAT, AMM operations on Halos are run by deterministic relays — no cognition.

```
lcts-{halo}                         # LCTS vault operations for Portfolio Halo
nfat-{halo}                         # NFAT facility operations for Term Halo
amm-{halo}                          # AMM operations for Trading Halo
```

For chain-side operational specs of these, see [`../smart-contracts/lcts.md`](../smart-contracts/lcts.md) and [`../smart-contracts/nfats.md`](../smart-contracts/nfats.md).

### Legacy mapping

| Old | New |
|---|---|
| `stl-base-{prime}` | `baseline-{prime}` (relay) |
| `stl-stream-{prime}-{actor}` | `stream-{prime}-{actor}` (sentinel) |
| `stl-warden-{prime}-{op}` | `warden-{prime}-{op}` (relay) |
| `stl-principal-{owner}` | `principal-{owner}` (sentinel) |
| `lpha-lcts-{halo}` | `lcts-{halo}` (relay) |
| `lpha-nfat-{halo}` | `nfat-{halo}` (relay) |
| `lpha-amm-{halo}` | `amm-{halo}` (relay) |

---

## Verification

Cross-checking positions against risk limits, computing per-risk-type CRRs / RRC / TRRC / Encumbrance Ratio, calculating PnL and carry — these are **synserv computations over book spaces**, not jobs assigned to a dedicated beacon. For each book (Riskbook, Halobook, Primebook, Genbook), synserv runs whatever calculation keeps derived state consistent with current input atoms in real time, using grounded primitives (`(chain-read …)`) for current chain state. The calculation logic is synart-resolved code; synserv executes it; wardens re-derive against the same code via the same primitives.

For the full computation surface, see [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) §4 (in-space calculation).

---

## Lifecycle

Principal-sentinels skip this lifecycle entirely — no accord, no formation assembly, no warden engagement. The lifecycle below applies to the stream-sentinel + baseline-relay + warden-relay setup.

### 1. Accord negotiation

- Ecosystem Actor proposes to operate a stream-sentinel for a Synomic Entity
- Terms negotiated: RTI, Performance Fee Ratio, slashing conditions
- Accord deployed as a recipe instance from the marketplace catalog (see [`../synoteleonomics/recipe-marketplace.md`](../synoteleonomics/recipe-marketplace.md))

### 2. Setup assembly

- baseline-relay deployed by Accordant GovOps (relay class, universal template + per-Prime config)
- stream-sentinel deployed by Ecosystem Actor (sentinel class, entart-resident loop + telart cognition)
- warden-relays engaged (minimum required number for the targeted TTS)
- All components register in Synome with the recipe identifier they're running

### 3. Activation

- Setup begins operating
- stream-sentinel sends intent into baseline-relay
- baseline-relay executes within RTI (or falls back to Base Strategy on stream disconnect)
- warden-relays monitor continuously, re-derive in parallel

### 4. Ongoing operation

- Continuous trading within RTI
- Periodic settlement and carry distribution per recipe payment terms
- warden-relay attestations logged to Synome
- Counterfactual simulation runs in parallel for carry attribution

### 5. Termination

Triggers:
- Accord expiration
- Mutual agreement
- Breach of terms (slashing per recipe)
- Governance intervention
- warden-relay-triggered halt (if not resolved)

---

## Connection to Laniakea Infrastructure

### PAU pattern

The baseline-relay operates a PAU within governance-approved bounds:

- baseline-relay holds pBEAMs granted via the BEAM cascade — see [`../smart-contracts/configurator-unit.md`](../smart-contracts/configurator-unit.md)
- Rate limits constrain maximum velocity
- SORL (25%/18h) constrains rate limit increases — see [`../smart-contracts/rate-limit-attacks.md`](../smart-contracts/rate-limit-attacks.md)

### Execution Engine

The Execution Engine is the component that actually holds pBEAMs and signs transactions:

- Held only by baseline-relay (or principal-sentinel in principal-control mode)
- Subject to warden-relay freeze authority via `gate-out (halt-baseline …)`

### Synome integration

The operating setup interacts with Synome for:

- Counterfactual simulation logging (baseline-relay)
- Warden attestation storage (warden-relays)
- Carry calculation inputs (synserv computation over book state)
- Setup status tracking (the `(beacon-status … active)` atom that wardens can retract)

---

## Open architectural questions

- **Principal-sentinel internal structure** — exact wiring of cognitive control + bundled relay + local govops bundle. Deferred.
- **Sentinel synodoxics treatment** — proper conceptual home for sentinel as a beacon class (trust model, governance criteria for instantiation, structural constructor). Tracked in [`../summaries/clean-todo.md`](../summaries/clean-todo.md) as part of the broader beacon-class conceptual treatment open question.

---

## Summary

> Sentinels are the action class with cognitive call-out density. Two variants: stream-sentinels (ecosystem actors proposing intent into a Prime's baseline-relay) and principal-sentinels (folio owners with bundled cognition + direct PAU control). Both require independent warden-relays for safety. Sentinels are not in Phase 1; this is forward-looking architecture.

### Key principles

1. **Sentinels are the cognitive action class** — relays handle deterministic action; sentinels have call-out density into operator telart.
2. **No "sentinel formation" anymore** — what existed as Baseline/Stream/Warden becomes baseline-relay + stream-sentinel + warden-relay(s), with three distinct classes (relay, sentinel, relay).
3. **Streaming Accord governs stream-sentinel ↔ baseline-relay** — the recipe instance that prices intent flow and carry.
4. **TTS measures safety** — warden-relay tick + re-derive latency + halt propagation. Call-out latency drops out vs legacy model.
5. **Independence is structural** — warden-relays must be operated by independent parties.
6. **Compounding within bounds** — streams enable intelligence accumulation; synomic constraints prevent catastrophic outcomes.
7. **Not in Phase 1** — Phase 1 has only relays, govops-controlled, no AI logic.

---

## Related Documents

| Document | Relationship |
|---|---|
| [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) | Canonical beacon taxonomy (six classes); relay vs sentinel split |
| [`../noemar-synlang/synlang-patterns.md`](../noemar-synlang/synlang-patterns.md) | §5 call-out primitive; §6 sentinel/relay patterns (canonical home) |
| [`../noemar-synlang/runtime.md`](../noemar-synlang/runtime.md) | §11.6 call-out primitive; cert/auth chain |
| [`../noemar-synlang/topology.md`](../noemar-synlang/topology.md) §9 | Space + beacon naming convention |
| [`../synoteleonomics/recipe-marketplace.md`](../synoteleonomics/recipe-marketplace.md) | Streaming Accord as recipe instance |
| [`../risk-framework/operational-risk-capital.md`](../risk-framework/operational-risk-capital.md) | ORC sizing |
| [`../risk-framework/sentinel-integration.md`](../risk-framework/sentinel-integration.md) | Risk framework cross-refs |
| [`../synomic-entities/folio.md`](../synomic-entities/folio.md) | Folio integration: principal vs automated |
| [`../synomic-entities/prime.md`](../synomic-entities/prime.md) | Prime context |
| [`../smart-contracts/configurator-unit.md`](../smart-contracts/configurator-unit.md) | BEAM cascade |
| [`../smart-contracts/rate-limit-attacks.md`](../smart-contracts/rate-limit-attacks.md) | Rate limit / SORL / IRL calibration |
| [`../summaries/clean-todo.md`](../summaries/clean-todo.md) | Open: beacon-class conceptual treatment |
