# Luna56Max quiet breathing idle

## Outcome

Independent `gpt-5.6-luna/max` construction from the frozen neutral source is
complete. The deliverable is a transparent 128×192 six-frame native animation
with a tagged 1,700 ms loop, native 1× and 3× GIF proof, ordered PNGs, contact
sheet, fresh-reopen evidence, and a duplicate-only native edit proof.

## Source and independent decisions

- Frozen source: repo `inputs/neutral.aseprite`, SHA-256
  `d76266fa8afcd1de643e6b6421ec4dfe4fa77f8044a1d083205b921eb2f25540`.
- Frozen video evidence pack SHA-256:
  `c946289c8fc1ff74faf4fbc0206c58f2e1c9eebd37e18f595f5418e9b5e93a95`.
- The source is a 128×192 RGB native sprite with the hidden
  `guide-source-seed (hidden)` and eleven visible normal-blend named layers.
  The original layer names, order, visibility, blend mode, palette and hidden
  guide were preserved. No added layer was needed.
- The chosen motion is a restrained six-frame breath: the chest/upper body
  rises by one pixel, the tote follows one key later, and the loop returns to
  exact neutral. Shoes and denim are protected to keep both feet planted. No
  blink or expression redesign was introduced.
- Timings are authored for this character and are not inferred from the video
  recording FPS: `420, 140, 180, 220, 180, 560 ms` (total `1700 ms`).

## Native MCP construction operations

All native operations below were performed by the dedicated headless
`mcp__aseprite_ai_artist` server after the explicit editor lease. No UI,
Code-MCP, direct editor CLI/Lua, backend proxy, image generation or native
file-writing script was used.

1. `preflight(mode=headless)` reported Aseprite `1.3.18.6-dev` and Pebbly
   extension `0.8.2`; the source was opened and inspected with `sprite_info`.
2. The source document was saved as `luna56-idle.aseprite`.
3. Frame 1 was duplicated five times with `linkCels=false`, retaining 12
   layers per frame (72 full-canvas cels total).
4. Frame durations were set to the six values above, and tag `idle-breathe`
   was created for frames 1–6, forward, looped.
5. Relative cel moves were applied in batch by named layer:
   - frame 2: upper-body layers `(dx=0, dy=-1)`;
   - frame 3: upper-body `(0,-1)`, tote and strap `(0,-1)`;
   - frame 4: upper-body `(0,-1)`, tote and strap `(1,-1)`;
   - frame 5: tote and strap `(1,0)`;
   - frame 1 and frame 6 remain exact rest; shoes and denim never move.
6. `look filmstrip` and pixel reads were used to inspect the complete loop and
   exact ownership. No artistic correction draw pass was required.
7. The native source was saved and exported through MCP to ordered PNGs and
   native 1×/3× GIFs.

## Verification and evidence boundaries

- `verification.json` contains per-frame hashes, alpha bounds/opaque counts,
  GIF durations and matte/alpha-normalized frame comparisons.
- Both GIFs contain six frames with durations exactly matching the native
  timeline. After flattening alpha to the comparison matte (and nearest-neighbor
  normalizing the 3× GIF), every visible frame comparison is exact.
- The saved source was closed, freshly reopened, re-inspected, and re-exported.
  All six fresh-reopen PNGs are pixel-identical to the first exports.
- A duplicate-only native copy was edited on `03-shirt`, frame 3, at `(55,39)`
  by one pixel and saved as `revision/luna56-idle-duplicate.aseprite`; its
  revised frame differs from the final frame by exactly one composited pixel.
  The final source was not changed by that proof.
- `sprite_info` confirmed 6 frames, 12 original layers, 72 cels, the hidden
  guide and `idle-breathe` tag; `read_pixels`, `look ascii`, `look filmstrip`,
  save/reopen and export checks supplied the mechanical evidence.
- The server preflight advertised a `validate` feature, but no callable
  `validate` tool was exposed in this session. That check is reported as
  unavailable rather than claimed as passed.
- No Godot preview or gameplay-scale check was run. User visual approval,
  publication and engine integration remain outside this experiment.

## Local artifact map

See `delivery.json` for the machine-readable relative paths and SHA-256 map.
The main native source is `luna56-idle.aseprite`; frames are `frames/frame-0.png`
through `frames/frame-5.png`; GIF proof is under `proof/`; and the reviewed
contact sheet is `contacts/idle-contact.png`.

Status: native documents closed; lease released; offline packaging complete.

## Technical seam/overlap repair

The parent alpha audit found new enclosed body holes caused by the intentional
one-pixel upper-body/tote moves: 64, 44, 83 and 65 pixels on frames 2–5. The
first native and all first-pass exports remain preserved at the original paths.
After a new editor lease, I opened that source and saved a separate repaired
copy under `technical-repair/`.

The correction is deliberately sparse and technical, not a motion redesign:
one visible normal-blend layer named `09-anim-overlap-repair` was added at the
end of the stack. It has cels only on frames 2–5 and contains exactly the
checker-listed coordinates, colored from the exact neutral composite using the
existing palette. Frames 1 and 6 have no repair cel and remain exact neutral;
all original named layers, their order/properties, the guide, shoes, denim,
timings and tag remain intact. Native draw readback reported 64/44/83/65
changed pixels with no color snapping, and every listed coordinate is opaque
with its intended neutral color after repair.

The repaired native was saved, closed, freshly reopened and re-exported. The
fresh source reports 13 layers, 76 cels, and `09-anim-overlap-repair` cels on
frames 2–5. Reopened PNGs are pixel-identical to the repaired exports. Native
1×/3× GIFs retain six frames and the exact authored durations; matte/alpha
comparisons are exact. The repaired contact sheet is
`technical-repair/contacts/idle-contact.png`.

A duplicate-only repaired native was edited by one pixel at `(73,36)` on the
new repair layer, saved and exported as `technical-repair/revision/`; the
repaired deliverable differs by exactly one pixel in that proof copy. The
machine-readable repaired evidence is in
`technical-repair/verification.json`; `delivery.json` points to the repaired
paths while retaining an `original` block for the first pass.
