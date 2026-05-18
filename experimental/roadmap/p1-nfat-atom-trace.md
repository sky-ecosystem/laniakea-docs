# P1 NFAT Atom Trace

**Status:** Resolved Phase 1 atom trace (2026-05-17).
**Scope:** One funded `nfat-term` custodial-crypto loan from constructor writes through `prime-er` emission. Scenario constants and reducer catalogs stay symbolic; the atom flow, gates, and rollup path are binding P1 shape.

This is a companion to the worked NFAT example in [`phase-1-spaces.md`](phase-1-spaces.md). It does not add Spaces, verbs, or beacon classes.

## Trace discipline

- Every atom below lives in the Space shown above it. Cross-Space reads happen only through known registries, cross-book duality, or the explicit P1 exceptions already in the Space spec.
- Attestor atoms are boolean gates. They never supply collateral, debt, price, LTV, or CRR numbers.
- Market facts come from `&entity.oracle.crypto-majors.ticks`; loan facts come from exobook atoms plus the `CHAINREAD` sigil.
- Synserv may emit derived atoms as cache/output, but authority comes from deterministic re-derivation from source atoms each heartbeat.
- `patch-{prime}` enters only at the Prime primebook as `exsynTRRC`; it never affects the insyn NFAT trace.

## IDs used

| Item | ID |
|---|---|
| Halo | `spark-term` |
| Prime | `spark` |
| Halobook | `hbk-001` |
| Riskbook | `rbk-001` |
| Exobook / loan | `spark-term-loan-001` |
| NFAT unit | `nfat-spark-term-001` |
| Borrower | `borrower-001` |
| Current epoch | `E` |
| Funding timestamp | `T_fund` |
| Heartbeat timestamp | `H` |

## 1. Constructor and operational writes

These are gate-mediated operational writes, not sudo. The constructors are run by `relay-halo-spark-term`; NFAT deployment is run by `relay-prime-spark`. The borrower readiness / Core inclusion / final admission path precedes this trace: `synops-halo-spark-term` records the proposed setup and request, `relay-core-govops` records Configurator inclusion, and `attest-data-spark-term` certifies the non-derivable legal / operational / credit claims.

### 1.1 Halobook

```metta
;; in &entity.halo.spark-term.root
(sub-space halobook hbk-001 &entity.halo.spark-term.halobook.hbk-001)

;; in &entity.halo.spark-term.halobook.hbk-001
(book-kind hbk-001 halobook)
(parent-space hbk-001 &entity.halo.spark-term.root)
(halo-class-ref hbk-001 &entity.halo.spark-term.nfat-term)
(halobook-terms hbk-001
   (permitted-unwind [maturity health-factor-breach])
   (transfer-market none)
   (unit-standard nfat-term))
```

### 1.2 Riskbook

`create-riskbook` reads the local halo class and imports the local risk class's risk form into the new riskbook. Later canonical propagation changes the provenance of the risk form, not this read/import path.

```metta
;; in &entity.halo.spark-term.root
(sub-space riskbook rbk-001 &entity.halo.spark-term.riskbook.rbk-001)

;; in &entity.halo.spark-term.halobook.hbk-001
(child-riskbook hbk-001 rbk-001 &entity.halo.spark-term.riskbook.rbk-001)

;; in &entity.halo.spark-term.riskbook.rbk-001
(book-kind rbk-001 riskbook)
(parent-halobook rbk-001 &entity.halo.spark-term.halobook.hbk-001)
(risk-class-ref rbk-001 &entity.halo.spark-term.custodial-crypto)
(risk-form-import rbk-001 custodial-crypto {risk-form-hash})
(riskbook-composition rbk-001
   (senior-tranche-only true)
   (allowed-collateral [btc eth steth])
   (allowed-senior-denom [usdc usds usdt])
   (max-ttm-days 365)
   (halo-class nfat-term))
```

### 1.3 Exobook

`create-exobook` creates the borrower loan object in `ready-empty` state. Before funds are assigned and funding confirms, this is not funded borrower exposure and not SDR-matchable.

```metta
;; in &entity.halo.spark-term.root
(sub-space exobook spark-term-loan-001
   &entity.halo.spark-term.exobook.spark-term-loan-001)

;; in &entity.halo.spark-term.riskbook.rbk-001
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
   (maturity-T {maturity-T})
   (ttm-days-intended 180))

(lifecycle spark-term-loan-001 ready-empty {T_stage})
(reserved-principal spark-term-loan-001 usdc 750000 {T_stage})
```

### 1.4 Attestor gates

The class-accordant `attest-data-spark-term` beacon writes three boolean surfaces. `scope-ref` binds the off-chain claim to the relevant structural facts; market state is not in scope.

```metta
;; in &entity.halo.spark-term.custodial-crypto
(custodial-borrower-admission borrower-001
   (attestor attest-data-spark-term)
   (timestamp {T_attest})
   (refresh-due {T_borrower_refresh})
   (status ok)
   (disbursement-account ethereum disbursement-account-001)
   (collateral-account ethereum collateral-account-001)
   (claims
      (configurator-whitelist-current true)
      (legal-framework-enforceable true)
      (account-binding-valid true)
      (custody-setup-current true)
      (borrower-credit-standing normal))
   (scope-ref {borrower-setup-hash})
   (sig "..."))

;; in &entity.halo.spark-term.riskbook.rbk-001
(riskbook-attestation rbk-001
   (attestor attest-data-spark-term)
   (timestamp {T_attest})
   (refresh-due {T_riskbook_refresh})
   (underwriting pass)
   (claims
      (legal-structure-enforceable true)
      (borrower-credit-standing normal)
      (custodian-compliance-current true))
   (scope-ref {structural-config-hash})
   (sig "..."))

;; in &entity.halo.spark-term.exobook.spark-term-loan-001
(exobook-term-attestation spark-term-loan-001
   (attestor attest-data-spark-term)
   (timestamp {T_attest})
   (refresh-due {T_exobook_refresh})
   (underwriting pass)
   (claims
      (term-enforceable true)
      (maturity-T {maturity-T})
      (ttm-days-at-funding 180)
      (cash-conversion-path-valid true)
      (disbursement-readiness true))
   (scope-ref {exobook-term-config-hash})
   (sig "..."))
```

### 1.5 Funding confirmation and NFAT unit

After the funding transaction confirms, the exobook becomes active and the certified TTM becomes the term used for SDR matching.

```metta
;; in &entity.halo.spark-term.exobook.spark-term-loan-001
(funding-confirmation spark-term-loan-001
   (chain ethereum)
   (tx {funding-tx})
   (block {funding-block})
   (timestamp T_fund))
(lifecycle spark-term-loan-001 funded-active T_fund)
(term-start spark-term-loan-001 T_fund)
(ttm-days-official spark-term-loan-001 180)

;; in &entity.halo.spark-term.halobook.hbk-001
(nfat-unit nfat-spark-term-001
   (source-riskbook rbk-001)
   (source-exobook spark-term-loan-001)
   (source-senior-tranche senior-001)
   (notional usd 750000)
   (maturity-T {maturity-T})
   (halo-class nfat-term))
(nfat-holder nfat-spark-term-001
   (prime spark)
   (holder-pau spark-prime-pau)
   (timestamp T_fund))

;; in &entity.prime.spark.root
(prime-nfat-allocation spark nfat-spark-term-001
   (halo spark-term)
   (notional usd 750000)
   (timestamp T_fund))
```

## 2. External input atoms before heartbeat

### 2.1 Market memory

The exact reducer catalog is deferred, but the risk form reads this family of atoms from the Crypto Majors Oracle.

```metta
;; in &entity.oracle.crypto-majors.ticks
(price-tick btc usd {btc-usd-price} {T_market})
(price-tick usdc usd {usdc-usd-price} {T_market})
(realized-vol btc (window 30d) (reducer realized-vol-v1) {btc-vol-30d} {T_market})
(correlation btc eth (window 90d) (reducer corr-v1) {btc-eth-rho} {T_market})
(impact-curve btc usd
   (side sell)
   (sell-size {scenario-sell-size})
   (horizon 4h)
   (reducer impact-v1)
   (slippage {btc-impact-slippage})
   {T_market})
(max-drawdown btc (window 365d) (reducer crash-shape-v1) {btc-max-drawdown} {T_market})
(liquidity-quantile btc (window 365d) (quantile 0.05) {btc-p05-depth} {T_market})
(market-data-freshness btc {seconds-old} {T_market})
(source-disagreement btc price {source-disagreement-pct} {T_market})
```

### 2.2 SDR capacity, allocation, and capital scalars

The daily DSC SDR pipeline writes current-epoch capacity and allocation atoms. `structural-demand` owns the total SDR production pipeline; `sdr-auction` owns the Prime split. Structbooks read the allocation atom shape, not the allocator provenance.

```metta
;; in &entity.generator.usge.structural-demand
(lot-age-surface E {surface-hash} {source-ref}
   (summary {lot-age-summary}))
(lindy-sdr-bucket-capacity 6 {lindy-capacity} E {model-version} {surface-ref})
(sdr-policy-overlay 6 E
   (max-cap {max-cap})
   (haircut {haircut})
   (eligible-sources {source-set}))
(effective-sdr-bucket-capacity 6 200000000 E
   (lindy-ref {lindy-ref})
   (policy-ref {policy-ref}))

;; in &entity.generator.usge.sdr-auction
(sdr-allocation spark 6 200000000 E)

;; in &entity.prime.spark.root
(prime-trc spark {spark-trc} E)
(prime-ijrc spark {spark-ijrc} E)

;; in &entity.prime.spark.primebook
(exsyn-trrc-claim spark {spark-exsyn-trrc} {T_patch})
```

If the heartbeat is inside the 13:00-16:00 UTC processing window, synserv first refreshes `&core.treasury`, refreshes the lot-age surface in `&entity.generator.usge.structural-demand`, runs Lindy SDR + the SDR policy overlay, reads Prime IJRC, runs the temporary SDR auction in `&entity.generator.usge.sdr-auction`, and writes the next/current epoch allocation atoms. Otherwise it reads the already-current epoch allocation.

## 3. Synserv heartbeat trace

### 3.1 Exobook derivation

Synserv reads exobook source atoms, term attestation, and chain state. The `CHAINREAD` calls are sigil calls resolved through the grounding/workcell stack, not beacon writes.

```metta
;; reads from &entity.halo.spark-term.exobook.spark-term-loan-001
(lifecycle spark-term-loan-001 funded-active T_fund)
(collateral-ref spark-term-loan-001 ...)
(senior-tranche spark-term-loan-001 senior-001 ...)
(ttm-days-official spark-term-loan-001 180)
(exobook-term-attestation spark-term-loan-001 ...)

;; CHAINREAD sigil calls
(CHAINREAD ethereum collateral-account-001 (balance btc) {block-H})
(CHAINREAD ethereum {loan-contract} (debt-outstanding spark-term-loan-001) {block-H})
(CHAINREAD ethereum {loan-contract} (liquidation-threshold spark-term-loan-001) {block-H})
(CHAINREAD ethereum {loan-contract} (liquidation-bonus spark-term-loan-001) {block-H})
```

Derived output:

```metta
;; in &entity.halo.spark-term.exobook.spark-term-loan-001
(exobook-current-state spark-term-loan-001 H
   (collateral btc {collateral-amount})
   (senior-debt usdc {senior-debt})
   (lt {liquidation-threshold})
   (liquidation-bonus {liquidation-bonus})
   (ttm-days 180)
   (lifecycle funded-active))

(exobook-equity spark-term-loan-001 H {equity-usd})
(exobook-sptp spark-term-loan-001 H
   (credit-spread-days 180)
   (rate-days 180)
   (bucket 6))
```

If the exobook is still `ready-empty`, synserv can derive setup state, but it does not emit SDR-matchable term exposure.

### 3.2 Riskbook gates and risk-form execution

Synserv checks all boolean gates before CRR output is eligible for rollup.

```metta
;; reads
;; &entity.halo.spark-term.custodial-crypto
(custodial-borrower-admission borrower-001 ...)

;; &entity.halo.spark-term.riskbook.rbk-001
(riskbook-attestation rbk-001 ...)
(risk-form-import rbk-001 custodial-crypto {risk-form-hash})
(riskbook-composition rbk-001 ...)

;; &entity.halo.spark-term.exobook.spark-term-loan-001
(exobook-term-attestation spark-term-loan-001 ...)
(exobook-current-state spark-term-loan-001 H ...)

;; &entity.oracle.crypto-majors.ticks
(price-tick ...)
(impact-curve ...)
(max-drawdown ...)
(market-data-freshness ...)
```

Gate result:

```metta
;; in &entity.halo.spark-term.riskbook.rbk-001
(rollup-gate rbk-001 spark-term-loan-001 H pass
   (borrower-admission ok)
   (riskbook-attestation pass)
   (exobook-term-attestation pass)
   (scope-match true)
   (fresh true))
```

Risk form execution is scenario-synchronous. It computes each exobook's senior loss under each approved scenario, then aggregates same-scenario losses at the riskbook before taking the max.

```metta
;; in &entity.halo.spark-term.riskbook.rbk-001
(scenario-senior-loss rbk-001 spark-term-loan-001 {scenario-id}
   (stressed-asset-value {stressed-asset-value})
   (senior-notional {senior-notional-usd})
   (senior-loss {senior-loss-usd})
   H)

(custodial-crypto-crr-components spark-term-loan-001 H
   (default-crr {default-crr})
   (spread-crr {spread-crr})
   (rate-crr {rate-crr})
   (liquidity-crr {liquidity-crr})
   (binding-scenario {binding-scenario-id}))

(riskbook-loss rbk-001 {scenario-id} H {riskbook-loss-usd})
(riskbook-default-crr rbk-001 H {riskbook-default-crr})
```

The attestor has no path to influence `{default-crr}` except by pass/fail inclusion. Quantitative values are from exobook state, `CHAINREAD`, market memory, and risk-form data atoms.

### 3.3 Halobook projection

The halobook reads child riskbook outputs and projects the NFAT as a Prime-side asset through cross-book duality.

```metta
;; reads from &entity.halo.spark-term.riskbook.rbk-001
(custodial-crypto-crr-components spark-term-loan-001 H ...)
(riskbook-default-crr rbk-001 H ...)

;; reads from &entity.halo.spark-term.halobook.hbk-001
(nfat-unit nfat-spark-term-001 ...)
(nfat-holder nfat-spark-term-001 (prime spark) ...)
(halobook-terms hbk-001 ...)
```

Derived output:

```metta
;; in &entity.halo.spark-term.halobook.hbk-001
(halobook-exposure hbk-001 H
   (riskbook rbk-001)
   (senior-notional-usd {senior-notional-usd})
   (holder-prime spark))

(nfat-prime-projection nfat-spark-term-001 spark H
   (source-exobook spark-term-loan-001)
   (notional-usd 750000)
   (sptp-bucket 6)
   (default-crr {default-crr})
   (spread-crr {spread-crr})
   (rate-crr {rate-crr})
   (liquidity-crr {liquidity-crr})
   (permitted-unwind [maturity health-factor-breach])
   (transfer-market none))
```

Halobook aggregation is pure summation across riskbook units. It does not net risk across riskbooks.

### 3.4 Prime structbook matching and position capital

The Prime structbook reads NFAT projections from all three P1 Halos and current SDR allocations from the Generator `sdr-auction` Space. Cumulative matching means bucket 6 can consume bucket 6 and higher buckets.

```metta
;; reads from &entity.halo.spark-term.halobook.hbk-001
(nfat-prime-projection nfat-spark-term-001 spark H ...)

;; reads from &entity.generator.usge.sdr-auction
(sdr-allocation spark 6 200000000 E)

;; reads from other halobooks during the same sweep
(nfat-prime-projection {other-nfat} spark H ...)
```

Example evaluation for the single position, assuming the same sweep finds `190000000` already matched against bucket `6+` before this NFAT:

```text
available_capacity_6_plus = 200000000
already_matched_6_plus    = 190000000
remaining_capacity        = 10000000
position_size             = 750000

matched_portion           = min(750000, 10000000) = 750000
unmatched_portion         = 0
position_capital          = matched_portion * default-crr
                          + unmatched_portion * max(default-crr, forced-loss-capital)
                          + unmatched_portion * rate-crr
```

Derived output:

```metta
;; in &entity.prime.spark.structbook
(structbook-eligibility nfat-spark-term-001 H pass
   (sptp-bucket 6)
   (sdr-bucket-covered true)
   (sdr-allocation-present true)
   (active-sub-book structbook))

(structbook-match nfat-spark-term-001 H
   (required-bucket 6)
   (matched-notional 750000)
   (unmatched-notional 0)
   (allocation-source &entity.generator.usge.sdr-auction)
   (epoch E))

(structbook-position-capital nfat-spark-term-001 H
   (matched-notional 750000)
   (unmatched-notional 0)
   (default-crr {default-crr})
   (forced-loss-capital {forced-loss-capital})
   (rate-crr {rate-crr})
   (position-capital {position-capital-usd}))

(structbook-insyn-trrc spark {spark-structbook-trrc} H)
```

If capacity is exhausted, `matched-notional` goes to `0`, `unmatched-notional` goes to `750000`, and the same formula emits a higher position capital. There is no route-change event.

### 3.5 Primebook TRRC and ER

The Prime primebook is where the insyn/exsyn split closes.

```metta
;; reads from &entity.prime.spark.structbook
(structbook-insyn-trrc spark {spark-structbook-trrc} H)

;; reads from &entity.prime.spark.primebook
(exsyn-trrc-claim spark {spark-exsyn-trrc} {T_patch})

;; reads from &entity.prime.spark.root
(prime-trc spark {spark-trc} E)
```

Derived output:

```metta
;; in &entity.prime.spark.primebook
(prime-insyn-trrc spark {spark-structbook-trrc} H)
(prime-trrc spark
   (+ {spark-structbook-trrc} {spark-exsyn-trrc})
   H)
(prime-er spark
   (/ (+ {spark-structbook-trrc} {spark-exsyn-trrc})
      {spark-trc})
   H)
```

`prime-er` is the Phase 1 deliverable. Governance consumes it externally; settlement and penalty actions remain manual in P1.

## 4. Default-deny branches exposed by the trace

| Failure | Result |
|---|---|
| Missing / stale / blocked borrower admission | Exobook cannot roll up. |
| Missing / stale / failed riskbook attestation | Riskbook and all child exobooks are excluded. |
| Missing / stale / failed exobook term attestation | That exobook is excluded; no SDR-matchable term exposure. |
| Scope mismatch on any attestation | Same as missing; the boolean no longer binds the current structure. |
| Exobook still `ready-empty` | Setup state can be tracked, but it is not funded exposure and not SDR-matchable. |
| Composition does not match `custodial-crypto` | CRR 100% default-deny if still admitted into a book; ordinary P1 constructors should reject it first. |
| Market memory stale / divergent beyond risk-form tolerance | Risk form haircuts or default-denies according to its data-quality rule. |
| No current SDR allocation | Matched portion is zero; position remains in `structbook` but capitalizes as unmatched. |

## 5. What this resolves

The trace pins down the end-to-end reads and writes that were the final Phase 1 design follow-up:

- constructor writes for halobook, riskbook, exobook, and NFAT unit;
- boolean attestor gates and their exact downstream role;
- risk-form composition from exobook state, `CHAINREAD`, market memory, and scenarios;
- concrete `structbook` matching against `sdr-allocation` atoms;
- upward rollup from exobook derivation to riskbook CRR, halobook projection, Prime structbook capital, `insynTRRC + exsynTRRC`, and final `prime-er`.

## 6. Implementation pickups

Residual items are calibration / implementation details, not P1 topology blockers:

- enumerate the exact `scope-ref` predicates for borrower admission, riskbook shared structure, and exobook term attestation;
- choose final implementation field names for the atom shapes above if the v1 runtime wants a narrower syntax;
- calibrate the first approved scenario constants when CRR values become real;
- finalize the exact market-memory reducer catalog. The mechanism is already settled in [`market-memory-oracle.md`](market-memory-oracle.md).
