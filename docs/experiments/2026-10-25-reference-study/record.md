# Experiment: reference direction and existing Aseprite integration

- Status: observed tool proof; concept feedback pending
- Date: 25 October 2026
- Question: which visible qualities of the supplied Until Then reference should guide an original combat asset, and can the user's existing Aseprite build support scripted native edits?
- Relevant guides: current reference-derived proposals in docs/art/style-guide.md and docs/art/motion-guide.md; no original asset approval yet.
- Baseline: repository revision 9e35c5c; research/rules only, no original generated concept or proven Aseprite integration in this repository.
- Completion criterion for this increment: preserve references, generate one controlled concept comparison, document limitations, and demonstrate native save/reopen/revision/export with the already-built app. This is not the full character/attack pipeline proof.
- Tools: built-in image generation (one call); user's compiled Aseprite 1.3.18.6-dev; Python standard library; no new paid API, MCP, or skill installed.

## Plan and authority

The user prefers the whole Until Then art direction, especially the carnival image, and authorized starting reference exploration. They subsequently requested making the existing compiled Aseprite available in Applications for other projects. The build was found under `/Users/guhan/Documents/ChatGPT/Gadot Sample/ForestDuel/.tools/aseprite/build/bin/Aseprite.app` and copied with `ditto` into `/Applications/Aseprite.app`. The original was preserved. No existing Applications copy was overwritten. Linked libraries inspected with `otool -L` were system libraries/frameworks.

The build's version command aborted inside the sandbox; running through the normal approved escalation returned its version. The copied app and Lua check ran through that same execution boundary. No host-trust or Code-MCP authority setting was changed. GUI startup was not visually inspected.

## Artifacts

- User references: [R001 carnival](../../../assets/references/until-then-carnival-user.png), [R002 Steam capture](../../../assets/references/until-then-store-user.png).
- Original generated [lighting study v01](../../../assets/concepts/2026-10-25/lighting-study-v01.png), created with built-in image generation, using both supplied screenshots as appearance references, not edit targets.
- Exact [generation prompt](concept-prompt-v01.txt). All three panels hold the provisional subject/outfit/scene approximately constant; the intended comparison variable is lighting. Generated panels are not pixel-identical fixtures.
- [Research](../../research/until-then-art-direction.md), including evidence boundaries and primary-source links.
- Reproducible [Lua smoke check](aseprite-smoke.lua), native [before](tool-proof/swatches-before.aseprite) and [after](tool-proof/swatches-after.aseprite), exported [before PNG](tool-proof/swatches-before.png) and [after PNG](tool-proof/swatches-after.png), and [check results](tool-proof/checks.txt).

Run the tool proof from the repository root (the output directory must exist):

```sh
/Applications/Aseprite.app/Contents/MacOS/aseprite --batch \
  --script-param output="$PWD/docs/experiments/2026-10-25-reference-study/tool-proof" \
  --script "$PWD/docs/experiments/2026-10-25-reference-study/aseprite-smoke.lua"
```

## Observations

| Check | Method and target | Observed result | Evidence |
| --- | --- | --- | --- |
| Reference direction | User's supplied stills and explicit preference | Cinematic pixel-art reference preferred; original character, scale and combat choices remain open | Reference log |
| Concept comparison | Visual review of generated A/B/C board | A warm, B relatively neutral, C cool. Full-body subject readable; result is finer, noisier and more painterly than preferred reference. Clothing/hair need simpler clusters before production. No approval inferred | Lighting study v01 |
| Source structure | Aseprite batch Lua creates, saves, closes, reopens, asserts two named layers | Passed for a 32x16 swatch fixture only | Lua script and checks.txt |
| Localized revision | Reopen native file, replace accent cel, save/reopen, compare decoded RGBA PNGs | Exactly 64 accent pixels changed; remaining 448 pixels unchanged | Before/after native files, PNGs, checks.txt |
| Native file validity | Header size/magic/dimensions/frame count check plus Aseprite reopen | Passed; 32x16, one frame, native magic 0xA5E0 | Native files |
| Character consistency/editability | Production character source | Not run; generated board is flattened concept imagery | None |
| Attack/contact/timing | Motion source and playback | Not run; no attack selected | None |
| Godot/game scale | Actual engine execution with the candidate | Not run | None |

## User feedback

R001 and Until Then's overall appearance are preferred references. No feedback or approval has yet been received for the generated original C001 board, its outfit, or a lighting panel. The prototype swatches have no art-direction significance.

## Decision and continuation

- Continue concept refinement using the supplied reference direction; retain variants separately.
- Aseprite CLI/Lua is a locally proven candidate for subsequent construction. No third-party MCP is currently needed to cross this integration boundary.
- Last proven state: one generated comparison board plus existing Aseprite native save/reopen/revision/export, not a playable character.
- Next owner/action: user gives concrete feedback on A/B/C lighting and rendering; agent refines pixel grouping and preserves an approved original candidate before creating dependent sprite/attack assets. A combat clip, weapon and camera decision become useful before the attack stage.
- Files are local working-tree changes; no commit or remote publication was performed for this study.
