# Attestor Atom Schema — Custodial-Crypto

**Status:** Resolved for the Phase 1 `custodial-crypto` risk class (2026-05-14). Resolves [`p1-design-followups.md`](p1-design-followups.md) §1.1 for this risk class only.

**Scope:** Custodial-crypto riskbooks (and via them, all exobooks bundled in those riskbooks). Opaque-RWA risk classes (legacy HVB-style, no on-chain visibility) need a richer numeric attestation schema and are out of scope here — not a Phase 1 risk class.

---

## 1. The reframe — why the attestation is boolean

For custodial-crypto, every quantitative CRR input is **insyn**:

| Input | Source |
|---|---|
| Collateral asset + amount | `chain-read` on the borrower's visible on-chain account |
| Debt outstanding, LT, liquidation bonus, derived LTV | `chain-read` on the loan contract |
| Price, order-book depth, volatility history | `market-data-beacon` (Crypto Majors Oracle) |

The borrower's crypto holdings sit in a visible on-chain account; the loan terms are on-chain. Nothing quantitative needs an attestor.

So the attestor is **not** an oracle of loan facts. It is a **legal / operational / credit underwriter** of the things the chain cannot show — and its output is **boolean**. It signs that:

- the legal structure of the deal is sound and enforceable,
- the borrower is a real company in normal credit standing,
- the custodian's licensing / insurance / regulatory status is current.

The original `phase-1-spaces.md` "Attestation model" sketch carried `assets-attested`, `debt-outstanding`, and a 24h `refresh-due`. All three are wrong-headed under this reframe: the first two are now insyn, and the cadence is credit-review-paced, not market-paced. This schema drops them.

## 2. Where the attestation sits

Custodial-crypto has two legs; the attestation lives on the first.

**Leg 1 — Borrower ↔ Halo (no instrument).** The Halo PAU sends USDC/USDT out to the borrower. The only record is synome book atoms: the exobook holds the collateral reference (the borrower's on-chain account, `chain-read`) as its asset side, the disbursed principal as the senior tranche (liability), and borrower equity as the junior tranche. The riskbook holds that senior tranche as its asset (cross-book duality on a plain tranche atom — no ERC-721). **The `riskbook-attestation` atom lives in the riskbook Space and gates whether the riskbook (and all exobooks bundled in it) rolls up.** One attestation per riskbook — the attestor signs the shared structural facts (legal framework, borrower(s), custodian) covering every exobook in that riskbook. Construction of a riskbook around homogeneous structural facts is the v1 discipline that makes this scoping work.

**Leg 2 — Halo ↔ Prime (NFAT instrument).** The Prime deploys capital into the Halo; `record-unit` mints an NFAT (= Halo Unit) into the Prime's PAU. The NFAT is the liability of the halobook and the asset of the primebook. This leg is downstream of the attestation and unaffected by it.

Rollup path: `exobook → riskbook → halobook → (NFAT) → primebook → ER`.

## 3. Schema

```metta
;; in &entity.halo.{halo-id}.riskbook.{rbk-id}
(riskbook-attestation {rbk-id}
   (attestor      {attest-data-{halo-id}-id})  ; per-halo attestor; cert chain in &core.registry.beacon
   (timestamp     T)
   (refresh-due   T+{review-cadence})          ; credit-review paced; governance-set per halo class
   (underwriting  pass)                        ; pass | fail — gates the riskbook (and all exobooks under it)
   (claims                                     ; itemized liability surface; slashing attaches per claim
      (legal-structure-enforceable  true)      ; loan docs valid + enforceable; governing law sound
      (borrower-credit-standing     normal)    ; normal | watch | impaired
      (custodian-compliance-current true))     ; custodian licensing / insurance / regulatory status current
   (scope-ref     {structural-config-hash})    ; content hash over the riskbook's structural config (exobook composition + per-exobook loan terms, borrower(s), custodian, collateral-account binding, collateral asset type)
   (sig           "..."))
```

## 4. Field semantics

- **`underwriting`** — the admission gate. `pass` admits the riskbook (and all exobooks under it) to rollup; `fail` excludes the riskbook (default-deny).
- **`claims`** — the discrete facts the attestor signs under liability, itemized so slashing magnitude can be calibrated per claim (§7). `legal-structure-enforceable` and `custodian-compliance-current` are boolean. `borrower-credit-standing` is three-state: `normal` is unremarkable; `watch` and `impaired` are signals the risk form may consume (§9) — `watch` as a CRR uplift, `impaired` as exclusion. This is the one field beyond pure-boolean, and it is there because borrower creditworthiness is genuinely part of what the attestor underwrites.
- **`scope-ref`** — content hash over the riskbook's *structural* config (its exobook composition, plus per-exobook loan terms, borrower identity, custodian, collateral-account binding, collateral asset type). It binds the boolean to a specific configuration: "I underwrote *this*." A change that moves outside the underwritten structural config forces re-attestation; market state (price, scheduled amortization, LTV drift) does not. Adding or removing an exobook in the riskbook also forces re-attestation. The exact set of structural predicates is the surviving open sub-question (§8).
- **`refresh-due`** — see §5.
- No `assets-attested`, no `debt-outstanding` — those are insyn (`chain-read`), not attested.

## 5. Refresh cadence

Credit-review-paced, not market-paced. The attestor underwrites slow-moving facts (legal structure, borrower credit, custodian compliance); none of them move with price. `review-cadence` is governance-set per halo class — indicatively on the order of a quarter, definitely not the 24h the original sketch carried. A single cadence per attestation atom in v1; per-claim cadences (e.g. a faster touch on `borrower-credit-standing`) are a possible later refinement, deferred.

## 6. Default-deny gate

Consistent with v1-principle #10. A riskbook does **not** roll up (and neither do any of its exobooks) if its attestation is:

- `(underwriting fail)`, or
- stale — `now > refresh-due`, or
- missing.

In any of these cases the risk form excludes the riskbook's positions and the Prime's structbook cannot account for them. This is the integrity discipline that keeps attestors honest and prevents stale legal/credit facts from poisoning the rollup.

## 7. Slashing surface

The `claims` block *is* the slashing surface. The synome cannot verify these facts directly — that is the whole point of the attestor — so slashing is reactive: if a position sours and post-mortem shows a claim was false at attestation time (legal structure unenforceable, borrower already impaired, custodian insurance lapsed), the attestor is slashed. Itemizing the claims lets slashing magnitude scale per claim. The magnitudes themselves are not set here — they belong to the Oracle Entity stub-spec (clean-todo Pass B).

## 8. Open sub-question (surviving)

**`scope-ref` granularity.** The *principle* is settled — `scope-ref` covers structural configuration, not market state. What remains open is the exact list of riskbook + exobook atom predicates that count as "structural" (and therefore re-attestation-forcing). Candidate set: riskbook composition (which exobooks are bundled), plus per-exobook loan terms (LT, liquidation bonus, maturity, governing law), borrower identity, custodian identity, collateral-account binding, collateral asset type. Forcing trigger: building the v1 attestor.

The privacy-bucket question (how to expose loan-level data in aggregate without revealing individual positions) **largely dissolves** for custodial-crypto: the boolean attestation carries no loan-level numbers, so there is nothing to bucket. Privacy is automatic.

## 9. Downstream consequences

**§1.2 — risk-form signature.** The attestation is an **admission gate, not a data source**. The risk form's inputs are `chain-read` (collateral, debt, terms) + `market-data` (price, liquidity, vol) + the boolean gate. The risk form never reads numbers *out of* the attestation; it only checks `underwriting = pass` and may branch on `borrower-credit-standing`.

**§1.3 — CORE integration.** CORE's inputs (LTV, LT, liquidation bonus, collateral asset, borrow value, order-book depth, price history, HHI) are now **entirely insyn** — `chain-read` + `market-data`, zero attestor dependency. The integration question collapses to purely "where does CORE's math run" (A integrate / B proxy / C rebuild), not "how does CORE get its inputs."

**§1.4 — atom-level walkthrough.** The trace's first step is the boolean gate check on each riskbook before any quantitative rollup of its exobooks.

---

## File map

| Doc | Relationship |
|---|---|
| [`p1-design-followups.md`](p1-design-followups.md) | §1.1 is resolved by this doc (custodial-crypto risk class only) |
| [`phase-1-spaces.md`](phase-1-spaces.md) | "Attestation model" section now carries the boolean schema (per the 2026-05-15 topology redesign); the attestor loop lives at `&entity.halo.{id}.custodial-crypto.attest-data` per the per-halo risk class structure |
| [`phase-1-overview.md`](phase-1-overview.md) | Orientation entry point — the Attestor Oracle front anchors here |
| [`../risk-framework/riskbook-layer.md`](../risk-framework/riskbook-layer.md) | §8 example risk form (the equation that consumes the boolean gate) |
| [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) | `attest-data-beacon` class; the attestor's beacon |
