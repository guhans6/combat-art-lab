# Aseprite reconstruction principles for the first original character

**Date:** 26 October 2026  
**Scope:** a newly specified original woman character: brown tied hair, olive hooded jacket, off-white tee, wide high-waisted blue jeans, pale sneakers, and a cream shoulder tote. These rules support faithful construction from the user's approved reference, not copying any *Until Then* character, pose, setting, or sprite.

**Status note, 27 October:** this is preserved first-pass guidance. Its suggested ~180px working height and economical face treatment were hypotheses, not demonstrated fidelity limits or approved facial simplifications. In particular, preserve the reference's distinct near/far eyes and rightward expression rather than applying the single-eye suggestion below mechanically. Use the newer [concept-to-native research](concept-to-native-pixel-art.md), [style priorities](../art/style-guide.md#reference-feasibility-and-preservation-priorities) and [feasibility workflow](../workflow/art-production.md) for new reconstruction; existing protected corrections retain their own locks.

## Working scale

The requested roughly 180-pixel character height is a production choice, not an inference about the reference game. At that height, face, hands, jacket folds, shoe shape, and tote strap can read without turning into smooth painted detail. Start the standing test in a canvas with at least a little transparent margin above the hair and below the ground anchor; lock the ground line before drawing. Confirm the actual canvas size only after the first game-scale Godot preview.

## Build order and specific rules

1. **Silhouette before interior pixels.** Block the head/hair mass, jacket/tee torso, broad jean silhouette, separated shoes, and tote as five readable masses in flat colours. At thumbnail size the tote must still read as an offset cream shape with one unbroken shoulder-to-body strap. Do not use a dark outline around every internal seam.
2. **Use deliberate clusters.** A cluster is a purposeful connected group of same-colour pixels. Prefer short stepped edges that support a curve or plane; remove isolated one-pixel noise unless it carries a deliberate cue such as an eye, earring, or fabric nick. Use the Pencil, Line, and Polygon tools for clean constructed edges, then revise clusters by hand. Aseprite documents all three tools. [Aseprite drawing](https://www.aseprite.org/docs/drawing/)
3. **Separate planes by value before hue detail.** For each material, define shadow, base, and light roles first: brown hair (dark mass, warm base, sparse light ridge); olive jacket (deep fold/shadow, main cloth, smaller warm light); off-white tee (not pure white); blue jeans (large midtone, stronger inseam/under-jacket shadow, limited knee/outer-leg light); pale sneakers (simple light mass plus sole separation). Reserve the brightest light for a few focal edges, instead of spreading it across every material.
4. **Keep face information economical.** Give the head a readable hairline and jaw/neck separation before adding features. At this scale, one eye/eyelash cluster, a small nose-plane shift, and a controlled mouth cluster are usually more stable than fully rendered facial symmetry. Review 100%, enlarged, and gameplay scale; only the last determines whether a facial mark earns its pixels.
5. **Let clothing explain the body.** Put the jacket's highest contrast at the open front/hood and sleeve overlap; use the tee as a simpler light central plane; use the jean waist, crotch/inner-leg negative space, and large outer-leg shapes to show wide high-waisted construction. The tote overlaps the jacket, not the body contour ambiguously; its strap follows a simple, readable diagonal.
6. **Design for animation now.** Keep `body`, `hair`, `jacket`, `tee`, `jeans`, `sneakers`, `tote`, and `guide-ground` as named layers, with a separate `fx` layer later. The contact points—feet, shoulder/strap, hands, and hair tie—must be unambiguous in the still before animating. Aseprite's layer/frame/cel model lets one cel be revised without altering the others. [Aseprite basics](https://www.aseprite.org/docs/basics/)
7. **Do not force a small palette prematurely.** Begin RGB with named palette swatches so the character can be matched to the chosen reference. Move to Indexed mode only once a deliberate palette is approved; indexed pixels point to palette entries, so a later swatch edit changes every use. [Aseprite colour modes](https://www.aseprite.org/docs/color-mode/)

## Sources worth applying

- Pixel artist Pedro Medeiros (Saint11) maintains free, artist-authored visual studies that include character silhouette, portrait/face/human, clothes/fabric, shading/volume, outlines/contrast, banding, idle animation, attack impact, and motion blur. Use these as a review checklist, not a style template. [Saint11 tutorial index](https://saint11.org/blog/pixel-art-tutorials/) (accessed 2026-10-26)
- Saint11 identifies himself as Pedro Medeiros and links educational material on low resolution, consistency, scaling, and use of 3D reference. The research here inspected the written index, not a video tutorial. [Saint11 home](https://saint11.org/) (accessed 2026-10-26)
- Aseprite's official documentation confirms Lua scripting, sprite creation/open/save-copy operations, and the relevant image, selection, palette, layer, cel, frame, tag and graphics-context API surfaces. That is enough for a reproducible construction script; it does **not** prove an arbitrary script can drive every interactive drawing tool identically across installed versions. [Aseprite API](https://www.aseprite.org/api) (accessed 2026-10-26)
- Aseprite's official animation guide supports per-frame duration, tags, onion skinning, and preview. Use it once the still passes game-scale review; do not generate attack frames before the standing pose and anchor are approved. [Aseprite animation](https://www.aseprite.org/docs/animation/) (accessed 2026-10-26)
- Lospec's beginner article is a respected community orientation source rather than a first-party editor manual. Its useful constraint here is that pixel art is deliberate pixel control, not merely a small image or low colour count. [Pixel Art: Where to Start](https://lospec.com/articles/pixel-art-where-to-start/) (accessed 2026-10-26)

## Tool decision

Use the already installed `/Applications/Aseprite.app` build and its built-in Lua capability for the first proof. No additional MCP, plugin, asset pack, or external drawing dependency is needed before we verify that build can create, save, reopen, and export the native source. Any later tool should be selected only to solve an observed limitation.

## First proof checklist

- Native source reopens with the named layers intact.
- The standing pose reads at gameplay scale, with grounded shoes and a clean tote strap.
- An intentionally small revision—change jacket accent or tote detail—affects only its layer/expected pixels.
- Export remains transparent where expected and preserves the ground anchor.
