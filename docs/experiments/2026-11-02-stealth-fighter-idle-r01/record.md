# Stealth fighter — first native idle study, 2 November 2026

Status: completed bounded native/runtime experiment; human motion/art approval pending. User selected “Current A far left” (original Silver Pines A), retaining existing beard provisionally. No generated beard variant selected. Current view/outfit unchanged.

## Outcome and artifact

Native assets/source/stealth-fighter/idle-r01/idle.aseprite SHA256 e839783e58f01e61b1839f18ee6208437ec9424c0403a148f331f32e9ad653fd. Five frames over3000ms (850/450/500/650/550), rest→inhale→apex→exhale→rest. Seven semantic native layers,31cels,32source-derived palette entries. Source-derived crop/mask seed128x264 canvas,240pxbody(rest),241pxapex from supported1pxrise; grid is provisional, not final game resolution. No eyes/blink added. Hair follows skull without separate sway; lowerbody/belt/sword and farhand held.

Source authority: assets/concepts/stealth-fighter/game-specific-r01/silver-pines/corrected.png SHA a3cc3ab1d658ac3d2d464ef4781ed966e815c7eedeefcf5801d81ca93924ab9c. Manual spatial polygon, nearest source transfer and32-color material sample policy, not global background color removal. Native constructed using dedicated Aseprite MCP draw grids/layers/frames; scripts prepare sample masks, recipes and inspect evidence. All native saves/reopen through MCP. Read existing art workflow, pixel-art-director animation/connected-form gates. No image generation this round.

## Checkpoints / observed evidence

1. Scratch two-layer edit: asymmetric image visually received, exact coordinate read, onepixelchange, erased-grid-dot semantics observed; protectedlayer/composite save-reopen exact and deliberate outofmaskchange rejected.
2. Static seed: lead viewed actual original plus source/seed/native at1x/3x and6actual isolatedowners; native export exact seed. Hairtie/face sampling simplifies detail but broadidentity/style retained. Lead cleared only provisional motion preparation.
3. Structuralkeys: rest/transition/apex, landmarks/actual native owners and hiddenowners reviewed. Initial apex FAILED: shoulder slit and dotted alpha seams. One scoped backing repair plus precise forearm-owner reassignment closes gaps; fixed owners/composites retained. Failed/repaired/final sources preserved in native-work/keys. Lead inspected repairedcontrast5x and finalcycle2x; material/neck/arm/waist joins support continuation. Body anatomy under clothes remains approximate/inferred; hidden fullrig not established.
4. Finalnative: independent native reader verifies5frames/7layers/31cels, metadata/palette, PNG/sheet/freshMCP-reopen, fixedlowerbody/swordbelt/farhand, registeredhead1pxrise, exactfirst/last, y153+fixed and0enclosedalphaholesallframes. Duplicate-only3pixelbuckle edit/reopen proves useful edit; hidden pixels and othermetadata protected. See native-work/delivery/checks.json.
5. GIF boundary: rawMCPGIF preserves timings/alpha but remaps89/89/86/89/89 nearblack pixels by2RGBlevels. Rawexports retained. Lead exported explicitpalette GIF from exactPNGs; all5 visibleRGBA/timings exact (lead-review/cycle-technical.json). Opaque slate2xpreview is nearest-only display packaging, not nativeartedit.
6. Runtime: dedicated Godot MCP ran /private/tmp/stealth-idle-godot on Godot4.7.2-stable (official), OpenGLCompatibility AppleM3Pro,640x360viewport/1280x720window, nearestfilter. One study atnative1x and sameanimation projected128pxbody. Atleast3loops recorded withall5captures; MCPstop finaloutput observed12loops, errors[]. Sourceframe opaque RGB equals all5 native1xactor captures exactly; evidence/runtime.json,pixel-checks.json,mcp-debug.json,mcp-stop.json. Engine stopped. Delivered godot-preview is byte-copy of tested project/frames excluding .godotcache; originaltestedtemp path recorded.

Lead visually reviewed still exports/contact/contrastmatte and Godotapex capture. Continuous temporal naturalness was NOT perceived by the lead; exact authoredspeed GIF and actual engine timing/captures are supplied for user review. Godot-poses-at-authored-timing.gif reconstructs capturedposes at source durations, not a continuous video capture. No claim of combat/playability or final motion approval.

## Delivery map and continuation

- assets/source/stealth-fighter/idle-r01/idle.aseprite: editable master; source recipe and construction notes.
- assets/export/stealth-fighter/idle-r01/: frames, sheet+metadata, timings, exactpalette nativeGIF.
- assets/previews/stealth-fighter/idle-r01/idle-2x.gif: exactcolor slate-matte2x display preview; source-to-native and contacts, actual Godotcapture.
- This experiment: native-work contains original failedkeys, repairedkeys, drawingops, source masks/recipes, ownership/landmarks, smoke and localedit proofs. Itsoriginal/tmp paths map to identical copiedfiles here. All oldconcept/source assets preserved.

User next judges whether breathing feels too held/subtle/stepped or useful, independently from retained appearance. Agent owns named correction. Camera remains3quarter and finalface/style/native/displayresolution open. No productionreplacement, newinstallation, commit/push/publication. AllownedAseprite documentsclosed; engine stopped.
