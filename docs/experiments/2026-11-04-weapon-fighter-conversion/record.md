# Weapon fighter — conversion only

- Status: observed; user review pending. Date: 4 November 2026.
- Request: source conversion to brawler scale/Aseprite canvas, with no AI correction.
- Baseline: `original.png`, SHA256 `7069b5792b13defba56febb6415824b82ab4c1d4395b577aaacef1b0f140a05d`.
- Intent: deterministic conversion, not reconstruction. No existing character's dimensions/palette are inherited.
- Tools: Aseprite 1.3.18.6-dev / Pebbly 0.8.2 headless dedicated MCP; Python 3.11 / Pillow 12.0.0. No generation, repaint, new installation or paid service.

## Research checked today

- [WayForward: River City Girls 2](https://www.wayforward.com/games/river-city-girls-2/): game identity and presentation confirmed; no universal sprite dimensions found. Official image retrieval timed out.
- [RCG2 Misako archive](https://www.spriters-resource.com/pc_computer/rivercitygirls2/asset/190132/): extracted frames listed, but ZIP retrieval returned HTTP403. Native frame dimensions could not be measured.
- [Independent reference study](https://talk.pokitto.com/t/devlog-unnamed-entry/2291): estimates original River City Girls sprites around64px tall. Third-party approximation, not verified RCG2 dimensions.
- [Artist's own RCG-style commissions](https://tamanegi-k.carrd.co/): approximately48×72 sprite /100×100 image. This is the artist's fan-art specification, not official game dimensions.
- [Ubisoft: Scott Pilgrim](https://www.ubisoft.com/en-us/games/scott-pilgrim-vs-the-world-the-game/editions/complete) and [Dotemu: TMNT Shredder's Revenge](https://www.dotemu.com/announcing-teenage-mutant-ninja-turtles-shredders-revenge/): related brawler references; Dotemu explicitly describes pixel-art rendering. Exact sprite dimensions unestablished.

Decision: **provisional64px visible height**, not an exact verified RCG2 match. Preserve the wide pose/weapon on128×80 rather than shrink the body to fit a square. Exact game-size matching remains unresolved.

## Contract and artifacts

LOCK: source pose, proportions, face, hair, outfit, weapon and retained RGB samples. FLEX: backdrop alpha, aspect-preserving nearest-neighbor sampling and canvas placement. FREE: none. No correction pass.

- `fighter-64.aseprite`: one RGB frame / one flat editable layer, `Converted original - no corrections`. Not a semantic reconstruction or rig.
- `fighter-64.png`: transparent128×80, visible bounds(9,8)-(118,72) =109×64.
- `fighter-64-6x.png`: nearest-neighbor enlargement of actual native export.
- `reopened.png`: fresh MCP reopen/export evidence.
- `convert.py`, `pixels.json`, `recipe.json`, `foreground-mask.png`: reproducible mask and source sampling operations. Character/native writes used dedicated MCP.
- `mask-review.png`, `review-light.png`, `review-dark.png`: diagnostic alpha/scale previews.
- `verification.json`: independent checks and native SHA.

The opaque1536×1024 backdrop is a narrow muted pink-brown range. Four-neighbor components remove the border-connected backdrop plus three visually reviewed enclosed weapon openings(262,5439,300 source pixels). Small similarly colored shoulder-metal marks remain opaque. This explicit mask is source preparation, not generated background removal. No smoothing, quantization, dithering or invented paint.

## Observed evidence

Original inspected: tied swept brown hair, right-facing profile, rust/cream coat, spread boots and large forward metal weapon. Actual native export reviewed at1×/6× plus source mask and light/dark mattes. Main masses remain; face/expression and trim lose detail through sampling. No repair attempted under the user's restriction.

PASS: independent every-pixel source-coordinate sampling(0 mismatches), binary alpha,128×80 canvas,64px visible height, unchanged source, independently parsed native layer/cel exactly equals PNG, fresh reopen/export exactly equals first export.2685 opaque pixels /1682 sampled RGB colors. RGB texture retained without palette reduction. MCP `validate` is not exposed; independent checks cover only the stated file/pixel properties.

`smoke.aseprite` is a separate tool image/coordinate-readback scratch pattern, not art. Final native SHA256: `cb9ef10c0afd004be373e0e806a5ab225a5c7bfc568c27117db09aa7d6ad3a85`.

Completed: conversion, native save, export, visual inspection, fresh reopen. Not performed: AI correction, semantic reconstruction, animation, Godot, user approval, publication or visible-window installation. Backend is headless; saved file can be opened in Aseprite. Next owner: user reviews conversion; exact game-size matching requires a measurable native reference. Existing work preserved.
