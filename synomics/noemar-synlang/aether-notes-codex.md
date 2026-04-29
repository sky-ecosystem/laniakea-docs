# AETHER - Codex Notes From A Second Pass

Date: 2026-04-25

Scope: I read `aether-notes-claude.md`, the public docs, core engine code,
Space/query code, protocol code, Atlas/SkyClaw data and APIs, RSI, CLAW, tests,
and the web/API product surface. I could not run the Python probes locally
because this machine exposes Python 3.9.6 on `python3`, while `pyproject.toml`
requires Python >=3.10 and the package imports use 3.10 type syntax.

## Short Thesis

AETHER is best understood as an in-process, typed, S-expression logic database
and rule engine that is being turned into an agent substrate.

The strongest claim is not "AETHER delegates computation to Python libraries."
That is true for protocols, but incomplete. The core `Space` and rewriter
compute plenty: matching, unification, backward chaining, compound query
resolution, negation-as-failure, builtin arithmetic/comparison/list operations,
memoized rewriting, and closed-world/open-world query semantics. Protocols are
the extension boundary for specialized computation, not the whole engine.

My current framing:

1. `Space` is the center of gravity.
2. Protocols give external computation a symbolic, auditable contract.
3. Atlas is the main pressure test for real, messy rulebook reasoning.
4. RSI and CLAW are attempts to move agent behavior, learning, and extension
   into the same fact/rule/protocol substrate.
5. The web/API surface is not decorative. It is already shaping the core toward
   datasets, streaming agents, cancellation, auth, and repeatable demos.

## What I Think Is Real Versus Aspirational

Real today:

- A pure-Python S-expression AST with parser, canonicalization, rules, variables,
  matching, unification, rewriting, and memoization.
- A `Space` abstraction with facts, rules, type/validation hooks, an inverted
  index, open-world `query()`, and closed-world `query_closed()`.
- Compound query resolution for `and`, `or`, `not`, nested compounds,
  existential variables in compound bodies, multi-variable joins, and several
  Atlas-discovered resolver regressions.
- Protocol dispatch for graph, SMT, symbolic math, temporal, PLN, and custom
  protocols.
- A substantial PLN implementation with belief storage, revision, chaining,
  evidence stamps, delta-method uncertainty formulas, and protocol queries.
- Atlas/LKIF/Sky governance data that acts as a real integration test, not just
  example content.
- RSI rule-author and protocol-author loops that fork Spaces, try changes,
  run regression checks, and promote successful changes.
- CLAW agent-loop state represented as AETHER facts, with rule-derived stopping
  policy and a real closed learning loop.
- API and web layers that expose datasets, queries, findings, graph/SMT demos,
  RSI streaming, and agent workflows.

Aspirational or limited today:

- General source-code self-rewriting. Rule addition and protocol promotion exist,
  but broad code rewriting remains future work.
- Cost-based query planning. The resolver has meaningful indexing and joins, but
  it is not yet a mature database optimizer.
- Fully compositional protocol routing. Nested protocol expressions work, but
  the router substitutes only the first result of a protocol subexpression.
- Strong sandboxing for generated protocol code. There is an import deny-list and
  staging path protection, but verification imports candidate code in-process.
- Complete resolver support for recursive/transitive closure over bare facts.
  Atlas currently ships explicit workarounds for this.
- A single canonical docs story. Several docs and comments are ticket history;
  some say work is missing even though code now exists, and some TODOs are stale.

## Architecture As I See It

### 1. Nodes And Syntax

The AST layer is intentionally small:

- `src/aether/nodes/atom.py`
- `src/aether/nodes/expression.py`
- `src/aether/nodes/rule.py`
- `src/aether/nodes/variable.py`
- `src/aether/parser/parser.py`

`Expression` equality and hashing intentionally ignore metadata and beliefs.
That makes canonical symbolic identity stable while letting provenance/trust
ride alongside the term. `Rule.create` enforces a useful discipline: variables
on the RHS must appear on the LHS unless the RHS is compound. That is what makes
existential variables explicit in rule bodies like:

```lisp
(= (has-friend $x)
   (and (likes $x $y)
        (likes $y $x)))
```

The parser treats `(= lhs rhs)` and `(-> lhs rhs)` as rules when validation
allows it. That means most data files are not just fact bags; they are also
loadable programs.

### 2. Space And Query Resolution

`src/aether/space/space.py` is the load-bearing file. It is where AETHER stops
being a syntax experiment and becomes a query engine.

The important behavior:

- `Space.add()` validates, type-checks, runs consistency checks, notifies
  protocols via `on_add`, stores facts/rules, and dual-stores fact-declaration
  rules like `(= (foo a) True)` as facts.
- `Space.query()` stages direct indexed lookup, backward chaining, protocol
  routing, simplification, and rewrite evaluation.
- `Space.query_closed()` gives CWA semantics through `ClosedResult`: unknown
  means known false, and limits raise rather than silently returning partial
  results.
- The compound resolver normalizes to NNF, resolves `and` by joining binding
  sets, resolves `or` by union/deduplication, and handles negation-as-failure
  by subtracting bindings after proof checks.
- The resolver has accumulated fixes for Atlas-grade cases: NAF over rule
  bodies, nested rule calls with existentials, ground-plus-existential
  conjunction order, and top-level compound queries with free variables.

This is more than "index lookup plus Python evaluation." It is a real custom
logic engine, with all the usual hard parts surfacing in the tests.

### 3. Indexing Is Useful But Overstated In Some Docs

`src/aether/space/index.py` maintains:

- `by_head`
- `by_arity`
- `by_position`

But the general `InvertedIndex.candidates()` path mostly uses variable/all,
atom head lookup, and expression head plus arity. It does not generally plan a
query by intersecting multiple positional indexes. `by_position` exists and is
used through helpers like `facts_by_head_and_arg()` and by PLN/Atlas-style
lookups, but the main resolver is closer to:

> head/arity-filtered candidate lookup plus binding-set joins

than:

> full database-style positional index planning

That distinction matters because several docs imply "constrain first" as if the
current engine already does optimal index intersections. The current
implementation is directionally aligned with that idea, but not all the way
there.

### 4. Rewriter And Builtins

`src/aether/engine/rewriter.py` is the other core. It handles rewrite
strategies, builtin reduction, special forms, and simplification.

One concrete correction to the docs: the SymbolicMath protocol is not what
handles ordinary `+`, `-`, `*`, comparisons, `and`, `or`, `not`, `if`, and
similar forms. Core builtin reduction handles those. `SymbolicMathProtocol`
handles `sym-*` heads like `sym-simplify`, `sym-solve`, `sym-diff`,
`sym-integrate`, and `sym-expand`.

This reinforces the broader point: AETHER computes internally, then delegates
specialized domains through protocols.

## Protocols

The protocol layer is clean and important:

- `src/aether/protocols/base.py`
- `src/aether/protocols/registry.py`
- `src/aether/protocols/router.py`
- `src/aether/protocols/validation.py`

Each protocol owns explicit heads and receives expressions through a common
`validate()` / `evaluate()` contract. The registry enforces that every handled
head starts with the protocol name plus `-`, and blocks reserved builtin heads.

I would describe the real model as "head ownership" more than "prefix
ownership." Multiple protocol instances can share a `name` with disjoint heads;
that pattern is used by the CLAW agent-skill protocols.

The router supports nested protocol expressions by resolving arguments
inner-to-outer. The main limitation is that `_resolve_args()` takes `results[0]`
for each protocol subexpression. So if a protocol returns multiple candidate
results, nested composition does not produce a cross-product of possibilities.
This is fine for many demos, but it is a real limit for symbolic/probabilistic
composition.

The existing protocols reveal the intended shape:

- Graph uses NetworkX for graph traversal/centrality-style questions.
- SMT uses Z3 for assertions, solving, and proving.
- Symbolic math uses SymPy, but only under `sym-*`.
- PLN stores and derives uncertain beliefs.
- Temporal gives interval/window semantics used by Atlas API demos.

## PLN

The PLN docs are mostly aligned with the code. The strongest implementation
ideas are:

- beliefs are represented as `(pln-belief <concept> <strength> <confidence>)`
- confidence is treated as evidence count rather than as a second probability
- formulas propagate uncertainty using delta-method approximations
- evidence stamps prevent some forms of circular/overlapping evidence
- derived beliefs can be written back into the Space

One stale-doc correction: `docs/AETHER_PLN_GUIDE.md` has older roadmap language
around conjunction/disjunction, but code now implements and exposes `pln-and`
and `pln-or`.

The PLN protocol itself scans facts in several places. That is acceptable at
current sizes, but if PLN becomes a high-throughput subsystem, the index
integration will need the same attention as `Space` query planning.

## Atlas / Sky Governance

I agree with Claude's notes that Atlas is not a side quest. It is the central
applied target, and it has clearly driven resolver fixes.

But I would frame Atlas in two layers:

1. Core Atlas library space: `src/aether/atlas/overview.py` loads the default
   file list with LKIF, roles, rules, enforcement, deontic translations,
   scenario data, dense scenario data, and LKIF crosschecks.
2. API/product Atlas space: `services/api/app/adapters/aether/datasets/atlas.py`
   starts from the core loader, then adds governance multisig data, invariant
   catalogue data, registers graph/PLN/SMT/temporal protocols, and loads
   temporal crosschecks.

That means "Atlas" is not one fixed Space in practice. The product-facing Atlas
is richer than the default library loader.

Things I found important:

- `data/lkif_core.aether` is a 525-fact legal ontology substrate.
- `data/atlas_lkif_bridge.aether` explicitly says LKIF is a structural template,
  not normative external authority.
- Atlas has 32 roles and 9 constraints as stable baseline counts in tests.
- The bridge and crosscheck data encode contradictions, gaps, and
  recommendations as editor-assistant findings.
- `src/aether/atlas/verification.py` implements an invariant verifier for
  proposed edits, even though the `data/atlas_invariants.aether` header still
  contains older "not yet implemented" language.
- Tests lock in baseline invariant behavior: 14 invariants, with an intentionally
  non-trivial fail/pass pattern on dense scenario data.

Atlas also documents resolver limits better than the abstract docs do:

- `atlas_lkif_bridge.aether` avoids a general transitive closure rule because
  recursive closure over bare facts still fails.
- `bridge_classifications_for()` manually iterates known classes because the
  resolver cannot enumerate `(lkif__is-a <entity> $cls)` in the desired reverse
  direction.
- `atlas_invariants.aether` wraps invariant queries as rules because bare
  conjunction queries can hit QR-010's variable-name-sensitive hang.
- `atlas_rules.aether` still has a QR-008 TODO comment even though QR-008 is
  marked fixed in the ticket doc. That looks stale, not necessarily a current
  failure.

This makes Atlas valuable in a specific way: it is not just proving that AETHER
can answer governance questions. It is exposing the exact places where the
resolver still needs database/Datalog maturity.

## RSI

There are two RSI tracks.

### Rule Author

`src/aether/rsi/rule_author.py` is an async ReAct-style loop using LiteLLM. It
can:

- fork a Space
- add a candidate rule
- run queries
- diff bindings
- run a regression suite
- inspect findings/improvements
- promote or discard staging changes

The staging layer in `src/aether/rsi/staging.py` is simple and pragmatic. It
forks facts/rules/beliefs, shares protocol objects, promotes additively, and
rolls back if promotion partially fails.

The important robustness pattern is that the final answer is reconciled against
actual tool state. The LLM does not get to merely claim that it promoted a rule.

### Protocol Author

`src/aether/rsi/protocol_author.py` and `src/aether/rsi/protocols.py` add a
narrow source-mutation path. The agent can draft a Python protocol adapter in a
staging directory, verify that it defines exactly one `Protocol` subclass,
register it in a forked Space, run a test query, and then promote the file into
`src/aether/protocols`.

That is more than pure rule self-modification. It is source writing, but bounded
to protocol adapters.

The caveat is security. The draft verifier parses imports and blocks obvious
dangerous modules (`os`, `subprocess`, `socket`, `requests`, etc.), and there
are tests for traversal/clobbering/symlink safety. Still, candidate code is
imported in-process during verification. That is not a malicious-code sandbox.
It is a product/prototype safety boundary.

## CLAW

CLAW is more central than the README makes it sound.

`src/aether/claw/loop.py` runs a ReAct-style agent loop, but the interesting
part is that conversation state, tool calls, errors, thresholds, session data,
skill metadata, and stop conditions are pushed into a `Space`. The loop then
queries rules/protocols to decide behavior.

Important files:

- `src/aether/claw/claw_space.py`
- `src/aether/claw/claw_query.py`
- `src/aether/claw/loop.py`
- `src/aether/claw/learning.py`
- `src/aether/claw/policy_rules.py`
- `src/aether/claw/layer1/query.py`
- `src/aether/claw/layer1/authoring.py`

The closed-loop learning test is persuasive: two runs fail in the same way,
observations are emitted into a persistent LearningSpace, a policy is derived,
and the third run changes behavior without a code/config change.

That is the "agent substrate" story in miniature:

```text
agent run -> facts -> learned policy -> projected into next run -> different outcome
```

Caveat: skill permissions (`SAFE`, `WORKSPACE`, `SYSTEM`) are currently
declarative/observable. The code comments say enforcement is later work.

## API And Web Product

The product surface is extensive enough that it should be treated as part of
the architecture:

- `services/api/app/adapters/aether/adapter.py` is the async boundary around the
  blocking in-process core.
- Dataset plugins load Spaces and register protocols.
- SpaceManager caches loaded Spaces with per-dataset locks.
- RSI routes expose both blocking and SSE streaming endpoints.
- The web workbench has dataset selection, rule/protocol mode, presets,
  featured scenarios, cancellation, traces, and status refresh.

One detail I liked: the web SSE hook aborts in-flight RSI runs on unmount and
distinguishes user cancellation from other aborts. That is not core reasoning,
but it shows the system is being built as a usable tool, not only a paper demo.

## Where I Agree And Disagree With Claude's Notes

I agree with the big picture:

- Atlas is the flagship applied testbed.
- CLAW is a surprise relative to the README and is important.
- The repository is not just a library; it is a full research/product stack.
- The RSI roadmap matters because the system is trying to reason about and
  improve itself.
- The docs are numerous and some are more like engineering journals than final
  specs.

My main corrections:

1. I would not say AETHER is mainly a "manager distributing tasks to experts."
   Protocols fit that metaphor, but `Space` and the rewriter are themselves a
   substantial reasoning engine.

2. I would qualify claims about O(1) variable lookup. The main resolver does
   not generally use the positional index as a full query planner. It mostly
   uses head/arity filtering plus binding joins.

3. I would qualify "protocols chain across protocols." They do, but nested
   protocol composition currently takes the first result from each protocol
   subexpression, so it is not full nondeterministic composition.

4. I would distinguish core Atlas from API Atlas. The API plugin loads extra
   multisig, invariant, temporal, and protocol machinery that the default
   `load_atlas_space()` does not include.

5. I would not treat L4 source rewriting as entirely future. General source RSI
   is future, but the protocol-author path already writes promoted Python files
   into the protocol package.

6. I would avoid exact global test-count claims. I saw 269 files under `tests`,
   while `pyproject.toml` intentionally excludes integration, smoke, CLAW,
   ingest, generated, and migration tests from the default run.

7. I would be cautious about docs as ground truth. `AETHER_QUERY_RESOLUTION_`
   architecture docs contain historical roadmap language, while ticket docs and
   tests show several of those items are now fixed. Some data-file TODOs also
   appear stale.

8. I would correct the SymbolicMath story. Ordinary arithmetic is a core
   rewriter builtin; the SymPy protocol is `sym-*`.

## Sharp Edges And Risks

The biggest technical risks I see:

- Query planning is still ad hoc. The resolver is much better than a naive
  rewriter, but it is not yet a cost-based Datalog engine.
- Recursive/transitive closure remains weak, especially over bare facts.
- There are still Atlas workarounds for reverse class enumeration and bare
  conjunction hangs.
- Protocol composition is shallow in multi-result cases.
- Several protocols scan all facts. That is acceptable now, but it is not the
  long-term scaling shape.
- RSI protocol authoring imports untrusted candidate code in-process.
- CLAW permission levels are not enforcement yet.
- Docs freshness is uneven, so a reader can easily confuse completed tickets,
  stale TODOs, design intent, and current behavior.
- The local dev environment matters. This repo expects Python >=3.10; Python
  3.9 fails before even running examples.

## What I Would Do Next

If I were continuing the exploration or preparing a technical roadmap, I would
focus on these threads:

1. Make the query planner honest and measurable.
   - Use positional indexes in candidate planning where possible.
   - Add explicit join ordering.
   - Track when the engine falls back to scans or residuals.

2. Resolve QR-009 and QR-010 cleanly.
   - Transitive closure over bare facts is core for ontologies.
   - Bare conjunction query hangs are dangerous because time limits not being
     honored is a reliability problem, not only an expressiveness problem.

3. Clarify protocol composition semantics.
   - Decide whether multi-result protocol args should produce cross-products,
     streams, ranked top-k, or require explicit aggregation.

4. Harden protocol-author sandboxing.
   - Import deny-lists are not enough for adversarial code.
   - A subprocess/container boundary would match the threat model better.

5. Split docs into "current behavior" and "design log."
   - The repo has valuable ticket archaeology, but new readers need canonical
     current-state docs that do not mix stale roadmap with shipped code.

6. Treat CLAW as a first-class AETHER consumer.
   - CLAW is proving that AETHER facts can govern an agent loop, not just answer
     static KB queries. That may be more strategically important than yet
     another protocol demo.

## Bottom Line

My revised hypothesis after the repo pass:

AETHER is a practical attempt to make agent reasoning inspectable and editable
by forcing more of the system into S-expressions: domain facts, rules, beliefs,
protocol boundaries, agent traces, learned policies, and self-improvement
proposals.

The current implementation is strongest when the query shapes are head-keyed,
rule-wrapped, and Atlas-style. It is weaker when asked to behave like a general
Datalog database with recursive closure, reverse enumeration, and arbitrary bare
conjunctions. That is not a fatal flaw; it is exactly where the next engineering
work is visible.

I would summarize the project as:

> AETHER is not just a MeTTa replacement and not just a Python library router.
> It is a symbolic control plane for agent systems, with a real but still
> maturing query engine at its core.

