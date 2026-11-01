# Terra 5.6 quiet-breath idle — preparation

Prepared 30 October 2026 by `gpt-5.6-terra` at medium reasoning. This document is
pre-lease planning only: no Aseprite API call, native mutation, or production-sprite
write has occurred.

## Frozen inputs inspected

| Input | SHA-256 | Role |
| --- | --- | --- |
| `../inputs/neutral.aseprite` | `d76266fa8afcd1de643e6b6421ec4dfe4fa77f8044a1d083205b921eb2f25540` | Common 128×192, 12-layer native rest source; read-only. |
| `../inputs/neutral.png` | `e7c62ff0e2f3f88b10b17904322f834175e62d33579cc646a9e6396f940b57ad` | Visible baseline inspected at 1×. |
| `../inputs/character-scene.png` | `a274a80133371b61387848495bf0dd93546ba5daf0a60c051b27109237160eae` | Approved full-body identity/style anchor, visually inspected. |
| `../inputs/character-closeup.png` | `0577f22e5ab53bfa9f05f8a63947cf39c0626c84efae88d6594b1cce9421ada7` | Approved head/upper-body anchor, visually inspected. |
| `../inputs/blink-source.aseprite` | `25ae8dc1952cf5ef62d081735f52a56cb4cd726c08423d639b3c510b2d6f6f42` | Optional inherited blink source; not selected for this first construction pass. |
| `../inputs/evidence-pack.zip` | `d1b8998eb2eace9e74062a7afb3c5bc0e8711a6666ef95c8c723ac134eb65457` | Immutable video-evidence delivery. |

The neutral is a compact, front-facing pixel construction: tied dark-brown hair,
olive zip jacket, pale tee, roomy blue denim, cream shoulder tote, and two planted
sneakers. Its readable anchors are the toe-row/ground alignment, diagonal strap,
jacket opening, near hand/pocket area, hair silhouette, and quiet small mouth/eyes.
The approved images retain a warmer, more softly modeled version of exactly those
identity cues; they are identity and material anchors, not pixels to copy.

## Source evidence actually inspected

I read `README.md`, `EVIDENCE-REVIEW.md`, the motion index, and directly inspected
still extractions from these native-speed excerpts, retained locally in
`prep-video-stills/`:

- `clip-01-core-poses` (05:04–05:18): two breathing poles organize the body above
  a stable lower anchor.
- `clip-02-chest-subpixel` (06:54–07:20): intermediate chest-highlight clusters
  soften the one-pixel pose change instead of a blanket displacement.
- `clip-03-arms-delay` (10:14–10:32): secondary hand/arm response is delayed,
  not locked to the torso.
- `clip-04-hair-settle` (12:07–12:29): hair has a modest delayed flare/settle.
- `clip-05-leg-shading` (14:26–14:46): leg silhouette can stay fixed while its
  shadow clusters change.
- `clip-06-breathe-tag` (15:46–16:10): a 13-frame breathe sequence is an example,
  not a timing mandate; the project is separated from a held idle state.

The pack does *not* establish its original editable cels, palette, or exact
durations. My timing and all character-specific drawings will be authored decisions.

## Task profile and independent construction decision

I will make one `Breathe` loop with **eight frames**, so that the sequence reads
quietly rather than as a repeated bob: 110, 90, 80, 90, 110, 90, 80, 90 ms
(740 ms total). Frame 1 is the rest anchor and frame 5 is the inhaled extreme;
frames 2–4 and 6–8 are separately authored transitions. The stationary foot sole
pixels and canvas origin are the grounding invariant.

The main construction pass will use a copied native source and named cels on its
existing semantic layers. I will inspect the actual layer owners before committing
the following planned operations:

| Region | Rest/inflate decision | Return/secondary decision | Material rule |
| --- | --- | --- | --- |
| Feet / sole | Exact reuse across every cel. | Exact reuse. | No silhouette or shade change. |
| Jeans | Keep outer silhouette and crotch seam fixed. | Shift only one or two existing dark inner-fold clusters late in the cycle. | The denim highlight/shadow roles remain on the same leg planes. |
| Jacket + tee torso | Inhale increases chest/upper-jacket width by one isolated contour step at the upper ribs; jacket opening and tee clusters are reconstructed around it. | Transition pixels form the soft displacement, rather than moving entire horizontal rows. | Preserve olive base/shadow and pale-tee hierarchy; no relighting. |
| Near/far sleeves and hands | Shoulders lead, cuffs/hands lag by one transition frame and move at most a pixel. | Cuffs settle after the torso. | Preserve hand silhouette and sleeve shade direction. |
| Tote / strap | Strap attachment remains coherent at shoulder; bag body is largely held. | One-pixel delayed lower/bag contour settle only if layer ownership permits. | Cream bag planes stay stable. |
| Head / face | Shift head as one rigid 1-pixel vertical response only if required by neck correspondence; expression stays neutral. | Hair/bun has a late one-pixel settling contour, not an independent sway. | No eye/mouth redesign and no face-palette changes. |

This is an animation construction, not a local face correction. It is deliberately
limited to one coherent construction pass. I reserve one correction pass only for a
specific defect seen in the exported loop (for example a broken jacket contour,
unreadable overlap, or inconsistent denim shadow), retaining both checkpoints.

## Planned native and proof sequence after lease grant

1. Discover the dedicated headless Aseprite MCP schema, preflight, then run its
   required scratch smoke in this folder: asymmetric transparent two-layer sprite,
   readable preview/grid, one-pixel edit, save/reopen/export equality, and a
   duplicate-only proof edit. I will record literal tool results and versions.
2. Open a private copy of `neutral.aseprite`; inspect 12-layer metadata, palette,
   hidden guide, frame/cel ownership, and the baseline composite before any drawing.
3. Save a rest checkpoint; create all eight timing cels and perform the bounded
   operations above on explicit layer/frame targets. I will retain a literal
   operations record (coordinates/grids or tool payloads) and export every
   transparent frame through MCP.
4. Inspect native-size and nearest-neighbour enlarged key and transition sheets;
   examine torso, shoulder/neck, cuff/hand, hair, bag strap, and jeans shadows.
   Make at most the one stated correction pass.
5. Build faithful neutral-matte 1× and 3× GIFs from the MCP-exported PNGs,
   preserving indexed/RGBA pixel values (no quantization). Decode the GIFs and
   compare them frame-for-frame against the source exports.
6. Check all frame alpha for unintended holes/partial pixels; compare canvas,
   palette, layer metadata, hidden guide and unchanged rest data against the copied
   baseline as appropriate. Save/reopen the final source and require fresh exported
   composite equality. The duplicate-only revision will be in a separate proof
   copy, never silently folded into the selected animation.

I can inspect pose sheets and decoded timing, but cannot personally establish
temporal naturalness until playback is actually observed; that remains an explicit
boundary rather than an inferred pass. Godot integration, user approval, commits,
and publication are outside this assignment.
