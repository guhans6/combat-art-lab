# Observations and decision trail

## Intake and baseline

Opened full six input images, original-neutral PNG, original native through dedicated MCP and approved scene/close-up. New idle has tied brown hair, pale tie, rightward three-quarter face, pale tee/olive jacket/wide blue jeans/pale sneakers/cream tote. Original neutral has more restrained eye/hair clusters and a somewhat narrower head. Source05 opens the mouth; this experiment deliberately keeps the original restrained face/head drawing as the identity anchor rather than importing inconsistent new head sizes. Neutral and source proposals are not approved production animation.

Actual PNGs are1448×1086, partial alpha present, thousands of colors, with faint alpha extending near entire image borders. Many saturated red/yellow/blue/green edge pixels are visible on tote, trousers and negative spaces. Complete main silhouettes were visually opened before masks. Reviewed spatial windows and dominant eight-connected opaque subject masks remove distant alpha; explicitly named contaminant hues are removed from source masks, not blanket white deletion. All six binary masks and full inputs retained. Raw conversions in review/raw-conversion-*.png are seed diagnostics, not native masters.

Original128×192 translates(+60,+8). It measures183px crown-to-sole; native action256×208 adds room. New torso transfer uses0.18px/sourcepx above pelvic belt, legs register hip→sole independently by **anatomical span**, not alpha boxes. Pickup lower body and rigid head are original native pixels. Source head is omitted above actual neck boundary; neutral head ends y41, neck backing belongs to shirt/neck owner. New idle remains comparison guidance; no incompatible second idle is inserted at entry/return. Anatomical-observations.json records approximate visible points/uncertainty; they support inspection, not automatic bone-length scores.

## Backend proof

Dedicated MCP ready: Pebbly0.8.2, headless Aseprite1.3.18.6-dev. Godot MCP reports4.7.2.stable.official.ed1daf0bf. Doctor is non-launching inventory. Full two-layer16×16 scratch proof performed: asymmetric L, red two-by-two patch, isolated cream13,12; ASCII read; exactly one8,5 pixel revision; protected native layer exact; skip leaves pixel, erase removes it; save/reopen/export match; known protected-pixel edit is independently rejected. Initial pixels-op schema used `pixels` rather than required `points`, rejected without edit, corrected using grid. No raw Lua, editor CLI, Python native writer, Code-MCP or UI automation.

`validate` is advertised as a preflight feature but not exposed as a callable tool. No successful validate call is claimed. Independent file checks replace only its technical boundary. They do not judge art.

## Structural iterations (finite budget)

- Pass01: initial keys show remnants around reconstructed tote and a missing shoe tip. Explicitly rejected. Warm bag shadows were classified as skin; a prop removal predicate also applied below prop height and removed shoe pixels. No expansion from this state.
- Pass02: spatial hand regions constrain warm pixels, prop replacement ends above shoes. Opened actual native/composite/owner/hidden evidence. Caught residual **old dark bag outlines on jacket owner** in pickup, and raised forearm pixels assigned to shirt-neck because of y-only neck classification. Rejected those ownership/cleanup states.
- Pass03 (second bounded structural correction): actual bag-body spatial masks remove dark remnants on original owners; hand ownership uses reviewed hand regions; neck is spatially restricted near neck, not any skin above a horizontal line. All six actual dedicated PNG exports match the independently decoded native composites. Files retained: structural-pass01/02/03.aseprite, literal recipes and mask inputs. Independent structural review pending at this point; no clearance inferred from export equality.

Current owners: legs/shoes; rear handle; connected jacket/sleeves; shirt/neck backing; bag body/rim; near straps/seams; hands/forearms; rigid head. A visible source-mask separation does not establish a reusable hidden-surface rig. Existing form overlaps remain part of the connected-unit drawing.

Prop construction sites G/FL/FR/NL/NR/M/bottom retain one local cloth object. Mouth18px below gathered grip, body≈26px at broadest×29px long. Carried version compresses width0.67 and lengthens handle drop to33px in high grip /22px in low grip; bag **body** length is unchanged. Windup angle+29°, extension−50°, recovery−43°. Far roots terminate behind rim; near bands continue to v24 inside the front surface, with short shadow seams. These routes are construction hypotheses made inspectable in native owners/hidden views, not claims that the source proves hidden roots. Detail has not yet been added to these plane studies.

## Evidence limits

All visual observations so far are still/full-frame/cropped inspection at native size and integer zoom. The original-key comparison uses explicitly labeled diagnostic resampling for the original references and1.5× complete action canvases; actual1× PNGs and2× key sheet are separate. An earlier comparison crop cut off the extended bag; helper was corrected before independent review, actual native/export never cropped. Site guides use separate legends to avoid labels obscuring roots. Research inspected primary written tutorials/docs, not continuous media. No motion perception, Godot run, new user artistic approval, production replacement, commit or publication is yet established.

## Transfer and final cycle gate

Independent review initially stops expansion on missing shoulder/grip transfer, while clearing shown endpoint anatomy/attachments. New transfer study provides actual shoulder-clearance lift and gather. First transfer study is retained; revision angles the lifted forearm to reveal the lower strand caught by the other hand and restores exposed coat backing. Independent continuation clears the two new keys/return route. Source/sprite01 is not used as a competing rest scale.

Cycle expands to19exposures,2230ms after one timing revision (windup−20ms, contact−10ms, idle inspection hold+100ms). The one50ms drawn smear is F9,820–870ms; clean A uses an on-model transit on the same clock. Contact F10 is870–960ms; final exact idle begins1730ms. Front/right support component is exact F8→F13; rear/left support component is exact F13→F14. The reviewer initially flagged F14 using global maximum sole y, then retracted after actual component correspondence proved the support is unchanged; rear screen-space contact may be higher on the reference's perspective ground. One global y is not the actual support-foot contract.

## Final focused correction and outcome

The first completed-cycle preview is **not** the final deliverable. Independent review finds flat orange forearms/weak wrist/finger definition and simpler cloth in authored families F4–6,F8–9,F14–16. It also traces smear's FL=(152,98) ending5Manhattanpixels from fabric; connectivity through the other far root was insufficient. Last bounded correction replaces that whole rear-handle cel with FL=(160,99), directly covered by both actual rear and body/rim owners. No obsolete fork remains.

Material03 maps the actual windup sleeve/forearm material clusters by anatomical length/cross-section inside the authored forms; it tapers wrists and draws distinct palm/thumb/finger/overlap clusters. Jacket alpha is exact; hand contour changes are intentional on the actual owner. No random texture or colors added to hit a numerical target. Native-scope proof records17changedcels only: jacket/hands in eight frames, plus smearF9rearhandle. Head, shirt/neck, legs, nearhandle, bagbody, timing and palette stay exact. Primary opened actual before/after/composite/native previews; independent final review clears still anatomy/material/grip/neighbor evidence and recommends provisional playback candidate. User approval remains pending.

Selected native artifacts are explicitly named **tote-clean-material03.aseprite** and **tote-smear-material03.aseprite**. Earlier generic natives remain preserved before-correction candidates; old GIF/runtime evidence must not be cited as corrected playback. Corrected exports, fresh-reopen/local-edit proof and final Godot run are recorded separately in record.md/proof. Full literal replay inputs are frozen from final native pixels/structure; a complete fresh rebuild was not executed. Continuous motion perception remains unverified by agents.

## Runtime probe ownership correction

Actual C-probe auditing found rectangular crops from the full composite included346/115non-prop pixels in F8/F9. Final fixture requires a dedicated-MCP isolated native prop-owner sheet, verified19/19 against rear-handle/body-rim/near-handle owners, with no whole-character fallback. Character native sources and A/B art remain exact. Initial isolated-sheet startup used nonexistent Image.has_alpha(); actual Godot MCP caught the error, retained in proof/runtime-isolated-prop-startup-failure.json. That guard was removed in favor of the existing per-pixel opaque/transparent screen before a fresh dedicated rerun. Final results are in the runtime-material03 records.
