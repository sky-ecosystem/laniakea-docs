# Isolated Deployment

**Status:** Draft (synlang-native rewrite). MDC section is **speculative** — preliminary design, subject to significant revision.
**Last Updated:** 2026-05-07

---

## Scope

**Isolated deployment** is a mode in which JRC or MDC capital is deployed into assets that are **ring-fenced from the Prime's main portfolio**. Isolated assets are excluded from the Prime's TRRC calculation; instead they are mapped 1:1 against the isolated capital that funds them — the isolated capital itself is the full risk buffer, no separate CRR calculation applies.

Isolated deployment **does not create leverage**. It is a direct capital deployment mechanism, not an amplification of the Prime's risk-taking capacity.

This doc covers the mechanism in general (§§1–8) and includes a speculative section on **MDC** — Mezzanine Deployment Capital — which uses isolated deployment as its standard mode (§9).

---

## 1. Definition

A deployment is isolated when:

1. The deployed assets are **excluded from the Prime's portfolio-level TRRC calculation**.
2. The capital backing the deployment is designated as isolated — it cannot simultaneously serve as leverage buffer for the Prime's general book.
3. Losses on the isolated position **reduce the backing capital directly**, not the Prime's general capital pool.
4. The synome records the isolated deployment **separately from the Prime's general book state** — distinct atoms under the Prime's entart subtree, with provenance traceable across hops.

The constraint is:

```
Isolated deployed assets ≤ Isolated capital committed
(1:1 — no leverage ratio applies)
```

---

## 2. Eligible capital

Available to:
- **IJRC** — the Prime's internal junior risk capital
- **EJRC** — external junior risk capital (normie TEJRC or bespoke)
- **MDC** — mezzanine deployment capital (see §9)

**Not available:** GSRC and ISRC leverage capital. SRC goes through the standard leverage ingression framework (per [`capital-stack.md`](capital-stack.md) §3) and contributes to TRC. It is not a direct deployment instrument.

---

## 3. Effect on the Prime's effective JRC

JRC or MDC committed to isolated deployment is **no longer available for other purposes**:

- **IJRC or EJRC** in isolated deployment reduces the Prime's **effective JRC** for leverage purposes — meaning SRC ingression capacity, MDC capacity, and any other JRC-anchored limits are all reduced accordingly.
- **MDC** in isolated deployment reduces the available MDC for other MDC deployments.

Same capital unit can't simultaneously act as leverage buffer for the general book *and* as isolated deployment capital. The Prime must allocate explicitly.

---

## 4. Primary use case: internal egression as EJRC into another Prime

The principal use case for isolated deployment is providing EJRC to another Prime via internal egression — without going through the external LCTS mechanism.

### Mechanics

Prime A designates capital (JRC or MDC) for isolated deployment into Prime B as EJRC:

```
Prime A side                          Prime B side
─────────────────────────────         ─────────────────────────────
Isolated deployment asset             EJRC received from Prime A
  → backed 1:1 by JRC or MDC            → ingressed via leverage curve
  → excluded from Prime A's TRRC        → contributes to Prime B's TRC
  → loss reduces Prime A's JRC          → quality: per ingression model
    or MDC directly                       (synomic / non-synomic, duration)
```

### Synlang form

The two sides express as paired atoms in their respective entart roots:

```metta
;; in &entity.prime.a.root
(isolated-deployment-asset $prime-a $target $amount $epoch
   (provenance $capital-source))                            ; IJRC | EJRC | MDC

;; in &entity.prime.b.root
(ejrc-ingressed $prime-b $source-prime-a $nominal $effective
   (synomic? $bool) (duration-months $n))
```

Both atoms cross-reference each other; the link is auditable. Provenance — who originated the capital, through which isolated deployment it traveled, at which Prime it is currently ingressed — flows through a registry sub-Space (e.g., `&core.registry.cross-prime-flows`, registered at the appropriate sudo boundary) so multi-hop chains are traversable.

Two-tier authority and naming follow `noemar-synlang/topology.md` patterns: the isolated-deployment atom lives in Prime A's entart root; the ingression atom lives in Prime B's entart root; both are gate-mediated writes through `&core.syngate` with the relevant govops-prime beacons signed.

### EJRC quality in internal egression

Quality attributes apply to the EJRC at Prime B per the standard ingression model (`capital-stack.md` §4):

- **Synomic** — if the arrangement is governed by a synome-encoded framework between synomic entities: 2× multiplier on anchor / max
- **Non-synomic** — bilateral arrangement without synome encoding: 1× multiplier
- **Duration commitment** — the agreed uningression delay between the two Primes

### Prime A's exposure

Exactly the capital committed, 1:1, ring-fenced. Prime A does **not** participate in Prime B's leverage; it provides capital that Prime B ingresses normally.

### Prime B's treatment

The received EJRC is ingressed via the leverage ingression curve — same as any other EJRC.

---

## 5. Other use cases

Isolated deployment applies wherever a Prime wants to deploy capital into a specific position that should not interact with its general TRRC book:

- **Strategic capital commitments** — providing capital to a specific project, fund, or vehicle.
- **Side pockets** — ring-fencing exposure to illiquid or bespoke assets that should not affect the Prime's general leverage ratio.
- **MDC direct deployment** — MDC capital deployed into assets via isolated deployment is the standard mode for MDC (see §9).

---

## 6. Loss mechanics

Losses on an isolated position reduce the backing capital directly:

| Backed by | Loss flow |
|---|---|
| **IJRC** | Reduces Prime A's IJRC → reduces effective JRC → reduces SRC ingression capacity and MDC capacity |
| **EJRC** | Reduces the EJRC position; since IJRC and EJRC are pari passu in the going-concern waterfall, this reduces the JRC pool proportionally |
| **MDC** | Reduces the MDC position and therefore the MDC liquidation claim |

In no case does an isolated deployment loss flow through to the Prime's general leveraged portfolio. The ring-fencing is strict.

---

## 7. Synome tracking

All isolated deployments are recorded in the synome with:

- Identity of the capital source (which Prime, which capital type)
- Deployed-to target (asset, counterparty, or receiving Prime)
- Amount and 1:1 mapping
- Duration and exit terms (if applicable)
- For internal egression: link to the receiving Prime's EJRC ingression atom

Multi-hop chains (Prime A → Prime B → Prime C) are fully traceable. Each hop creates a linked atom; loops and circular dependencies are detectable. The whole chain is auditable through entart subtree traversal.

**Vocabulary discipline.** The doc uses the synart layer (entart subtrees of synomic entities) and the registry layer (`&core.registry.…`) explicitly; "synome" is reserved for the ledger as a whole, "synart" for its canonical part, and "telart" for per-teleonome reasoning. Per `noemar-synlang/topology.md` §5–§6.

---

## 8. Settlement

Isolated deployment state settles on the same cycle as everything else. The synserv heartbeat reads `isolated-deployment-asset` atoms when computing TRRC (excluding them from the Prime's portfolio aggregation) and reads `ejrc-ingressed` atoms when computing the receiving Prime's effective JRC. See [`settlement-cycle.md`](settlement-cycle.md).

---

## 9. MDC — Mezzanine Deployment Capital (speculative)

> **Status: Speculative.** Potential future feature. May or may not be implemented. Design is preliminary and subject to significant revision.

### Position in the capital structure

```
IJRC + EJRC   (pari passu, proportional to nominal)   ← going-concern first loss
Prime Token   (forced inflation before liquidation)    ← recapitalization
────────────────────────────────── liquidation threshold
MDC           (subordinated claim in liquidation)      ← liquidation residual
SRC           (senior claim in liquidation)            ← liquidation senior
```

Unlike JRC and SRC, **MDC is not a leverage instrument**. It does not amplify the Prime's deployment capacity through the ingression curve. It is deployed directly 1:1 into assets without risk-weight or CRR constraints.

MDC's structural position means SRC holders benefit from MDC sitting below them in liquidation priority. In a going-concern scenario MDC is unaffected by operating losses; MDC holders' exposure is binary — paid in full or receive a residual recovery in a Prime liquidation event.

### Going-concern loss mechanics

MDC does not absorb losses during normal Prime operations:

1. Operating losses hit JRC (IJRC + EJRC absorb proportionally by nominal)
2. If JRC is exhausted, Prime Token is inflated to raise capital. Inflation continues until the hole is covered or the market stops buying (token price approaches zero)
3. If inflation cannot cover, the Prime is liquidated

MDC holders are unaffected through steps 1 and 2.

### Liquidation mechanics

In a Prime liquidation, all assets are sold and proceeds distributed in this order:

1. **SRC paid first** — all SRC holders (GSRC and ISRC) made whole to the extent possible.
2. **MDC receives the residual** — whatever remains after SRC is satisfied is distributed to MDC holders proportionally.

JRC holders and Prime token holders receive nothing in liquidation — their claims were extinguished in the going-concern sequence and inflation attempt.

MDC recovery depends on:
- Total liquidation value of the Prime's assets
- Total SRC outstanding at time of liquidation
- If liquidation proceeds > SRC: MDC holders recover the excess
- If liquidation proceeds ≤ SRC: MDC holders recover nothing

### Deployment mechanics

MDC capital is deployed directly into assets 1:1. The Prime acts as operator of MDC-funded positions.

**No CRR or risk-weight constraints apply to MDC-deployed assets.** MDC does not go through the leverage ingression curve and does not generate an ingression adjustment on Generator debt. MDC-deployed assets are not included in the Prime's TRRC calculation. The MDC capital is itself the full risk buffer for the assets it funds — no additional capital adequacy calculation is required.

This means:
- MDC capital of 100 can be deployed into 100 of any asset, regardless of that asset's CRR
- MDC does not increase the Prime's TRC or affect the Encumbrance Ratio
- MDC-funded positions are tracked in the synome but separate from the Prime's leverage book

**Capital source:** MDC can only be funded by isolated capital (TISRC-style). GSRC cannot be used to fund MDC. This ensures that global srUSDS holders are not directly exposed to MDC-style deployment without the protection of the standard leverage ingression framework.

### MDC capacity limit

```
MDC limit = 3 × Total JRC

Where Total JRC = IJRC + all EJRC (nominal),
                  regardless of whether JRC is in isolated deployment mode or not.
```

All forms of JRC count toward the base. A Prime that uses EJRC for isolated deployment into another Prime does not reduce its JRC base for MDC limit purposes.

**The 3× multiplier is preliminary** and should be reconsidered. It may be appropriate to increase this significantly once the risk dynamics of MDC are better understood in practice. Tradeoff: a higher multiplier allows Primes to operate larger MDC books relative to JRC but increases operational exposure relative to skin-in-the-game.

### Rationale for the JRC-based limit

Although MDC does not create leverage, the JRC-based limit exists for two reasons:

1. **Operational quality signal.** JRC represents the Prime's genuine skin in the game. A Prime managing enormous MDC books relative to its JRC has diminishing economic incentive to manage carefully. The limit ensures the Prime's own capital remains meaningful relative to total managed exposure.

2. **Indirect JRC exposure.** In a liquidation scenario, losses from any portion of the Prime's portfolio (including JRC-leveraged assets) precede MDC in the going-concern sequence. A Prime with thin JRC relative to large MDC books reaches the liquidation threshold sooner, increasing the probability that MDC holders face an actual liquidation event.

### Yield

MDC holders are more junior than SRC holders in liquidation and bear more risk. MDC should earn a higher yield than SRC; the spread reflects probability-weighted liquidation shortfall risk.

MDC yield accrues from the deployed assets — MDC holders receive the returns from the positions MDC capital is deployed into, net of the Prime's operating fee.

### Relationship to isolated deployment (general mechanism)

MDC capital can be deployed in isolated deployment mode (the general mechanism in §§1–8). When MDC is isolated-deployed, the deployed assets are ring-fenced from the Prime's general TRRC book, and losses reduce the MDC position directly. Isolated deployment is the mechanism by which MDC capital can be directed to specific positions — including providing capital to another Prime as EJRC via internal egression.

---

## 10. Vocabulary discipline

The doc previously used "Synome-MVP" and other transitional vocabulary loosely. The synlang-native usage is:

- **Synome** — the ledger as a whole.
- **Synart** — the canonical part of the synome (entart subtrees + universal `&core.*` Spaces). Where atoms live.
- **Telart** — per-teleonome reasoning (private, not replicated). Not relevant to isolated deployment.
- **`&core.…`** — universal registries (constitutional / framework / library / etc.).
- **`&entity.…`** — entity entart subtrees.

When this doc says "tracked in the synome" it means specifically: atoms in the Prime's entart subtree, with cross-Prime provenance through a registry sub-Space.

---

## File map

| Doc | Relationship |
|---|---|
| [`README.md`](laniakea-docs/accounting/README.md) | Accounting directory index |
| [`capital-stack.md`](capital-stack.md) | Leverage ingression model; isolated deployment is outside the ingression curve and reduces effective JRC for leverage |
| [`settlement-cycle.md`](settlement-cycle.md) | Isolated deployment state settles on the daily cycle |
| [`../risk-framework/book-primitive.md`](../risk-framework/book-primitive.md) | 6-tuple book structure; isolated positions are units linked across entarts |
| [`../risk-framework/tranching.md`](../risk-framework/tranching.md) | Exoassets / exoliabs / waterfall (MDC sits between JRC and SRC in liquidation only) |
| [`../noemar-synlang/topology.md`](../noemar-synlang/topology.md) | Entart subtree pattern; `&core.registry.…` for cross-entity provenance |

---

## One-line summary

**Isolated deployment ring-fences IJRC / EJRC / MDC into 1:1 deployments outside the Prime's TRRC book — reducing effective JRC for leverage purposes, recording paired atoms across entarts for provenance, and serving as the canonical mechanism for one Prime to provide EJRC to another via internal egression; MDC (speculative) uses this mode for direct deployment with a 3 × JRC capacity limit and a liquidation-only claim subordinated to SRC.**
