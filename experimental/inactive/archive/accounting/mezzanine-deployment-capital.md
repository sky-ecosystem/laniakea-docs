# Mezzanine Deployment Capital (Speculative)

**Status:** Speculative — potential future feature. May or may not be implemented. Design is preliminary and subject to significant revision.
**Last Updated:** 2026-04-09

---

## Overview

Mezzanine Deployment Capital (MDC) is a proposed capital tranche that sits structurally between Junior Risk Capital (JRC) and Senior Risk Capital (SRC) in the Prime's capital structure. Unlike JRC and SRC, MDC is not a leverage instrument — it does not amplify the Prime's deployment capacity through the ingression curve. Instead, MDC capital is deployed directly 1:1 into assets without risk-weight or CRR constraints.

MDC's structural position means SRC holders benefit from MDC sitting below them in liquidation priority. In a going-concern scenario MDC is unaffected by operating losses. MDC holders' exposure is binary: they are either paid in full or receive a residual recovery in a Prime liquidation event.

---

## Capital Structure Position

The full Prime capital structure, from first-loss to last-loss:

```
IJRC + EJRC   (pari passu, proportional to nominal)   ← going-concern first loss
Prime Token   (forced inflation before liquidation)    ← recapitalization mechanism
────────────────────────────────── liquidation threshold
MDC           (subordinated claim in liquidation)      ← liquidation residual
SRC           (senior claim in liquidation)            ← liquidation senior
```

### Going-Concern Loss Mechanics

MDC does not absorb losses during normal Prime operations. The going-concern sequence is:

1. Operating losses hit JRC (IJRC and EJRC absorb proportionally by nominal amount)
2. If JRC is exhausted, Prime Token is inflated — the protocol forces issuance of new Prime tokens to raise capital and cover the remaining loss. Inflation continues until the hole is covered or the market stops buying (token price approaches zero)
3. If inflation cannot cover the hole, the Prime is liquidated

MDC holders are unaffected through steps 1 and 2. Their exposure only materializes at step 3.

### Liquidation Mechanics

In a Prime liquidation, all assets are sold and proceeds are distributed in the following order:

1. **SRC paid first** — all SRC holders (GSRC and ISRC leverage) are made whole to the extent possible
2. **MDC receives the residual** — whatever remains after SRC is satisfied is distributed to MDC holders proportionally

JRC holders and Prime token holders receive nothing in liquidation — their claims were extinguished in the going-concern loss sequence and inflation attempt prior to liquidation.

MDC recovery therefore depends on:
- Total liquidation value of the Prime's assets
- Total SRC outstanding at time of liquidation
- If liquidation proceeds > SRC, MDC holders recover the excess
- If liquidation proceeds ≤ SRC, MDC holders recover nothing

---

## Deployment Mechanics

MDC capital is deployed directly into assets on a 1:1 basis. The Prime acts as operator of MDC-funded positions.

**No CRR or risk-weight constraints apply to MDC-deployed assets.** MDC does not go through the leverage ingression curve and does not generate an ingression adjustment on Generator debt. MDC-deployed assets are not included in the Prime's RWA/TRRC calculation. The MDC capital itself is the full risk buffer for the assets it funds — no additional capital adequacy calculation is required.

This means:
- MDC capital of 100 can be deployed into 100 of any asset, regardless of that asset's CRR
- MDC does not increase the Prime's TRC or affect the Prime's Encumbrance Ratio
- MDC-funded positions are tracked in the Synome but are separate from the Prime's leverage book

**Capital source:** MDC can only be funded by isolated capital (TISRC-style). GSRC cannot be used to fund MDC. This ensures that global srUSDS holders are not directly exposed to MDC-style deployment without the protection of the standard leverage ingression framework.

---

## MDC Capacity Limit

The maximum MDC a Prime may hold is:

```
MDC limit = 3 × Total JRC

Where Total JRC = IJRC + all EJRC (nominal)
                  regardless of whether JRC is in isolated deployment mode or not
```

All forms of JRC count toward the base — normie TEJRC, synomic bespoke EJRC, and IJRC — whether or not that JRC has been deployed in isolated deployment mode. A Prime that uses EJRC for isolated deployment into another Prime does not reduce its JRC base for MDC limit purposes.

**Note:** The 3× multiplier is a preliminary parameter and should be reconsidered. It may be appropriate to increase this significantly once the risk dynamics of MDC are better understood in practice. The choice of multiplier involves a tradeoff: a higher multiplier allows Primes to operate larger MDC books relative to their JRC, but increases the operational exposure relative to skin-in-the-game.

### Rationale for JRC-Based Limit

Although MDC does not create leverage, the JRC-based limit exists for two reasons:

1. **Operational quality signal.** JRC represents the Prime's genuine skin in the game. A Prime managing enormous MDC books relative to its JRC has diminishing economic incentive to manage those books carefully. The limit ensures the Prime's own capital remains meaningful relative to total managed exposure.

2. **Indirect JRC exposure.** In a liquidation scenario, losses from any portion of the Prime's portfolio (including JRC-leveraged assets) precede MDC in the going-concern sequence. A Prime with thin JRC relative to large MDC books reaches the liquidation threshold sooner, increasing the probability that MDC holders face an actual liquidation event.

---

## Yield

MDC holders are more junior than SRC holders in liquidation and therefore bear more risk. MDC should earn a higher yield than SRC. The yield spread between MDC and SRC reflects the probability-weighted liquidation shortfall risk.

MDC yield accrues from the deployed assets — MDC holders receive the returns from the positions MDC capital is deployed into, net of the Prime's operating fee.

---

## Relationship to Isolated Deployment

MDC capital can be deployed in isolated deployment mode (see `isolated-deployment.md`). When MDC is isolated-deployed, the deployed assets are ring-fenced from the Prime's general RWA book, and losses reduce the MDC position directly. Isolated deployment is the mechanism by which MDC capital can be directed to specific positions — including providing capital to another Prime as EJRC via internal egression.

---

## Connection to Other Documents

| Document | Relationship |
|---|---|
| `risk-capital-ingression.md` | Ingression model for JRC and SRC; MDC is outside this framework |
| `isolated-deployment.md` | The deployment mode MDC uses |
| `books-and-units.md` | MDC positions are tracked as units in the Prime's book structure |
| `daily-settlement-cycle.md` | MDC capacity and deployment state settled on the daily cycle |
