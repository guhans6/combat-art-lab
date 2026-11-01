# Clean transparent-cutout generation attempt

**Status:** a generated clean transparent candidate is retained for a separate conversion comparison; it is not an identity-exact replacement.

## Question

Can image generation remove the approved full-character cutout's bright edge halo and detached pixels while retaining the same character as a genuinely transparent PNG?

## Authority and scope

- Edit target: `assets/references/approved-2026-10-26/character-cutout.png` (`4dd54a802798adc994a14349025ab48bc5830e43507d1c1c09822de692c280b8`).
- Identity references: `character-scene.png` (`a274a80133371b61387848495bf0dd93546ba5daf0a60c051b27109237160eae`) and `character-closeup.png` (`0577f22e5ab53bfa9f05f8a63947cf39c0626c84efae88d6594b1cce9421ada7`).
- User authorization: one clean-background generation attempt and one concrete repair attempt. No original was changed.

## Attempts

Both attempts used the built-in image-generation editor with all three local files as inputs and `transparent_background: true`. The first asked for removal of edge halos and detached contamination while preserving the full-body character, pose, costume, lighting, and pixel-art treatment. The repair prompt explicitly called out its dark gradient, glow, colored haze, and black backdrop and again required true transparency outside the character.

The exact prompts and interpretation correction are in [generation-prompts.md](generation-prompts.md). Matting previews are `previews/clean-v1-on-white.png`, `previews/clean-v1-on-checker.png`, and `previews/clean-v1-on-dark-gray.png`; `previews/scene-rough-clean-comparison.png` compares the approved scene, rough cutout, and generated candidate.

| Candidate | SHA-256 | Alpha-zero pixels | Partial-alpha pixels | Alpha bounds | Result |
| --- | --- | ---: | ---: | --- | --- |
| `inputs/generated-v1-background-failure.png` | `8f575851be0e3db4051aacef362cfb84cb370d40ed632e7edf52c162dad11e0b` | 1,042,100 | 530,764 | `(39,17)-(1004,1490)` | Retained first attempt. |
| `inputs/generated-v2-background-failure.png` | `12e971cc9e3cbfa7add2a17a62ff53d1f45b3c55197ce23c336a6447bed1f49e` | 1,051,204 | 521,660 | `(0,0)-(926,1491)` | Same bytes as the accepted clean candidate, retained under its historical attempt name. |

Both outputs are 1024×1536 RGBA and have no fully opaque pixels; their alpha reaches 254. The initial dark preview was misleading: it was the renderer's display of transparent/semitransparent pixels rather than a visible backdrop after normal alpha compositing. The candidate was composited onto white, checkerboard, and dark-gray mattes. Those previews show a clean exterior with no visible surrounding glow or detached fragments. The accepted stable copy is `inputs/clean-generated-cutout-v1.png`, byte-identical to the second attempt.

The candidate is not a literal edge-only correction. Against the approved scene/close-up, it retains the standing pose, tied hair, olive jacket, cream shirt, blue jeans, tote, shoes, and warm palette, but reinterprets the eye/lid shapes and small smile, hair outline/bun strands, and jacket/jeans shading. It is therefore a generated source candidate for comparison, not an approved replacement asset.

## Decision and continuation

Keep both attempt-named files as generation evidence. The accepted stable copy is sent to a separate worker for a matched conversion comparison with the rough cutout and current version. The original rough cutout remains the provenance reference, with its documented halo/specks.

No native asset, sprite conversion, animation, Godot run, commit, push, or user visual approval was produced here.
