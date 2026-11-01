# Setup and capability verification

Prepared 2026-10-26. This is an installation plan, not a record of installation.
Run it on the machine hosting the agent and Aseprite, not in an unrelated chat
container. Read the repository instructions and preserve unsaved documents first.

## Portable copy into a chosen project

The canonical source is this complete `pixel-art-director` folder. To reuse it,
copy the folder into the receiving project's discoverable skill location—for example:

```bash
mkdir -p /absolute/path/to/chosen-project/.agents/skills
cp -R /absolute/path/to/pixel-art-director \
  /absolute/path/to/chosen-project/.agents/skills/pixel-art-director
```

This is a documented receiving-project action, not a global installation. Preserve
the complete folder (including `scripts/`, `references/`, `assets/`, and tests).
The historical v03 profile is optional and must be selected explicitly with
`prepare_run.py --profile`; create/select a task-specific profile for other art.
After copying, discover the receiving host's skill support and backend runtime, then
run its scratch smoke test below. A copied folder does not prove host discovery,
backend connectivity, or art-tool availability.

## 1. Inventory before installing

From the skill directory:
```bash
python3 scripts/doctor.py
python3 -m unittest discover -s tests -v
```
The included Python utilities need Python 3.10+ and Pillow. They were tested in
this delivery environment with Pillow 12.3.0. Install a missing dependency in a
project-local virtual environment only when authorized; record the resolved
version. The art tools themselves have different prerequisites.

The user's repository records Aseprite 1.3.18.6-dev at
`/Applications/Aseprite.app/Contents/MacOS/aseprite`. The default doctor checks the
executable's presence without launching it. If a direct version diagnostic is needed,
run `python3 scripts/doctor.py --probe-aseprite-version` only where direct app launch
is permitted; an application-registration failure in a restricted shell is a launch
context result, not proof of a damaged build or MCP failure. Do not rebuild or
purchase Aseprite automatically. Read existing client MCP configuration without
printing unrelated credentials. Look for duplicate Aseprite servers and old plugin
names. Inventory an already installed integration before replacing it.

## 2. Select and pin one backend

**Recommended pilot: Pebbly Aseprite AI Artist.** The inspected source manifest
is version 0.8.2, Node >=22.6.0; installation docs require Aseprite >=1.3.
These are observed source values, not a guarantee that a package registry release
matches the current main branch. Check the package/release provenance before
installing and record the exact resolved version/commit. Do not silently resolve
`latest` during repeated model comparisons.

First choose **headless** for isolated reproducible runs, or **live** when watching
and undoing edits in Aseprite is important. Both need the same visual verification.
Headless uses the batch runner and does not require the live bridge/extension.
Never run both against the same native file.

Inspect help and the selected client's proposed config before writing:
```bash
npx @pebbly/aseprite-ai-artist@0.8.2 --help
npx @pebbly/aseprite-ai-artist@0.8.2 install gemini --project --dry-run
# For Claude Code instead, select `claude`, not `--all`.
```
Running npx downloads/executes code: do this only after the source/dependency
review and normal installation authorization. If the exact release is unavailable,
stop to select a reviewed commit or existing verified version; do not quietly
change the experiment's version.

For a headless configuration, the documented flags are:
```bash
npx @pebbly/aseprite-ai-artist@0.8.2 install gemini --project --headless \
  --aseprite /Applications/Aseprite.app/Contents/MacOS/aseprite --dry-run
```
After reviewing the diff/backups, apply the same command without `--dry-run`.
Inspect the resulting launch command: a pinned installer invocation does NOT
prove that the saved server command is pinned. Pin the actual launch command to
the reviewed version or to a locked local build. Preserve other server entries.

For live mode only, install the matching extension, save open user documents,
then arrange a normal restart of Aseprite:
```bash
npx @pebbly/aseprite-ai-artist@0.8.2 install-extension
npx @pebbly/aseprite-ai-artist@0.8.2 doctor
```
Do not force-quit the application, install every client, or auto-merge an upstream
AGENTS section into the user's instructions. Use the narrow routing snippet in
this package if a routing change is authorized.

**Alternative: Diivi.** Inspect its current README, pin a reviewed commit in an
isolated checkout, preserve/use its dependency lock, and configure the documented
`uv --directory /absolute/checkout run -m aseprite_mcp` entrypoint with the verified
Aseprite path. Current README prerequisites: Python 3.13+ and uv. Do not use Steam
credentials or Docker to reinstall an editor that is already available.

## 3. Load the same skill in each host

The main SKILL.md follows the Agent Skills format with only portable name and
description metadata. Keep the entire skill directory together, including scripts
and references. Use one canonical copy; avoid divergent per-client rewrites.

Gemini CLI documents workspace `.agents/skills/` and `.gemini/skills/` discovery.
Claude Code documents `.claude/skills/` project skills. Use the host's supported
link/install mechanism or explicitly ask it to read the canonical SKILL.md. Do
not assume a slash command is portable. Other hosts must be verified individually.
For a first fair comparison, use the same core skill and MCP; do not give only one
host extra critic agents, automatic hooks, or image generators.

The upstream Pebbly workflows can be accessed through its MCP prompts/resources
or installed skill files. Load `fix` for an existing sprite and `draw` for new
construction; our task profile remains the authority on scope, grid and reference.
The generic fallback is "read this SKILL.md and follow it", with an actual read
confirmation and tool capability test.

## 4. Smoke test on a scratch document

This test is a required procedure, NOT an already executed result in this kit.
Use a newly created scratch folder and record the actual tool calls and outputs.

1. Discover tools; record server, client, model, editor versions and selected mode.
2. Create a 16x16 transparent sprite with two named layers. Draw an asymmetric
   three-color pattern and an isolated pixel. Save as a new `.aseprite` file.
3. Request the preview through the same tool route the agent will use for art.
   Have the agent identify the pattern's orientation and isolated pixel location;
   confirm against exact pixel reads. A response containing a path is not proof
   that the model received or inspected the image.
4. Read a small patch as a grid/pixel matrix. Change exactly one intended pixel on
   one layer. Verify the new color, exactly one changed composite pixel, and zero
   changes to the protected layer. Test erase and transparent-skip semantics.
5. Save and reopen the scratch source; export PNG again. Compare rendered pixels
   and inspect both layer images/metadata. If using live mode, also test undo on
   the scratch document and then reapply the same verified change.
6. Attempt a controlled out-of-mask change on another scratch copy and confirm
   the independent checker rejects it. Do not rely on a selection's existence.
7. Record `PASS` only for observed results. Tool discovery without image delivery,
   or correct export without native structure, is partial setup, not completion.

## 5. Security and budget boundaries

Pebbly's security document says its live bridge binds localhost but has no local
client authentication and no filesystem sandbox root. Do not describe a workspace
folder as an enforced sandbox. Use separate scratch/candidate copies and a host/OS
sandbox when available; do not expose the bridge remotely. Keep raw-Lua opt-in
off unless necessary. Stop only the process you started when cleaning up.

The MCP is local, but a cloud-hosted model can still receive images/content through
its agent client. Local editing does not mean end-to-end offline operation. Do
not upload private assets to extra services or enable paid image APIs without
approval. Use the user's selected model/provider and normal spending limits.

## Sources

- https://github.com/with-pebbly/aseprite-ai-artist/blob/main/docs/INSTALL.md
- https://github.com/with-pebbly/aseprite-ai-artist/blob/main/package.json
- https://github.com/with-pebbly/aseprite-ai-artist/blob/main/SECURITY.md
- https://github.com/diivi/aseprite-mcp
- https://agentskills.io/specification
- https://geminicli.com/docs/cli/skills/
- https://geminicli.com/docs/tools/mcp-server/
- https://code.claude.com/docs/en/skills
