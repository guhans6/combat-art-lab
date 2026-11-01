# Built-in image-generation prompts

Both calls used the local rough cutout as edit target and the approved scene and close-up as identity references, with `transparent_background: true`.

## Attempt 1

> Use case: background-extraction
> Asset type: clean supporting reference for sprite conversion
> Input images: Image 1 is the edit target; Images 2 and 3 are identity and lighting references.
> Primary request: Create a clean transparent-background PNG of exactly the same full-body female pixel-art character shown in Image 1. Remove only the bright white/black edge halos, stray fragments, and contamination outside the character.
> Subject invariants: same standing pose and framing; tied brown hair with cream tie; face and small relaxed smile; olive hooded jacket, cream shirt, loose blue jeans, cream tote bag, brown-and-cream shoes. Preserve the original pixel-art aesthetic, proportions, interior drawing, colors, and warm lighting.
> Constraints: true transparent background with no checkerboard painted into the image; leave empty space fully transparent; clean crisp character boundary; no new objects, no background, no text, no cropping, no pose change, no redraw or restyling of the face, clothing, or lighting. Treat Images 2 and 3 as authoritative if Image 1’s edge artifacts obscure the character.

## Attempt 2

> Use case: background-extraction
> Asset type: transparent PNG reference for sprite conversion
> Input Image 1 is the exact edit target. Images 2 and 3 are identity references only.
> Correct the failed cutout: output ONLY the same full-body pixel-art character from Image 1, with genuine alpha transparency everywhere outside the character. Delete the dark gradient, glow, colored haze, black backdrop, white halos, and all detached specks. Preserve the character itself: identical standing pose, framing, tied brown hair and cream tie, face and small smile, olive hooded jacket, cream shirt, blue jeans, cream tote, shoes, pixel-art style, internal colors, and warm light. No background pixels of any color or opacity. Do not crop, repaint, redesign, smooth, alter the face, change proportions, move the character, or add any objects/text.

## Interpretation correction

Attempt 2 initially looked dark in the generation preview. Its white, checkerboard, and dark-gray alpha-matte previews demonstrate that the dark display was not an exterior glow after normal compositing. It is retained as `inputs/clean-generated-cutout-v1.png`.
