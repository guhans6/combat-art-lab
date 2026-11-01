# Standing reconstruction v02

Face-first refinement of the preserved v01. Main asset: `standing.aseprite`; main transparent export: `assets/export/standing-v02/standing.png`.

The same 12 semantic layers, 128x192 canvas, pose and y186 ground anchor are retained. `standing-face-checkpoint.aseprite` preserves the face-only increment. `standing-face-pass01.aseprite` is an earlier face attempt, not the final candidate. The tote-color revision remains a test-only sibling; main design retains a cream tote.

From the repository root:

```sh
/Applications/Aseprite.app/Contents/MacOS/aseprite --batch \
  --script-param root="$PWD" --script "$PWD/assets/source/standing-v02/draw.lua"

/Applications/Aseprite.app/Contents/MacOS/aseprite --batch \
  --script-param root="$PWD" --script "$PWD/assets/source/standing-v02/verify-and-revise.lua"

/Users/guhan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  assets/source/standing-v02/preview-and-check.py
```

Existing output directories must be present. The source uses authored geometry/pixel instructions; only the comparison script opens the reference. Native drawing/revision uses no computer interaction or extra MCP. The Python command uses the existing bundled Pillow runtime; no new installation was needed.

The final candidate is pending visual review. See the [refinement record](../../../docs/experiments/2026-10-26-standing-refinement/record.md) for changes and observed checks. v01 remains the previous milestone and has not been overwritten.
