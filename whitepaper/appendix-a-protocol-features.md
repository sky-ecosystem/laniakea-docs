# Appendix A: Protocol Features

Exhaustive list of Sky Core mechanisms. Together with Appendix B (Agent Primitives), this provides complete coverage of every mechanism in Sky Ecosystem.

---

## Core Tokens

### SKY

The community governance token for Sky Ecosystem.

| Property | Value |
|----------|-------|
| Total Supply | 23.46 billion SKY |
| Emissions | Permanently disabled (no new minting except emergency recapitalization) |
| Conversion Rate | 24,000 SKY = 1 MKR |
| Upgrade Penalty | Increases 1% per quarter for unclaimed MKR to drive migration |

**Functions:**
- Governance voting power (when staked)
- Staking rewards recipient (SSTR)
- Collateral for SKY-backed borrowing
- Deflationary via Smart Burn Engine buyback/burn

**Supply Dynamics:**
- ~14% of original MKR supply remains unclaimed post-migration
- 1% quarterly burn of SKY backing unclaimed MKR (~24 year burn schedule)
- Continuous buyback/burn from protocol surplus via Smart Burn Engine

---

### USDS

The primary stablecoin of Sky Ecosystem.

| Property | Value |
|----------|-------|
| Peg | 1:1 USD |
| Supply | $9.86 billion (December 2025) |
| Standard | ERC-20 |
| Backing | Overcollateralized by crypto assets, Treasuries, and credit positions |

**Key Characteristics:**
- 1:1 convertible with DAI (upgrade path)
- Can be deposited to receive sUSDS (yield-bearing)
- Freely transferable and composable with DeFi protocols
- Available on Ethereum mainnet + L2s/L1s via SkyLink
- Decentralized yield-generating stablecoin focused on capital formation (not a payment stablecoin)

---

### sUSDS

The savings token representing USDS deposits earning the Sky Savings Rate.

| Property | Value |
|----------|-------|
| Standard | ERC-4626 vault |
| Yield Mechanism | Exchange rate increases continuously at Sky Savings Rate |
| Lock-up | None — freely redeemable at any time |
| Multi-chain | Earns yield on all supported chains via SkyLink |

**How It Works:**
1. User deposits USDS into savings contract
2. User receives sUSDS tokens at current exchange rate
3. Exchange rate increases over time as yield accrues
4. User redeems sUSDS for increased amount of USDS

---

### stUSDS

Segregated junior risk capital token for SKY-backed borrowing.

| Property | Value |
|----------|-------|
| Purpose | Fund SKY-backed borrowing; absorb SKY liquidation losses |
| Yield | Higher than sUSDS (compensates for haircut risk) |
| Risk | Exchange rate can decrease via haircuts if SKY liquidations fail |
| Debt Ceiling | Dynamic — equals total stUSDS deposits |

**Risk Isolation Model:**
- Protocol isolated from SKY collateral losses
- stUSDS holders explicitly accept downside risk
- Losses absorbed by stUSDS before any impact to main protocol
- Higher yield compensates for additional risk

**Dynamic Debt Ceiling:**
```
Max SKY-Backed Debt = Total USDS in stUSDS Contract
```
- No manual ceiling adjustments needed
- Ceiling scales automatically with stUSDS deposits
- Market-driven capacity limits

---

### srUSDS (Planned)

Senior risk capital token providing global backing for all USDS.

| Property | Value |
|----------|-------|
| Purpose | Global senior risk capital for USDS; backs all protocol exposure |
| Standard | LCTS-based (queue settlement) |
| Risk Profile | Lower risk than JRC; absorbs losses only after JRC depleted |
| Settlement | Weekly queue processing (deposit/redemption) |
| Status | **Planned** |

**Mechanics:**
- Users deposit USDS to deposit queue → converts to srUSDS at settlement
- Users add srUSDS to redemption queue → converts back to USDS at settlement
- Queue entries can be withdrawn before settlement lock
- Conversion rate updated at each settlement based on pool performance

---

## SKY Token System

### SKY Staking

Stake SKY to earn staking rewards (SSTR) and participate in governance.

| Property | Value |
|----------|-------|
| Lock-up | None — freely unstakeable at any time |
| Rewards | Sky Staking Rewards (SSTR) |
| Governance | Staked SKY enables voting on governance proposals |
| Collateral | Staked SKY can be used as collateral for borrowing |

**Staking Flow:**
1. User stakes SKY
2. Receives staking rewards (SSTR) from TMF Step 5
3. Can delegate voting power to Aligned Delegates
4. Can use staked SKY as collateral for USDS borrowing

---

### SKY-Backed Borrowing

Use staked SKY as collateral to borrow USDS while continuing to earn staking rewards.

| Property | Value |
|----------|-------|
| Collateral | Staked SKY |
| Borrowed Asset | USDS |
| Borrow Rate | Sky Borrow Rate (governance-set, utilization-based) |
| Liquidation Ratio | 120% |
| Risk Capital Source | stUSDS pool (segregated) |

**Key Benefits:**
- Continue earning staking rewards while borrowing
- Lower effective borrowing cost due to reward offset
- No sacrifice of governance participation
- Market-driven capacity via stUSDS deposits

---

### SKY Voting Delegation

Delegate voting power to Aligned Delegates while retaining token custody.

| Property | Value |
|----------|-------|
| Mechanism | Delegate Contracts |
| Token Custody | Retained by delegator |
| Voting Power | Transferred to Aligned Delegate |
| Revocability | Can change or revoke delegation at any time |

**Aligned Delegates:**
- Anonymous Alignment Conservers receiving delegated voting power
- Ranked by delegated voting power (L1, L2, L3)
- Subject to strict operational security and accountability requirements
- Receive budget allocations tied to voting activity

---

### Smart Burn Engine

Algorithmic SKY buyback using protocol surplus.

| Property | Value |
|----------|-------|
| Source | TMF Step 4 allocation (20% × Net Revenue Ratio) |
| Mechanism | Programmatic open-market buybacks |
| Distribution | Purchased SKY distributed to stakers |
| Governance | Parameters subject to change through decentralized governance |

**Current Behavior (Temporary):**
- Steps 4 and 5 are currently unified
- All funds from both steps used to buyback SKY
- All purchased SKY distributed to stakers as yield

**Planned: Dynamic Burn Rate Formula**
```
Burn Rate = (1 - MC / TMC) × 50%
```
Where:
- MC = Current Market Capitalization
- TMC = 8.5 + (200 × growth_rate) × annual_profits
- Buys more when price is low, retains capital when high

**Since February 2025:**
- $92.2 million in SKY repurchased
- ~6.3% of total supply

---

## Savings & Yield

### Sky Savings Rate (SSR)

Base yield rate for sUSDS holders.

| Property | Value |
|----------|-------|
| Recipient | sUSDS holders |
| Distribution | Automatic via sUSDS exchange rate increase |
| Multi-chain | Same rate on all supported chains via SkyLink |

**Rate Setting:**
- **Current:** Governance process with risk advisor inputs
- **Post-Laniakea:** Algorithmic based on USDS price and ASC balance

See [Monetary Policy](#monetary-policy) for full details.

---

### Staking Rewards (SSTR)

Yield distributed to SKY stakers from TMF Step 5.

| Property | Value |
|----------|-------|
| Source | TMF Step 5 (100% of remainder after Steps 1-4) |
| Recipient | Staked SKY holders |
| Mechanism | SKY buyback distributed to stakers |

**Current Phase (Genesis):**
- Primary destination for protocol surplus
- Majority of net revenue flows to staking rewards
- As revenue scales, more flows to burn and fortification

---

### stUSDS Yield

Higher yield than sUSDS compensating for haircut risk in SKY-backed borrowing.

| Property | Value |
|----------|-------|
| Base | Sky Savings Rate |
| Premium | Utilization-based spread from SKY borrowing |
| Risk | Exchange rate can decrease via haircuts |
| Target Utilization | 90% |

---

### srUSDS Yield (Planned)

Senior risk capital yield with lower risk profile than junior capital.

| Property | Value |
|----------|-------|
| Source | Interest on originated Senior Risk Capital |
| Deductions | Sky Spread + 5% ESRC Earnings Fee |
| Risk | Absorbs losses only after JRC depleted |
| Status | **Planned** |

---

## Risk Capital System

### stUSDS (Junior Risk Capital)

Segregated pool backing SKY-backed borrowing; first-loss position for SKY collateral risk.

| Property | Value |
|----------|-------|
| Position | Junior (first-loss) |
| Scope | SKY-backed borrowing only |
| Yield | Higher than sUSDS |
| Risk | Exchange rate can decrease via haircuts |

---

### srUSDS (Senior Risk Capital) — Planned

Global senior risk capital for all USDS; LCTS-based with queue settlement.

| Property | Value |
|----------|-------|
| Position | Senior (absorbs after JRC depleted) |
| Scope | All USDS exposure globally |
| Settlement | Weekly LCTS queue processing |
| Status | **Planned** |

---

### Loss Absorption Waterfall

Defined sequence for absorbing losses, structured in three tiers.

```
Loss Event
    ↓
┌─── PRIME-LEVEL (per-Prime) ─────────────────────────────────────┐
│  1. First Loss Capital (10%)   │  ← Prime's IJRC absorbs first  │
├────────────────────────────────┤                                │
│  2. Remaining JRC (pro-rata)   │  ← IJRC + EJRC proportionally  │
├────────────────────────────────┤                                │
│  3. Agent Token Inflation      │  ← Dilute Prime token holders  │
├────────────────────────────────┤                                │
│  4. TISRC                      │  ← Prime-isolated SRC          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─── SYSTEM-LEVEL (shared across all Primes) ─────────────────────┐
│  5. Global SRC (srUSDS)        │  ← System-wide senior capital  │
├────────────────────────────────┤                                │
│  6. SKY Token Inflation        │  ← Dilute protocol token       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─── NUCLEAR OPTIONS (protocol reserves / peg) ───────────────────┐
│  7. Genesis Capital Haircut    │  ← Protocol reserves           │
├────────────────────────────────┤                                │
│  8. USDS Peg Adjustment        │  ← Final backstop              │
└─────────────────────────────────────────────────────────────────┘
```

| Step | Capital Layer | Tier | Mechanism |
|------|---------------|------|-----------|
| **1** | First Loss Capital | Prime | First 10% of IJRC absorbed before any other capital |
| **2** | Remaining JRC | Prime | IJRC + EJRC share losses proportionally |
| **3** | Agent Token Inflation | Prime | Dilute Prime token holders (potentially to infinity) |
| **4** | TISRC | Prime | Prime-isolated senior risk capital |
| **5** | Global SRC (srUSDS) | System | Shared senior risk capital pool |
| **6** | SKY Token Inflation | System | Dilute SKY holders at protocol level |
| **7** | Genesis Capital | Nuclear | Protocol reserves haircut |
| **8** | USDS Peg Adjustment | Nuclear | Final backstop — affects all USDS holders |

**First Loss Capital (FLC):**
- First 10% of Total JRC absorbed solely by Prime's own capital (IJRC)
- Ensures Prime has direct skin in the game for initial losses
- Losses beyond FLC allocated pro-rata across remaining JRC (internal + external)

**Token Inflation Layers:**
- Agent Token Inflation (step 3) dilutes the specific Prime's token holders
- SKY Token Inflation (step 6) dilutes protocol-level token holders
- Both can theoretically cover unlimited losses through dilution

**Nuclear Options:**
- Steps 7-8 should never be reached under normal conditions
- Genesis Capital is the protocol's reserve fund
- Peg Adjustment is the absolute last resort, affecting all USDS holders

---

## Governance Infrastructure

### Sky Atlas

Human-readable governance constitution defining principles, structure, and agent type definitions.

| Property | Value |
|----------|-------|
| Purpose | Define WHAT must be true: principles, governance structure, rules |
| Nature | Human-readable, interpretable |
| Modification | Elevated thresholds reflecting constitutional nature |

**Document Hierarchy:**
1. **Immutable Documents**: Scopes, Articles, Sections (locked at Endgame)
2. **Primary Documents**: Core documents, Active Data Controllers, Budget Controllers
3. **Supporting Documents**: Active Data, Budgets, Precedents
4. **Accessory Documents**: Translations, Archives

**Core Principle: Spirit of the Atlas**
- All rules have underlying intent to serve human values and Universal Alignment
- Facilitators interpret Spirit when explicit guidance is absent
- Balance between "letter of the rule" and true purpose

---

### Sky Synome (Planned)

Machine-readable operational database containing all parameters, artifacts, and transaction logs.

| Property | Value |
|----------|-------|
| Purpose | Contain ALL operational data; machine-readable state |
| Contents | Agent Artifacts, rate limits, penalty schedules, transaction logs |
| Relationship | Atlas is single root node within Synome |
| Status | **Planned** |

---

### Governance Polls

SKY holder signaling votes; non-binding.

| Property | Value |
|----------|-------|
| Duration | 3 days |
| Purpose | Gather consensus, signal preferences |
| Binding | No — signaling only |
| Proposers | Facilitators or recognized Ecosystem Actors |

---

### Executive Votes

On-chain parameter changes; binding.

| Property | Value |
|----------|-------|
| Frequency | ~Bi-weekly (30-day expiration) |
| Purpose | Implement binding protocol changes |
| Execution | Requires more SKY support than any other active proposal |

**Process:**
1. Governance Point prepares Executive Sheet and Document
2. Spell Team crafts and reviews smart contract
3. Fork testing on mainnet fork
4. Publication to Voting Portal (vote.sky.money)
5. SKY holders vote; winning proposal executes

---

### Spells

Smart contracts that execute governance decisions on-chain.

| Property | Value |
|----------|-------|
| Purpose | Execute protocol changes approved through Executive Vote |
| Execution | One-time; self-destructs after execution |
| Review | Requires Spell Team review and fork testing |

**Current Behavior:**
Spells perform all types of protocol actions — parameter changes, contract deployments, role assignments, and cross-chain bridge configuration.

**Post-Laniakea Behavior:**
- Spells primarily trigger Prime Spells or configure cross-chain bridges
- Direct protocol modifications become rare as Laniakea factory standardizes operations
- See Appendix B for Agent Spells (Prime Spells, Halo Spells)

---

### Aligned Delegate System

Ranked delegates (L1-L3) with compensation tied to governance activity.

| Property | Value |
|----------|-------|
| Ranking | Based on delegated voting power |
| Compensation | Budget allocations modified by activity metrics |
| Accountability | Subject to derecognition for misalignment |

**Misalignment Handling:**
- First mild breach: Warning, no substantial penalty
- Second breach or severe first breach: Immediate derecognition
- Derecognition permanently removes individual from AC role

---

### Facilitator Framework

Interpret Atlas on behalf of Executor Agents.

| Property | Value |
|----------|-------|
| Role | Interpret Atlas and Artifacts for Executors |
| Discretion | Broad discretionary authority when explicit guidance absent |
| Precedents | All interpretations documented as Facilitator Action Precedents |

---

### Atlas Edit Cycle

Process for modifying Atlas documents through governance.

| Property | Value |
|----------|-------|
| Trigger | Ranked Delegate with sufficient AD Buffer |
| Protection | Triggering Threshold stake required (lost if rejected) |
| Vote Type | Governance Poll only (no Executive Vote) |

---

## Revenue & Treasury

### Treasury Management Function (TMF)

5-step sequential waterfall distributing all protocol net revenue.

| Step                              | Allocation                              | Purpose                                        |
| --------------------------------- | --------------------------------------- | ---------------------------------------------- |
| **1. Security & Maintenance**     | 21% (Genesis) / 4-10% (Post-Genesis)    | Core teams, security, risk management          |
| **2. Aggregate Backstop Capital** | Variable (target: 1.5% of total supply) | Solvency buffer for bad debt protection        |
| **3. Fortification Conserver**    | 20% × Net Revenue Ratio                 | Legal defense, resilience, unquantifiable risk |
| **4. Smart Burn Engine**          | 20% × Net Revenue Ratio                 | SKY buybacks                                   |
| **5. Staking Rewards**            | 100% of remainder                       | Distributed to SKY stakers                     |

**Key Property:** Each step calculates allocation based on what remains after previous step (sequential waterfall).

**Temporary Behavior:** Steps 4 and 5 are currently unified — all funds from both steps are used to buyback SKY and distribute to stakers.

---

### Aggregate Backstop Capital

Solvency buffer for bad debt protection.

| Property | Value |
|----------|-------|
| Target | 1.5% of total supply (USDS liabilities) |
| Fill Rate | Dynamic based on buffer status |
| Maximum Allocation | 50% of available funds when empty |
| Skip Condition | 0% allocation when buffer is full |

**Phases:**
- **Phase 1 (Safety Floor):** Buffer < 125M → MIN(25%, calculated rate) floor
- **Phase 2 (Filling):** 125M ≤ Buffer < Target → Calculated rate
- **Phase 3 (Full):** Buffer ≥ Target → 0% allocation

---

### Fortification Conserver

Alignment Conserver for legal defense and unquantifiable risk.

| Property | Value |
|----------|-------|
| Allocation | 20% × Net Revenue Ratio of Step 2 Result |
| Purpose | Legal defense, resilience, unquantifiable risk management |
| Scaling | Grows with net revenue (larger scale requires greater legal infrastructure) |
| Current Entity | Fortification Foundation |

---

### Staking Rewards Distribution

100% of TMF remainder after Steps 1-4; primary destination during Genesis Phase.

| Property | Value |
|----------|-------|
| Allocation | 100% of Step 4 Result |
| Recipient | SKY stakers |
| Mechanism | SKY buyback distributed to stakers |

---

## Monetary Policy

### Sky Savings Rate (SSR)

Base yield rate for sUSDS holders.

| Property | Value |
|----------|-------|
| Distribution | Via sUSDS exchange rate increase |
| Multi-chain | Same rate on all supported chains |

**Current Behavior:**
SSR is set through governance process with inputs from risk advisors. Rate adjustments consider market conditions, protocol revenue, and competitive positioning.

**Post-Laniakea Behavior:**
SSR will be algorithmically determined based on:
- **USDS Price** — Rate adjusts to maintain peg stability
- **Actively Stabilizing Collateral (ASC)** — Available ALM liquidity supporting the peg (see `## Peg Stability`)

This removes governance overhead and enables real-time rate optimization.

---

### Base Rate

Protocol-wide stability fee applied to all borrowing.

| Property | Value |
|----------|-------|
| Application | All capital deployed through Allocation System |
| Collection | Monthly Settlement Cycle |
| Revenue | Flows to Net Revenue → TMF |

---

### Sky Borrow Rate

Rate for borrowing USDS against SKY collateral.

| Property | Value |
|----------|-------|
| Collateral | Staked SKY |
| Rate Structure | Base + utilization-based slopes |
| Target Utilization | 90% |

**Formula:**
```
SKY Borrow Rate = SKY Borrow Base Rate
                + Slope1 × min(Utilization, Target Utilization)
                + Slope2 × max(0, Utilization - Target Utilization)
```

---

## Peg Stability

### LitePSM

USDC ↔ USDS 1:1 conversion; primary peg stability mechanism.

| Property | Value |
|----------|-------|
| Conversion | 1:1 USDC to USDS and vice versa |
| Purpose | Enable arbitrageurs to maintain peg |
| Effect | Creates tight band around the dollar |
| Availability | Mainnet + supported chains |

---

### Actively Stabilizing Collateral (ASC) and Demand Absorption Buffer (DAB)

ASC and DAB are the Asset Liability Management (ALM) liquidity layers that keep USDS close to $1 through market-making:

- **ASC**: highly liquid, non‑USDS assets that can be used to buy USDS during downward peg pressure (buy support).
- **DAB**: highly liquid USDS (or USDS-equivalent) positions that can be used to sell USDS during upward peg pressure (sell support).

| Layer | Holds | Peg pressure addressed | Example forms |
|------|-------|-------------------------|--------------|
| **ASC** | Non‑USDS, USD‑adjacent liquidity | USDS < $1 | USDC in LitePSM/PSMs; stablecoin liquidity provision paired with USDS |
| **DAB** | USDS (or USDS-equivalent) liquidity | USDS > $1 | USDS/DAI positioned to provide sell-side liquidity |

**Resting vs. latent ASC**
- **Resting ASC** provides immediate buy support near the peg (e.g., USDC in LitePSM/PSMs; stablecoin liquidity paired with USDS).
- **Latent ASC** can be converted into resting ASC on short notice (targeted within ~15 minutes); latent ASC is capped (e.g., max 25% of total ASC).

**Minimum requirements (parameterized)**
- **Minimum ASC**: defined as a percentage of the total Sky Collateral Portfolio (e.g., 5% in current implementations).
- **Minimum DAB**: defined relative to ASC (e.g., DAB sized at 25% of the required ASC), with an allowed upside spread (e.g., selling up to 1.001 USD per USDS).

**Peg defense event**
- **Trigger**: the average USDS price on designated DEX venues falls below a downside threshold (e.g., 0.999).
- **Obligation**: purchase USDS at a rate defined as a fraction of the ASC requirement on a fixed cadence (e.g., 6.25% of the ASC requirement every 6 hours) until the event clears.

Prime Agents are required to maintain ASC and DAB proportional to the capital they deploy from the Sky Collateral Portfolio, and the system can support rentals that transfer ASC/DAB obligations together between Primes.

More detail: `risk-framework/asc.md`.

---

## Multi-Chain

### SkyLink

Native token bridging to L2s and major L1s.

| Property | Value |
|----------|-------|
| Purpose | Cross-chain token transfers and functionality |
| Tokens | USDS, sUSDS, SKY |
| Chains | Ethereum, Base, Arbitrum, Optimism, Unichain, Avalanche, Solana (via Keel) |

**Capabilities:**
- Native token transfers
- Native savings rates (sUSDS earning SSR)
- Native token rewards distribution
- Native 1:1 USDC ↔ USDS conversion

---

### Native Savings Rates

sUSDS earning SSR on all supported chains.

| Property | Value |
|----------|-------|
| Rate | Same SSR as Ethereum mainnet |
| Mechanism | SkyLink synchronization |

---

### Cross-Chain USDC Conversion

1:1 USDC ↔ USDS on all supported chains.

| Property | Value |
|----------|-------|
| Rate | 1:1 |
| Mechanism | Per-chain PSM deployments |
| Availability | All SkyLink-connected chains |

---

## Settlement & Operations

### Monthly Settlement Cycle

Current settlement cadence for risk capital and distributions.

| Property | Value |
|----------|-------|
| Timing | End of each calendar month |
| Status | Active |

**What Gets Settled:**
1. Net Revenue Calculation → TMF waterfall
2. Senior Risk Capital Origination → clearing price, costs, OSRC credited
3. srUSDS Conversions → queued deposits/redemptions processed
4. Smart Burn Operation → burn rate calculated and executed
5. GovOps Functions → payments, compliance, penalties

---

### Weekly Settlement Cycle (Planned)

Post-Laniakea: Tue lock → Wed settle; faster capital reallocation.

| Period | Timing | Purpose |
|--------|--------|---------|
| Measurement | Tuesday noon → Tuesday noon | Data collection, bid submission |
| Processing | Tuesday noon → Wednesday noon | Calculation, verification |
| Settlement | Wednesday noon | All changes take effect |

**Status:** Draft

---

### OSRC Auction (Planned)

Sealed-bid auction for Senior Risk Capital capacity allocation.

| Property | Value |
|----------|-------|
| Timing | Weekly at settlement |
| Mechanism | Sealed-bid, uniform-price |
| Duration | OSRC valid for one week; no rollover |
| Status | **Planned** |

---

### Duration Bucket Auction (Planned)

Capacity reservations for duration-matched asset deployment.

| Property | Value |
|----------|-------|
| Purpose | Reserve capacity in Duration Buckets for long-duration assets |
| Benefit | Lower capital requirements when assets match liability duration |
| Status | **Planned** |

---

## Compliance

### Geographic Filtering

IP-based blocking/hiding for restricted jurisdictions.

| Type | Description |
|------|-------------|
| **Limited Filtering** | Hide yield features in certain jurisdictions |
| **Full Block** | Complete access restriction (Cuba, Iran, Syria, North Korea, etc.) |

---

## Legacy Systems

### DAI

Original stablecoin; 1:1 convertible with USDS.

| Property | Value |
|----------|-------|
| Conversion | 1:1 with USDS |
| Status | Legacy (still active) |
| History | Launched 2017; first decentralized stablecoin at scale |

---

### MKR

Original governance token; 1:24,000 convertible with SKY.

| Property | Value |
|----------|-------|
| Conversion | 1:24,000 with SKY |
| Unclaimed | ~14% of original supply |
| Upgrade Penalty | 1% per quarter (drives migration) |
| Status | Legacy (still active) |

---

### DSR

DAI Savings Rate; predecessor to SSR.

| Property | Value |
|----------|-------|
| Successor | Sky Savings Rate (SSR) |
| Status | Legacy (still active for DAI holders) |

---

### Legacy Vaults

Original collateralized debt positions.

| Property | Value |
|----------|-------|
| Function | Deposit collateral → mint DAI |
| Successor | Allocation System via Sky Agents |
| Status | Legacy (still active) |

---

### PSM (Legacy)

Original peg stability modules.

| Property | Value |
|----------|-------|
| Successor | LitePSM |
| Status | Legacy |

---

*This appendix should be updated as new features are deployed or deprecated.*
