# Four-model evidence-guided idle experiment

30 October 2026. User request: use the evidence ZIP in chat
`01a18cd0-a2a3-7b11-bdc7-ac7d5478e755` to make idle animations for the current
character with Luna5.6Max, Luna6Max, Terra5.6 and Sol6.1, independently in fresh
contexts. Parent is orchestration/technical checks only.

## Inputs and protocol

[Common brief](BRIEF.md), [frozen input manifest](input-manifest.json).
ZIP source: AgentWatch `output/2026-10-30-pixel-idle/pixel-idle-evidence-pack.zip`.
Its SHA256 is `d1b8998eb2eace9e74062a7afb3c5bc0e8711a6666ef95c8c723ac134eb65457`.
All248 entries passed ZIP integrity/path checks and were extracted locally. Pack
limitations (missing creator source/project, exact palette and cel timings) remain
explicit. The tutorial supplies motion-workflow evidence, not the character design.

Common neutral native SHA256:
`d76266fa8afcd1de643e6b6421ec4dfe4fa77f8044a1d083205b921eb2f25540`.
Offline native read confirms its single128x192 frame equals the shared neutral PNG.
All artists receive identical originals, baseline, optional existing blink, evidence
pack and constraints. Input/protection snapshots precede construction. No artist
sees another contestant's work; no parent drawing recipe/critique/rescue is supplied.
Each has one construction pass plus at most one self-identified artistic correction.
The independent timing and method choices are part of each end-to-end result;
this is not an isolated measurement of model drawing ability or cost.

## Assignments and editor coordination

All four `spawn_agent` calls explicitly use `fork_turns="none"` and a self-contained
brief. The user-requested models override normal cheaper-profile routing.

| Artist | Exact requested model/effort | Owned output | Agent |
| --- | --- | --- | --- |
| Luna5.6Max | gpt-5.6-luna/max | `luna56-max/` | `/root/idle_luna56_max` |
| Luna6Max | gpt-6-luna/max | `luna6-max/` | `/root/idle_luna6_max` |
| Terra5.6 | gpt-5.6-terra/medium | `terra56/` | `/root/idle_terra56` |
| Sol6.1 | gpt-6.1-sol/high | `sol61/` | `/root/idle_sol61` |

Max is explicitly requested for the two Lunas; Terra medium and Sol high are the
declared orchestration choices. All requested model launches were accepted. No
fallback, cross-agent collaboration or extra reviewer model is allowed.

Dedicated MCP preflight before dispatch: ready, headless, Aseprite1.3.18.6-dev,
Pebbly0.8.2, no open sprite. Artists prepare in parallel and request exclusive
native-editor leases. The parent grants one at a time, then moves to the next on
explicit release. All native drawing/save/export remains dedicated MCP. No direct
Aseprite CLI/Lua launch, UI, Code-MCP, new installation, imagegen substitution,
global configuration, commit, push or publication is authorized by this experiment.

## Completion boundary

Deliver four independent attempted native loops with actual exports/timing, faithful
1x/3x previews, operations, separate visual decisions and scoped technical evidence.
Report any failed/blocked candidate honestly without substituting another model.
Parent verifies inputs/protected history and delivered artifacts, presents outputs
without choosing a visual winner, and updates the handoff. Native proof, temporal
observation, user art approval, other-project installation and Godot gameplay are
separate claims. No repository-wide Definition of Done is added.

## In-progress checkpoints

- Terra56 released the first editor lease with an8-frame/740ms loop. Parent native,
  PNG and visible GIF timeline checks passed. The worker's raw GIF-RGBA-versus-PNG
  inequality was due to comparing transparency/matte differently; visible composited
  RGB/timing are exact. A later full-pixel body alpha check flagged61/54/54/64 new
  enclosed gap pixels on F3–6. Terra independently confirmed exposed cel seams and
  prepared a focused technical repair. Its first delivery is retained as evidence;
  it is not yet technically cleared.
- Sol61 released the second lease and delivered8 native frames/3380ms; both GIFs
  preserve the visible timeline (one identical hold merges to7 encoded frames).
  Parent independently passed native/export/palette/existing-layer/shoes/guide,
  rest and binary-alpha/new-body-hole checks. Reopen-export pixel multisets match;
  the separate duplicate revision changes exactly one native pixel. Artist source
  decisions and actual-speed/Godot/user-approval boundaries remain its record's claims.
- Luna6Max holds the third editor lease. Luna5.6Max has a reserved first-pass slot;
  it has not yet received native access. No contestants see each other's outputs.

Later checkpoint: Luna6 released and delivered its first10-frame/2390ms candidate;
parent technical checks passed. It independently requested its one available artistic
correction after its own contact-sheet review; no parent art critique was supplied.
Luna5.6 released its fourth lease and delivered6 frames/1700ms. Native/export/GIF
timeline and source protections pass, but the same body-alpha checker flags64/44/83/65
new enclosed gap pixels on F2–5. Coordinates were returned only to that artist for
independent technical investigation. Terra has lease5 for its prepared seam repair;
Luna6's artistic correction is queued sixth and Luna5.6's technical repair seventh.

The Luna5.6 actor was interrupted/resumed once during an extended silent preparation
phase to resolve readiness/queue status. It continued the same independent assignment,
exact model and Max effort, with its own saved context/files and no parent transcript
or other artist recipe. It subsequently completed native work; no model substitution
or claim of model unavailability was made.

All artists received the same environment clarification (existing bundled Pillow,
no installation) and the same layer-scope clarification: existing named metadata/order
stay intact; declared normal-blend animation overlap backing layers are permitted.
This accommodates meaningful native animation structure rather than imposing exact
layer-count equality. Any addition must be declared and keep rest/guide exact.
Technical findings are returned only to the originating artist, without art direction
or another model's recipe. Repairs/retries are recorded separately from art passes.

Coordination evidence: [editor lease log](editor-leases.json),
[Terra first technical check](terra56-parent-check.json),
[Sol technical check](sol61-parent-check.json),
[supplemental reopen/revision checks](parent-supplemental-checks.json).

## Final delivery and observed acceptance

All four requested exact-model artists delivered an editable native loop and faithful
PNG/GIF evidence. Final sources, frame counts and authored loop durations:

| Artist | Native | Frames / cycle | SHA256 |
| --- | --- | --- | --- |
| Luna5.6Max | `luna56-max/technical-repair/luna56-idle-repaired.aseprite` | 6 / 1700ms | `f7aa4235209d78823d7fe769e4ba53035692bc014d1af2e5fda11af93ed655d9` |
| Luna6Max | `luna6-max/idle-candidate-corrected.aseprite` | 10 / 2390ms | `57d27225db3b800816bf8399fbd0443188cca4ed1fab41b641c2194de953bbe4` |
| Terra5.6 | `terra56/native/terra56-breathe-seam-repair.aseprite` | 8 / 740ms | `9db6aa3cce3210376b6b6ce9b3f013f8798dd59b70fecf13adff7453ce7d5df8` |
| Sol6.1 | `sol61/pass01.aseprite` | 8 / 3380ms | `e93d058a373ef5329ee862523a966e6db225ee0f5ba6fafd294a574b34b6c6c5` |

The [entrypoint](README.md) links all native files, previews, artist records and
the [animated comparison](comparison/index.html). Each independent loop retains its
own timing at a common matte and scale. No loop is stretched to match another.

Luna6 used its one self-requested artistic correction: it moved an existing shirt
crease by one pixel at the peak, changing four color values. Its initial source,
exports, checks and record remain separate. Sol used one main art pass with a
small collar-overlap technical repair. Terra and Luna5.6 retained their first native
deliveries and independently repaired only parent-flagged alpha seams, using declared
normal-blend backing layers. Parent independently confirmed all original cels are
exact in those two repaired sources and every changed composite coordinate is a
flagged gap filled with its neutral-source value: [Terra delta](terra56-parent-repair-delta.json),
[Luna5.6 delta](luna56-max-parent-repair-delta.json). This does not score their art.

During Terra's repair queue, the actor was discovered already interrupted, not
actively editing. A nonmutating readiness probe reported ready/no active document;
the same Terra actor/model/effort was resumed with its own prepared repair. No
substitution was made. Its repaired source/PNGs and later faithful GIFs were delivered,
while its final native reopen was honestly left for the coordinator's read-only audit.

Fresh final verification:

- All four [parent technical deliveries](parent-technical-checks.json) pass: declared
  dimensions/timings, exact native/PNG pixels, rest, original layer metadata/order,
  native palette chunks, hidden guide/shoes, binary alpha and no newly enclosed body
  holes under the declared body-region check. Original source hole at63,116 is
  inherited unchanged; this check is not a complete silhouette/art-quality verdict.
- All four1x/3x artist GIFs equal the intended native visible timeline. Merged identical
  holds are handled by timeline equivalence. [Common-matte GIFs](comparison/manifest.json)
  likewise pass exact1x/3x comparisons with explicit palettes and no quantization.
- Parent exclusively reopened **each final saved native through dedicated MCP**, read
  metadata, exported a horizontal PNG/atlas, then closed it without drawing or native
  resave. All**32** fresh frame crops and atlas durations match independent native
  composition and delivered PNGs; all four source hashes remain exact. Final document
  list is empty. [Reopen verification](parent-reopen/verification.json),
  [actual MCP calls](parent-reopen/mcp-log.json). This supplies Terra's missing final
  repaired-source reopen boundary as well as uniform final checks for the others.
- All**2,791** pre-existing files under assets/experiments, all six frozen common
  inputs and all**248** extracted evidence files match their recorded originals/ZIP.
  No old art, blink, historical experiment or archive was modified.
- The parent timing verifier accepted legitimate merged holds and rejected altered
  pixel/timing fixtures. Actual initial alpha failures were detected and became green
  after the artists' own repairs. This is focused mechanical evidence, not an art score.

The parent owns only orchestration, shared input preparation, technical findings,
read-only reopen/export proof and faithful comparison packaging. No parent drawing,
recolor, animation edit, artist substitution or cross-contestant art critique occurred.
All four began with explicit fresh contexts; subsequent continuations concerned only
that artist's own work. Different decisions/retries remain part of each end-to-end
result; no isolated quality/cost ranking is justified.

**Remaining owner/action:** user compares movement, material appearance and expression
separately on the actual timed candidates. No winner or whole-animation approval is
inferred. Actual-speed viewing by the agents, Godot/gameplay proof, production readiness,
other-project installation and publication remain unperformed. A later selected/scoped
animation revision or engine test belongs to a subsequent user-directed task. No
manual repainting is assigned to the user. No commit, push, global config or new install.
