# Research: portable, evidence-led pixel-art agents

Research date: 26 October 2026. Prepared for the user's combat-art-lab character
workflow. This report separates inspected source, published demonstrations,
local utility tests, and experiments that still need to run on the user's machine.

## Recommendation

Keep Aseprite as the native editor. Test **Pebbly Aseprite AI Artist** as the first
cross-agent integration, with this small project-specific director skill above
its existing edit/draw workflows. Keep **Diivi Aseprite MCP** as the principal
alternative and the existing **CLI/Lua** process as a control condition. Do not
install three editors or three servers to answer one face-likeness question.

This choice is about inspectable operations, image feedback, scoped revision and
portable instructions. It is not evidence that Pebbly, or any particular model,
will reproduce the approved face better. Only a frozen-input visual test can
answer that for this asset.

## What the existing project actually does

Read through Code-MCP: root AGENTS.md, CONTEXT.md, GLOSSARY.md, handoff, ADR 0001,
style guide, Git status, and `assets/source/standing-v03/edit-head.lua`.

The source opens a layered native v02, edits permitted head-layer images through
Lua pixel/polygon/line operations with a hard mask, saves v03, exports PNG, and
reopens the result. The project records an installed Aseprite 1.3.18.6-dev and
successful earlier local-revision checks. These are existing records/source,
not fresh Aseprite runs performed in this research session. The records state no
new MCP was installed for that work; global client configuration was not audited.

The working tree contains substantial uncommitted/untracked art. Later v04 and
background work also exist in the records. The comparison must copy named v03
inputs rather than commit, reset, replace or automatically select later files.
The current 128x192 grid is an experimental project choice, not a measured native
resolution of Until Then. The v01 45-color figure is not a global palette rule:
the style guide records 51 for v02 and no new colors for the v03 correction.

Important reference priority: approved close-up and full scene first, generated
cutout second. The style guide explicitly keeps the primary images authoritative
when the cutout introduces artifacts. A future model should not be forced to
reproduce every detail of a subtly changed image-generator extraction.

## Tool and skill assessment

### Pebbly Aseprite AI Artist — recommended pilot

Inspected README, installation/security docs, package manifest, fix skill, gallery
entry and benchmark/rubric. Source version observed: 0.8.2, Node >=22.6.0.

Useful fit: existing project workflows, regional image/ASCII inspection, palette-
aware grid editing, scoped changes, native saves, explicit live/headless modes,
and undo-oriented editing. Reuse the `fix` procedure rather than inventing another
pixel editor. Our director adds strict source priority, identity observations,
protection rules and fair comparison. In headless mode the live extension is not
needed. The host still must actually deliver images to the selected model.

Security limits matter: the live localhost bridge is not authenticated against
other local processes, and file paths are not confined by a sandbox root. Treat
installation as granting local editing authority. Pin the actual server launch,
not only an installer command. Use scratch files and disable raw Lua by default.

Sources:
- https://github.com/with-pebbly/aseprite-ai-artist
- https://github.com/with-pebbly/aseprite-ai-artist/blob/main/package.json
- https://github.com/with-pebbly/aseprite-ai-artist/blob/main/docs/INSTALL.md
- https://github.com/with-pebbly/aseprite-ai-artist/blob/main/skills/fix/SKILL.md
- https://github.com/with-pebbly/aseprite-ai-artist/blob/main/SECURITY.md

### Diivi Aseprite MCP — credible alternative

Inspected current README, not just old launch-era descriptions. It now documents
image feedback through `view_sprite`, compact pixel rows, regional reads, layer
exports, bounds/diffs, palette inspection and animation utilities. It is therefore
incorrect to dismiss the current version as a few primitive drawing functions
without visual feedback. Its broader API is useful for explicit file/batch work.

Use it when that backend suits the chosen host or a measured pilot favors it.
Preserve its exact commit and dependency lock. Its current README requires Python
3.13+ and uv. Do not assume its row transparency semantics match Pebbly's.

Source: https://github.com/diivi/aseprite-mcp

### MalloyTheDev Aseprite MCP — optional specialist alternative

The README describes native headless editing, pixel maps, preview images, diffs,
animation metrics, no-clobber defaults and workspace-scoped paths. It also links
script-reproducible showcases. These support investigation of its tool behavior,
not a claim that its automatic scores measure human-face resemblance. It is not
necessary to add this large tool surface to the initial experiment.

Source: https://github.com/MalloyTheDev/aseprite-mcp

### Existing pixel-art-studio skill — do not import wholesale

Inspected the actual SKILL.md in AnastasiyaW/codex-claude-code-config. It provides
programmatic rendering and review concepts, but also imposes defaults such as
32x32 for vague requests, blanket restrictions on lone pixels, and a numerical
quality threshold presented as sufficient to ship. Its renderer is not itself
proof of native Aseprite editability. Those rules conflict with this task's
existing grid, meaningful single-pixel facial features and human likeness review.

Retain only the general idea of staged creation and separate evaluation, written
here independently. No third-party scripts, large rule corpus or auto-scoring
criteria from that skill are bundled or executed.

Source:
https://github.com/AnastasiyaW/codex-claude-code-config/blob/main/skills/creative/pixel-art-studio/SKILL.md

### Installed skills and portability

Used the installed writing-for-agents guidance to structure the skill as ordered
steps with observable completion conditions and branch-specific reference files.
The installed sprite-pipeline skill's approved-seed and stable-anchor principles
are relevant for later animation, but its generator-oriented strip workflow is
not a substitute for native pixel correction.

Use Agent Skills-compatible name/description frontmatter. Hosts still differ in
skill discovery, MCP prompts/resources and image delivery. The portable fallback
is a direct file read of the same SKILL.md. Gemini and Claude documentation were
checked for skill/MCP support; no cross-client execution was performed here.

Sources:
- https://agentskills.io/specification
- https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL-MECHANICS.md
- https://geminicli.com/docs/cli/skills/
- https://geminicli.com/docs/tools/mcp-server/
- https://code.claude.com/docs/en/skills

## Demonstrations and what they establish

### 1. Independent tool-calling drawing experiment

LJ Miranda's 20 July 2025 article, *Draw me a swordsman*, publishes model outputs,
a tool-based setup and evaluation notes. The four-frame Opus example image was
retrieved and visually inspected: a simple small humanoid with sword-direction
changes. This is real visible output, but far below the facial-detail problem
here. The article chooses the best of three runs; its historical model results
are not a current ranking. Its older tool limitations should not be attributed
to Diivi's current expanded implementation.

https://ljvmiranda921.github.io/notebook/2025/07/20/draw-me-a-swordsman/
https://ljvmiranda921.github.io/assets/images/draw-me-a-swordsman/claude-opus_spritesheet.png

### 2. Concept/storyboard to native character animation

Pixeli's *Blacksmith fire slam* record documents a 64x64, eight-frame attack,
supplied image-model concept/storyboard, model/host/plugin information, prompts,
PNG/GIF links and a downloadable .aseprite source. It discloses four human
interventions, including supplying references and approving two critique rounds.
The page's own art-craft rating is still absent.

This is a relevant published workflow, not a verified result on the user's
character. The record/links were inspected; the hosted strip image could not be
retrieved in this session, and the native file was not opened locally. Therefore
this report does not claim to have verified its visual fidelity or native layers.

https://pixeli.pebbly.space/g/2026-09-29-blacksmith-fire-slam

### 3. A benchmark that separates correctness from craft

Pixeli's Boombox Mage page reports one run with 15/15 compliance checks but only
30% craft. That is a useful warning against treating a valid export or clean lint
as good art. The table mixes plugin versions, shows best runs, and has sparse
human judging. It does not establish a fair universal model winner or predict
which model will match this face.

https://pixeli.pebbly.space/benchmarks/boombox-mage
https://github.com/with-pebbly/aseprite-ai-artist/blob/main/gallery/RUBRIC.md

### Evidence conclusion

There is enough published evidence to justify testing tool-directed native art.
There is not enough inspected evidence to promise reference-accurate facial
reconstruction at this resolution. The appropriate next evidence is a local,
repeatable, blinded comparison, preserving every attempt and intervention.
Marketing claims, stars, tool counts and uninspected social-media clips are not
used as proof of drawing quality.

## Pixel-art learning sources and adopted lessons

### Cure — PixelJoint, *The Pixel Art Tutorial*

Primary tutorial text inspected. It distinguishes deliberate pixel control from
simply using a small image or non-blurring software, discusses clusters, edge
handling and manual anti-aliasing, and allows tools such as fills without requiring
every pixel to be individually clicked. Adopt the cluster/contour review, not a
rule that every isolated facial pixel is forbidden.

https://pixeljoint.com/forum/forum_posts.asp?TID=11299

### Pedro Medeiros / Saint11 — consistency and social-first tutorial archive

Primary article inspected: separate resolution, palette and stylistic consistency;
use intentional scaling and internal consistency. His tutorial archive explicitly
states its cards were originally focused on Twitter. This provides an attributable
social-media-origin teaching source rather than unsourced reposts. The archive
was located; individual tutorial cards were not all inspected or copied.

https://saint11.art/blog/consistency/
https://saint11.art/blog/pixel-art-tutorials/

### AdamCYounis — *Pixel Art Class: Character Heads* (YouTube)

Located the original video. The accessible page exposed title/metadata, not a
usable transcript or full visual sequence, so this report does not claim the
lesson was watched or extract specific timestamped advice from it. It is a
focused follow-up learning resource for head construction.

https://www.youtube.com/watch?v=j2sjA9wLHpE

### Brandon James Greer — pixel-art fundamentals / review videos

Located the beginner playlist and secondary references to *How to "Proofread"
Your Pixel Art (5 Review Tips!)*. The primary video's full content was not
retrievable here. Treat it as a learning lead, not evidence for claims about a
technique the research agent supposedly observed. The executable workflow's
rules are grounded in the readable primary tutorials and the actual project.

https://www.youtube.com/playlist?list=PLxfQIomHccxvoTON6hXhfZyAUdFXd-z1P

## What the new skill changes

The cycle becomes: inspect original and native sprite; record visible discrepancies;
choose one small change; read exact pixels; edit under a mask; inspect at native
scale and zoom; verify protected data; retain or revert; repeat within budget.

For faces, the observations concern eye centers/near-far sizes, eyeline, nose axis,
cheek-to-chin silhouette, fringe openings, ear overlap and expression. The skill
explicitly rejects a universal instruction to move eyes closer, and does not
mistake the existing v03 pupil coordinates for ideal target values. Detailed
landmark arithmetic is only justified where the reference actually supports it.

For new construction, silhouette and major material planes precede accents.
For animation, approved key poses, timing and stable anchors precede in-betweens.
For all tasks, correct files and good-looking art are reported separately.

## Delivery verification boundary

The included scripts create frozen copies, generate the exact head mask, check
PNG properties/protected pixels, create nearest-neighbor comparison sheets, and
inventory executable versions. Synthetic unit tests exercise their failure paths.
They do not call models, install servers, execute Aseprite, or judge artistic
likeness. The included setup procedure must be run on the host before claiming a
working drawing integration. No current asset was refined or published here.
