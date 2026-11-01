# Headless transaction differential probe

- Date: 29 October 2026.
- Scope: infrastructure-only diagnosis of trial B's pre-art Aseprite transaction
  failures. No contestant source, reference, or output was opened.

## Trigger evidence

Trial B's [blocker evidence](../../trial-b/blocker-evidence.json) reports that a
fresh headless 16×16 document accepted `sprite_manage new`, `sprite_info`, and
read-only `layer list`, but each write (`layer` rename/create and `draw` grid/rect)
failed with `aseprite_error` and an opaque `function:0x...` message. It remained
unmodified and was closed unsaved. This is a technical block before an artistic pass,
not an art-quality result.

An initial static hypothesis was that the installed 0.8.2 extension's `new` branch
sets `app.sprite` but not `app.layer`/`app.frame`, whereas transactional mutators call
`app.transaction`. A read-only source assertion reproduced that code shape. That is
not sufficient causal proof, and the actual differential below falsifies it as a
general current-backend defect.

## Actual differential

The parent paused both contestants and granted a separate headless infrastructure
slot. Aseprite preflight reported ready (1.3.18.6-dev; extension 0.8.2). Two scratch
documents used identical operations:

1. `sprite_manage new` created 16×16 RGB `#35`; `sprite_info`; batched rename of
   `Layer 1` to `probe-base` plus creation of `probe-edit`; one 3×3 filled red
   rectangle at `(2,2)` on `probe-edit`; exact 3×3 layer readback; save/export/close.
2. `sprite_manage open` opened the deterministic transparent
   [opened-blank-16.png](opened-blank-16.png); `sprite_info`; the same layer batch,
   rectangle, and exact readback; save/export/close.

Both layer batches succeeded with two visible editable layers. Each drawing call
reported `pixelsChanged: 21`; exact layer readback returned nine `#ff0000` samples.
The opened-document preview visibly contains only the red 3×3 square. Both exports
are byte-identical (`2baea1fba775f3b77455969c4770dea4438751baa744b416282b8adacb935ea1`).
The native outputs are retained as [new-blank.aseprite](new-blank.aseprite) and
[opened-blank.aseprite](opened-blank.aseprite).

## Result and boundary

The precise new-vs-open transaction hypothesis is **not reproduced** in the shared
backend. No extension, configuration, mode, package, fixture, or global setting was
changed; both scratch documents were closed. There is no evidence for a shared
workspace-local adapter repair, and none was applied. Trial B's recorded failure
remains preserved; further diagnosis needs a fresh failure trace from its own session
or another safely scoped infrastructure reproduction. This probe gives no artwork,
coordinates, or corrective guidance to either contestant.
