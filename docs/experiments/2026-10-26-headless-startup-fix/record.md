# Aseprite headless startup diagnosis and Test2 repair

26 October 2026. Requested scope: unblock the separate agent in `/Users/guhan/Downloads/Test2`; do not reconstruct a character or import earlier artwork.

## Cause and evidence

The executable is healthy. Its macOS application-registration initialization aborts when launched inside the restricted shell-command sandbox used for the other agent's manual MCP test. The user-supplied crash stack ends at `HIServices::_RegisterApplication`, `NSApplication sharedApplication`, and `os::AppOSX::init`, before artwork or the headless Lua runner is processed.

Minimal reproducible command, run twice in the normal command sandbox:

```sh
python3 docs/experiments/2026-10-26-headless-startup-fix/probe-startup.py
```

Both runs returned `passed:false`, subprocess return code `-6` (SIGABRT), with no version output, in 0.152s and 0.141s. Exactly the same probe under approved `require_escalated` execution returned `passed:true`, `Aseprite 1.3.18.6-dev`, in 0.061s. No binary, settings or environment-variable changes were made between those probes.

The full original MCP configuration was also tested through `harness/test-aseprite-mcp.py`: MCP handshake succeeded but `preflight.ready=false`, with the exact directive `Headless Aseprite exited (signal SIGABRT) before it was ready.` The preserved original configuration subsequently returned `ready:true` outside the command sandbox. This separates the crash cause from the launcher improvements below.

Ranked hypotheses were stated before differential testing: (1) sandboxed application registration, (2) damaged settings, (3) inherited environment, (4) damaged binary. The direct inside/outside comparison confirms the execution-context cause for this reproduction. It does not establish that every possible Aseprite crash has the same cause. No preference reset, binary rebuild/reinstall, signing change or live-mode fallback was necessary.

## Separate configuration defect

The other chat's actual working directory is `/Users/guhan/Downloads/Test2`, verified from its task metadata. Its only Aseprite MCP config was one directory lower, at `aseprite-reconstruction-2026-10-26/.codex/config.toml`. Running `codex mcp get aseprite-ai-artist --json` from Test2 initially returned `No MCP server ... found`. Test2 was already recorded as trusted; trust settings were not changed.

A config file in a child directory was not available to the chat rooted at its parent. [Official Codex MCP documentation](https://developers.openai.com/codex/mcp/) was fetched on 26 October 2026 to verify project-scoped `.codex/config.toml`, command/args/cwd/env and timeout fields.

## Applied repair

- Added `/Users/guhan/Downloads/Test2/.codex/config.toml`, at the chat's actual workspace root.
- Updated the matching child configuration, preserving its original bytes in `diagnostics/startup-repair/nested-config-before.toml`. Both configurations name the same server, rather than starting competing live/headless backends.
- Stabilized the already-reviewed Pebbly 0.8.2 npm archive in the target's `.tools/pebbly`, with a local installation and dependency lock. Used `--ignore-scripts` and a separate temporary npm cache. No global package/cache ownership changes.
- Pinned the actual server command to absolute Node and local `dist/cli.js` paths. The command explicitly selects headless mode and the existing Aseprite binary; it no longer depends on npx finding/downloading the server at launch.
- Set an isolated target-local `ASEPRITE_USER_FOLDER` and kept raw Lua disabled. Working directory is the target's reconstruction folder.
- No sandbox policy, global client configuration, trust setting, Aseprite app/extension, artwork, or references were modified. The command sandbox still applies to ordinary shell calls. This repair does not make an unapproved sandboxed shell launch valid.

After the root config was added, `codex mcp get` from Test2 found the enabled, pinned server and the correct command, cwd and environment. Native client tool exposure after reloading the other chat is a remaining handoff boundary, not an observed result here. The direct test below uses the actual repaired config through an approved MCP adapter.

## Focused regression and capability verification

`diagnostics/startup-repair/test-aseprite-mcp.py` in the target reads the actual root config and exercises the real MCP protocol through the installed SDK. It asserts actual `preflight.ready`, not just a successful server handshake. It requires a new output directory so reruns preserve evidence.

Approved invocation (writes scratch swatches only):

```sh
python3 /Users/guhan/Downloads/Test2/aseprite-reconstruction-2026-10-26/diagnostics/startup-repair/test-aseprite-mcp.py \
  --workspace /Users/guhan/Downloads/Test2 \
  --output /Users/guhan/Downloads/Test2/aseprite-reconstruction-2026-10-26/diagnostics/startup-repair/smoke-verified
```

Do not repeat this as an ordinary sandboxed shell command; request the normal targeted execution approval if using the shell adapter. Prefer the configured MCP tools loaded by the client for continuing work. Do not disable the workspace sandbox to run this test.

Observed: Pebbly 0.8.2 handshake; headless `ready:true`; Aseprite `1.3.18.6-dev`; 36 successful MCP calls. A new 16x16 transparent two-layer document contained a red L open to the right, green right branch, and isolated blue pixel at (12,4). Returned MCP image bytes were viewed by the current model, including after edit, reopen and erase.

Independent checks passed:

- Exactly one composite/native pixel changed at (2,2), red to green. An attempted adjacent write was selection-clipped.
- The protected layer's full pixel data and metadata stayed equal.
- Native close/reopen retained two layers, one frame, and a fresh RGBA-identical PNG.
- Transparent skip preserved the existing pixel; default grid transparency erased it.
- A deliberate out-of-mask write on a different scratch copy was rejected by both PNG and native-data checks.

Exact calls, tool catalog, returned image bytes, native files, exports and results are under the target's `diagnostics/startup-repair/smoke-verified`. `independent-smoke-checks.json` records the separate checks. The original config's approved green preflight is preserved separately, so the evidence does not conflate sandbox removal with the new launcher/user-folder settings. Each probe closed only the processes/documents it started; no live editor UI was operated.

## Continuation boundary

Reload/open the other chat's workspace at `/Users/guhan/Downloads/Test2` so its normal tool catalog loads the new root config. The agent should call the configured `preflight`, then inspect a returned scratch preview through its own model before starting the blank-document reconstruction. A successful smoke test by this model does not certify that a different model received the same image.

The normal sandboxed version command will still abort: the correct resolution is the MCP's host-managed launch or an explicitly approved outside-sandbox adapter. Avoid repeated unapproved shell retries; those attempts explain the repeated macOS crash-report dialogs. No persistent permission broadening is part of the fix.

No character reconstruction, previous sprite/script/reference import, commit or publication occurred. The other agent remains responsible for reference-only drawing and artistic review. No messages were sent to that chat. The crash stack/probe results and the tested setup are the evidence supplied for its continuation.
