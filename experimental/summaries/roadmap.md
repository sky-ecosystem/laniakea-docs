# Roadmap

**Status:** `phase-1-overview.md` is the orientation entry point; `phase-1-spaces.md` v4 is the canonical live Phase 1 spec (66 fixed Spaces, 7 active Primes, 3 P1 Halos, daily synomic settlement cycle, treasury, market-memory oracle, Lindy SDR production, ownership-weighted temporary SDR auction); `p1-nfat-atom-trace.md` is the resolved atom-level trace; `attestor-atom-schema.md` defines borrower admission + exobook attestation; `roadmap-ideas.md` carries the lift / insyn-exsyn / temporary-equation / DSC / market-memory development discipline; `v1-principles.md` distills the current invariants.
**Canonical home:** `lani/roadmap/`

---

## TL;DR

Roadmap docs are the live carve-out layer for Laniakea: the main corpus describes target architecture, while `roadmap/` states what exists in each phase and how future phases extend it additively. Phase 1's single deliverable is **real-time ER per Prime**, emitted continuously by synserv. P1 has 66 fixed Spaces, 7 active Primes, 3 P1 Halos (`spark-term`, `grove-term`, `maple-term`), `nfat-term` halo class, `custodial-crypto` risk class, per-halo attestor sub-Spaces, daily DSC for structural-demand processing, and no Core Entity halo-mode.

The important 2026-05-17 cleanup: P1's demand side is now a real synomic loop, not sudoed allocations. `&core.settlement` holds the daily epoch; synserv cuts at 13:00 UTC, processes 13:00-16:00 UTC, and advances at 16:00 UTC. `&core.treasury` stores clean treasury facts (Sky-controlled addresses and Sky Prime token share). `&entity.generator.usge.structural-demand` holds the lot-age surface, Lindy SDR, SDR policy overlay, and effective SDR bucket capacity; `&entity.generator.usge.sdr-auction` contains the temporary ownership-weighted SDR auction. Legacy monthly settlement remains entirely out-of-band and invisible to the synome.

## Section Map

§1 Directory contract · §2 Phase 1 live reality · §3 Fronts · §4 Lift patterns · §5 Beacons · §6 Worked example · §7 Attestation / borrower onboarding · §8 Current open work

## §1 Directory Contract

Each phase doc answers: what Spaces exist, what each holds, which loops / beacons write there, which atoms are fixed vs operational, and what later phases add without moving read paths. Any sudo event during a phase is a phase boundary. Fronts are an orientation device, not a topology layer.

| Phase | Focus |
|---|---|
| **1** | Real-time ER per Prime; daily DSC for structural-demand processing; Lindy SDR production + temporary SDR auction; manual economic settlement / penalty action outside synome |
| **2-4** | Settlement closure / TMF / LCTS and the first canonical propagation sources |
| **5-8** | Factory stack for Halo / Prime / Generator expansion |
| **9-10** | Sentinel formations; real OSRC + SDR auctions; SDRR with fee attribution |
| **Beyond** | Richer cognitive recipes and generalist teleonomes |

## §2 Phase 1 Live Reality

**Topology totals**

| Category | Count |
|---|---:|
| Universal `&core.*` (`syngate`, `loop.synserv`, `registry.beacon`, `test-suite`, `settlement`, `treasury`) | 6 |
| Generator (`usge`: root + structural-demand + auction + protocol-registry) | 4 |
| Oracle (Crypto Majors: root + market-data + ticks) | 3 |
| Per-Prime ×7 (root + primebook + structbook + relay + protocol-registry) | 35 |
| Per-Halo ×3 (root + nfat-term + custodial-crypto + custodial-crypto.attest-data + relay + protocol-registry) | 18 |
| **Fixed Spaces at genesis** | **66** |
| Constructor-made (halobooks, riskbooks, exobooks) | unbounded |

**Architectural cuts**

- **All logic in synlang from day 1.** CRR, routing, ER, equity invariants, loop bodies, constructors, Lindy SDR, and the temporary SDR auction are real synlang. Python is only for grounded primitives.
- **Insyn/exsyn TRRC split.** `TRRC = insynTRRC + exsynTRRC`; `TRC` is synome-tracked; `ER = TRRC / TRC`. Per-Prime patch-beacons write exsyn-TRRC claims directly into each primebook until those exposures migrate insyn.
- **Phase-invariant consumption sites.** Risk forms, loop bodies, structural-demand allocations, and treasury facts are read from their long-term locations in P1. Later phases change provenance, not read paths.
- **Daily synomic settlement cycle (DSC).** DSC is the only settlement cadence visible to the synome. Legacy monthly settlement is out-of-band. P1 uses DSC for structural-demand processing.
- **Demand side.** Effective SDR bucket capacity is computed in P1 from the scraped lot-age surface, Lindy SDR, and the governance-set SDR policy overlay. Buckets are 30-day / 51 total. The P1 allocator splits every bucket across active Primes by ownership weight: `0.05 + 0.95 * Sky token share`, multiplied by Prime IJRC. Structbooks read only current-epoch allocation atoms, with no reservation market or carry-forward accounting.
- **Treasury.** `&core.treasury` stores clean financial facts only: Sky-controlled addresses and raw Sky Prime token share. The temporary ownership-weight formula lives entirely in the auction body.
- **Risk form.** `custodial-crypto` is a stress-envelope model over exobook assets and liability waterfall. It outputs default, spread, rate, and liquidity CRR components. CORE is calibration / reference, not the direct P1 engine.
- **Market memory.** Crypto Majors Oracle stores reducer outputs and checkpoints derived from raw source tapes held by archive nodes. The same reducer formulas run historical replay and live-tail.
- **Attestation.** Borrower admission lives at risk-class / halo-class level; exobook attestation checks deal-specific facts such as term / maturity enforceability. Missing or failing attestation excludes the exobook.
- **Constructor-made books.** Halobooks / riskbooks / exobooks are created by govops flows, not sudo. Exobooks can enter a staged pre-send state with reserved funds still in the Halo PAU.
- **Authority.** `&core.registry.beacon` is the authority root. No standing Guardian entart in P1.

## §3 Fronts

**Structural fronts**

- **Core:** substrate Spaces, DSC, treasury, beacon registry, test suite.
- **Prime-Halo:** ER pipeline, halobook/riskbook/exobook constructors, attestations, risk form, structbook rollup.
- **Demand Side:** Generator structural-demand capacity, pro-rata SDR allocation, treasury input, market-memory inputs.

**Operator fronts**

- **synserv:** heartbeat, DSC state machine, processing-task dispatch, ER recomputation.
- **govops:** constructors, deploy / rollover / withdraw flows, unlaunched-token treasury values, capacity policy atoms.
- **Attestor Oracle:** borrower admission and exobook/riskbook attestations.
- **Market Oracle:** Crypto Majors market memory.
- **patch beacon:** temporary exsyn-TRRC gap filler per Prime.
- **test-runner:** shadow-frame acceptance suite.

## §4 Lift Patterns

`roadmap-ideas.md` is the canonical pattern doc.

- **Lift principle:** code is synlang; data is atoms; grounded primitives stay grounded.
- **Insyn/exsyn:** split quantities by epistemic provenance; shrink exsyn over time without changing synlang consumers.
- **Phase-invariant consumption sites:** the read path exists in P1 and survives later provenance migrations.
- **Black-box deferral:** keep the signature real when the body is not yet known.
- **Temporary-equation body:** use real provisional synlang when the body is known to be temporary. P1 pro-rata SDR allocation is the canonical case.
- **Temporary-equation containment:** keep temporary logic inside the body that will later be swapped; keep long-term systems clean.
- **DSC:** capabilities enter the synome by entering the daily synomic settlement cycle; there is no in-synome monthly cycle.
- **Market memory:** raw history lives in archive nodes; reducer outputs live in synome; replay and live-tail use the same formulas.

## §5 Beacons

P1 beacons are deterministic programs, not AI teleonomes. Approximate identities: canonical synserv, market-data-crypto-majors providers, three attestor loops, seven patch-beacons, seven prime govops relays, three halo govops relays, and test-runner.

| Class | Notes |
|---|---|
| `synserv` | Heartbeat, ER, DSC, processing-task dispatch |
| `market-data-beacon` | Pushes market-memory reducer outputs and current-state atoms |
| `attest-data-beacon` | Per-risk-class attestation loop; writes admission / riskbook / exobook attestations |
| `patch-beacon` | Guardian-sudoed exsyn scaffold, used for per-Prime exsyn-TRRC claims |
| `govops-prime` / `govops-halo` | Constructor and operational relay bodies |
| `test` | Shadow-frame only |

## §6 Worked Example

The worked NFAT example lives in `phase-1-spaces.md`. Current shape:

1. A Halo govops relay stages an exobook and exo unit with reserved USDC/USDS/USDT still in the Halo PAU.
2. Borrower admission has already whitelisted the borrower through Core Council / configurator process, with a disbursement account and collateral account recorded.
3. Exobook-level attestation verifies deal-specific facts, especially the maturity / TTM claim.
4. After funds leave the PAU and the funding transaction confirms, the exobook becomes funded and eligible for rollup.
5. The risk form runs approved stress scenarios over BTC/ETH/stETH/USDC/USDT market-memory inputs and projects losses through the exobook waterfall.
6. The risk form returns four CRR components. For P1 structbook, SDR-matched portions make spread/rate/liquidity non-binding; default loss remains capitalized. Unmatched portions carry forced-loss / rate treatment.
7. Structbook reads current-epoch `sdr-allocation` atoms from `&entity.generator.usge.sdr-auction`, blends matched/unmatched, contributes insynTRRC, and primebook emits ER.

## §7 Attestation / Borrower Onboarding

`attestor-atom-schema.md` is now broader than "boolean schema." It covers:

- borrower admission at risk-class / halo-class level;
- `disbursement account` (where funds are sent) and `collateral account` (where collateral / liquidation claim is tracked);
- Core Council `aBEAM` / configurator whitelist coordination;
- first-contact attestation before a borrower can receive funds;
- ongoing riskbook / exobook attestation;
- staged pre-send exobook lifecycle.

The attestor is not a numeric oracle. Quantitative market / chain facts come from chain reads and market memory. The attestor gates legal, custody, account, term, and operational facts.

## §8 Current Open Work

Open details are calibration and tracing, not topology:

- exact P1 stress scenario catalog and scenario constants;
- exact market-memory reducer catalog for Crypto Majors;
- full atom-level NFAT trace after the latest staged-exobook / risk-form / settlement updates;
- later open-ended endoscraper primitive surface for live Lindy lot-age scraping;
- later real OSRC + SDR auction machinery and SDRR fee attribution.

## Cross-References

`noemar-synlang/topology.md` · `noemar-synlang/runtime.md` · `macrosynomics/beacon-framework.md` · `risk-framework/custodial-crypto-risk-form.md` · `risk-framework/market-memory-oracle.md` · `risk-framework/primebook-composition.md` · `risk-framework/matching.md` · `accounting/settlement-cycle.md` · `accounting/sdr-auction.md` · `synodoxics/lift.md`

## File Map

| File | What it adds beyond this summary |
|---|---|
| `phase-1-overview.md` | Fronts orientation and topology-by-front enumeration of the 66 fixed Spaces |
| `phase-1-spaces.md` | Canonical P1 v4 Space-by-Space spec, genesis steps, tests, ER diagram, and worked NFAT example |
| `p1-design-followups.md` | Locked decisions and remaining open calibration / atom-trace work |
| `attestor-atom-schema.md` | Borrower admission, disbursement/collateral account vocabulary, first-contact and exobook attestation, staged lifecycle |
| `roadmap-ideas.md` | Lift / insyn-exsyn / phase-invariant / temporary-equation / DSC / market-memory patterns |
| `v1-principles.md` | Current P1 invariants |
| `asc-transition.md` | ASC / DAB / peg-defense transition details |
