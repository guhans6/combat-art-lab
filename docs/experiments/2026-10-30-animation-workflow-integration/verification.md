# Verification and delivery boundary

30 October 2026. Local working-tree artifacts; no commit or publication.

## Fresh checks

Bundled runtime: `/Users/guhan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
Commands run from the repository root with `PYTHONDONTWRITEBYTECODE=1`:

```sh
PYTHONPATH=. <bundled-python> docs/experiments/2026-10-30-animation-workflow-integration/audit.py
<bundled-python> -m unittest discover -s tools/pixel-art-director/tests -v
<bundled-python> /Users/guhan/.codex/skills/.system/skill-creator/scripts/quick_validate.py tools/pixel-art-director
<bundled-python> docs/experiments/2026-10-30-animation-workflow-integration/validate_delivery.py --package
```

- Offline audit: all28 native composites equal actual frame PNGs; both supplied GIFs
  equal native images at3x and exact native timing. All three rest composites equal;
  no new visible RGB in any pose. Independently inspected same-matte contacts.
  [Measurements and exact hashes](audit.json), [diagnosis](record.md).
- Source helpers: **35/35 pass**. Portable helper code was unchanged.
- `quick_validate.py`: **could not run**, `ModuleNotFoundError: No module named 'yaml'`.
  No dependency was installed. Supplementary Ruby Psych `safe_load` frontmatter
  parsing, name/description/schema checks and unfinished-placeholder check passed
  on source and extraction. This is not a claim that the official validator passed.
- Skill local links/anchors: **22/22** resolve in source and standalone extraction.
  Every newly added link in maintained project docs resolves. This check does not
  revalidate remote sites or all inherited historical project links.
- Project skill discovery symlink resolves to `tools/pixel-art-director`.
- Independent forward instruction pass: **8/8 scenarios exercised**, with actual
  read-only art diagnosis for the first and fixture-based branch decisions for the
  others. It found an inherited alpha completion/scope ambiguity; the narrow fix
  was reread and accepted in continuation of that pass. No outstanding issue.
  [Full actual outcomes, consulted paths and revision hashes](forward-review.md).
  This is instruction validation, not eight executed art tasks.
- Preservation: all **2,751** pre-existing files under `assets` and
  `docs/experiments` retain their original hashes. This includes originals, blink,
  historical experiments, handoff analysis and previous ZIPs. Bytecode caches are
  excluded. [Before manifest](protected-inputs-before.json),
  [result](delivery-validation.json).

## Portable artifact

[pixel-art-director-2026-10-30-animation-continuity-v1.zip](pixel-art-director-2026-10-30-animation-continuity-v1.zip)

SHA256: `33779e6da10dedb6fec0da2b59e4aed92337b4198850f77e6c7c583a82797473`.
All22 packaged files equal the canonical source by SHA256, ZIP integrity passes,
and the package has one `pixel-art-director/` root with no symlink/repo dependency.
It was extracted into a new `/private/tmp/combat-art-animation-package-*` directory;
all **35/35** tests passed with that directory as cwd, and local links/frontmatter
passed there. [Manifest](bundle-manifest.json), [extracted test output](extracted-tests.txt).
The helper's `--package` mode uses exclusive creation and cannot overwrite an archive.
Rerun without `--package` to validate the existing artifact against maintained source.

## Scope of proof

The changed workflow is available through the existing local symlink and source.
The bundle is ready for review/copying; other-project installation and behavior on
another host were not performed. No Aseprite backend launch/mutation, art drawing,
Godot run, actual-speed visual playback, user art approval, global configuration,
commit, push or publication occurred. No new animation is validated by these tests.

The experiment-local helpers only read old art and write diagnostic evidence in
this new folder. `audit.py` fails closed for unsupported native composition;
`validate_delivery.py` checks real links, extracted file equality, preservation and
actual helper tests. They do not score art or simulate a human's temporal perception.

The exact maintained diff against the already-dirty starting files is retained in
[maintained-changes.patch](maintained-changes.patch), with initial copies under
`baseline/`. Those copies are historical comparison evidence, not alternate maintained
skill sources. [Maintained file hashes](maintained-file-hashes.json) identify the
four project documents and five skill documents changed. Local experiment evidence
links resolve; experiment helpers compile and were exercised by
the actual audit/package runs. `git diff --check` passes. No repository-wide
Definition of Done was invented.
