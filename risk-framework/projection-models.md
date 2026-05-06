# Projection Models

**Status:** Draft (Phase 2 layer doc, 2026-05-05)

The pattern by which complex or non-tranchable positions enter the risk framework. Each category brings a **projection function** that converts the position into a stress-loss number under each scenario. Sophisticated finance lives in the projection layer; the substrate stays clean.

Companion to:
- `book-primitive.md` — rules attached to books and projection models are complementary
- `risk-decomposition.md` — projection-model risk is one capital dimension
- `tranching.md` — directly-tranchable positions don't need projection models; everything else does
- `riskbook-layer.md` — Riskbook category equations consume projection models

---

## TL;DR

The substrate (book primitive + tranching + currency frame) handles directly-modelable positions: linear claims, tranche structures, native asset holdings. **Anything more complex** — vanilla options, callable bonds, MBS with prepayment, CDS, Asian/lookback options, cat bonds — gets handled via a **projection model** declared by the position's category.

A projection model is a function: `(position, scenario) → stress-loss-number`. It can be analytical (Black-Scholes for vanilla options), simulation-based (Monte Carlo for path-dependent), lattice-based (callable bonds), or parametric (default probability × LGD for CDS).

**Projection-model risk is its own capital dimension** — categories with weaker projection models (newer instruments, less-tested math, more degrees of freedom in calibration) carry an explicit "model uncertainty haircut" on top of the projected number. The framework's epistemics are first-class.

---

## Section map

| § | Topic |
|---|---|
| 1 | Why projection models exist |
| 2 | The projection contract |
| 3 | Categories declare projection models |
| 4 | Examples by position type |
| 5 | Rules vs projections — complementary |
| 6 | Projection-model risk as own capital dimension |
| 7 | One-line summary |

---

## 1. Why projection models exist

The substrate was designed to handle the cases that compose cleanly:
- Direct asset holdings (ETH, USDC, T-bills) — read stress from the asset's canonical liquidity profile
- Tranched exobooks (Sparklend, NFAT, ABF) — propagate asset stress through the tranche waterfall
- Linear claims with deterministic payoffs

For **everything else**, the substrate would either need to natively model every weird position type (huge complexity, brittle to new instruments) or refuse to model them at all (CRR 100% on most of structured finance).

The projection-model pattern is the third option:

> Each category brings a function that converts the position into a stress-loss number under each scenario. The substrate stays clean; the sophistication lives in the projection layer.

This is structurally identical to how option-pricing libraries work: the option's structure is a category, the pricing model is a projection function, the inputs are position parameters and market state, the output is a number. The framework lets categories carry projection models without dragging the model's machinery into the substrate.

---

## 2. The projection contract

A projection model is a function with this signature:

```
project: (position, scenario) → stress-loss-number
```

Where:
- **Position** is the structural specification (notional, strike, expiry, terms, etc.)
- **Scenario** is a coordinated stress case from `&core-framework-stress-scenarios` (e.g., severe-correlated-crash with all stress dimensions parameterized)
- **Stress-loss-number** is the dollar (or frame-currency) loss the position would realize under that scenario

The projection function may be:
- **Analytical** — closed-form formula (Black-Scholes for vanilla options)
- **Simulation-based** — Monte Carlo over stochastic paths
- **Lattice-based** — binomial/trinomial trees for path-dependent options
- **Parametric** — simple parameterized functions (default-prob × LGD for CDS)
- **Machine-learned** — a model trained on historical stress data

The contract is the same regardless of implementation: given a position and scenario, return a stress-loss number.

---

## 3. Categories declare projection models

Each category in `&core-framework-risk-categories` may declare a `projection-model` along with its composition constraints:

```metta
(risk-category-def vanilla-european-call
   (level position-instrument)
   (projection-model black-scholes
      (variables strike expiry notional underlying-price implied-vol risk-free-rate)
      (under-scenario $s
         (let* (($u-stressed (apply-scenario $s underlying-price))
                ($v-stressed (apply-scenario $s implied-vol)))
           (compute-bs-pnl $u-stressed $v-stressed strike expiry notional)))))
```

The Riskbook category equation that holds this position invokes the projection model:

```metta
(= (riskbook-position-loss $position $scenario)
   (let (($cat (category-of $position)))
      (project-with-model (projection-model-of $cat) $position $scenario)))
```

**Default-deny applies:** categories without a declared projection-model get CRR 100%. The framework refuses to model what it doesn't have a projection for, rather than silently lowering the bar.

---

## 4. Examples by position type

| Position type | Projection model |
|---|---|
| Senior loan tranche | Direct (tranche waterfall, per `tranching.md`) |
| ETH holding | Direct (asset stress profile, per `asset-classification.md`) |
| Vanilla European call/put option | Black-Scholes (or Heston, local-vol) → stress P&L |
| American option | Lattice (binomial/trinomial) → stress price |
| Callable bond | OAS / lattice / prepayment model → stress price |
| MBS with prepayment | Prepayment model → stress cashflows |
| CDS | Default probability × LGD → stress payoff |
| Asian/lookback option | Monte Carlo or analytic → stress price |
| Cat bond | Probability of trigger × payoff → stress |
| Convertible bond | Combined credit + equity-option model → stress price |
| Variance swap | Variance forecast model → stress payoff |

Vanilla holdings → trivial projection (linear pass-through). Sophisticated structures → sophisticated projections. Categories without declared projection → CRR 100% (default-deny).

The projection layer is where domain expertise lives. A category can declare a state-of-the-art projection (e.g., a calibrated Heston model with a stochastic volatility surface) and the substrate just runs it. A category can also declare a simple conservative projection (e.g., 100% loss on trigger) and the substrate runs that. The substrate doesn't care about the projection's sophistication; it cares about correctness within the projection's declared validity.

---

## 5. Rules vs projections — complementary

Rules (per `book-primitive.md` §4) and projection models are complementary tools, not alternatives:

| | Rules | Projection models |
|---|---|---|
| **Express what** | The contract DOES — the truth of the obligation | An analytical method for computing risk under stress |
| **Used at** | Runtime (book state evolves per the rules) | Risk computation (capital math at one moment) |
| **When useful** | When obligation dynamics need to be tracked accurately | When the rule is too computationally heavy to inline at risk-comp time |
| **Verifiability** | Synart-resolved code; warden re-derivable | Same — projection is also synlang |

A vanilla call can be modeled as a rule (conditional payoff at expiry: `max(spot − strike, 0)`) AND as a Black-Scholes projection. The rule expresses what the contract IS; the projection model expresses what it's WORTH UNDER STRESS. Both can coexist.

For complex contracts (callable bonds, MBS, accumulators), running the full rule across stress paths via Monte Carlo is one valid approach; using a calibrated projection model is another. The framework supports both. Categories choose based on computational cost vs accuracy trade-offs.

---

## 6. Projection-model risk as own capital dimension

A projection model has uncertainty. Black-Scholes assumes log-normal returns; reality has fat tails. Local-vol calibration extrapolates beyond observable strikes. Monte Carlo has finite-sample error. Newer instruments have less-tested math.

This uncertainty should be **first-class in the framework's capital math**:

```metta
(risk-category-def some-novel-derivative
   (projection-model novel-stochastic-model
      ;; ... projection definition ...)
   (model-uncertainty-haircut 0.20))   ; 20% haircut on top of projected number
```

The model-uncertainty haircut is a category-level parameter set by governance. Higher for newer / less-tested / more-parameterized models; lower for well-established / parsimonious / well-calibrated models. The haircut is applied as a multiplier on the projected number when computing capital.

This makes the framework's epistemics first-class: it admits when it's less sure and reserves accordingly.

| Model status | Typical haircut |
|---|---|
| Black-Scholes for vanilla options (decades of validation) | ~0% |
| Lattice models for American options (well-established) | ~0–5% |
| Heston / local-vol (calibrated, established) | ~5–10% |
| Monte Carlo for path-dependent (well-defined) | ~5–15% |
| Novel parametric models | ~20–30% |
| Bleeding-edge ML-based projections | ~30–50% |
| No declared projection | CRR 100% (default-deny) |

The exact numbers are governance choices; the architecture exposes the dimension.

### What the framework cannot model

The framework is honest about its limits:

- **Multi-agent strategic equilibrium / game theory** — rules express what one party will do; can't natively model what counterparties will do under stress
- **Subjective contracts** — "best efforts," "commercially reasonable," "in good faith" have legal meaning but aren't deterministic
- **Genuinely novel risk modes** — stress libraries are backward-looking; can't see modes we haven't conceived of
- **Recursive market impact** — when we liquidate, we move the market; slippage models capture current depth but not "the depth disappears when other large holders are doing the same thing"

For each of these, the answer is: declare conservative defaults, willingness to use CRR 100%, and rely on governance discipline + scenario library curation to expand coverage over time.

---

## 7. One-line summary

**Categories declare projection models — functions from (position, scenario) to stress-loss-number — that handle complex positions without dragging the math into the substrate; the substrate stays clean for the directly-modelable cases (asset holdings, tranches, linear claims) and lets sophisticated finance live in the projection layer; rules and projection models are complementary, not alternatives; projection-model uncertainty is a first-class capital dimension via category-level haircuts; categories without declared projections fall through to CRR 100% (default-deny).**

---

## File map

| Doc | Relationship |
|---|---|
| `book-primitive.md` | Rules attached to books — complementary to projection models |
| `risk-decomposition.md` | Projection-model risk is one capital dimension |
| `tranching.md` | Tranche structures don't need projections; everything else does |
| `riskbook-layer.md` | Riskbook category equations consume projection models |
| `currency-frame.md` | Projections operate on stressed values that already include currency frame translation |
| `asset-classification.md` | Asset-level stress profiles are inputs to projection models |
| `capital-formula.md` | Projection outputs propagate into the per-position capital formula |
