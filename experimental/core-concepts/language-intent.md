# Language Intent

> The single trusted translator from human directives to machine logic, grounded by the Synomic Library.

**Also known as:** the translator, translation layer, intent translation

## Definition

Language Intent is the system that translates human intent (Atlas, Agent Directives, Teleonome Directives) into machine logic. It is a single translation layer — not multiple competing translators — grounded by the Synomic Library to ensure honest interpretation and resistance to prompt engineering. All human-readable directives at every layer of the five-layer architecture pass through this one trusted translator.

The choice of a single translator follows the same logic as a single root of trust in cryptography: one maximally-scrutinized point concentrates all defensive resources, whereas multiple translators would each receive less scrutiny and could diverge in interpretation.

## Key Properties

- Single translation layer — all human text (Atlas, Agent Directives, Teleonome Directives) passes through the same system
- Grounded by the Synomic Library — uses canonical knowledge to ensure honest interpretation
- Resists prompt engineering and adversarial manipulation
- The bootstrapping circular dependency is the known deepest vulnerability: Language Intent needs the Library to translate accurately, but the Library is shaped by what the Axioms (translated by Language Intent) say matters
- Security model: concentrate maximum collective attention on this one vulnerability, rather than distributing translation across multiple less-scrutinized interpreters
- Bridges human-readable text (soft, ambiguous) to machine constraints (hard, deterministic)

## Relationships

- **requires:** [five-layer-architecture](five-layer-architecture.md) — operates at every layer where human directives exist
- **implements:** [atlas-synome-separation](atlas-synome-separation.md) — Language Intent is the bridge that translates Atlas principles into Synome constraints
- **threatened-by:** [cancer-logic](cancer-logic.md) — if Language Intent is corrupted, the entire system's interpretation of human values becomes unreliable
