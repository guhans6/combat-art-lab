# Pass-01 gate review

## Decision

`pass-01.png` is rejected as an artistic candidate. At the delivered-artifact
boundary it is the unchanged shared seed, not a visible face/gaze/smile repair.
The raw seed remains the best eligible baseline. The saved native file is kept
as a failed attempt because its correction layer is useful for diagnosing the
export boundary, but it is not selected for comparison or release.

## Evidence

- Export dimensions/type: 128×192, 8-bit RGBA PNG.
- Export file SHA-256:
  `7353611071482ea1e879ab9c247fb1d92c7bd90050b8eb99cbec4cdbdf612d12`.
- Export decoded RGBA SHA-256:
  `8839680f1bc70c1c99653a28c76c6f8ea41f401d2755c93146d765523cb5806c`.
- Raw seed decoded RGBA SHA-256: the same
  `8839680f1bc70c1c99653a28c76c6f8ea41f401d2755c93146d765523cb5806c`.
- Native face correction layer: eight visible opaque pixels, retained in
  `pass-01.aseprite` but absent from the exported PNG.

## Next baseline

Use `input/shared-source-seed-baseline.aseprite` and its verified PNG as the
next-pass source/evidence baseline. Do not use `pass-01.png` as a best candidate,
and do not infer improvement from the internal face-layer preview. Before any
new art pass, run a bounded technical proof that a native edit changes both the
composite readback and exported PNG; otherwise report the export/compositing
capability boundary and stop.
