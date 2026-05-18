# Appendix D: Tokens

Complete reference of all tokens in the Sky ecosystem.

---

## Core Tokens

| Token | Symbol | Type | Description |
|-------|--------|------|-------------|
| **Sky Dollar** | USDS | Stablecoin | Primary unit of account; 1:1 USD peg; ~$9B supply |
| **Savings USDS** | sUSDS | Yield token | Deposit USDS → earn Sky Savings Rate automatically |
| **Sky** | SKY | Governance | Voting rights + profit share via staking/buybacks |
| **Segregated stUSDS** | stUSDS | Risk capital | Segregated capital for SKY-backed borrowing; bears haircut risk |

---

## Legacy Tokens

| Token | Symbol | Type | Description |
|-------|--------|------|-------------|
| **Dai** | DAI | Stablecoin | Original stablecoin; 1:1 convertible with USDS |
| **Maker** | MKR | Governance | Original governance token; 1:24000 convertible with SKY |

---

## Agent Framework Tokens

### Prime Agent Tokens

| Token | Symbol | Agent | Description |
|-------|--------|-------|-------------|
| **Spark** | SPK | Spark | Spark Prime governance token |
| **Grove** | — | Grove | Grove Prime governance token |
| **Keel** | — | Keel | Keel Prime governance token |
| **Obex** | — | Obex | Obex Prime governance token |

*All Prime tokens: 10B genesis supply, emissions permanently disabled*

### Risk Capital Tokens

| Token | Type | Scope | Description |
|-------|------|-------|-------------|
| **srUSDS** (Planned) | Senior Risk | Global | Senior risk capital for all of USDS; LCTS-only |
| **TEJRC** | Junior Risk | Per-Prime | Tokenized external junior risk capital; LCTS-only |
| **TISRC** | Senior Risk | Per-Prime | Tokenized isolated senior risk capital; LCTS-only |
| **TESRC** | Senior Risk | Per-Prime | Tokenized external senior risk capital |

### Queue & Position Tokens

| Token | Type | Description |
|-------|------|-------------|
| **LCTS Shares** | Position | Non-transferable internal accounting for queue positions (Portfolio Halos) |
| **NFAT** | Position | Non-Fungible Allocation Token — transferable claim on individual Term Halo deals |
| **Halo Unit Shares** | Ownership | Pro-rata claim on Halo Unit assets |

### Token Standards

| Standard | Token Type | Characteristics |
|----------|------------|-----------------|
| **LCTS** | Fungible | Liquidity Constrained Token Standard — queue-based entry/exit, pooled positions, uniform terms |
| **NFATS** | Non-fungible | Non-Fungible Allocation Token Standard — individual deals, bespoke terms, transferable |

---

## Future Tokens (Post-Laniakea)

| Token | Type | Description |
|-------|------|-------------|
| **SGAs** | Stablecoin | Sky Generated Assets — new currencies issued by Generators |

---

## Token Mechanics

### USDS
- 1:1 peg to USD
- Minted against collateral or via PSM
- Convertible 1:1 with DAI
- Available on multiple chains via SkyLink

### sUSDS
- ERC-4626 vault token
- Exchange rate increases at Sky Savings Rate
- No lock-up; freely redeemable
- Earns yield on all supported chains

### SKY
- Governance voting power
- Staking rewards (SSTR)
- Collateral for SKY-backed borrowing
- Deflationary via Smart Burn Engine
- 24,000 SKY = 1 MKR (conversion rate)

### stUSDS
- Segregated from main protocol risk
- Higher yield than sUSDS (compensates for haircut risk)
- Dynamic debt ceiling = total stUSDS deposits
- Absorbs losses from SKY liquidation failures

### srUSDS
- LCTS-based subscribe/redeem
- Exchange rate set each settlement
- Increases from yield, decreases from haircuts
- Global senior risk capital for USDS

### NFAT
- ERC-721 representing claim on Term Halo deal
- Each NFAT has individual terms (duration, size, yield) within buybox
- Transferable — can be sold or used as collateral
- Burned on redemption when funds are claimed

### LCTS
- Queue-based entry and exit
- Daily settlement processing (lock 13:00 UTC, settle by 16:00 UTC)
- Pooled positions with uniform terms
- Non-transferable queue positions; shares may be transferable depending on implementation

---

## Token Addresses

See [Appendix G: Deployed Infrastructure](appendix-g-infrastructure.md) for contract addresses.
