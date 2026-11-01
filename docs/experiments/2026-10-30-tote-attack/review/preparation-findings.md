# Preparation findings carried into this rescue

1. Equal grid slots were not equal pose bounds. The full main6 PNG contains bag
   tips beyond nominal cell boundaries. The first crop discarded these pixels
   before resizing, so merely widening a final canvas could not restore the bag.
   The rescue extracts complete source silhouettes/components, masks neighboring
   pose spill, retains one source-family scale, then registers the intended ground
   contact. Native320×192 adds action margins while drawn character scale is retained.
2. The first neutral-head transplant removed anatomical collar backing. Its later
   silhouette connection still contained a doubled neck. Native component/anchor
   tests catch missing connections, not the correctness of a connected joint; the
   independent visual key review remains necessary. Rescue keeps source head/neck
   together and reviews identity/materials rather than enforcing a faulty transplant.
3. The reported lack of editable raster import was an inference from one reference
   tool's guide-only behavior. Parent ran actual `sprite_manage open PNG`, inspected
   its editable normal RGB layer, saved native and changed exactly one pixel with
   `draw grid`. Evidence/png-paint-import-proof.json disproves the blocker. The existing
   adapter guidance now explains this capability test; no new backend/installation.

These findings support this local source-guided construction. They do not establish
universal automatic segmentation, arbitrary pose inference, other-host installation
or artistic approval. Original sources and both failed artist attempts are retained.
