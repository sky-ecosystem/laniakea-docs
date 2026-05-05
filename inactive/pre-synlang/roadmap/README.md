# Implementation Roadmap

Phased implementation plan for Laniakea infrastructure, from Phase 0 legacy exceptions through full autonomous operation with Sentinel formations in Phase 10. The progression follows three stages: foundational infrastructure (Phases 0-4), factory systems for scalable deployment (Phases 5-8), and full automation through Sentinel formations (Phases 9-10).

Start with [`roadmap-overview.md`](roadmap-overview.md) for the complete summary including dependency graph, key milestones, and beacon taxonomy reference.

## Documents

| Document | Description |
|---|---|
| [roadmap-overview.md](roadmap-overview.md) | Master overview with phase summary, dependencies, milestones, and document index |
| [phase-0-legacy-exceptions.md](phase-0-legacy-exceptions.md) | Grove pre-standardization deployments; acknowledged technical debt (runs concurrently with Phase 1) |
| [phase1/](phase1/) | **Phase 1 subdirectory** — all Phase 1 specifications |
| [phase1/phase-1-overview.md](phase1/phase-1-overview.md) | Phase 1 overview — deliverables, substages, end state |
| [phase1/synome-mvp-reqs.md](phase1/synome-mvp-reqs.md) | Phase 1 requirements for Synome-MVP (inputs/outputs, APIs, schemas, and non-goals) |
| [phase1/halo-book-deep-dive.md](phase1/halo-book-deep-dive.md) | Halo Book implementation spec for Phase 1 (lifecycle, Synome schema, offboarding, creation policy) |
| [phase-2-monthly-settlement.md](phase-2-monthly-settlement.md) | Full lpla-checker with settlement tracking; formalized monthly settlement cycle |
| [phase-3-daily-settlement.md](phase-3-daily-settlement.md) | Transition from monthly to daily settlement cycle |
| [phase-4-lcts-launch.md](phase-4-lcts-launch.md) | srUSDS and first Portfolio Halo (LCTS); Core Council manages srUSDS rate pre-auction |
| [phase-5-halo-factory.md](phase-5-halo-factory.md) | Automated Halo Agent creation with LCTS/NFAT class attachment |
| [phase-6-generator-pau.md](phase-6-generator-pau.md) | Single-ilk USDS Generator PAU replacing per-Prime ilks |
| [phase-7-prime-factory.md](phase-7-prime-factory.md) | Automated Prime deployment via Laniakea Factory |
| [phase-8-generator-factory.md](phase-8-generator-factory.md) | Automated Generator deployment; full factory stack operational |
| [phase-9-sentinel-base-warden.md](phase-9-sentinel-base-warden.md) | Baseline Sentinel (stl-base) and Warden Sentinels; auction activation (OSRC + Duration) |
| [phase-10-sentinel-stream.md](phase-10-sentinel-stream.md) | Stream Sentinel for proprietary intelligence and alpha generation |

## Related

- [`smart-contracts/`](../smart-contracts/) — Contract architecture referenced throughout (PAU pattern, LCTS, NFATS, Diamond PAU, Configurator)
- [`synomics/macrosynomics/beacon-framework.md`](../synomics/macrosynomics/beacon-framework.md) — Beacon taxonomy (LPLA/LPHA/HPLA/HPHA) that the roadmap progressively deploys
- [`accounting/daily-settlement-cycle.md`](../accounting/daily-settlement-cycle.md) — Settlement timing specification that Phases 2-3 implement
- [`trading/sentinel-network.md`](../trading/sentinel-network.md) — Sentinel formation architecture for Phases 9-10
