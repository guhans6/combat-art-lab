# Actual Reddit video study and coordinated idle probe

30 October 2026. **Actual video access succeeded; one coordinated native prototype is retained for user playback judgment.** The previous study's HTTP403 limit was resolved by the user's direct MP4. No source artwork was copied into the character.

## Evidence actually inspected

[Source Reddit thread](https://www.reddit.com/r/PixelArt/comments/abp752/creating_the_idle_animation/); expiring direct media URL, download hash and provenance are in [provenance.json](provenance.json). Parent downloaded HTTP200; copied the exact file locally as reference.mp4,2382655bytes. ffprobe identifies H264,480x480,30fps,29.266667seconds; [full metadata](ffprobe.json). Decode succeeded with installed ffmpeg. License is unspecified: local study only, no art reuse or redistribution as a deliverable.

Inspected [exact process frames](process-contact.png) at0/2/4/6/8/10/12/14seconds; [overview](overview-contact.png); all50 extracted final-segment samples at10fps in [contact1](final-contact-1.png) and [contact2](final-contact-2.png). Also decoded66 consecutive30fps frames covering24–26.2seconds for [measurements](measurements.json). The final contacts show decoded chronological poses; these still-image tools do not establish real-time playback watched by the model.

Observed editing: selection/repositioning of the head and torso creates conspicuous white separation gaps; later frames restore green shirt/sleeve/strap continuity. By14seconds the gaps have been filled. In final repeated poses, cap/head, shoulder line, torso and backpack move upward together over a stable leg base, followed by a lower settling pose. Mouth shape changes during the accent. This is an expressive bob/huff, not an anatomical definition or our desired amplitude. The useful lesson is coordinated masses, gap repair, and holds.

Measured from compressed screen pixels in24–26.2seconds: red cap top moves approximately y84→80→76, then y88 on the settling pose; green-shirt upper bound changes about206→198; backpack brown upper bound about183→178. A stable bounds state persists roughly24.733–25.533seconds. These are threshold-based observations of encoded video timing and screen pixels, **not original sprite pixels, source cel durations or the author's animation frame rate**. Compression and mouth/shape changes make precise native reconstruction unjustified.

## What our failures show

The earlier lifted shoulders under a fixed head changed their relationship and read as shrugging. The next pass fixed all upper structure and animated interior cloth, which the user read as wind. These observed failures implicate motion design and overconstrained coordination before resolution. They do not prove that this canvas cannot convey breathing.

A one-pixel step is the smallest spatial change available under this palette/grid policy. It can look stepped when a slow idle has only two vertical positions. More timeline frames alone do not create intermediate geometry. A higher native grid could permit smaller displayed movements but would require a separate controlled test; enlarging this sprite alone establishes no quality gain. First test coherent motion on the existing grid, then judge whether its remaining stepping justifies such a test.

## One bounded prototype and result

[Prototype record](prototype/record.md), [3x exact animation](prototype/proof/neutral-3x.gif), [prior cloth left / coordinated right](prototype/proof/cloth-left-coordinated-right-3x.gif). Parent inspected actual full-body and upper-body contacts, found correlated head/collar/shoulder movement and no obvious seam/foot regression, and requested no extra aesthetic pass. Eight tiny peak-pose joint gaps discovered by independent coverage checking were backed locally; no broader redraw occurred.

The new candidate preserves the original neutral expression and blink drawing/timing. Head/neck/shoulders/chest rise1px together, tapering into fixed waist, hands and tote. There are only two head-height positions, with a small lower-chest follow-through. Natural breathing at played speed remains unproven. User next plays the GIF; no Godot, gameplay, publication or artistic approval is claimed.
