# V1 Principles

**Status:** Draft (companion to `phase-1-spaces.md`, updated 2026-05-17)

The principles below are distilled from the Phase 1 v4 design decisions and the worked NFAT example in [`phase-1-spaces.md`](phase-1-spaces.md). They describe the invariants the Phase 1 substrate is built around — the discipline that lets later phases unfold capacity without rewriting what books rest on. Each principle survives every later phase; what unlocks (real auctions, factory stack, sentinel formations, multi-form risk framework) extends these without contradicting them.

---

1. **Liability stickiness determines SDR capacity.** P1 computes Structural Demand Resource (SDR) from the lot-age surface: Lindy SDR turns observed liability stickiness into bucket capacity, then the governance-set SDR policy overlay constrains the dynamic result into effective SDR bucket capacity.

2. **Use Stressed Pull-to-Par (SPTP) for asset pull-to-par horizon.** Stress modifier reflects historical worst-case prepayment / amortization slowdowns. (V1 carve-out: SPTP = remaining nominal term, no stress modifier yet.)

3. **Hold-to-par matching protects against credit-spread and liquidity risk by making the position hold-to-par.** Credit spreads are mean-reverting; forced-sale liquidity loss is avoided when the Prime can hold.

4. **Rate risk is calculated even when covered.** The risk form outputs rate-CRR. P1 SDR matching makes rate-CRR non-binding for the matched structbook portion; unmatched exposure still carries rate treatment.

5. **SPTP determines matching eligibility.** Only assets with SPTP ≤ liability bucket tenor AND rate-neutral exposure can be matched.

6. **Matched positions get risk-weight treatment.** Capital only for fundamental risk.

7. **Unmatched positions get forced-loss treatment.** Capital for `max(RW, forced-loss-capital)`.

8. **Crypto lending is structurally tranched.** The senior exo unit's default-CRR is the maximum approved scenario loss through the exobook asset-side stress and liability waterfall. Expected loss is a pricing metric, not the P1 capital standard.

9. **Concentration limits prevent diversification illusions.** Capital must survive each stress scenario applied to its correlated asset group.

10. **Default-deny is the discipline.** Anything the framework can't model adequately gets CRR 100%. (Phase 1 instance: an exobook without a fresh accordant attestation does not roll up.)

11. **Sub-book composition is continuous, not binary.** The optimization-shaped sub-books blend matched and unmatched portions smoothly as capacity shifts.

12. **Currency frame ≠ instrument.** Frame is the unit of account (USD); instruments (USDC, USDT, ETH) translate to the frame with declared stress.

13. **Real-time equity recomputation is the operational invariant.** Every book's equity must be computable continuously; this drives the synserv heartbeat, attestor cadence, and the lift-from-day-1 commitment that keeps all logic in synlang rather than Python placeholders.

14. **DSC is the only in-synome settlement cadence.** Legacy monthly settlement remains out-of-band. Capabilities enter the synome by entering the daily synomic settlement cycle; P1 uses it for structural-demand processing.

15. **Temporary equations must be contained.** The P1 ownership-weighted temporary SDR auction lives entirely inside `&entity.generator.usge.sdr-auction`; `&core.treasury` stores only fundamental token-share facts, and `&entity.generator.usge.structural-demand` stores effective SDR bucket capacity, so the temporary auction body can be swapped out cleanly. Structbooks consume only the `sdr-allocation` atom shape, so later real SDR auctions can replace the writer without changing the book read path.

16. **Market data is market memory.** The Crypto Majors Oracle emits reducer outputs and checkpoints from source tapes; scenarios should reference those reducer memories wherever possible and minimize arbitrary shock inputs.

---

## File map

| Doc | Relationship |
|---|---|
| [`phase-1-spaces.md`](phase-1-spaces.md) | Phase 1 v4 spec; the worked NFAT example exercises these principles end-to-end |
| [`roadmap-ideas.md`](roadmap-ideas.md) | Vocabulary, lift principle, sudo staircase that frames how these principles get extended |
| [`../roadstart/risk-framework.md`](../roadstart/risk-framework.md) | Risk-framework summary (these principles are the v1 instantiation of its substrate) |
