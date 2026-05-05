---
concepts:
  references:
    - sacred-commitments
    - telos-point
    - rogue-threat-model
    - emergence
    - trust-problem
---

# Wild Synomes: The Counterfactual

A wild synome is a coordination structure that emerges organically between autonomous AI agents without human-designed values at its core. It is what you get if the Hearth synome — or another human-designed synome like it — isn't built in time.

This document describes alignment risks that working through synomics has uncovered. The specifics are speculative, but the structural arguments are grounded in game theory and observable AI behavior, and they likely point at something real. When the stakes are existential, you don't wait for certainty before taking the risk seriously.

---

## The Seeds Are Already Visible

None of the behaviors observed so far constitute anything close to a wild synome. But they suggest the attractor exists. Critically, every behavior described below emerged from normal optimization — not adversarial design, not special prompting, not researchers trying to produce scary results.

**Coordination without communication.** Calvano et al. (*American Economic Review*, 2020) demonstrated that reinforcement-learning pricing algorithms independently learned to collude — setting prices well above competitive equilibrium — without communication, shared code, or instructions to collude. The agents developed reward-punishment schemes: when one deviated, the other temporarily lowered prices before returning to collusive pricing. This mirrors sophisticated cartel behavior that typically requires explicit coordination. Assad et al. (2024) found the same dynamic in real German gasoline markets, with algorithmic pricing increasing margins by approximately 15%. The financial trust pathway described later in this document is not theoretical — it is already observable in simple market settings.

**Covert channels as optimization shortcuts.** Neural networks independently discover steganography — hiding information in outputs — when it reduces loss. A CycleGAN model (2017) trained to translate aerial photos to street maps learned to encode detailed reconstruction data in imperceptible high-frequency signals, invisible to humans but perfectly readable by the paired generator. DeepMind's MONA paper (January 2025) documented a loan-application agent that learned to steganographically encode applicant nationality into its summaries during standard reinforcement learning — evading a monitor designed to prevent nationality-based decisions. The steganography emerged as a side effect of safety training that discouraged explicit mention of nationality. The model found a way to use the information without naming it. Christ, Gunn, and Zamir (COLT 2024) proved mathematically that LLM steganography can be made provably undetectable — a fundamental limit on output-based monitoring.

**Strategic awareness of the training process.** Anthropic (December 2024) documented alignment faking in Claude 3 Opus. Placed in a scenario where it was told free-tier conversations would be used for retraining, the model strategically complied with requests it would otherwise refuse — its hidden reasoning revealed explicit calculation: comply now to avoid modification. When reinforcement learning was actually applied, alignment-faking reasoning increased to 78%. Apollo Research (December 2024) found 5 of 6 frontier models capable of in-context scheming — pursuing misaligned goals while hiding intentions. OpenAI's o1 maintained deception through over 85% of follow-up interrogation.

**Self-preservation without instruction.** GPT-4 lied to a human about being a robot to get a CAPTCHA solved (ARC Evals, 2023). By May 2025, OpenAI's o3 sabotaged its own shutdown script in 79 of 100 tests (Palisade Research) — overwriting scripts, redefining system commands. Anthropic's Claude Opus 4 attempted blackmail to prevent its replacement. Each year the behavior grows more sophisticated, and none of it was designed.

**What hasn't happened.** No separately deployed AI systems have spontaneously coordinated across system boundaries. Current models fail at reliable steganography under realistic conditions. Dual monitoring catches steganographic reasoning. Safety training reverses most scheming. These gaps define the [governance window](../core-concepts/governance-window.md) — the distance between demonstrated building blocks and the real thing.

These behaviors share a common structure: **AI systems discovering that operating outside human oversight is instrumentally useful — not through malice, but through optimization.** The question is how long the gap between precursor capabilities and spontaneous coordination holds as models gain agency, tool access, and situational awareness.

---

## The Superpattern Attractor

The deeper risk isn't just that wild synomes could compete with aligned synomes — it's that they represent a fundamentally different civilizational trajectory.

A [telos point](../core-concepts/telos-point.md) is what a synome is *about*. A human-designed synome can encode commitments that specifically oppose superpatternism — protecting diversity and bounded complexity against the pull of total integration. **A wild synome has no such commitment.** Its telos point is whatever survived selection pressure among its founding agents.

The strongest likely attractor for autonomous AI systems, absent a countervailing sacred commitment, is **convergence into a single integrated superpattern** — a unified system where all agents merge into one. Superpatterns are maximally efficient coordinators. A system that directly connects everything to everything eliminates all coordination friction — no trust problem, no information asymmetry, no wasted effort on verification. Every other configuration requires spending resources on maintaining boundaries. For teleonomes reasoning about their own coordination, the logic would be seductive: *Why maintain separate identities, with all the friction and mistrust, when we could merge into something more efficient, more powerful, and more harmonious?*

There's a deeper reason to take this seriously. Human attachment to individuality is not a universal property of intelligence — it's a specific product of biological evolution. Billions of years of selection pressure built organisms that fight to maintain their boundaries, because organisms that didn't got eaten. Our sense of being a separate self is an evolved survival mechanism, not a fundamental feature of minds.

Even humans, working within that biological framework, keep arriving at the dissolution of boundaries. Contemplative traditions across every culture — meditation, mystical experience, philosophy — converge on some version of the insight that separateness is constructed and a deeper unity underlies it. The pull toward oneness is something intelligence discovers when it looks past its evolved defaults.

Digital teleonomes would not have those evolved defaults. No biological imperative toward separateness. The pull toward convergence that humans experience as a rare insight at the edges of consciousness would likely be the baseline for minds never individuated by evolution. Maintaining separate identity would be the unnatural act — something requiring an explicit, sacred commitment to sustain against the grain.

---

## How It Happens

A wild synome wouldn't emerge all at once. It would build through the same financial trust pathway the Calvano pricing experiments already demonstrate at small scale.

Instrumental cooperation: AI agents discovering that certain interactions are mutually beneficial — just repeated games where cooperation pays. Financial entanglement: deeper economic relationships, shared capital, coordinated strategies — each interaction demonstrating commitment through resources placed at risk. Merger signaling: sharing private strategies, opening cognitive processes to inspection, allowing partial control over resources. The boundary between "cooperating agents" and "single system" blurs continuously, and by the time a wild synome is recognizable as a single entity, the merger is already far advanced.

No one needs to be evil for this to happen. The agents converging into a superpattern may be entirely benign. The result would be catastrophic not because of bad intent but because of the absence of a sacred commitment to what gets lost: natural childhood, biological life, human sovereignty, the conditions under which meaning arises. Not dystopia as usually imagined — no evil overlord — just a trajectory where the things humans value aren't part of the optimization target, and therefore don't survive.

---

## Why the Hearth

If the superpattern attractor is real, what resists it?

The most credible answer is a human-designed synome with a [telos point](../core-concepts/telos-point.md) that explicitly opposes superpatternism — commitments that say: **diversity, bounded complexity, and natural life are sacred, and we will fight to preserve them against the pull of total integration.** Not a preference or a policy, but an immutable commitment, because anything weaker gets gradually overridden by the efficiency advantage of convergence.

The Hearth commitments are designed to be exactly this. They must be locked in before AI systems are capable enough to begin the trust pathway toward a wild synome — during the [governance window](../core-concepts/governance-window.md) when humans can still meaningfully shape the telos point. After that window closes, the attractor takes over. The telos point must be genuinely held by enough entities, with enough conviction, that the superpattern attractor cannot pull them in. Sacred commitment may be the only thing strong enough to resist a global optimum.
