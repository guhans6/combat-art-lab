# Trial A construction recipe

## Method

Use assisted reconstruction with a converted seed plus bounded native cleanup. The
source has the exact target aspect ratio, so the first preparation is a single
8:1 nearest-neighbour reduction from 1024x1536 to 128x192. This preserves source
clusters without introducing a smoothing pass. A reviewed alpha threshold then
removes low-alpha halo samples (alpha <= 16) and makes the retained silhouette
opaque. The reduction is retained as a named seed, not presented as the finished
editable asset.

The Aseprite master keeps the seed, source-guided raster regions, and authored edits
distinguishable. Planned/native layers are:

1. `converted-seed` — source-derived reduced pixels, retained for provenance.
2. `hair-face-raster` — converted source pixels clipped to the head/neck region.
3. `jacket-shirt-raster` — converted source pixels clipped to the torso region.
4. `jeans-raster` — converted source pixels clipped to the lower-body region.
5. `tote-shoes-raster` — converted source pixels clipped to tote/shoe coverage.
6. `silhouette-coverage` — authored opaque edge repairs and reviewed transparent
   openings; only used where the seed has a visible alpha defect.
7. `hair-face` — authored hair-mass, fringe, eye, cheek, and smile cleanup.
8. `jacket-shirt` — authored jacket/hood/shirt plane and overlap cleanup.
9. `jeans` — authored broad denim planes, leg gap, and restrained folds.
10. `tote-shoes` — authored tote strap/bag and shoe cluster cleanup.
11. `cleanup-accents` — sparse final pixels with a reason recorded per cluster.
12. `reference` — locked visual guide only, hidden in runtime exports.

If the backend cannot promote the seed into a paint layer without flattening, keep
the imported seed as the visible base and demonstrate meaningful semantic overlay
layers plus a localized overlay edit. Do not claim that a reference guide is art or
that a flattened import alone is a rig.

## Ordered native pass

1. Create a new 128x192 RGBA sprite in the dedicated editor session and save it in
   this trial directory. Inspect the returned document structure before edits.
2. Import the prepared seed/reference at native size with nearest-neighbour fit.
   Hide or remove the guide from every runtime export.
3. Establish the named semantic layers in one batched layer operation where the
   backend supports it. Keep `converted-seed` below authored layers. When useful,
   duplicate the converted seed and clear outside reviewed rectangular semantic
   regions so the native source retains inspectable parts instead of only empty
   labels; retain the original seed as provenance/backing.
4. Inspect the full composite at 1x and integer zoom. Confirm the silhouette, hair
   tie, head turn, eye relationship, jacket opening, wide-leg negative space, tote
   attachment, and shoe grounding before detail.
5. Add one bounded authored cleanup transaction: remove obvious halo/edge leakage,
   consolidate noisy clusters, and restore the restrained smile/eye hierarchy. Use
   only the palette already present or explicitly sampled from the equal inputs.
6. Inspect a native preview and an exact pixel/ASCII crop of the head and lower
   silhouette. Read back any region before changing it again.
7. Save the native source and export the first transparent PNG as `passes/pass-01.png`.
   Keep every failed attempt under `passes/` instead of overwriting it.
8. Build the comparison sheet with the approved original crop, pass-01 native-size
   candidate, and identical 4x nearest-neighbour views. Record visual observations
   separately from technical checks, then stop and wait for supervisor feedback.

## Palette and alpha policy

Start with source-derived colors from the seed. No fixed palette count is imposed.
Do not color-key a whole garment. Any transparency deletion requires a reviewed
spatial mask and a contrasting-background inspection. Preserve intentional hair
openings and the leg gap; repair only enclosed holes or visibly broken coverage.

## Revisions and proof

Pass 02 and pass 03 each make one coherent correction chosen from observed defects;
the supervisor may identify mistakes but does not supply coordinates or colors. The
candidate and every prior pass remain intact. After the artistic passes, duplicate
the native source, perform one useful localized edit (for example a tote accent or
jacket zipper mark) on the duplicate, reopen/export it, and compare protected
semantic layers and the untouched candidate. This proof-only duplicate is not an
additional art pass, but all editor calls remain in the ledger.

## Reproduction

Run:

```sh
docs/experiments/2026-10-29-luna-independent-trials/trial-a/scripts/prepare_seed.sh
```

Then use only the dedicated Aseprite MCP session after the supervisor's explicit
slot grant. The source hash, seed hash, native source path, export settings, all
operations, and actual editor-call count must be recorded in the pass records.
