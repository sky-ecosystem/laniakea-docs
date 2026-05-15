# Pylon Entity

**Status:** Stub spec — type designation. Token model and governance shape confirmed; loss-waterfall and capital-layer structure specified; many parameters open. No instantiations yet.

A Pylon Entity is a synomic entity that takes principal positions in derivatives, faces customers (primarily Primes and Folios), and mutualizes solvency with peer Pylons through Ring coalitions hosted inside Sequencer Entities. The collateralized Pylon layer + mutualized Ring assurance fund + winner haircut replaces the perpetual-exchange ADL pattern; losses are absorbed by pre-funded capital and recovery tools, not propagated to surviving traders by surprise.

For Synomic Entity theory, see [`../macrosynomics/synomic-entities.md`](../macrosynomics/synomic-entities.md). For the matching-venue counterpart, see [`sequencer-entity.md`](sequencer-entity.md).

---

## Properties

| Property | Description |
|---|---|
| **Rank** | 2 (accordant to a Guardian) |
| **Scope** | Multiple Pylons coexist; a Pylon may belong to one or more Ring coalitions across one or more Sequencer Entities |
| **Function** | Take principal positions in derivatives; face Primes / Folios as customers; contribute to Ring assurance funds; absorb own customer-default losses with own capital |
| **Dependencies** | Accordant to Ozone; routes orders through Sequencer Entities; coordinates with peer Pylons via Ring accord |
| **Governance** | **Tokenized** — Pylon governance token; decentralized capital-weighted governance via token holders (Prime-style) |

---

## Ring Coalitions

A **Ring** is the inter-Pylon accord pattern that operates a single derivatives market — not itself an entity. A Ring lives **inside the hosting Sequencer Entity's entart** as a sub-structure (e.g., `&entity.sequencer.{id}.ring.{ring-id}`). Each Ring is parameterized by:

- A **product** (BTC perps, ETH perps, FX pair, exotic structure)
- A **Pylon membership** (≥ 2 Pylons; new Pylons join through Ring-membership accord)
- An **assurance-fund target** (the size the Ring's pre-funded mutual default fund must reach)
- **Margin schedules** (initial and variation margin requirements for customer positions)
- **Recovery-tool spec** (VMGH parameters; optional partial tear-up; dissolution threshold)
- An **attestation accord** with one or more Oracle Entities for aggregate health reporting

### Minimum viable Ring

```
Ring = ≥ 2 Pylons + ≥ 1 Sequencer + accord protocol
```

- **Two Pylons** is the structural minimum — mutualization requires at least one peer to underwrite against. A single-Pylon "Ring" is just that Pylon's own collateral, which isn't mutualization.
- **One Sequencer** is required because a derivatives market without a matching venue is a credit facility, not a market.
- The **accord protocol** is the synomic encoding of Ring rules: membership criteria, contribution requirements, margin schedules, recovery-tool sequence, dispute resolution.

### Criss-cross membership

Pylons may belong to multiple Rings across multiple Sequencer Entities. Memberships are independent and siloed:

- Sequencer A may host Rings for BTC perps and ETH perps; Sequencer B may host its own BTC perps Ring (different membership) and a Eurodollar Ring.
- A Pylon's per-Ring pledge to Ring X is fully isolated from its per-Ring pledge to Ring Y, regardless of whether X and Y are at the same Sequencer.
- A Sequencer compromise / retirement kills only its own Rings; Pylons keep memberships at other Sequencers intact.

This makes Pylons compete on (1) Ring portfolio, (2) pricing and customer relationships, and (3) capital efficiency — see [§ Differentiation](#differentiation).

### Ring creation as product listing

Ring creation is a **product decision, not an entity-creation decision**. A coalition of prospective Pylons proposes Ring parameters to a Sequencer; the Sequencer accepts via Guardian Accord and instantiates the Ring inside its entart; Pylons post initial assurance-fund contributions and the Ring goes live. New Rings retire cheap (Sequencer removes them from its entart after positions wind down).

Value capture (5% Entity Creation Fee + 50 bps/yr Entity Upkeep) accrues at the Pylon level, not the Ring level — Pylons are the persistent governance-token-holding entities; Rings are configurations of accord parameters they participate in.

---

## Pylon Capital Structure

A Pylon's capital is organized in three layers with cleanly separated roles in the loss waterfall:

| Layer | Purpose | Touchable by own-customer default? | Touchable by Ring mutualization? |
|---|---|---|---|
| **Sky regulatory minimum** | Pylon entity-viability floor (staff, infrastructure, compliance) | **No** | **No** |
| **Extra capital** (voluntary) | Cushion above the regulatory floor; absorbs own customer-default residuals before Ring fallback | **Yes — absorbs first** | **No — protected** |
| **Per-Ring pledges** | Pre-funded contributions to specific Rings' assurance funds | **Yes — after extra capital exhausted** | **Yes — this is the assurance fund contribution** |

The discipline is asymmetric: **extra capital is at risk only when the Pylon's own underwriting fails. Other Pylons' failures can only reach the Pylon's per-Ring pledges, never its general balance sheet.** This is the FCM/CME pattern transcribed — FCM general capital (ANC) absorbs own customer defaults; FCM guaranty-fund contribution is the mutualized layer.

### Sky regulatory minimum

A baseline capital requirement Sky imposes on any entity operating as a Pylon. Sized to keep the entity operationally viable (paying recurring upkeep, maintaining beacons, satisfying continuous attestation obligations). Never burned for trading losses — protected from both own-customer-default cascades and Ring mutualization. Conceptually similar to a bank's CET1 minimum: a floor below which the entity ceases to be a Pylon in good standing.

### Extra capital

Voluntary capital held above the regulatory minimum, at the Pylon's discretion. Functions as a corporate buffer that absorbs the Pylon's own customer-default residuals before the Pylon defaults to any Ring. Pylons that take risky customers without legal recourse burn through extra capital fast; conservative Pylons rarely touch it.

**Extra capital is not load-bearing for risk-treatment of Ring units.** The Prime risk-treatment equation for Ring-issued positions treats extra capital as zero — pricing Ring units conservatively under the assumption that any customer default immediately triggers mutualization. Reality is usually better (extra capital absorbs most defaults before mutualization fires), but the model doesn't depend on it.

This conservative-modeling discipline serves two purposes:
- **Prevents single-Ring arbitrage.** If extra capital state affected Ring-unit CRR, single-Ring Pylons could arbitrage by holding huge extra capital with no diversification penalty. Multi-Ring Pylons would be disadvantaged. The model staying blind to extra capital preserves the multi-Ring incentive structure.
- **Reflects extra capital's bilateral nature.** Extra capital only protects the specific Pylon's own customer-default cascade. Other Pylons in the Ring see no direct benefit. Its value accrues to the Pylon (fewer mutualization triggers) and to its customers (longer survival under stress), but not to the Ring as a whole.

Extra capital is the **competitive moat** — Pylons with more of it can quote tighter customer pricing (lower realized customer-default costs) and signal operational continuity through stress. Token holders price it; the risk model ignores it.

### Per-Ring pledges

Pre-funded capital pledged to a specific Ring's assurance fund. Each Ring's assurance fund is the sum of its members' pledges, sized by the Ring's parameters (per-Pylon floor + Ring-aggregate Cover-N target, see § [Assurance fund sizing](#assurance-fund-sizing)).

Per-Ring pledges are the **only system-recognized loss-absorbing capital**. The risk model reads them when pricing Ring units; mutualization waterfalls consume them; recovery tools activate when they're exhausted.

Per-Ring pledges are siloed: Ring A losses consume only Ring A pledges. A Pylon's Ring B participation is structurally insulated from any Ring A event.

### SORL-bounded pledge rebalancing

A Pylon can reallocate capital across its Ring memberships, but movement is rate-limited to prevent reactive escape from mutualization:

- **Pledge increases** to any Ring are instant. Adding capital is always allowed.
- **Pledge decreases** require settlement-boundary processing and an advance-notice lockup (≥ 1 epoch, attestable to other Ring members so they can adjust positioning).
- **Full exit** from a Ring requires a longer lockup with continued obligation through the window — analogous to CME Rule 913.A's 5-business-day post-obligation withdrawal period. Pylon must satisfy outstanding mutualization claims before exit takes effect.

This is the SORL pattern applied to Ring pledges: instant tightening, gated loosening. Same discipline as PAU rate limits. Reactive escape requires the friction window to be shorter than time-to-default-resolution, which it isn't.

---

## The Two Waterfalls

Loss absorption follows one of two distinct cascades depending on whose customer failed.

### Waterfall 1 — Pylon's own customer defaults

A customer of Pylon X defaults on a position in Ring R:

| Layer | What's consumed |
|---|---|
| 1 | Customer's posted margin (LSOC-segregated; customer-side collateral) |
| 2 | Pylon X's extra capital (absorbs the residual; Ring is unaffected) |
| 3 | If extra capital insufficient → Pylon X defaults to Ring R |
| 4 | Pylon X's per-Ring-R pledge |
| 5 | Surviving Pylons' per-Ring-R pledges (Ring R's assurance fund mutualization) |
| 6 | VMGH on Ring R winners (variation margin gains haircut) |

Most defaults stop at Layer 2. The Pylon eats the customer's loss with its own capital, Ring R's assurance fund is untouched, other Pylons in Ring R never know. Mutualization only fires when extra capital plus the Pylon's own per-Ring pledge are both exhausted.

### Waterfall 2 — Ring mutualization (triggered by another Pylon's failure)

Pylon Y in Ring R has defaulted because Y's extra capital and per-Ring-R pledge were exhausted by Y's own customer default. Now Y's residual loss enters mutualization:

| Layer | What's consumed |
|---|---|
| 1 | Defaulting Pylon Y's per-Ring-R pledge (already consumed at the end of Waterfall 1) |
| 2 | Surviving Pylons' per-Ring-R pledges only — **extra capital is NOT touched** |
| 3 | VMGH on Ring R winners |

The asymmetry is the key property: **other Pylons' failures can only reach your per-Ring pledge, never your general balance sheet.** A Pylon's extra capital is dedicated to its own underwriting decisions and is protected from peer-Pylon failures.

### What's absent

- **No Sequencer participation.** Sequencer holds no collateral, contributes nothing to any waterfall layer. Sequencer's accountability is purely operational (revocability for sequencing misbehavior) — see [`sequencer-entity.md`](sequencer-entity.md).
- **No Ring-entity skin-in-the-game.** Ring is not an entity; nothing at the Ring level absorbs loss other than the Pylon-funded assurance fund.
- **No assessments.** Pylons commit at most their pre-funded pledges. No callable layer demanding additional cash during a crisis. Capital exposure is fully knowable ex ante.
- **No Sky backstop in normal operation.** Sky Aggregate Backstop Capital does not absorb Ring losses. Recovery tools (VMGH, optional tear-up, optional Ring dissolution) cap loss at the Ring level. Only if a specific Ring is sanctioned as systemically significant under Core Council governance would Sky ABC enter the picture — and such designation is exceptional, not default.

---

## Customer Collateral Segregation (LSOC analog)

Customer margin posted to a Pylon is held in dedicated synomic structures the Pylon administers but does not economically own — analogous to CFTC Reg 1.20 / Part 22 LSOC ("Legally Segregated, Operationally Commingled").

- Customer margin is **not** Pylon equity. It doesn't appear on the Pylon's balance sheet for capital-adequacy purposes.
- On Pylon insolvency, customer margin is bankruptcy-remote — customer property has priority over Pylon general creditors against the segregated pool.
- Margin can be operationally commingled at the Ring / Sequencer level for efficiency, but each customer's share is legally allocated. A fellow customer's default cannot reach non-defaulting customers' collateral.

The Pylon's regulatory-minimum capital requirement (analogous to CFTC Reg 1.17's 8%-of-risk-margin rule) is calibrated against **gross customer risk margin**, not against customer collateral itself. Even though customers post the bulk of the margin, the Pylon must hold its own capital proportional to the gross risk it clears.

---

## Why the Pylon Bears Risk (vs. pure passthrough)

A Pylon could in principle pass all customer collateral straight to the Ring and hold no risk itself. It doesn't, because it bears three residual risks that customer collateral alone doesn't cover:

1. **Settlement-timing / VM advance.** When Ring positions mark to market and variation margin moves intra-epoch, the Pylon may need to settle to the Ring before the customer has funded their margin call. The Pylon fronts variation margin from its own capital during the gap. Sky's faster settlement cadence shrinks this gap vs. CME's hours-long window, but doesn't eliminate it entirely if the Pylon extends bilateral grace periods or off-chain credit.
2. **Customer credit / under-margining.** Customers can default with margin that's exhausted faster than the Pylon can liquidate the position. The Pylon eats the residual. Pylons that demand additional bilateral collateral (legal recourse, off-chain assets, parent guarantees) reduce this exposure; Pylons that take only on-chain margin absorb more.
3. **Operational / make-whole.** Errors in customer allocation, sequencing-acceptance mistakes, system outages — anything the Pylon promised but failed to deliver, the Pylon eats.

The 8%-of-risk-margin minimum (and the Pylon's voluntary extra capital above it) is calibrated to these residual risks. Customer collateral covers customer's own positions; Pylon capital covers the gap.

---

## Customer Relationships and Pricing

Pylon customers are primarily **Primes** (using Ring derivatives in their hedgebooks) and **Folios** (principal-controlled holders deploying capital). Customer relationships are bilateral, layered above Ring rules.

### Two-layer risk management

A Pylon manages risk at two distinct levels with different mechanics:

| Level | Scope | Mechanism |
|---|---|---|
| **Pylon-to-Ring** | Uniform per Ring rules | Per-Ring pledge, margin schedules, attestation cadence, ER caps — standardized; the mutualization waterfall operates over these uniform pledges |
| **Pylon-to-customer** | Bilateral, idiosyncratic | Margin terms (within Ring's customer-margin floor), legal recourse arrangements, additional collateral demands, KYC posture, fee structure — each Pylon-customer relationship is its own contract |

Ring rules set the **floor** for customer margin and the Pylon's mutualization obligation. The Pylon decides whether to demand additional protection from customers above the floor: ISDA-style master agreements, credit support annexes, third-party guarantees, custodied off-chain collateral (T-bills, real estate liens), tighter operational margin, withdrawal-notice requirements, geographic / KYC restrictions.

### Differentiation

Pylons in a Ring face identical risk per Ring rules, so they don't differentiate on raw risk-bearing. They differentiate on:

1. **Pricing.** The effective spread / yield / financing rate the Pylon quotes to a customer above raw Ring matching cost. Same risk under the Ring's rules, different prices. Institutional customers signing comprehensive legal recourse get tighter pricing (lower realized cost of customer default); retail or pseudonymous customers pay wider spreads.
2. **Relationship structure.** Long-term agreements that prevent pure-mercenary trade-by-trade shopping: capacity reservations (Prime pre-pledges flow, gets preferred pricing on guaranteed depth); volume-tier commitments with rate steps; preferred-routing arrangements; cross-product bundling.
3. **Ring portfolio.** Which Rings the Pylon participates in. A Pylon broadly active across correlated Rings (BTC perps + ETH perps + FX) can offer cross-margin offsets a single-Ring Pylon can't.
4. **Capital efficiency.** Underwriting and operational skill that lets the Pylon absorb customer defaults with less extra capital, leaving more room for tighter pricing without proportionally more risk.

This mirrors CME's FCM equilibrium: a small number of FCMs (post-consolidation ~10 economically significant) competing on **bundled** capital strength, cross-margin offsets, intraday credit policies, and relationship terms — not on raw matching fees.

### Cross-margin offset as Pylon-level commercial decision

Rings are fully siloed in mutualization terms. A Prime holding offsetting positions in BTC perps Ring and ETH perps Ring still posts full margin to each Ring per their respective margin schedules.

**Cross-margin offset is a Pylon-level commercial product**, not a Ring-level rule. A Pylon participating in both Rings can offer its Prime customers cross-Ring margin offset bilaterally — recognizing the customer's combined position and charging less aggregate margin than the Rings' floors. The Pylon absorbs the cross-Ring correlation risk: if both Rings crash together, the Pylon's customer defaults more than either Ring individually would predict. This is a deliberate underwriting choice the Pylon makes.

This is the FCM-style "bundled prime brokerage" moat: Pylons broad across many correlated Rings can offer cross-margin packages that single-Ring Pylons can't match. Earned through underwriting skill at the Pylon level, not built into Ring rules.

---

## Assurance Fund Sizing

Each Ring's assurance fund — the aggregate of member Pylons' per-Ring pledges — needs to be sized to absorb plausible stress. Two complementary framings:

- **Per-Pylon floor.** Each Pylon must contribute at least X% of its gross customer risk margin in that Ring as a per-Ring pledge (the Reg 1.17 8%-of-risk-margin analog). Ensures individual Pylons have meaningful skin in the game proportional to their book.
- **Ring-aggregate Cover-N target.** The total fund must absorb simultaneous default of the N largest Pylons in the Ring under a defined stress scenario. Contributions are allocated pro-rata to scaled Pylon exposure if the sum of floors falls short of Cover-N.

In practice both rules apply: a per-Pylon floor ensures individual underwriting discipline; a Ring-aggregate target ensures systemic depth. If per-Pylon floors already sum to ≥ Cover-N, the extra is surplus safety. If they sum to less, Pylons top up pro-rata to meet the Cover-N target.

Specific N (Cover-2, Cover-3, ...) and stress-scenario parameters are Ring-level governance decisions, set at Ring instantiation and revised by member accord. Conservative Rings (institutional customers, low-recovery-tool spec) target Cover-3 or higher; aggressive Rings target Cover-2.

---

## Recovery Tools

When a Ring's assurance fund is exhausted, recovery tools cap further loss before the Ring is forced into dissolution. Each Ring's accord specifies which tools apply, at what trigger, and how.

| Tool | Mechanism | Trade-off |
|---|---|---|
| **VMGH** (variation margin gains haircutting) | Winners on the period give back a fraction of their gains pro-rata to cover residual loss | Standardized; predictable; spreads loss across winners regardless of fault |
| **Partial tear-up** | Defaulter's remaining positions are forcibly closed at imposed prices; assigned to matching counterparties | Operationally complex; controversial; concentrates loss on specific survivors |
| **Forced allocation** | Survivors required to take on portions of defaulter's portfolio at clearing prices | Most invasive; rarely used; preserves market continuity in worst cases |
| **Ring dissolution** | Ring winds down; all positions closed at clearing prices; residual loss spread proportionally; Ring ceases to exist | Final option; market disrupted but bounded |

VMGH is the natural default and the only one most Rings will need. Tear-up and forced allocation are TradFi recovery tools for clearinghouses; whether to include them in a Ring's accord depends on customer base and product complexity. Dissolution is a backstop that triggers only when even recovery tools can't restore solvency.

The Ring's recovery-tool spec is read by the risk-treatment equation: Rings with weak recovery tools (VMGH only, no tear-up) get higher CRR on their units; Rings with full recovery-tool stacks (VMGH + tear-up + forced allocation, with stable dissolution criteria) get lower CRR.

---

## Regulation via Risk Treatment

Core Council does not directly approve Rings or set Ring-level rules. Regulation operates **upstream**, at the Prime risk-framework form for Ring-issued positions.

When a Prime holds a Ring-issued derivative (perp position, options, etc.) in its hedgebook, the risk treatment is determined by the form in `&core.framework.risk.forms`. The risk form reads Ring characteristics from Oracle-Entity-attested atoms:

- **Coverage ratio:** assurance fund / gross open interest under stress
- **Pylon membership:** count, capital concentration (HHI), individual ER distributions
- **Attestation cadence and quality** for aggregate Ring health
- **Recovery-tool spec:** which tools are configured, at what triggers
- **Historical performance:** prior stress events, mutualization frequency, recovery-tool activations

→ produces CRR for Primes holding the Ring's units.

A Ring with weak fundamentals (insufficient pre-funding, concentrated Pylon membership, sparse attestation, weak recovery tools, history of stress events) gets a high CRR. Primes need more TRC to hold its units. Demand for those units drops. The Ring's flow shrinks. Either the Ring reforms (improves coverage, attracts more Pylons, strengthens recovery tools) or it dies.

This is **macroprudential regulation via risk-form tuning**:

- **Continuous, not binary.** Core Council dials risk weight gradually; bad Rings get progressively starved rather than abruptly closed.
- **No approval bottleneck.** New Rings spin up at product cadence; their economics are determined by characteristics, not by an approval workflow.
- **Market discipline.** Pylons in a Ring want low CRR on the Ring's units (so Primes hold them), so they self-regulate to meet risk-form criteria.
- **Composable.** Per-Ring, not per-Pylon. The risk model doesn't need to track Pylon-level interactions across Rings; just Ring-level attestation atoms.

The analogy is Basel risk-weights: regulators don't tell banks what to hold; they price different exposures at different capital costs and let market mechanics drive allocation. Here Core Council prices Ring units at different CRRs and lets Prime allocation discipline drive Ring evolution.

---

## Capital Model — Formal Summary

Per-Pylon variables tracked in `&entity.pylon.{id}.primebook` (or equivalent):

- **TRC** (Total Risk Capital) — sized to the Pylon's gross customer risk margin across all Ring memberships, plus extra capital
- **TRRC** (Total Required Risk Capital) — derived from open positions, mark-to-market exposure, sum of per-Ring pledge requirements
- **ER** (Encumbrance Ratio) — TRRC / TRC, target ≤ 0.90 (same constraint as Primes)
- **Per-Ring pledges** — itemized per Ring membership; sum constrained by TRC availability after extra-capital allocation
- **Extra capital** — voluntary, tracked separately for staking-reward signaling and customer-facing capital strength

Standard 5% Entity Creation Fee + 50 bps/yr Entity Upkeep applies on Pylon governance tokens — see [`../accounting/entity-fees.md`](../accounting/entity-fees.md). Cross-Entity Upkeep Rebate available for Pylons holding other Synomic Entity tokens.

---

## Beacon Classes

TBD. Likely includes:

- `pylon-{entity}` — relay (high-authority action) beacon for Pylon operations (position open / close / transfer, customer-facing operations, Ring-pledge management)
- `pylon-monitor-{entity}` — low-authority observation for risk monitoring (synserv in-space rule plus archive beacon, or a passive relay where on-chain action is needed)
- Operating setup at later phases: `baseline-{pylon}` relay + `warden-{pylon}-{operator}` relay + `stream-{pylon}-{actor}` stream-sentinel, deployed together for real-time risk management. Sentinel/relay configs live in `&entity.pylon.{id}.relay.baseline`, `&entity.pylon.{id}.relay.warden.{operator}`, and `&entity.pylon.{id}.sentinel.{actor}`.

---

## Lifecycle

Created via Guardian Accord under SpellCore. The 5% creation fee is paid by issuing 5% of the Pylon's governance tokens to Sky Core; the remaining 95% goes to the creator. Standard 50 bps/yr upkeep applies on the Pylon's governance-token market cap.

The Pylon operates within encoded mandates: products it can clear (which Ring memberships are permitted), per-Ring pledge limits, leverage caps, ER constraints.

Customer onboarding is a Pylon-level operation. Customers (Primes, Folios, occasionally other entities) sign bilateral terms with the Pylon governing margin, recourse, fees, and operational SLAs. These bilateral arrangements have a natural synomic encoding as **ecosystem accords** between specific Pylons and specific customers — pre-negotiated term sheets recognized in the Pylon's entart, attested into the synome, evaluated like any other commitment.

See [`creation-restructuring.md`](creation-restructuring.md).

---

## Open Questions

- **Per-Pylon floor and Cover-N targets.** Specific calibration: what's the 8%-of-risk-margin analog for Sky's risk model? Cover-2 default, with Cover-3 for systemic Rings?
- **Pledge-rebalancing friction parameters.** Exact lockup duration for pledge decreases and full Ring exits. CME's 5-business-day analog under daily settlement; what's right under Sky's faster cadence?
- **Customer abstraction.** Are Pylon customers represented as on-synome accounts, or off-synome (Pylon holds aggregate positions on behalf of off-synome users)? Hybrid?
- **Cross-margin product spec.** Standardized template for Pylon-offered cross-Ring margin offset products? Or fully bilateral / unregulated at the customer relationship layer?
- **Liquidation mechanics.** What's the synomic equivalent of CME's "Cessation of Trading" + "Auction Liquidation" sequence within a Ring?
- **Default-cascade response.** If defaults cascade faster than Pylons can adjust pledges, do Rings have a "circuit breaker" mechanism beyond recovery tools?
- **Operating setup.** Are Pylons operated by a full operating setup (baseline-relay + warden-relay + stream-sentinel for continuous real-time risk management), deterministic relays only, or hybrid? Probably full setup at scale, but Phase 1 may use plain relays only.
- **Sky-backstop sanctioning criteria.** Specific governance process by which a Ring becomes "systemically significant" and eligible for Sky ABC backstop. Default: no backstop.
- **Recovery-tool calibration.** Concrete VMGH cap, tear-up parameters, dissolution thresholds — all Ring-level governance decisions but worth a default template.
- **Attestation cadence floor.** Minimum frequency of Oracle-Entity attestation for Ring health before the risk-treatment equation imposes default-deny.

---

## Relationship to Other Entity Types

| Comparison | Pylon Entity | Other |
|---|---|---|
| vs **Prime** | Takes principal positions in derivatives; faces customers; bears risk capital | Allocates capital across deal-driven Halos; doesn't run a customer-facing derivatives book |
| vs **Sequencer Entity** | Bears risk capital; takes positions | No collateral; matches orders; hosts Rings as accord patterns in its entart |
| vs **Trading Halo (AMM)** | Customer-facing broker-dealer for derivatives; bilateral relationships | AMM venue; oracle-priced; not a counterparty in the broker-dealer sense |
| vs **Oracle Entity** | Tokenized; bears principal risk | Tokenless; provides data; bears no principal risk |
| vs **Generator** | Operational allocator; risk-capital-bearing; multiple | Foundational credit creator; balance-sheet; singular |

---

## Related

- [`../macrosynomics/synomic-entities.md`](../macrosynomics/synomic-entities.md) — Synomic Entity theory
- [`sequencer-entity.md`](sequencer-entity.md) — Matching venue Pylons route to; host of Ring sub-structures
- [`oracle-entity.md`](oracle-entity.md) — Price / liquidity / attestation feeds Pylons and Rings depend on
- [`prime.md`](prime.md) — Counterparties to Pylons for derivatives positions
- [`folio.md`](folio.md) — Counterparties to Pylons for principal-controlled deployments
- [`../macrosynomics/beacon-framework.md`](../macrosynomics/beacon-framework.md) — Beacon taxonomy
- [`creation-restructuring.md`](creation-restructuring.md) — Entity creation mechanism
- [`../accounting/entity-fees.md`](../accounting/entity-fees.md) — Fee model
- [`../risk-framework/capital-formula.md`](../risk-framework/capital-formula.md) — Risk-treatment risk forms for Ring-issued units
