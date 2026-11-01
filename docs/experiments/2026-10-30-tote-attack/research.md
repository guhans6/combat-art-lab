# Tote swing: recovery and momentum research

**Status:** research and pose-sheet review only; no native art, exports, timings, engine
scene, or configuration changed.  
**Recorded:** 30 October 2026  
**Question:** How can the current two-handed tote swing make the middle recovery/grip
and bag momentum read more convincingly without discarding or regenerating the sheet?

## Inputs inspected

- Supplied main six-pose sheet:
  `codex-clipboard-7365e076-79f3-450e-aea8-9e144b9f2f81.png` (1774 × 887).
  It reads left-to-right/top-to-bottom as neutral, draw-to-grip, rightward extension,
  long strike/follow-through, extended continuation, then re-shoulder.
- Supplied three-pose diagnostic sheet:
  `codex-clipboard-7d7c7f95-8808-4a79-9084-0cc80022e098.png` (2172 × 724):
  left wind-up, middle weak recovery, right re-shoulder.

These are still-image/pose observations, not temporal playback. The proposed changes
below therefore remain a playback candidate, not a finding that the action already
works at authored speed.

## Focused source findings

| Source and access | Direct lesson | Applied, bounded use here |
| --- | --- | --- |
| Raymond Schlitter, [*Pixelblog 9: Melee Attacks*](https://www.slynyrd.com/blog/2018/9/8/pixelblog-9-melee-attacks) (creator-authored text/image tutorial; accessed 2026-10-30) | A stance should fit the implement’s balance; heavy actions benefit from a slower anticipation/recovery, while the smear stays brief. A motion path should lead naturally from stance to follow-through; overshoot occurs before a moving object settles. Game feel constrains how much anticipation/recovery is acceptable. | Read the tote as a **loaded but flexible** improvised weapon, not a sword. Preserve the lunge/long extension and make the recovery show an arrest then redirect rather than a sudden hang. Do not add filler frames merely to make it smooth; retain a quick transit between committed strike poses and decide recovery duration with gameplay. |
| Raymond Schlitter, [*Pixelblog 53: Punches and Kicks*](https://www.slynyrd.com/blog/2024/11/25/pixelblog-53-punches-and-kicks) (creator-authored text/image tutorial; accessed 2026-10-30) | The examples build force through torso/hip change while an intended supporting foot contact is retained; recovery brings the limbs and torso part way back rather than resetting every part simultaneously. It also calls out fabric/hair physics as a separate consideration. | The strike should be driven from planted foot/root → pelvis → thorax → shoulders → elbows → wrists, with the bag following the wrist/handle rather than leading independently. In the middle recovery, begin to re-center the pelvis/torso and bend the elbows, but leave the tote farther along the prior right/down path for one transition before it arrives by the hip. |
| Ferdinand Engländer, [*Anticipation*](https://www.animatorisland.com/animation-terms/anticipation/) (author-attributed Animator Island glossary entry; accessed 2026-10-30) | A brief motion opposite the coming force both creates room to apply it and tells the viewer the impending direction. | The existing left wind-up already performs this job. Strengthening recovery does **not** require a new, larger wind-up or regeneration; protect that readable contrast and spend the edit on the post-strike redirection.
| Ferdinand Engländer, [*Beyond the bouncing tail*](https://www.animatorisland.com/beyond-the-bouncing-tail/) (creator-authored article; accessed 2026-10-30) | Follow-through/overlap is a whole-body relationship, not a detachable “tail pass”: hips, shoulders, head, and wrist may lead at different times, and attached elements differ in weight/stiffness. Plan what drags, pulls, pushes, follows, and swings before adding the secondary motion. | Use a declared chain instead of a blanket one-frame lag: planted feet/root → pelvis → thorax/shoulders → elbows → wrists/hands → handle loops → tote rim/body. The two arms and hands are the active constraint; hair/jacket hem can have smaller, separately justified follow-through. The bag needs neither a fixed rotation nor the same delay as every other part.
| Animator Island, [*Best animation exercise for beginners*](https://www.animatorisland.com/best-animation-exercise-for-beginners/) (publisher’s own lesson page with an embedded free tutorial; accessed 2026-10-30) | The lesson’s published chapter list covers planning an arc, varying spacing/ease, timing charts, volume, fast motion, and anticipation. | Before drawing extra detail, put the wrists and tote mass on a visible arc/timing plan, then test the spatial gaps: open/committed strike, rapid deceleration/redirect, then re-shoulder. Preserve bag volume and handle length across the keys; only deform where cloth tension or compression explains it.

### Source limits

- All five are animator-/publisher-authored instructional pages, not a physics
  simulation or a tote-specific combat study. Their principles guide a stylized pose
  decision; they do not prove a particular real tote mass, cloth fill, hit force, or
  combat-safe technique.
- The first four were inspected as text/HTML and page metadata; no claim here rests on
  visual inspection of their embedded images. The embedded Animator Island lesson was
  **not played or visually watched** here; only its publisher-written description and
  chapter list were used. No claim is based on seeing its motion.
- No current Aseprite or Godot implementation fact was needed for this recommendation,
  so no software-documentation/version claim is made. Aseprite 1.3.18.6-dev and Godot
  4.7.2 are historical project context, not tested prerequisites for this research.
- No source specifies a universal part delay, frame count, or quality score. The
  intended gameplay speed, active/contact interval, camera, tote contents/weight, and
  final facing are still unresolved in the project motion guide.

## Reading the existing poses

The six poses already establish a useful broad story: a two-handed pickup/grip,
counter-direction wind-up, an open rightward strike, a longer follow-through, and a
return to shoulder. The long bag silhouette and widened lunge communicate reach well.

The diagnostic middle recovery is weaker because it appears to jump from the fully
committed swing toward a vertically hanging bag. The hands/forearms do not yet show a
clear shared handle constraint or a change from pushing the load outward to catching it
and guiding it home. That makes the tote look lighter and more detached than the
preceding large arc, even though the final re-shoulder is a plausible destination.

This is an inference from the supplied stills and the attachment-chain reasoning above;
it is not a claim that a rendered sequence will necessarily fail.

## Minimal revision plan: strengthen, do not regenerate

1. **Keep the present macro keys.** Preserve the wide planted/lunging strike and the
   re-shoulder pose; they are the valuable silhouette anchors. Do not replace the tote
   with a rigid club or make a fresh pose sheet merely to change the recovery.
2. **Make a recovery-transition drawing between extended follow-through and the current
   middle/return.** The leading leg/root remains credibly planted until the body weight
   visibly starts returning; pelvis and ribcage begin to untwist/re-center. Bend both
   elbows toward the torso and keep both hands visibly around the same short bundle of
   handles. Do not have an elbow, wrist, or handle disconnect simply to place the bag.
3. **Let the load briefly remain downstream.** At that transition, the bag body is
   still outward and slightly low relative to the hands while the wrists redirect it;
   then its center travels on a tightening curved path toward the carrying-side hip.
   The handles span continuously from both grips to the rim, with a small, plausible
   change of curve/tension. Their visible length must not telescope from frame to frame.
4. **Deform according to cloth, not rigid rotation.** Keep the bag’s broad mass
   recognizable, but let its rim/near handle corners be pulled toward the hands and
   let the hanging lower body lag/settle. Compression/creases belong where the grips
   tension the top and where the bag changes direction; do not rotate the whole tote
   as one hard prop or apply identical lag to tote, sleeves, jacket, and hair.
5. **Finish the body recovery deliberately.** Once the tote reaches the hip-side
   carrying path, re-stack shoulders above the re-centering pelvis, restore the arm
   bend, then let the feet/root return only when the authored action needs it. A
   planted lunge must not slide under a supposedly weighty swing; any step must be an
   explicit new contact, not independent per-frame ground alignment.

## Suggested phase/pose map (no preset frame count)

| Phase | Existing material / focused addition | What must be legible |
| --- | --- | --- |
| Ready and shared grip | Existing neutral and draw-to-grip | One believable two-hand handle bundle; shoulder, elbow, wrist, and tote attachment agree. |
| Counter-wind-up | Existing leftward preparation | Body/bag travel opposite the eventual rightward swing while feet/root set the base. |
| Contact / committed extension | Existing rightward extension | Strike direction and attack extent are readable; active gameplay interval remains an explicit later choice. |
| Follow-through | Existing long extension | Root and lunge absorb the swing; hands have not inexplicably released or shortened the handle. |
| **Arrest and redirect** | **New localized recovery-transition key** | Pelvis/thorax begin returning, elbows bend, hands retain shared grip, tote remains downstream/low and begins a curved return. |
| Carry-side settle / re-shoulder | Existing middle recovery revised, then existing re-shoulder | Tote approaches hip/shoulder path with shortening visible arc, then cloth/handles settle under a supported carry—not a sudden vertical drop. |

The new key is a proposal, not an instruction to add a fixed number of frames. If an
already-existing pose can be redrawn to express the same arrest-and-redirect moment,
use that localized correction first. Determine holds and timing only after the action
is played at intended speed; contact, follow-through, recovery, and the return to
allowed player control should be recorded separately.

## Review checklist for the next art pass

- Compare current and revised keys on the same matte at native size and integer zoom.
- Scrub/preview the action at authored speed; inspect the path of pelvis, shoulders,
  elbows, wrists, handle loops, tote rim, and tote mass—not just the outer bag
  silhouette.
- Confirm the planted/lunging foot and root do not drift. If a reposition step is
  desired, declare its contact and root offset instead of fitting the lowest pixel to
  ground each drawing.
- Check that grip ownership, arm lengths, shoulder/elbow/wrist continuity, handle
  length, tote volume, jacket overlap, and hair attachment survive the recovery.
- Inspect without smear, shake, or impact effect before using those effects. Decide
  motion/anatomy, material/cloth, source/export, user visual approval, and later Godot
  gameplay separately, as required by the motion workflow.

## Unresolved before implementation

- Is the tote empty, lightly loaded, or deliberately heavy? Its intended contents
  change the size and number of visible settling beats.
- Is the rightward extension only a visual swing or the active hit interval? No
  collision/hitbox timing has been selected.
- Does recovery return to a neutral stance, a shoulder carry, or a combat-ready grip?
  The current final pose suggests shoulder carry, but that has not been approved as
  gameplay state.
- Actual-speed native playback, user visual approval, and Godot gameplay observation
  are not part of this research artifact and remain unperformed.

## Next owner/action

The construction agent can make the localized **arrest-and-redirect** recovery key in
the current native sequence, retain the best current sheet as a checkpoint, then export
and review a no-effects playback. The user should assess the resulting tote weight,
grip readability, and return feel before the sequence is called visually approved.
