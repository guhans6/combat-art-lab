# Single authorized mouth correction plan

The parent’s defects-only review of the first export says its mark at the far-right edge of the lower face reads as a protruding lip/pout. This is the expression-failure condition that authorizes the single correction. I inspected the actual approved close-up and scene again beside the baseline and first candidate, at native and 8× integer zoom. In the reference, the closed smile sits inside the cheek below the eye line and reads as one short shallow stroke; the candidate’s first mark sits too far toward the profile edge and directly under the existing warm facial patch.

## Frozen correction scope (before second draw)

- Keep the same native owner: `08-hair-tie-and-hair`; do not transfer ownership.
- Correction mask: `[65,28,71,30)` in zero-based, half-open canvas coordinates (x=65–70, y=28–29, 12 pixels). This is the union of the prior mark and the small central-cheek replacement.
- Restore prior pixels to the baseline colors: `(68,29) #fda977`, `(69,28) #f6a26e`, `(70,28) #fda977`.
- Place the 3-pixel stroke at `(65,29)`, `(66,29)`, `(67,28)`, in existing warm-brown palette color `#744c40`.
- Rationale: this moves the mark two to three pixels inward, beneath the eye midpoint/inner cheek rather than at the far profile edge, and gives a slight upward asymmetry toward the character’s gaze. It avoids the warm facial pixels at x=68–69,y=27, the profile boundary at x≥72, and all eyes/face outline pixels.
- No other edits. This is the one permitted correction; no further art pass is in budget.

