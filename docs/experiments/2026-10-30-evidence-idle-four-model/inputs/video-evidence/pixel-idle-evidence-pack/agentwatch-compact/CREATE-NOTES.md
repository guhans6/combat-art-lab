# Create a Video Knowledge Pack

This package contains deterministic source evidence for one video. Create a
portable, evidence-grounded **Video Knowledge Pack** from the evidence that is
actually available here. AgentWatch does not author the notes.
AgentWatch does not send this package to a chat or guarantee that a receiving
application accepts a folder or ZIP. It can structurally validate and package a
returned typed draft, but it does not author or semantically grade the notes.

## Pinned package context

- Package ID: `pkg-27f82cd7-dcb1-4305-a5dd-278495b4c140`
- Source ID: `src-c946289c8fc1ff74faf4fbc0`
- Run ID: `run-685706ba8c60b1e15f47126ff98be675f978cf4d084c31ad4f4e1a70a3821ede`

For a typed return draft, read immutable `package.json` and copy its exact
`package_id`, `package_payload_sha256`, and `source_content_sha256` values into
the draft's `source` object. Do not compute a hash for `CREATE-NOTES.md`: the
package payload pin is recorded in `package.json`, avoiding a self-hash cycle.

## Typed draft scaffold

Before authoring or freezing a typed raw candidate, create a separate author
workspace with the public command:

```text
video-context knowledge-pack init-draft PACKAGE_DIR --output AUTHOR_WORK_DIR
```

`AUTHOR_WORK_DIR` must not already exist and must be outside this immutable
package. The command creates `draft.json`, `intake-receipt.json`, and a local
README. It copies exact source pins, official-code IDs, and receipt record IDs
and hashes from this package, but it does not inspect source material, write
semantic content, or claim grounding. Keep the generated official-code ID rows:
fill their blank `disposition` and `text` values rather than inventing IDs or
renaming `text` to `explanation`. When `evidence-index.json` supplies chapter
metadata, keep and complete the generated chapter rows using exactly
`visual_claim` with supported selected frame IDs, or `unavailable` with an
empty frame list and a truthful nonempty reason. The scaffold omits chapter
rows when metadata is absent; do not fabricate chapters.

The generated receipt starts with every record at `pending`. After truthful
inspection, change only each receipt record's `status` to `inspected`; preserve
its source pins, record IDs, hashes, and record count. `available`,
`unreadable`, and `pending` are honest states but do not pass the required
intake gate. The scaffold does not reserve or create a finalization destination:
choose a distinct, nonexistent `--output` path only when finalizing. This
typed-workspace procedure is optional for the manual Markdown fallback below.

Read `EVIDENCE-TIMELINE.md` and `evidence-index.json` before writing notes. When
`text_evidence.ocr.primary_text_path` is included, read the complete compact
primary OCR at `ocr/OCR-TEXT.md` in sequential groups of no more than
10 OCR records per read. Record each group's first and last frame ID in the
coverage section before continuing. Use `ocr/OCR-READABLE.md` only when a
material detail requires its detailed regions. `ocr/frame-ocr.raw.jsonl` is
the companion source-record sidecar; it preserves each complete nested OCR
object and is not the default reading path:

```json
{"frame_id":"frame-001","absolute_seconds":12.5,"ocr":{"status":"ok","text":"...","regions":[]}}
```

When `text_evidence.apple_copy_code.availability` says included, read
`code/APPLE-COPY-CODE.md` as the readable, once-entity-decoded rendering of
official Apple Copy Code. `code/apple-copy-code.raw.jsonl` is the byte-exact
raw source-record sidecar. Do not decode the rendered code a second time,
combine code blocks, or invent source code. Inspect the labelled sheets and
supplied frames or crops needed to ground material details. Those artifacts are
sampled evidence, not proof that every moment was observed.

When official code is included, inventory every labelled official-code block
before drafting the notes. In the coverage section, record each block ID,
source time, and disposition: `quoted`, `summarized`, `omitted`, `duplicate`,
or `superseded`. Typed finalization requires every available block exactly once
in `code_dispositions`. For `quoted`, use a typed code block with the exact
`code_id`; omit `lines` to select the full source block, or use one contiguous
inclusive 1-based range. Partial ranges are visibly limited and list omitted
source lines. A non-quoted disposition requires a nonempty reason; duplicate
and superseded entries also identify their distinct target code ID. The strict
`--require-full-code` policy accepts only full typed rendering of every
available block. Exact source-selected code proves excerpt integrity, not the
semantic correctness of prose or selection.

When completeness accounting is requested, add one `code_explanations` entry
for every available official-code ID. Explain purpose and behavior, including
conditionals, nontrivial formulas, special cases, and concurrency boundaries
where the supplied source supports them; mark uncertainty rather than inventing
intent. Add one `chapter_dispositions` entry for every exported chapter. Use
`visual_claim` only with unique typed visual frame IDs whose exported
`chapter_membership` is `assigned` to that chapter. Membership is derived from
the frame's decoded source PTS, not the requested seek time. For older packages
without this field, finalization falls back to the exported temporal interval.
An explicit `no_chapters` membership means the source supplied an empty chapter
list, while `unavailable` means chapter metadata was not supplied. Use
`unavailable` with an empty frame list and a nonempty reason when
a meaningful visual chronology cannot be supported. This is structural
accounting, not a benchmark answer or an automatic understanding grade.

## Required recorded intake

This package's `INTAKE-MANIFEST.json` is the exact inventory for typed
finalization. The scaffold-generated `intake-receipt.json` carries one record
for every manifest ID with its exact hash. Only `inspected` completes required coverage.
`available`, `unreadable`, and `pending` are honest statuses, but they do not
waive a required source record. Do not add, skip, omit, or mark a record not
applicable to bypass coverage. Keep an `attempts` list for any self-validation
before first submission. The receipt is a recorded author assertion; it does
not prove that an external tool opened or displayed an artifact, or that anyone
understood it. Validate before return with:

```text
video-context knowledge-pack validate PACKAGE_DIR DRAFT_JSON --intake-receipt RECEIPT_JSON
```

## Source-to-draft reconciliation

Before writing final prose, turn each bounded source chunk you read into one or
more atomic propositions, then reconcile those propositions with the draft.
Keep this external-author working record outside this immutable package and
outside the typed JSON draft. It is a working aid, not source evidence, a
delivery receipt, proof that another application opened an asset, proof of
comprehension, or an AgentWatch semantic grade.

Use this inline external draft reconciliation record for every bounded source
chunk. Fill its source type/path, exact IDs/time, and bounded excerpt from the
source you actually read; do not replace missing or partial source with a
completed row.

| Source type and package path | Exact IDs/time and bounded excerpt | Atomic proposition | Draft location | Reconciliation |
| --- | --- | --- | --- | --- |
| `<transcript, OCR, official code, frame, or chapter path>` | `<exact evidence/frame/code IDs, source time or interval, bounded excerpt or direct observation>` | `<one source-supported fact, condition, relationship, or uncertainty>` | `<section/heading/block, or not yet drafted>` | `<retained, corrected, or omitted>; reason; unresolved question if any` |

For each bounded source chunk, record propositions before relying on them in
the notes. Reconcile execution order, branch conditions, concurrency causes,
chapters, actions, and resources when the available source supports them. If
records conflict, re-read the raw source record or asset and preserve the
conflict or uncertainty if it remains. When carrying a proposition across note
contexts, mark the later use as direct or inherited from a prior cited record,
and preserve the reconciliation ledger across revisions. Do not place this
table, source excerpts, timestamps, or evidence IDs in the typed JSON draft;
this reconciliation record stays outside the typed JSON draft.

`CITATION-MANIFEST.json` is the deterministic binding for every supplied
native frame: frame ID, evidence ID, displayed source time, decoded source PTS,
and exact package-local path. Use `VISUAL-OBSERVATIONS.md` as an
external-author working record. Open one native image per tool call and, while
it is visible, replace only its observation placeholder with a bounded direct
observation or `unreadable`. This ledger is not AgentWatch source evidence.
Synthesize direct visual claims only from the matching ledger row. Keep each
factual clause atomic for attribution. When a sentence combines a direct visual
observation with transcript, OCR, or official-code context, split it into
separately attributed clauses and identify the supporting source type for each.
Do not use a visual citation to support information only present in transcript,
OCR, or official code.

## Evidence access checklist

Before writing notes, check `evidence-index.json` and record which of the
transcript, OCR, and Apple Copy Code paths are accessible in the receiving
environment. Treat `absent` and `partial` availability as limitations, not as
empty content. Verify that every citation you use names a supplied evidence or
frame ID and source time. If an asset cannot be opened, say that it was not
available to you; do not claim that you read or inspected a file merely because
this package contains it.

In the notes' coverage section, log each actually inspected visual asset with
its exact package path, source time, and frame or evidence ID, plus the visible
text or content used for the claim. Record the actual file, time range, and
frame or evidence ID reviewed; a record count, file listing, or batch display
order is not review coverage. While using the chronological guide, verify the
cited asset before writing a visual claim. Do not infer visual detail from an
adjacent frame, transcript text, or batch display order.

Before completing an initial knowledge pack, account for every manifest row in
the visual-observation ledger with zero observation placeholders and record
each supplied contact sheet that was inspected. Include meaningful
chronological visual events when the supplied frames support them, carrying
their matching ledger citations into the notes. Do not substitute a
transcript-only timeline or generic ledger summary for material visible code,
formulas, diagrams, UI, or other on-screen changes.

Keep the timeline chronological and include meaningful visual events only where
the supplied frames support them. Direct visual observations require the
matching typed `visual` block and a selected frame ID. Transcript, OCR, and
official-code claims are different source types; do not relabel them as direct
visual observations or infer unobserved visual detail from them.

For manual Markdown delivery only, keep each direct visual claim's normal
Markdown link package-relative to the final portable notes root and append the
exact `video-context:visual-citation` record copied from the matching ledger
row. Never abbreviate an evidence ID or asset path, and never combine an ID,
time, or path from different rows. This manual Markdown rule does not apply to
the typed JSON return below.

## Create the current notes now

Produce a useful R0 knowledge pack now; do not wait for a possible follow-up.
The preferred portable folder contains:

- `README.md` or `overview.md` for navigation;
- `timeline.md` with timestamped sections spanning the source duration and
  every available chapter or meaningful interval;
- optional `topics/*.md` only when the video has substantial topical structure;
- a coverage, uncertainty, and unresolved requests section; and
- local assets linked with standard relative Markdown links using the exact
  package-local asset path recorded in `evidence-index.json`.

For every material claim, cite the source timestamp and stable evidence or
frame ID. Distinguish direct visual observations, transcript text, OCR text,
and inferences. Preserve exact readable technical, code, slide, and UI detail
when the linked evidence supports it. Mark unreadable text, sampled or
unobserved intervals, conflicts, and unknowns instead of filling them in.
Do not infer transient actions, continuous motion, or exact code from a sparse
sheet or an insufficiently readable image.

If a folder or ZIP cannot be created, return one complete, copyable `timeline.md`
with the same timestamps, evidence citations, relative links where available,
and limitations. That fallback is still useful knowledge notes; it is not an
AgentWatch extraction failure.

## Optional typed finalization return

To let AgentWatch validate structure and produce a portable derived package,
return one UTF-8 JSON file with this exact top-level schema:

```json
{
  "schema_version": "video-context.knowledge-draft.v1",
  "source": {
    "package_id": "<package.json package_id>",
    "package_payload_sha256": "<package.json package_payload_sha256>",
    "source_content_sha256": "<package.json source_content_sha256>"
  },
  "title": "Author title",
  "sections": [
    {
      "heading": "00:12 — source-backed detail",
      "blocks": [
        {"type": "prose", "text": "Author prose."},
        {"type": "visual", "text": "Bounded directly observed statement.", "frame_id": "<frame ID>"},
        {"type": "code", "code_id": "<official code ID>"}
      ]
    }
  ],
  "code_dispositions": [
    {"code_id": "<official code ID>", "disposition": "quoted"}
  ],
  "code_explanations": [
    {"code_id": "<official code ID>", "text": "Purpose and source-bound behavior."}
  ],
  "chapter_dispositions": [
    {"chapter_id": "<exported chapter ID>", "disposition": "visual_claim", "frame_ids": ["<typed visual frame ID>"]}
  ],
  "limitations": ["Sampled or unobserved intervals remain limited."]
}
```

Select typed frame and code IDs from the immutable package records. Do not put
asset paths, evidence IDs, timestamps, hashes, Markdown citations, author code
text, language metadata, or exactness claims in typed blocks: finalization
resolves those from the source package. Use `{"lines": [first, last]}` only on
a code block when intentionally selecting a partial contiguous range; omitted
`lines` means the whole available block. Do not place fenced code or native
frame Markdown links, HTML, or copied visual-citation records in JSON text.
For a typed `visual` block, select `frame_id` only; the renderer adds its
canonical link and citation record. The finalizer retains the raw JSON bytes,
generates citations and exact code mechanically, and reports structural
coverage and explicit limitations. It does not establish semantic faithfulness,
meaningful observation quality, or complete understanding.

The finalized package keeps this immutable Compact package below `source/`.
Generated canonical frame and code links therefore begin with `source/` (for
example, `source/frames/...`). Its root contains generated `NOTES.md`,
`validation-report.json`, the raw author draft, and finalization controls.

## Ask for more evidence only when needed

If a bounded visual evidence gap matters, fill in the supplied
`follow-up.awreq` template with one or more source-linked gaps.
Keep that request separate from the notes. The user manually submits it to
AgentWatch, reviews the deterministic preview, and explicitly approves any
fulfillment. AgentWatch does not automatically contact this conversation.

## Return for a revision

When the user brings a follow-up delta back, use its complete copyable
`FOLLOW-UP.md` and cumulative evidence index in this same conversation. Keep
one current readable notes set and preserve earlier versions plus a
source-linked change report. Retain earlier supported facts and code in the
current notes, or explicitly identify each evidence-backed correction,
withdrawal, or relocation. Where a retained detail is supported by a linked
current transcription rather than a later directly shown image, say so.
