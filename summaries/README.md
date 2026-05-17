# Laniakea Summaries — Big-Picture Mode Entry

You are most likely an LLM at session start. Two work modes exist:

- **Big-picture mode** (Laniakea-wide thinking — cross-cutting design, "how does this affect X elsewhere"): you're in the right place. Read this file plus every summary in the Index below (parallel `Read` calls, single message — don't delegate to a background agent). That's your default loaded context.
- **Focused mode** (phase execution — getting shit done on P1 / P2 / etc.): close this dir, start at `../roadstart/README.md` instead. Load only `roadstart/` + `roadmap/` (no external dependencies — roadmap carries lean P1-scoped versions of the four risk-framework detail files it binds to); skip the summaries.

If unsure which mode the task wants, ask.

## Design intent

Three layers:

1. **Repo root `README.md`** — high-level pitch + directory map.
2. **`summaries/` (here)** — one summary per active subdirectory; orientation layer.
3. **Detail files** (everything else) — pure reference: formulas, atom shapes, worked examples. Paged in surgically when a question demands depth.

Detail files carry **no orientation** — no TL;DRs, no "what this dir is about" intros, no status banners. That's this layer's job. **Per-directory `README.md` files do not exist and should not be created** — they would duplicate the summaries and waste tokens. The one exception is `roadstart/README.md`, which serves the same entry-point function for focused mode that this file serves for big-picture mode. If you find a README anywhere else, it's a bug.

Every byte in a detail file should be reference content the summary couldn't carry; every byte in a summary should be orientation the detail files don't need to repeat.

## Index

| Summary | Status |
|---|---|
| [core-concepts](core-concepts.md) | live |
| [macrosynomics](macrosynomics.md) | mixed |
| [synodoxics](synodoxics.md) | mostly target |
| [neurosymbolic](neurosymbolic.md) | target |
| [synoteleonomics](synoteleonomics.md) | mostly target |
| [noemar-synlang](noemar-synlang.md) | mostly target |
| [risk-framework](risk-framework.md) | target + P1 live |
| [accounting](accounting.md) | mixed / P1 DSC live |
| [smart-contracts](smart-contracts.md) | mixed |
| [sentinel](sentinel.md) | mostly target |
| [synomic-entities](synomic-entities.md) | mixed / P1 topology current |
| [governance](governance.md) | mostly target |
| [growth-staking](growth-staking.md) | speculative |
| [roadmap](roadmap.md) | live P1 orientation |

Each summary ends in a `## File map` listing every detail file in its directory and what each adds beyond the summary. Use that as the entry to detail files; don't grep first.

## When adding or changing content

- **Framing / orientation** → summary file. Never in detail files.
- **Specific formula, parameter table, worked example, atom shape, edge case** → detail file. Update the summary's section pointer and File map row if the doc shape changes.
- **New concept used in 2+ dirs or 4+ docs** → graduate to `core-concepts/`.
- **Numeric parameter, name, or status changing** → search the corpus and update everywhere it's quoted. There is no canonical source-of-truth designation yet (tracked in `clean-todo.md`).
- **Never create `dir/README.md`** — the summary in this directory is the entry point for that dir.

## Naming work is open

Naming conventions (Space sigils, class taxonomies, instance identifiers, operational prefixes) evolved piecemeal and need a fractal first-principles pass. When you hit a naming-shape question mid-task, **flag it** rather than resolving locally. See `clean-todo.md` §1.

## Files in this directory

- `README.md` — this file
- 14 summary files (see Index)
- `clean-todo.md` — deferred-cleanup register
