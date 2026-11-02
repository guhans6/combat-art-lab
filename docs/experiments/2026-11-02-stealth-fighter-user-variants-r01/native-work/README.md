# Four editable user-variant static sprites

Final candidates: variant-01, variant-03, variant-04, variant-05. No winner selected. Each folder contains:

- static.aseprite and exact static.png: final source and transparent export.
- reopened.png: fresh dedicated-MCP native reopen/export.
- recipe.json, native-draw-ops.json and semantic-owner PNGs: hash-bound source, mask, palette and native-grid reproduction inputs.
- source-spatial-mask-native.png and raw-unquantized.png: reviewed spatial source transfer; raw-seed.png is the final64-color seed, exactly equal to the native composite.
- source-mask-review-3x.png, face-review.png, review-seed.png and native-owner-contact-3x.png: source/mask/appearance and editable-owner review artifacts.
- edit-proof.aseprite, edit-proof.png, edit-proof-reopened.png and edit-proof-comparison-8x.png: useful24px bracer-only revision on a duplicate; not a new proposed design.
- coverage.json, edit-proof-protection.json and edit-proof-png-check.json: focused observed checks.
- pass00-mediancut/: retained first conversion preparation.01 also retains its initial native.
- pass02-preownership/: prior native/proof sources, before source-backed semantic ownership repair.04 additionally retains pass01-precoverage/ before its three-pixel alpha correction.

Read observations.md for construction decisions, source-specific face/appearance observations, repair evidence, limitations and next ownership. checks.json is the fresh consolidated technical audit; mcp-final-metadata.json contains actual final native tool readbacks. The initial broad ownership split and median-cut palette are not the final sources. Native sources were created/edited only with dedicated MCP; scripts only prepare/review/audit. The exposed backend has no callable validate tool; none is claimed.

Body240px in128×264 at y13..252; intended gameplay body152px via shared152/240 scale. One held-rest frame each,64 visible source-derived colors and binary alpha. Runtime evidence and user artistic selection are separate from these native checks.
