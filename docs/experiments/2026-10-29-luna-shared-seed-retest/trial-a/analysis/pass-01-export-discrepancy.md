# Pass-01 export discrepancy

## Classification

Pass-01 is an unchanged-seed export and therefore fails the artistic-goal gate.
The native document contains an internal face correction layer, but the actual
PNG delivered at the editor boundary is byte-for-byte the shared baseline. The
face-layer readback is retained as implementation evidence only; it is not a
visible-artifact proof and pass-01 is not an eligible candidate.

## Observed evidence

- Native source: `passes/pass-01.aseprite`, SHA-256
  `609e2f13df50f36448c75eda38b2268c4e3808ce427105e6e135e57181a1242f`.
- Protected base layer `shared-source-seed`: decoded RGBA SHA-256
  `8839680f1bc70c1c99653a28c76c6f8ea41f401d2755c93146d765523cb5806c`,
  7,844 visible pixels, binary alpha.
- Correction layer `pass-01-face-correction`: eight visible opaque pixels in
  the intended face mask; its native cel raw/decoded SHA-256 is
  `cf0ab95ae966916f12314201cf41c27178e1c577c9c4d62e24dad500a3613997`.
- Export: `passes/pass-01.png`, 128×192 RGBA, file SHA-256
  `7353611071482ea1e879ab9c247fb1d92c7bd90050b8eb99cbec4cdbdf612d12`,
  decoded RGBA SHA-256 equal to the raw seed
  (`8839680f1bc70c1c99653a28c76c6f8ea41f401d2755c93146d765523cb5806c`).
- Read-only local compositing of the eight fully opaque overlay pixels predicts
  decoded RGBA SHA-256
  `5c6533d48ed388fd44295a70848b02693d74a3f2231cf844c4d14bf6bcce0d97`, so the
  exported artifact does not include the native overlay.

## Narrow hypotheses, not conclusions

The evidence is compatible with an export/compositing boundary problem rather
than a failed draw: the overlay cel persists in the native file, but both the
composite readback and PNG export resolve to the protected base. Possible causes
include layer visibility/blend/compositing state not honored by this export route,
an exporter that resolves only the base cel, or an MCP document-state mismatch.
No root cause has been selected without a controlled editor probe.

## Next-pass gate

The raw seed export is the only eligible baseline. Before any further artistic
edit, one small non-art technical probe must demonstrate that a deliberately
localized native change appears in both composite readback and exported PNG.
If it does not, stop and report the backend/export capability boundary; do not
reinterpret an internal layer readback as visual success. Preserve this failed
pass and all hashes unchanged.
