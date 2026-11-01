# Independent Sol review and bounded expression rescue

30 October 2026. Requested route: Sol6.1/high final critic/editor. The exact pre-mouth Luna6 full-body cleanup is the common baseline; approved original scene/close-up remain identity/style authority. This is a static local-expression study, not an animation or model benchmark. Preflight observations and landmark uncertainty are in [observations.md](observations.md). Existing unrelated work, originals and Luna artifacts remain unchanged.

## Result for user review

Retain Luna's **neutral**, plus **Sol smile pass01** and **Sol surprise pass01**, as review candidates. User visual approval remains pending. One initial rescue round addressed two failed variants; zero correction rounds were needed. There was no broader face, hair or body redraw.

| Expression | Initial independent review | Retained candidate and remaining limits |
| --- | --- | --- |
| Neutral | Pass for the named rest expression: short closed horizontal mouth, relaxed open eyes and inherited identity. | [Luna native](../luna/passes/luna6-neutral.aseprite), [fresh PNG](../luna/proof/luna6-neutral-reopened.png). No Sol edit. At 1x it remains quiet. |
| Subtle smile | Reject: dark equal corner dots and a low center form an isolated squared U. The smile label did not establish the intended delicate friendliness. | [Sol native](passes/sol-subtle-smile-pass01.aseprite), [fresh PNG](passes/sol-subtle-smile-pass01-reopen.png). Warmer connected shallow curve, softened uneven corners; more friendly than neutral without the dark U. At 1x subtle, at 8x the native staircase remains. Exact original mouth shape is not claimed. |
| Surprise | Reject: inherited warm mouth plus dark edge hook, with mostly calm eyes/brows; insufficiently coherent expression. | [Sol native](passes/sol-surprise-pass01.aseprite), [fresh PNG](passes/sol-surprise-pass01-reopen.png). Compact open mouth, slightly lifted near-brow arch and more eye opening, while keeping pupils/gaze and unequal eye relationship. Reads as mild surprise; not dramatic shock. This new expression is authored inference, not copied from an approved surprise reference. |

Actual-export comparison: [fullbody 1x](reviews/final-fullbody-1x.png), [fullbody 3x](reviews/final-fullbody-3x.png), [head 1x](reviews/final-head-1x.png), [head 8x](reviews/final-head-8x.png), and [direct original/head 8x](reviews/final-direct-original-head-8x.png). The sheets contain original baseline, neutral, smile and surprise. Head sheets also show canonical original, with any reference downsampling explicitly labeled. Sprite panels use only integer nearest-neighbor zoom. Direct original face/mouth crops remain separately available. [Review provenance](reviews/final-review-provenance.json) records exact paths/hashes and approximate registration; source/cutout proportions still differ. Initial Luna sheets are retained under `reviews/initial-luna-*`.

## Fresh inspection after critic edits

Parent independently opened actual Sol head8x and fullbody3x exports, then reported: smile is now a quiet connected curve instead of the dark U; surprise has more open eyes/mouth and reads as mild surprise instead of the first hook. Parent retained both for user review and requested no further art. The first and reopened exports are byte-identical, so final sheets show the same inspected art. This is fresh independent agent inspection, not user approval. At native 1x all three expressions remain restrained; identity, outline, hairstyle, pose and body stay consistent. Neither an agent review nor the technical checks establish future animation/gameplay readability.

## Scoped construction and evidence

Registration and actual MCP owner/frame readback preceded edits. Visible owner is inherited `08-hair-tie-and-hair`, frame1; the nominal face layer does not own the edited pixels. This inherited semantic naming flaw is preserved, rather than silently repartitioned during an expression correction. Smile scope: half-open `[66,26,71,29)`. Surprise scope: eye/brow interior `[61,18,74,24)` plus the same mouth region, with nose `(71,24)` protected. Actual surprise rescue writes were further restricted to ten registered coordinates; only warm exposed brow interior and existing eye pixels were changed. No fringe/silhouette pixel was edited.

[Smile operations](operations/subtle-smile-pass01.json) and [surprise operations](operations/surprise-pass01.json) retain exact colors/coordinates, source, reasoning and output. All drawing used two batched native MCP draw calls: 4 smile operations/6 incremental changed pixels and 7 surprise operations/10 incremental changed pixels. Save-as followed mutation into new Sol paths; actual natives were freshly opened and exported again. No Lua, direct CLI drawing, UI automation, Code-MCP, image generation, installation or outside service was used for artwork.

[Strict independent checks](proof/summary.json), rerunnable with [verify.py](rebuild/verify.py), pass for all three variants:

- Relative to unchanged full-body baseline: neutral **2**, smile **7**, surprise **12** visible/native pixel changes, each within its declared facial scope. Incremental rescue versus corresponding Luna input is **6** and **10** respectively; these counts are evidence, not artistic quotas.
- Zero protected composite or native changes; all other eleven layers and every owner-layer pixel outside scope unchanged. Exact incremental operation-coordinate masks also pass native protection checks.
- All alpha values unchanged: 7,844 opaque pixels, fixed 128x192 canvas, same silhouette. Nose, hair/fringe boundaries, head contour, pose, clothing and body remain protected.
- Same native header, frame/non-cel chunks, palette, layer metadata, cel geometry/opacity/z; 12 layers, one 100ms frame, 255-entry palette. Independent native composition equals each fresh reopened PNG. First/reopened PNGs are byte-identical.
- Original baseline/reference and all Luna inputs retain their hashes. Controlled all-protected negative checks correctly reject each expression patch.

Native hashes: neutral `d76266fa8afcd1de643e6b6421ec4dfe4fa77f8044a1d083205b921eb2f25540`; smile `101f736106eb0ad18f98159fcf0aae729e27f7bf6e0991c463c523b3a5dd1062`; surprise `ee6dfc67cd196be62398dc1f20e0571662e62bf869dbe8c131741ca072889b76`.

Backend: dedicated Aseprite AI Artist MCP 0.8.2, explicitly headless, Aseprite1.3.18.6-dev. Preflight ready was observed. Backend `validate` is advertised but absent from connected tool inventory; independent strict native/PNG checks were used instead. No fresh standalone scratch smoke was run by this critic; prior backend evidence and the actual scoped edits/native reopen are the observed proof. Inventory doctor's editor `--version` check exited -6, while actual MCP preflight/edit/save/reopen/export succeeded. One saved smile session later reported modified; it was preserved as a new [proof-only resave](proof/smile-session-resave.aseprite) before closing. Independent native content/metadata equality confirms it contains no unseen art. No force discard occurred. All documents were closed; final MCP list was empty and editor lease released.

## Delivery boundary

Local native correction, export and protection are proven. Parent independently inspected edited artwork; user selection is pending. No animation, Godot/gameplay playback, project-wide installation/enablement, commit, push, publication or production-asset promotion occurred. Next owner: parent presents the exact comparison/candidates to the user. Further artwork requires a new scoped decision after user feedback.
