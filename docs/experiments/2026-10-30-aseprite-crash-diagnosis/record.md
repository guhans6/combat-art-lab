# Aseprite launch-crash triage

- Status: observed; no repair applied
- Date: 30 October 2026
- Question: whether the agent-visible crash establishes a damaged source build/setup,
  or a narrower launch-context failure.
- Scope: distinguish application launch, headless MCP readiness, document save/reopen,
  and MCP drawing errors without calling the active editor or changing artwork,
  configuration, or the installed application.
- Tools and permissions: read-only filesystem inspection; `plutil`, `codesign`,
  `otool`, `sw_vers`, and retained macOS diagnostic reports. No Aseprite executable,
  MCP, UI, installer, configuration, or source-build command was run.

## Observations

| Check | Method and target | Observed result | Evidence path |
| --- | --- | --- | --- |
| Crash phase | Read every retained `aseprite-*.ips` report through 30 October | All 21 reports terminate with `SIGABRT` in macOS application registration: `___RegisterApplication_block_invoke` → `_RegisterApplication` → `GetCurrentProcess` → `NSApplication sharedApplication` → `os::AppOSX::init` → `main`. No document, Lua runner, draw, or save frame appears before the abort. | `/Users/guhan/Library/Logs/DiagnosticReports/aseprite-*.ips` (local OS evidence; intentionally not copied) |
| Current reported failures | Inspect the four 30 October crash reports | Each was launched by `Python`/`python3`, owned by the ChatGPT coalition, and aborted about 0.12–0.22 seconds after launch. This matches a direct executable probe, not an in-editor save failure. | Same OS reports, timestamps 08:43:58, 09:14:48, 09:53:08, 10:14:47 +0530 |
| Existing differential repro | Read the previous controlled diagnosis | The identical direct `--version` probe returned `-6` in the restricted shell but returned `Aseprite 1.3.18.6-dev` under approved execution, with no binary, preferences, or environment change. | `../2026-10-26-headless-startup-fix/record.md`, `red-sandboxed-startup.json` |
| Installed bundle metadata | Read Info.plist, signature, architecture, linked system frameworks | Aseprite is arm64, version `1.3.18.6`; the local bundle is ad-hoc signed. This establishes provenance characteristics only; it neither proves nor disproves the registration crash cause. | `/Applications/Aseprite.app/Contents/Info.plist` |
| Configured headless boundary | Read project config and Pebbly launcher source | The configured server uses the explicit executable, local Pebbly `0.8.2`, `serve --headless`, and project-local `ASEPRITE_USER_FOLDER`. Pebbly owns one long-lived `aseprite -b` process and reports a pre-ready exit rather than silently losing a document. | `.codex/config.toml`; `.art-tools/pebbly/node_modules/@pebbly/aseprite-ai-artist/dist/bridge/headless.js` |
| Actual MCP/save evidence | Read 27–30 October technical records | Multiple headless MCP runs report `ready:true`, native edits, save-as to new paths, fresh reopen, and byte-identical PNG exports. A stale already-saved in-memory document can persist the wrong one-layer source; save-as after mutation is the recorded workaround. These are distinct from the launch abort. | `../2026-10-30-fullbody-automated-reconstruction/record.md`; `../2026-10-30-luna-fullbody-once/trial-b/record.md`; `../2026-10-30-sol-smile-repair/record.md` |

## Conclusion

The evidence does **not** support rebuilding or replacing Aseprite as a fix. The
repeatable failing boundary is direct launch under the restricted command sandbox, at
macOS application registration, before Aseprite reads a document or performs an art
operation. The normal dedicated headless MCP route has separate positive readiness
and save/reopen evidence.

The direct `--version` check in `tools/pixel-art-director/scripts/doctor.py` is a
misleading health signal here: it starts the same GUI-linked executable and can create
another crash report. A red doctor result does not establish that the headless MCP route
is unavailable; a green result alone would not prove native editing.

## Applied narrow repair

The user authorized the following narrow doctor guardrail after the active editor
leases were released. The direct Aseprite version probe is explicit opt-in. Default inventory
would report only the discovered executable path and file metadata, with a `not_run`
reason directing agents to configured MCP `preflight` for the real working boundary.
An explicit probe flag preserves direct version diagnostics for approved/outside-sandbox
contexts. Add a focused test proving the default doctor path never invokes Aseprite.

Changed canonical files only:

- `tools/pixel-art-director/scripts/doctor.py`: adds non-launching
  `aseprite_inventory()` and the opt-in `--probe-aseprite-version` flag.
- `tools/pixel-art-director/tests/test_tools.py`: mocks the default no-launch path
  and the explicit-probe behavior.
- `tools/pixel-art-director/SKILL.md` and `references/setup.md`: distinguish default
  inventory, explicit direct diagnostics, and the MCP-preflight evidence boundary.

This does not address separate MCP transaction, save-target, or schema errors. It
does not claim that all Aseprite crashes are cured or that MCP readiness was retested.
No Aseprite editor, source build, binary, global setting, project MCP configuration,
or artwork was changed.

## Isolated proposed-patch validation

The proposed patch was first applied only to a disposable copy under
`/private/tmp/aseprite-guardrail-test.0OWJfD`; no Aseprite process was touched.
The same checks were then run against the applied canonical skill. Focused checks
passed:

- Mocking `doctor.subprocess.run`, default `aseprite_inventory(sys.executable)` made
  zero subprocess calls and returned `version_probe: "not_run"`.
- With the same mock, explicit `probe_version=True` made exactly one synthetic
  `--version` call and returned its mocked version output.
- The patched default CLI, supplied the real Aseprite path, emitted the non-launching
  inventory boundary; `py_compile` passed. The command did not execute Aseprite.

The system Python lacks Pillow (`ModuleNotFoundError` before test execution), so no
installation was performed. Re-running the copied suite with the existing bundled
runtime at `/Users/guhan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`
then passed all 35 tests, including both new mocked doctor tests. This remains
valid for both the isolated copy and the applied canonical files.

The canonical default doctor command was also run with the real discovered Aseprite
path. It returned `found: true`, `version_probe: "not_run"`, and the explicit MCP
readiness boundary; it did not execute Aseprite. Ruby frontmatter/local-link checks
and `git diff --check` passed.

## Updated portable skill package

The new archive is
`pixel-art-director-2026-10-30-crash-guardrail.zip` in this experiment directory.
It preserves all older archives, excludes `__pycache__` and `.pyc`, and has SHA-256
`c899e68f89463196c9fa478d8644e4f35dde92a31ccc8f8c9ec6d39bb0336912`.
After extraction to a disposable directory, its 21 non-cache files matched the
canonical inventory and SHA-256 file-for-file; the extracted suite passed all 35
tests using the existing bundled Pillow runtime. This validates package
self-containment and content equality, not a second-host MCP connection.

## Decision and continuation

- Last proven state: direct restricted-shell launch is red; prior dedicated headless
  MCP edit/save/reopen is green; current art and configuration remain untouched.
- Next action: parent decides whether to apply the doctor guardrail, then may grant a
  short exclusive lease for one controlled preflight plus scratch-save test if current
  runtime confirmation is needed.
