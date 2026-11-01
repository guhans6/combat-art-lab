# Revise a Video Knowledge Pack

This follow-up delta adds source-linked evidence to a previously delivered
Video Evidence Pack. Return it manually to the same conversation that wrote
the current notes. AgentWatch does not send it to that conversation, import
the resulting notes, or grade their semantic quality.

## Pinned revision context

- Package ID: `pkg-27f82cd7-dcb1-4305-a5dd-278495b4c140`
- Source ID: `src-c946289c8fc1ff74faf4fbc0`
- Run ID: `run-685706ba8c60b1e15f47126ff98be675f978cf4d084c31ad4f4e1a70a3821ede`
- Receipt ID: `receipt-26be61fa-4307-49e1-b9ce-b5230047249a`

Read this complete `FOLLOW-UP.md`, the original `EVIDENCE-TIMELINE.md`, and the
cumulative `evidence-index.json`. Treat the new assets as additional sampled
evidence. The index preserves earlier and new evidence identities; absence of
a new asset does not make an earlier fact unsupported.

## Revise without losing grounded knowledge

Update the current readable notes using the new evidence, keeping timestamped
sections and source-linked citations. Use standard relative Markdown links only
for assets actually included in this delta or cumulative folder. For an earlier
evidence item that is recorded in the index but whose asset is not included,
cite its evidence ID and source time and state that the asset remains in the
parent package; do not invent a local relative link. Preserve earlier supported
facts, code, and visual details in the current notes. If later evidence
requires a change, explicitly record the evidence-backed correction,
withdrawal, or relocation instead of silently dropping the detail.

Keep traceable earlier versions and add a source-linked change report that
states what changed, why, and which citations support the revision. Maintain a
coverage, uncertainty, and unresolved requests section. Distinguish direct
visual observation, transcript or OCR support, inference, unreadable detail,
and sampled or unobserved intervals. Do not treat a later sample as evidence
of continuous motion or an exact onset time unless the evidence establishes it.
When a current detail is retained through linked transcription rather than a
later directly shown image, mark that distinction.

If a folder or ZIP cannot be updated, return one complete, copyable `timeline.md`
with current citations, relative links where available, the limitations section,
and the change report. The preferred portable folder may also retain `README.md`,
`overview.md`, and only useful topical files.

If another bounded gap remains, prepare a separate request using
`follow-up.awreq`. The user manually submits that request to AgentWatch and
explicitly approves any later fulfillment; no request authorizes extraction by
itself.
