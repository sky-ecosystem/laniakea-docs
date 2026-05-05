# Smart Contracts

On-chain contract architecture for Laniakea's capital deployment infrastructure. The core design principle is the PAU (Parallelized Allocation Unit) pattern — Controller + ALMProxy + RateLimits — reused identically across all four layers (Generator, Prime, Halo, Foreign). Layers differ only in configuration, not in contract code.

Start with [`architecture-overview.md`](architecture-overview.md) for the four-layer architecture, capital flow diagrams, and the PAU pattern.

## Documents

| Document | Description |
|---|---|
| [architecture-overview.md](architecture-overview.md) | Four-layer architecture (Generator/Prime/Halo/Foreign), PAU pattern, capital flow, Laniakea Factory |
| [diamond-pau.md](diamond-pau.md) | EIP-2535 Diamond proxy architecture replacing legacy single-controller PAUs |
| [configurator-unit.md](configurator-unit.md) | Governance layer for PAUs — aBEAM/cBEAM hierarchy, SORL, BEAMTimeLock mechanics |
| [lcts.md](lcts.md) | Liquidity Constrained Token Standard — queue-based token conversion with generation model |
| [nfats.md](nfats.md) | Non-Fungible Allocation Token Standard — bespoke deal mechanics with Halo Book/Unit separation |
| [fixed-rates.md](fixed-rates.md) | Yield Splitter — splitting yield-bearing tokens into Principal Token (PT) and Yield Token (YT) |
| [rate-limit-attacks.md](rate-limit-attacks.md) | Rate limit attack vectors (configuration theft, rate climbing) and IRL/SORL parameter calibration |

## Deferred Specifications

| Topic | Status | References |
|---|---|---|
| **Folio PAU architecture** — folio-side sentinels, principal control folios | Specification deferred pending Folio Agent deployment | [`risk-framework/sentinel-integration.md`](../risk-framework/sentinel-integration.md) for folio sentinel types (`stl-base-{folio}`, `stl-warden-{folio}`, `stl-principal-{owner}`); [`sky-agents/folio-agents/`](../sky-agents/folio-agents/) for the folio agent specification |

## Related

- [`roadmap/`](../roadmap/) — Implementation phases that progressively deploy this contract infrastructure
- [`synomics/macrosynomics/beacon-framework.md`](../synomics/macrosynomics/beacon-framework.md) — Beacon taxonomy; beacons operate PAUs via BEAMs
- [`sky-agents/halo-agents/`](../sky-agents/halo-agents/) — Halo types that use LCTS (Portfolio), NFATS (Term), and AMM (Trading) contracts
- [`risk-framework/`](../risk-framework/) — Risk calculations that constrain rate limit parameters
