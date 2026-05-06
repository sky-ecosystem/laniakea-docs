# Sky Ecosystem Documentation — Laniakea Upgrade

Technical documentation for Sky Ecosystem and the Laniakea upgrade — a comprehensive infrastructure overhaul rolling out through 2026.

## What is Laniakea?

Laniakea is Sky's infrastructure for **automated capital deployment at scale**. It introduces:

- **Unified capital flow architecture** — Capital flows from Sky Core → Primes → Halos → end investments, with every flow rate-limited
- **Scientific risk management** — Basel III-inspired framework determining capital requirements based on asset duration and forced realization probability
- **Autonomous operation** — Sentinel network operates infrastructure within governance-defined bounds, enabling 99% automation
- **Daily settlement cycles** — Standardized daily cycles for auctions, distributions, and LCTS token settlement (lock 13:00 UTC, settle by 16:00 UTC)

## Repo Layout

This repo is currently focused on **synomics** — the study of the Synome and the entities that inhabit it — together with the risk framework and the Noemar runtime that underlies it. Synomics is the data-and-AI-governance layer of the Laniakea program. Earlier-phase material (whitepaper, smart contracts, accounting, roadmap, etc.) is preserved in `inactive/pre-synlang/` while the active synomics-native rewrite proceeds. See [`clean-up-plan.md`](clean-up-plan.md) for the rewrite sequence.

### Active

| Directory | Description |
|---|---|
| [`core-concepts/`](core-concepts/) | Atomic concept definitions shared across the synomics narrative directories — also hosts the synomics overview |
| [`macrosynomics/`](macrosynomics/) | System-level structure — layers, agents, beacons, governance (the deontic skeleton); meta-architectural layering |
| [`synodoxics/`](synodoxics/) | Knowledge dynamics — probabilistic mesh, retrieval policy, security model, Noemar substrate (artifact tiers + telseed bootstrap) |
| [`neurosymbolic/`](neurosymbolic/) | Practical cognition — live graph context, context manipulation, attention allocation, hardware-aware cognition |
| [`synoteleonomics/`](synoteleonomics/) | Individual teleonomes — what they are, economics, memory, resilience, binding, autonomy paths, recipe marketplace |
| [`hearth/`](hearth/) | Telos point and high-level commitments |
| [`noemar-synlang/`](noemar-synlang/) | Noemar runtime + synlang technical reference — language reference, topology, runtime architecture, boot model, scaling, code patterns |
| [`risk-framework/`](risk-framework/) | Capital framework — duration model, asset classification, capital formulas, sentinel integration |

### Inactive

| Directory | Description |
|---|---|
| [`inactive/pre-synlang/`](inactive/pre-synlang/) | Earlier-phase docs (whitepaper, smart-contracts, accounting, roadmap, sky-agents, trading, governance-transition, growth-staking, skychain, input-documents, forecast_model) — being progressively rewritten synlang-native |
| [`inactive/archive/`](inactive/archive/) | Source material for the synomics rewrite (lift, lift-weakness, prior synomics summaries) |

## Key Documents

| Document | Description |
|---|---|
| [`core-concepts/README.md`](core-concepts/README.md) | Synomics directory framing and atomic concept index |
| [`macrosynomics/synome-overview.md`](macrosynomics/synome-overview.md) | Architecture entry point — five layers, dual architecture, knowledge hierarchy |
| [`macrosynomics/beacon-framework.md`](macrosynomics/beacon-framework.md) | Beacon taxonomy — two-tier authority + I/O role under it; in-space calculation; sentinel formations |
| [`hearth/README.md`](hearth/README.md) | The system's telos point and high-level commitments |
| [`risk-framework/README.md`](risk-framework/README.md) | Risk framework module index |
| [`synomics-overview.md`](synomics-overview.md) | Synomics concept map — four-tier architecture, blockchain analogy, authority chain, settlement, recipe marketplace |

## Using This Repository

This documentation is designed for navigation with **code LLMs** (Claude Code, Cursor, etc.). The information density and cross-references between documents make AI assistance valuable for efficiently traversing the content.

**Getting started:**
- New readers: [`core-concepts/README.md`](core-concepts/README.md) for synomics framing, then pick a direction
- Architecture-first: [`macrosynomics/synome-overview.md`](macrosynomics/synome-overview.md)
- Purpose-first: [`hearth/README.md`](hearth/README.md)
- Implementation-first: [`synomics-overview.md`](synomics-overview.md)

## Status

These documents are drafts under active development. The corpus is in a synlang-native rewrite (see [`clean-up-plan.md`](clean-up-plan.md)); content may change as the protocol evolves.

## Links

- [Sky Ecosystem](https://sky.money)
- [Sky Forum](https://forum.sky.money)
