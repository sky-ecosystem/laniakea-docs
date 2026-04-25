# Isolated Deployment

**Status:** Draft
**Last Updated:** 2026-04-09

---

## Overview

Isolated deployment is a mode in which JRC or MDC capital is deployed into assets that are ring-fenced from the Prime's main portfolio. Assets held in isolated deployment are **not counted in the Prime's RWA or TRRC calculation**. Instead they are mapped 1:1 against the isolated capital that funds them — the isolated capital itself is the full risk buffer, and no separate CRR calculation applies.

Isolated deployment does not create leverage. It is a direct capital deployment mechanism, not an amplification of the Prime's capacity to take risk beyond its capital base.

---

## Definition

A deployment is isolated when:

1. The deployed assets are excluded from the Prime's portfolio-level TRRC calculation
2. The capital backing the deployment is designated as isolated (it cannot simultaneously serve as leverage buffer for the Prime's general book)
3. Losses on the isolated position reduce the backing capital directly, not the Prime's general capital pool
4. The Synome records the isolated deployment separately from the Prime's general book state

The constraint is:

```
Isolated deployed assets ≤ Isolated capital committed

(1:1 — no leverage ratio applies)
```

---

## Eligible Capital

Isolated deployment is available to:

- **IJRC** — the Prime's own internal junior risk capital
- **EJRC** — external junior risk capital (normie TEJRC or bespoke)
- **MDC** — mezzanine deployment capital (see `mezzanine-deployment-capital.md`)

**GSRC and ISRC leverage capital cannot be used for isolated deployment.** SRC goes through the standard leverage ingression framework and contributes to TRC. It is not available as a direct deployment instrument.

---

## Effect on the Prime's Capital Base

JRC or MDC committed to isolated deployment is **no longer available for other purposes**:

- IJRC or EJRC in isolated deployment reduces the Prime's **effective JRC** for leverage purposes — meaning SRC ingression capacity, MDC capacity, and any other JRC-anchored limits are all reduced accordingly
- MDC in isolated deployment reduces available MDC for other MDC deployments

This is correct behavior: the same capital unit cannot simultaneously act as a leverage buffer for the general book and as isolated deployment capital. The Prime must choose how to allocate its capital base.

---

## Key Use Case: Internal Egression into Another Prime's EJRC

The primary use case for isolated deployment is providing EJRC to another Prime via internal egression — without going through the external LCTS mechanism.

**Mechanics:**

Prime A designates capital (JRC or MDC) for isolated deployment into Prime B as EJRC:

```
Prime A books:                    Prime B books:
─────────────────────────────     ─────────────────────────────
Isolated deployment asset         EJRC received from Prime A
  → backed 1:1 by JRC or MDC        → ingressed via leverage curve
  → excluded from Prime A's RWA     → contributes to Prime B's TRC
  → loss reduces Prime A's JRC      → quality: per ingression model
    or MDC directly                   (synomic/non-synomic, duration)
```

Both sides are recorded as a single Synome entry linking Prime A's isolated position to Prime B's EJRC ingression. The chain of provenance is fully traceable: the Synome records who originated the capital, through which isolated deployment it traveled, and at which Prime it is currently ingressed.

**Prime A's exposure:** exactly the capital committed, 1:1, ring-fenced. Prime A does not participate in Prime B's leverage — it is simply providing capital that Prime B ingresses.

**Prime B's treatment:** the received EJRC is ingressed normally via the leverage ingression curve in `risk-capital-ingression.md`. Quality attributes (synomic status, duration commitment) apply as normal. If the internal egression is between Synomic agents with a Synome-encoded framework, the synomic multiplier applies.

### EJRC Quality in Internal Egression

When JRC is isolated-deployed as EJRC to another Prime:
- If the arrangement is governed by a Synome-encoded framework between Synomic agents: qualifies as **synomic EJRC** at Prime B (2× multiplier on anchor/max)
- If it is a bilateral arrangement without Synome encoding: qualifies as **non-synomic EJRC**
- Duration commitment is the agreed uningression delay between the two Primes

---

## Other Use Cases

Isolated deployment applies wherever a Prime wants to deploy capital into a specific position that should not interact with its general RWA book:

- **Strategic capital commitments** — a Prime providing capital to a specific project, fund, or vehicle
- **Side pockets** — ring-fencing exposure to illiquid or bespoke assets that should not affect the Prime's general leverage ratio
- **MDC direct deployment** — MDC capital deployed into assets via isolated deployment is the standard mode for MDC (see `mezzanine-deployment-capital.md`)

---

## Loss Mechanics

Losses on an isolated position reduce the backing capital directly:

- If backed by **IJRC**: the loss reduces Prime A's IJRC, which reduces its effective JRC, which reduces its SRC ingression capacity and MDC capacity
- If backed by **EJRC**: the loss reduces the EJRC position. Since IJRC and EJRC are pari passu in the going-concern waterfall, this reduces the JRC pool proportionally
- If backed by **MDC**: the loss reduces the MDC position and therefore the MDC liquidation claim

In no case does an isolated deployment loss flow through to the Prime's general leveraged portfolio. The ring-fencing is strict.

---

## Synome Tracking

All isolated deployments are recorded in the Synome with:

- Identity of the capital source (which Prime, which capital type)
- Deployed-to target (asset, counterparty, or receiving Prime)
- Amount and 1:1 mapping
- Duration and exit terms (if applicable)
- For internal egression: link to the receiving Prime's EJRC ingression record

Multi-hop chains (Prime A → Prime B → Prime C) are fully traceable through the Synome. Each hop creates a linked Synome entry. This allows provenance auditing and ensures that loops or circular dependencies can be detected.

---

## Connection to Other Documents

| Document | Relationship |
|---|---|
| `risk-capital-ingression.md` | Leverage ingression model; isolated deployment is outside the ingression curve |
| `mezzanine-deployment-capital.md` | MDC uses isolated deployment as its standard deployment mode |
| `books-and-units.md` | Isolated positions are units in the Prime's book; linked via Synome to the receiving entity |
| `daily-settlement-cycle.md` | Isolated deployment state settled on the daily cycle |
