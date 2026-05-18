# Sigils and Workcells -- P1 Inventory

**Status:** P1 substrate inventory.
**Scope:** Synserv/runtime-facing callable surface and workcells for Phase 1. Beacon-local teleonome/operator sigils are deliberately deferred; from synserv's perspective, beacons feed signed envelopes through syngate.

This file is the complete P1 inventory. [`grounding-and-workcells.md`](grounding-and-workcells.md) defines the conceptual stack; this file pins the actual P1 callable/workcell list.

---

## 1. Callable categories

| Category | P1 members | Backed by workcell? | Notes |
|---|---|---:|---|
| **Special forms** | `if`, `let`, `match`, `quote` | No | Evaluator control. Not functions and not sigils. |
| **Stdlib pure** | `+`, `-`, `*`, `/`, `min`, `max`, `sum`, `=`, `<`, `<=`, `>`, `>=`, `sha256` | No | Deterministic local functions. No authority boundary. |
| **Native stdlib sigil** | `NOW` | No | Runtime-grounded heartbeat time. Shadow tests may override it. |
| **Workcell-backed sigils** | `SYNGATE-READ`, `CHAINREAD` | Yes | Capability-bearing calls through bindings to implements and workcell hubs. |
| **Bootstrap-only powers** | `MATERIALIZE-IMPLEMENT`, `BIND-SIGIL`, `REGISTER-WORKCELL-HUB`, `ENABLE-LOOP` | Boot only | Only callable by `&core.bootstrap`; not ordinary loop powers. |
| **Noemar-native controls** | frame `fork`, `switch`, `discard`, `diff` | No | Test/boot harness operations, not P1 loop-callable sigils. |

Explicitly out of ordinary P1 loop scope: `SENDTX`, `ASKLLM`, randomness, stochastic powers, non-Ethereum chain access, sentinel call-outs, and beacon-local operator tooling.

---

## 2. Native stdlib sigil

### `NOW`

```text
(NOW) -> timestamp
```

`NOW` returns the synserv heartbeat scheduler timestamp for the current evaluation. It is stable within one heartbeat. Production uses the scheduler timestamp; shadow tests can pin or override it.

P1 uses `NOW` for DSC cut/settle checks, freshness/staleness checks, and timestamping derived heartbeat outputs. It is not an arbitrary machine-clock read inside equations.

---

## 3. Workcell-backed sigils

### `SYNGATE-READ`

```text
(SYNGATE-READ cursor limit) -> (batch next-cursor envelopes)
```

Reads a replayable batch of first-pass-valid beacon envelopes from the syngate intake workcell.

The workcell performs the first pass:

- envelope parses;
- signature is valid for the included pubkey;
- pubkey belongs to a registered beacon identity set known to the intake workcell;
- basic spam, nonce, and rate-limit prefiltering passes.

The workcell does **not** decide:

- whether the beacon may perform the attempted verb;
- whether the verb may target the requested Space;
- whether the payload shape is valid for that verb;
- whether the write should be sequenced into synart.

Synserv performs the second pass in synlang by reading `&core.syngate` and `&core.registry.beacon`: external verb whitelist, verb-to-target routing, beacon status/class, and auth grants. Accepted writes are routed into their target Spaces; rejected envelopes can be recorded as rejection/audit atoms according to the syngate loop body.

### `CHAINREAD`

```text
(CHAINREAD chain target query block-ref) -> result-with-provenance
```

P1 supports `ethereum` only. `CHAINREAD` is read-only, deterministic at an explicit block reference, and returns provenance sufficient for conformance checks.

Minimum P1 query families:

- balances and ownership: ERC20/native balances, NFATS owner/token state where receipt validation needs it;
- contract reads: view calls or storage reads for debt outstanding, liquidation threshold, liquidation bonus, Configurator whitelist state, PAU/NFATS state;
- event/log ranges: ERC20 `Transfer` history for lot-age surfaces, plus queue, conversion, mint, and related operational events when required by receipt validation;
- transaction receipts/status: funding confirmations, queue claims, conversions, NFAT mints, disbursements, and Core govops Configurator actions.

`CHAINREAD` never sends transactions. Relay actions remain external/operator decisions recorded as signed atoms; synserv may verify the recorded receipts through `CHAINREAD`.

---

## 4. Workcells

| Workcell | Backs | Required components |
|---|---|---|
| `syngate-intake-workcell` | `SYNGATE-READ` | Signed submission queue/network ingress, registered-beacon pubkey snapshot, signature verifier, nonce/rate-limit prefilter state, cursor store. |
| `eth-mainnet-read-workcell` | production `CHAINREAD` | Ethereum full/archive node or equivalent RPC, provider redundancy, explicit block refs, log/receipt access, proof/provenance reporting, health checks. |
| `eth-mainnet-fork-workcell` | shadow/test `CHAINREAD` | Forked Ethereum state or deterministic fixtures with the same read interface as production. |

No P1 clock workcell exists: `NOW` is native scheduler time. Beacon-local workcells for market-data, attestors, relays, synops, patch providers, and future teleonomes are out of scope for this inventory.

---

## 5. Space feed map

| Space / flow | Feed path |
|---|---|
| `&core.syngate` | `SYNGATE-READ` batches, then synlang second-pass auth/routing against `&core.syngate` and `&core.registry.beacon`. |
| `&entity.oracle.crypto-majors.ticks` | Signed `market-data` beacon atoms. Market oracle reducer/source tooling is not a P1 synserv sigil. |
| Halo risk class and book Spaces | Signed `attest-data`, `relay-halo`, and `synops-halo` envelopes through syngate. |
| Prime primebooks | Signed `patch-{prime}` exsyn TRRC atoms through syngate, plus synserv-derived `prime-er`. |
| `&entity.generator.usge.structural-demand` | Synserv uses `CHAINREAD` for Ethereum USDS/DAI/sUSDS/sDAI balances and transfer history, then writes lot-age, Lindy SDR, and policy-overlay outputs. |
| Exobook and risk rollup | Synserv uses `CHAINREAD` for collateral, debt/config state, funding confirmations, and receipt validation; market facts arrive from `crypto-majors.ticks`. |
| `&core.settlement` | Synserv uses `NOW` for DSC cut, processing, and settle transitions. |

---

## 6. Loop requirement shape

The synserv loop declares stdlib modules, native sigils, workcell-backed sigils, bindings, workcells, and conformance tests separately:

```metta
(loop-requires synserv-canonical
   (stdlib [core-special-forms-v1 core-stdlib-v1])
   (native-sigils [NOW])
   (sigils [SYNGATE-READ CHAINREAD])
   (bindings [syngate-read-v1 chainread-eth-mainnet-v1])
   (workcells [syngate-intake-workcell eth-mainnet-read-workcell])
   (tests [syngate-read-conformance-v1 chainread-conformance-v1]))
```

In shadow tests, `chainread-eth-mainnet-v1` is rebound to `eth-mainnet-fork-workcell`; the synlang read path does not change.
