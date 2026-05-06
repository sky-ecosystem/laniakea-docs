# Operational Risk Capital

**Status:** Draft
**Last Updated:** 2026-02-06

---

## Overview

Operational Risk Capital (ORC) is capital posted by the entity that holds execution authority over a PAU (the guardian/Accordant — see Glossary: Guardian Role Mapping), covering the maximum damage that entity could cause before detection and shutdown.

**ORC is a parallel track to portfolio risk capital** (CRR-based, computed via [`risk-decomposition.md`](risk-decomposition.md), [`book-primitive.md`](book-primitive.md), and the layer docs) — it addresses operational compromise, not market/credit risk. The two capital pools protect the Prime against different threat classes; both are required, additively.

| Concept | Portfolio Risk Capital | Operational Risk Capital |
|---------|----------------------|------------------------|
| **What it covers** | Market, credit, duration, and liquidity risk | Damage from compromised guardian |
| **Sized by** | CRR per [`risk-decomposition.md`](risk-decomposition.md) — five risk types blended through sub-book routing | Rate limits × detection window |
| **Posted by** | Prime (from JRC/EJRC/SRC) | Guardian (Accordant to the Prime) |
| **Framework** | [`capital-formula.md`](capital-formula.md) and the layer docs | This document |

**Both are required.** A Prime needs portfolio risk capital to cover investment losses AND its guardian needs operational risk capital to cover compromise damage. These are independent, additive requirements.

---

## Core Formula

```
ORC ≥ Maximum Damage During Detection Window
```

The detection window and damage model differ by phase:

### Phase 1: Pre-Sentinel (GovOps Guardians)

In Phase 1, guardians are GovOps teams holding cBEAMs. The relevant attack model is a compromised relayer key.

```
ORC ≥ Type 1 Max Loss × N
    = IRL × Accumulation Factor × N
```

Where:
- **IRL** = Initial Rate Limit ($100K)
- **Accumulation Factor** = `1 + 0.25 × SORL` = 1.0625 (at SORL = 25%; see `smart-contracts/configurator-unit.md` for canonical SORL parameters)
- **N** = number of attack surfaces (initialization targets)

The detection window is **Time to Freeze (TTF)** — typically 24 hours for Phase 1 monitoring.

See `smart-contracts/rate-limit-attacks.md` for the full attack model and parameter derivation.

**Example:** With N=10 surfaces, ORC ≥ $100K × 1.0625 × 10 ≈ **$1.06M per guardian**.

> **Note on Type 2 harm:** This formula covers Type 1 (direct extraction — 100% attacker profit). Type 2 (operational extraction via slippage grinding) causes larger marginal harm (~$2.05M/N₁ vs ~$395K/N₁ at adopted parameters) but has a much lower attacker extraction rate (~10%). The adopted SORL/IRL parameters were optimized for combined weighted harm across both types — see `smart-contracts/rate-limit-attacks.md` for the full model. Total weighted harm at adopted parameters is ~$2.36M/N₁.

### Sentinel Era: TTS-Based

> **Transition:** The shift from Phase 1 (TTF-based) to sentinel-era (TTS-based) ORC occurs when sentinel formations replace GovOps guardians as PAU operators (Phase 9-10). During the transition, both models may coexist — PAUs still operated by GovOps use the Phase 1 formula; PAUs operated by sentinel formations use the TTS formula.

When sentinel formations operate PAUs, the guardian (Accordant to the Prime) posts ORC based on Time to Shutdown:

```
ORC ≥ Rate Limit × TTS
```

Where:
- **Rate Limit** = the PAU's `maxAmount` (instantaneous buffer ceiling), not the replenishment slope. If TTS exceeds the refill period, damage is `maxAmount + slope × TTS`; for short TTS the buffer ceiling dominates
- **TTS** = Time to Shutdown — worst-case time for wardens to detect and halt a rogue sentinel

See `trading/sentinel-network.md` for TTS determinants and warden economics.

**Example:** With Rate Limit = $100M/day and TTS = 4 hours, ORC ≥ $100M × (4/24) ≈ **$16.7M**.

---

## Relationship to Rate Limits

ORC and rate limits are directly linked — they constrain each other:

**Given fixed ORC:**
```
Max Rate Limit ≤ ORC / TTS
```

A guardian with $20M ORC and 4-hour TTS can support rate limits up to $120M/day.

**Given target rate limit:**
```
Required ORC ≥ Rate Limit × TTS
```

A Prime targeting $200M/day with 4-hour TTS requires $33.3M in guardian ORC.

This is how capital requirements translate to PAU rate limits (risk-framework open item #4).

---

## ORC vs Portfolio Capital: How They Interact

Both capital pools protect the Prime, but against different risks:

```
Prime Capital Requirements:
  Portfolio Risk Capital (CRR-based)
    └── Covers: market losses, credit events, duration mismatches
    └── Sized by: capital-formula.md
    └── Funded by: IJRC + EJRC + SRC (ingression-adjusted)

  Operational Risk Capital (ORC)
    └── Covers: damage from compromised execution authority
    └── Sized by: Rate Limit × TTS (or IRL × accumulation × N)
    └── Funded by: Guardian's own capital (Guardian Accord)
```

**Key distinction:** Portfolio risk capital is Prime capital (shared across all positions). ORC is Accordant capital (specific to the party holding execution keys). A Prime is rooted under the single operational Guardian (Ozone) but may have multiple Accordants if execution authority is decomposed by PAU scope, each posting ORC for their scope of authority.

---

## Guardian Accords

A **Guardian Accord** is the agreement between a Prime and its guardian defining:

| Parameter | Description |
|-----------|-------------|
| **Scope** | Which PAUs the executor operates |
| **Rate limits** | Maximum rate limits the guardian can exercise |
| **ORC requirement** | Minimum operational risk capital posted |
| **TTS commitment** | Warden coverage and detection guarantees |
| **Penalties** | Consequences for violations or losses |

In Phase 1, guardian accords are implicit (GovOps teams operate under Core Council governance). In the sentinel era, guardian accords become explicit smart contracts — the Streaming Accord is a specialized form for stream sentinel operators.

> **Folio ORC note:** Automated folios (those operated by sentinel formations via guardian accord) inherit the full ORC framework — their guardians post ORC and their sentinel formations include wardens, so TTS-based sizing applies identically to Primes. Principal-control folios, by contrast, have no TTS and no wardens; risk is bounded solely by rate limits, since the principal is both operator and beneficiary and there is no external execution authority to insure against. This distinction matters for Phase 9+ ORC sizing: automated folios scale ORC with warden quality like any other sentinel-operated PAU, while principal-control folios require no ORC charge at all.

---

## Warden Economics

Wardens are capital efficiency multipliers for ORC:

```
Better wardens → Lower TTS → Lower ORC requirement → Higher rate limits
```

| Warden Quality | Typical TTS | ORC for $100M/day Rate Limit |
|----------------|-------------|------------------------------|
| Basic (1 warden, manual) | 24h | $100M |
| Standard (2 wardens, automated) | 4h | $16.7M |
| Premium (3+ wardens, diverse, certified) | 1h | $4.2M |

This creates a market for warden services where safety is priced in, not externalized. Primes that invest in better warden coverage gain operational efficiency.

---

## Trading Execution Risk (Prime Intent Vaults)

ORC covers damage from compromised execution authority (guardian keys). A related but distinct risk exists in **Prime Intent Vaults (PIVs)** — bounded trading sub-accounts where working capital is at risk during intent-based trading.

PIV trading risk is managed through on-chain enforcement, not ORC:

- **Delegated Intent Policy (DIP)** — on-chain policy defining allowed assets, position limits, velocity limits, concentration caps
- **Per-window caps** — stateful limits on delegated trading volume per time window
- **EIP-1271 validation** — settlement contract validates each intent against the vault's policy before execution

PIV capital is isolated from the Prime's main PAU by design — the vault holds only the working capital needed for active trading, bounding worst-case loss.

See `trading/sky-intents.md` for the full PIV specification and security model.

> **Forward reference:** For broader trading execution risk — settlement failure, stale oracle prices, counterparty default between match and settlement — a dedicated risk framework module is planned. See the "Planned Modules" section in the [`risk-framework/README.md`](README.md).

---

## Connection to Other Documents

| Document | Relationship |
|----------|--------------|
| `smart-contracts/rate-limit-attacks.md` | Phase 1 attack model and IRL/SORL parameter derivation |
| `trading/sentinel-network.md` | TTS definition, warden economics, Streaming Accords |
| `risk-framework/capital-formula.md` | Portfolio risk capital (the other capital requirement) |
| `risk-framework/sentinel-integration.md` | How beacons use risk framework outputs |
| `smart-contracts/configurator-unit.md` | SORL and rate limit mechanics |
| `trading/sky-intents.md` | Prime Intent Vault trading risk — on-chain enforcement via DIP |

---

*This document defines Operational Risk Capital. For portfolio risk capital, see `capital-formula.md`. For the full sentinel specification, see `sentinel-network.md`.*
