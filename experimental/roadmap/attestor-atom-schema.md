# Attestor Atom Schema — Custodial-Crypto

**Status:** Resolved for the Phase 1 `custodial-crypto` risk class (updated 2026-05-17).

**Scope:** Custodial-crypto borrower readiness, borrower admission, riskbook admission, and individual exobook term verification. Opaque-RWA risk classes (legacy HVB-style, no on-chain visibility) need a richer numeric attestation schema and are out of scope here.

---

## 1. The reframe

For custodial-crypto, every quantitative CRR input is **insyn**:

| Input | Source |
|---|---|
| Collateral asset + amount | `CHAINREAD` on the borrower's collateral account |
| Debt outstanding, LT, liquidation bonus, derived LTV | `CHAINREAD` on the loan/configurator contracts |
| Price, liquidity, volatility, impact, liquidation-overhang history | Crypto Majors market-memory oracle |

The attestor is therefore not an oracle of loan facts. It is a legal / operational / credit underwriter of what the chain cannot show — its output is readiness/admission/term verification: borrower setup (disbursement + collateral account, custody, legal framework) acceptable before Core Council inclusion, Configurator / aBEAM whitelist path completed for final admission, riskbook shared structure underwritten, exobook maturity / TTM and cash-conversion terms enforceable.

No `assets-attested`, no `debt-outstanding`, no 24h market refresh — those fields are insyn or irrelevant to the attestor cadence.

---

## 2. Account Vocabulary

The durable pair is:

| Term | Meaning |
|---|---|
| **disbursement account** | Borrower-controlled Ethereum address that receives loan principal from the Halo PAU. |
| **collateral account** | Linked account the exobook tracks and expects to be able to liquidate against; attestors verify legal claim, custody setup, and account binding. |

Disbursement-account onboarding matches onboarding into the Configurator smart contract. It is not a loose address field.

---

## 3. Borrower Readiness and Admission

Borrower onboarding has two boolean steps because Core Council / Configurator inclusion cannot be attested as current before it happens.

1. `synops-halo-{id}` writes a proposed borrower setup into the per-halo risk-class Space and submits a Core Council request only after the class-accordant attestor says the setup is ready for inclusion.
2. Core Council / Configurator inclusion is recorded through `relay-core-govops`.
3. The class-accordant `attest-data-{halo-id}` beacon then posts final borrower admission with `configurator-whitelist-current true`.

The final borrower admission is the rollup gate. Readiness is the gate for requesting Configurator inclusion, not for rolling up exposure.

```metta
;; in &entity.halo.{halo-id}.custodial-crypto
(proposed-borrower-setup {borrower-id}
   (proposed-by           {synops-halo-{halo-id}-id})
   (timestamp             T)
   (disbursement-account  ethereum {addr})
   (collateral-account    ethereum {addr})
   (custodian             {custodian-id})
   (legal-framework-ref   {legal-ref})
   (scope-ref             {borrower-setup-hash}))
```

```metta
;; in &entity.halo.{halo-id}.custodial-crypto
(borrower-readiness-attestation {borrower-id}
   (attestor              {attest-data-{halo-id}-id})
   (timestamp             T)
   (refresh-due           T+{readiness-review-cadence})
   (readiness             pass)                  ; pass | fail
   (claims
      (legal-framework-enforceable    true)
      (account-binding-valid          true)
      (custody-setup-current          true)
      (borrower-credit-standing       normal))   ; normal | watch | impaired
   (scope-ref             {borrower-setup-hash})
   (sig                   "..."))
```

The readiness claims are suitable evidence for `request-borrower-inclusion`; they deliberately do not claim that the Configurator whitelist is already current.

```metta
;; in &entity.halo.{halo-id}.custodial-crypto
(custodial-borrower-admission {borrower-id}
   (attestor              {attest-data-{halo-id}-id})
   (timestamp             T)
   (refresh-due           T+{borrower-review-cadence})
   (status                ok)                    ; ok | watch | blocked
   (disbursement-account  ethereum {addr})
   (collateral-account    ethereum {addr})
   (claims
      (configurator-whitelist-current true)
      (legal-framework-enforceable    true)
      (account-binding-valid          true)
      (custody-setup-current          true)
      (borrower-credit-standing       normal))   ; normal | watch | impaired
   (scope-ref             {borrower-setup-hash})
   (sig                   "..."))
```

If borrower admission is missing, stale, blocked, or scope-mismatched, no exobook for that borrower can roll up.

---

## 4. Riskbook / Exobook Attestation

The riskbook attestation gates shared legal / custody / credit structure for a homogeneous bundle — it does not certify every loan-level variable by implication. v1 discipline: construct riskbooks around homogeneous structural facts, then attach per-exobook attestations for variables that differ per loan. The main P1 exobook-level fact is maturity / TTM; the risk form uses certified term only after the funding transaction confirms.

```metta
;; in &entity.halo.{halo-id}.riskbook.{rbk-id}
(riskbook-attestation {rbk-id}
   (attestor      {attest-data-{halo-id}-id})
   (timestamp     T)
   (refresh-due   T+{review-cadence})
   (underwriting  pass)                        ; pass | fail
   (claims
      (legal-structure-enforceable  true)
      (borrower-credit-standing     normal)
      (custodian-compliance-current true))
   (scope-ref     {structural-config-hash})
   (sig           "..."))
```

```metta
;; in &entity.halo.{halo-id}.exobook.{loan-id}
(exobook-term-attestation {loan-id}
   (attestor      {attest-data-{halo-id}-id})
   (timestamp     T)
   (refresh-due   T+{review-cadence})
   (underwriting  pass)                        ; pass | fail
   (claims
      (term-enforceable           true)
      (maturity-T                 {maturity-T})
      (ttm-days-at-funding        {ttm-days})
      (cash-conversion-path-valid true)
      (disbursement-readiness     true))
   (scope-ref     {exobook-term-config-hash})
   (sig           "..."))
```

`scope-ref` binds the riskbook attestation to shared structural config: borrower identity, disbursement/collateral accounts, custodian, collateral asset type, and legal setup. `exobook-term-attestation.scope-ref` binds the per-exobook term, maturity, funding path, cash-conversion path, and disbursement readiness. Market state is not part of either scope-ref.

---

## 5. Exobook Staged Lifecycle

The exobook and exo units can be created before funds are sent. In the `ready-empty` state, the borrower, collateral account, term intent, and tranche skeleton are recorded, but no assets have been assigned. After queue claim and conversion, `synops-halo-{id}` can assign USDC accounting into the riskbook/exobook path without moving chain funds. The money is operationally on the way out under the relay's strategy, but it is not yet a funded borrower exposure and not yet SDR-matchable term exposure.

```text
borrower admission ok
  -> create exobook + exo units in ready-empty state
  -> relay claims queued Prime funds and converts into USDC
  -> synops assigns book assets into riskbook/exobook accounting
  -> term attestation verifies intended maturity / TTM
  -> relay sends funds to disbursement account
  -> funding tx confirms
  -> exobook state becomes funded-active
  -> certified maturity/TTM becomes official for risk and SDR matching
```

If the send or attestation fails, the reserve unwinds back to ordinary PAU cash.

---

## 6. Default-Deny Gate

A borrower or riskbook does not roll up if its required attestation is:

- `fail` / `blocked`,
- stale (`now > refresh-due`),
- missing,
- or scope-mismatched.

In those cases the risk form excludes the positions and the Prime's structbook cannot account for them. This keeps stale legal/credit facts from poisoning the rollup.

---

## 7. Slashing Surface

The `claims` blocks are the slashing surface. The synome cannot directly verify these facts at the time of attestation, so slashing is reactive: if a position sours and post-mortem shows a claim was false at attestation time, the attestor is slashed. Itemizing the claims lets slashing magnitude scale per claim. Magnitudes belong to the Oracle Entity stub-spec, not this atom schema.

---

## 8. Downstream Consequences

The risk form's inputs are `CHAINREAD` + market-memory atoms + these boolean gates — it never reads loan numbers out of attestations. CORE (calibration/reference) is also entirely insyn-fed, zero attestor dependency. Binding P1 risk form: [`custodial-crypto-risk-form.md`](custodial-crypto-risk-form.md).

---

## File Map

| Doc | Relationship |
|---|---|
| [`phase-1-spaces.md`](phase-1-spaces.md) | Topology and worked P1 flow |
| [`custodial-crypto-risk-form.md`](custodial-crypto-risk-form.md) | Risk form that consumes these gates |
| [`market-memory-oracle.md`](market-memory-oracle.md) | Market inputs consumed by the risk form |
| [`../roadstart/big-picture.md`](../roadstart/big-picture.md) | `attest-data-beacon` class — see "Beacon taxonomy" section |
