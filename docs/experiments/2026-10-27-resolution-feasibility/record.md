# Resolution feasibility: bounded two-pass studies

- Status: observed, **inconclusive as a resolution comparison**; visual approval unknown.
- Date: 27 October 2026.
- Question: whether additional native pixels make the approved character's face and upper body more feasible to construct and revise.
- Approved visual references: [full scene](character-scene.png), [close-up](character-closeup.png), with [cutout](character-cutout.png) secondary where edge artifacts occur. Reference image hashes are in [input-hashes](input-hashes.txt); originals were checked afterward in [original-hashes-after](original-hashes-after.txt).
- Baseline: copy of v04 [native master](baseline.aseprite), [fresh export](baseline.png). Provisional original canvas 128×192, drawn height 184 pixels. No gameplay display target is established.
- Scope: two fresh upper-body studies, no full character, environment, animation, or gameplay claim. A maximum of two coherent passes per study was allowed; two passes each were performed.
- Drawing agent: `gpt-6.1-terra`, high reasoning, dispatched by Codex Desktop. Headless Aseprite 1.3.18.6-dev via authored CLI/Lua; direct MCP preflight reports Pebbly 0.8.2 ready but art did not use MCP drawing calls. Parent performed independent pixel/native/document checks. Full model token/cost totals, artistic elapsed time and drawing-operation totals were not measured.

## Profile and observations before drawing

Keep the rightward three-quarter pose, tied brown hair and loose fringe, warm skin, olive jacket, pale shirt and cream tote strap. Separate back/front hair, face, features, jacket, shirt and tote for revision. The scene and close-up are authoritative over the cutout. Eyes point right; the far eye is narrower, and hair overlaps a partly covered ear. Exact source pixels cannot be inferred from the reference's rendering. The baseline has a smaller face and many clustered hair and jacket marks. Hypothesis: a larger grid can offer separately placeable eye, brow, smile and fringe clusters; the additional area does not itself ensure likeness.

## Artifacts and equivalence

- [192-equivalent source](study-192.aseprite), [native export](study-192.png), [4× nearest-neighbor](study-192-4x.png): crop canvas 120×132. A hypothetical full character at 1.5× the baseline canvas is 192×288, with projected 276-pixel body height if proportions were preserved.
- [256-equivalent source](study-256.aseprite), [native export](study-256.png), [4× nearest-neighbor](study-256-4x.png): crop canvas 160×176. A hypothetical full character at 2× the baseline canvas is 256×384, with projected 368-pixel body height if proportions were preserved.
- [Baseline crop at 4×](baseline-crop-4x.png) takes x=24..103, y=0..87 of the v04 export, 80×88 pixels.
- [Matched-display diagnostic](matched-display.png) presents those crop canvases at 6×, 4× and 3×, respectively, all to 480×528 using integer nearest-neighbor. **These canvas ratios do not mean the depicted anatomy is matched:** the new heads are proportionally larger and the torso is cut differently. Thus this sheet is a diagnostic of these attempts, not a controlled comparison or a gameplay-size preview.
- [Drawing source](draw.lua) records authored polygon/pixel operations, with separately specified coordinates for each study. No reference or baseline raster is imported into either master. Common palette and motif were used; composition and drawing effort are confounded with resolution.

## Second pass and visual assessment

The [192 second-pass master](study-192-pass02.aseprite) and [256 second-pass master](study-256-pass02.aseprite) have [native exports](study-192-pass02.png), [256 native export](study-256-pass02.png), [192 4×](study-192-pass02-4x.png), and [256 4×](study-256-pass02-4x.png). [Matched diagnostic](matched-display-pass02.png) shows the same 6×/4×/3× canvas scaling as pass 01. [Second-pass source](draw-pass02.lua) transforms the authored head polygon coordinates around the neck junction to reduce their size, then adds individually placed ponytail clusters; this is a revision of each first pass, not a separate independently drawn comparison. The originals remain intact.

Visual inspection: the second pass reduces the oversized heads and adds some ponytail separation, but the heads are now lower in frame than v04 and their facial form and expression remain simplified. The torso lacks hood, sleeves, hands and detail. While the revision changes proportions, it does not match the baseline or approved reference well enough to isolate resolution. Neither pass supports a quality ranking or production decision. The matched-display image is a crop-canvas diagnostic, not matched anatomical framing or gameplay proof.

Both pass-02 files reopened with seven layers and one frame and exported identically; on separate duplicate files a one-pixel edit was visible and transparent corners remained. See [native checks](native-check-pass02.txt) and [pixel checks and SHA-256](pixel-check-pass02.txt). This checks mechanical editability, not an artistic correction. The study sources and previews are unapproved and remain local.

The parent independently reran both Python comparison scripts and used the existing `tools/check_native_pilot.py` reader against all four source/edit-proof pairs. [Independent native checks](independent-native-checks.json) confirm declared dimensions, seven layers and one frame, equal layer metadata and cel geometry/opacity/z, exactly one changed `Back hair` pixel at (0,0), and zero changes in the other six layers. **The strict native comparison rejects all four pairs for header and non-cel chunk changes:** header color-count bytes differ and an old palette chunk (`0x0004`) becomes a modern palette chunk (`0x2019`) on save. Exact all-metadata preservation is therefore not proven, even though RGBA layer protection passes. These fresh studies had no frozen-palette requirement; this result would need resolution before claiming compliance with a strict correction profile. The fail-closed reader covers the observed RGBA/raw-or-compressed cels, not every Aseprite feature.

**Technical recovery, separate from the two art passes:** [verify-normalized.lua](verify-normalized.lua) exports and saves new second-pass scratch copies before freezing them, then reopens and edits only (0,0) on `Back hair`. Both normalized exports remain RGBA-identical to the original second-pass art. The unchanged strict checker now passes both normalized source/edit pairs, including header, all non-cel chunks, layer/frame/cel metadata, zero protected-layer changes and exactly one changed composite pixel. See [normalized native checks](normalized-native-checks.json); `study-192-pass02-normalized.aseprite` and `study-256-pass02-normalized.aseprite` are technical baselines only, with `-normalized-edit` files as edit proofs. Original sources, failed checks and previews are retained. This establishes scoped editing after a stable saved/exported baseline, not improved artistic quality; it does not permit ignoring metadata changes in other runs.

## Independent review dimensions

These are agent observations, not a numerical score or user acceptance.

| Dimension | Observation and evidence boundary |
| --- | --- |
| Character identity | Costume colors and tied hair remain recognizable cues; the face and tied-hair construction differ substantially from the approved concept. Neither candidate is accepted. |
| Silhouette | Ponytail/torso read as broad masses, but distinctive fanned hair, hood and relaxed sleeve shapes are missing. |
| Face | Two unequal right-looking eye marks are present; anatomy, head placement and expression remain inconsistent with reference/baseline. |
| Pixel craftsmanship | Deliberate opaque shapes are editable; simple flat polygons and limited planes do not reproduce the reference's hair/cloth construction. File correctness does not remedy this. |
| Style consistency | No controlled scene placement was performed; quieter detail than v04 is visible in the diagnostic, but environment compatibility remains untested. |
| Native editability | Seven meaningful layers and exact reopen/export passed. Initial strict duplicate comparisons exposed palette/header changes; normalized technical baselines subsequently passed the unchanged strict checker. See both reports above. |
| Animation feasibility | Not tested; no key poses or timing revision. |
| Gameplay readability | Not tested; no selected screen scale or actual Godot run. |

## Checks and observed limitations

| Check | Result |
| --- | --- |
| Native source and export | Existing Aseprite 1.3.18.6-dev ran via CLI/Lua outside the restricted shell, after its sandboxed doctor inventory returned SIGABRT. No installation. Both sources reopened at declared dimensions with seven visible named layers and one frame; fresh exports matched pixel-for-pixel. [Native output](native-check.txt), [pixel checks](pixel-check.txt). |
| Local edit | On reopened duplicates only, one magenta pixel was added at transparent (0,0); the composite changed by exactly one pixel. [192 edit source](study-192-edit-proof.aseprite), [256 edit source](study-256-edit-proof.aseprite). This is a mechanical layer edit proof, not an artistic revision. |
| Transparency | Both exported corners at (0,0) are transparent; no comprehensive alpha/palette policy was asserted. |
| Identity and orientation | Two eyes and rightward-facing pose are present, but the eyes are oversized and the facial anatomy more frontal than the approved concept. The face/head occupies too much of the frame to match v04's proportions. |
| Hair and clothing | Ponytail reads as a flat oval rather than overlapping tied locks; fringe and head shape are simplified. Jacket lacks the approved hood, construction and rich fabric folds; shirt lacks most folds; only tote strap appears. Both are below the reference and v04 in these respects. The larger study adds brow, iris and a few small shape clusters, but these do not establish superior likeness. |
| Cost | No paid service, new installation, or image-generation operation used. Individual drawing time and per-operation cost were not measured; no cost comparison can be inferred. |
| Motion, engine, game-scale and user approval | Not performed/unknown. |

## Decision and continuation

Do not select a production resolution from these drawings. They confound grid size, anatomical proportions, framing and execution effort; they show only that two layered studies can be created and reopened. Preserve both first passes as evidence, not accepted sprites. The next artist/agent should first align the head-to-body scale and crop to the v04/reference, then create an independently matched redraw under a newly agreed budget with distinct ponytail clumps, less frontal facial geometry and jacket/hood planes. Compare at matched full-character projected height and native zoom, with the user choosing whether likeness merits further work. Actual animation burden and Godot readability remain untested. No commit or publication was performed.

## Reproducible next experiment (planned, unexecuted)

1. Use the copied primary close-up and scene above. Freeze one head/shoulder reference crop; record that crop in original-image coordinates. Use v04 as a labeled baseline only, rather than inheriting its incorrect face geometry.
2. Record approximate hair-top, eyeline, chin, neck junction and shoulder positions as fractions of this crop, with uncertainty where the reference is ambiguous. Map the same layout into candidate native crops; document rounding and full-character equivalence. Make a silhouette/large-plane blockout at 128-equivalent first, compare at matched display height, and correct proportions/framing before any detail pass.
3. After that blockout is comparable, author face/hair clusters at 128- and 192-equivalent grids with the same identity priorities and bounded pass budget. Include 256-equivalent only if a specific important feature remains unresolved. A fresh baseline-scale redraw helps distinguish improved construction from resolution effects; none has been performed in this experiment.
4. Preserve every checkpoint. Export 1x and integer zoom plus equal displayed anatomical framing; label reference resampling. Review the eight dimensions above, record actual start/end times and observable tool/drawing operations, and demonstrate a small local revision on a duplicate plus reopen/export.
5. Agent recommends a direction with visible reasons; user selects identity/expression. Keep production grid, animation method and Godot scale provisional until their own proofs run. The next owner is an agent for layout/construction and the user for artistic selection, not manual repainting.

The revised director/workflow now require the layout checkpoint exposed by this attempt. That instruction change is implemented; its effectiveness awaits the planned controlled redraw.

## Rebuild and verification commands

From the repository root, with the existing Aseprite binary and bundled Python/Pillow (no installation):

```sh
study_dir="$PWD/docs/experiments/2026-10-27-resolution-feasibility"
/Applications/Aseprite.app/Contents/MacOS/aseprite -b --script-param "out=$study_dir" --script "$study_dir/draw.lua"
/Applications/Aseprite.app/Contents/MacOS/aseprite -b --script-param "out=$study_dir" --script "$study_dir/draw-pass02.lua"
/Applications/Aseprite.app/Contents/MacOS/aseprite -b --script-param "out=$study_dir" --script "$study_dir/verify.lua"
/Applications/Aseprite.app/Contents/MacOS/aseprite -b --script-param "out=$study_dir" --script "$study_dir/verify-pass02.lua"
/Applications/Aseprite.app/Contents/MacOS/aseprite -b --script-param "out=$study_dir" --script "$study_dir/verify-normalized.lua"
/Users/guhan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B "$study_dir/check.py"
/Users/guhan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B "$study_dir/check-pass02.py"
/Users/guhan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B "$study_dir/verify-evidence.py"
```

These reproduce the recorded attempts, not the planned improved experiment. They overwrite this experiment's outputs: use a new run directory with the frozen inputs copied there when making a new attempt, keeping this evidence intact. CLI startup may require the existing targeted execution allowance on this host; no broader machine setting is part of the art workflow. Direct MCP preflight in this chat returned ready for headless Aseprite 1.3.18.6-dev / Pebbly 0.8.2, but these drawings and reopen proofs used CLI/Lua; direct MCP drawing/image delivery was not tested here. Exact artistic work time and full drawing-operation counts were not captured and remain unknown; there were four art passes, plus the separate technical checks, with no image generation or paid art service.
