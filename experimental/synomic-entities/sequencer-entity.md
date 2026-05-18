# Sequencer Entity

**Status:** Stub spec — type designation. No instantiations yet.

A Sequencer Entity is a synomic entity that runs orderbook matching as a regulated venue and hosts Ring coalitions for derivatives products. It is trusted to sequence orders and execute matching without frontrunning, with that trust enforced by **revocability** — no collateral, no slashing, no participation in any loss waterfall. Sequencer Entities are the on-chain analog of a registered exchange or matching venue: operational trust enforced by external authority, not by capital at risk.

For Synomic Entity theory, see [`../macrosynomics/synomic-entities.md`](../macrosynomics/synomic-entities.md). For the principal-bearing counterpart, see [`pylon-entity.md`](pylon-entity.md).

---

## Properties

| Property | Description |
|---|---|
| **Rank** | 2 (accordant to a Guardian) |
| **Scope** | One Sequencer Entity per matching venue; may host multiple Rings |
| **Function** | Sequence orders, run matching algorithm, return trade prints; host Ring sub-structures and their accord protocols |
| **Dependencies** | Accordant to Ozone; serves Pylons, Primes, and Halos as venue |
| **Governance** | Tokenless or with limited governance token (TBD) |
| **Collateral** | **None** — no operational collateral, no risk capital, no slashing collateral. Trust enforced by revocability. |

---

## What Distinguishes Sequencer Entity

Sequencer Entities sit between order submitters and execution. They need first-class entity status because:

- **They see order flow before matching.** Frontrunning is a real attack surface; the entity is trusted not to.
- **They sequence transactions.** Sequencing affects pricing and execution; the entity is trusted to sequence fairly.
- **They host Rings.** Ring sub-structures live inside the Sequencer's entart — the Sequencer is the structural admin of the Rings operating on its venue.
- **They don't bear principal positions.** Unlike a Pylon, they don't take positions; they only match other entities' orders. The trust model is operational, not capital-bearing.

### Trust enforcement: revocability, not collateral

Sequencer Entities post **no collateral and bear no slashing**. The model is regulated-venue-by-revocation, not bonded-venue-by-slashing:

- **Synomic registry as audit trail.** Order receipt, sequence assignment, match log are all written into synome state via Sequencer's beacons. Every transaction has a provable trail.
- **Oracle Entity audits.** Independent attestation beacons verify aggregate trading behavior, flag anomalies (frontrunning patterns, miss-sequencing, censoring), and attest to operational compliance.
- **Core Council revocability.** A misbehaving Sequencer Entity can be retired by Core Council governance, immediately killing its operating authority. The Sequencer's right to operate is its entire skin in the game; revocation is catastrophic for the operating organization (loss of business, reputation, deployed capital invested in matching infrastructure).
- **Recourse against operator.** If Sequencer misbehavior causes financial harm (e.g. miss-sequencing that propagates wrong fills into settlement), there is no on-chain financial recourse from the Sequencer itself — it has no collateral. Recovery flows through Core Council escalation: revocation, legal action against the operating organization, potential restitution from Sky Aggregate Backstop Capital if the harm is judged systemically significant. This is a **governance escalation path, not an automatic on-chain mechanism**, and the lack of automatic financial recourse is a known open question — see § [Open Questions](#open-questions).

This makes Sequencer Entities analogous to a registered exchange — a regulated venue with operational trust enforced by external authority. The model closely matches how clearinghouses-without-bonds operate in practice: regulators can shut them down, which is the credible threat.

### Why no collateral

A Sequencer doesn't take principal risk. The losses it might cause (sequencing misbehavior, miss-fills, frontrunning) are operational, not directly capital-related. Posting collateral against operational misbehavior would be theatre — the meaningful consequence is revocation and reputational destruction, not a slashable bond.

This also keeps the entity-type taxonomy clean: Sequencer joins the **purely operational, trust-by-revocability** cluster alongside Oracle Entity and Core Entity. The "tokenized + risk-capital-bearing" cluster (Generator, Prime, Pylon, Guardian, governed Halo) is separate.

---

## Hosting Rings

A Sequencer Entity hosts one or more Rings inside its entart. Rings are **sub-structures, not separate entities** — they live at addresses like `&entity.sequencer.{seq-id}.ring.{ring-id}` and inherit the Sequencer's structural infrastructure (matching engine, sequencing layer, attestation interfaces).

| Element | Owned by Sequencer's entart |
|---|---|
| Ring's accord parameters (product, margin schedules, recovery-tool spec) | Yes |
| Ring's Pylon membership list (foreign references into Pylon entarts) | Yes |
| Ring's assurance-fund balance attestations | Yes |
| Ring's match log and trade history | Yes |
| Pylon's per-Ring pledge | Foreign reference — actual capital tracked at the Pylon's entart |

The Sequencer is the **admin** of its Rings, not the **counterparty** to their trades. Sequencer responsibilities:

- Apply the Ring's matching algorithm
- Enforce the Ring's margin schedules (reject submissions that would breach margin)
- Maintain Ring's match log and emit attestation atoms via Oracle Entity beacons
- Process Ring's membership accords (new Pylons joining; departures after lockup)
- Execute the Ring's recovery-tool sequence if assurance fund is exhausted

Sequencer responsibilities **don't** include:

- Bearing any portion of mutualization loss (that's Pylon-funded)
- Setting Ring rules unilaterally (Ring rules are inter-Pylon accord; Sequencer hosts them)
- Custodying Pylon collateral (per-Ring pledges remain in Pylon entarts as committed atoms; Sequencer references them)

### Criss-cross Ring memberships

A Sequencer can host any number of Rings; a Pylon can belong to Rings hosted at multiple Sequencers. The full criss-cross pattern is unconstrained:

- Sequencer A hosts BTC perps Ring (Pylons P1, P2, P3, P4) and ETH perps Ring (Pylons P1, P2, P5, P6)
- Sequencer B hosts its own BTC perps Ring (different membership: P3, P4, P7, P8, P9) and a Eurodollar Ring (P1, P10)
- Same Pylon P1 is a member of three Rings across two Sequencers; its per-Ring pledges are siloed per Ring.

A Sequencer compromise / retirement kills only its own Rings. Pylons retain memberships at other Sequencers; their per-Ring pledges at the affected Sequencer become claims on whatever recovery process the retirement triggers (likely orderly Ring dissolution under Core Council governance, with positions closed at clearing prices).

---

## Use Cases

| Use case | Notes |
|---|---|
| **Derivatives matching** (primary) | Host Rings for perp swaps, futures, options, exotic structures. Pylons join Rings to provide principal capacity; Primes / Folios trade against Pylon positions. |
| **Spot trading** | Orderbook matching for tokenized assets (PT/YT, Halo Units, etc.). No Ring needed — direct matching with bilateral settlement. |
| **Cross-Halo unit trading** | Secondary market for Halo Units that aren't natively LCTS-fungible. |

Multiple Sequencer Entities can coexist; consumers route to whichever Sequencer supports their products. Sequencer Entities are independent — not bound to any specific Pylon or Ring; their commercial relationship is with the entire set of Rings they host plus any direct spot-trading users.

---

## Beacon Classes

TBD. Likely includes:

- `sequencer-receive` — accept orders, write to sequence log
- `sequencer-match` — apply matching algorithm, write trade prints, emit fills
- `sequencer-cancel` — process order cancels, write cancel atoms
- `sequencer-ring-admin` — process Ring-level accord operations (membership changes, accord parameter updates within bounds)
- `sequencer-recovery` — execute Ring recovery-tool sequence (VMGH calculation, partial tear-up assignment, dissolution trigger) when activated by Ring accord

Specific class taxonomy depends on whether sequencing and matching are conceptually separated or unified, and on how Ring-administrative actions are bundled with matching beacons.

---

## Capital Model

Sequencer Entities have **no capital model in the loss-absorption sense**. They hold no risk capital, no operational collateral, no slashing bond. The entity's only "capital" is whatever the operating organization needs to fund the matching infrastructure (servers, beacons, regulatory compliance, organizational overhead) — and that's the operating organization's commercial concern, not a system-recognized layer.

Sequencer Entities are **typically tokenless**. Some may issue limited governance tokens for organizational reasons (e.g., to coordinate among multiple operating partners), but token issuance triggers Entity Creation Fee + Upkeep per the unified rule in [`../accounting/entity-fees.md`](../accounting/entity-fees.md). A tokenless Sequencer pays no fee directly; revenue to Sky may come through other channels (per-trade fees, Ring-hosting fees split between Sequencer operator and Sky Core — TBD).

---

## Lifecycle

Created via Guardian Accord under SpellCore. Tokenless or limited-token. Revoked via Core Council governance on misbehavior — revocation kills the Sequencer's operating authority; any Rings it hosted enter orderly dissolution (positions closed at clearing prices, residual loss spread proportionally, Pylons released to continue at other Sequencers).

See [`creation-restructuring.md`](creation-restructuring.md).

---

## Open Questions

- **Sequencing model.** First-come-first-served from beacon receipt? Time-priority with explicit timestamps? Auction-style batches per epoch? Likely product-dependent and configured per Ring.
- **Matching algorithm.** Order types supported (limit, market, IOC, post-only); pro-rata vs price-time priority. Likely product-dependent.
- **Censorship resistance.** What prevents a Sequencer Entity from selectively dropping orders? Backup-Sequencer routing? Mandatory order broadcast? Oracle-Entity-observed order-receipt attestation?
- **MEV / frontrunning detection.** Concrete attestation surfaces an Oracle Entity can audit to prove frontrunning post-hoc. What atoms are mandatory in the sequence / match log?
- **Fee structure.** Maker-taker? Per-trade? Ring-hosting subscription paid by Pylon coalitions? How do fees split between the Sequencer operator and Sky Core?
- **Relationship to LCTS.** Are Sequencer Entity matches written through LCTS, or is matching distinct from LCTS-style daily settlement?
- **Cross-Sequencer arbitrage.** When multiple Sequencer Entities serve the same product (different Rings, possibly overlapping Pylon membership), what guarantees price coherence?
- **Operational-harm recourse.** If a Sequencer's misbehavior causes financial harm beyond reputational consequences and revocation, there's no automatic on-chain financial recourse (since no collateral). The path is governance escalation to Core Council, potentially restitution from ABC if systemically significant. This is acknowledged as a known gap — alternative mechanisms (e.g., insurance bonds, operator-personal-liability arrangements off-chain) are open.
- **Hyperliquid analog.** Hyperliquid is a single-entity Layer-1 with consensus-as-matching, and also bears the principal risk itself (no separation of venue from broker-dealer). Sequencer + Pylon Ring is the explicitly-separated alternative: Sequencer matches, Pylons take risk. UX-side: is the user experience comparable? What's lost / gained?

---

## Relationship to Other Entity Types

| Comparison | Sequencer Entity | Other |
|---|---|---|
| vs **Pylon** | Sequences and matches orders; doesn't take positions; no collateral | Takes principal positions; bears risk capital; mutualizes via Ring assurance fund |
| vs **Trading Halo (AMM)** | Orderbook matching; no inventory; tokenless | AMM with oracle-priced inventory; Halo-class entity bearing AMM-side risk |
| vs **Oracle Entity** | Operational venue; tokenless; revocability-enforced trust | Tokenless data provider; revocability-enforced trust (similar trust model, different function) |
| vs **Generator** | Operational venue; non-balance-sheet | Foundational credit creator; balance-sheet |

Sequencer Entity and Oracle Entity are structurally similar in trust model — both are tokenless, both bear no collateral, both rely on revocability rather than slashing for accountability. They cluster together as **purely operational synomic infrastructure**.

---

## Related

- [`../macrosynomics/synomic-entities.md`](../macrosynomics/synomic-entities.md) — Synomic Entity theory
- [`pylon-entity.md`](pylon-entity.md) — Principal-bearing broker-dealer that uses Sequencer Entities as venue and participates in Sequencer-hosted Rings
- [`oracle-entity.md`](oracle-entity.md) — Audit / attestation provider for Sequencer operational compliance and Ring health
- [`halo-trading.md`](halo-trading.md) — AMM Trading Halo (alternative venue type — bears principal risk via inventory)
- [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) — Beacon taxonomy
- [`../smart-contracts/fixed-rates.md`](../smart-contracts/fixed-rates.md) — PT/YT use case for orderbook matching
- [`creation-restructuring.md`](creation-restructuring.md) — Entity creation mechanism
- [`../accounting/entity-fees.md`](../accounting/entity-fees.md) — Fee model
