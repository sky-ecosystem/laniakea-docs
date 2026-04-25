# Sky Ecosystem Documentation — Laniakea Upgrade

Technical documentation for Sky Ecosystem and the Laniakea upgrade — a comprehensive infrastructure overhaul rolling out through 2026.

## What is Laniakea?

Laniakea is Sky's infrastructure for **automated capital deployment at scale**. It introduces:

- **Unified capital flow architecture** — Capital flows from Sky Core → Primes → Halos → end investments, with every flow rate-limited
- **Scientific risk management** — Basel III-inspired framework determining capital requirements based on asset duration and forced realization probability
- **Autonomous operation** — Sentinel network operates infrastructure within governance-defined bounds, enabling 99% automation
- **Daily settlement cycles** — Standardized daily cycles for auctions, distributions, and LCTS token settlement (lock 13:00 UTC, settle by 16:00 UTC)

This repository provides a complete view of all future Laniakea upgrades alongside current Sky Ecosystem parameters and features.

## Using This Repository

This documentation is designed for navigation with **code LLMs** (Claude Code, Cursor, etc.). The information density and cross-references between documents make AI assistance valuable for efficiently traversing the content.

**Getting started:**
- Read the whitepaper for the narrative overview
- Explore specific directories for technical depth
- Use your AI assistant to search across documents and trace concepts

## Contents

| Directory | Description |
|---|---|
| [`whitepaper/`](whitepaper/) | Public-facing narrative — main 8-part whitepaper plus appendices (glossary, tokens, design rationale, infrastructure) |
| [`risk-framework/`](risk-framework/) | Basel III-inspired capital requirements — duration model, asset classification, capital formulas, sentinel integration |
| [`accounting/`](accounting/) | Settlement operations — daily settlement cycle, auctions, tug-of-war allocation, capital recognition |
| [`smart-contracts/`](smart-contracts/) | On-chain architecture — PAU pattern (Controller + ALMProxy + RateLimits), Diamond proxy, LCTS, NFATS, rate limits |
| [`roadmap/`](roadmap/) | Implementation phases 0–10 — from MVP beacons through factory stack to full sentinel automation |
| [`sky-agents/`](sky-agents/) | Synomic Agent specifications — Generators, Primes, Halos, Guardians, plus creation and restructuring mechanics |
| [`trading/`](trading/) | Sentinel network and Sky Intents — real-time execution infrastructure and intent-based trading protocol |
| [`synomics/`](synomics/) | The Synome and the entities that inhabit it — macrosynomics, synodoxics, neurosymbolic, synoteleonomics, the Hearth, core concepts |
| [`governance-transition/`](governance-transition/) | Alignment conserver consolidation — three legacy roles merged into single Guardian role with collateral backing |
| [`growth-staking/`](growth-staking/) | Growth Staking — SKY staker incentives tied to ecosystem growth asset holdings (Agent governance tokens and Prime junior risk capital / TEJRC) |
| [`skychain/`](skychain/) | Skychain research — proposed AI-native EVM blockchain optimized for agent operation |
| [`input-documents/`](input-documents/) | Community contributions — submit PRs with corrections, suggestions, questions, or new information |

## Key Documents

| Document | Description |
|---|---|
| [`whitepaper/sky-whitepaper.md`](whitepaper/sky-whitepaper.md) | Main whitepaper — business model, tokens, agents, risk, governance |
| [`whitepaper/appendix-f-glossary.md`](whitepaper/appendix-f-glossary.md) | Term definitions |
| [`smart-contracts/architecture-overview.md`](smart-contracts/architecture-overview.md) | Four-layer capital flow architecture and PAU pattern |
| [`synomics/macrosynomics/beacon-framework.md`](synomics/macrosynomics/beacon-framework.md) | Beacon taxonomy — power x authority matrix (LPLA/LPHA/HPLA/HPHA) |
| [`roadmap/roadmap-overview.md`](roadmap/roadmap-overview.md) | Master roadmap with phase summaries, dependencies, and milestones |

## Contributing

This repository is public to invite contributions from Sky Ecosystem community members.

**How to contribute:**
1. Create a pull request adding a new file to the `input-documents/` directory
2. Your input document can contain: corrections, new information, opinions, context, questions, or suggestions
3. Contributors with write access will review and merge relevant content into the core documentation

See `input-documents/README.md` for guidelines.

## Status

These documents are drafts under active development. Content may change as the protocol evolves.

## Links

- [Sky Ecosystem](https://sky.money)
- [Sky Forum](https://forum.sky.money)
