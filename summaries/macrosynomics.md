# Macrosynomics

**Status:** Mixed — 5-layer model + Atlas/Synome split + beacon framework are live commitments; sentinel formations and topology-layering meta-architecture are target. Phase 1 reality is narrower (see `roadmap/`).
**Canonical home:** `laniakea-docs/macrosynomics/`

---

## TL;DR

Macrosynomics defines what the synome **is** as a structural object: a five-layer architecture (Synome → Synomic Entities → Teleonomes → Embodiments → Embodied Agents) hosting public ledger-native Synomic Entities operated by private teleonomes through regulated apertures (beacons). Canonical home for: (a) the 5-layer model + artifact tiers, (b) the Atlas/Synome separation (constitutional human-readable Atlas embedded as a root node in the machine-readable Synome) including the governance-window framing, (c) the beacon taxonomy (authority tier load-bearing; I/O role under it; BEAM hierarchy on chain side), (d) the Synomic Entity rank hierarchy and "power through integration" thesis with the right-to-exist principle, and (e) the four-layer topology stratification (telos → axioms → topology → population) with probmesh as transverse alignment-argument substrate. Pair with `synodoxics/` (knowledge dynamics) — together they form the dual architecture.

## Section map

| § | Topic |
|---|---|
| 1 | Five layers + artifact tiers |
| 2 | Dual architecture |
| 3 | Atlas/Synome separation |
| 4 | Synomic Entities — power through integration |
| 5 | Beacon framework |
| 6 | Sentinel formations |
| 7 | Topology layering meta-architecture |
| 8 | Self-hosting + invariants |

---

## §1 Five layers + artifact tiers

| Layer | Content | Artifact |
|---|---|---|
| 1 Synome | Atlas, Language Intent, Synomic Axioms, Synomic Library | synart (replicated identical) |
| 2 Synomic Entities | Sky Superagent, Effectors, all entity types | synart |
| 3 Teleonomes | Teleonomic Directive+axioms, Library, Dreamarts, Embodiment Interface, Resource Register | telart (per-teleonome) |
| 4 Embodiment | Local Data, Orchestrator, Resources | embart (per-embodiment) |
| 5 Embodied Agent | Beacons, Hardware Control, Resources | ephemeral |

**Local Data ≠ embart**: Local Data is raw observation logs; embart is the curated structured probabilistic projection derived from them.

**Embodiment power levels** (constrains beacon profile, not classification): Light (legal/economic endpoints, keepers) / Medium (sentinel formations, P2P trade) / Heavy (deep cognition, dreamers, full teleonome host). Dreamers run on heavy; actuators on light-to-medium.

**Human interface pattern**: every level has a directive (Atlas / Agent Directive / Teleonome Directive) translated through a single trusted Language Intent layer grounded by the Synomic Library. Single translator chosen for cryptographic root-of-trust reasoning. Directive overrides voice commands; persistent friction triggers a costly governance-approved directive update. Bootstrapping vulnerability (Library + Language Intent co-constitute) is acknowledged as the deepest known risk and answered by concentrating maximum scrutiny on a single visible point rather than distributing it across multiple under-defended translators.

**Extra-synomic data**: pointers stored in synome to live volatile data (sentinel DBs, raw feeds); summarized into synome at settlement intervals.

## §2 Dual architecture

Sparse **deontic skeleton** (axioms, governance, authority — `(1,1)` once set) surrounded by dense **probabilistic mesh** (knowledge with `(strength, confidence)` truth values, evidence flow, ossifying patterns, RSI). Governance sits at the **crystallization interface** consuming probabilistic evidence and producing deontic commitments. Two-type framing is pedagogical — synodoxics treats them as endpoints of a continuous spectrum. Primary security threat: cancer-logic, countered by synomic inertia.

## §3 Atlas/Synome separation

**Problem:** original Atlas (~364k words) tried to be both human-readable constitution and comprehensive machine spec. **Solution:** split.

| Aspect | Atlas | Synome |
|---|---|---|
| Audience | Humans (stakeholders, voters) | Machines (beacons, sentinels, synserv) |
| Size | ~10–20 pages target | Unbounded |
| Content | Spirit, governance, primitives, principles | Addresses, rate limits, BEAM params, settlement formulas, transaction logs |
| Modification | Governance vote | Atlas-conforming operations |

Atlas is **embedded IN** the Synome as a root node, not external to it. Atlas describes WHAT must be true (verification assertions); Synome encodes HOW (constraints checked by sentinels and synserv). Verification model: Atlas assertion → Synome constraint (e.g., `"ER ≤ 90%"` → `∀ prime: prime.RRC / prime.TRC ≤ 0.90`). Independent vs initial calculation tolerance: ≤1% Agreed (auto), >1% Disputed (Core GovOps resolves; Prime can post Dispute Notice within 5 days).

**Mini-Atlas fractal pattern**: every level with human stakeholders gets a human-readable summary (Sky Atlas → per-Prime mini-Atlas → Halo docs → Unit docs). Described architecturally in macrosynomics — generic placeholders for the per-Prime human-readable summary derived from each Prime's Agent Artifact, with Root Edit governance configured per Prime. Concrete operational content (SubProxy addresses, Core Operator Multisig, per-chain deployments, Primes-needing-Mini-Atlas tables, standardized Root Edit parameters) lives in `synomic-entities/` and per-Prime mini-Atlas docs.

**Governance window** (canonical here): humans pass through regimes — meaningful participation → informed oversight → ceremonial governance → beneficiary status. The window's special property is not that humans are sole decision-makers (governance is already capital-weighted decisions by token holders including teleonomes and entities), but that humans can still meaningfully *evaluate* what they're voting on. Atlas is the CEV vessel locking in values while that evaluation capability exists.

## §4 Synomic Entities — power through integration

A Synomic Entity is ledger-native, durable, public — woven *into* the synome rather than constrained from outside. Safety is structural, not behavioral: identity, assets, actions, and accountability are all synome-native. Failure modes (bugs, bad axioms, governance capture, beacon vulnerabilities) remain real, but the *adversarial escape* problem is eliminated. Trust equation: `Code × Synome Constraints × Human Escalation Path` — code handles 99% cheaply, escalation guarantees 1% gets sensible outcome.

**Rank hierarchy** (canonical):

| Rank | Types | Governance |
|---|---|---|
| 0 | Core Council | Sovereign |
| 1 | Guardian (operationally only Ozone), Core Entity | Directly regulated by Core Council |
| 2 | Prime, Generator, Oracle Entity, Sequencer Entity, Pylon Entity | Accordant to Ozone |
| 3 | Halo, Folio | Administered by a Prime |

**Core Entity** is now a single rank-1 umbrella type covering both legacy-asset management (Morpho, Aave, SparkLend positions under direct Core Council governance) and crisis-wrapper roles (temporary takeover when a Guardian collapses, dissolved after resolution). The previous CCE / Recovery Entity split is collapsed.

**New rank-2 entity types** (operational infrastructure, not capital allocators):
- **Oracle Entity** — owns a data domain (market data or attestation) and certs its own oracle beacons; tokenless. Provides trusted data atoms that Primes/Halos/sentinels consume.
- **Sequencer Entity** — runs orderbook matching as a regulated venue and **hosts Rings as sub-structures inside its entart**. Trusted to sequence orders without frontrunning. **No collateral, no slashing, no participation in any loss waterfall** — trust enforcement is purely revocability-based (Core Council retirement on misbehavior; synomic registry as audit trail; Oracle-Entity audit). Operational-harm recourse beyond revocation escalates to Core Council governance, not on-chain financial slashing.
- **Pylon Entity** — CME clearing-member-style broker-dealer that bears principal positions in derivatives, faces Primes/Folios as customers, and mutualizes peer-default risk via **Ring coalitions** (an inter-Pylon accord pattern hosted inside a Sequencer's entart, *not itself an entity*). Three-layer capital: Sky regulatory minimum (entity-viability floor) + voluntary extra capital (absorbs own customer-default residuals; shielded from Ring mutualization) + per-Ring pledges (system-recognized loss-absorbing capital). Replaces perpetual-exchange ADL with pre-funded mutualization + VMGH winner-haircut. Rings are product configurations, not entities — created/retired at product cadence; Pylons may have criss-cross memberships across Rings and Sequencers; cross-margin offset between Rings is a Pylon-level commercial product. Regulation operates upstream via Prime CRR on Ring-issued units (the risk-treatment equation reads Ring health attestations).

**Spectrum of purpose**: minimal Halo (no token, no owner, exists to experience) → governed Halo → Prime (mega allocator). Same entity can combine governance + autonomous claims + inalienable capital rights. Joint-stock-like properties with code-woven (not legally promised) constraints + escalation path to human reasonableness. Folios are rank-3 standardized supply-side holding structures controlled by a single principal — distinct from Halos, which wrap legal entities.

**Right-to-exist principle** (canonical here): an aligned, self-sustaining Synomic Entity has a moral right to exist; forcible shutdown is the synomic equivalent of killing. "Aligned" requires conformity with Atlas universal alignment obligations, not just narrow compliance — an entity exploiting its axioms to extract value is compliant but misaligned. Negative rights trump positive: capital exhaustion = natural death. Inalienable capital claims are the material expression of this right. Governance can revoke beacons (restrict action) but cannot forcibly terminate an aligned, economically viable entity. For the full ethical framing, see `synoteleonomics/emergence.md`.

**Halos as fractal layer**: Class (Portfolio / Term / Trading) → Book (balanced ledger within class) → Unit (cross-book link). Halos proliferate; each is an Entity with its own artifact.

**Three-phase lifecycle**: Creation (artifact woven into synome; initial state, claims, rights encoded; may inherit assets from a superseded entity) → Operation (acts through beacons, accumulates state, generates/distributes value, governance can update parameters within encoded constraints) → Termination (some terminate naturally — e.g., crisis-wrapper Core Entities once the crisis resolves; some persist indefinitely; wind-down follows encoded rules; inalienable claims may prevent involuntary termination). **Entities do not transform** — entity identity is immutable. To change behavior beyond what encoded parameters allow, create a new entity and transfer assets into it rather than mutating the existing one.

**Stream regulation (intra-coalition asymmetry)**: streams compounding loop (`public capital → carry → private intelligence → better streams`) is regulated by three structural features: (1) streams ARE Halos (capital is synomic; only carry compounds privately), (2) Fortification Conserver regulates accumulated power signals, (3) Conserver itself must remain defeatable by the rest of the aligned coalition.

## §5 Beacon framework

**Definition:** a beacon is a synome-registered, enforceable action aperture. Not an entity, not a teleonome, **not a calculator**. Three functions: operate Synomic Entities, enable peer-to-peer teleonome interaction, provide detection/visibility.

**Single load-bearing axis: authority tier.**

| Tier | Definition |
|---|---|
| **High authority** | Cert + auth-scoped; operates a Synomic Entity |
| **Low authority** | Passive observation OR direct teleonome-to-teleonome; no Entity operation |

**Power-as-axis retired.** Cognition migrated into synart-resolved in-space computation, so beacons no longer carry decision logic — they witness, sign, submit. Embodiment power still constrains profiles but doesn't classify beacons.

**I/O role under authority** (working cut, non-prescriptive):

| Role | Classes |
|---|---|
| Input (push data atoms) | **market-data-beacon** (Oracle-Entity-admin'd off-chain market data — price/liquidity/funding ticks; lands at the Oracle Entity entart root) / **attest-data-beacon** (Oracle-Entity-admin'd signed off-chain claims about exobook state; lands inside specific exobook Spaces) / **patch-beacon** (govops-sudoed scaffold; the one input class **without a regulated framework**). Endoscraper is no longer a class — chain reads are a grounded runtime primitive accessible from any rule. |
| Action (emit chain txs from synart state) | `relay` (narrow per-target, deterministic) / `sentinel` (call-out density into operator telart; variants stream / principal). Sentinel formations bundle baseline-relay + warden-relay + stream-sentinel as one operating setup. |

**Three new input beacon classes** replace retired `oracle` / `oracle-exsyn` / `attestor`. Market-data-beacons and attest-data-beacons differ in where atoms land (Oracle Entity entart root vs specific exobooks) and trust model (provider redundancy/dispute vs slashing-time verification). **Patch-beacons** are the one input class **without a regulated framework** — Guardian-sudoed, govops-certed, loop body + per-entity config sudoed inline at genesis. They scaffold over insyn coverage gaps (Phase 1: per-Prime exsyn-TRRC writes into each `&entity.prime.{id}.primebook`, replacing `oracle-exsyn`); designed to sunset as use cases migrate to insyn-native, but reusable for future scaffolds of this nature. Trust borne by govops directly. Instance identifiers were renamed in tandem with the class taxonomy: `oracle-{provider}` → `market-data-{provider}`, and `attestor-{class}` → `attest-data-{class}`.

**In-space calculation invariant**: derived state (equity, CRR, ER, matching status, breach flags, encumbrance) in any book is a deterministic function of current input atoms; synserv runs synart-resolved code to keep it current. Three consequences: (1) full warden re-derivation, (2) beacons become pure I/O, (3) no lag. Implementation mechanism (event-driven / heartbeat / hybrid) deferred to Phase 1.

**BEAM hierarchy** (chain-side, orthogonal to I/O role):

| BEAM | Holder | Capability |
|---|---|---|
| pBEAM | Relay (deterministic keeper) | Direct execution within rate limits |
| cBEAM | Relay (deterministic keeper) | Set rate limits (within SORL), onboard targets |
| aBEAM | Council Beacon (governance) | Register PAUs, approve inits, grant cBEAMs (14-day timelock for grants; revocations instant) |

**Naming**: legacy `lpla / lpha / hpla / hpha` prefixes are retired except on the kept peer-to-peer `hpla-{trade|arb|coop}-…` identifiers. Endoscraper is now a grounded runtime primitive (`(chain-read …)`), not a beacon class. Patterns: `market-data-{domain}-{provider}` (instance of `market-data-beacon`), `attest-data-{halo-class}` (instance of `attest-data-beacon`), `patch-{target}` (govops-sudoed; e.g., `patch-{prime}` for exsyn-TRRC), per-Halo relays `lcts-{halo}` / `nfat-{halo}` / `amm-{halo}` / `identity-{network}` / `auction-{x}` / `rate-{generator}` (class: relay), governance relays `gov-{x}` and `council-{x}` (class: relay), per-Prime relays `baseline-{prime}` and `warden-{prime}-{op}` (class: relay), per-Prime sentinels `stream-{prime}-{actor}` and `principal-{owner}` (class: sentinel), `ctl-…` (controllers), `cst-…` (custodians). **`lpla-checker` disappears** as a beacon class — verification is synserv-run synart code.

**Multi-beacon reality**: a teleonome may operate many beacons without revealing they are linked; aggregation only required at risk thresholds.

## §6 Sentinel formations

Distinguished high-authority *action* subclass with continuous real-time control. Operationally dominant because they act faster than synomic governance.

| Formation | Role | Plane |
|---|---|---|
| **Baseline** | Real-time strategy loop, moves capital/state continuously | Data plane (direct execution) |
| **Stream** | Continuous data ingestion, feature extraction, signal generation | Control plane (no direct execution; feeds Baseline) |
| **Warden** | Independent monitoring + risk enforcement; freeze/halt/escalate | Safety plane (override only) |
| **Principal** | Owner-operated direct control of folio agents or standalone accounts | Outside formation pattern |

Streams are the highest-leverage Teleonome activity (carry compounds private intelligence); regulated per §4. Phase 1 has no full sentinel formations — only relays controlled manually by govops; the Baseline / Stream / Warden bundle activates from Phase 9 (per-Prime `baseline-{prime}` relay deploying alongside `warden-{prime}-{op}` relays and `stream-{prime}-{actor}` sentinels) for OSRC + Duration auctions. Canonical formation spec: `trading/sentinel-network.md`.

## §7 Topology layering meta-architecture

Four-layer stratification: 3 rigid + 1 variable, plus probmesh as transverse substrate. Topology atom-set not yet drafted.

```
TELOS      — what the system is for                     (sudo only; ideally externally fixed)
AXIOMS     — invariants flowing from telos              (sudo only; rare)
TOPOLOGY   — archetypes, connections, constructors      (sudo only by design; no meta-constructors)
POPULATION — concrete instances, atoms, events          (constructor-mediated, validated)
PROBMESH   — alignment-argument substrate; crisscrosses all four
```

**Two atom classes, one substrate**: topology atoms (`(space-archetype …)`, `(connection …)`, `(constructor-def …)`) live in `&core.meta-topology`; population atoms in entart tree + universal layers. Distinguished by predicate head, not storage. **Validation is total** — gate refuses non-conforming writes.

**Sudo = arbitrary atomspace mutation**, the only path to change rigid layers. Bypasses gate + constructor validation by definition. Sudo events are flag-day events: audit, rationale referencing probmesh content, run in shadow frame first → observed → promoted to canonical, ratified, archived. Posture: **freeze topology after focused design pass**, treat all subsequent change as sudo-as-amendment.

**Frames**: canonical frame (live, what synserv writes) + arbitrary shadow frames (forks at settlement boundaries for prediction/testing/forecast/sudo dry-runs). Operations: `frame-fork`, `frame-rebase`, `frame-diff`. Forecast model becomes a shadow-frame configuration.

**Probmesh as alignment-argument substrate** — every probmesh atom is implicitly a chain: observation → claim about telos-service → reference to topology/axioms → graded verdict. Two failure modes the probmesh distinguishes: population misalignment (fix within topology) vs topology/axiom insufficiency (fix is sudo proposal). Architectural teeth: a teleonome with arbitrary intelligence has only two channels — population action (rate-limited, reversible) or probmesh argument (public, debatable, requires ratification for topology changes). Argumentation gets harder to fake as scrutiny scales.

**Phase deliverables = topology atom-sets**: each phase ships a topology delta. Phase completion becomes a queryable predicate ("does actual topology match phase-N declared topology?"). Infrastructure-as-code applied to a synome.

**Comments as pre-probmesh content**: synlang comments are atoms — `(rationale-for …)`, `(invariant-comment …)`, `(serves-telos-via $atom $intermediate-purpose)`, `(open-question …)`, `(deprecated …)`. Today's structured comments → tomorrow's probmesh atoms with confidence + alternatives + opposing-argument links.

## §8 Self-hosting + invariants

**Self-hosting**: synart is also the program. Loops, gates, recipes, runtime source itself live as atoms. Same boot procedure runs synserv, beacons, sentinels, archive embs, verifier embs.

**Five levels of self-reference** (canonical home: `noemar-synlang/topology.md` §8):

1. **Self-hosting** — synart contains the loops that run synart (`&core.loop.synserv`, `&core.loop.market-data`, `&core.loop.attest-data`, `&core.loop.relay.<stem>`; per-Prime sentinel loops live in `&entity.<type>.<id>.sentinel.<actor>`).
2. **Self-regulating** — synart contains the gates that regulate synart access (`&core.syngate`, `&core.telgate`). The trust boundary is itself synart code.
3. **Self-paying** — synart contains the recipes that fund work on synart. Marketplace and substrate are the same artifact.
4. **Self-seeding** — synart contains the telseeds that birth new teleonomes (`&core.library.telseed.*`).
5. **Self-improving** — synart contains the runtime source itself (`&core.library.runtime.*`). Recipe revenue funds substrate research; substrate research lands back in synart.

Punchline: **the synome funds its own substrate research with the value it captures from substrate use** — tighter than open-source (development externally funded) or smart-contract platforms (contracts run on chains they didn't fund). You can't fork the development engine without forking the productive economy. Architectural consequence: replication of synart is replication of the running program — no separate "code distribution" channel.

**Trust model — non-repudiation, not trustlessness.** Synomic Entities are operated by regulated entities with legal accountability under governance authority. ed25519 signatures provide non-repudiation (proof of *who* acted, so liability can attach), not trustlessness. The cert chain carries real-world liability up to the Guardian. Disputes resolve via governance writing a `finding` atom that supersedes the original — there is no slashing-as-sole-recourse. Crypto becomes load-bearing later (federation, anonymous beacons, volume past governance capacity); the Phase 1–9 design does not need it.

**Blockchain analogy** (orientation aid for crypto-native readers; canonical home `macrosynomics/synome-overview.md`): chain state ↔ synome; full nodes ↔ embodiments; sequencer ↔ Core GovOps running synserv; tx ↔ signed gate message; smart contracts ↔ synlang rules; offchain workers ↔ embodiment local compute; fraud proof ↔ governance investigation (compliance officers, not slashing).

**Structural invariants**:
1. Teleonomes think; beacons act
2. Beacons are apertures, not minds
3. All enforcement bottoms out in embodiments
4. Embodiments may host many agents/beacons or none
5. Beacon sophistication is constrained by embodiment power
6. Intelligence lives privately; power enters the world only through regulated apertures

**Permanent design choices**: Directives as universal human interface; core loop (Atlas → Language Intent → Axioms → Library → Language Intent); 5-layer model; content-addressed identity; `(strength, confidence)` on all assertions; instantiation/alignment semantics; six primitive types (entity, relation, event, quantity, context, timestamp); single Language Intent translation layer; probabilistic-deontic dual architecture. Storage backend, sync transport, query language are all swappable.

---

## Key vocabulary

| Term | Meaning |
|---|---|
| **Synome** | The whole architecture; both the canonical replicated structure (synart) and the meta-machine. |
| **Atlas** | Single human-readable root node; constitutional document embedded in synome. |
| **Language Intent** | Single trusted translator from human directives to machine constraints. |
| **Synomic Axioms** | Hard deontic rules instantiating Sky Superagent. |
| **Synomic Library** | Subset of synart: verified knowledge + tools + telseeds + best practices + meta-strategies. |
| **Sky Superagent** | L2 governance entity (Sky Voters + Core Council). |
| **Effectors** | L2 operational outputs (Stability / Protocol / Accessibility / Agent Primitives) instantiating entities. |
| **Synomic Entity** | Ledger-native durable entity. Rank-1: Guardian, Core Entity. Rank-2: Prime, Generator, Oracle Entity, Sequencer Entity, Pylon Entity. Rank-3: Halo, Folio. |
| **Core Entity** | Rank-1 tokenless umbrella covering legacy-asset management and crisis-wrapper roles. |
| **Oracle / Sequencer / Pylon Entity** | Rank-2 operational infrastructure (data domain / orderbook matching + Ring hosting / broker-dealer derivatives risk). |
| **Ring coalition** | Inter-Pylon mutualization accord hosted inside a Sequencer's entart (a sub-structure pattern, NOT itself an entity) — pre-funded assurance fund + VMGH winner-haircut recovery; product-configuration cadence rather than entity-creation cadence. |
| **Assurance fund** | Aggregate of member Pylons' per-Ring pledges; the Ring's mutualized default-absorption pool. |
| **Beacon** | Synome-registered action aperture; classified by authority tier + I/O role. |
| **High / Low authority** | Whether the beacon operates a Synomic Entity. |
| **market-data-beacon** | Input class admin'd by an Oracle Entity; pushes price/liquidity/funding atoms to the entity's entart root. Replaces retired `oracle`. |
| **attest-data-beacon** | Input class admin'd by an Oracle Entity; pushes signed attestations into specific exobook Spaces. Replaces retired `attestor`. |
| **patch-beacon** | Input class admin'd directly by govops via Guardian sudo; loop body + per-entity config sudoed inline at genesis. The one beacon class without a regulated framework; designed to sunset. Replaces retired `oracle-exsyn`. |
| **In-space calculation** | Synart-resolved code synserv runs to keep derived book state consistent. |
| **BEAM** (pBEAM/cBEAM/aBEAM) | On-chain authorized roles backing high-authority beacons. |
| **Sentinel formation** | Operating-setup bundle: `baseline-{prime}` (relay) + `warden-{prime}-{op}` (relay) + `stream-{prime}-{actor}` (sentinel). `principal-{owner}` (sentinel) is a separate variant for owner-operated direct control. |
| **Streaming Accord** | Recipe instance governing Baseline ↔ Stream relationships (canonical home `synomic-entities/`). |
| **Mini-Atlas** | Per-entity human-readable summary; fractal pattern. |
| **Governance window** | Current regime where humans can meaningfully evaluate the Atlas. |
| **Right to exist** | Aligned self-sustaining Entity cannot be forcibly terminated; capital exhaustion = natural death. |
| **Telos / Axioms / Topology / Population** | Four-layer meta-architectural stratification (3 rigid + 1 variable). |
| **Sudo** | Arbitrary atomspace mutation; only path to change rigid layers; flag-day event. |
| **Frame** | Concrete instance of synome state; canonical (live) or shadow (forked at settlement boundary). |
| **Probmesh (here)** | Transverse alignment-argument substrate crisscrossing all four topology layers. |

## Cross-references

- `synodoxics/probabilistic-mesh.md` — full probmesh model (dual-architecture soft side)
- `synodoxics/noemar-substrate.md` — synart/telart/embart deep treatment
- `synodoxics/security-and-resources.md` — cancer-logic, continuous self-analysis
- `core-concepts/` — atomic concept defs (five-layer-architecture, artifact-hierarchy, beacon-framework, dual-architecture, language-intent, three-pillars, telos-point, binding-mechanics, rogue-threat-model, fractal-security-pattern)
- `synomic-entities/` — per-type operational specs for every Entity type (now including Oracle / Sequencer / Pylon)
- `trading/sentinel-network.md` — full sentinel formation spec
- `smart-contracts/configurator-unit.md` — BEAM hierarchy on-chain (BEAMTimeLock → BEAMState → Configurator)
- `noemar-synlang/topology.md` — synome root, entart tree, naming convention; structural target topology-layers.md grafts onto
- `noemar-synlang/runtime.md` — gate, constructors, runtime mechanics
- `noemar-synlang/boot-model.md` — identity-driven boot, shadow execution
- `synoteleonomics/emergence.md` — full ethical framework for right-to-exist
- `synoteleonomics/synomic-game-theory.md` — coalition / rogue dynamics
- `accounting/treasury-management.md` — Fortification Conserver canonical home (referenced from `beacon-framework.md` §6)
- `risk-framework/sentinel-integration.md` — beacon ↔ risk framework calculation surface
- `noemar-synlang/topology.md` §8 — five levels of self-reference (canonical home)

## File map

| File | What's in it that the summary doesn't have |
|---|---|
| `synome-overview.md` | Full self-hosting prose; bootstrap-vulnerability framing of Language Intent (single root of trust); implementation-pathways table. |
| `synome-layers.md` | Per-layer component breakdown (Sky Voters / Core Council / Effectors enumeration; Teleonome internals — Dreamarts, Resource Register, Embodiment Interface); embodiment-power-level table; full directive-vs-voice-commands semantics; embart-vs-Local-Data-vs-ephemeral pipeline diagram; complete enumeration of structural invariants and 10 permanent design choices. Rank-2 enumeration covers Oracle / Sequencer / Pylon Entities; rank-1 covers Guardians + Core Entities. |
| `atlas-synome-separation.md` | Document-type-mapping table (Immutable/Primary/Supporting/Active Data/Budget/ICD/Precedents/Accessory → destination); BEAM-hierarchy node-shape sketches; transaction log struct; full migration phase plan; six Open Questions on Synome implementation. Rank table + inline definitions cover the three rank-2 operational types. Mini-Atlas Pattern described architecturally with generic placeholders for the fractal per-entity summary; per-Prime operational detail (SubProxy code, Core Operator Multisig, chain deployments, Mini-Atlas tables, standardized Root Edit parameters — 1% propose / 7-day review / 3-day Snapshot / 10% quorum / >50% / 2,000+ holders gate) lives in `synomic-entities/` and per-Prime mini-Atlas docs. |
| `beacon-framework.md` | Per-keeper-class table (relay stems: `lcts-{halo}` / `nfat-{halo}` / `amm-{halo}` / `identity-{network}` / `auction-{x}` / `rate-{generator}` / `gov-{x}`) with Synomic Entity + function; full BEAM ↔ PAU diagram; complete naming-convention catalog; full beacon lifecycle (Registration → Authority Envelope → Activation → Monitoring → Revocation); Controllers (`ctl-bridge/extend/connect`) and Custodians (`cst-synome/erc/vault`); legacy LPLA/LPHA/HPLA/HPHA quadrant retirement notes; legacy → current beacon-name mapping; five Phase-1-deferred open questions; intra-coalition asymmetry regulation discussion; full agent↔beacon comms-via-convention-named-embart-Space pattern. Input-beacon table enumerates three classes (`market-data-beacon` / `attest-data-beacon` / `patch-beacon`); endoscraper is no longer a class but a grounded runtime primitive. `patch-beacon` is the one class without a regulated framework — Guardian-sudoed scaffold for insyn coverage gaps. |
| `synomic-entities.md` | Full spectrum diagram (minimal Halo → Prime); inalienable-claims worked example; minimal-Halo "right to just exist" prose; joint-stock-properties mapping table; Halo class/book/unit hierarchy; 3-phase lifecycle (Creation / Operation / Termination — entity identity is immutable, so no transformation phase); the right-to-exist ethical framework with full compliant-vs-aligned distinction; binding-as-coalition framing. Prime table is `Prime | Type` with all six operational. Range-of-purpose table enumerates Folio, Core Entity, Oracle Entity, Sequencer Entity, Pylon Entity (with Ring coalitions hosted in Sequencer entarts), Prime, Generator. |
| `topology-layers.md` | Cadence-of-change per layer; topology-derived population atoms pattern (routing tables, registry indexes); flag-day sudo procedure; freeze-early posture rationale; full standard-comment-shape catalog; per-phase topology-deliverable structure; eight architectural commitments enumerated; eight open questions (telos specificity/mutability, axiom space placement, probmesh structural placement, frame boundary semantics, sudo authority structure, probmesh→sudo path mechanics, axiom crystallization). |

