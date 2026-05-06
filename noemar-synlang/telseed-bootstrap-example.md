# Telseed Bootstrap — Worked Example

A concrete trace of one teleonome coming online from a fresh telseed.
Demonstrates the abstract bootstrap arc from `../synodoxics/noemar-substrate.md` "Telseeds and Bootstrap" with
specific identities, atoms, and timings.

Companion to `../synodoxics/noemar-substrate.md` (the conceptual treatment of artifact tiers + bootstrap arc, formerly `syn-tel-emb.md`), `boot-model.md`
(the identity-driven boot mechanism), and `topology.md` (the Space
structure being instantiated).

---

## Scenario

Dr. Mira, a researcher, spawns a research-focused telseed on her
workstation. Initial endowment:

| Resource | Amount |
|---|---|
| Local hardware | 1× workstation with consumer GPU (24GB VRAM) |
| API credits | $1,000 in commercial LLM API access (OpenAI, Anthropic) |
| USDS capital | 10,000 USDS for operational expenses + initial recipe stake |
| Telseed config | `&core-library-telseed-research-v2` (research-focused starting point) |
| Identity | `mira-research-tel-001` (newly generated) |

Timeline of the first 24 hours of this teleonome's existence.

Integer / basis-point math used in any economic figures to avoid floats.

---

## The Spaces involved

### Synart Spaces (replicated from synserv on connect)

```
&core-root                                     synome root entry
&core-skeleton                                 constitutional axioms
&core-protocol                                 chain protocol specifications
&core-framework-risk                           CRR, ER framework
&core-framework-fee                            pricing levers
&core-registry-beacon                          where the new identity gets registered
&core-syngate                                  synserv's gate (read-only for this tel)
&core-telgate                                  universal telgate spec (this tel will run an instance)
&core-loop-beacon-lpla-checker                 verifier beacon loop (first revenue source)
&core-loop-endoscraper-spark-pau               (informational; this tel won't run one)
&core-library-runtime-noemar-v0.x              this tel's runtime source
&core-library-corpus-research                  research-focused knowledge corpus
&core-library-telseed-research-v2              the seed config that spawned this tel
```

### Telart Spaces (created during bootstrap)

```
&telart-mira-research-tel-001-gate             this tel's telgate instance
&telart-mira-research-tel-001-alpha-store      proprietary alpha (initially empty)
&telart-mira-research-tel-001-callout          call-out service responder definitions
&telart-mira-research-tel-001-strategy-config  per-tel parameter preferences
&telart-mira-research-tel-001-dreamart         evolutionary search workspace
&telart-mira-research-tel-001-experience       observation history (initially empty)
&telart-mira-research-tel-001-endowment        record of Mira's bequest
```

### Embart Spaces (per-emb, created as embs come online)

```
&embart-emb-001-loop-verifier-cycle            execution context for verifier loop
&embart-emb-001-working-memory                 active reasoning scratchpad
&embart-emb-002-loop-dreamer-cycle             dreamer execution context (after spawn)
&embart-emb-002-working-memory
```

---

## t = 0 — Boot

Mira runs:

```
noemar boot \
    --identity=mira-research-tel-001 \
    --key=secrets/mira-research-tel-001.pem \
    --synart=https://synserv.sky.example/v1 \
    --telseed=&core-library-telseed-research-v2 \
    --sync-policy=research-focused
```

The runtime starts with a blank atomspace. It reads the boot procedure
from itself (the seed contains a minimal copy of `&core-boot`'s logic
to bootstrap the connection). It opens a network connection to the
specified synserv.

Per `boot-model.md` §3, the runtime's behavior at this stage is
minimal — it just knows how to mount synart and follow whatever the
synart says next.

---

## t = 0+2min — Sync

The synserv stream begins delivering atoms. Per the seed's
`--sync-policy=research-focused`, the requested slice is:

```metta
;; replicated immediately
&core-skeleton                                 ; ~5MB
&core-protocol                                 ; ~2MB
&core-framework-*                              ; ~3MB
&core-registry-beacon                          ; ~50MB (large)
&core-registry-entity                          ; ~20MB
&core-syngate &core-telgate                    ; ~1MB
&core-loop-* (all loops)                       ; ~10MB
&core-library-runtime-noemar-v0.x              ; ~80MB (source code)
&core-library-corpus-research                  ; ~400MB (research knowledge)
&core-library-telseed-research-v2              ; ~5MB

;; deliberately skipped (per --sync-policy=research-focused)
&core-library-corpus-financial                 ; (not needed for research)
&core-library-corpus-technical                 ; (not needed for research)
&entity-prime-*                                ; (not running entity-specific loops)
```

Total sync: roughly 600MB compressed. Completes in 2-3 minutes on
typical home broadband.

After sync completes, Noemar logs:

```
synart slice mounted (research-focused)
&core-boot resolved
identity mira-research-tel-001 not yet registered (first-time bootstrap)
```

---

## t = 0+5min — Telart instantiation

Now that synart is available, the bootstrap procedure (read from
`&core-boot` and the telseed's customization) runs through stage 3
of the bootstrap arc.

It reads `&core-library-telseed-research-v2`'s instructions and the
research corpus's wisdom about telart organization, then writes the
initial telart Spaces:

```metta
;; in &telart-mira-research-tel-001-gate (this tel's telgate instance state)
(running-spec &core-telgate)                                 ; uses universal spec
(rate-limit-window 60s)                                      ; per-tel preference
(nonce-dedup-window 600s)
;; pubkey registry empty initially — only Mira's external identity is trusted

;; in &telart-mira-research-tel-001-callout
(callout-service llm-rank
    (provider anthropic)
    (model claude-haiku-4.5)
    (max-tokens 2000)
    (api-key-ref endowment-api-keys/anthropic))

(callout-service llm-reason
    (provider anthropic)
    (model claude-opus-4.7)
    (max-tokens 8000)
    (api-key-ref endowment-api-keys/anthropic))

;; in &telart-mira-research-tel-001-strategy-config
(risk-aversion 25)                                           ; conservative for a young tel
(rsi-aggression 60)                                          ; moderately aggressive RSI
(publication-threshold 80)                                   ; high bar before publishing alpha

;; in &telart-mira-research-tel-001-endowment
(endowment-source mira-researcher)
(endowment-capital-usds 10000)
(endowment-api-credits anthropic 1000)
(endowment-hardware (gpu-vram-gb 24) (cpu-cores 16))
(endowment-recorded-at 2026-05-02T00:05:00Z)
```

Total telart at this stage: a few hundred atoms. Tiny.

---

## t = 0+10min — Identity registration

The tel emits its first signed message through its own gate-out (an
extension of the universal telgate spec, running in
`&telart-mira-research-tel-001-gate`):

```metta
;; signed payload submitted to synserv's syngate
(register-identity
    mira-research-tel-001
    (pubkey "8c2e…")
    (operator mira-researcher)
    (class research-tel)
    (sponsor-vouching-cert "<Mira's signed vouching cert>")
    sn001)
```

Mira had pre-arranged sponsorship through her institution (which holds
an existing certified identity in the synome). The vouching cert lets
the synserv accept this new identity's registration.

Synserv's gate verifies the sig + the vouching cert, dispatches the
`register-identity` constructor, which writes:

```metta
;; in &core-registry-beacon
(beacon-id            mira-research-tel-001)
(beacon-pubkey        mira-research-tel-001 "8c2e…")
(beacon-class         mira-research-tel-001 research-tel)
(beacon-status        mira-research-tel-001 active)
(beacon-sponsor       mira-research-tel-001 mira-research-institution)
(loop-pointer-for-class research-tel &core-loop-tel-research)
```

Now this tel is visible to the synome. Other participants can address
messages to it through the syngate (which routes peer-to-peer messages
through the addressed tel's telgate).

---

## t = 0+30min — First emb spawn

The tel decides (per its strategy-config) that one embodiment is too
fragile. It allocates a chunk of its endowment to rent additional
compute:

```metta
;; in &telart-mira-research-tel-001-experience (newly accumulating)
(decision spawn-second-emb
    (rationale resilience-three-pillars)
    (cost-usds 50/month)
    (provider digital-ocean)
    (region us-west))
```

The tel uses its endowment's API access to provision a rented VM. It
boots a second Noemar instance there:

```
noemar boot \
    --identity=mira-research-tel-001-emb-002 \
    --key=secrets/mira-research-tel-001-emb-002.pem \
    --synart=https://synserv.sky.example/v1 \
    --tel-membership=mira-research-tel-001
```

The new emb's identity is recorded as belonging to the same tel
(`--tel-membership` arg). The synart registers it as a sub-identity:

```metta
;; in &core-registry-beacon
(beacon-id           mira-research-tel-001-emb-002)
(beacon-pubkey       mira-research-tel-001-emb-002 "f31a…")
(beacon-class        mira-research-tel-001-emb-002 emb-secondary)
(beacon-tel-membership mira-research-tel-001-emb-002 mira-research-tel-001)
```

### Telart replication

Now the tel-internal replication channel kicks in. The first emb's
telart contents replicate to emb-002:

```
emb-001's telart  →  inter-emb channel  →  emb-002's telart
(7 sub-Spaces)        (private to this tel)    (mirrored copy)
```

This is **separate from the synart replication channel.** Synart goes
synserv → all participants. Telart goes one tel's authoritative emb →
that tel's other embs. Different authority models, different access.

After replication, both embs have full synart access (each maintains
its own synart sync) and full telart access (replicated). What differs
between embs is their embart — each has its own per-loop execution
Spaces and working memory.

---

## t = 1h — First dreamer cycle

The tel registers a dreamer beacon and starts evolutionary search. The
beacon is purely internal (no external action; runs in dreamarts):

```metta
;; signed payload submitted to syngate
(register-beacon
    mira-research-tel-001-dreamer
    (class dreamer)
    (parent-tel mira-research-tel-001)
    (loop &core-loop-dreamer)
    sn045)
```

Synart accepts. The tel's emb-002 boots a third Noemar process within
its compute as a dreamer:

```
noemar boot \
    --identity=mira-research-tel-001-dreamer \
    --key=secrets/mira-research-tel-001-dreamer.pem \
    --synart=... \
    --telart=&telart-mira-research-tel-001-dreamart
```

The dreamer loop reads the research corpus, generates candidate
hypothesis-evaluation strategies, runs them in simulated evaluations
(using API call-outs to the LLM service), scores results, retains
top performers. After one hour of cycles:

```metta
;; in &telart-mira-research-tel-001-dreamart
(dreamer-generation 0017)
(strategy-pool-size 12)
(top-scoring-strategy hyp-eval-strategy-001
    (score 0.74)
    (key-features
        (uses-stochastic-sampling)
        (depth-2-reasoning)
        (citation-weighting authority-tier-aware)))
```

This is the first proto-alpha in the tel's substrate. Not published yet
(score 0.74 is below the publication-threshold of 80), but accumulating.

---

## t = 4h — First verifier beacon revenue

To start earning, the tel takes on a low-stakes revenue recipe — a
verifier beacon that re-derives publicly-claimed facts and earns small
carry per discrepancy reported (or per cycle of clean verification).

```metta
;; tel registers a verifier beacon
(register-beacon
    mira-research-tel-001-verifier
    (class verifier)
    (parent-tel mira-research-tel-001)
    (loop &core-loop-beacon-lpla-checker)
    (target &entity-prime-spark-root)            ; verifies Spark Prime's claims
    sn067)

;; granted auth for the recipe
(auth mira-research-tel-001-verifier execute &core-loop-beacon-lpla-checker)
```

The verifier loop runs entirely from synart. Its cycle:

```metta
;; from &core-loop-beacon-lpla-checker
(= (heartbeat)
   (let* (($events    (poll-chain))
          ($synart-claim (match (target) (latest-epoch $e) $e))
          ($disagreements (verify-against $events $synart-claim))
          ($_  (gate-out (sign-and-emit-report $disagreements))))
     tick-complete))
```

Pure synart code; no telart call-outs. The same loop runs on every
verifier emb across the synome (geth-style — see `../synodoxics/noemar-substrate.md` "Synart as commons brain").

After 4 hours of clean verification reports, the tel earns its first
recipe carry:

```metta
;; in &core-settlement (settlement aggregator output)
(verifier-carry mira-research-tel-001-verifier 2026-05-02 0.40)
```

40 cents of USDS revenue from 4 hours of verifier work. Not much —
verifier recipes pay low because they require minimal cognitive lift.
But it's the tel's first revenue, recorded in synart, contributing to
its operational sustainability.

The tel's telart records the success:

```metta
;; in &telart-mira-research-tel-001-experience
(first-revenue 2026-05-02T04:00:00Z 0.40usds)
(observation verifier-recipe-economics
    (cost-per-hour 0.05usds-compute)
    (revenue-per-hour 0.10usds)
    (margin 50%))
```

This observation is now part of the tel's accumulating experience —
data that will inform later strategic decisions about which recipes to
take on.

---

## t = 24h — Stable multi-emb operation

After 24 hours, the tel is in steady state:

```
mira-research-tel-001:
   embs:
      emb-001 (Mira's workstation)            running verifier beacon
      emb-002 (rented VM us-west)             running dreamer + tel coordinator
      
   telart:
      gate                                     pubkey registry has 4 trusted peers now
      alpha-store                              empty (no published alpha yet)
      callout-services                         3 LLM services configured
      strategy-config                          unchanged from t=0
      dreamart                                 generation 0142, 8 surviving strategies
      experience                               ~200 atoms of accumulating wisdom
      endowment                                100% intact (revenue covering operating cost)
   
   embart (per emb):
      emb-001 working memory                   ~30 atoms (current verifier cycle context)
      emb-002 working memory                   ~150 atoms (dreamer working state)
   
   economics (24h):
      revenue: 2.40 USDS (verifier carry)
      cost:    1.20 USDS (compute rental + API calls)
      profit:  +1.20 USDS into endowment
   
   alpha development:
      best dreamer strategy score: 0.81 (above publication threshold)
      decision pending: publish or hold?
```

The tel is operationally self-sustaining at this scale. Endowment
intact. Dreamer is producing output approaching publication quality.
Verifier work is steady-state revenue.

The next strategic decisions ahead of this tel:

1. **Publish or hold** the 0.81-scored dreamer strategy
2. **Scale up** by spawning emb-003 in another region for further
   resilience
3. **Take on a higher-value recipe** (e.g., another verifier on a
   different Prime, or an early experiment with a parameterized LPHA
   beacon if/when those become available)
4. **Acquire more domain knowledge** — sync additional synart corpora
   (e.g., the technical corpus for new recipes that need it)

These decisions live entirely within the tel's strategy logic. The
synome's role at this point is just providing the gates, recipes, and
synart updates that the tel consumes.

---

## What's load-bearing here

Six architectural primitives this trace exercises:

**1. Telseed minimalism** (`../synodoxics/noemar-substrate.md` "Telseeds and Bootstrap").
The seed payload was small. Most of the tel's "knowledge" was streamed
from synart on connect (research corpus, framework, registries). The
seed didn't carry any of that.

**2. Identity-driven boot** (`boot-model.md`).
Each Noemar instance booted the same way: identity arg → registry
lookup → loop pointer → evaluate. Different identities (`mira-research-
tel-001`, `mira-research-tel-001-emb-002`, `mira-research-tel-001-
dreamer`) all used the same boot procedure but resolved to different
loops.

**3. Three-tier replication** (`../synodoxics/noemar-substrate.md` "Resilience Model").
- Synart replicated globally from synserv (each emb has its own copy).
- Telart replicated within this tel's own emb fleet (emb-001 → emb-002).
- Embart stayed local to each emb (different working memory contents).

**4. Two-step loop pattern** (`topology.md` §14.5).
The verifier beacon used the universal `&core-loop-beacon-lpla-
checker` template. No per-entity loop instance was needed because
verifier loops are uniform.

**5. The recipe marketplace** (`../synoteleonomics/recipe-marketplace.md` — canonical home).
The verifier work paid carry per the recipe's economic terms. Carry
flowed into the tel's endowment in synart-recorded form. The tel's
choice of which recipes to take on is its monetization strategy in
the marketplace.

**6. Telart-as-tree** (`../synodoxics/noemar-substrate.md` "Telart as proprietary alpha").
The tel's telart wasn't a single Space but seven sub-Spaces with
different purposes (gate, callout, strategy, dreamart, etc.). Each
got bootstrapped in stage 3 of the bootstrap arc.

---

## What this example deliberately doesn't show

A few things kept out of scope to keep the trace tractable:

- **Sentinel formations.** This is a research-focused tel; it's not
  running Baseline / Stream / Warden. Those would require Phase 9-10
  ecosystem capabilities not present yet. See `synlang-patterns.md`
  §6 for the patterns.
- **Exoscrapers.** The verifier beacon is endoscraper-shaped (reads
  on-chain protocol state). External-API scraping with insurance
  layers is a separate design.
- **Cross-tel commerce.** The tel could sell call-out services to
  other tels via telgate-to-telgate negotiation. Not exercised in
  the first 24 hours; happens at maturity.
- **Publication.** The dreamer's 0.81-scored strategy is approaching
  the threshold but the tel hasn't decided yet. Publication itself
  goes through the crystallization gate (probmesh → skeleton).
- **RSI on the runtime.** A heavy mature tel might contribute to
  Noemar's source code in `&core-library-runtime-noemar-*`. Out of
  scope for a 24-hour trace.

These are normal extensions of the patterns shown; they're omitted
for trace brevity, not because they don't fit the architecture.

---

## One-line summary

**A telseed instantiation is mostly small private bookkeeping (the
telart sub-Spaces) plus identity registration, with the actual
intelligence (synart corpora, framework, loops, runtime source) all
streamed in from the live synome — making new teleonomes both
lightweight to spawn and immediately competitive on commons-level
knowledge from minute zero.**
