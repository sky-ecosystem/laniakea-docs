# P1 Borrower-to-ER User Scenario

**Status:** Companion scenario for Phase 1.
**Scope:** One `spark-term` borrower onboarding and NFAT origination through the first Spark Prime `prime-er` update.

This is a narrative path through the topology in [`phase-1-spaces.md`](phase-1-spaces.md), with key atoms shown where the authority boundary or rollup path matters. It does not add Spaces, entarts, beacon classes, or a queue Space.

## Fixed scenario

| Item | Value |
|---|---|
| Halo | `spark-term` |
| Prime | `spark` |
| Risk class | `custodial-crypto` |
| Halo class | `nfat-term` |
| Borrower | `borrower-001` |
| Halobook | `hbk-001` |
| Riskbook | `rbk-001` |
| Exobook / loan | `spark-term-loan-001` |
| NFAT unit | `nfat-spark-term-001` |
| Loan | 180-day USDC senior loan |
| Senior notional | 750,000 USDC |
| Collateral | BTC at pre-recorded collateral account |

Illustrative numbers are deliberately simple. The CRR values are assumed outputs of the P1 risk form; this scenario is about path and authority, not calibration.

## Topology commitments

- No borrower Space exists. Borrower setup and admission atoms live in `&entity.halo.spark-term.custodial-crypto`.
- The NFATS queue is chain-side Halo Facility infrastructure. The synome sees queue deposits, queue claims, conversions, and mints through relay receipts and halobook liability atoms.
- `relay-prime-spark` and `relay-halo-spark-term` record chain-coupled actions. `synops-halo-spark-term` records in-synome borrower requests and book-accounting assignments only.
- `attest-data-spark-term` writes boolean gates. It never supplies collateral, debt, price, LTV, or CRR numbers.
- `synserv-canonical` derives risk, matching, TRRC, and ER from atoms plus `CHAINREAD` sigil calls.

## 1. Borrower proposed to the risk class

Halo govops wants to prepare a borrower before any capital is queued. `synops-halo-spark-term` writes the proposed borrower setup into the local risk class Space.

```metta
;; in &entity.halo.spark-term.custodial-crypto
(proposed-borrower-setup borrower-001
   (proposed-by synops-halo-spark-term)
   (timestamp T0)
   (disbursement-account ethereum disbursement-account-001)
   (collateral-account ethereum collateral-account-001)
   (custodian custodian-001)
   (legal-framework-ref legal-framework-001)
   (scope-ref borrower-setup-hash-001))
```

The class-accordant attestor underwrites the setup before it goes to Core Council. This is not final admission, because Configurator inclusion has not happened yet.

```metta
;; in &entity.halo.spark-term.custodial-crypto
(borrower-readiness-attestation borrower-001
   (attestor attest-data-spark-term)
   (timestamp T1)
   (refresh-due T1+90d)
   (readiness pass)
   (claims
      (legal-framework-enforceable true)
      (account-binding-valid true)
      (custody-setup-current true)
      (borrower-credit-standing normal))
   (scope-ref borrower-setup-hash-001)
   (sig "..."))
```

## 2. Borrower inclusion requested from Core Council

With readiness attested, `synops-halo-spark-term` submits the borrower to Core Council for Configurator inclusion.

```metta
;; in &entity.halo.spark-term.synops
(borrower-inclusion-request req-borrower-001
   (borrower borrower-001)
   (risk-class &entity.halo.spark-term.custodial-crypto)
   (readiness-ref borrower-readiness-attestation borrower-001 T1)
   (requested-action configurator-include-borrower)
   (scope-ref borrower-setup-hash-001)
   (timestamp T2))

;; in &core.governance.requests
(core-request req-borrower-001
   (from synops-halo-spark-term)
   (target &core.registry.protocol)
   (request-kind borrower-configurator-inclusion)
   (borrower borrower-001)
   (disbursement-account ethereum disbursement-account-001)
   (collateral-account ethereum collateral-account-001)
   (evidence borrower-readiness-attestation borrower-001 T1)
   (status submitted)
   (timestamp T2))
```

Core govops processes the request and records the Configurator action through `relay-core-govops`.

```metta
;; in &core.governance.requests
(request-status req-borrower-001 approved T3)
(request-status req-borrower-001 executed T4)

;; in &core.relay.govops
(core-govops-action req-borrower-001
   (action configurator-include-borrower)
   (chain ethereum)
   (tx configurator-tx-001)
   (timestamp T4))
```

After inclusion is real, `attest-data-spark-term` posts final borrower admission. This is the borrower-level rollup gate.

```metta
;; in &entity.halo.spark-term.custodial-crypto
(custodial-borrower-admission borrower-001
   (attestor attest-data-spark-term)
   (timestamp T5)
   (refresh-due T5+90d)
   (status ok)
   (disbursement-account ethereum disbursement-account-001)
   (collateral-account ethereum collateral-account-001)
   (claims
      (configurator-whitelist-current true)
      (legal-framework-enforceable true)
      (account-binding-valid true)
      (custody-setup-current true)
      (borrower-credit-standing normal))
   (scope-ref borrower-setup-hash-001)
   (sig "..."))
```

## 3. Books created in ready-empty mode

The borrower is admitted, but no Prime has funded the deal yet. `relay-halo-spark-term` creates the book stack in `ready-empty` mode.

```metta
;; in &entity.halo.spark-term.root
(sub-space halobook hbk-001 &entity.halo.spark-term.halobook.hbk-001)
(sub-space riskbook rbk-001 &entity.halo.spark-term.riskbook.rbk-001)
(sub-space exobook spark-term-loan-001
   &entity.halo.spark-term.exobook.spark-term-loan-001)

;; in &entity.halo.spark-term.halobook.hbk-001
(book-kind hbk-001 halobook)
(halo-class-ref hbk-001 &entity.halo.spark-term.nfat-term)
(lifecycle hbk-001 ready-empty T6)
(child-riskbook hbk-001 rbk-001 &entity.halo.spark-term.riskbook.rbk-001)

;; in &entity.halo.spark-term.riskbook.rbk-001
(book-kind rbk-001 riskbook)
(parent-halobook rbk-001 &entity.halo.spark-term.halobook.hbk-001)
(risk-class-ref rbk-001 &entity.halo.spark-term.custodial-crypto)
(risk-form-import rbk-001 custodial-crypto risk-form-hash-001)
(lifecycle rbk-001 ready-empty T6)
(child-exobook rbk-001 spark-term-loan-001
   &entity.halo.spark-term.exobook.spark-term-loan-001)

;; in &entity.halo.spark-term.exobook.spark-term-loan-001
(book-kind spark-term-loan-001 exobook)
(parent-riskbook spark-term-loan-001 &entity.halo.spark-term.riskbook.rbk-001)
(borrower spark-term-loan-001 borrower-001)
(frame spark-term-loan-001 usd)
(collateral-ref spark-term-loan-001
   (asset btc)
   (chain ethereum)
   (account collateral-account-001))
(senior-tranche spark-term-loan-001 senior-001
   (denom usdc)
   (notional 750000))
(junior-tranche spark-term-loan-001 junior-001
   (notional-rule residual-equity))
(term-intent spark-term-loan-001
   (maturity-T maturity-T-001)
   (ttm-days-intended 180))
(lifecycle spark-term-loan-001 ready-empty T6)
```

At this point there is a borrower and an action-ready book stack, but no asset exposure and no Prime-side position.

## 4. Spark Prime queues USDS

Spark Prime agrees out of band to fund this ready halobook. `relay-prime-spark` deposits USDS into the NFATS queue and records the Prime-side intent and receipt.

```metta
;; in &entity.prime.spark.relay
(nfat-queue-deposit spark-term hbk-001
   (prime spark)
   (asset usds)
   (amount 750000)
   (chain ethereum)
   (tx prime-queue-deposit-tx-001)
   (timestamp T7))

;; in &entity.prime.spark.root
(prime-nfat-deploy-intent spark nfat-spark-term-001
   (halo spark-term)
   (halobook hbk-001)
   (notional usd 750000)
   (timestamp T7))
```

The queue is not a synome Space. It is contract state in the Halo Facility.

## 5. Halo claims queue funds and mints the NFAT

`relay-halo-spark-term` claims the queued USDS, mints the NFAT to Spark Prime, records the halobook liability, and converts USDS to USDC through on-chain PAU actions.

```metta
;; in &entity.halo.spark-term.halobook.hbk-001
(queue-claim hbk-001 claim-001
   (from-prime spark)
   (asset-in usds)
   (amount-in 750000)
   (chain ethereum)
   (tx halo-queue-claim-tx-001)
   (timestamp T8))

(nfat-unit nfat-spark-term-001
   (source-riskbook rbk-001)
   (source-exobook spark-term-loan-001)
   (source-senior-tranche senior-001)
   (notional usd 750000)
   (maturity-T maturity-T-001)
   (halo-class nfat-term))

(nfat-holder nfat-spark-term-001
   (prime spark)
   (holder-pau spark-prime-pau)
   (timestamp T8))

(halo-cash-conversion hbk-001 conversion-001
   (from usds 750000)
   (to usdc 750000)
   (chain ethereum)
   (tx halo-usds-usdc-conversion-tx-001)
   (timestamp T9))
```

The NFAT mint signals that a borrower-ready action exists and that Spark Prime now holds a Halo Unit claim. The underlying borrower exposure is still not active until book accounting is assigned, attested, and disbursed.

## 6. Synops assigns book assets

The USDC is now held by the Halo as a result of relay-recorded chain actions. `synops-halo-spark-term` assigns the in-synome accounting path from the halobook into the specific riskbook and exobook. This moves no chain funds.

```metta
;; in &entity.halo.spark-term.halobook.hbk-001
(book-asset-assignment assign-001
   (assigned-by synops-halo-spark-term)
   (from-halobook hbk-001)
   (to-riskbook rbk-001)
   (to-exobook spark-term-loan-001)
   (asset usdc)
   (amount 750000)
   (source-receipt conversion-001)
   (timestamp T10))

;; in &entity.halo.spark-term.exobook.spark-term-loan-001
(assigned-principal spark-term-loan-001
   (asset usdc)
   (amount 750000)
   (assignment assign-001)
   (timestamp T10))
```

This is pure synome bookkeeping. If `assign-book-assets` points to a missing relay receipt or a mismatched halobook/riskbook/exobook parent chain, the assignment is invalid.

## 7. Attestor signs safe-to-disburse term readiness

The exobook term attestation is refreshed after assignment. It binds the term, funding path, cash conversion, and disbursement readiness.

```metta
;; in &entity.halo.spark-term.exobook.spark-term-loan-001
(exobook-term-attestation spark-term-loan-001
   (attestor attest-data-spark-term)
   (timestamp T11)
   (refresh-due T11+90d)
   (underwriting pass)
   (claims
      (term-enforceable true)
      (maturity-T maturity-T-001)
      (ttm-days-at-funding 180)
      (cash-conversion-path-valid true)
      (disbursement-readiness true))
   (scope-ref exobook-term-config-hash-001)
   (sig "..."))
```

The attestor still does not attest prices, collateral amounts, LTV, or CRR.

## 8. Halo disburses the loan

Before disbursement, current market and collateral facts are already available to synserv through the ordinary input paths.

```metta
;; in &entity.oracle.crypto-majors.ticks
(price-tick btc usd 80000 T_market)
(price-tick usdc usd 1.0000 T_market)
(impact-curve btc usd
   (side sell)
   (sell-size 750000)
   (horizon 4h)
   (reducer impact-v1)
   (slippage 0.025)
   T_market)
(market-data-freshness btc 30 T_market)

;; CHAINREAD sigil calls available to synserv
(CHAINREAD ethereum collateral-account-001 (balance btc) block-H)
(CHAINREAD ethereum loan-contract-001 (liquidation-threshold spark-term-loan-001) block-H)
(CHAINREAD ethereum loan-contract-001 (liquidation-bonus spark-term-loan-001) block-H)
```

`relay-halo-spark-term` sends USDC to the borrower and records the funding confirmation. The exobook becomes funded exposure only now.

```metta
;; in &entity.halo.spark-term.exobook.spark-term-loan-001
(funding-confirmation spark-term-loan-001
   (chain ethereum)
   (tx borrower-disbursement-tx-001)
   (block funding-block-001)
   (timestamp T_fund))
(lifecycle spark-term-loan-001 funded-active T_fund)
(term-start spark-term-loan-001 T_fund)
(ttm-days-official spark-term-loan-001 180)
```

## 9. Risk form emits CRR components

On the next heartbeat, synserv reads the borrower admission, riskbook attestation, refreshed exobook term attestation, exobook state, `CHAINREAD` chain data, and market memory. The P1 risk form emits assumed CRR components.

```metta
;; in &entity.halo.spark-term.riskbook.rbk-001
(rollup-gate rbk-001 spark-term-loan-001 H pass
   (borrower-admission ok)
   (riskbook-attestation pass)
   (exobook-term-attestation pass)
   (scope-match true)
   (fresh true))

(custodial-crypto-crr-components spark-term-loan-001 H
   (default-crr 0.055)
   (spread-crr 0.018)
   (rate-crr 0.012)
   (liquidity-crr 0.030)
   (binding-scenario btc-liquidity-crash-v1))

(riskbook-crr-components rbk-001 H
   (default-crr 0.055)
   (spread-crr 0.018)
   (rate-crr 0.012)
   (liquidity-crr 0.030)
   (source-exobook spark-term-loan-001))
```

The values above are placeholders. The important point is that all four risk types are present and travel upward.

## 10. Halobook projects the NFAT risk vector

The halobook projects the now-risked NFAT unit as a Prime-side asset.

```metta
;; in &entity.halo.spark-term.halobook.hbk-001
(nfat-prime-projection nfat-spark-term-001 spark H
   (source-exobook spark-term-loan-001)
   (notional-usd 750000)
   (sptp-bucket 6)
   (default-crr 0.055)
   (spread-crr 0.018)
   (rate-crr 0.012)
   (liquidity-crr 0.030)
   (permitted-unwind [maturity health-factor-breach])
   (transfer-market none))
```

## 11. Spark structbook has zero SDR

The scenario deliberately sets Spark's current SDR allocation for bucket 6 to zero. The position remains in `structbook`, but it is fully unmatched.

```metta
;; in &entity.generator.usge.sdr-auction
(sdr-allocation spark 6 0 E)

;; in &entity.prime.spark.structbook
(structbook-match nfat-spark-term-001 H
   (required-bucket 6)
   (matched-notional 0)
   (unmatched-notional 750000)
   (allocation-source &entity.generator.usge.sdr-auction)
   (epoch E))
```

For this zero-SDR scenario, the unmatched structbook capital formula is:

```text
unmatched_crr = max(default-CRR, spread-CRR + liquidity-CRR) + rate-CRR
              = max(0.055, 0.018 + 0.030) + 0.012
              = 0.067

position_capital = 750000 * 0.067 = 50250
```

```metta
;; in &entity.prime.spark.structbook
(structbook-position-capital nfat-spark-term-001 H
   (matched-notional 0)
   (unmatched-notional 750000)
   (default-crr 0.055)
   (spread-crr 0.018)
   (liquidity-crr 0.030)
   (rate-crr 0.012)
   (unmatched-crr 0.067)
   (position-capital 50250))
```

## 12. Spark Prime ER updates

Assume Spark had existing insynTRRC of 300,000, exsynTRRC of 1,200,000 from the patch beacon, and TRC of 5,000,000.

```metta
;; in &entity.prime.spark.structbook
(structbook-insyn-trrc spark 350250 H)

;; in &entity.prime.spark.primebook
(prime-insyn-trrc spark 350250 H)
(prime-trrc spark 1550250 H)
(prime-er spark 0.31005 H)
```

Before this NFAT entered the rollup:

```text
ER_before = (300000 + 1200000) / 5000000 = 0.30000
ER_after  = (350250 + 1200000) / 5000000 = 0.31005
```

The Prime ER changes because the NFAT's CRR vector ripples from the riskbook to the halobook projection, then into Spark's zero-SDR structbook as fully unmatched capital.

## What this scenario resolves

- Borrower setup has a pre-Core-Council readiness gate and a post-Configurator final admission gate.
- Book construction can happen before NFAT mint: books start `ready-empty`, then the NFAT is minted only after the borrower/action is ready.
- Queue/claim mechanics remain chain-side; no queue Space is added.
- `synops-halo` can assign in-synome book accounting after relay receipts, but cannot move funds.
- The first ER update uses the normal P1 path with `structbook`, with zero SDR making the position fully unmatched.
