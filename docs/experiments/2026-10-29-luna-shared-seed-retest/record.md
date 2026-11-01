# Shared sharp-seed retest preparation

- Date: 29 October 2026.
- Status: shared fixture and controlled briefing ready; contestant art passes are not run by this preparation.
- Question: can the requested Luna profiles be compared on one identical, user-preferred sharp pixel-route starting point without carrying prior corrective artwork into either trial?

## Frozen common input

The common source is the exact full-canvas `converted-seed` layer at index zero of
the prior trial A `pass-01.aseprite`, extracted with the read-only
[extractor](shared/extract_source_seed.py). The same named layer in `pass-02.aseprite`
has identical decoded RGBA and raw-cel SHA-256. The extraction includes no overlay,
face correction, semantic-layer copy, raster patch, or correction script. Native
layer provenance demonstrates which source layer was used; the historic record is the
evidence that that layer was source-derived.

| Property | Observed value |
| --- | --- |
| Canvas / cel | 128×192 / `[0,0,128,192]` |
| Visible pixels / RGB colors | 7,844 / 254 |
| Alpha policy | Binary `{0,255}` |
| Decoded RGBA and source cel SHA-256 | `8839680f1bc70c1c99653a28c76c6f8ea41f401d2755c93146d765523cb5806c` |
| Ordered native palette | 255 entries including transparent index zero; chunk SHA-256 `f2d4907a7493af8e6557f933e3c2c40d73f733658fc8250d925f79678ffb5b81` |
| Deterministic extracted PNG | [source-only-converted-seed.png](shared/source-only-converted-seed.png), file SHA-256 `074168d9bfc5b2a2f2751810152bb0c31a71e7027a5368c0b393e17449fb84eb` |

The original raw FFmpeg alpha-clean seed remains a different preparation (3,572
visible colors); it was not substituted. The historical final export's reported 253
visible colors is also not the base measurement. The controlled base is 254 visible
RGB colors, as measured above.

## Minimal native baseline

Using the authorized headless dedicated Aseprite MCP only, the extracted PNG was
opened, its already-imported 255-entry palette inspected, its sole layer renamed
`shared-source-seed`, then saved as
[shared-source-seed-baseline.aseprite](shared/shared-source-seed-baseline.aseprite).
This was mechanical fixture assembly, not art construction. Aseprite 1.3.18.6-dev /
extension 0.8.2 reported ready; no mode switch, UI, Lua, direct CLI, image generation,
or prior correction asset was used. The document was exported, closed, reopened, and
exported again before the editor document was closed.

The native source has one frame and one editable full seed layer. Its exact ordered
palette, decoded pixels, dimensions, and binary alpha match the extracted PNG. Both
baseline exports decode equal to the source seed; their byte-identical PNG SHA-256 is
`7353611071482ea1e879ab9c247fb1d92c7bd90050b8eb99cbec4cdbdf612d12`.

## Controlled packet

[fixture.json](shared/fixture.json) freezes source, fixture, reference, palette,
workflow, and brief hashes. [trial-context.md](shared/trial-context.md) supplies a
neutral scoped context that preserves project obligations while deliberately excluding
prior trial operations, correction coordinates, and outcomes. The parent-authored
[common brief](BRIEF.md) holds the equal budgets and review loop.

## Checks and evidence boundary

`python3 shared/verify_shared_fixture.py` passed: it decoded all three PNGs with a
standard-library reader and compared them with both the old native source layer and
the new native fixture; it also compared ordered native palette entries. The persisted
result is [shared-fixture-checks.json](shared/shared-fixture-checks.json).
`git diff --check`, JSON parsing for `fixture.json`, and canonical skill-symlink
discovery passed. The bundled runtime Python (Pillow 12.3.0) ran all 32 existing
pixel-director unit tests successfully. The default `python3` lacks Pillow, so the
bundled runtime was intentionally used; no dependency was installed. A 4× MCP preview
was inspected only to confirm the shared source was readable; it is not an
art-quality approval.

## Not performed / next owner

No contestant artwork, local correction, model assessment, animation, Godot playback,
user artistic approval, commit, push, publication, or production promotion occurred.
The parent orchestrator may now copy the same frozen fixture into both assigned trial
directories, verify copy hashes before drawing, and serialize their editor slots.

## Independent generic-routing review

Independent reviewer `reference_generalization_sol61` found no issue with the applied
generic routing clarification: a soft-painted nonhuman sprite first follows the neutral
intake; an explicitly crisp low-resolution pixel target reaches the director after its
target contract; the face/grid examples remain conditional; and the illustrated/rigged/
action validation matrix is discoverable from CONTEXT and handoff. This is a
documentation-routing observation, not art validation. Frozen workflow, brief, and
fixture files were not changed after the trial packet was prepared.
