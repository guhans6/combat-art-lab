# Pixel-art director setup and v03 head pilot

Date: 26 October 2026. Local working-tree artifact; base Git revision `9e35c5c13987a153e942e6f93f49f247fad13c3a`. No commit or publication.

## Outcome

The supplied director was installed as a canonical project copy in `tools/pixel-art-director`, with a project discovery symlink in `.agents/skills`. No existing extracted kit was located in the searched paths; the supplied `pixel-art-agent-kit.zip` was extracted into `/private/tmp/pixel-art-pilot-kit` and its skill read there. The older `combat-art-lab.zip` was not reapplied over this working tree. The user's explicit request controls scope; the kit's suggested later repeated-model benchmark was not run.

Pebbly 0.8.2 is installed locally under ignored `.art-tools/pebbly`, with a dependency lock and the registry archive preserved there. Its launch is pinned to the installed local entrypoint in `.codex/config.toml`. Only this project’s Codex configuration was created. No global or other-client configuration was written. Existing Aseprite was reused; no extension, editor update, paid service, or image generator was installed or used. Raw Lua stayed disabled.

The actual current model was `gpt-6.1-sol`, high reasoning, confirmed from this chat's turn context. Host execution origin is Codex Desktop. The installed desktop bundle reports ChatGPT `26.1021.31345` build `21828`; CLI `0.162.1`. macOS `26.6.2` arm64, Node `26.9.0`, bundled Python `3.12.14`, Pillow `12.3.0`, Aseprite `1.3.18.6-dev`. Backend npm gitHead: `5894b12cead839789077b279369409f868451ffc`; resolved MCP SDK `1.32.2`. Exact transitive versions and integrity hashes are in `package-lock.json` and `resolved-node-dependencies.json`.

## Configuration versus observed operation

`codex mcp get aseprite-ai-artist --json` successfully read the project configuration. This chat's already-loaded native tool catalog did not expose the new server. Rather than claim discovery proved setup, the current model operated the actual pinned MCP server through a small logged stdio adapter, using the same desktop host’s shell tools. MCP `look` returned image bytes, which the adapter saved without alteration and the host's `view_image` delivered to this model. Native image read, pixel read, draw, export and save/reopen were exercised through this route.

The configured automatic MCP launch/tool exposure after a desktop chat reload is **not yet observed**. This is a remaining client-enablement boundary, separate from the passing adapter-based toolchain proof. Next owner: the next Codex session can invoke `preflight` and `look` from its normal MCP catalog; if unavailable, inspect the project setting/reload behavior. The tested adapter remains in `session-adapter.mjs` and `rpc-adapter.py`; it is not another model or a replacement drawing backend. The pilot-owned server was stopped after saving all files.

## Setup evidence

- Inventory found the existing editor, Node, uv and Codex, but no configured Aseprite server. The default Python lacked Pillow; the bundled runtime already had Pillow 12.3.0, so no Python package was installed.
- Reviewed exact npm package manifest, MIT license, CLI, surgical installer, headless runner, drawing/inspection schemas, fix workflow, and source INSTALL/SECURITY at the npm commit. Archive SHA-512 matched registry metadata. Installation used `--ignore-scripts` and a separate temporary cache after the default cache returned EPERM; no cache ownership was changed.
- Installer dry-run proposed `@latest` despite the exact installer version. The actual project launch instead points to the locked local build. No whole-client installer or AGENTS merger ran.
- The shell sandbox aborted the editor's initial version probe. Approved targeted escalation allowed the existing binary/headless session to run; no persistent sandbox settings were changed.
- `smoke/checks.json`: 16x16, two named layers, asymmetric red L with green right branch, isolated blue pixel at (12,4). Returned previews were visually inspected. Exact pixel reads matched. A one-pixel selection clipped an attempted adjacent write. Exactly one composite/native pixel changed and the protected layer stayed equal. Native close/open yielded a matching fresh PNG. Transparent skip preserved the pixel; default grid transparency erased it. A deliberate (15,15) out-of-mask write was rejected independently.
- All 18 supplied utility tests passed under the bundled runtime. The independent native reader was corrected for a local variable shadowing bug before reporting checks; it then passed the scratch proof and separately rejects the out-of-mask native scratch change. It refuses unsupported cel encodings rather than silently ignoring them.

The headless backend is file-capable rather than an enforced workspace sandbox. This run used only new scratch and candidate paths. No live bridge/extension or user editor documents were used.

## Frozen trial

Run: `art-runs/2026-10-26-gpt61-sol-pilot-01`. `task.json` retains the supplied combat-art-lab-v03 profile. The baseline is exactly `assets/source/standing-v03/standing.aseprite`, never v04 or a background scene. Frozen originals, copies and reference SHA-256 values are in `frozen-inputs.json`. Native composite matched the supplied baseline PNG. The four allowed layer names exist, and the generated mask matches `edit-head.lua` at all 24,576 coordinates: x34..79/y2..30, excluding neck notch x57..65/y29..30. Native canvas 128x192, one 100ms frame, 12 layers, 52 palette entries including transparency, 51 visible RGB colors.

The complete close-up and scene were viewed before editing. `observations.md` records visible differences, approximate landmarks, confidence, hypotheses and review outcomes. Eye centers were retained; there was no assumed requirement to move them closer.

Two visual passes were run, within the three-pass budget. The art phase used 34 MCP calls (034..067); setup used 33 separately. Host shell/vision orchestration is additional, so this is not a pure cross-host tool-count benchmark. MCP art interval was approximately 207 seconds; setup and reporting time are excluded. Cost/token charges are unknown. No human drawing, extra critic, subagent, seed control or paid generation was involved.

Pass 01 changed six feature-layer pixels: far-iris continuity and a shallow smile. Pass 02 tested rear-hair contour cuts: 26 hair-layer changes, 32 total composite changes. Both passed protection checks. Pass 02's angular opening looked less convincing than the reference's curled clumps; it is retained as a rejected alternative. Pass 01 was restored as the final candidate. No third pass was made.

One fully transparent pixel in pass 01 produced a palette-lock notice about its invisible RGB. A subsequent exact pixel read confirmed alpha remained zero. Final independent checks found no new visible color, partial alpha or silhouette change. Grid/clear erasure is clearer for subsequent edits.

## Deliverables and verification

- `work/candidate.aseprite`: selected layered native candidate.
- `work/candidate.png`: transparent native 128x192 export.
- `evidence/reference-before-after-head.png`: both primary references and baseline/candidate heads.
- `evidence/reference-before-after-full.png`: primary scene and full sprites at 3x.
- `evidence/native-and-zoom-difference.png`: actual 1x sprites plus 8x head and exact visible difference.
- `passes/`: both native/PNG checkpoints and independent PNG/native checks.
- `evidence/all-checkpoints-head.png`: selected/rejected comparison.
- `evidence/edit-history.json` and `evidence/mcp-operations.json`: exact RGBA edits and actual drawing requests/results. Full setup+trial logs and raw returned preview images are in this record's `backend-session/`.
- `evidence/final-native-checks.json`: all non-cel chunks equal, including palette/tags/layer order/flags/visibility/opacity/blend; frame timing and canvas equal; all cel positions/dimensions/opacity/z equal; all hidden/protected layer pixels equal. Only six pixels on `11-face-features` differ. Both skin and hair layers remain exactly equal in the selected candidate.
- `evidence/native-reopen-checks.json`: actual MCP close/reopen and a fresh RGBA-identical export. Native SHA-256 and PNG hashes identify the delivered files.
- `preservation-checks.json`: all 206 pre-existing art/context/doc files hashed before setup remained byte-identical before the additive handoff update. Later versions and uncommitted art were preserved. Handoff was then appended with this milestone; its existing prefix was preserved and separately checked.

## Remaining uncertainty and next owner

This is a small expression correction, not an established likeness improvement. The hair still reads round and bright, the chin is pointed, eye shapes are simplified, and the smile is square at enlarged scale. The user owns artistic selection after comparing the actual output. No visual approval or numerical human score is inferred. No animation, Godot playback, production readiness or publication is claimed.

Automatic client MCP exposure after reload remains untested; the actual drawing/image/pixel/native workflow through the current host adapter is proven. Human next action: review the selected pass's identity/expression and decide whether to keep it. Agent next action, after that direction: resolve one observed head discrepancy in a new isolated run, preserving this evidence.

## Primary sources inspected on 26 October 2026

- [Official Codex MCP configuration](https://developers.openai.com/codex/mcp/) and [local skill discovery](https://developers.openai.com/codex/skills/): project config and symlinked `.agents/skills` support. Configuration does not establish runtime image delivery.
- [Pebbly installation](https://github.com/with-pebbly/aseprite-ai-artist/blob/5894b12cead839789077b279369409f868451ffc/docs/INSTALL.md), [security boundaries](https://github.com/with-pebbly/aseprite-ai-artist/blob/5894b12cead839789077b279369409f868451ffc/SECURITY.md), and npm archive/metadata at 0.8.2. The exact local schemas and source were also read.
- [Aseprite native file specification](https://github.com/aseprite/aseprite/blob/main/docs/ase-file-specs.md), used for independent native chunk/pixel verification. This custom checker is scoped to the observed RGBA source, not a general format certification.
