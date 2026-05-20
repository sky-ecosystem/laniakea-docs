# Input Documents

This directory collects community contributions to the Laniakea documentation.

## How to Contribute

1. **Fork this repository** and create a new branch from `main`
2. **Run `/propose`** in Claude Code to generate a correctly-formatted input document, or write one manually following the format below
3. **Submit a pull request** containing only files within `input-documents/`

PRs that touch only `input-documents/` are reviewed lightly at merge — the substantive review of each proposed change happens at implementation time when an authorised editor runs `/apply-inputs`.

## What to Include

- **Corrections** — Errors or outdated information you have identified
- **New information** — Data, parameters, or context that should be documented
- **Suggestions** — Proposed improvements or new content areas
- **Opinions** — Perspectives on design decisions or trade-offs (go in `opinions/` subfolder)
- **Open questions** — Unknowns that must be resolved before a change can be proposed (go in `open/` subfolder)

---

## Scope

Each input document should cover one coherent proposal — a set of changes that are logically connected and would be reviewed together. A single document may touch multiple related files if those changes are part of the same logical update. Independent changes should be submitted as separate documents.

---

## Change Proposal Format

Change proposal documents go directly in `input-documents/`. They contain one or more specific, ready-to-implement changes.

### Front-matter

```yaml
---
id: <short-descriptive-slug>
author: <github-username>
date: YYYY-MM-DD
status: pending                         # pending | partially-applied | rejected
targets:
  - path/to/file.md
addresses: open/<question-slug>.md      # omit if not resolving an open question
---
```

### Body

```markdown
## Summary
One paragraph describing what this changes and why.

## Changes

### CHANGE-001
- **Status:** pending
- **Type:** replacement                 # replacement | insertion-after | deletion | find-replace
- **File:** `path/to/file.md`
- **Section:** `## Section Name > ### Subsection Name`
- **Rationale:** Why this specific change is needed.

**Before** (must appear verbatim in the target file, ≥3 lines, unique within the file):
```
exact lines to match
at least three of them
unique within the file
```

**After:**
```
the replacement text
```

---

### CHANGE-002
...
```

### Change types

| Type | Before block | After block | Behaviour |
|------|-------------|-------------|-----------|
| `replacement` | Required (≥3 lines, unique) | Required | Replaces Before with After |
| `insertion-after` | Required (≥3 lines, unique) | Required | Inserts After immediately following Before; Before is unchanged |
| `deletion` | Required (≥3 lines, unique) | Omit | Removes Before block entirely |
| `find-replace` | See below | See below | Pattern search across files |

### Find-replace format

```markdown
### CHANGE-001
- **Status:** pending
- **Type:** find-replace
- **Scope:** `path/to/subtree/**/*.md`  # omit to search entire repo (excluding input-documents/)
- **Match count at proposal time:** 12
- **Rationale:** ...

**Find:**
```
text to find
```

**Replace:**
```
replacement text
```
```

### Status values per change

`pending` | `applied` | `skipped` | `rejected — <note>` | `needs-review`

---

## Open Questions Format

When a change cannot yet be proposed because information is missing or a decision is needed, submit an open question document to `input-documents/open/` instead.

### Front-matter

```yaml
---
id: <short-descriptive-slug>
author: <github-username>
date: YYYY-MM-DD
type: open-question
priority:                               # leave blank, or: normal | high | blocking
target-files:
  - path/to/relevant/file.md
---
```

### Body

```markdown
## Question
The specific unknown.

## Context
Why this matters. What the answer affects. What the plausible options are, if known.

## Attempted addressed by
_(none)_
```

When a change proposal that addresses this question is submitted, a line is appended under "Attempted addressed by":

```
- `change-doc-filename.md` — pending implementation
```

Open question documents are deleted by `/apply-inputs` once the change that addresses them is successfully applied.

---

## What Happens Next

After a PR is merged:

1. An authorised editor runs `/apply-inputs` in Claude Code
2. Each change is shown as a diff for explicit approval before anything is written
3. Changes are applied, skipped, or rejected — status is tracked in the input document
4. Once every change in a document is definitively resolved (each marked `applied` or `rejected — <note>`) and at least one was applied, the document is deleted from this folder — it is preserved in git history
5. Documents where every change was rejected are kept in this folder with `rejected` status
6. Open question documents in `open/` are deleted when the change that addresses them is fully applied
