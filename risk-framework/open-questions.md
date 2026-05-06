# Risk Framework — Open Questions

**Status:** Living document. Tracks risk-framework design questions
that have been deferred rather than answered. Each entry: what the
question is, why it's blocked, and what would force a decision.

Add new entries at the bottom as they emerge. When an entry is
resolved, mark it RESOLVED with a date and where the decision landed
(commit, doc section, etc.) and leave the entry in place for history.

Last updated: 2026-05-03.

---

## Q24 — Attestor atom schema + reconciliation cycle

**What:** Atom shape for off-chain attestation claims, plus the
reconciliation cycle for cases where on-chain endoscrapers can't
verify the claim (off-chain custody, off-chain contract terms,
compliance facts).

**Why deferred:** The cert/auth/beacon-class machinery already exists
(per `../noemar-synlang/runtime.md`); the genuinely new design is the
attestation atom schema and the reconciliation flow. No concrete
attestor exists yet to drive the schema choice.

**Forcing trigger:** Building the v1 crypto-collateralized lending
test attestor (per `../inactive/archive/risk-framework-redesign-2026-05-03.md`
§3.4). The test attestor is the first concrete instance and will
shape the schema.

**Cross-refs:** `noemar-synlang/beacons.md` (input beacon role
includes attestor), `../inactive/archive/risk-framework-redesign-2026-05-03.md`
§3.4.

---

## Q26 — Privacy buckets for v1 crypto-lending test

**What:** Bucket boundaries and code lists for the v1 test's
privacy-preserving onboarding — LTV bucket boundaries, term bucket
boundaries, jurisdiction code list, custodian ID schema.

**Why deferred:** Bucket choices ARE the regulatory surface — they
define what governance approves at category level. Choosing them
needs both operational input (what loans the test will actually
include) and governance input (what disclosure level is acceptable).

**Forcing trigger:** Actual loan onboarding for the v1 test. Until
real deals are being categorized, the bucket boundaries are
hypothetical.

**Cross-refs:** `../inactive/archive/risk-framework-redesign-2026-05-03.md`
§3.5 (privacy approach for v1).

---

## Q27 — Crypto stress scenario calibration

**What:** Concrete parameter values for the crypto stress scenarios
used by the v1 Riskbook category equation. Specifically:
- Magnitude of `severe-crypto-correlated-crash` (BTC/ETH drop, window)
- Liquidation-window duration assumptions
- `stETH-ETH-peg-break` parameters
- USDC/USDT depeg priors
- Custodian-failure binary probability

**Why deferred:** Hand-tuned values are workable for v1, but they
need governance discussion before they bind real capital
requirements. Calibration is also tied to the broader stress-scenario
library curation effort that hasn't started.

**Forcing trigger:** Computing actual CRR values for v1 positions —
the moment governance has to defend a CRR number, the stress
scenarios behind it become load-bearing.

**Cross-refs:** `../inactive/archive/risk-framework-redesign-2026-05-03.md`
§3.6 (stress scenarios for v1), `noemar-synlang/risk-framework.md` §6
(stress simulation as canonical equation type).

---

## Correlation framework specifics

**What:** Three under-specified parts of `correlation-framework.md`:
- Stress calibration — how to set `L(c, s)` parameters for each
  category × scenario pair
- Multi-group assets — how to handle exposures that fall in multiple
  categories without double-counting or under-penalizing
- Aggregation method — independent worst-case caps (Method A) vs
  joint optimization (Method B) as canonical

**Why deferred:** The cap-enforcement mechanism is settled; the
calibration methodology is deferred until concentration limits
actually bind in practice. Premature calibration would lock in
parameters that may not survive contact with real portfolios.

**Forcing trigger:** When portfolio composition first approaches a
category cap, or when governance proposes a new category — both will
force a calibration decision for that category.

**Cross-refs:** `correlation-framework.md` §"How Caps Are Set" and
"Open Questions"; `../inactive/archive/risk-framework-redesign-2026-05-03.md`
Part 7 item 4 (concentration L3 deferred).

---

## USDS lot-age tracking infrastructure

**What:** How to track USDS lot ages in real time so the Lindy
Duration Model can produce a current liability-duration distribution.
Includes scraping USDS, DAI (DAI→USDS migration), and sUSDS
(savings-tier holders).

**Why deferred:** v1 uses manual governance-set capacity (per
`../inactive/archive/risk-framework-redesign-2026-05-03.md` §3.8 carve-out 1). Real-time
Lindy is a Phase 2+ feature that requires the data infrastructure to
exist first.

**Forcing trigger:** When manual structural-demand allocations need
to be replaced with Lindy-driven dynamic allocations — likely when
the v1 test scales beyond a small fixed allocation per Star Prime.

**Cross-refs:** `duration-model.md` §"Two-Layer Capacity Calculation"
(the Lindy layer requires this data), `../inactive/archive/risk-framework-redesign-2026-05-03.md`
§1.13 (structural demand scraping architecture) and §3.7 (Phase 1
manual override).

---

## How to add a new entry

When a new question gets deferred (instead of decided), add an entry
at the bottom with:
- `## <short title>`
- **What:** one paragraph stating the question
- **Why deferred:** one paragraph on what's blocking
- **Forcing trigger:** what would make this need an answer
- **Cross-refs:** which docs / sections relate

When an entry is answered, prepend `**RESOLVED <date>:**` to the title
and add a short note about where the decision landed. Keep the
original question text intact for history.
