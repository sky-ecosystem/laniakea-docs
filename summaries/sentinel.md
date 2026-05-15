# Sentinel

**Status:** forward-looking — sentinels are not in Phase 1 scope. P1 has only relays (deterministic, govops-controlled). This summary describes the architecture for when ecosystem actors with proprietary intelligence and folios under principal control come online.
**Canonical home:** `laniakea-docs/sentinel/`

---

## TL;DR

Sentinels are the **action class with cognitive call-out density** in the Laniakea beacon taxonomy. They split into two variants — **stream-sentinels** (ecosystem actors proposing intent into a Prime's baseline-relay) and **principal-sentinels** (folio owners with direct PAU control + bundled relay + local govops). What was previously called a "sentinel formation" (Baseline / Stream / Warden) is now three different classes: baseline-relay (deterministic strategy execution), warden-relay (deterministic halt monitor), and stream-sentinel (the only true sentinel — has cognitive call-outs). Streaming Accord governs stream-sentinel ↔ baseline-relay; carry math runs against a deterministic counterfactual. TTS = warden tick + synart re-derive + halt propagation (no call-out term anymore, since warden is deterministic). ORC = Rate Limit × TTS, posted by Guardian.

## Section map

| § | Topic |
|---|---|
| §1 | What sentinels are (vs relays) |
| §2 | Class variants (stream-sentinel / principal-sentinel) |
| §3 | The operating setup (baseline-relay + warden-relays + stream-sentinel) |
| §4 | TTS and ORC economics |
| §5 | Streaming Accord (RTI, carry, compounding loop) |
| §6 | Principal-sentinels |
| §7 | Folio integration |
| §8 | Where sentinel Spaces live |
| §9 | Naming conventions and identifiers |
| §10 | Verification via grounded chain-read primitive |
| §11 | Setup lifecycle |
| §12 | Connection to PAU / BEAM / Synome |

---

## §1 What sentinels are

A sentinel is a **high-authority action beacon with call-out density into operator telart**. Strategy involves designated cognitive call-outs (LLM, classifier, scorer); strategy bounds and envelope-check code live in synart (auditable); cognitive content is non-deterministic and private (verifiable only by output-shape conformance and provenance).

The load-bearing distinction is **relay vs sentinel**:

| Class | Cognition | Strategy location | Verifiability |
|---|---|---|---|
| relay | none | universal synart template at `&core.loop.relay.<stem>` | full — any warden re-runs same code |
| sentinel | call-out density | per-entity Space in entart (no universal template) | bounds + envelope verifiable; cognitive output verified only by shape + provenance |

The legacy "sentinel formation" (Baseline / Stream / Warden) was three roles bundled into one subclass. The post-noemar architecture splits them:

| Legacy role | New class | Why |
|---|---|---|
| Baseline (~95% synart, 5% call-out) | **relay** (stem `baseline-`) | Deterministic strategy is fully synart-resolvable post-noemar; no real cognitive density |
| Warden (~95% synart, 5% call-out) | **relay** (stem `warden-`) | Verify+halt is also deterministic synart re-derivation via grounded chain-read primitive |
| Stream (~10% synart, 90% call-out) | **sentinel** (variant stream) | Genuinely requires local cognition for intent proposal |
| Principal (varies) | **sentinel** (variant principal-sentinel) | Direct PAU control by single operator with discretionary cognition |

## §2 Sentinel variants

| Variant | Operator | Authority over PAU | Bundled with |
|---|---|---|---|
| **stream-sentinel** | Ecosystem actor (proprietary intelligence) | None — proposes intent within bounds; no PAU keys | A separately-operated baseline-relay executes |
| **principal-sentinel** | Folio principal | Direct — operates PAU directly with cognitive call-outs | Bundled relay + local govops over its own folio |

stream-sentinels are the more common pattern at Prime scale — an ecosystem actor (proprietary trading firm, research tel) brings cognition; the Prime's baseline-relay executes deterministically within RTI. Principal-sentinels are for folio principals who want direct control plus their own cognition.

## §3 The operating setup

What replaces "sentinel formation" is **Prime operating setup** — a baseline-relay + zero-or-more stream-sentinels + ≥1 warden-relays, all wired to one PAU:

| Component | Class | Synart share | Call-out share | Holds PAU keys? |
|---|---|---|---|---|
| `baseline-{prime}` | relay | 100% | 0% | Yes (pBEAM) |
| `warden-{prime}-{op}` × N | relay | 100% | 0% | No (freeze authority only) |
| `stream-{prime}-{actor}` | sentinel | ~10% | ~90% | No (proposes intent) |

```
stream-sentinel (cognition; private)
       │
       │ intent within RTI
       ▼
baseline-relay (deterministic; PAU keys)
       │
       │ chain tx
       ▼
chain state (readable by anyone via (chain-read …))
       ▲
       │ re-derive
       │
warden-relay × N (independent operators; deterministic)
       │
       ▼
agree → continue / disagree → freeze BEAM
```

**Why the separation:**
- baseline-relay → all execution flows through public deterministic synart code
- stream-sentinel → proprietary intelligence influences execution without exposing strategy or holding keys
- warden-relay → independent deterministic re-derivation; halt authority on divergence

Inter-component communication is synart-defined (`gate-out (emit-to-baseline …)`, `gate-out (freeze-beam …)`); no out-of-band coordination.

**Independence requirement:** warden-relays MUST be operated by distinct parties from each other and from baseline-relay operator. Independence is what makes multiple wardens multiplicative rather than additive.

## §4 TTS and ORC

**Time to Shutdown (TTS)** prices safety in the operating setup — worst-case window between baseline-relay doing something wrong and a warden-relay halting it.

```
TTS = (warden tick interval) + (warden synart re-derive latency) + (halt propagation)
```

Each component has a measurable bound. **Note:** the call-out-latency term that the legacy formation model carried is gone, because warden-relays don't do call-outs — they're deterministic. Stream-sentinel call-out latency doesn't enter TTS because the baseline's RTI check enforces bounds regardless.

During the [0, TTS] window, a compromised baseline can damage at most `Rate Limit × TTS`. The Guardian (Ozone) posts:

```
Required ORC ≥ Rate Limit × TTS
```

**Readings:** for Primes with fixed rate limits → better wardens → lower TTS → less ORC. For the system, safety is priced in, not externalized. **TTS determinants:** number of independent warden-relays, operator diversity, monitoring latency, halt propagation speed, warden certification.

ORC calibration (IRL/SORL × Type 1/Type 2 attacks) lives in `risk-framework/operational-risk-capital.md` and `smart-contracts/rate-limit-attacks.md`.

## §5 Streaming Accord

Governs **stream-sentinel ↔ baseline-relay** — a recipe instance in the marketplace. Canonical recipe shape in `synoteleonomics/recipe-marketplace.md`.

**Components:** Risk Tolerance Interval (RTI — position / velocity / concentration limits, prohibited actions); Performance Fee Ratio; Termination conditions; Dispute resolution.

**Carry math:**
```
Carry = (Actual PnL − Counterfactual Baseline PnL) × Performance Fee Ratio
```
Underperformance → zero carry. Counterfactual computed by baseline-relay running its deterministic Base Strategy in simulation in parallel with live operation.

**Compounding loop (the core economic claim):** `Public capital → Private intelligence → Better streams → More carry → More intelligence`. Carry is private — accrues to the operating teleonome and can be reinvested into proprietary capability. Bounded by: public deterministic baseline-relay execution, independent warden-relays with halt authority, rate limits + ORC, governance revocability.

**Intra-coalition asymmetry regulated** by three structural features: (1) streams are Halos (public capital stays synomic; only carry compounds privately), (2) Fortification Conserver regulates accumulated power signals, (3) Conserver must remain defeatable by the rest of the aligned coalition.

## §6 Principal-sentinel

Direct-control sentinel without a separately-operated baseline-relay. Used for folios under principal control where one competent operator wants direct PAU control plus their own cognition.

Bundles three things into one identity:
1. **Cognitive control** — call-outs into principal's telart for discretionary intent
2. **Bundled relay** — direct PAU operation (pBEAM holdership, tx signing)
3. **Local govops** — folio-scoped governance

Trade-offs vs the stream-sentinel + baseline-relay + warden-relay setup: no separately-operated baseline (no fallback Base Strategy on cognition failure); no independent wardens (self-accountable); no formation-level ORC (principal bears own risk); rate limits are sole on-chain constraint; proprietary algorithms throughout. Expected users: companies that already run stream-sentinels elsewhere — they have infra and algorithms to operate autonomously. PAU still provides structural protection (rate limits, audited contracts); formation-level protections absent.

**Open: internal structure** — exact wiring of cognition + bundled relay + local-govops bundle deferred. Class is positioned in the taxonomy; concrete pattern TBD.

## §7 Folio integration

Folios are user-facing capital-deployment surfaces — each is a PAU operated by either an automated setup or a principal-sentinel.

| Mode | Operator | Pattern |
|---|---|---|
| **Automated folio** | baseline-relay (`baseline-{folio}`) + optional stream-sentinel (`stream-{folio}-{actor}`) + warden-relays | Principal writes directive → setup executes within directive bounds |
| **Principal control folio** | principal-sentinel (`principal-{owner}`) | Principal operates PAU directly with cognitive call-outs |

Directive bounds for automated folio are the folio analogue of the RTI in a Streaming Accord. See `synomic-entities/folio.md`.

## §8 Where sentinel Spaces live

Sentinels have **no universal synart template** — strategy is per-operator and cognitive content is private. Sentinel loop bodies live in the entart of the entity they operate on:

| Sentinel | Entart Space |
|---|---|
| stream-sentinel for Spark | `&entity.prime.spark.sentinel.{actor}` |
| principal-sentinel for a folio | `&entity.folio.{owner}.sentinel-principal` |

The entart-resident Space holds bounds, gate-out shape, call-out registry pointers, and envelope-check synart code. The cognitive call-outs resolve to services in the operator's telart agart, off-corpus.

Relays, by contrast, have universal synart templates at `&core.loop.relay.<stem>` plus per-entity config in entarts (e.g., `&entity.prime.spark.relay.baseline`). Relays standardize; sentinels are per-operator.

## §9 Naming conventions

Beacon identifiers: `<stem>-<owner>[-<disambiguator>]` (dash-separated, no sigil; see `macrosynomics/beacon-framework.md` §9).

| Stem-owner pattern | Class | Variant |
|---|---|---|
| `baseline-{prime}` / `baseline-{folio}` | relay | — |
| `warden-{prime}-{operator}` / `warden-{folio}-{operator}` | relay | — |
| `stream-{prime}-{actor}` / `stream-{folio}-{actor}` | sentinel | stream |
| `principal-{owner}` | sentinel | principal-sentinel |
| `lcts-{halo}`, `nfat-{halo}`, `amm-{halo}` | relay (NOT sentinel) | — |
| `auction-{x}`, `council-{x}`, `identity-{net}`, `rate-{gen}` | relay | — |

**Legacy mappings:**

| Old | New |
|---|---|
| `stl-base-{prime}` | `baseline-{prime}` (relay) |
| `stl-warden-{prime}-{op}` | `warden-{prime}-{op}` (relay) |
| `stl-stream-{prime}-{actor}` | `stream-{prime}-{actor}` (sentinel) |
| `stl-principal-{owner}` | `principal-{owner}` (sentinel) |
| `lpha-lcts/nfat/amm-{halo}` | `lcts/nfat/amm-{halo}` (relay) |

## §10 Verification via grounded chain-read primitive

Cross-checking positions against risk limits, computing per-risk-type CRRs / RRC / TRRC / ER, calculating PnL and carry — these are synserv computations over book spaces, not jobs for dedicated beacons. synserv runs synart-resolved calculation against current input atoms + the grounded chain-read primitive for live mainnet state.

Wardens use the same computation surface for re-derivation: a warden-relay re-runs baseline-relay's deterministic strategy by calling `(chain-read …)` itself and applying the same synart code. Divergence past tolerance triggers BEAM freeze.

Because endoscraper is now a grounded primitive (not a beacon class), there's no separately-operated scraper to disagree with. The runtime primitive IS the canonical source; wardens calling it get the same answer as synserv.

## §11 Setup lifecycle

Principal-sentinels skip this entirely. The lifecycle below applies to stream-sentinel + baseline-relay + warden-relay setups.

1. **Accord negotiation** — Ecosystem Actor proposes; RTI / fee ratio / slashing negotiated; accord deployed as recipe instance.
2. **Setup assembly** — baseline-relay by Accordant GovOps; stream-sentinel by Ecosystem Actor; warden-relays engaged (≥ min for targeted TTS); all register in Synome.
3. **Activation** — stream-sentinel sends intent; baseline-relay executes within RTI (falls back to Base Strategy on stream disconnect); warden-relays monitor and re-derive in parallel.
4. **Ongoing** — continuous trading within RTI; periodic settlement and carry distribution; warden attestations logged; counterfactual simulation parallel for carry attribution.
5. **Termination** — accord expiration, mutual agreement, breach (slashing), governance intervention, warden-triggered halt.

## §12 Connection to PAU / BEAM / Synome

- **PAU pattern** (Controller + ALMProxy + RateLimits): baseline-relay holds **pBEAMs** granted via the BEAM cascade (`smart-contracts/configurator-unit.md`); rate limits cap velocity; **SORL** (25%/18h) constrains rate-limit increases.
- **Execution Engine** = component that holds pBEAMs and signs txs. Held only by baseline-relay (or principal-sentinel). Subject to warden-relay freeze via `gate-out (freeze-beam …)`.
- **Synome integration:** counterfactual simulation logging (baseline-relay), warden attestation storage, carry inputs (synserv over book state), setup status tracking via `(beacon-status … active)` atom that wardens can retract. Retracting that atom is the on-chain effect of a warden halt.

---

## Key vocabulary

- **Sentinel** — Action class with cognitive call-out density into operator telart. Two variants: stream and principal-sentinel.
- **Stream-sentinel** — Sentinel variant: ecosystem actor proposes intent into baseline-relay; no PAU keys.
- **Principal-sentinel** — Sentinel variant: folio owner with direct PAU control + bundled relay + local govops.
- **Relay** — Action class without cognition; deterministic synart-resolved I/O. Absorbs former Baseline + Warden + executor + relayer.
- **Streaming Accord** — Recipe instance governing stream-sentinel ↔ baseline-relay; RTI, performance fee, slashing, termination, dispute resolution.
- **RTI (Risk Tolerance Interval)** — Off-chain behavioral envelope enforced by baseline-relay.
- **TTS / ORC** — Time to Shutdown and Operational Risk Capital (= Rate Limit × TTS), posted by Ozone Guardian.
- **Execution Engine** — Holds pBEAMs and signs PAU txs; uniquely held by baseline-relay (or principal-sentinel).
- **Carry** — `(Actual PnL − Counterfactual Baseline PnL) × Performance Fee Ratio`; private, accrues to operating teleonome.

## Cross-references

- `noemar-synlang/synlang-patterns.md` §5–§6 — Canonical home for relay/sentinel patterns and the call-out primitive.
- `macrosynomics/beacon-framework.md` — Canonical beacon taxonomy; six-class system; relay vs sentinel split; in-space calculation surface (§4).
- `synoteleonomics/recipe-marketplace.md` — Streaming Accord as recipe instance.
- `risk-framework/operational-risk-capital.md`, `risk-framework/sentinel-integration.md` — ORC sizing and risk-framework cross-refs.
- `smart-contracts/configurator-unit.md`, `smart-contracts/rate-limit-attacks.md` — BEAM cascade; IRL/SORL calibration.
- `synomic-entities/folio.md`, `synomic-entities/prime.md` — Folio (principal vs automated), Prime context.
- `noemar-synlang/runtime.md` §11.6 — Call-out primitive; cert/auth chain.
- `noemar-synlang/topology.md` §9 — Space + beacon naming convention.
- `summaries/clean-todo.md` — Open: beacon-class conceptual treatment for sentinel / relay / market-data / attest-data.

## File map

| File | What's in it that the summary doesn't have |
|---|---|
| `sentinel-network.md` | Full canonical text: ASCII diagrams of the operating setup, verbatim "Why the separation" rationale per role, full lifecycle stage descriptions with trigger lists, the explicit "Verification" section explaining grounded chain-read primitive, naming convention with legacy mapping, and the summary at the bottom. |
