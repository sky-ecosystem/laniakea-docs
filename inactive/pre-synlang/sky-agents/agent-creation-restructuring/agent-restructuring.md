# Agent Restructuring

**Status:** Draft concept
**Date:** February 2026

---

## Overview

Agent Restructuring defines two standard actions that allow agents to reorganize capital and infrastructure within the Sky Ecosystem. These are always-available actions — any agent can initiate them at any time, subject to the constraints below.

All restructuring actions require a **Guardian Accord** — the initiating agent must first secure a guardian to support the action, and the guardian triggers the restructuring on their behalf. See [Agent Creation](agent-creation.md) for details on the guardian accord process.

---

## Type 1 Restructure

**Action:** Agent A creates a new agent, transfers assets into it, and receives ownership or tokens in return.

**Mechanics:**

1. Agent A initiates creation of a new Agent B (Halo or Prime)
2. Agent A transfers selected assets into Agent B
3. Agent A receives control of Agent B:
   - **If B is a Halo:** Agent A receives admin ownership (un-tokenized Halo controlled by a single admin owner)
   - **If B is a Prime:** Agent A receives admin ownership. The Prime does not issue tokens at creation — it starts as an admin-controlled entity. The Prime's Sky Agent Primitives (capital deployment from Sky Protocol, ingression, etc.) are not accessible until tokens are issued. Token issuance happens later at the owner's discretion, at which point the owner receives 95% of tokens (5% agent creation fee to the protocol).

**Availability:** All agents, including Folio Agents.

**Use cases:**

- A Folio Agent holder decides to formalize their growth asset portfolio into a Standard Halo — assets transfer out, admin control transfers back
- A Folio Agent holder with a strong thesis seeds a new Prime — assets transfer out, admin control transfers back. Prime remains in a waiting period until the owner issues tokens, at which point Sky Agent Primitives become accessible and the Folio Agent receives 95% of tokens (growth assets at GF 2.5×)
- An existing Prime spins off a specialized strategy into a new Halo subsidiary
- A Halo creates a new Halo to isolate a specific asset class or geography

**Example — Folio Agent seeds a Prime:**

```
Before:
  Folio Agent
    ├── Staked SKY: $100k
    └── Assets: $500k (mixed portfolio)

Type 1 Restructure → creates Prime "Alpha"

Immediately after:
  Folio Agent
    ├── Staked SKY: $100k
    └── Admin control of Alpha Prime

  Alpha Prime (new, admin-controlled, no tokens yet)
    └── Assets: $500k (transferred from Folio Agent)
    └── Sky Agent Primitives: LOCKED (waiting period)

After token issuance:
  Folio Agent
    ├── Staked SKY: $100k
    └── Growth Assets: 95% of Alpha Prime tokens
        (valued at min(book, market) for staking factor purposes)

  Alpha Prime (tokenized, Sky Agent Primitives active)
    └── Assets: $500k
```

---

## Type 2 Restructure

**Action:** Agent A spins off its infrastructure — not just assets, but its entire operational system and parts of its synomic artifact — into a new Halo that it controls. Agent A then optionally upgrades its own agent type.

**Mechanics:**

1. Agent A creates a new Halo B
2. Agent A transfers its agent infrastructure (operational system, relevant parts of synomic artifact) into Halo B
3. Agent A receives admin ownership of Halo B
4. Optionally: Agent A upgrades its own agent type from Halo to Prime

Agent A retains its identity and token throughout. The infrastructure is what moves.

**Availability:** All agents except Folio Agents.

**Use cases:**

- A successful Standard Halo upgrades to Prime status — it spins off its existing operations into a subsidiary Halo (which it controls via admin), then upgrades itself to a Prime. The token stays the same, token holders are now holding a Prime token instead of a Halo token, and the Prime controls its former operations as a subsidiary.
- A Halo that has grown complex separates its infrastructure into a subsidiary for cleaner governance, without upgrading.

**Example — Standard Halo upgrades to Prime:**

```
Before:
  Halo "Beta" (tokenized)
    ├── Token: BETA
    ├── Infrastructure: lending protocol + oracle system
    └── Assets: $200M deployed

Type 2 Restructure → spins off infra, upgrades to Prime

After:
  Prime "Beta" (same token: BETA)
    ├── Token: BETA (unchanged, now a Prime token)
    └── Admin control of:
        └── Halo "Beta Operations" (new, un-tokenized)
            ├── Infrastructure: lending protocol + oracle system
            └── Assets: $200M deployed
```

---

## Relationship to Growth Staking

Type 1 Restructure is the natural mechanism by which Folio Agent holders graduate into the Agent layer:

1. Staker creates a Folio Agent, accumulates assets via Growth Staking rewards
2. When ready, Type 1 Restructure → creates a Standard Halo or Prime
3. Agent tokens flow back into the Folio Agent as growth assets (GF 2.5×)
4. The staker now earns Growth Staking rewards via their Agent tokens while their capital is actively deployed

Type 2 Restructure enables Standard Halos to upgrade to Prime status as they mature — preserving token holder continuity while gaining Prime-level capabilities (capital deployment from Sky Protocol, ingression, risk capital origination).

---

## Constraints and Open Questions

- **5% agent creation fee** — Applies when a Prime issues tokens (whether created via Type 1 Restructure or standalone agent creation). Fee is 5% of total token supply retained by the protocol. Does not apply to Halos.
- **Synomic artifact transfer** — In Type 2, which parts of the synomic artifact transfer to the new Halo vs. stay with the original agent? Likely: operational artifacts transfer, identity/governance artifacts stay.
- **Governance approval** — Does upgrading from Halo to Prime (Type 2) require governance approval, or is it a permissionless action?
- **Reversibility** — Can a Type 2 Restructure be reversed (Prime downgrades back to Halo, reabsorbs subsidiary)?
