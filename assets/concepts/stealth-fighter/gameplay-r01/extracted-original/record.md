# Original background extraction attempt

One built-in image generation edit, 2026-11-01. No retry. Input was the sole edit target: `assets/concepts/stealth-fighter/atmosphere-r01/A/simplified-01.png` (SHA-256 `e1dcf18e72ce22b8b6c6031d0f00da91259dcbf4c2bfbb0e0c12c8d1c56b6e1e`). Output is the unchanged raw tool result, `cutout.png` (SHA-256 `a9bcfb49e2652658ef309e1dc465964728a5dd128e60ee25a5627945e51945a0`). Tool source: `/Users/guhan/.codex/generated_images/01a197f7-c88f-7b61-946d-56113aa56765/exec-5979550b-4673-4129-a773-cfcf04634b5d.png`. The call used `transparent_background: true`.

Exact prompt:

```text
Use case: background-extraction
Asset type: sprite cutout
Input image 1: the provided image is the sole edit target.
Primary request: Isolate the complete character as a cutout on actual transparency. Remove the entire surrounding scene, including floor, haze, wall, glow, rim-light spill and all shadows outside the figure. Alpha must be 0 immediately outside the character silhouette; do not paint a black, white, or checkerboard plate.
Constraints: Change only the background. Preserve the complete character unchanged: exact same pose, camera, face, outfit, proportions, colors and pixel-art appearance.
```

Output dimensions 1024 × 1536; actual alpha: 1,122,644 zero, 450,220 partial, and 0 fully opaque pixels. Nonzero-alpha bounding box `[55, 19, 1004, 1503]`, exclusive maximum, Core Graphics bitmap coordinates. This broad bounding box does not establish a tight silhouette. Visual inspection shows substantial dark and orange halo outside the figure, and the character has been redrawn with altered proportions, face and detail. This fails the requested extraction and invariance criteria; it is not a clean sprite cutout or approved gameplay asset. No engine or user visual approval is claimed.
