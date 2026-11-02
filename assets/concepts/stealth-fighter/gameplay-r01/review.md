# Gameplay concept comparison — 1 November 2026

## User decision and scope

The user likes atmosphere-r01/A/simplified-01.png character design a lot, accepts its direction, and accepts the atmosphere for now with later reconsideration. Preserve that image as the approved direction anchor (SHA-256 e1dcf18e72ce22b8b6c6031d0f00da91259dcbf4c2bfbb0e0c12c8d1c56b6e1e). Exact face, gameplay camera, displayed size and native sprite grid remain open. User requests transparent in-game presentation, camera correction, scenarios and facial alternatives, with parallel subagents per variant. This does not approve any new generated variant.

User subsequently requires GPT-6.1 only, any reasoning, no Astra. The initial 5.6 task was interrupted before any output appeared; all delivered generation work in this round used GPT-6.1 Terra/high agents orchestrating the built-in image tool. This is the orchestration model identity, not an assertion about the image generator model. Initially two outputs were grouped per agent; after the user's correction, each further variant had a separate fresh parallel agent. Parent performed the visual review below.

## Presented artifacts

- views-comparison.png: left side-corrected/cutout.png; right shallow-corrected/cutout.png. Matched full-image presentation, same original dimensions. Neither achieves a strict orthographic profile; torso/boots retain depth. Left is the more useful side-facing study. The original was a portrait-like front-torso/head-side pose with visible boot tops; the discrepancy is real, rather than simply background framing.
- faces-comparison.png: left face-soft-corrected/raw.png; right face-firm-corrected/raw.png. Separate agents and exact prompts. Parent favors left as a younger, calmer interpretation; right has a heavier jaw/brow, more severe/mature expression. Both remain more detailed than intended; hair fringe/collar/framing and lighting drift slightly, so this is not a perfectly isolated bone-structure comparison. No user selection yet.
- scenarios/comparison.png: three same-image static mockups at projected visible-body heights 96, 128 and 160 pixels in a 640x360 comparison viewport, same environment, x=200 and foot baseline y=273. Body normalization uses documented alpha>128 bounds, not the full low-alpha halo. These are display sizes, not native sprite resolution. Parent favors 128 as an initial balance of detail and arena space; movement/combat can change the conclusion. Empty arena is temporary context, not approved world/level design.

## Transparency and failed attempts

All candidate cutouts have actual alpha but retain a translucent halo. Do not label any as a clean background-free production export. Numeric alpha checks and raw prompts are recorded in each subfolder. No pixel masks or repainting were applied to hide the defect. Even extraction-only original cutout retained a halo and redrew the character. Therefore clean cutout and fully corrected gameplay camera remain unresolved after bounded attempts; no further blind retries this round.

views/side.png and quarter.png are the first two attempts. side-corrected/ and shallow-corrected/ are independent correction attempts. extracted-original/ is the isolated extraction-only attempt. Preserve all. faces/unassigned-01.png and -02.png are excluded from comparisons: a worker result-reporting error lost the prompt/output mapping, and their detail/framing drift. The two exact attempted prompts and uncertainty are preserved in faces/unassigned-manifest.md. Do not relabel them as controlled soft/firm outcomes.

## Tool and evidence boundary

10 built-in image generation calls total: 2 initial views, 2 unassigned face studies, 1 empty arena, 2 independent camera corrections, 2 independent face alternatives, 1 extraction-only attempt. No CLI/API generation, new installation, purchase, native sprite construction, animation, Godot playback, commit or publication. Original outputs remain unchanged. Per-agent records contain exact prompts, references/roles and generated source paths. presentation.json and scenarios/scale-manifest.json record comparison layout transforms; layouts embed unchanged raster sources. Parent inspected actual anchor, corrected views, both final face alternatives, arena and all three rendered comparison boards. PNG dimensions/hashes and JSON decoding verified in checks.json. No numerical metric establishes visual approval.

## Next decision

User chooses useful face cues, more side-on versus shallow-turn presentation and preferred screen framing. Clean alpha and the remaining perspective require a controlled correction before production. The existing art pipeline is unchanged. No canonical native grid or final face is silently selected.
