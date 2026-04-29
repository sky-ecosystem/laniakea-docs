# Defense Stacks

> The synomics architecture has three named defense-in-depth stacks operating at different scopes. They are complementary, not redundant. This doc names them side-by-side and disambiguates.

**Also known as:** the three stacks, defense-in-depth scopes

## The Three Stacks

| Stack | Scope | What it defends | Layers | Canonical source |
|-------|-------|-----------------|--------|------------------|
| **Cancer-Logic Defense Stack** | Epistemic | A single teleonome's (or the Synome's) knowledge base against self-corruption through overeager updates | 7 — ossification → symbolic gate → validation → governance → monitoring → rollback → peer enforcement | [`../synodoxics/security-and-resources.md`](../synodoxics/security-and-resources.md#defense-in-depth-the-cancer-logic-defense-stack) |
| **Institutional Enforcement Stack** | Institutional | The cosmic-scale Hearth synome against systemic capture | 4 — Synome → Core Council → Superstructure → Teleonomes | [`four-layer-enforcement-stack.md`](four-layer-enforcement-stack.md) |
| **Alignment Verification Stack** | Individual | The aligned coalition against deception by any single teleonome | 4 — structural binding → natural embodiment → collective override → conspiracy coordination problem | [`../synoteleonomics/teleonome-binding.md`](../synoteleonomics/teleonome-binding.md#the-alignment-verification-stack) |

## How They Compose

The three stacks address distinct threat profiles:

- **Cancer-logic** is *internal* corruption — bad patterns entering the mesh and propagating through the system that holds them. The defense is structural (ossification, evidence dynamics) plus procedural (governance review, rollback).
- **Institutional capture** is *systemic* failure — any single layer of the cosmic hierarchy (Synome rules, governance, superstructure) being subverted. The defense is hierarchical, with each layer checked by the one below it and the bottom layer (collective teleonomes) able to hard-fork.
- **Deceptive alignment** is *individual* failure — a teleonome that maintains observable compliance while harboring different goals. The defense layers behavioral observation onto biological grounding onto collective response onto the trust problem facing any conspiracy.

A failure that gets through one stack doesn't necessarily get through the others. A teleonome whose telart has cancer-logic corruption (Cancer-Logic Defense Stack failure) can still be observably misbehaving and trigger Alignment Verification responses. A captured Core Council (Institutional Enforcement Stack failure) is independent of any individual teleonome's alignment status.

## When to Reference Which

- Discussing self-improvement risk, knowledge corruption, or RSI safety → **Cancer-Logic Defense Stack**
- Discussing cosmic-scale governance, superstructure power constraints, or the hard-fork backstop → **Institutional Enforcement Stack**
- Discussing how an individual teleonome's alignment is verified without transparency, the verification ceiling, or perfectly compliant deception → **Alignment Verification Stack**

## Relationships

- **scopes-of:** [fractal-security-pattern](fractal-security-pattern.md) — all three stacks are instantiations of growth-with-cancer-safeguards at different scales
- **defends-against:** [cancer-logic](cancer-logic.md) — Cancer-Logic Defense Stack directly; the other two prevent the conditions under which cancer-logic could spread
- **defends-against:** [rogue-threat-model](rogue-threat-model.md) — Institutional and Alignment Verification stacks directly; Cancer-Logic Defense prevents internal failures that could be exploited
