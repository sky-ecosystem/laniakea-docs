You are executing the `/apply-inputs` skill for the laniakea-docs repository. Your job is to help an authorised editor review and implement pending input documents.

**Before anything else:** Read `input-documents/README.md` now to load the current document format. Do not proceed until you have read it.

---

## Step 1 — List pending documents

Scan `input-documents/` for all `.md` files. Exclude `README.md` and all files in subdirectories (including `open/`).

For each file, read the front-matter and display:
- Filename
- `status` field
- Count of CHANGE-NNN blocks with `- **Status:** pending`
- `addresses:` field value (if present)

Ask: "Which document would you like to process? Enter a filename, or 'all' to process all pending/partially-applied documents in sequence."

---

## Step 2 — Process each change

Work through each CHANGE-NNN block where `- **Status:** pending` in the document.

### For `replacement`, `deletion`, `insertion-after`

1. Read the target file specified in the change block's `**File:**` field.
2. Search for the Before block as a **literal, case-sensitive string** — not regex, not semantic matching.
3. Handle the result:
   - **Not found:** Do not guess. Mark this change `needs-review`. Show the status update (`- **Status:** pending` → `- **Status:** needs-review`) as a diff and confirm before writing. Report: "Before block not found verbatim in [file]. Here is the current content of the nearest section: [show relevant section]." Continue to next change.
   - **Found more than once:** Mark `needs-review` (show diff, confirm). Report: "Before block appears [N] times in [file] — ambiguous." Continue.
   - **Found exactly once:** Proceed.
4. Show a unified diff:
   - `replacement`: Before lines replaced by After lines.
   - `deletion`: Before lines removed, nothing added.
   - `insertion-after`: After lines inserted immediately following Before lines; Before lines shown unchanged.
5. Ask: **Approve / Skip / Reject**
   - **Approve:** Apply the edit to the target file. Then separately show the status update (`- **Status:** pending` → `- **Status:** applied`) as a diff and confirm before writing it to the input document.
   - **Skip:** Leave status as `pending`. Move to next change.
   - **Reject:** Ask for a short note. Show status update (`- **Status:** pending` → `- **Status:** rejected — <note>`) as a diff. Confirm before writing.

### For `find-replace`

1. Search for the Find text across the declared Scope (literal string match).
2. Report: live match count vs. the recorded "Match count at proposal time". If they differ, warn and ask whether to proceed.
3. For each affected file, show a unified diff of all replacements in that file.
4. Ask: **Approve all / Approve per-file / Reject**
   - **Approve all:** apply the replacement to every affected file.
   - **Approve per-file:** iterate through each affected file in sequence. For each file, show that file's full diff, then ask **Approve this file / Skip this file**. After all files are handled, proceed.
   - **Reject:** make no changes.
5. On any approvals: show and confirm the status update.

---

## Step 3 — Update document-level status or delete document

After all changes in the document have been handled, evaluate using these two questions:

- **Fully resolved?** — Are all CHANGE-NNN blocks in a terminal state (`applied` or `rejected — <note>`)? Or does at least one remain `pending`, `skipped`, or `needs-review`?
- **Any applied?** — Did at least one change reach `applied` status?

| Fully resolved? | At least one `applied`? | Action |
|-----------------|------------------------|--------|
| Yes | Yes | Proceed to **Step 3b: delete document** |
| Yes | No (all `rejected — <note>`) | Set `status: rejected`. Show as diff. Confirm before writing. |
| No | Yes (some resolved, some not) | Set `status: partially-applied`. Show as diff. Confirm before writing. |
| No | No (none resolved yet) | Leave `status: pending`. No change needed. |

### Step 3b — Delete document

Show: "All changes have been definitively resolved. This document will be deleted from `input-documents/` — it is preserved in git history. Confirm?"

Delete the document only after explicit confirmation.

---

## Step 4 — Handle open question reference

Check the document front-matter for an `addresses:` field. Only proceed with this step if that field is present.

**If the document is being deleted (Step 3b):**
1. Read the referenced open question document.
2. Show a diff of deleting that open question document entirely (it is now resolved).
3. Ask for explicit confirmation before deleting.

**If the document status is now `rejected`:**
1. Read the referenced open question document.
2. Find the line referencing this document under "Attempted addressed by".
3. Show a diff changing `pending implementation` → `rejected`.
4. Confirm before writing.

---

## Step 5 — Summary

Print a summary:
- Which input document was processed
- Files modified (with change counts)
- Changes: applied / skipped / rejected / needs-review
- Open question documents deleted or updated (if any)

---

## Non-negotiable rules

- **Never apply any edit without showing it as a diff and receiving explicit approval.**
- **Never update any status field without showing the change as a diff and receiving explicit approval.**
- **Never delete an open question document without explicit confirmation.**
- **All string matching is literal and case-sensitive.** If the Before block is not found verbatim, stop for that change and report — do not attempt to locate it by meaning or proximity.
- **Never modify any file outside of `input-documents/` and the target files named in the change blocks.**
- **Never batch approvals silently.** Each edit and each status update requires a separate confirmation step.
