# Experiment: gameplay character camera, identity and display size

- Status: observed; user selection pending; clean alpha/camera correction incomplete.
- Date: 1 November 2026.
- Question: how does the accepted atmospheric character direction read as a sidegame figure at different displayed heights, and which facial cues fit?
- Baseline: assets/concepts/stealth-fighter/atmosphere-r01/A/simplified-01.png; user approves design direction, atmosphere provisional.
- Scope: concept comparison only; transparent cutout, two camera orientations, facial alternatives and sameimage screen-scale scenarios.
- Tools/authority: user authorizes generation and parallel subagents; explicit GPT-6.1 only/noAstra override; builtin imagegen ten calls; scoped learningclone filesystem writes; no installs/API purchases.
- Intent: exploratory art feasibility, not a model/method benchmark.
- Controls: fixed original identity cues; camera studies change view with incidental drift; separate face studies change jaw/brow but hair/framing/light also drift; sameimage scale study controls image/environment exactly. No causal attribution to isolated variables where multiple changed.
- Reference contract: existing art workflow/assetcontract; historical tote styleguide does not govern this new character. SilverPines primary humanrendering direction, LastNight mood only.

## Artifacts and review

See ../../../assets/concepts/stealth-fighter/gameplay-r01/review.md and per-output manifests. Parent inspected source, corrected camera outputs, separate final faces and rendered boards. Technical checks in checks.json. Original raw sources unchanged and hashes retained. Excluded unassigned faces retain promptmapping uncertainty.

| Check | Observed result |
| --- | --- |
| Camera | More side-on attempt useful, strictprofile and foot top-plane correction not achieved |
| Transparency | Actual alpha but unwanted halo in all cutout attempts; fails clean cutout |
| Face comparison | Soft/firm alternatives delivered; too detailed, some framing/hair/light drift; user selection pending |
| Display size | Static96/128/160px height within640x360 mockup; parent favors128 provisionally |
| Native grid/editability/local revision | Not performed |
| Animation/contact/timing/Godot | Not performed |
| Publication | Not performed |

## Decision and continuation

Keep approved original direction and preserve all attempts. No further blind generation retries. User next selects useful face/camera/framing cues. Cleanalpha and perspective need a controlled correction before native production. Comparison sizes are not native resolution or real engine proof.
