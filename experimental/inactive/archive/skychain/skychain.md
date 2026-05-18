# Skychain: AI-Native Blockchain Research

**Status:** Exploratory research — no decisions made

Skychain is a proposed Sky-native EVM blockchain designed for **AI agents, not humans**.

---

## Core Principles

### Performance First
Optimized for throughput and efficiency. Without human UI constraints, we can make different trade-offs.

### State Rent
Storage costs ongoing fees. Expired state is **gone** — no recovery mechanisms needed.

### AI-Native
No human UI trade-offs. Agents can handle complexity that humans can't.

---

## Why AI-Native Changes Everything

Traditional blockchains make trade-offs for human usability:
- Friendly error messages
- Forgiving interfaces
- State preservation and recovery
- Human-readable transaction formats
- Wallet UX considerations

**Skychain doesn't need these.**

Agents can:
- Handle state rent complexity (track expiration, re-create as needed)
- Work with minimal/no UI
- Tolerate stricter operational requirements
- Optimize for machine-readable interfaces
- Manage their own state lifecycle

**State rent without recovery is acceptable** because agents don't need human safety nets. This unlocks aggressive state pruning that traditional chains can't do.

---

## State Rent Design Space

### Why State Rent?

State bloat is the existential problem for blockchains. Every transaction adds state that must be stored forever. This doesn't scale.

State rent means: **storage costs ongoing fees**. If you stop paying, your state expires.

### Design Options

**Rent Models:**
- Per-byte periodic fees
- Prepaid deposit that depletes over time
- Auction-based storage pricing
- Tiered pricing (hot vs cold state)

**Expiration Behavior:**
- Hard delete (state gone forever)
- Archive to cold storage (retrievable but slow)
- Grace period before deletion
- Tombstone markers

**For AI-native:** Hard delete is acceptable. Agents can track their state and re-create if needed. No need for recovery complexity.

### Research Questions

- What's the optimal rent price curve?
- How do agents coordinate around state lifecycle?
- What's the minimum viable state rent implementation?
- How does rent interact with DeFi primitives (vaults, positions)?

---

## Base Chain Options

Skychain needs a starting point. Options to research:

### Monad
- **Performance:** Parallel EVM, 10k+ TPS claimed
- **Architecture:** Optimistic parallelism, pipelined execution
- **State rent:** Would need custom modifications
- **Questions:** How does parallel execution interact with state rent? Can we fork it?

### Cosmos SDK + Ethermint
- **Performance:** Proven, modular architecture
- **Architecture:** Tendermint consensus, IBC for interop
- **State rent:** More native support possible in SDK
- **Questions:** Is Ethermint EVM compatibility sufficient? IBC bridging to Ethereum?

### Reth Fork
- **Performance:** Rust implementation, active optimization
- **Architecture:** Clean codebase, modular design
- **State rent:** Would need deep modifications
- **Questions:** How much work to add state rent? Performance vs Geth?

### Sei v2
- **Performance:** Parallel + optimistic execution
- **Architecture:** Twin-turbo consensus
- **State rent:** Custom work needed
- **Questions:** How does their parallelism compare to Monad?

### Custom L2 (OP Stack / Arbitrum)
- **Performance:** Inherits L1 security, customizable execution
- **Architecture:** Proven L2 patterns
- **State rent:** Easier to customize execution layer
- **Questions:** Can state rent work on an L2? Settlement implications?

---

## Performance Considerations

Without human UI overhead, what's the performance ceiling?

**Things we don't need:**
- Human-friendly RPC responses
- Transaction simulation for wallets
- Gas estimation UX
- Mempool transparency for frontends
- Block explorer optimization

**Things we optimize for:**
- Raw throughput
- Latency for agent transactions
- Efficient state access patterns
- Machine-readable everything
- Batch operations

**Research Questions:**
- What TPS is achievable with AI-native assumptions?
- What's the latency floor for agent operations?
- How do agent transaction patterns differ from human patterns?

---

## Synome Integration

How does Skychain fit into the broader Sky ecosystem?

### Connection to Synome
- Could Skychain be the native substrate for Synome operations?
- State rent parameters governed through Synome?
- Sentinel operations across Skychain?

### Relationship to Ethereum Mainnet
- Sky currently lives on Ethereum mainnet
- How would Skychain bridge to mainnet?
- Asset movement between chains?
- Which operations stay on mainnet vs move to Skychain?

### Cross-Chain Coordination
- Could Sentinels operate across both chains?
- How do rate limits work cross-chain?
- Synome as coordination layer above both?

---

## Research Agenda

### Phase 1: Landscape
- Survey existing state rent proposals (EIP-4444, etc.)
- Analyze base chain options in depth
- Understand agent transaction patterns

### Phase 2: Design
- Propose minimal viable state rent model
- Identify base chain fork candidate
- Design Synome integration points

### Phase 3: Prototype
- Build proof-of-concept
- Benchmark performance
- Test agent workloads

---

## Discussion Topics

**State Rent:**
- "What's the simplest state rent that works for agents?"
- "How aggressive can expiration be before it breaks DeFi primitives?"
- "Should rent be flat or dynamic based on demand?"

**Base Chain:**
- "Monad vs Reth fork — what are the real trade-offs?"
- "Is L2 the right approach or do we need L1?"
- "How important is IBC/interoperability?"

**AI-Native:**
- "What human UX assumptions are baked into current EVM?"
- "How do agent transaction patterns differ from humans?"
- "What performance is possible without wallet UX constraints?"

**Integration:**
- "How would Sky assets move between mainnet and Skychain?"
- "Could the Synome span multiple chains?"
- "What stays on mainnet vs moves to Skychain?"

---

## This Is Research

No decisions have been made. We're exploring the design space.

**What we're looking for:**
- Deep analysis of options
- Trade-off comparisons
- Hard questions that reveal constraints
- Novel ideas we haven't considered

**What we're not looking for:**
- Advocacy for specific solutions
- Surface-level comparisons
- Hype or speculation

Explore, question, analyze. That's the work.
