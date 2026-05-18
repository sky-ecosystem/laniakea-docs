# Smart Contracts

**Status:** mixed — PAU pattern + Configurator live (legacy); Diamond PAU placeholder; LCTS, NFATS, Yield Splitter draft target; rate-limit-attacks calibrated (SORL=25%, IRL=$100K adopted)
**Canonical home:** `lani/smart-contracts/`

---

## TL;DR

The on-chain (EVM) layer for capital deployment. One reusable building block — the **PAU** (Controller + ALMProxy + RateLimits) — is deployed at every layer (Generator → Prime → Halo → Foreign), differing only in configuration. A **Configurator Unit** (BEAMTimeLock + BEAMState + Configurator) sits above PAUs and enforces the **aBEAM/cBEAM** access split: Core Council (aBEAM) registers PAUs and pre-approves "inits" through a 14-day timelock; GovOps (cBEAM, accordant to a PAU) operate within those bounds, subject to **SORL** (default 25% increase per 18h `hop`; decreases instant). **Diamond PAU** (EIP-2535) is the planned upgrade replacing the 24KB-bound monolithic Controller. Two Halo-level token standards: **LCTS** (queue + generation, daily-batch-settled — used for srUSDS / TEJRC / TISRC / Portfolio Halos) and **NFATS** (per-deal ERC-721 with Halo Unit / Halo Book separation, attestor-gated book lifecycle — used for Term Halos). The **Yield Splitter** turns any LCTS or ERC-4626 token into PT/YT pairs as standard ERC-20s; trading happens on whatever venue lists them — most naturally a Trading Halo AMM (oracle-referenced), with external orderbook venues and third-party AMMs as additional venue families. `rate-limit-attacks` calibrates IRL/SORL by trading Type 1 (config theft, 100% extraction) vs Type 2 (slippage extraction, ~10%).

## Section map

| § | Topic |
|---|---|
| §1 | PAU pattern + four-layer architecture |
| §2 | Configurator Unit — aBEAM/cBEAM, BEAMTimeLock, SORL |
| §3 | Diamond PAU |
| §4 | LCTS |
| §5 | NFATS |
| §6 | Yield Splitter |
| §7 | Rate-limit attack calibration |

---

## §1. PAU pattern + four-layer architecture

PAU = **Controller** (entry, enforces rate limits — `MainnetController`/`ForeignController`) + **ALMProxy** (custody, executes via `doCall()`) + **RateLimits** (linear replenishment, `maxAmount` + `slope`). Layers differ only in upstream/downstream wiring:

| Layer | Chain | Upstream | Downstream |
|---|---|---|---|
| Generator | Mainnet | ERC-20 stablecoin | Prime via ERC-4626 vault |
| Prime | Mainnet | Generator | Halos (incl. Core Halos), Foreign Primes |
| Halo | Mainnet | Prime | RWA / custodian / regulated endpoints |
| Foreign Prime | Altchain | Mainnet Prime via bridge (no vault) | Foreign Halos |
| Foreign Halo | Altchain | Foreign Prime | RWA on that chain |

Connection mechanisms: ERC-4626 vaults; direct ALMProxy↔ALMProxy bridge; CoreHaloFacet for Core Entities (Morpho/Aave/SparkLend). Three governance scopes: Generator / Mainnet / per-chain altchain. Targets approved as **general onboarding** (any PAU) or **limited onboarding** (specific PAU — bridge routes, KYC'd offramps). **Laniakea Factory** stamps audited PAU templates (Gen/Prime/Halo/Foreign + Skylink).

**Capital flow vs risk-capital flow run in parallel.** PAU flow = Generator→Prime→Halo→RWA. Risk-capital tokens (srUSDS / TEJRC / TISRC) issued via LCTS; Primes ingress them as capital base. User touchpoints: demand-side sUSDS, supply-side Folios. **Folio PAU spec deferred.**

**Architectural invariants:** rate limits universal; governance above contracts (no Controller redeployment for config); same contracts different config; **instant decrease, constrained increase**. PAUs are operated by high-auth action beacons (relayers, executors, sentinel formations) and all map to Layer-2 Synomic Entities.

## §2. Configurator Unit — aBEAM / cBEAM / SORL

Three contracts: **BEAMTimeLock** (OZ TimelockController + pause; all *additions* through 14-day delay), **BEAMState** (storage for inits + accordant mappings), **Configurator** (operational interface for cBEAMs; enforces SORL on increases).

**Two-tier access:**

| Role | Held by | Action class | Timelock |
|---|---|---|---|
| **aBEAM** | Core Council, Mom, Freezer | Register PAU; add init rate limit (global `pau=0` or restricted); add init controller action (e.g. `setMaxSlippage`); grant cBEAM | ✓ for additions |
| aBEAM | same | Unregister PAU, delete init, revoke cBEAM, pause timelock | ✗ instant (emergency) |
| **cBEAM** | GovOps ("accordant" to PAU) | `setRateLimit` (against existing init); `callControllerAction`; `setRelayer`; `setFreezer`; decrease/remove rate limit | SORL on increases only |

**SORL = canonical rate-limit-on-rate-limits.** Defaults: `hop = 18h`, `maxChange = 25%`. Decreases always instant. **This document is the canonical source for SORL parameters.** `hop`, `maxChange`, and timelock delay are themselves modifiable only through BEAMTimeLock.

**Invariants:** PAU must be registered before configuration; no rate-limit set without matching init; cBEAM check enforced; instant decreases never blocked.

**Onboarding:** aBEAM `setPauContracts` + `addInitRateLimits` + `addInitControllerActions` + `addGovOps` (all timelocked) → 14 days later GovOps `setRateLimit` + `callControllerAction` + `setRelayer` (typically self) → deploy. Subsequent increases bound by SORL.

One Configurator Unit per scope (Generator / Mainnet / per-chain altchain).

## §3. Diamond PAU (placeholder, target architecture)

EIP-2535 Diamond proxy replaces the legacy single-Controller design — Solidity 24KB bytecode limit binds as integrations grow. Diamond proxy routes selectors to facets (illustrative: ERC4626Facet, SwapFacet, MorphoFacet, NFATFacet, AdminFacet); upgrades happen via `diamondCut` per facet. Diamond storage pattern (namespaced `bytes32` slots) avoids collisions. ALMProxy + RateLimits unchanged. Configurator integrates identically — sees facet functions transparently. Migration is per-PAU. **Spec is a placeholder; actual facet sets defined per phase.**

## §4. LCTS — Liquidity Constrained Token Standard

Queue-based standard for capacity-constrained conversions. Paired **SubscribeQueue** + **RedeemQueue**, each driven by `lcts-{halo}` (high-auth action/executor beacon holding LCTS-pBEAM) calling `lock()` / `settle(capacity)`.

| Entity | Token | Role |
|---|---|---|
| Generator | srUSDS | External pooled Senior Risk Capital |
| Prime | TEJRC | Tokenized External Junior Risk Capital |
| Prime | TISRC | Tokenized Isolated Senior Risk Capital |
| Halo | Halo Unit shares | Default for capacity-constrained Portfolio Halos |

Risk-capital tokens MUST use LCTS. Halo Units default to LCTS but may use NFATS or stablecoin-style vaults instead.

**Single-generation + hard-lock model.** At most one current generation in ACTIVE/LOCKED, plus 0+ FINALIZED. Queue may be DORMANT.

```
DORMANT --(first sub/redeem)--> ACTIVE --(lock)--> LOCKED --(settle)--> ACTIVE
                                  ▲                    │
                                  └─ FINALIZED → DORMANT (if drained)
```

Daily cadence: **Lock 13:00 UTC, Settle by 16:00 UTC**, immediate unlock. LOCKED blocks all current-gen mutations (FINALIZED gens still claimable). A generation may span multiple days if capacity-constrained.

**Share math:** `shares = amount × totalShares / totalUnderlying` (1:1 if first). Reward accrual via `rewardPerToken` accumulator + per-user `rewardDebt` snapshot. All ops O(1). **Settle:** `convertAmount = min(capacity, totalUnderlying)` → move underlying to converter (Holding System) → mint reward asset → update accumulator. Drained → FINALIZED + DORMANT.

**Capacity sources** (srUSDS): (1) net flow netting; (2) OSRC capacity (governance pre-auction; auction-cleared once live); (3) per-epoch redemption limit. At most one side accumulates a multi-day backlog. **Target spread mechanism (srUSDS):** `lcts-{halo}` reduces subscribe capacity if demand would compress yield below governance-set spread above SSR.

**Exchange rate interface (required):** `exchangeRate() → uint256` returning underlying-per-1e18-shares. Increases on yield, decreases on haircut. Required for **Yield Splitter** integration.

**Holding System** backs srUSDS with sUSDS; funded by Prime PAUs (Core Council multisig pre-funding temporarily). USDS auto-converts to sUSDS on subscribe so users earn savings yield while queued.

## §5. NFATS — Non-Fungible Allocation Token Standard

Bespoke per-deal deployment between Primes and Halos. Each NFAT (ERC-721) is a **Halo Unit** (liability) — claim on a **Halo Book** (asset; balanced ledger; bankruptcy-remote boundary). **Onchain (NFAT):** custody, ownership, facility params, principal, depositor, mint timestamp. **Offchain (Synome):** APY, term / maturity, payment schedule, maturity date, book assignment, book contents (via attestor).

**Halo Class = NFAT Facility = PAU + NFAT extensions** (queue, ERC-721 minting, redeem contract). Buybox = acceptable parameter ranges. Two beacons: **`nfat-{halo}`** (high-auth action/executor — claims from Prime queue, mints NFAT, changes book status, funds redemptions) and **`attest-data-{class}`** (high-auth input/attestor — posts risk attestations; cannot move capital).

**Unit ↔ Book mapping.** 1:1 simple; many-units : one-book (privacy via blending); recursive (Book A holds units from Book B → tranching). Pari passu within a book; full isolation across books. **Terms source:** general buybox or **ecosystem accord** (pre-negotiated overriding buybox).

**Queue.** Share-based like LCTS but **no generations, no lock window**. Withdraw any time before claim. `nfat-{halo}` claims selectively: `claim(target, amount)` burns shares proportionally → mints NFAT → moves sUSDS to Facility ALMProxy.

**Book lifecycle:** `CREATED → FILLING (USDS) → DEPLOYING (obfuscated, high CRR) → AT REST (attested, medium CRR) → UNWINDING → CLOSED`. **Two-beacon deployment gate:** `attest-data-{class}` posts pre-deployment attestation before `nfat-{halo}` flips to DEPLOYING — independent validation. CRR by phase qualitative here; numeric values owned by `risk-framework/capital-formula.md`. Obfuscation purpose: blending loans in one book prevents outsiders inferring individual terms.

**Redemption (claim ticket model):** Halo deposits funds into Facility redeem contract; Prime burns/spends NFAT to claim. Patterns: bullet (burn at maturity), amortizing (spend NFAT, principal reduced), periodic interest (claim, NFAT unchanged). Halo penalized if late; Prime can delay with no penalty. NFATs transferable; optional KYC whitelist. **Wrapped NFATs** (optional): NFAT in wrapper → fungible ERC-20 for fractional ownership of that specific deal. NFATS positions itself as a **superset of RiverUSDS / ERC-7540** when deposits are pre-agreed and tokens have transfer restrictions.

## §6. Yield Splitter (Fixed Rates)

Single contract splitting any yield-bearing Sky token into a **Principal Token (PT)** + **Yield Token (YT)** for a given maturity. PT = zero-coupon bond redeemable 1:1 for underlying at maturity; YT = receives all yield until maturity, worthless after.

**Architecture:** one contract, **Token Registry** (permissionless registration if token exposes `exchangeRate()`) + many **buckets** per `(token, maturity)`. Bucket creation permissionless; PT/YT deployed as ERC-20 clones via CREATE2 (deterministic addresses).

**Supported tokens:** sUSDS/sSGA (via `convertToAssets(1e18)`), srUSDS/srSGA/TEJRC/TISRC/Halo LCTS tokens (via LCTS `exchangeRate()`).

**Operations:**
- **Split:** `ptAmount = ytAmount = amount × currentExchangeRate / 1e18` (in underlying-asset-denominated units).
- **Merge** (pre-maturity): burn equal PT+YT, settle YT pending yield, return underlying.
- **RedeemPT** (post-maturity): snapshot `finalExchangeRate` on first call; `tokensOut = amount × 1e18 / finalExchangeRate`.
- **ClaimYield** (anytime): `pendingYield = ytBalance × (pyIndex - ytRewardIndex[user]) / 1e18`.

**PY Index ratchet:** `pyIndex = max(pyIndex, newRate)` — never decreases. On haircut: PT principal protected (YT yield pauses); if rate at maturity is still below PY Index, PT redeems below par. **Risk hierarchy:** YT absorbs moderate decreases (paused yield); PT absorbs extreme unrecovered losses.

**Trading is venue-agnostic.** PT and YT are standard ERC-20s; the Yield Splitter contains no AMM curve, no orderbook, and no protocol-level liquidity management. Three venue families can list PT/YT:

| Venue family | Fit | Notes |
|---|---|---|
| **Trading Halo AMM (oracle-referenced)** | Strong fit for PT — closed-form NAV trajectory of a zero-coupon claim is well-suited to oracle/governance-set rate curves; no impermanent loss; standard PAU + rate-limit envelope. YT is harder to oracle-price and may be quoted with a wider spread or routed elsewhere. | Most likely first venue in the current roadmap (Phase 5+ Halo factory stack). |
| **External orderbook venue** | Natural fit — zero-coupon bonds (T-bills, STRIPS) trade on orderbooks in TradFi. Multi-maturity on one venue, professional fixed-income market making, direct rate discovery via bid/ask. | A native Sky orderbook venue is **not currently scheduled**. |
| **Third-party AMM** | Permissionless — PT/YT can be listed on any external AMM that lists ERC-20s. | Liquidity emerges where market makers choose. |

Implied rate (any venue): `(1 / PT_Price)^(1/years) - 1`. Naming: `PT-{TOKEN}-{MATURITY}`, `YT-{TOKEN}-{MATURITY}`.

YT transfers must hook back into Splitter (`onYTTransfer`) to update yield accounting — implementation choice between callback or making the Splitter the YT token.

**Roadmap:** PT/YT markets become useful once at least one trading venue lists them; in the current roadmap that is most likely a Trading Halo (Phase 5+ Halo factory stack). Native Sky orderbook is not currently scheduled.

## §7. Rate-limit attack calibration

Two attack categories constrain IRL and SORL. Both require compromised Guardian (relayer key + cBEAM).

| Attack | Mechanism | Profit | Capital | Eliminable? |
|---|---|---|---|---|
| **Type 1 — Configuration theft** | Onboard rate limit to misconfigured/uninitialized vault, accumulate, drain via e.g. Morpho donation | 100% of loss | Minimal (gas) | Yes — atomic slippage limits at onboarding |
| **Type 2 — Operational extraction** | Cycle capital through routes with slippage; capture via MEV sandwich (~10%) or shorting (~1-2%) | ~10% of loss | ≈ attack size | No (inherent to DEX) |

**Bootstrap constraint:** `IRL × (1 + SORL)^30 = 100M` (peacetime: one SORL step/day, 30 days to 100M/day target).

**Harm model:**
```
Total Harm = N₁ × [3 × IRL × (1 + 0.25×SORL) + 6M × (1.25×SORL + 0.25×SORL²)]
```
Theft Multiplier = 3×, Surface Ratio R = N₂/N₁ = 3×. N₁ factors out — only ratios matter.

**Continuous optimum: SORL ≈ 25.5%, IRL ≈ $109K. Adopted: SORL = 25%, IRL = $100K.** Total Harm ≈ $2.36M per N₁. Bootstrap to 100M/day in ~31 days.

**TTS** (Time-to-Shutdown) = 24h under current model. SORL `hop = 18h` lets attacker get two cooldown bumps within TTS. **Optimal SORL % is independent of target scale** — only absolute values change.

**Guardian ORC:** `ORC ≥ Type 1 Max Loss × N₁ ≈ $100K × 1.0625 × 10 ≈ $1.06M` for N₁=10.

**Priority mitigation:** atomic slippage limit configuration at vault onboarding eliminates Type 1 entirely.

---

## Key vocabulary

| Term | Meaning |
|---|---|
| PAU | Parallelized Allocation Unit — Controller + ALMProxy + RateLimits |
| Diamond PAU | EIP-2535 faceted upgrade replacing monolithic Controller |
| Configurator Unit | BEAMTimeLock + BEAMState + Configurator — governance over a PAU set |
| aBEAM / cBEAM | Admin BEAM (Core Council, timelocked) / Configurator BEAM (GovOps, accordant to PAU) |
| Accordant | GovOps holding a cBEAM for a specific PAU |
| Init | Pre-approved rate-limit or controller-action template a cBEAM can instantiate |
| SORL | Second-Order Rate Limit — `hop`/`maxChange` (default 25%/18h). **Canonical here.** |
| IRL | Initial Rate Limit (adopted: $100K) |
| LCTS | Liquidity Constrained Token Standard — generation queue, daily lock/settle |
| LCTS-pBEAM / `lcts-{halo}` (class: relay) | Permission + beacon for `lock()`/`settle()` |
| Generation | LCTS cohort sharing capacity proportionally |
| NFATS | Non-Fungible Allocation Token Standard — per-deal ERC-721 |
| NFAT Facility / Halo Class | PAU + NFAT extensions with a buybox |
| Halo Unit / Halo Book | Liability side (the NFAT) / asset side (balanced ledger; bankruptcy-remote boundary) |
| `nfat-{halo}` / `attest-data-{class}` | High-auth action (executor) and input (attestor) beacons for an NFAT Facility |
| Buybox / Ecosystem accord | Acceptable parameter range / pre-negotiated terms overriding buybox |
| Yield Splitter / Bucket | Single contract / `(token, maturity)` pair with own PT, YT, PY Index |
| PT / YT | Principal Token (par at maturity) / Yield Token (captures all yield) |
| PY Index | Splitter's tracked exchange rate; ratchets upward only |
| Trading Halo AMM | Oracle-referenced AMM (PAU + rate-limit envelope); primary venue family for PT |
| TTS | Time-to-Shutdown (24h in Phase 1) |
| Theft Multiplier / Surface Ratio | 3× / N₂/N₁ = 3× — harm model weights |
| Holding System | Backs srUSDS with sUSDS; sources redemptions, absorbs haircuts |

## Cross-references

- `macrosynomics/beacon-framework.md` — beacon taxonomy; relay/sentinel classification
- `macrosynomics/synome-overview.md` — five-layer architecture
- `accounting/daily-settlement-cycle.md` — LCTS lock/settle synchronized
- `accounting/risk-capital-ingression.md` — Prime ingress of srUSDS/TEJRC/TISRC
- `risk-framework/capital-formula.md` — owns numeric CRR for NFAT phases
- `risk-framework/operational-risk-capital.md` — ORC sizing
- `synomic-entities/halo-portfolio.md` — Portfolio Halos use LCTS
- `synomic-entities/halo-term.md` — Term Halos use NFATS
- `synomic-entities/halo-trading.md` — Trading Halo (oracle-referenced AMM); primary venue family for PT/YT
- `synomic-entities/folio.md` — Folio (full Folio PAU spec deferred)
- `sentinel/sentinel-network.md` — sentinel formations operating PAUs
- `roadmap/roadmap-ideas.md` / `roadmap/phase-1-spaces.md` — phase progression context for LCTS / NFATS / Yield Splitter rollout

## File map

| File | What's in it that the summary doesn't have |
|---|---|
| `architecture-overview.md` | Full ASCII capital-flow diagram; per-layer narrative; connection-type table; per-layer governance scope; supply/demand-side touchpoints |
| `configurator-unit.md` | Full Solidity interfaces (`BEAMState`, `BEAMTimeLock`, `Configurator`, `BEAMRoleTimeLock`, `BEAMRoleDirect`); ASCII architecture diagram; three end-to-end user stories; admin-role prerequisites; default parameters table |
| `diamond-pau.md` | Legacy vs Diamond comparison; ASCII facet diagram; illustrative facet list; diamond storage code snippet; migration steps |
| `lcts.md` | Full per-queue behavior specs; 7 user stories (multi-epoch, dormant restart, etc.); edge-case list; gas table; srUSDS subscribe/redeem flow diagrams; capacity-determination factors |
| `nfats.md` | Full Halo class diagram; 12 detailed scenarios (bullet, partial, amortizing, secondary, late-funding, multi-prime, whitelist, default, etc.); book-lifecycle state machine; attestor flow diagram; payment patterns; RiverUSDS/ERC-7540 mapping; wrapped NFAT detail |
| `fixed-rates.md` | Token-registry table; bucket-lifecycle ASCII; precise yield-attribution math; negative-yield (haircut) handling; PT/YT property table; YT transfer-hook options; venue-family rationale (Trading Halo AMM oracle-pricing argument; orderbook fixed-income parallel; third-party AMMs); 5 user stories; gas table |
| `rate-limit-attacks.md` | Type 1 (Morpho donation) and Type 2 (Uniswap sandwich) attack timelines; profit models (MEV vs short); accumulation factor derivation; bootstrap-constraint table; harm-model derivation; sensitivity tables; bootstrap timeline day-by-day; mitigations table |
