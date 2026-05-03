# Notes 1 — Session handoff (2026-05-03)

What didn't make it into the formal docs from this session, captured
here so it survives a context clear. Everything else from the session
landed in commits (see below).

---

## Session checkpoints (origin/main)

| Commit | Pass |
|---|---|
| `a455947` | Ozone single-guardian topology + USGE generator naming (7 files) |
| `ff27d0f` | `listener-loops.md` sketch — in-space calculation pattern |
| `a57b97b` | `beacons.md` sketch — two-role taxonomy (input vs action) |
| `e847761` | `risk-framework/open-questions.md` — 5 deferred questions tracker |
| `6af50d0` | Stale TBD fix in `listener-loops.md` |

The 15-item punch list from this session's start is fully processed.
Nothing pending decision.

---

## Loose ends to address before rewrite begins

### 1. Keel ambiguity (real inconsistency, blocks accurate examples)

User listing was "Spark, Grove, Obex (and others coming later)".
Ozone-pass updates use Spark/Grove/Obex as example children. But:

- `CLAUDE.md` says operational set = Spark/Grove/Keel (Star Primes) +
  Obex (Institutional Prime) — 4 entities currently
- `risk-framework-redesign-2026-05-03.md` §3.1 (the v1 test scenario)
  still reads "3 Star Primes (Spark, Grove, Keel)" — left untouched in
  the Ozone pass

Most likely intent: **all four (Spark/Grove/Keel + Obex) are
accordant to Ozone**; the user's verbal listing was off-the-cuff and
not exclusive. If so, examples in `topology.md`, `syn-overview.md`,
and `risk-framework-redesign-2026-05-03.md` Part 2 + Appendix A
should be updated from `Spark/Grove/Obex` to `Spark/Grove/Keel/Obex`
(or just keep three as a representative subset and note "+ Obex /
others").

Quick clarification at session start unblocks this. ~5 min fix once
decided.

### 2. synome-extra-info.md §10 / §11 status drift

The rewrite plan in `synome-extra-info.md` was written before this
session. Some items are now done; preconditions in §11 are now met:

- §10 item 17 ("Update topology.md") — DONE (Ozone pass)
- §10 item 20 ("Update syn-overview.md, syn-tel-emb.md,
  settlement-cycle-example.md") — PARTIAL (Ozone-side updates landed;
  risk-content updates pending)
- §11 says "Resolve Q17 and items B/C/D before starting rewrite" —
  all four resolved this session

Worth a quick cleanup pass at the start of the new session: update
§10 to mark done items and §11 to note preconditions are now met.

### 3. Phase 1-2 docs are write-from-scratch

The `synome-extra-info.md` §10 plan calls for these new files in
`laniakea-docs/risk-framework/`:

- `risk-decomposition.md`
- `book-primitive.md`
- `tranching.md`
- `currency-frame.md`
- `riskbook-layer.md`
- `halobook-layer.md`
- `primebook-composition.md`
- `hedgebook.md`
- `projection-models.md`

None exist yet. The rewrite session is primarily writing these from
the substrate already in `risk-framework-redesign-2026-05-03.md` and
`synome-extra-info.md`.

---

## Working observations from this session

### Doc length preference

User explicitly cut `listener-loops.md` from a 519-line comprehensive
options enumeration to a 108-line concept sketch with implementation
deferred ("just write some available ideas but dont settle on a
particular model yet, we'll decide later when we get deep into the
implementation of the first phase").

Inference for the upcoming rewrite: prefer **tight, focused docs**
(~100-200 lines) for design surfaces with deferred decisions. Save
the comprehensive treatment for genuinely settled material (worked
examples, reference specs). When in doubt, lean shorter and
implementation-deferred.

### Decision sequence preference

User worked through the 15 open items in batches: high-impact
decisions first (Q17 → Ozone), then mechanical work (topology pass),
then sketches for the new design surfaces (listener-loops →
beacons), then the deferred-questions tracker. Each pass got its
own commit + push for revertibility.

If the rewrite proceeds the same way: largest conceptual decisions
first, then mechanical updates, then sketches for new patterns,
with commits at each natural boundary.

---

## Recommended opening sequence for the next session

1. Resolve the Keel question (loose end #1)
2. Apply the Keel decision to the affected files (topology.md,
   syn-overview.md, risk-framework-redesign-2026-05-03.md)
3. Update synome-extra-info.md §10 status markers and §11
   preconditions (loose end #2)
4. Begin Phase 1 of the rewrite plan: `risk-decomposition.md` first
   (it's the conceptual root the others specialize from)

After step 4, follow the existing §10 sequence.

---

## Files that are the substrate for the rewrite

If reading from cold start:

1. `risk-framework-redesign-2026-05-03.md` — Parts 1-8 (architectural
   primitives, test setup, Q1-Q33, future work, key insights)
2. `synome-extra-info.md` — refinements + the §10 rewrite plan
3. This doc (`notes1.md`) — handoff loose ends and observations
4. `listener-loops.md` + `beacons.md` — new sketches from this session
5. `risk-framework/open-questions.md` — deferred questions tracker
6. Existing `risk-framework/*.md` files — what's being rewritten

The new docs to write (Phase 1-2 of §10 plan) draw from #1 and #2.
