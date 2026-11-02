# Hair comparison r01 — frozen study specification

Date: 1 November 2026. User explicitly authorized three hairstyle options and subagents, with parent review for discrepancies. Existing image_gen built-in route only. This is original character concept exploration, not a native sprite, animation, final identity approval or Godot proof.

## Shared provisional appearance

Young male, early/mid twenties; lean athletic adult with mildly stylized (approximately 6.5–7 heads tall) proportions, not chibi. Warm medium-light brown skin within user medium-fair/brown range; lean adult face, modest dark eyes, light jaw/upper-lip stubble, visible face and hair. Long near-black hair is a common provisional color. Restrained observant expression, no smile exaggeration.

Cloth-first simple LIGHT armor: muted indigo short-sleeved collarless cloth top, modest fitted charcoal torso protection (two or three broad planes, not a full heavy suit), open/mobile shoulders/elbows, one tapered worn-steel forearm guard with a long central ridge inspired by the researched Thanjavur silhouette, simple narrow rust-colored waist tie/belt, short split waist cloth over fitted charcoal/indigo trousers, simple dark ankle boots. Compact one-handed straight sword sheathed at hip, dark grip, small guard, scabbard angled to avoid leg overlap. Sparse detail; no jewelry, religious iconography, royal decoration, cape, hood, cybernetic limbs, gadget clutter, neon or magic. Subtle future feel only through refined materials, seams and flush fastening shapes. All details are fictional study choices, not an asserted historical kit.

Color roles: muted indigo main cloth, charcoal secondary cloth/protection, dull worn steel, small rust accent, natural warm medium-light brown skin and near-black hair. Reference swatches for prompt intent only: indigo #344257; charcoal #292d33; rust #914d3a. Final native palette not selected.

## Framing and style

Single full-body character on flat warm very light gray background (#e6e2da). Requested portrait image 1024x1536, same actual dimensions for all variants. Near-side three-quarter view facing image-right, enough face visible. Upright relaxed-alert pose, feet planted, arms relaxed slightly clear of torso, body and head identical across variants. Feet baseline approx y1390, body/head top around y180, figure centrally framed; these are prompt requests to verify, not guaranteed measurements. No labels/text/logo/borders or other characters. Same neutral upper-left illumination and restrained grounding shadow.

Pixel-style concept art with crisp stepped contours, coherent deliberate pixel clusters, broad restrained material shadow planes. Adult proportions and small restrained facial features; avoid strongly anime faces, oversized eyes/heads/spiky hair, painterly blur and photorealism. This is a high-resolution generated concept; no actual native resolution or game readability is established.

## Only comparison variable

A: long hair in a LOW PONYTAIL tied near nape, swept away from face, tail to upper back.
B: long hair HALF TIED at rear, remaining lower length LOOSE to upper back; same color/length family, same exposed face and hairline.
C: long hair fully LOOSE, swept BACK off face to upper back; same color/length family, same exposed face and hairline.

Generate A first as a shared edit anchor. B and C MUST edit A as their sole identity/layout target, never be independent text-only redraws. Inspect A using view_image before editing. Change only hair arrangement and the immediately occluded/revealed background or neck/shoulder areas. Preserve exact face/expression, outfit design/color, armor/sword, hands, body proportions/pose, camera, feet baseline, lighting, framing, background and image dimensions. Do not rescale or recenter the character due to hair silhouette changes.

## Generation budget and records

Initial generation: one base A plus one edited B and one edited C (three images). Parent may authorize a bounded targeted repair for a specific observed discrepancy. No generation loop, unrelated character variants, new service, CLI fallback, native construction or pipeline edits.

Every worker owns only its A/ B/ C directory, saves exact prompt and exact input paths, original built-in output path, copied raw file, dimensions/hash, metadata and self-review. Parent owns this shared spec, manifests, comparison layout and final review. Preserve originals and rejects. No commits/pushes.
