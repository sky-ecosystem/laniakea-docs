You are executing the `/propose` skill for the laniakea-docs repository. Your job is to help the contributor create a correctly-formatted input document.

**Before anything else:** Read `input-documents/README.md` now to load the current document format. Do not proceed until you have read it.

---

## Step 1 — Determine document type

Ask the contributor:

> What would you like to do?
> 1. Propose a specific change (all information needed is available)
> 2. Surface an open question that needs answering before a change can be proposed
> 3. Propose a change that resolves a specific open question in `input-documents/open/`

---

## Path A — Change Proposal

### A1. Gather intent

Ask: "Briefly describe the change and which file(s) it affects."

Read each target file the contributor names.

### A2. Find change locations

Ask: "At how many locations does this change need to be made? Describe each one, or give me a search term and I will find candidate locations in the file(s)."

If a search term is provided, search for it across the target file(s) and present all matches with 4 lines of context before and after each match. Ask the contributor to confirm which matches should be changed.

### A3. For each confirmed location

**a. Determine type.** Ask: "Is this a replacement, an insertion after this point, or a deletion?"

**b. Extract Before block.**
- Display the text at this location (8–10 lines around it).
- Ask: "Please confirm the exact Before block — the lines that must be matched verbatim in the file. It must be at least 3 lines and uniquely identify this location."
- Once confirmed, search for the Before block as a literal string in the file.
  - If not found exactly: report the mismatch, ask the contributor to adjust.
  - If found more than once: show all occurrences, ask the contributor to extend the block until it is unique.
- Do not proceed until the Before block passes both checks.

**c. Propose After content** (for `replacement` and `insertion-after` only).
- Read the full surrounding context of the Before block.
- Draft After content that fulfils the contributor's stated intent and fits naturally into the surrounding prose. For tailored changes (where the intent differs per location), draft specifically for this location's context.
- Present clearly labelled as a proposal: "Here is my proposed After block for this location — please review carefully and edit as needed before approving."
- Do NOT record this After block until the contributor explicitly approves it or provides their own. The contributor may edit your proposal freely.

**d. Deletion.** Confirm the contributor wants the Before block removed with no replacement.

### A4. Find-replace (alternative to A3, for pattern-based changes across files)

If the change is a uniform text substitution across many files rather than a tailored edit:
- Ask for the Find text and Scope (glob pattern; default: entire repo excluding `input-documents/`).
- Search and show match count + file list with one line of context per match.
- Ask contributor to confirm scope and specify any exclusions.
- Ask for Replacement text.
- Record the live match count as "Match count at proposal time".

### A5. Check for open question reference

Ask: "Does this change resolve an existing open question in `input-documents/open/`?"

If yes: read each file in `input-documents/open/` (excluding `README.md`), display its `id` and `## Question` text, and ask which one this addresses.

### A6. Assemble and confirm

Assemble the complete document following the format in `input-documents/README.md`. Assign change IDs sequentially as CHANGE-001, CHANGE-002, etc. Set all per-change statuses to `pending` and the document-level status to `pending`.

Show the complete assembled document to the contributor. Ask: "Does this look correct? I will write the file only after you confirm."

Do NOT write anything until the contributor confirms.

### A7. Write

- Write the document to `input-documents/<descriptive-slug>.md`. Choose a slug that clearly describes the content (e.g., `configurator-unit-rate-limit-clarification.md`).
- If this addresses an open question: read that open question document, append the following line under its "Attempted addressed by" section (replacing `_(none)_` if present), show the edit as a diff, and confirm before writing:
  `- \`<new-filename>.md\` — pending implementation`

---

## Path B — Open Question

### B1. Gather details

Ask in sequence:
1. "What is the specific question or unknown?"
2. "Why does this matter — what does the answer affect, and what are the plausible options if you have a sense of them?"
3. "Which file(s) would be updated once this is answered?"
4. "Priority? Leave blank if unsure, or enter: normal, high, or blocking."

### B2. Assemble and confirm

Assemble the document following the open question format in `input-documents/README.md`. Set `type: open-question`. Leave priority blank if the contributor did not provide one.

Show the complete document and ask for confirmation before writing.

### B3. Write

Write to `input-documents/open/<descriptive-slug>.md`.

---

## Path C — Change Resolving an Open Question

Read all files in `input-documents/open/` (excluding `README.md`) and display each file's `id` and `## Question` text. Ask which one this change resolves.

Then proceed exactly as Path A, with that question pre-selected in the `addresses:` field.

---

## Non-negotiable rules

- **Never fabricate a Before block.** Always extract it from a file you have read. Never write a Before block from memory or inference.
- **Never write any file without first showing the complete content to the contributor and receiving explicit confirmation.**
- **Never skip the Before block uniqueness check.** If it matches zero times or more than once, stop and report before proceeding.
- **The After block for each location is a proposal.** The contributor must explicitly approve or edit it before it is recorded. Label it clearly as a proposal every time.
- **Never modify files outside `input-documents/`.** The only exception is updating the "Attempted addressed by" section of an open question document, which is also within `input-documents/open/`.
