# E1-v2 broader material cleanup

Control A is the frozen E0 120x112 B00 source. The approved close-up remains the
authority; the 1024x1536 cutout is supporting-only because its partial-alpha
extraction halo and specks make it unsuitable as a clean production source.

Candidate B is reproducible existing-palette material mapping: 384 olive-range
opaque 01-jacket pixels map to a five-colour olive ramp and 8 warm-light opaque
02-shirt pixels map to a three-colour cream ramp. Face, eyes/brows, mouth, all
hair/tie layers, neck/ear, alpha, canvas, frame count and palette are excluded.

mapping-report.json retains the warnings-first rule and exact ramp policy. The first
review sheet is source-control-candidate.png. It shows a visibly flatter, more
coherent jacket material treatment at 4x; this is a comparison, not an automatic
promotion or user approval.

final-comparison.png is the final source/control/candidate sheet with actual 1x,
4x nearest-neighbour, and the 392-pixel change mask. change-ledger.json records
every old/new pixel, layer, coordinate and deterministic rule. The ledger was
extracted after the mapping run; it is evidence, not a pre-run diagnostic. The
mapping report's warnings-first language means only that mapping is not automatic
erase/fill, not that the ledger was preselected by lint.

Both raw-strict-check.json and normalized-strict-check.json pass with 384 allowed
jacket and 8 allowed shirt pixels, zero protected changes, and unchanged native
metadata. outputs/candidate-normalized-reopened.png is the fresh reopen export.
artifact-manifest.json freezes the produced artifacts. At 1x no unambiguous visual
win is claimed; the tradeoff is a flatter, more regular jacket treatment that may
lose some source-derived depth. Control A remains the safe baseline pending review.
