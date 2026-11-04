# Use the conversion and Aseprite workflow on another machine

Prepared 5 November 2026. Use branch `work/new-character-ready`: `main` still
contains the initial workspace setup, not the later conversion pipeline.

```sh
git clone --branch work/new-character-ready https://github.com/guhans6/combat-art-lab.git
cd combat-art-lab
```

The clone includes conversion scripts, reviewed recipes/masks, source images,
native examples and the complete `tools/pixel-art-director` skill. It does not
include installed Python/Node packages, Aseprite or Godot applications, global
skills, credentials or the old machine's tool caches. Historical reports retain
the paths of their original runs; those paths are evidence, not setup inputs.

For Dot or another hosted agent environment, have the agent inspect the execution
host first: run `python3 -c "import platform; print(platform.system(), platform.machine())"`,
`node --version` and `npm --version`, and locate an existing Aseprite executable.
The browser/device displaying the chat does not identify the execution host's OS.
Run setup in the host that will actually execute the converter and MCP. If that
host has no Aseprite executable or cannot run a local stdio MCP server, PNG
conversion can still work, but native automation needs a compatible host/tool
connection. This publication has not tested Dot's runtime or its MCP support.

## 1. Install the conversion runtime

Use Python 3.11+ with venv/pip. From the repository root on macOS/Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r learning/aseprite/automation/requirements.txt
```

On Windows, use `py -3 -m venv .venv` and substitute
`.venv/Scripts/python.exe` for `.venv/bin/python` in the commands below.
The frozen conversion dependency is Pillow 13.0.0. It also serves the director's
Python checks; the older director requirements alone permit versions too old for
this converter's `get_flattened_data()` API.

Replay the included reach conversion into a new output directory:

```sh
.venv/bin/python learning/aseprite/automation/convert_image.py --recipe learning/aseprite/automation/reach.json --out .scratch/reach-portability-check
```

Compare `converted.png` with
`learning/aseprite/practice/reach-script-2026-11-01/converted.png`.
For another known source, use `lantern-144.json`; its expected output lives in
`learning/aseprite/practice/lantern-original-converted-2026-11-03/`.
Existing output directories are refused: choose a fresh name for each replay.
On macOS, `learning/aseprite/automation/run-reach.command` uses this venv without
depending on the original machine's Python cache.

For a new image, supply a recipe with a source path, reviewed foreground mask
or alpha threshold, scale/height, canvas and anchors. Paths are relative to the
recipe. Conversion samples source pixels; choosing a silhouette, repairing
anatomy, creating semantic layers and approving art remain separate work.

## 2. Restore the Aseprite automation connection

Use an existing Aseprite 1.3+ installation and Node 22.6.0+ with npm. No purchase
or editor installer is bundled. The original editor was Aseprite 1.3.18.6-dev;
a different editor/OS needs its own smoke test.

```sh
npm ci --prefix tools/aseprite-mcp --ignore-scripts --no-audit --no-fund --cache .art-tools/npm-cache
```

This installs Pebbly `@pebbly/aseprite-ai-artist@0.8.2` from the checked-in lock.
The dependency graph and archive integrity are preserved from the tested install;
the old `file:pebbly-0.8.2.tgz` dependency is replaced by the registry URL for the
same integrity-checked archive. `node_modules` stays ignored. No extension is
needed for the headless route used here.

The tracked `.codex/config.toml` contains the original Mac's absolute paths.
Before opening a new Codex session, replace its existing Aseprite server and env
tables with this block, filling in the new machine's absolute paths. Preserve
other settings; do not append a duplicate table. Find Node with `command -v node`
on macOS/Linux or `where.exe node` on Windows. Windows TOML paths can use `/`.

```toml
[mcp_servers.aseprite-ai-artist]
command = "/ABSOLUTE/PATH/TO/node"
args = ["/ABSOLUTE/PATH/TO/combat-art-lab/tools/aseprite-mcp/node_modules/@pebbly/aseprite-ai-artist/dist/cli.js", "serve", "--headless", "--aseprite", "/ABSOLUTE/PATH/TO/aseprite"]
cwd = "/ABSOLUTE/PATH/TO/combat-art-lab"
startup_timeout_sec = 30
tool_timeout_sec = 60

[mcp_servers.aseprite-ai-artist.env]
ASEPRITE_AI_ALLOW_LUA = "0"
ASEPRITE_USER_FOLDER = "/ABSOLUTE/PATH/TO/combat-art-lab/.art-tools/pebbly/user-folder"
```

On a standard Mac install the editor executable is
`/Applications/Aseprite.app/Contents/MacOS/aseprite`. On Windows select
`Aseprite.exe`; on Linux select the actual installed executable. Create the
`ASEPRITE_USER_FOLDER` directory if it is absent. These are host-local config
edits; avoid publishing one machine's replacement paths as a universal config.

For conversion/Aseprite work only, add `enabled = false` inside the existing
`[mcp_servers.godot-art-lab]` table so its old paths are not launched. If engine
playback is needed later, restore its pinned dependencies and paths separately
using [the Godot setup record](../tools/godot-mcp/README.md).

Open this checkout in Codex and trust the project when appropriate. Reload/start
a new session after configuration. Project MCP settings require a trusted
project. Configuration discovery alone does not prove a working editor.

## 3. Verify the native workflow on the receiving machine

Read `tools/pixel-art-director/SKILL.md` and its
[setup and scratch-test procedure](../tools/pixel-art-director/references/setup.md).
The `.agents/skills/pixel-art-director` link points to that checked-in folder.
If a Windows checkout materializes the symlink as a text file, read the canonical
skill directly; skill auto-discovery has not been verified on that host.

Ask the agent to use the dedicated Aseprite MCP: preflight in headless mode,
create a scratch two-layer pattern, save it, change one pixel on a copy,
reopen/export and check both the intended change and protected layer. Have the
agent inspect the actual preview. Then open a converted PNG and save a separate
native master with the converted base preserved and corrections on another
layer. A flat conversion does not become a semantic reconstruction merely by
saving it as `.aseprite`.

The included [lantern native-copy verification](../learning/aseprite/practice/lantern-original-converted-2026-11-03/README.md)
and [weapon conversion record](experiments/2026-11-04-weapon-fighter-conversion/record.md)
are previous-machine evidence. Installation, MCP availability, save/reopen and
preview inspection on the receiving machine remain to be performed there.

## Sources and evidence boundary

Checked 5 November 2026: installed Pebbly 0.8.2 README/package manifest and npm
registry version, engines, archive URL and integrity; preserved install lock;
[official Codex MCP configuration](https://developers.openai.com/codex/mcp).
Setup changes do not enable a paid image service or validate new artwork.
See the portability entry in [the handoff](handoff.md) for the fresh checks run
on the publishing machine. Windows/Linux editor playback remains untested.
