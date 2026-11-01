# Checkpoint observations

- Opened canonical scene and supporting cutout/old clean plate visually before work.
  Scene/close-up remain identity/style authority; the cutout has edge artifacts and
  changed facial details, so no cutout pixels are used. Existing clean plate is only
  a supporting scenery source in this new experimental branch; older drawn scenery
  is preserved. This does not reverse its prior rejection or claim new user approval.
- static-seed-review.png and static-composite-3x.png inspected. Same character/stance,
  proportions, hair/outfit and source lighting survive the fixed 4:1 reduction.
  Warm background contamination appears around lower trouser edges/open leg space.
  Continue one scoped matte cleanup; no independent redraw, head replacement or scale change.
- static-cleaned-review.png inspected. Denim boundary cleanup removes visible warm
  source contamination; reference proportions and stance remain. Face is necessarily
  much smaller than the prior bust study and must be judged at game scale. Native
  canvas is 96x216 with explicit padding; it is not a larger portrait pasted on a body.
  Continue to static Godot import/playback before idle expansion.
- Environment source conversion uses the same spatial reduction, a 96-color environment
  policy and binary visible-part masks. 13 parts reassemble the source-derived context;
  six form the first shop's visible parts. Occluding plants may remain within these
  visible samples; no hidden architecture or ready parallax cutouts are inferred.

- Actual Godot static runtime: 4.7.2.stable.official.ed1daf0bf, OpenGL/Metal compatibility
  renderer on Apple M3 Pro. ART_LAB_READY reported a 362x296 viewport, one frame,
  nearest filter and fixed root (108,48). Engine viewport capture succeeded and was
  visually opened at native size and 3x. Character/background density and warm/cool
  relationships fit materially better than the old independent redraw; small face
  remains soft. Shoes meet pavement with no visible second figure behind them.
  Continue bounded idle construction. The HUD second line was clipped, so final
  viewport reserves 32 rather than 24 pixels below the unchanged 362x272 art region.
- Headless editor import logs an installed-engine cleanup crash on exit, including
  editor_node singleton/thread cleanup messages, even with normal cache access. The
  separate graphical game runtime starts/render-captures successfully. No clean
  editor-exit claim. Native Godot CUA access was not approved; do not retry through
  another UI path. Runtime-produced images/logs remain the observed boundary;
  real keyboard/button interaction is not claimed.
