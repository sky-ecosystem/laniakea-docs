# V1 Principles

**Status:** Draft (companion to `phase-1-spaces.md`, 2026-05-15)

The thirteen principles below are distilled from the Phase 1 v3 design decisions and the worked NFAT example in [`phase-1-spaces.md`](phase-1-spaces.md). They describe the invariants the Phase 1 substrate is built around — the discipline that lets later phases unfold capacity without rewriting what books rest on. Each principle survives every later phase; what unlocks (auctions, daily settlement, factory stack, sentinel formations, multi-form risk framework) extends these without contradicting them.

---

1. **Liability duration determines duration capacity.** The Lindy Duration Model measures how much of the liability base is short-term vs long-term.

2. **Use Stressed Pull-to-Par (SPTP) for asset duration.** Stress modifier reflects historical worst-case prepayment / amortization slowdowns. (V1 carve-out: SPTP = remaining nominal term, no stress modifier yet.)

3. **Duration matching protects against credit spread risk, not rate risk.** Credit spreads are mean-reverting; rate shifts can be permanent. Matching covers the first; the second requires hedging.

4. **All fixed-rate exposure must be rate-hedged** (or hold rate-hedge capital) for matched treatment. (V1 carve-out: rate-hedge capital waived for matched NFAT positions.)

5. **SPTP determines duration matching eligibility.** Only assets with SPTP ≤ liability tier duration AND rate-neutral exposure can be duration-matched.

6. **Matched positions get risk-weight treatment.** Capital only for fundamental risk.

7. **Unmatched positions get forced-loss treatment.** Capital for `max(RW, forced-loss-capital)`.

8. **Crypto lending is structurally tranched.** The senior tranche's risk = asset stress through junior cushion. Gap risk has unified into the standard tranche math.

9. **Concentration limits prevent diversification illusions.** Capital must survive each stress scenario applied to its correlated asset group.

10. **Default-deny is the discipline.** Anything the framework can't model adequately gets CRR 100%. (Phase 1 instance: an exobook without a fresh accordant attestation does not roll up.)

11. **Sub-book composition is continuous, not binary.** The optimization-shaped sub-books blend matched and unmatched portions smoothly as capacity shifts.

12. **Currency frame ≠ instrument.** Frame is the unit of account (USD); instruments (USDC, USDT, ETH) translate to the frame with declared stress.

13. **Real-time equity recomputation is the operational invariant.** Every book's equity must be computable continuously; this drives the synserv heartbeat, attestor cadence, and the lift-from-day-1 commitment that keeps all logic in synlang rather than Python placeholders.

---

## File map

| Doc | Relationship |
|---|---|
| [`phase-1-spaces.md`](phase-1-spaces.md) | Phase 1 v3 spec; the worked NFAT example exercises these principles end-to-end |
| [`roadmap-ideas.md`](roadmap-ideas.md) | Vocabulary, lift principle, sudo staircase that frames how these principles get extended |
| [`../risk-framework/`](../risk-framework/) | Target risk framework (these principles are the v1 instantiation of its substrate) |
