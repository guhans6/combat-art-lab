# Review a repair and its regressions

Use for meaningful revisions with a retained before/candidate baseline. Existing
reference, native-protection and animation procedures still apply. A comparison
sheet is evidence to inspect, not a completed review.

## Prepare the comparison

Freeze the exact baseline role (approved, retained or diagnostic), requested gain,
candidate/native/export correspondence, allowed edit scope and affected frames.
Name vulnerable attachment/overlap relationships and nearby features worth preserving.
For proportion, grip or attachment changes, use the
[connected-form checkpoint](structure.md) and bind its marked reference,
native-owner isolation/hide views and neighboring poses as `evidence` below.
Keep the original identity/style reference available; an unapproved seed is not an
approved appearance baseline.

For same-grid edits use `scripts/comparison_review.py` from this skill directory:

```sh
python3 scripts/comparison_review.py build --spec /path/comparison.json --out /path/new-packet
python3 scripts/comparison_review.py verify --packet /path/new-packet/packet.json
```

Paths inside the spec are relative to the spec file. Example:

```json
{
  "baseline_role": "retained source; user approval pending",
  "registration": "same native grid and root; no per-image fitting",
  "required_frame_ids": ["F9"],
  "evidence": [{"role": "candidate native", "path": "candidate.aseprite"},
               {"role": "native/export readback", "path": "readback.json"}],
  "frames": [{"id": "F9", "before": "before.png", "after": "after.png",
    "mask": "allowed.png",
    "regions": [{"name": "arms-grip-handles-rim", "crop": [140,55,225,165]}]}],
  "zoom": 4
}
```

Choose task-specific crops; these coordinates are illustrative. Masks use existing
binary grayscale semantics: white editable, black protected, both required.
New colors/partial alpha remain disallowed unless the spec explicitly sets
`allow_new_colors`/`allow_partial_alpha` true under the task's policy.
The affected-frame inventory and registration basis are declarations to verify
against native changes; equal dimensions do not prove anatomical alignment.
Different poses/canvases need documented registration or a labeled reference view
using the existing reference helper, not automatic bounds fitting or invented diffs.

The helper reuses pixel protection checks and separately reports changed pixels
outside named close-review crops. An automatic full-frame overview does not count
as close review. Scope or coverage failures emit a diagnostic packet and exit1;
invalid inputs exit2. Add crops for legitimate peripheral changes and retain the
failed packet. Widening a mask does not authorize an unintended edit. A retrospective
diagnostic mask must be labeled as such. Zero changes establish no improvement.

## Inspect before deciding

Open clean before/candidate views and differences at native size and integer zoom.
Use native-image coordinates in observations, not enlarged sheet coordinates; check
important cited locations against the actual crop/pixel readback before relying on them.
Inspect all changed regions, changes inside the allowed scope, connected unchanged
surroundings and the full asset's silhouette, proportions, expression and materials.
For an attachment ask: which edge covers which, where does the obscured part
reappear, and what supports the load? For a grip, follow cuff→wrist→fingers→each
handle→rim. Opaque connectivity alone answers none of those semantic questions.

For animation, inspect neighboring keys and affected transitions/loop return, plus
authored-speed playback when perceptually available. Hash-bind those evidence
files too. State still-only limits; filmstrips and runtime events do not establish
continuous motion perception. PNG comparison cannot detect hidden native damage.

At the existing independent-review boundary, give the critic task/locks/exact images
without the producer's praise or success conclusion. Have it describe visible
relationships and seek regressions before stating a decision. This is a fallible
review aid, not guaranteed debiasing or a reason to add an expensive critic to every
minor edit. If the critic edits, another reviewer must freshly inspect its output.

## Record two decisions

Bind a short manual review to the SHA256 of `packet.json` and the candidate/native
hashes. Use concrete observations, not “looks connected” or a computed art score:

| Area/frame/crop, viewed file and scale | Target improvement | New regressions / preserved connections | Decision and uncertainty |
| --- | --- | --- | --- |
| Each named region and important join | Visible gain or absent gain | What became worse, including inside scope | pass / reject / uncertain |
| Full asset and affected neighboring poses | Contextual gain | Identity, anatomy, material and silhouette changes | pass / reject / uncertain |

Record reviewer role, playback evidence actually perceived, best eligible prior,
latest status and next baseline. A rejected/uncertain structural join prevents
selection as an improved result even when the requested feature got better.
Mechanical completeness is not inspection; covered pixels are merely available to
inspect. Keep rejected attempts and choose no selected result when necessary.

Before relying on that review, compare its recorded packet hash and run `verify`.
It checks spec/source/evidence/sheet freshness; it does not interpret review prose,
authenticate caller declarations, certify native/export equality or defend against
deliberate evidence forgery. Source or packet changes require a new packet and
affected review. Build/verify always leave visual acceptance and user approval
pending. Agent observations, engine execution and the user's artistic acceptance
remain separate claims.
