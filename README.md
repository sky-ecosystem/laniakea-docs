# Sky Ecosystem Documentation — Laniakea Upgrade

Technical documentation for Sky Ecosystem and the Laniakea upgrade — a comprehensive infrastructure overhaul rolling out through 2026.

## What is Laniakea?

Laniakea is Sky's infrastructure for **automated capital deployment at scale**. It introduces:

- **Unified capital flow architecture** — Capital flows from Sky Core → Primes → Halos → end investments, with every flow rate-limited
- **Scientific risk management** — Basel III-inspired framework determining capital requirements based on asset duration and forced realization probability
- **Autonomous operation** — Sentinel network operates infrastructure within governance-defined bounds, enabling 99% automation
- **Weekly settlement cycles** — Standardized Tue-Wed cycles for auctions, distributions, and LCTS token settlement

This repository provides a complete view of all future Laniakea upgrades alongside current Sky Ecosystem parameters and features.

## Using This Repository

This documentation is designed for navigation with **code LLMs** (Claude Code, Cursor, etc.). The information density and cross-references between documents make AI assistance valuable for efficiently traversing the content.

**Getting started:**
- Read the whitepaper for the narrative overview
- Explore specific directories for technical depth
- Use your AI assistant to search across documents and trace concepts

## Contents

### whitepaper/
The public-facing narrative wrapper around the Laniakea system.

| Document | Description |
|----------|-------------|
| sky-whitepaper.md | Main 8-part document covering business model, history, tokens, agents, risk, and governance |
| appendix-a-protocol-features.md | Exhaustive list of Sky Core mechanisms |
| appendix-b-sky-agent-framework-primitives.md | Sky Agent Framework capabilities (Primes, Halos, Executors) |
| appendix-c-treasury-management-function.md | Complete TMF waterfall specification |
| appendix-d-tokens.md | Complete token reference (USDS, sUSDS, SKY, stUSDS, and agent tokens) |
| appendix-e-design-rationale.md | Q&A explaining critical design decisions |
| appendix-f-glossary.md | Term definitions |
| appendix-g-infrastructure.md | Deployed contracts, bridges, and legacy systems |

### risk-framework/
Basel III-inspired capital requirements framework. Core principle: **Capital Requirement = Drawdown Magnitude × Forced Realization Probability**

| Document | Description |
|----------|-------------|
| README.md | Framework overview and module map |
| duration-model.md | Liability duration analysis, SPTP buckets, structural caps |
| asset-classification.md | Asset characteristics, fundamental risk, drawdown risk |
| matching.md | Rate risk vs credit spread risk, SPTP eligibility |
| asset-type-treatment.md | Worked treatments for TradFi, crypto, hybrid assets |
| collateralized-lending-risk.md | Jump-to-default and liquidation loss (gap risk) |
| market-risk-frtb.md | FRTB-style drawdown treatment for unmatched liquid assets |
| asc.md | Actively Stabilizing Collateral requirements |
| capital-formula.md | Capital formulas and computation flow |
| correlation-framework.md | Category caps and capacity rights |
| risk-capital-ingression.md | How external capital is recognized on Prime balance sheets |
| tugofwar.md | Capacity allocation when reservations exceed availability |
| weekly-settlement-cycle.md | Settlement timing and processes |
| sentinel-integration.md | Output metrics and Sentinel integration |
| examples.md | Current vs proposed examples |

### smart-contracts/
Laniakea smart contract architecture built on the **PAU pattern** (Parallelized Allocation Unit).

| Document | Description |
|----------|-------------|
| architecture-overview.md | Four-layer capital flow (Generator → Prime → Halo → RWA), PAU pattern, modular design |
| configurator-unit.md | Governance layer: BEAM hierarchy (aBEAM/cBEAM/pBEAM), rate limits, SORL |
| lcts.md | Liquidity Constrained Token Standard — queue-based tokens for fair capacity distribution |
| nfats.md | Non-Fungible Allocation Token Standard — bespoke capital deployment deals with individual terms |

### governance-operations/
Governance structure and autonomous operational infrastructure.

| Document | Description |
|----------|-------------|
| sentinel-network.md | Autonomous agents (Sentinels) operating infrastructure: taxonomy, interfaces, toolkit |
| atlas-synome-separation.md | Two-layer split: Atlas (human-readable constitution) + Synome (machine-readable database) |

### legal-and-trading/
Trading infrastructure, compliance frameworks, and institutional integration.

| Document | Description |
|----------|-------------|
| passthrough-halo.md | Standardized wrapper enabling rapid RWA product launch with immediate capital |
| identity-network.md | KYC/identity verification as a Halo type — on-chain registry of verified addresses |
| sky-intents.md | Intent-based trading protocol: fair matching, no MEV, permissioned trading |

### input-documents/
Community contribution directory. Submit PRs with corrections, suggestions, questions, or new information.

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
