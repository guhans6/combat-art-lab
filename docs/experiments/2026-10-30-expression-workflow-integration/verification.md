# Expression workflow and portable-skill verification

- Date: 30 October 2026.
- Status: implementation, local/package checks and independent instruction review passed; artwork user visual judgment remains separate.
- Scope: the maintained workflow, director skill, profile preparation behavior,
  experiment template, handoff, and a versioned portable archive. No art, native
  master, historical experiment, engine scene, global configuration, commit, or
  publication was changed.

## Changed checkpoint

`tools/pixel-art-director` now keeps the detailed expression procedure in
`references/face-likeness.md`: reference/pose registration, confidence, actual native
feature ownership, scope freezing, morphology/contrast/context review, and finite
critic rescue followed by fresh independent inspection. `SKILL.md` routes ambiguous
facial work there without requiring combat-art-lab-relative files. The historical v03
profile remains bundled and explicitly optional.

`prepare_run.py` now requires `--profile` and writes its brief from that task's ID and
reference roles instead of naming the historical standing-v03/neck correction. The
focused custom-profile regression proves this behavior. Project routing records the
user-selected current roles: Luna6 Max for routine drawing, Terra for workflow
implementation, and one Sol6.1/high final critic/rescue maximum when warranted;
availability and user override remain explicit.

## Observed checks

| Check | Result |
| --- | --- |
| Bundled Pillow runtime: full known suite | 33/33 passing, including alpha-coverage, reference-review, custom-profile brief behavior, and frozen-input/mask protections |
| Extracted portable archive: full known suite | 33/33 passing |
| Extracted CLI | `prepare_run.py --help` passed |
| Archive inventory/tree | Complete canonical tree extracted; per-file SHA-256 inventory matched; no `__pycache__` or `.pyc` members |
| Discovery | `.agents/skills/pixel-art-director` remains a symlink to `../../tools/pixel-art-director` |
| Frontmatter and links | Ruby YAML parsed `SKILL.md`; portable skill links have no repository-relative target; `git diff --check` passed |
| Skill validator | Not run: bundled validator raised `ModuleNotFoundError: No module named 'yaml'`; PyYAML is unavailable and was not installed |

## Portable artifact

- Archive: `pixel-art-director-2026-10-30.zip`
- SHA-256: `74d9257a877134c9e5b657ce86c6e8909b10c0318479dc6ac06145bbe4651be4`
- Extracted verification location: `/private/tmp/pixel-art-director-package.Nolv5s`

To reuse it, copy the complete extracted `tools/pixel-art-director` folder into the
chosen receiving project at `.agents/skills/pixel-art-director`; then have that host
discover the skill/backend and run the scratch smoke procedure in `references/setup.md`.
Use a receiving-project profile explicitly with `prepare_run.py prepare --profile ...`.
This package proof does not establish installation, host discovery, backend
connectivity, or artistic quality in another project.

## Remaining boundary

Independent [forward review](forward-review.md) passed all twelve expression, critic, unavailable-model, routine-edit, benchmark-equity and custom-profile scenarios with documented limits. Source, discovered skill and extracted archive each passed 33/33 tests. Instruction scenarios are not live drawing trials. Current Sol smile pass02 remains a user-review candidate; this documentation work neither selects nor approves it. The updated local skill is available through the existing discovery symlink. The portable archive is ready to copy, but installation/discovery and backend smoke in another project are not performed. Next art boundary is a separately scoped expression strip after the user chooses the still direction.
