# Matched head comparison

The companion image `matched-head-comparison.png` is one equal-size 16× nearest-
neighbor strip, left to right:

1. **APPROVED REFERENCE** — `input/references/character-closeup.png` crop
2. **RAW SEED** — `evidence/seed-head-16x.png`
3. **BEST PASS-02** — `evidence/pass-02-head-16x.png`
4. **NEW PASS-03** — `evidence/pass-03-head-16x.png`

The first panel is padded to the same 544×576 panel size because the approved
reference crop is not sprite-sized. The three sprite panels use the same crop,
scale and nearest-neighbor treatment. Pass-02 is the prior eligible candidate;
pass-03 is the last allowed face-expression attempt.
