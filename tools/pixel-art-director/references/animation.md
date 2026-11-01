# Animation: motion and appearance continuity

Use for constructing, revising or diagnosing a frame sequence. A static expression
edit uses [face-likeness.md](face-likeness.md); deliberate facial changes within a
sequence use that procedure as well as this one. Apply the receiving project's
references and constraints. No character, model, palette size or frame count is a default.

## Establish the task profile

Record the exact native baseline/export and reference roles, accepted qualities,
rejected qualities, and unresolved selection. A preference for one quality does not
approve the whole candidate or select a side of a multi-panel comparison.
Start construction with a convincing static checkpoint; name whether it is
user-selected or agent-provisional. Broader production requires user acceptance.

Keep a short task-specific profile in the run record:

- Motion: action, phases/timing, key poses, grounded/root travel, intended scale and
  desired restraint; motion reference intervals and what they demonstrate.
- Appearance: material base/shadow/light roles, lighting direction/value hierarchy,
  characteristic fold/texture clusters, contours and silhouette/volume cues to retain.
- Scope: actual native owners, per-region reuse/deformation/redraw, permitted
  expression changes, protected regions, anchors, palette policy and pass budget.
- Evidence: key/transition/loop comparisons, playback path, native/export checks and
  the next decision. Mark unobserved playback and unknown game scale explicitly.

Use only fields relevant to this sequence. A diagnostic may begin from rejected
poses; that does not make them a baseline for dependent production. An image-model
sheet may supply poses but is not a native master; record generation, raster reuse,
authored drawing and manual intervention separately. Keep method changes separate
from a frozen model comparison.

Inspect the complete silhouette of every generated pose before cutting a sheet.
Printed or requested grid slots are layout hints: hair, limbs or a swinging prop
may cross a cell boundary. Use reviewed per-pose masks or wider crops that retain
the whole subject while excluding neighboring pose fragments. Verify crop coverage
before conversion and normalization; enlarging the later canvas cannot restore
source pixels already discarded. Register the retained anatomy and intended contact,
rather than fitting each resulting silhouette independently.

## Choose a method for each part

Apply [connected forms](structure.md) before drawing or transforming keys. Its
marked proportions, object sites and composite/owner-hide/neighbor checkpoint
govern structural continuation; a common scale and connected pixels are insufficient.

Inspect visible pixels and actual native ownership before moving a named layer.
Use cel translation/rotation or copied pixels for rigid parts and holds where their
shape remains valid. For changing torso volume, cloth tension, foreshortening or
occlusion, construct the changed contours/planes and repair overlaps and exposed
areas. Reuse legitimate unchanged regions. A request for redraw preserves the
appearance contract; it does not authorize relighting or costume restyling.

Decide anatomy, connected parts and volume in the key poses before in-betweens.
For attacks establish anticipation, contact and recovery; for loops establish the
rest, extremes, transitions and seam. Keep shared native scale/slots and declared
anchors. Record intended root/jump offsets instead of independently fitting bounds
or grounding each pose. Keep effects separate so the underlying action is reviewable.
Inspect affected overlaps with [alpha-coverage.md](alpha-coverage.md).

### Plan connected motion before extending the keys

Choose one primary action and a shared phase timeline (for breathing: rest,
inhale, apex, exhale, settle). Write a frame/duration table for the torso,
shoulders, neck/head, arms, clothing, hair and carried objects; mark unchanged
parts explicitly. Each primary attachment follows that action with its own
appropriate displacement and shape. Independent part clocks and a blanket
one-frame delay for every part are not motion plans.
Treat backend idle recipes (such as "head last", delayed face contents, mandatory
horizontal drift or different part-loop lengths) as optional techniques. Apply
them only when the character's anatomy and action justify them; the task's
attachment constraints and reviewed key poses take precedence.

Record the attachment chain and constraints: ground/root → pelvis → thorax →
shoulders/neck → head and arms; hair follows its skull attachment, straps follow
shoulder and bag attachments. Locate actual native owners, including cross-part
pixels. For pocketed hands, hold wrist/pocket contact and reshape or reuse the
sleeve between elbow and shoulder; moving a whole hand cel can break that contact.
Preserve neck/collar overlap and limb length/volume across each transition.

Give each secondary delay a physical cause, attachment and release condition.
Loose cloth may settle after a torso change; a tied hair mass or supported bag
can remain still. Use different amplitudes and supported follow-through rather
than identical whole-body translation. Add a separate blink only within its eye
scope. With one-pixel motion, inspect the quantized steps: more timeline frames
or delayed parts do not themselves create smoother motion.

**Checkpoint before cycle acceptance:** inspect actual exported rest/extreme/
transition poses and final→first return at native size and integer zoom, then
review the loop at authored speed. Follow chest→collar→neck→head, shoulder→elbow→
wrist and strap→bag through the cycle; check feet/pockets and corresponding cloth
clusters for drift, floating marks or shape flicker. Record motion and material
decisions separately. Fix attachment/phase breaks before dependent animation work.
Checks may enforce declared anchors, registered rigid parts, phase relationships,
alpha and export timing; they do not establish natural movement or artistic approval.
When actual temporal perception is unavailable, state the gap and deliver a playback
candidate for the user's review; decoded timestamps and a filmstrip are pose evidence.

## Compare corresponding forms and material roles

At the keys, compare actual baseline and candidate exports on the same matte and
scale, with source pose labels and timing. Establish correspondence using collar,
seams, silhouette, joints or other relevant landmarks. Register rigid regions when
appropriate; use local form correspondence for deforming regions. A head offset is
not a registration model for the shirt. Record occlusion or uncertain correspondence.

Track representative shadow, fold and highlight clusters through adjacent poses,
extremes, release and loop return. Let them change with surface orientation, cloth
tension and cast-shadow occlusion while preserving recognizable material roles,
value hierarchy, light direction and rendering density. Explain changed clusters
through those forms; an unexplained patch that appears, swaps light/shadow roles or
changes texture warrants correction or an unresolved/rejected appearance decision.
Declare intentional relighting/restyling as a separate variant when authorized.

An unchanged palette can still produce apparent color/material changes through
redistributed shade area and cluster topology. New-RGB counts, histograms and pixel
diffs are diagnostic observations. Motion, occlusion and ROI membership affect them;
they establish neither a defect nor an artistic pass. Exact pixels across all poses
are also not required. If a GIF looks different, decode it against the intended
native composites and inspect a shared matte before attributing the cause to art
or export. Preserve independent timings when comparing different loops.

## Make separate review decisions

For revised keys, apply [comparison review](comparison-review.md) to the actual
before/candidate exports and affected-frame inventory. Carry the attachment/context
observations through adjacent keys; crop coverage is not anatomical clearance.

Before extending keys into a cycle, and again on actual exported transitions and
loop return, record observations and a decision for each relevant dimension:

- Motion/timing and anatomy/volume: coordination, silhouette, contact, planted-foot
  behavior and connected overlaps; name pose evidence separately from playback.
- Material/shading: continuity against the appearance baseline and reference, with
  specific changed cluster/pose evidence.
- Identity/expression: intended versus incidental changes, using the facial
  procedure when features change or become ambiguous.
- Technical scope/native/export: protected pixels, palette, transparency, source
  structure, timing and fresh reopen/export checks suited to the task.

Motion gains cannot compensate for rejected material appearance or expression;
technical success cannot waive any visual decision. Retain the best eligible
checkpoint per agreed goal; if none meets it, record no selected animation and
preserve partial preferences. Correct within scope/budget or stop that branch.

Inspect native-size and useful integer zoom poses, full character/context, and
actual-speed playback at the intended timing. A filmstrip supports pose inspection,
not temporal perception. State who observed which exact playback artifact, at what
scale/speed; if only stills and decoded timings are available, retain a playback
candidate and explicitly leave temporal judgment unverified. A disclaimer is not
a substitute for the pose/material review that is available. User approval and
engine/gameplay playback remain separate evidence boundaries.
