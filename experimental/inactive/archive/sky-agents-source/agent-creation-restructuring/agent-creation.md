# Agent Creation

**Status:** Draft concept
**Date:** February 2026

---

## Overview

Agent creation is the process by which new agents are brought into existence within the Sky Ecosystem. Both existing agents and external users (individuals or entities not yet operating an agent) can create new agents.

All agent creation — and all restructuring actions — require a **Guardian Accord**: the creator must first secure a guardian agent to support and trigger the action on their behalf (except for Core Council-administered types, which are created directly by Core Council governance).

---

## The Guardian Accord

Before any rank 2 or rank 3 agent can be created, the creator must obtain a **Guardian Accord** — an agreement with a guardian agent to facilitate the creation.

**Process:**

1. **Request** — The creator (agent or external user) approaches a guardian agent and requests support for creating a new agent
2. **Accord** — The guardian evaluates the request and, if accepted, enters into a guardian accord with the creator
3. **Execution** — The guardian triggers the on-chain creation action, instantiating the new agent

The guardian accord requirement applies to both agent creation and [agent restructuring](agent-restructuring.md) (Type 1 and Type 2). Guardians serve as the operational gatekeepers for bringing new agents into the ecosystem.

---

## Creation by External Users

External users — individuals or entities that do not yet operate an agent — can create agents to enter the Sky Ecosystem:

**Creating a Folio Agent:**
- Instant creation, minimal requirements
- Entry point for Growth Staking participation
- Guardian Accord is satisfied automatically (auto-accord) — preserving instant creation while maintaining the formal requirement. The guardian accord for folios is a lightweight, programmatic process rather than a bilateral negotiation

**Creating a Standard Halo:**
- User obtains a guardian accord
- Guardian triggers Halo creation
- User receives admin ownership of the new Halo (un-tokenized)
- User can optionally issue tokens later

**Creating a Prime:**
- User obtains a guardian accord
- Guardian triggers Prime creation
- User receives admin ownership of the new Prime (un-tokenized)
- Prime enters a **waiting period** — Sky Agent Primitives (capital deployment from Sky Protocol, ingression, risk capital origination) are not accessible until tokens are issued
- User issues tokens at their discretion: receives 95% of total supply, 5% retained by the protocol as agent creation fee
- Sky Agent Primitives become accessible upon token issuance

---

## Creation by Existing Agents

Existing agents can create new agents as part of their operations. This is mechanically identical to [Type 1 Restructure](agent-restructuring.md#type-1-restructure) — the creating agent transfers assets into the new agent and receives ownership or tokens in return. The guardian accord requirement applies.

---

## Creation by Core Council

Rank 1 agents (other than Guardians) are created directly by Core Council governance:

**Creating a Core Controlled Agent:**
- Core Council governance action (via SpellCore)
- No guardian accord required — Core Council has direct authority
- Typically created to manage legacy protocol positions or for new Core Council operational needs

**Creating a Recovery Agent:**
- Core Council governance action (via SpellCore) in response to a crisis
- No guardian accord required
- Created when a Guardian collapses or is implicated in misconduct
- Temporary — dissolves after the crisis is resolved

---

## Agent Types

| Agent Type | Rank | Token Required | Sky Agent Primitives | Creation Fee | Created By |
|---|---|---|---|---|---|
| **Folio Agent** | 3 | No | No | None | External user (via Guardian Accord) |
| **Standard Halo** | 3 | Optional | No | None | External user or existing agent (via Guardian Accord) |
| **Prime** | 2 | Required for primitives | Yes (after token issuance) | 5% of token supply | External user or existing agent (via Guardian Accord) |
| **Generator** | 2 | Yes | N/A (is the primitive source) | 5% of token supply | Governance |
| **Guardian** | 1 | Yes | N/A | Collateral posting | Governance |
| **Core Controlled** | 1 | No | No | None | Core Council (SpellCore) |
| **Recovery** | 1 | No | No | None | Core Council (SpellCore, crisis response) |

**Sky Agent Primitives** — the set of protocol-level capabilities exclusive to Primes: receiving capital from Sky Protocol, participating in ingression, originating risk capital, and accessing settlement infrastructure. These are locked until the Prime has issued tokens, creating a natural gate between admin-controlled setup and full protocol participation.

---

## Prime Waiting Period

When a Prime is created (either by an external user or via Type 1 Restructure), it does not issue tokens immediately. During this waiting period:

- The Prime exists as an admin-controlled entity
- Assets can be transferred in and managed
- The synomic artifact can be developed
- Operational infrastructure can be built
- **Sky Agent Primitives are not accessible**

This waiting period allows the creator to set up the Prime's operations, build its synomic artifact, and prepare for tokenization — without rushing to issue tokens before the agent is ready. Token issuance is a deliberate step that signals readiness for full protocol participation.

---

## Open Questions

- **Guardian selection** — How do creators find and select guardians? Is there a registry of available guardians, or is it a bilateral negotiation?
- **Guardian obligations** — What does the guardian commit to in the accord? Ongoing operational support, or just the creation trigger?
- **Folio Agent guardians** — Resolved: Folio Agents use an automatic guardian accord (auto-accord), preserving instant creation. See "Creating a Folio Agent" above.
- **Creation limits** — Are there any governance-set limits on the rate of new agent creation?
