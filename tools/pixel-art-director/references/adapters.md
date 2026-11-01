# Drawing backends and capability contract

Inspected 2026-10-26. Tool names below are discovery hints, not substitute schemas.
Read the connected server's live tool definitions before issuing calls. Prefer
one selected backend for an entire experiment, and record its version or commit.

## Required capabilities

| Need | Pebbly candidate | Diivi alternative | Existing CLI/Lua |
|---|---|---|---|
| Inventory document | `preflight`, `sprite_info` | `get_sprite_info` | open source and inspect native objects |
| See artwork | `look` preview/region | `view_sprite` | PNG export + host image-read tool |
| Read exact pixels | `look` ASCII, `read_pixels` | `read_rows`, pixel/rect queries | native image pixels |
| Patch clusters | `draw` grid / scoped operations | `draw_rows`, pixel operations | masked Image edits |
| Scope writes | selection + layer + region | explicit layer/region, verify exact mask | enforce mask in write function |
| Verify change | diff/validation + independent checks | `compare_frames`, bounds/lint + checks | independent PNG/native checks |
| Save editable source | `sprite_manage` save-as | file-backed native source | native saveAs |

### Pebbly: recommended first integration to test

Use the existing `fix` workflow for local correction, with `review`/`export` as
needed. For new construction, use `brief`/`draw`/`shade` as subordinate procedures.
The custom director supplies source priority, project locks and evaluation rules;
do not install several competing top-level art routers into the same session.
Load the relevant skill/rules only, rather than the entire knowledge corpus.

The tool's `look` ASCII path and `draw` grid path form a read/edit/write loop.
Keep palette legend and origin attached to each region. **Transparent cells erase
by default; `transparent:"skip"` is additive behavior.** Test this in a scratch
sprite. Do not round-trip a partial grid without understanding its blank cells.

For source-assisted raster construction, test the actual paint-layer entry point
before declaring an import blocker. A reference-layer import is a different role
from opening a PNG as an ordinary editable document. On the project's tested
Pebbly0.8.2/headless host, `sprite_manage open` on a PNG produced an editable RGB
paint layer; native save and a one-pixel grid revision were verified. Use the
discovered layer-copy or grid path to construct target parts, and verify it on a
scratch document in the receiving host. A flattened import alone remains a seed;
retain meaningful parts, correction inputs and a demonstrated native revision.

Live mode edits the open Aseprite session. Headless is an explicit alternative
using batch Aseprite. A failed live connection is not permission to write the
same document on disk. Check the live owner's unsaved changes before any mode
change. Keep raw Lua disabled unless a required task and permissions justify it.

Sources:
https://github.com/with-pebbly/aseprite-ai-artist
https://github.com/with-pebbly/aseprite-ai-artist/blob/main/skills/fix/SKILL.md
https://github.com/with-pebbly/aseprite-ai-artist/blob/main/docs/INSTALL.md

### Diivi: credible alternative, not a primitive-only legacy server

The current project has regional image feedback, compact pixel rows, animation
inspection and native file operations. Its larger tool surface may be useful for
batch tasks; it is not evidence of better likeness. Use `view_sprite` after each
pass, not only at final export. Learn the actual frame/index conventions.

**`draw_rows` dots/unknown symbols leave existing pixels untouched.** Erasing
needs an explicit erase operation or another verified representation. This differs
from Pebbly's grid default. Verify selection coverage and transparent round-trips
on the installed revision before writing a production patch.

The README currently calls for Python 3.13+ and uv. Pin a reviewed repository
commit and lock dependencies, then configure the local module entrypoint. Do not
use Docker/Steam credentials merely because the README offers them; the user
already has a compiled Aseprite installation. Unrestricted `run_lua_script` is a
code-execution capability, not a harmless image filter.

Source: https://github.com/diivi/aseprite-mcp

### Direct Aseprite CLI/Lua: keep as the control condition

The project already records successful construction, save/reopen and local edits
through this route. The skill remains usable without an MCP. Preserve readable
Lua/drawing inputs and inspect exported images through the host's vision tool.
Do not replace a requested MCP test with this route silently. A separate CLI run
is useful for checking whether the MCP actually improves the feedback loop.

Source: https://www.aseprite.org/docs/cli/

## Optional tools not selected by default

MalloyTheDev's MCP exposes pixel-map operations, diffs, native workflow helpers and
script-reproducible showcases. Its broad analysis suite is worth testing later if
it solves a measured gap. Shape/stray-pixel scores still cannot assess facial
identity. A mathematical showcase proves a drawing operation, not autonomous
reference fidelity.
https://github.com/MalloyTheDev/aseprite-mcp

Image generators, PixelLab-style services and generic PNG renderers belong in a
separate concept/alternative-pipeline track, with explicit cost and provenance.
Do not substitute them into a native pixel-edit benchmark and claim the drawing
model alone produced the improvement.

## No universal compatibility promise

An MCP client must deliver image content to the selected model, permit the needed
local tools, and expose resources or an equivalent file-read path. Slash-command
names and configuration formats are host-specific. A resource advertised by the
server is not proof that this host/model can consume it. The smoke test decides.
