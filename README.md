# Sky Ecosystem Documentation — Laniakea Upgrade

Technical documentation for Sky Ecosystem and the Laniakea upgrade — a comprehensive infrastructure overhaul rolling out through 2026.

## What is Laniakea?

Laniakea is Sky's infrastructure for **automated capital deployment at scale**. It introduces:

- **Unified capital flow architecture** — Capital flows from Sky Core → Primes → Halos → end investments, with every flow rate-limited
- **Scientific risk management** — Basel III-inspired framework determining capital requirements based on asset duration and forced realization probability
- **Autonomous operation** — Sentinel network operates infrastructure within governance-defined bounds, enabling 99% automation
- **Daily settlement cycles** — Standardized daily cycles for auctions, distributions, and LCTS token settlement (lock 13:00 UTC, settle by 16:00 UTC)

## Repo Layout

This repo is currently focused on **synomics** — the study of the Synome and the entities that inhabit it — together with the risk framework and the Noemar runtime that underlies it. Synomics is the data-and-AI-governance layer of the Laniakea program. Earlier-phase material (whitepaper, accounting, roadmap, skychain, input-documents, forecast model) is preserved in `inactive/pre-synlang/` while the active synomics-native rewrite proceeds.

### Active

| Directory | Description |
|---|---|
| [`core-concepts/`](core-concepts/) | Atomic concept definitions shared across the synomics narrative directories — also hosts the synomics overview |
| [`macrosynomics/`](macrosynomics/) | System-level structure — layers, entities, beacons, governance (the deontic skeleton); meta-architectural layering |
| [`synodoxics/`](synodoxics/) | Knowledge dynamics — probabilistic mesh, retrieval policy, security model, Noemar substrate (artifact tiers + telseed bootstrap) |
| [`neurosymbolic/`](neurosymbolic/) | Practical cognition — live graph context, context manipulation, attention allocation, hardware-aware cognition |
| [`synoteleonomics/`](synoteleonomics/) | Individual teleonomes — what they are, economics, memory, resilience, binding, autonomy paths, recipe marketplace |
| [`noemar-synlang/`](noemar-synlang/) | Noemar runtime + synlang technical reference — language reference, topology, runtime architecture, boot model, scaling, code patterns |
| [`risk-framework/`](risk-framework/) | Capital framework — duration model, asset classification, capital formulas, sentinel integration |
| [`accounting/`](accounting/) | Funding side — settlement cycle, capital stack (JRC/EJRC/SRC/MDC, ingression, Genesis Capital), isolated deployment, duration allocation, legacy transition |
| [`smart-contracts/`](smart-contracts/) | On-chain contract architecture — PAU pattern, Configurator Unit, LCTS, NFATS, Diamond PAU, Yield Splitter, rate-limit attack analysis |
| [`sentinel/`](sentinel/) | Sentinel Network — Baseline / Stream / Warden / Principal formations; TTS-priced ORC; Streaming Accord (absorbed former `trading/`) |
| [`synomic-entities/`](synomic-entities/) | Per-type operational specs — Prime, Generator, Guardian (Ozone), Core Entity, Oracle / Sequencer / Pylon Entities, Folio, Halo (Portfolio / Term / Trading / Identity Network) |
| [`growth-staking/`](growth-staking/) | Growth Staking — GF tiers, Reference Valuation (global P/E model), stUSDS borrow surface, Folio integration, agent-internal staking |
| [`governance/`](governance/) | Practical voting and ratification — Core Council elections, SpellGuard, voting mechanics |
| [`roadmap/`](roadmap/) | Phase-specific reality — Phase 1 spaces, short-term actuators, v1 test example, ASC transition, vocabulary and conventions |

### Inactive

| Directory | Description |
|---|---|
| [`inactive/pre-synlang/`](inactive/pre-synlang/) | Remaining earlier-phase docs (whitepaper, accounting, roadmap, skychain, input-documents, forecast_model) — being progressively rewritten synlang-native. The pre-synlang `growth-staking/` source has been migrated; the active spec is at [`growth-staking/`](growth-staking/) (historical source preserved at `inactive/archive/growth-staking/`) |
| [`inactive/archive/`](inactive/archive/) | Source material for the synomics rewrite (lift, lift-weakness, prior synomics summaries) |

## Using This Repository

This documentation is designed for navigation with **code LLMs** (Claude Code, Cursor, etc.). The entry point is [`summaries/`](summaries/) — read [`summaries/README.md`](summaries/README.md) first; it explains the three-layer structure (root README → summaries → detail files) and lists all 14 directory summaries to load as default context.

Direct pointers for specific orientations:
- Architecture-first: [`macrosynomics/synome-overview.md`](macrosynomics/synome-overview.md)
- Purpose-first: [`core-concepts/telos-point.md`](core-concepts/telos-point.md)
- Beacons: [`macrosynomics/beacon-framework.md`](macrosynomics/beacon-framework.md)

Per-directory `README.md` files intentionally do not exist — the summaries serve that function.

## Status

These documents are drafts under active development. The corpus is in a synlang-native rewrite; content may change as the protocol evolves.

## Links

- [Sky Ecosystem](https://sky.money)
- [Sky Forum](https://forum.sky.money)
