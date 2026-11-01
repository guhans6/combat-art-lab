# Experiment: source-assisted head comparison and blink probe

- Status: observed; conversion route, final C01 provisionally recommended by agent, user selection pending.
- Date: 27 October 2026. Base revision: `9e35c5c13987a153e942e6f93f49f247fad13c3a`.
- Question: can trace guidance or conversion plus cleanup preserve this character/style
  more convincingly than the current independent redraw while remaining revisable?
- Scope: one head/shoulder crop, plus one bounded expression motion probe. This does
  not deliver a full-body combat asset, production grid, attack or Godot scene.
- Acceptance: concrete A/B native masters/exports, separate visual judgments, raw seed,
  reproducible masks/inputs, local edit/reopen evidence, preserved attempts and next step.
- Tools: installed Aseprite 1.3.18.6-dev CLI/Lua, bundled Python 3 with Pillow 12.3.0,
  built-in image_gen (one call), Codex in-app browser playback. No installation/new API
  credentials/paid service account/commit/publication. Exact execution-model ID and
  image-generation cost were not exposed. No new repository-wide DoD exists.

## Inputs and controls

The approved scene and close-up were opened visually before drawing. Roles/hashes are
in [reference-registry.json](reference-registry.json); visible invariants, palette and
budget in [style-contract.json](style-contract.json). Both arms use close-up crop
`(380,64)-(860,512)`, 480x448 source to 120x112 native (4:1). This is the prior crop
study framing, not a full-character equivalence or recommended production resolution.

The source is sufficient for this still's geometry/expression. A uses measured
source-coordinate polygons and sampled colors; B uses BOX reduction without dithering,
the same 48-color source-derived palette policy, traced binary silhouette and visible
semantic masks, then native hair/tie/lid/mouth cleanup. The palette is an experiment
control, not a project color cap. Some A colors are unused. Masks partition visible
samples only: no hidden body surfaces or complete rig are reconstructed.

Each arm had a blockout/seed and two artistic refinements. One optional hybrid follow-up
then restored the B01 mouth after final review caught a B02 regression. These are equal checkpoint
ceilings, not measured equal active labor; the trace route needed a technical repair.
No speed/effort causality or universal method superiority is claimed. The historical
redraw uses the same crop/grid but different history and effort, so it is context only.
[observations.md](observations.md) records decisions before advancing the corrected run.

## Concrete artifacts

| Artifact | Path / status |
| --- | --- |
| Original / A / raw B / cleaned B | [comparison.png](comparison.png); actual exports, original unresized, candidates 4x nearest neighbor |
| Trace native | [gated/a02-expression.aseprite](gated/a02-expression.aseprite); rejected as final treatment, retained |
| Converted/cleaned native | [b02-expression.aseprite](b02-expression.aseprite); retained with rejected mouth cleanup |
| Final selective rollback | [c01-restored-mouth.aseprite](c01-restored-mouth.aseprite); selected provisional bust |
| Central native / transparent PNG | [bust master](../../../assets/source/assisted-bust-v01/bust.aseprite), [bust export](../../../assets/export/assisted-bust-v01/bust.png) |
| Raw converted inputs | [prepared/converted-seed.png](prepared/converted-seed.png), unmasked seed and semantic masks in prepared/ |
| Source geometry / construction | [traces.json](traces.json), [prepare.py](prepare.py), [data.lua](data.lua), [build.lua](build.lua) |
| Native/display / layer structure | [native-and-display.png](native-and-display.png), [native-layers.png](native-layers.png) |
| Local revision | [localized-edit.png](localized-edit.png); duplicate-only tie edit, canonical cream design retained |
| Historical context | [historical-context.png](historical-context.png); not a third controlled arm |
| Generated intermediate + actual motion | [motion-reference-comparison.png](motion-reference-comparison.png) |
| Native blink / exported strip / timings | [blink master](../../../assets/source/assisted-bust-v01/blink.aseprite), [strip](../../../assets/export/assisted-bust-v01/blink-sheet.png), [layout](blink-layout.json) |
| Actual played preview | [GIF](blink-preview.gif), [local player](playback.html), [played screenshot](playback-playing.png), [review](playback-review.json) |

Original kit extracted as an evidence snapshot under `inputs/pixel_art_reference_lab`,
with its own manifest verified. Its instructions are reference material; the direct
user request and existing workspace remain authoritative. No competing workflow was
installed. Its findings/source register and prompt pack are linked from existing docs.
The package's original upload is preserved but current approved repo originals own
identity/style. All previous artwork and experiments remain unchanged.

## Visual assessment (agent, not user approval)

| Dimension | Trace A02 | Conversion route, final C01 |
| --- | --- | --- |
| Identity | Mapping retains hair/costume envelope, but face becomes generic | Same turned face/fringe/tied-hair identity survives substantially better |
| Expression | Weak graphic eyes, flatter cheek and over-simple mouth change the feel | Unequal eyes/rightward gaze and shallow restrained smile remain recognizable |
| Style / aesthetic | Broad flat planes and sparse marks lose original cinematic texture | Source clusters/colors preserve the intended language, with dense/muddy hair detail |
| Proportions / orientation | Framing controlled; cheek/jaw/fringe interpretation still differs | Source geometry is retained except intentional grid reduction and traced cutout edge |
| Pixel craftsmanship | Cleaner large planes but crude identity-bearing clusters | More convincing likeness; some noisy edge/highlight samples and flattened transitions remain |
| Editability | Nine semantic layers, isolated tie revision passed | Nine semantic visible parts, native feature cleanup and isolated tie revision passed |

Initial A/B and final C were inspected at 1x, 4x and a diagnostic projected 2x (240x224) bust display.
No game camera or full-character relationship is established. Warm/cool scene atmosphere
remains in the original; this test preserves local material relationships, not an
entire environment. Recommend the source-assisted conversion route (final C01) as the starting method for the next
same-character asset, with tighter mask/cluster cleanup. A is not an accepted alternative.

## Final selective rollback

The final enlarged mouth check [mouth-detail-review.png](mouth-detail-review.png)
revealed that B02's sampled mouth color erased the shallow smile's middle. The earlier
B01 mouth preserves the source expression better. Preserve B02 as a rejected mouth
attempt; C01 keeps B02's clearer eyes and restores exactly B01's separate mouth layer.
This is the optional hybrid follow-up justified by a specific failure, not an extra
unbounded redraw or a new comparison arm. [Original/C review](c01-review.png) was
inspected before selection. The unchanged strict native checker verifies that only
mouth pixels changed, with eight other layers and all metadata protected. The final
blink inherits the same mouth rollback; earlier motion sources/exports/evidence stay
under their original names and pre-rollback-evidence/. Central asset paths now identify C01.

## Supplementary image and motion boundary

After the conversion route's convincing provisional static result, one built-in generation requested an
open/half/closed blink sheet, using both canonical originals and B02 as a detail guide.
The exact prompt/attachments are in [generation-call.json](generation-call.json), based
on kit head-expression/key-pose prompts. Returned image is RGB 2029x775 with three
poses and gray background. It was reviewed for identity/style before use. It slightly
changes bun/strands/cheek/framing, so only eyelid-closure guidance was accepted for agent
use. It does not replace canonical identity, colors, proportions or crop. There is no
new human reference approval. No generated pixels were imported into native motion.

[motion.lua](motion.lua) initially retains B02 as base; [restore-mouth.lua](restore-mouth.lua)
then restores only the source-derived mouth on the final static and all motion frames.
The final probe keeps shared 120x112 canvas/palette, fixed crop
registration anchor `(64,104)`, zero root travel and five frames: 1600/50/90/60/600 ms.
Only the eyes layer changes. No per-frame fitting or scale adjustment. The five native
frames reopen/export exactly; eight other layers, cel geometry and silhouette remain
identical. The generated sheet need not be normalized into sprites because its geometry
is used only as pose guidance; native base registration is already shared.

The actual browser player cycled all five PNG frames at saved timings (AX events around
1600/1650/1740/1800 ms per cycle), and paused half/closed states were visually inspected.
[Playback evidence](playback-observed.txt) and screenshots preserve this. Blink reads as
closure/reopening with stable identity/volume, but closed lids are fairly straight and
half-lids look sleepy when held. This is a small expression probe, not proof of convincing
combat, secondary hair/tote motion, a timing-revision workflow or Godot readiness.

## Observed checks and limits

- [checks.json](checks.json): seven static native sources (six initial plus final C01), 120x112, nine named layers,
  binary transparency, exact RGBA fresh reopen exports. B00 exactly reassembles visible
  seed pixels from semantic layers.
- Three duplicate-only native tie edits pass the **unchanged** strict checker: A changes
  10 tie pixels, B and final C each change 23; other eight layers, native header/palette/non-cel metadata
  and cel metadata are protected. Reopened edit exports match. No checker exception.
- Scratch two-layer one-pixel edit/reopen passed; an all-protected negative mask fails.
  CLI pixel erase/skip semantics were not newly exercised; no grid-transparent patch API
  was used for this run. No current MCP drawing/connectivity/image-delivery claim.
- Motion: exact reopened five PNGs, stored durations, zero outside-eye changes, eight
  protected layers, unchanged alpha and exact return to starting export. Numeric checks
  and observed playback remain separate [reports](playback-review.json).
- [Fresh rebuild](rebuild-checks.json): A02, B02 and selected C01 PNGs match pixel-for-pixel after
  regenerating preparation data and native construction in a new temporary directory.
- Existing director utilities: 24 tests passed. Imported kit manifest verifies. Skill
  frontmatter parsed with Ruby YAML; bundled quick_validate could not run because its
  Python environment lacks PyYAML. No dependency installed to bypass that limitation.
- Preservation and exact artifact identities: [preservation-checks.json](preservation-checks.json)
  and [artifact-manifest.json](artifact-manifest.json). All pre-task artwork and prior
  experiments are unchanged; targeted workflow/research/skill/context changes are listed.

Technical failures are retained: initial A files under `unreviewed-batch/` contain a
cel-copy rendering bug and were saved before visual gating; they are excluded from the
method comparison. Fixed flush/one-checkpoint emission before the corrected reviewed
run. Preparation initially left mask boundary pixels unassigned (BOX/NEAREST mismatch);
consistent coverage fixed it. Scratch allowed-mask coordinates were corrected after
reading actual full-canvas cel geometry. These are disclosed implementation repairs,
not evidence of art acceptance. No historical failures were deleted.

## Reproduction

Use the bundled Python executable identified by load_workspace_dependencies (Pillow
12.3.0 here). From repository root, `prepare.py --out /absolute/new-folder` creates
source-derived data in a new folder. Create `new-folder/gated`, then run existing
Aseprite CLI `-b --script-param out=/absolute/new-folder --script-param arm=a
--script-param limit=0 --script-param destination=/absolute/new-folder/gated
--script docs/experiments/2026-10-27-assisted-head-comparison/build.lua`.
Inspect the actual export against the original, then repeat limit=1 and limit=2;
only the requested checkpoint is emitted and existing outputs are refused. Repeat
arm=b with the same out and limits (omit destination for B). `verify-native.lua`
performs fresh reopens and duplicate edit proofs. Run motion.lua with the retained B02/input/data, then restore-mouth.lua with B01 and B02
for the final C/static/blink variant. staticonly=yes reproduces only C01. The earlier
inputs and deterministic outputs remain retained; stochastic generation itself is
outside the deterministic boundary, so the returned source and exact call are retained.

Current native API details needed for new motion operations were checked against
[Aseprite Sprite](https://www.aseprite.org/api/sprite),
[Frame.duration](https://www.aseprite.org/api/frame) and
[Image:drawSprite](https://www.aseprite.org/api/image) documentation on 27 October 2026.
Other research uses the bundled dated source register; no new tools/algorithms installed.

## Decision, work accounting and next owner

The initial bounded request is delivered locally: guidance integrated, two candidate
methods tested, native sources/revision proofs/comparisons delivered and a small motion
probe actually played. User acceptance, full-body production treatment, representative
attack/contact, Godot validation, ongoing revision cost and publication remain open.
Two artistic refinements per arm, one source-supported mouth rollback and one supplementary generation were used; technical
repairs/replays are disclosed above. Exact active labor, draw-operation totals and model
cost were not captured, so no efficiency claim. started.json and final inventory timestamp
bound session wall time only, including docs/tool work.

**Next smallest action:** user reviews final C01 against the original and indicates whether
identity/style/expression are convincing enough to carry forward. Agent then applies
the selected source-assisted treatment to one full standing asset at an explicitly
chosen grid, improving silhouette extraction/cluster cleanup, before choosing a combat
camera/action. If C is still too noisy/soft, use the kit simplification prompt with the
canonical originals for a same-angle lower-detail reference and compare that source
at the same native grid; avoid another uncontrolled anatomy redraw. No manual repainting
is assigned to the user. No commits or publication were authorized/performed.
