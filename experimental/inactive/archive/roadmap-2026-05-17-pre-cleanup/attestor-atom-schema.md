# Attestor Atom Schema — Custodial-Crypto

**Status:** Resolved for the Phase 1 `custodial-crypto` risk class (updated 2026-05-17). Resolves [`p1-design-followups.md`](p1-design-followups.md) §1.1 for this risk class only.

**Scope:** Custodial-crypto borrower admission, riskbook admission, and individual exobook term verification. Opaque-RWA risk classes (legacy HVB-style, no on-chain visibility) need a richer numeric attestation schema and are out of scope here.

---

## 1. The reframe

For custodial-crypto, every quantitative CRR input is **insyn**:

| Input | Source |
|---|---|
| Collateral asset + amount | `chain-read` on the borrower's collateral account |
| Debt outstanding, LT, liquidation bonus, derived LTV | `chain-read` on the loan/configurator contracts |
| Price, liquidity, volatility, impact, liquidation-overhang history | Crypto Majors market-memory oracle |

The attestor is therefore not an oracle of loan facts. It is a legal / operational / credit underwriter of what the chain cannot show, and its output is admission/term verification:

- borrower, disbursement account, collateral account, custody setup, and legal framework are acceptable;
- Configurator / aBEAM whitelist path has admitted the borrower/account setup;
- the riskbook's shared structure is underwritten;
- the individual exobook's maturity / TTM and cash-conversion terms are enforceable.

No `assets-attested`, no `debt-outstanding`, no 24h market refresh. Those fields are insyn or irrelevant to the attestor cadence.

---

## 2. Account Vocabulary

The durable pair is:

| Term | Meaning |
|---|---|
| **disbursement account** | Borrower-controlled Ethereum address that receives loan principal from the Halo PAU. |
| **collateral account** | Linked account the exobook tracks and expects to be able to liquidate against; attestors verify legal claim, custody setup, and account binding. |

Disbursement-account onboarding matches onboarding into the Configurator smart contract. It is not a loose address field.

---

## 3. Borrower Admission

Borrower admission lives at the per-halo risk-class level because it is a class-specific permission to do custodial-crypto business with that borrower.

The Halo relay is also the Halo PAU relay for pBEAM and cBEAM execution, but it cannot whitelist a new custodial-crypto borrower alone. Halo govops coordinates with Core Council so the aBEAM/configurator path admits the borrower/account setup; then the class-accordant attestor posts the first-contact attestation.

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

The riskbook attestation gates shared legal / custody / credit structure for a homogeneous bundle. It does not certify every loan-level variable by implication. The v1 discipline is to construct riskbooks around homogeneous structural facts, then attach per-exobook attestations for the facts that vary at the individual loan level.

The main P1 exobook-level fact is maturity / TTM: the attestor verifies that the stated term and cash-conversion path are enforceable. The risk form uses that term only after the funding transaction confirms.

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
      (cash-conversion-path-valid true))
   (scope-ref     {exobook-term-config-hash})
   (sig           "..."))
```

`scope-ref` binds the riskbook attestation to shared structural config: borrower identity, disbursement/collateral accounts, custodian, collateral asset type, and legal setup. `exobook-term-attestation.scope-ref` binds the per-exobook term, maturity, funding path, and cash-conversion path. Market state is not part of either scope-ref.

---

## 5. Exobook Staged Lifecycle

The exobook and exo units can be created before funds are sent. In this staged/pre-send state, the exobook contains reserved USDC / USDS / USDT still sitting in the Halo PAU. The money is operationally on the way out under the relay's strategy, but it is not yet a funded borrower exposure and not yet SDR-matchable term exposure.

```text
borrower admission ok
  -> create exobook + exo units in staged/pre-send state
  -> reserve PAU cash
  -> term attestation verifies intended maturity / TTM
  -> relay sends funds to disbursement account
  -> funding tx confirms
  -> exobook state becomes funded/active
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

The risk form's inputs are `chain-read` (collateral, debt, terms) + market-memory atoms (price, liquidity, volatility, impact, liquidation overhang) + the boolean gates. It never reads loan numbers out of attestations.

CORE's inputs are now entirely insyn: `chain-read` + market memory, zero attestor dependency. CORE is calibration/reference material for P1; the binding risk form is the stress-envelope exobook waterfall in [`../risk-framework/custodial-crypto-risk-form.md`](../risk-framework/custodial-crypto-risk-form.md).

---

## File Map

| Doc | Relationship |
|---|---|
| [`p1-design-followups.md`](p1-design-followups.md) | §1.1 is resolved by this doc |
| [`phase-1-spaces.md`](phase-1-spaces.md) | Topology and worked P1 flow |
| [`../risk-framework/custodial-crypto-risk-form.md`](../risk-framework/custodial-crypto-risk-form.md) | Risk form that consumes these gates |
| [`../risk-framework/market-memory-oracle.md`](../risk-framework/market-memory-oracle.md) | Market inputs consumed by the risk form |
| [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) | `attest-data-beacon` class |
