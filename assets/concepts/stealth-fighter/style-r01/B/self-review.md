# Variant B self-review — Carved / atmospheric

## Observed result

`raw.png` is 1024×1536 and keeps the neutral light background, near-identical standing full-body placement, visible half-tied long hair, warm brown face, indigo cloth, charcoal trousers/armor, steel guard/sword, and rust waist accent. Its rendering uses more sculpted multi-value clusters, broken dark-to-light armor boundaries, deeper leg and hair shadows, and limited steel-edge wear. Cloth remains broader/matter than the more selectively accented metal.

## Drift flags

- **Medium risk — anchor exactness:** the face, bangs, chest armor shaping, hand/sword details, and some boot/cloth edges have been reinterpreted rather than being raster-identical. They appear to preserve identity and placement, but parent visual comparison should specifically check profile/expression and equipment contours.
- **Low-to-medium risk — texture density:** the chest armor and hair have visibly more mottled internal clustering than the anchor. It reads as carved/weathered rather than a uniform filter at review size, but should be judged for clarity at gameplay scale.
- **No observed prohibited drift:** no scene/vignette change, blood, horror costume, pallid skin, grey palette replacement, magic/neon/cyberpunk additions, extra equipment, or copied Moonscars character/environment.

## Evidence boundary

This is one generated concept-rendering candidate only. It is not native sprite construction, animation, Godot playback, user visual approval, or a production-ready asset.
