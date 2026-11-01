# Deterministic image preparation

No model, image generation, AI cleanup, network request or editor launch is used
by this conversion. The source PNG was previously AI-generated; the input mask
and anatomical anchor are previously reviewed choices. The run applies them.

On this Mac double-click `run-reach.command`, or run it in Terminal. Each default
run creates a new dated practice folder. Optionally pass a new output directory:

```sh
./run-reach.command /private/tmp/my-reach-draft
```

Open the resulting `converted.png` in Aseprite, save your own `.aseprite`, duplicate
the converted layer, and correct that duplicate yourself. `preview-3x.png` only
enlarges the display; `report.json` records the recipe and input/output digests.
The animation has not been replaced. This is a flat source-derived draft.

The launcher uses an already installed local Pillow runtime; if that cache is
removed it falls back to `python3`, which must have Pillow 13+. It does not install
anything. Portable equivalent:

```sh
python3 convert_image.py --recipe reach.json --out /path/to/new-output
```

The recipe keeps the foreground mask, samples nearest source RGB, uses binary
alpha, fits this upright pose to 183px and positions its foot/hip reference on a
256×208 canvas. No palette quantization, dithering, head replacement, tote redraw,
semantic layer segmentation or anatomy repair occurs. Visible colors are a subset
of the source’s colors, not necessarily the standing sprite’s palette. The rendered
output contains 4490 visible RGB colors. This preserves source hues rather than
forcing the earlier rejected small palette. It is not a claim of polished pixel craft.

For another image, supply a JSON recipe with `source`, optional `mask` (same image
size, white=foreground), `height`, `canvas`, `source_anchor` and `target_anchor`.
Without a mask, an alpha threshold (default160) defines foreground. Dirty alpha or
colored fringes need a suitable mask; this script cannot discover an arbitrary
character’s silhouette reliably. Do not fit every animation pose to183px: this
preset is specifically for the upright reach. Other poses need shared scale and
intentional anchors. Existing output directories and clipped placements are refused.

Earlier capability: parent branch `work/e0-deterministic-replay` contains
`docs/experiments/2026-10-29-clean-cutout-conversion/conversion/convert_fullbody.py`
(frozen128×192/48-color comparison), the deterministic E0 replay, and the new-keys
smear recipe (which also reconstructs head/prop geometry). Those are experiment
recipes, not a general converter. This small standalone preparation preserves the
reach source instead of invoking their reconstruction steps.

Library reference checked 1 November 2026:
[Pillow Image transforms](https://pillow.readthedocs.io/en/stable/reference/Image.html).
