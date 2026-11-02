# Traveler breathing r02 — motion sample only

This is a bounded amplitude correction to the disposable r01 traveler motion sample. The user rejected r01 as too bouncy and did not approve this design as a character proposal. No fighter application, new design, outfit, grid, palette, or production-art approval is implied.

`traveler-breathing-r02.aseprite` is the native master:96x160 RGB,10 named owners,120 editable cels,12 frames,4 distinct reused valid source poses,2800ms. Maximum supported head/shoulder lift is1px (r01:3px); chest-forward expansion is2px (r01:3px). Exact rest entry/return, fixed root(44,85), soles146, rest body137px. Every preview uses a common canvas;128px rest-body projection is fixed128/137 for every pose.

`breath-0.png` through `breath-11.png`, `breath-sheet.png`/JSON and `timings.json` are the exact MCP runtime exports. Durations remain200,180,180,200,220,300,200,220,260,280,300,260ms. The four poses are rest(0lift/0expansion), open(0/1), rise(1/1), apex(1/2), mapped rest/open/open/open/rise/apex/apex/rise/open/open/open/rest. Reduced amplitude creates longer quantized pose holds;12 timeline frames are not12 unique drawings. The apex pose spans500ms. Continuous naturalness remains a playback judgment.

`checks.json` verifies immutable source SHA, fixed native owner pixels including hidden content, all native metadata/geometry/palette/timing, the prefrozen mask, all12 PNG/native composites, exact fresh-reopened sheet, alpha/solid chest coverage, exact first/last rest, and valid-source-pose reuse. No joint repair was needed; the one permitted concrete joint-repair budget remains unused. Callablevalidate is absent despite the backend advertising it, so checks are independent native/PNG audits rather than a claimed validate-tool result.

`raw-mcp-breath.gif` is preserved raw. Decoding confirms exact opaque RGB, alpha,12 encoded frames and2800ms timeline. Lead owns comparative GIF presentation and Godot validation.

`edit-proof.aseprite`/PNGs are a duplicate-only local edit: three visible first-frame thorax pixels(47,75),(47,76),(47,77) change from coat highlight to base, narrowing that fold. The visible composite changes exactly3 pixels, alpha is unchanged,119 other cels and all other native pixels/metadata remain exact; fresh reopen matches. The main animation source is unchanged. `edit-proof-comparison-8x.png` shows the actual visible revision.

`contact-1x/2x/3x.png`, `before-after-upper-all-2x.png`, and `before-after-fixed128rest.png` provide the whole affected sequence. `masks/` contains120 actual native-part alpha masks. `../editable-upperbody-frozen.png` is the1909-pixel white-editable/black-protected mask frozen before mutation, with no editable pixels at y102 or below.

The exact invoked director helper built and verified `../comparison-packet/packet.json` over all12 registered before/after frames. Baseline role is “retained r01 motion rejected as too bouncy; sample appearance only.” Packet SHA256:dccf55d1111aabd0535d3386713f65428951b8f52dee26a502442dfce911aa77. It binds the native audit, native sources, frozen mask, original/corrected ownership views and whole-cycle comparisons. Mechanical freshness does not grant visual or user approval.

Construction sources: `../baseline.aseprite` (immutable exact r01 copy), `../prepare.py`, `../correction-ops.json` (source-pose mapping and native drawing grids), `../review_keys.py`, `../audit_delivery.py`, `../comparison.json`. All native edits/save/exports used dedicated Aseprite MCP1.3.18.6-dev/Pebbly0.8.2 headless. Pillow prepared grid data/masks/checks/review packaging only. No direct native writer, CLI, UI, image generation, new installation, repository write, commit or publication. All owned editor documents closed; last list empty.

Native SHA256:82e878fe5be2ebef488cd2465cc840280750eb2bc16636834212efca0ab1ebeb.
Baseline SHA256:a34a66c188f0f3f63fd0bb06e1ccdf1ed68c82b2f8fe0b617e42489be1313417.

Lead owns final archival, engine evidence, comparison playback and independent manual decisions. User owns motion approval. All files remain under this r02 run; r01 and the selected fighter are preserved.
