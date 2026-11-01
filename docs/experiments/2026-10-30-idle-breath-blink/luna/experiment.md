# Experiment: Luna6 idle breath and blink

- Status: observed — corrective pass01 retained for user review; visual approval is pending.
- Date: 2026-10-30.
- Question: does a restrained chest/shoulder garment expansion and brief asymmetric blink read as an idle loop while preserving the exact neutral character and stance?
- Relevant guides: [style guide](../../../../art/style-guide.md), [motion guide](../../../../art/motion-guide.md), [asset contract](../../../../art/asset-contract.md); current working-tree documents, no version tag.
- Baseline and last proven artifact: [exact Luna6 neutral source](../../../2026-10-30-expression-strip/luna/passes/luna6-neutral.aseprite), SHA-256 `d76266fa8afcd1de643e6b6421ec4dfe4fa77f8044a1d083205b921eb2f25540`; current candidate is [corrective pass01](passes/pass01/luna6-idle-breath-blink-pass01.aseprite), SHA-256 `d5b9d7675de8bea50a1941361d3e3bed3c187b3ee7e1d7e0585d51f8d37cc8ed`. Pass 0 remains preserved at [its native source](passes/luna6-idle-breath-blink.aseprite), SHA-256 `79c4ebc3df6f2d0c6d621d4c68329e075a10a8def7a9649463b312105d55221e`.
- Scope and completion criterion: one 2–4 second, review-only native loop with feet/denim fixed, no face bob, no new pose/outfit/weapon, brief eye closure and clean garment coverage; save, freshly reopen, inspect and export actual frames/GIF. Do not treat as production art or approval.
- Tools, versions, permissions and budget: dedicated headless Aseprite AI Artist MCP; Aseprite 1.3.18.6-dev, extension 0.8.2; bounded initial construction and up to two correction rounds after Sol critique; no additional paid budget was requested or used.
- Intent: end-to-end native animation pilot for review, not engine integration.
- Controlled and changed variables: exact neutral baseline, same canvas/palette/layers/pose. Pass01 replaces pass0's ineffective shirt-fold speck with staged 1px shirt-opening and jacket-shoulder deformation on F2–F4; the registered eye edits on F5–F7 are unchanged. Whole-cel torso movement was tried, rejected for coverage defects, and reverted. No attribution beyond these candidate revisions is claimed.
- Target contract/reference intake: 128×192 RGB, baseline 255-entry palette; approved identity/stance reference [scene](../../../2026-10-30-expression-strip/luna/inputs/character-scene.png) and face/expression reference [close-up](../../../2026-10-30-expression-strip/luna/inputs/character-closeup.png). Standing full-body view, existing olive jacket/pale shirt/wide denim/cream tote, fixed feet and head. No new style or pose inferred from the older idle experiment.
- Recipe/seed: deterministic native edits to the exact baseline; no image-generation seed. Fresh baseline export is [here](reviews/baseline-fresh.png).
- Defining feature priorities and correction locks: preserve face, fringe, body volume, stance, outfit, tote and shoes; no transparency gaps. Full-cel `07-face-and-neck` motion was rejected by native auto-review and left untouched.
- Face/expression registration: open-eye baseline detail owner is `08-hair-tie-and-hair`; allowed eye masks are `[62,20,67,24)` and `[70,20,73,22)`. The y19 fringe is protected. Any pixels outside those masks must remain exact.
- Actual visible owner/frame/cel readback: F1 neutral; F2/F4 expand the `03-shirt` opening and jacket shoulder edges partially; F3 uses the fuller expansion; F5/F6/F7 retain the registered eye detail on `08-hair-tie-and-hair`; F5–F8 return to the rest body shape.

## Plan

Pass01 is independently observable as native filmstrip and timed loop GIF. The remaining uncertainty is whether the staged shirt/shoulder expansion reads as breathing at 1× without distorting the outfit. Sol review is defects-only and does not edit the asset. One of at most two bounded correction rounds has been used; Luna can make at most one further round if the parent relays concrete findings.

## Artifacts

- Native source: [luna6-idle-breath-blink.aseprite](passes/luna6-idle-breath-blink.aseprite)
- Native Aseprite timed GIF: [luna6-idle-breath-blink.gif](exports/luna6-idle-breath-blink.gif)
- 3× neutral-matte playback preview: [idle-neutral-3x-preview.gif](exports/idle-neutral-3x-preview.gif)
- Transparent PNG strip: [idle-transparent-strip.png](exports/idle-transparent-strip.png)
- Frame PNGs: `exports/frame-0.png` through `exports/frame-7.png`
- Contact sheet: [contact-sheet-neutral-3x.png](proof/contact-sheet-neutral-3x.png)
- Fresh-reopen exports and mechanical metrics: `proof/reopened-0.png` through `proof/reopened-7.png`; [frame-metrics.json](proof/frame-metrics.json)
- Operation/rejection/correction record: [first-pass-log.md](operations/first-pass-log.md); proof-rendering script: [render_proof.py](operations/render_proof.py)
- Corrective pass01: [native source](passes/pass01/luna6-idle-breath-blink-pass01.aseprite), [native Aseprite GIF](exports/pass01/luna6-idle-breath-blink-pass01.gif), 8 frame PNGs `exports/pass01/frame-0.png`–`frame-7.png`, [neutral-matte preview](exports/pass01/idle-neutral-3x-preview.gif), [transparent strip](exports/pass01/idle-transparent-strip.png), [contact sheet](proof/pass01/contact-sheet-neutral-3x.png), [fresh-reopen metrics](proof/pass01/frame-metrics.json).
- Correction details: [correction-round-1.md](operations/correction-round-1.md); fresh-reopen flattened exports are `proof/pass01/reopened-0.png`–`reopened-7.png`.

## Observations

| Check | Method and target | Observed result | Evidence path |
| --- | --- | --- | --- |
| Style at game scale | Review full character at native size and nearest-neighbor enlargement | Pass01 silhouette, outfit and stance remain consistent; gameplay-scale engine view not run; Sol readability/contour review pending | `proof/pass01/contact-sheet-neutral-3x.png` |
| Source structure | Freshly reopen native source; inspect dimensions, palette baseline, layers, frames and tag | 128×192 RGB; 8 frames; 12 original layers/order/visibility; 255-entry palette established on baseline and no palette operation used; infinite `idle` tag | `proof/pass01/frame-metrics.json`, this folder's `task-profile.md` |
| Character/weapon consistency | Compare against approved scene and close-up | No weapon or pose added; only local shirt/chest and shoulder edges deform; feet, denim and head identity are preserved by per-layer comparisons | `proof/pass01/contact-sheet-neutral-3x.png`, `proof/pass01/frame-metrics.json` |
| Contact and timing | Read actual native GIF metadata and durations | Loop=0; exact 600/350/550/600/50/80/50/250ms sequence; total 2,530ms; no contact/action pose in scope | `proof/frame-metrics.json` |
| Localized art revision | Compare all native frames and head-layer exports against F1 | Pass01 body differences 11/24/11 pixels on F2/F3/F4, all in chest/shoulder bounds x39–88/y42–56; 13/26/13 eye pixels on F5/F6/F7; zero lost alpha and no changes outside the registered body/eye masks | `proof/pass01/frame-metrics.json` |
| Timing revision | Existing first-pass timing retained | Not run | — |

## Pass and selection ledger

| Checkpoint/native/export identity | Observed defect or change hypothesis | Technical result | Original/seed/best/new evidence and visual decision | Selected baseline/reason |
| --- | --- | --- | --- | --- |
| Pass 0; source hash `79c4ebc…d55221e`; 8 frames; 2.53s | Fold highlight was too subtle to read as breathing at 1× | Preserved; blink and structural checks pass | Sol rejected the breath gate. [Pass 0 contact sheet](proof/contact-sheet-neutral-3x.png), [metrics](proof/frame-metrics.json), [operation log](operations/first-pass-log.md) | Kept as history; superseded for current review by pass01. |
| Corrective pass01; source hash `d5b9d76…d37cc8ed`; 8 frames; 2.53s | Staged shirt/chest and shoulder expansion reviewed for breath read and contour | Native source reopens; all final PNG exports match fresh-reopen exports; zero alpha loss/out-of-mask edits; fixed-layer and eye-mask checks pass | Sol reviewed pass01 read-only and retained it for user review; parent independently confirmed GIF timing/loop. [Pass01 contact sheet](proof/pass01/contact-sheet-neutral-3x.png), [metrics](proof/pass01/frame-metrics.json), [correction record](operations/correction-round-1.md) | Selected for user review; original neutral and pass0 remain untouched. Not approved for production. |

**Review provenance:** Sol reviewed pass0 read-only and rejected the breath gate, then reviewed pass01 read-only and retained it for user review. The parent independently confirmed the final GIF timing/loop. User visual approval is still pending; no editor's review is treated as approval.

**Selection summary:** Pass01 is retained as the user-review candidate; pass0 is preserved as the rejected breath attempt. No version is user-approved. Remaining work belongs to the user: visual approval or concrete feedback. No further art edit is pending.

## User feedback

No visual approval has been received for this version.

## Decision and continuation

- Continue if the user requests a revision or supplies a concrete breath/readability concern.
- Reason and remaining uncertainty: pass01 was retained by Sol, but user visual approval remains separate; no gameplay-engine validation was requested.
- Usage consumed/remaining: one corrective round was used; no further correction is pending.
- Last proven state: pass01 source saved, freshly reopened and closed; 8-frame exports and infinite timing verified; original neutral and pass0 hashes unchanged.
- Smallest next action and next owner: user reviews the loop GIF and gives approval or concrete feedback.
