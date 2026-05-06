# Currency Frame

**Status:** Draft (Phase 2 conceptual core, 2026-05-05)

The accounting layer of the risk framework. Distinguishes the **frame** (abstract unit of account) from the **instrument** (concrete realization with its own stress profile). Defines how the Riskbook translates between native denominations and the Generator's frame, and why the framework is multi-generator-ready even though v1 is single-generator.

Companion to:
- `book-primitive.md` — the 6-tuple where `frame` lives as one component
- `tranching.md` — tranches have denominations, which are instruments, which translate via frames
- `riskbook-layer.md` — the layer where instrument-to-frame translation actually happens

---

## TL;DR

Two distinct concepts that used to be collapsed:

| Concept | What it is | Examples |
|---|---|---|
| **Frame** | Abstract unit of account in which value is measured. Set top-down by the Generator. | USD, EUR, BTC |
| **Instrument** | Concrete realization with its own stress profile relative to its frame | USDS, USDC, USDT (USD-frame proxies); EURC (EUR-frame proxy); BTC (its own native frame); ETH (volatile asset) |

Frame inheritance runs top-down: Genbook → Primebook → Halobook → Riskbook all inherit the Generator's frame. Instrument flexibility runs bottom-up: a Halo unit can hold positions in any instrument as long as it translates correctly to the inherited frame.

The **Riskbook is the translation layer**. Below it: arbitrary denominations. Above it: everything is in the Generator's frame, with stress declared.

---

## Section map

| § | Topic |
|---|---|
| 1 | Why frame ≠ instrument |
| 2 | Currency taxonomy |
| 3 | Frame inheritance |
| 4 | The Riskbook as translation layer |
| 5 | Multi-generator readiness |
| 6 | One-line summary |

---

## 1. Why frame ≠ instrument

In casual finance, "USD" usually means whatever you pay or receive in dollars — the abstract unit and the concrete instrument get used interchangeably. In a regulated synome, the distinction matters.

**Frame** is what value is measured *in*. A book denominated in USD frame means its assets, liabilities, and equity are all expressed in USD. Frame is abstract — you don't hold "USD frame"; you hold instruments that map to it.

**Instrument** is what you concretely hold. USDC is a USD-frame instrument, but USDC ≠ USD. USDC has its own depeg risk: at $0.95 it's still "1 USDC" but its USD-frame value is $0.95, not $1.00. The instrument-to-frame mapping is the place where stress lives.

**Why the distinction is structurally important.** A Prime can deploy USDT into a Halo unit. The Halo holds USDT positions; its Halobook is still USD-frame because the Generator (USDS Generator → USD frame) inherits down. The instrument flexibility (you can hold whatever stablecoin the Riskbook category accepts) doesn't break frame consistency (everything translates to USD with declared depeg stress).

Without this split, every book would have to commit to one specific instrument as its accounting unit, and changing instruments (or holding multiple) would force frame changes upstream. The split decouples the two: pick an instrument because it's operationally useful; the frame stays canonical.

---

## 2. Currency taxonomy

Currencies fall into three kinds, each with a distinct stress profile:

| Kind | What it is | Risk model | Examples |
|---|---|---|---|
| `unit-of-account` | Abstract reference, not held directly | None — it's the measuring stick | USD, EUR, JPY |
| `stablecoin-proxy` | Concrete instrument intended to track a unit-of-account | Depeg stress (probability + magnitude) | USDS, USDC, USDT (track USD); EURC (tracks EUR) |
| `native-volatile-asset` | Concrete instrument that *is* its own frame | Volatility stress (price changes relative to other frames via oracle) | BTC (its own native frame); ETH (volatile, USD-equivalent via oracle) |

Each currency declares:
- **Frame** it's denominated in (USD, EUR, BTC, etc.)
- **Stress profile** relative to its frame (depeg distribution for proxies; volatility for native assets)
- **Correlation** with other currencies (for joint-stress scenarios)
- **FX stress profile** per pair (for cross-currency conversions)

```metta
(currency-def usdc
   (kind stablecoin-proxy)
   (frame usd)
   (depeg-stress
      (scenario severe-correlated-crash (drop 0.05))
      (scenario credit-crisis           (drop 0.02))
      (scenario stable                  (drop 0.001)))
   (correlation-with usdt 0.85))

(currency-def eth
   (kind native-volatile-asset)
   (frame eth)                                            ; its own frame
   (oracle-pair eth/usd)
   (volatility-stress
      (scenario severe-correlated-crash (drop 0.55))
      (scenario credit-crisis           (drop 0.20))
      (scenario stable                  (drop 0.05)))
   (correlation-with btc   0.85)
   (correlation-with stETH 0.95))
```

These atoms live in `&core-registry-currency` (identity) and `&core-framework-currency-stress` (stress profiles). The split is intentional: identity is ~immutable; stress profiles are recalibrated more often.

---

## 3. Frame inheritance

Frame propagates top-down from the Generator. The USDS Generator is USD-frame; everything below it is USD-frame:

```
Generator (USGE)        — USD frame
   ↓
Genbook                 — USD frame
   ↓
Primebook               — USD frame
   ↓
Halobook                — USD frame
   ↓
Riskbook                — USD frame
   ↓
(translation happens here)
   ↓
Exobooks / exo assets   — native denominations (USDC, USDT, ETH, BTC, real cash, etc.)
```

A Halo deploying USDC into a position has a USD-frame Halobook holding USDC instruments; the Halobook's numbers are in USD, with USDC depeg stress applied at the translation layer. A Halo deploying ETH into a position has a USD-frame Halobook holding ETH instruments; ETH is volatility-stressed via its USD-pair oracle.

**Why top-down.** The Generator defines what unit it issues claims in (USDS, denominated in USD). All upstream books eventually redeem to the Generator, so they have to denominate in the same frame to make redemption math cleanly defined. Frame inheritance is the structural enforcement of "everything that flows up to the Generator speaks the Generator's language."

---

## 4. The Riskbook as translation layer

The Riskbook is where messy reality enters the synomic accounting frame:

> Below the Riskbook, the world has its own denominations (USDC positions, ETH collateral, real-world cash flows). At the Riskbook, you accept "this thing in frame X is worth Y in my frame, with stress profile Z." Above the Riskbook, everything is in the Generator's frame.

What the Riskbook does:
1. **Accepts external assets in their native denominations** — exo units pointing to USDC positions, ETH collateral, real-world receivables, etc.
2. **Applies depeg/FX stress for cross-currency equivalences** — USDC at "1.0 × USD with X% depeg stress" is the standard pattern
3. **Translates to the Generator's frame** — the Riskbook's issued unit is denominated in the inherited frame
4. **Issues Riskbook units that upstream books can consume as frame-pure** — the Halobook holding a Riskbook unit doesn't need to know what currencies the Riskbook holds; it just knows the unit's value in the shared frame

This decouples upstream books from instrument complexity. The Halobook composes Riskbook units assuming all are frame-pure; the Riskbook does the messy translation work, declaring its assumptions transparently.

### The "1:1 lock" calibration risk

When a Riskbook accepts USDC at "1.0 × USD with 5% depeg stress at the severe scenario," the 5% is a model assumption. If realized depeg approaches 5%, the assumption is breaking. This requires governance discipline:
- Cadence for stress-profile recalibration
- Alarms when realized depeg approaches modeled limits
- Mechanism to update the stress profile and propagate the update downstream

This is one of the open governance items tracked in `open-questions.md`. V1 uses hand-tuned conservative profiles without automated alarms.

---

## 5. Multi-generator readiness

V1 of the synome has **one Generator** (USGE → USDS, USD-frame). The framework is multi-generator-architecturally-ready — the design doesn't preclude future multi-generator Primes — but no second generator exists yet.

Future shape (not v1):
- Multiple Generators, each with its own frame (USDS / USD, EURS / EUR, BTC-G / BTC, etc.)
- Primes may serve a single Generator or multiple
- Per-Generator Genbook + Primebook
- Cross-Generator interactions happen at the Riskbook layer (with explicit FX-stress translation)

What v1 commits:
- Single-Generator scaffold (USGE)
- All books inherit USD frame
- Cross-currency translation happens at Riskbook layer (even though everything resolves to USD)
- The mechanism that handles future multi-Generator is the same mechanism that handles current cross-currency — `(serves-generator $prime $generator)` registry; one Primebook per generator served

This means cross-Generator architecture lands without rework when the second Generator goes live; the v1 "single Generator translates to USD" pattern is just a degenerate case of the multi-Generator pattern with N=1.

### Tranche-frame mismatches (deferred)

A tranche may, in principle, be denominated in a frame different from its book — e.g., a USD-frame book with a EUR-denominated tranche claim. This pattern is real (cross-currency tranches exist in structured finance) but adds complexity that v1 doesn't need. Deferred to v2+; flagged here so the v1 schema doesn't preclude it.

---

## 6. One-line summary

**Frame is the abstract unit of account a book is measured in (USD, EUR, BTC); instrument is the concrete realization with its own stress profile (USDS, USDC, ETH); frame inherits top-down from the Generator (Genbook → Primebook → Halobook → Riskbook); the Riskbook is the translation layer where native denominations enter the synomic accounting frame with declared stress; multi-generator architecture is ready but v1 is single-Generator (USGE → USDS → USD frame).**

---

## File map

| Doc | Relationship |
|---|---|
| `book-primitive.md` | The 6-tuple where `frame` lives as one component |
| `tranching.md` | Tranche denominations (instruments) translate via frames |
| `risk-decomposition.md` | Stress profiles for instruments (depeg, volatility) feed forced-loss math |
| `riskbook-layer.md` | Where instrument-to-frame translation actually happens; Riskbook category equations consume per-currency stress profiles |
| `asset-classification.md` | Per-asset canonical stress profiles include their currency dimension |
