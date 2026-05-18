# Term Halo Legal Infrastructure + SOFR Hedging — Phase 1

**Status:** Draft
**Last Updated:** 2026-02-24

---

## Overview

The legal infrastructure for Term Halos must be established before NFAT Facilities can operate (Phase 1.5+). This framework enables lpha-nfat to execute deals autonomously within governance-approved bounds.

This document also covers SOFR hedging requirements, which are a legal/structuring prerequisite for Primes deploying into duration NFATs.

---

## Design Principles

Inspired by Portfolio Halos, the Term Halo legal structure follows three principles:

| Principle | Application to Term Halos |
|---|---|
| **Default Ownership to Sky** | Fortification Conserver can assume control of NFAT Facility assets if legal intervention is needed |
| **Standardized Structures** | Buybox templates enable rapid deal execution without per-deal legal negotiation |
| **Pre-signed Integration** | Primes and counterparties pre-sign agreements covering the full buybox parameter range |

---

## The Buybox Model

Each NFAT Facility defines a **buybox** — the acceptable parameter ranges for deals within that facility:

| Parameter | Example Range |
|---|---|
| **Duration** | 6-24 months |
| **Size** | 5M-100M per NFAT |
| **APY** | 8-15% |
| **Counterparties** | Approved Primes only |
| **Asset Types** | Senior secured loans, investment-grade bonds |

**Key rule:** Deals within the buybox can be executed by lpha-nfat without additional governance approval. Deals outside the buybox require governance intervention.

The buybox is defined in the Halo Artifact and approved through governance. Changing the buybox requires an Artifact Edit.

### Terms Source

NFAT terms can come from two sources:

| Mode | Description |
|---|---|
| **General buybox** | Halo Class defines acceptable ranges; individual units fall within the buybox without predetermined terms. Halo has flexibility in structuring. |
| **Ecosystem accord** | Pre-negotiated agreement specifying individual unit and book terms. Overrides the general buybox. More constrained, more predictable for the Prime. |

---

## Legal Isolation

Bankruptcy remoteness is at the **Halo Book** level — the balanced ledger boundary:

- If one NFAT's underlying deal fails, other NFATs on different books in the facility are protected
- Each Halo Book functions as a serialized LLC equivalent (BVI SPC segregated portfolio)
- Recourse is limited to the specific book's assets
- Units sharing a book are **pari passu** on losses (pro rata by principal)
- Units on different books are **fully isolated**

| Halo Concept | BVI SPC Equivalent | Delaware Equivalent |
|---|---|---|
| **Halo Class** | The SPC entity itself | The Series LLC parent |
| **Halo Book** | Segregated portfolio (statutory ring-fencing under BVI BCA s.146) | Individual series (untested in bankruptcy) |
| **Halo Unit** | Share/interest within a portfolio | Membership interest in a series |

BVI SPCs provide materially stronger book-level isolation than Delaware Series LLCs — the BVI statutory segregation has been court-tested.

---

## Governance Artifacts

| Artifact | Contents |
|---|---|
| **Halo Artifact** | Overall governance, buybox definitions, recourse mechanisms, migration procedures |
| **Unit Artifact** | Per-NFAT operational parameters, legal recourse documentation, deal terms |

These artifacts provide complete transparency and serve as operational playbooks for all parties. They are the governance record of what the Halo is allowed to do and what happens when things go wrong.

---

## Deliverables

1. **Buybox Template** — Reusable legal framework defining acceptable deal parameters for each Halo Class
2. **Pre-signed Agreements** — Standard agreements Primes sign to participate in NFAT Facilities (covering the full buybox parameter range)
3. **Recourse Mechanisms** — Procedures for Fortification Conserver intervention on default
4. **Artifact Templates** — Governance documentation templates for Halo and Unit Artifacts

---

## SOFR Hedging

### Why This Matters

Primes deploying into NFATs with duration must manage interest rate risk. Fixed-rate NFATs create interest rate exposure: if SOFR rises, the Prime holds a below-market position.

When using the ALDM (Asset-Liability Duration Matching) system for duration matching, Primes have two options:

| Option | Description |
|---|---|
| **Fully Hedged** | Maintain a hedged interest rate position that provides variable yield based on SOFR movements (swaps, futures) |
| **SOFR Plus Terms** | Structure NFAT positions with SOFR plus spread pricing (floating rate) |

The duration matching system assumes either:
1. The Prime has hedged this risk externally, receiving variable SOFR exposure that offsets fixed NFAT duration, OR
2. The NFAT itself is priced as SOFR + spread, so yield floats with the benchmark

### Validation

lpla-verify validates that Primes deploying into duration NFATs have declared either:
- Hedge positions covering the interest rate exposure
- SOFR plus terms on the underlying NFAT

Primes without valid hedging or floating-rate terms cannot deploy into duration NFATs via the ALDM system.

---

## Substage Mapping

| Substage | Legal Work |
|---|---|
| **1.0** | Confirm Term Halo partners; begin buybox definition with first cohort |
| **1.5** | Halo1 legal framework complete — buybox template, pre-signed agreements, recourse mechanisms |
| **1.6** | Halo2-Halo6 — reuse Halo1 templates with partner-specific buybox parameters |

---

## Related Documents

| Document | Relationship |
|---|---|
| [`phase-1-overview.md`](phase-1-overview.md) | Phase 1 substages |
| [`halo-book-deep-dive.md`](halo-book-deep-dive.md) | Book-level bankruptcy remoteness mechanics |
| [`../../sky-agents/halo-agents/halo-class-book-unit.md`](../../sky-agents/halo-agents/halo-class-book-unit.md) | Legal mapping (BVI SPC / Delaware) for Class/Book/Unit |
| [`../../sky-agents/halo-agents/term-halo.md`](../../sky-agents/halo-agents/term-halo.md) | Term Halo business overview |
| [`../../smart-contracts/nfats.md`](../../smart-contracts/nfats.md) | NFAT smart contract specification |
