# Reach replacement practice copy

Comparison at exact2×: left=current frame2, right=deterministic converted reach.
Agent assessment: converted head angle, shoulder/hand pose and tote silhouette are
closer to original PNG, so selected as a manual-cleanup starting point. Fine pixel
noise and transitions to neighbors still need user review; no final art approval.

Open clean-reach-replacement.aseprite. Select frame2 (second column) and Corrections
(top row) to paint corrections. To erase base pixels, duplicate Frame2-converted
reach, hide its original and edit the duplicate; erasing a blank Corrections layer
does not erase underlying art. Replacement is flat, not separated into body parts.
The original eight layers remain for the other18frames; only their frame2cels were
removed in this copy. Source animation and converted PNG remain unchanged.

Checks:19frames,256×208,original timings/tag/palette; F2=100ms and exact converted
RGBA; all other18composites and source cels exact; blank Corrections; fresh native
reopen/export exact. No AI redraw, palette snapping or quantization. Native changes
through existing headless Aseprite MCP only. Advertised validate tool is not exposed;
focused independent native/pixel checks used. No new Godot run or publication.
