# Terra 5.6 independent breathing-idle delivery

The first retained candidate was `native/terra56-breathe-pass01.aseprite`. The
technical-repair candidate is `native/terra56-breathe-seam-repair.aseprite`: an eight-frame,
740 ms forward `Breathe` tag. It is a quiet upper-body inhale/readjust loop from the
common neutral source. Feet and denim were held at source positions; the jacket,
shirt, hands and face lift one pixel in the mid-inhale (frames 3–6), hair follows
one frame later (4–6), and the tote strap lifts only at the centre (4–5). This is a
compact construction choice, informed by the supplied evidence's torso-primary,
secondary-lag approach; it does not copy the tutorial's character, cels, palette,
or timing.

## Native construction

- Model: `gpt-5.6-terra`, medium reasoning.
- Drawing backend: dedicated `mcp__aseprite_ai_artist`, headless; preflight returned
  Aseprite `1.3.18.6-dev` ready with no open sprite.
- Native baseline: `../inputs/neutral.aseprite`, SHA-256
  `d76266fa8afcd1de643e6b6421ec4dfe4fa77f8044a1d083205b921eb2f25540`.
- Frame durations: 110, 90, 80, 90, 110, 90, 80, 90 ms.
- Literal operation scope: copied baseline to an eight-frame native source; moved
  `02a-jacket-left`, `02b-jacket-right`, `03-shirt`, `06a-left-hand`,
  `06b-right-hand`, and `07-face-and-neck` by `(0,-1)` on F3–F6;
  `08-hair-tie-and-hair` by `(0,-1)` on F4–F6; and `05-tote-strap` by `(0,-1)`
  on F4–F5. `00-shoes`, `01-denim`, `04-tote`, and the hidden guide were not
  moved. No palette edits or redraw pass were made.

## Evidence and decisions

The plan/inspection boundary is in [observations-and-plan.md](observations-and-plan.md).
Evidence IDs inspected were `clip-01-core-poses`, `clip-02-chest-subpixel`,
`clip-03-arms-delay`, `clip-04-hair-settle`, `clip-05-leg-shading`, and
`clip-06-breathe-tag`. Their direct influence was phase ordering and restraint;
the eight frames, exact durations, and all character edits are authored here.

Native frame-5 and GIF preview inspection showed a stable lower body and preserved
expression/identity at 4×. The visible change is intentionally small. I did not
spend the one optional correction pass because no concrete contour break was found
in the inspected key preview. A filmstrip cannot establish temporal naturalness;
the GIF is a playback candidate pending user review.

## Deliverables and technical evidence

- Native: `native/terra56-breathe-pass01.aseprite`, SHA-256
  `d5a2e13898881ff2617d0576fcbb45eca335776201e5a777c9d7392857b1f8be`.
- Transparent frame PNGs: `exports/frames/terra56_0.png` through `_7.png`.
- GIFs: `exports/terra56-breathe-1x.gif` and `exports/terra56-breathe-3x.gif`.
- Pose sheet: `exports/pose-contact-sheet.png`.
- Fresh reopen PNGs: `exports/reopened/`; every corresponding PNG is byte-equal
  to its first export.
- Scratch save/reopen: `scratch/smoke.aseprite` / `.png`; it recorded a readable
  asymmetric pattern and isolated editable pixel. The RGB scratch lacked a useful
  palette, so palette-lock snapped attempted coloured scratch cells to black; this
  capability result is preserved rather than treated as a palette pass.
- Duplicate-only local revision proof: `proof/duplicate-only-revision.aseprite` /
  `.png`; exactly one hair-layer pixel was changed in the proof copy, never the
  retained candidate.
- Full technical boundaries are in
  [technical-checks.json](verification/technical-checks.json).

After parent alpha review identified unintended F3–F6 internal transparent seams,
I retained pass01 unchanged and added normal layer `09-breath-seam-backing` to the
repair source. It has cels only on F3–F6 and paints exactly the flagged 61/54/54/64
coordinates from the F1 baseline palette. Existing layer order/properties and the
rest frames are preserved; offline Pillow checking confirms every flagged point is
opaque and F1/F2/F7/F8 match the original rest composite exactly. See
`verification/seam-repair-checks.json` and `technical-repair-payload.json`.

The repair playback package is `exports/repair/terra56-breathe-repair-1x.gif` and
`...-3x.gif`, made offline from the repaired transparent PNGs with an opaque black
neutral matte. It retains the 740 ms visual timeline exactly; Pillow coalesced
adjacent identical visual cels into five encoded GIF frames (200/80/200/90/170 ms),
which is timing-equivalent to the original eight durations. Every decoded GIF RGB
frame equals its corresponding repaired PNG composited over the same matte. See
`verification/repair-gif-checks.json`. The original MCP-made pass01 GIFs remain
preserved separately.

Fresh MCP reopen/export validation of the repaired native remains pending the
coordinator's read-only check. No Godot playback, engine integration, user visual
approval, commit, or publication was performed.
