# Laniakea Programme Overview

**Created:** 2026-02-01
**Purpose:** Summary of Laniakea scope, organisational structure, and skills requirements

---

## Part 1: Laniakea Summary Mind Map

```mermaid
mindmap
  root((Laniakea))
    Vision
      Automated capital deployment at scale
      Basel III-inspired risk management
      99% autonomous operation
      Weekly settlement cycles

    Capital Flow Architecture
      Generator Layer
        ERC20 stablecoin interface
        Deploys to Primes via ERC4626
      Prime Layer
        5 Star Primes: Spark, Grove, Keel, Star4, Star5
        1 Institutional Prime: Obex
        Own treasury and governance token
        First-loss capital providers
      Halo Layer
        Passthrough Halos: LCTS, pooled, fungible
        Structuring Halos: NFAT, bespoke, non-fungible
        Halo Classes share PAU + legal buybox
        Halo Units are individual products
      Foreign Layer
        Altchain deployments via bridges
        Foreign Primes and Foreign Halos

    Smart Contract Architecture
      PAU Pattern: Universal building block
        Controller: Rate limits and authorization
        ALMProxy: Custody and execution
        RateLimits: Linear replenishment
      Diamond PAU: EIP-2535 modular upgrade
      LCTS: Queue-based capacity distribution
      NFAT: Non-fungible allocation tokens
      Laniakea Factory: Standardized deployment

    Beacon Framework
      LPLA: Low Power Low Authority
        Reporting, data exchange
        lpla-checker: Position verification
      LPHA: Low Power High Authority
        Deterministic rule execution
        lpha-lcts: Passthrough Halo ops
        lpha-nfat: Structuring Halo ops
        lpha-auction: OSRC matching
      HPLA: High Power Low Authority
        Private trading, arbitrage
      HPHA: High Power High Authority
        Sentinel formations

    Sentinel Network
      stl-base: Baseline execution
        Public code, holds pBEAMs
        Executes Base Strategy
      stl-stream: Intelligence streaming
        Proprietary alpha generation
        Earns carry on outperformance
      stl-warden: Safety oversight
        Independent operators
        Halt authority
        Determines Time to Shutdown

    Risk Framework
      Capital Requirement Formula
        Drawdown Magnitude x Forced Realization Probability
      Duration Model
        SPTP buckets: Stressed Pull-to-Par
        Liability duration from USDS lot ages
      Two-Tier Capital
        JRC: Junior Risk Capital, first loss
        SRC: Senior Risk Capital, protected
      Encumbrance Monitoring
        Target ratio 90% or below
        Escalating penalties for breach

    Governance Architecture
      Atlas: Human-readable constitution
        Spirit and principles
        ~10-20 pages target
      Synome: Machine-readable database
        All operational parameters
        Agent Artifacts
        Transaction logs
      BEAM Hierarchy
        aBEAM: Admin, 14-day timelock
        cBEAM: Configurator, GovOps
        pBEAM: Protocol, Sentinels

    Token System
      USDS: Stablecoin, 1:1 USD peg
      sUSDS: Savings token, ERC-4626
      SKY: Governance token
      srUSDS: Senior Risk Capital token
      TEJRC: Tokenized External JRC
      TISRC: Tokenized Isolated SRC

    Phase 1 Deliverables
      Diamond PAU Deployment
      Synome-MVP
      MVP Beacons
        lpla-checker
        lpha-relay
        lpha-nfat
      Core Halos: Legacy asset wrapper
      Configurator Unit: Spell-less ops
      NFAT Smart Contracts
      Structuring Halo Legal Framework
      SOFR Hedging Requirements
```

---

## Part 2: Phase 1 Delivery Organisation

Phase 1 focuses on pragmatic delivery of minimal viable infrastructure for automated capital deployment, operating on a monthly settlement cycle.

### Phase 1 Organisational Structure

```mermaid
flowchart TB
    subgraph Leadership["Programme Leadership"]
        PD[Programme Director]
        TA[Technical Architect]
        PO[Product Owner]
    end

    subgraph Engineering["Engineering Teams"]
        subgraph SmartContracts["Smart Contracts Team"]
            SCL[SC Lead]
            SC1[Diamond PAU Engineer]
            SC2[NFAT Engineer]
            SC3[Configurator Engineer]
        end

        subgraph Beacons["Beacon Development Team"]
            BL[Beacon Lead]
            B1[lpla-checker Developer]
            B2[lpha-relay Developer]
            B3[lpha-nfat Developer]
        end

        subgraph Infrastructure["Infrastructure Team"]
            IL[Infra Lead]
            I1[Synome-MVP Engineer]
            I2[DevOps Engineer]
        end
    end

    subgraph RiskOps["Risk & Operations"]
        RFL[Risk Framework Lead]
        RF1[Risk Analyst]
        OL[Operations Lead]
        O1[GovOps Specialist]
    end

    subgraph Legal["Legal & Compliance"]
        LL[Legal Lead]
        L1[Structuring Lawyer]
        L2[Buybox Specialist]
    end

    subgraph QA["Quality Assurance"]
        QAL[QA Lead]
        QA1[Smart Contract Auditor]
        QA2[Integration Tester]
    end

    PD --> TA
    PD --> PO
    TA --> SCL
    TA --> BL
    TA --> IL
    PO --> RFL
    PO --> OL
    PD --> LL
    TA --> QAL

    SCL --> SC1
    SCL --> SC2
    SCL --> SC3
    BL --> B1
    BL --> B2
    BL --> B3
    IL --> I1
    IL --> I2
    RFL --> RF1
    OL --> O1
    LL --> L1
    LL --> L2
    QAL --> QA1
    QAL --> QA2
```

### Phase 1 Skills Matrix

| Role | Core Skills Required | Secondary Skills |
|------|---------------------|------------------|
| **Programme Director** | Programme management, stakeholder management, DeFi/TradFi domain knowledge | Risk management, governance |
| **Technical Architect** | Solidity, EVM architecture, system design, distributed systems | Security, formal verification |
| **Product Owner** | Product management, requirements gathering, DeFi protocols | Risk frameworks, tokenomics |
| **SC Lead** | Solidity expert, EIP-2535 (Diamond), ERC-4626, ERC-721 | Gas optimization, upgradability patterns |
| **Diamond PAU Engineer** | Solidity, Diamond proxy pattern, access control | Testing frameworks (Foundry) |
| **NFAT Engineer** | Solidity, ERC-721, queue mechanics | ERC-4626 vault patterns |
| **Configurator Engineer** | Solidity, timelocks, rate limiting | BEAM hierarchy, governance integration |
| **Beacon Lead** | Python/Go, event-driven architecture, blockchain integration | AI/ML foundations |
| **lpla-checker Developer** | Python/Go, risk calculations, data pipelines | Oracle integration |
| **lpha-relay Developer** | Python/Go, transaction management, rate limiting | MEV protection |
| **lpha-nfat Developer** | Python/Go, NFAT lifecycle, queue management | Smart contract interaction |
| **Infra Lead** | Database design, API architecture, cloud infrastructure | Graph databases, on-chain indexing |
| **Synome-MVP Engineer** | Database engineering, data modelling, signed statements | Cryptographic signatures |
| **DevOps Engineer** | Kubernetes, monitoring, CI/CD, blockchain nodes | Security, disaster recovery |
| **Risk Framework Lead** | Quantitative risk, Basel III/FRTB, capital requirements | DeFi risk, credit risk |
| **Risk Analyst** | Financial modelling, stress testing, scenario analysis | Duration analysis, correlation |
| **Operations Lead** | Operational processes, settlement cycles, incident response | Governance, compliance |
| **GovOps Specialist** | Governance operations, BEAM management, spell execution | Multisig coordination |
| **Legal Lead** | Structured finance, securities law, DeFi legal | Bankruptcy remoteness, SPV structures |
| **Structuring Lawyer** | Deal structuring, buybox design, counterparty agreements | Cross-jurisdiction compliance |
| **Buybox Specialist** | Parameter design, recourse mechanisms, legal templates | Regulatory frameworks |
| **QA Lead** | Test strategy, security testing, audit coordination | Smart contract testing |
| **SC Auditor** | Security auditing, formal verification, vulnerability analysis | Solidity, attack vectors |
| **Integration Tester** | End-to-end testing, beacon testing, settlement validation | Automation frameworks |

### Phase 1 Team Size Summary

| Function | Headcount |
|----------|-----------|
| Leadership | 3 |
| Smart Contracts | 4 |
| Beacon Development | 4 |
| Infrastructure | 3 |
| Risk & Operations | 4 |
| Legal & Compliance | 3 |
| Quality Assurance | 3 |
| **Total** | **24** |

---

## Part 3: Full Programme Organisation

The full programme includes Phase 1 plus subsequent phases with weekly settlement, AI-powered sentinels, multi-chain expansion, and full automation.

### Full Programme Organisational Structure

```mermaid
flowchart TB
    subgraph Executive["Executive Leadership"]
        CEO[Chief Executive]
        CTO[Chief Technology Officer]
        CRO[Chief Risk Officer]
        CLO[Chief Legal Officer]
    end

    subgraph ProgrammeMgmt["Programme Management Office"]
        PMO[PMO Director]
        PM1[Phase Lead - Infrastructure]
        PM2[Phase Lead - Automation]
        PM3[Phase Lead - Expansion]
    end

    subgraph Engineering["Engineering Division"]
        direction TB

        subgraph CoreSC["Core Smart Contracts"]
            CSCL[Director of SC Engineering]
            subgraph SCTeams["SC Teams"]
                SCT1[PAU Team]
                SCT2[Token Standards Team]
                SCT3[Factory Team]
            end
        end

        subgraph Automation["Automation & AI"]
            AAL[Director of Automation]
            subgraph AutoTeams["Automation Teams"]
                AT1[Sentinel Team]
                AT2[Beacon Team]
                AT3[ML/AI Team]
            end
        end

        subgraph Platform["Platform Engineering"]
            PEL[Director of Platform]
            subgraph PlatTeams["Platform Teams"]
                PT1[Synome Team]
                PT2[Observability Team]
                PT3[Infrastructure Team]
            end
        end

        subgraph MultiChain["Multi-Chain Engineering"]
            MCL[Director of Multi-Chain]
            subgraph MCTeams["MC Teams"]
                MCT1[Bridge Team]
                MCT2[Foreign Deploy Team]
                MCT3[Chain Integration Team]
            end
        end
    end

    subgraph Risk["Risk Division"]
        RD[Risk Director]
        subgraph RiskTeams["Risk Teams"]
            RT1[Capital Requirements Team]
            RT2[Market Risk Team]
            RT3[Credit Risk Team]
            RT4[Operational Risk Team]
        end
    end

    subgraph Operations["Operations Division"]
        OD[Operations Director]
        subgraph OpsTeams["Operations Teams"]
            OT1[GovOps Team]
            OT2[Settlement Team]
            OT3[Incident Response Team]
            OT4[Prime Operations Team]
        end
    end

    subgraph Legal["Legal & Compliance Division"]
        LD[Legal Director]
        subgraph LegalTeams["Legal Teams"]
            LT1[Structuring Team]
            LT2[Regulatory Team]
            LT3[Governance Legal Team]
        end
    end

    subgraph Security["Security Division"]
        SD[Security Director]
        subgraph SecTeams["Security Teams"]
            ST1[Smart Contract Security]
            ST2[Infrastructure Security]
            ST3[Audit Coordination]
        end
    end

    subgraph Product["Product Division"]
        PrD[Product Director]
        subgraph ProdTeams["Product Teams"]
            PrT1[Prime Products]
            PrT2[Halo Products]
            PrT3[User Experience]
        end
    end

    CEO --> CTO
    CEO --> CRO
    CEO --> CLO
    CEO --> PMO

    PMO --> PM1
    PMO --> PM2
    PMO --> PM3

    CTO --> CSCL
    CTO --> AAL
    CTO --> PEL
    CTO --> MCL
    CTO --> SD
    CTO --> PrD

    CRO --> RD
    CRO --> OD

    CLO --> LD

    CSCL --> SCT1
    CSCL --> SCT2
    CSCL --> SCT3

    AAL --> AT1
    AAL --> AT2
    AAL --> AT3

    PEL --> PT1
    PEL --> PT2
    PEL --> PT3

    MCL --> MCT1
    MCL --> MCT2
    MCL --> MCT3

    RD --> RT1
    RD --> RT2
    RD --> RT3
    RD --> RT4

    OD --> OT1
    OD --> OT2
    OD --> OT3
    OD --> OT4

    LD --> LT1
    LD --> LT2
    LD --> LT3

    SD --> ST1
    SD --> ST2
    SD --> ST3

    PrD --> PrT1
    PrD --> PrT2
    PrT3
```

### Full Programme Skills Matrix

#### Executive Leadership

| Role | Core Skills | Domain Expertise |
|------|-------------|------------------|
| Chief Executive | Strategic leadership, capital markets, regulatory relationships | DeFi, TradFi, governance |
| Chief Technology Officer | System architecture, engineering leadership, technology strategy | Blockchain, distributed systems, AI |
| Chief Risk Officer | Enterprise risk management, regulatory frameworks, quantitative methods | Basel III, FRTB, DeFi risk |
| Chief Legal Officer | Securities law, structured finance, regulatory compliance | Cross-jurisdiction, DAO governance |

#### Engineering Division

| Team | Core Skills | Specialist Skills |
|------|-------------|-------------------|
| **PAU Team** | Solidity, Diamond proxy, ERC-4626 | Upgradability, gas optimization, formal verification |
| **Token Standards Team** | Solidity, ERC-721, LCTS queue mechanics | Tokenomics, capacity distribution |
| **Factory Team** | Solidity, factory patterns, deployment automation | CREATE2, deterministic addresses |
| **Sentinel Team** | Python/Go, real-time systems, ML inference | Trading systems, execution algorithms |
| **Beacon Team** | Python/Go, event-driven architecture | Rate limiting, transaction management |
| **ML/AI Team** | Machine learning, reinforcement learning, NLP | On-chain data, market signals |
| **Synome Team** | Graph databases, data modelling, cryptographic proofs | Distributed state, consensus |
| **Observability Team** | Monitoring, alerting, distributed tracing | Prometheus, Grafana, on-chain indexing |
| **Infrastructure Team** | Kubernetes, cloud architecture, blockchain nodes | High availability, disaster recovery |
| **Bridge Team** | Cross-chain messaging, LayerZero, CCTP | Canonical bridging, security |
| **Foreign Deploy Team** | Multi-chain Solidity, chain-specific quirks | L2s, alt-L1s (Solana, etc.) |
| **Chain Integration Team** | Protocol integration, oracle networks | Price feeds, liquidity protocols |

#### Risk Division

| Team | Core Skills | Specialist Skills |
|------|-------------|-------------------|
| **Capital Requirements Team** | Quantitative modelling, capital formulas | Duration matching, encumbrance |
| **Market Risk Team** | FRTB, VaR, stress testing | Crypto volatility, drawdown modelling |
| **Credit Risk Team** | Credit analysis, default modelling | Jump-to-default, gap risk |
| **Operational Risk Team** | Operational controls, process risk | Sentinel risk, TTS analysis |

#### Operations Division

| Team | Core Skills | Specialist Skills |
|------|-------------|-------------------|
| **GovOps Team** | Governance operations, BEAM management | Spells, timelocks, multisig |
| **Settlement Team** | Settlement processes, reconciliation | Weekly cycle, auction settlement |
| **Incident Response Team** | Incident management, emergency procedures | On-chain triage, warden coordination |
| **Prime Operations Team** | Prime coordination, artifact management | Halo onboarding, Unit deployment |

#### Legal & Compliance Division

| Team | Core Skills | Specialist Skills |
|------|-------------|-------------------|
| **Structuring Team** | Deal structuring, buybox design | NFAT terms, bankruptcy remoteness |
| **Regulatory Team** | Securities regulation, compliance | Multi-jurisdiction, MiCA, US law |
| **Governance Legal Team** | DAO governance, constitutional design | Atlas/Synome, escalation procedures |

#### Security Division

| Team | Core Skills | Specialist Skills |
|------|-------------|-------------------|
| **Smart Contract Security** | Security auditing, formal verification | Attack vectors, invariant testing |
| **Infrastructure Security** | Key management, access control | HSMs, multisig, operational security |
| **Audit Coordination** | External audit management, remediation | Bug bounties, responsible disclosure |

#### Product Division

| Team | Core Skills | Specialist Skills |
|------|-------------|-------------------|
| **Prime Products** | Product management, Prime requirements | Capital deployment, risk capital |
| **Halo Products** | Product management, Halo requirements | Passthrough, Structuring, LCTS/NFAT |
| **User Experience** | UX design, developer experience | SDK, documentation, integrations |

### Full Programme Team Size Summary

| Division | Teams | Approximate Headcount |
|----------|-------|----------------------|
| Executive Leadership | 4 | 4 |
| Programme Management | 4 | 6 |
| Engineering - Core SC | 3 teams | 12 |
| Engineering - Automation | 3 teams | 15 |
| Engineering - Platform | 3 teams | 12 |
| Engineering - Multi-Chain | 3 teams | 10 |
| Risk | 4 teams | 12 |
| Operations | 4 teams | 14 |
| Legal & Compliance | 3 teams | 8 |
| Security | 3 teams | 8 |
| Product | 3 teams | 9 |
| **Total** | | **~110** |

---

## Part 4: Skills Gap Analysis - Phase 1 to Full Programme

### New Capabilities Required for Full Programme

| Capability | Phase 1 | Full Programme | Skills Delta |
|------------|---------|----------------|--------------|
| **AI/ML for Sentinels** | Not required | Critical | ML engineers, RL specialists, trading system experts |
| **Multi-Chain** | Not required | Required | Bridge engineers, alt-chain specialists |
| **Weekly Settlement** | Monthly only | Weekly automation | Higher ops velocity, auction systems |
| **HPHA Sentinels** | LPHA beacons only | Full sentinel formations | Streaming Accord, warden network |
| **Scale** | First cohort | Full ecosystem | Enterprise architecture, platform thinking |

### Critical Hiring Priorities for Expansion

1. **ML/AI Team** - For HPHA sentinel development (stl-stream intelligence)
2. **Bridge Team** - For Foreign layer deployment
3. **Settlement Team** - For weekly cycle automation
4. **Sentinel Team** - For stl-base/stl-warden implementation
5. **Observability Team** - For production monitoring at scale

---

## Part 5: Governance & Reporting Structure

### Phase 1 Governance

```
Sky Core Governance
       │
       ├── Core Council (aBEAM holders)
       │       │
       │       └── GovOps Teams (cBEAM holders)
       │               │
       │               └── Operational Beacons (pBEAM holders)
       │
       └── Fortification Conserver
               │
               └── Emergency Response
```

### Full Programme Governance

```
Sky Core Governance
       │
       ├── Core Council
       │       │
       │       ├── Generator GovOps
       │       ├── Prime GovOps (per Prime)
       │       │       └── Sentinel Formations
       │       │               ├── stl-base
       │       │               ├── stl-stream (Ecosystem Actors)
       │       │               └── stl-warden (Independent Operators)
       │       └── Halo GovOps (per Halo Class)
       │               └── LPHA Beacons
       │                       ├── lpha-lcts
       │                       └── lpha-nfat
       │
       ├── Fortification Conserver
       │       └── Legal recourse, asset recovery
       │
       └── Alignment Conservers
               └── Governance integrity
```

---

*Document generated from Laniakea documentation repository analysis.*
