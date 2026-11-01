# Technical seam-repair preparation

Parent's full alpha scan (`../terra56-parent-check.json`) found new enclosed,
transparent body gaps in F3–F6. Offline inspection confirms the cause: translating
selected independent upper-body cels upward exposed their former seam pixels over
the stationary denim/tote layers. These are unintended gaps, not deliberate
negative-space marks. The baseline's inherited hole at `(63,116)` remains out of
scope.

## Focused remedy pending a new lease

Create one new bottom-most visible native layer, `09-breath-seam-backing`, in a
*copy of the final source*. On F3–F6 only, paint exactly the parent-reported hole
coordinates with the RGBA colours from source frame F1 at the same coordinates.
Because the backing is below existing semantic layers, all intact pixels remain
unchanged and it is visible only through the unintended transparent seams. It uses
only baseline palette colours and makes no contour, expression, shading, timing,
or movement redesign. F1, F2, F7, F8 and the inherited F1 hole are not touched.

`prepare_technical_seam_repair.py` creates the literal MCP pixel payload from the
parent's coordinate list and baseline pixels; it does not write native artwork.
After a lease, I will inspect the actual layer order/metadata, use the generated
payload as the exact source, export all frames/GIFs to a **repair** subdirectory,
then rerun the Pillow full-alpha scan and fresh-reopen equality. The original
pass01 native/exports remain untouched as pre-repair evidence.

## GIF clarification

Parent's independent check establishes that both GIF timelines are exact against
the native frames after alpha/matte compositing. My earlier raw RGBA mismatch was
an alpha/matte representation boundary, not a visible colour discrepancy.
