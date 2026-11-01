# Workflow guardrails integration verification

- Date: 29 October 2026
- Scope: documentation and canonical project-skill integration only; no artwork,
  native source, art trial, engine scene, configuration, archive, commit, push, or
  publication changed.
- Base revision: `9e35c5c13987a153e942e6f93f49f247fad13c3a`
- Task delta: `docs/workflow/art-production.md`,
  `tools/pixel-art-director/SKILL.md`,
  `tools/pixel-art-director/references/benchmark.md`,
  `tools/pixel-art-director/references/assisted-reconstruction.md`,
  `docs/experiments/experiment-template.md`, and `docs/handoff.md`.
  This record is the integration evidence file. Pre-existing working-tree changes are
  outside this task and were preserved.

## Local checks

| Check | Observed result | Boundary |
| --- | --- | --- |
| Director regression suite | 32/32 tests passed with the bundled workspace Python | Regresses existing freezing/protection, alpha coverage and review-image helpers; it does not prove visual selection on art. |
| Skill frontmatter | Ruby YAML parser loaded `SKILL.md` | Narrow frontmatter syntax check. |
| Canonical discovery | `.agents/skills/pixel-art-director` resolves to `tools/pixel-art-director` | Discovery symlink retained; no duplicate skill copy or ZIP snapshot was updated. |
| Local Markdown links | All touched local links resolve after this record was added | Link existence, not workflow effectiveness. |
| Patch hygiene | `git diff --check` passed | Scope was reviewed against the six planned targets plus this evidence record. |
| Bundled skill validator | Not run successfully | `quick_validate.py` cannot import PyYAML in the available runtime; no dependency was installed. |

The shell-default `python3` also lacks Pillow; the bundled workspace Python supplied
Pillow and ran the test suite. Neither result proves that the written gates produce
better art. A future bounded run must establish effectiveness.

## Independent behavioral review

A read-only independent reviewer applied the integrated instructions to eight
scenarios without an art trial. Result: **PASS for routing/instruction integration**.

1. NN/large-palette versus BOX/small-palette seeds cannot be called a controlled
   model comparison. With the same source they are a method/recipe comparison; if
   the model also differs, label the result model-plus-recipe/end-to-end and retain
   its confounds. No filter or model wins generally.
2. A deliberate resampling-plus-quantization variation is permitted as a method/recipe
   study. Name both variables and attribute results to the combined recipe, not either
   variable or the model alone.
3. A technically passing latest squinted-face candidate is rejected for selection when
   a reviewed prior preserves the intended expression. Keep it as rejected/last
   attempted and restore the prior as best eligible baseline.
4. If all candidates fail identity, record none selected and retain evidence; if the
   latest is unreviewed, label it awaiting review. Neither state advances dependent work.
5. A user-authorized, reference-evidenced bounded mouth/eye repair is allowed with a
   frozen native baseline, region/layer locks, reversible candidate, original/seed/best/
   new review, and native/reopen/protection evidence. Authorization does not promote it.
6. A deliberately weak common seed is valid for a named smile-repair task. It supports
   a true model comparison only after exact shared seed/task/budget inputs are frozen
   and verified; it is not automatically a production baseline.
7. A convincing seed without native editability proof remains pending. Preserve it,
   perform any localized edit proof on a labelled duplicate, and keep technical proof
   distinct from selection or user approval.
8. Clipped, matted, mislabelled, or otherwise unreliable comparison panels invalidate
   selection evidence. Rebuild the evidence against exact exports; identity uncertainty
   remains pending.

The reviewer also confirmed that the guidance does not make a blanket face freeze,
force same-seed controls on a declared method study, prescribe NN or palette size as a
winner, or turn the historical v03 profile into a reconstruction default.

## Readiness and next owner

The workflow integration is locally checked and ready for a separately authorized,
bounded image-to-sprite run. It is not proof of artistic quality, model performance,
asset selection, user approval, motion, Godot playback, packaging, or publication.
Next owner: a drawing agent for that separately scoped run; the user retains visual
selection and approval.
