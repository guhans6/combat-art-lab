# Matched full-character conversion comparison

This converter compares the rough transparent cutout with an image-generation
cleaned cutout. It is deliberately separate from E0's 120x112 head crop.

Both inputs are placed on the same 1024x1536 canvas, reduced to 128x192 using BOX
sampling, and quantized with one 48-colour palette extracted only from near-opaque
pixels of the rough source. Alpha is reduced with BOX sampling and retained; it is
not thresholded into a game-ready binary silhouette.

If the generated image arrives at another size, it is aspect-preserved and centered
on the frozen canvas. `recipe.json` records that transform. A difference in pose,
identity, framing, lighting, or edge treatment therefore remains source evidence;
this comparison does not hide it through manual alignment.
