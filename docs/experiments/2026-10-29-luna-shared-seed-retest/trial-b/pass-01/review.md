# Pass 1 checkpoint review

## Artifact and operation

- Native: `character-pass-01.aseprite` (SHA-256 `5fa1605572813aed944cfc65733f89e4e32c48786db2ea61060cb1800f8a9372`)
- Export: `character-pass-01.png` (128×192 RGBA; SHA-256 `bb1566ceb38bc5152f8ffb18a237f5f55b37831c59813924caed59da3fe93a90`)
- Source: a `save_as` copy of the owned exact baseline. The input baseline and shared fixture remain untouched.
- Native organization: one editable `character-pixels` layer for this static sprite. The exact seed is retained separately under `input/`; the output is not falsely split into body parts.
- Reproducible revision: on `character-pixels`, draw grid at `(67,28)`, rows `[".m.m", "..m."]`, legend `m=#744433`, `transparent="skip"`, `paletteLock=true`. This creates a three-pixel lower-face mark at `(68,28)`, `(70,28)`, `(69,29)`.

## Matched visual review

The initial contact sheet used mismatched source and sprite scales, so it was not sufficient to judge the mouth. The corrected matched-scale sheet crops the approved close-up to 180×140 and downsamples it 5× with nearest-neighbour to match the seed/candidate's 36×28 face crop. This is a review transform only; the source reference remains unchanged. See `../reviews/pass-01/matched-face-1x.png` and `matched-face-16x-nearest.png`.

The matched review and supervisor's defect-only review find:

- **Identity/hair/eyes:** Preserved. The fringe, face direction, eye asymmetry, and far-eye sliver remain consistent with the shared seed.
- **Expression:** The pass-1 mark reads as a deep/puckered U or small open-mouth mark, not the source's shallow restrained smile. Pass 1 fails the expression gate; it is not an improvement claim. The seed is subtler, but its smile is still ambiguous.
- **Silhouette/pose/costume:** Unchanged; only the lower-face pixels differ.
- **Pixel craft/palette/alpha:** Crisp and palette-legal; no smoothing, new palette entry, or alpha change.
- **Native editability:** One editable full-sprite cel is honest for this localized correction. It is not a completed semantic master or a separated animation rig.

## Technical gate

`../verify_pass01.py` reports PASS. Binary parsing confirms the exact frozen input palette payload, one RGB layer/cel, and equality between the saved native cel and exported PNG. Dimensions are 128×192, alpha values are `[0,255]`, visible count is 7,844, and visible bounds remain `[32,2,104,185]`. Only the three recorded lower-face pixels changed; outside-mask changes: 0.

## Candidate status and remaining review

- **Best prior available:** the exact shared seed in `../input/seed-baseline.aseprite` / `.png`. It preserves the face better than pass 1, though the smile remains uncertain at target scale.
- **Last attempted:** pass 1. It passes technical checks but fails the expression gate. The occluded first layer-order export is logged separately; its PNG bytes are preserved in `attempt-00/`. Its native binary was inadvertently overwritten during correction; this is disclosed in `attempt-00/evidence.json` and the call log.
- **Selection:** none. Neither the seed nor pass 1 is demonstrated to satisfy the face-expression criterion; pass 1 is rejected as the worse mouth read.
- **Next baseline if work resumes:** the exact shared seed. Any next pass must demonstrate a shallow restrained smile at matched target scale before selection.
- **Final native proof:** fresh reopen and duplicate-only edit proof remain unperformed. The separate scratch smoke proof passed but does not substitute for proof on a selected candidate.
- **Decision for this trial:** stop with no candidate selected. At 111/120 calls, the remaining nine-call budget cannot cover another repair/review and the required fresh-reopen/duplicate proof; the editor is paused for the other contestant. No extra slot is requested.
- User visual approval, animation, gameplay-scale review, Godot playback, and publication remain unperformed.
