# Image-generation and editing prompt pack

These are reusable requests, not promises of exact output. The next agent selects and completes one for a specific reference gap. No new images were generated while creating this pack.

## Before sending
1. Attach actual canonical image files. For this character, prefer the workspace's approved scene/close-up; the bundled `references/approved_concept_upload.png` is a portable fallback. Include the approved full-body reference for full-body requests. An old reconstruction is not automatically the design authority.
2. Attach an accepted native sprite when matching an established production treatment. Label identity/style and pose-only references explicitly; a pose-only image must not replace costume or identity.
3. Combine the style anchor below with **one** task prompt. Fill bracketed variables with observed/selected values. Remove irrelevant alternatives. Do not send raw placeholders or several conflicting pose requests.
4. Use available generation/editing tools and their actual schemas. Existing subscription access is preferred; no new API purchase/key usage is implied. If unavailable, use the user-request packet.
5. Inspect the generated output, record its provenance and decide its role before converting it. Repeat generations only within a declared budget.

## Prompt files
- [00_STYLE_ANCHOR.md](00_STYLE_ANCHOR.md): common identity/style instructions.
- [01_PRODUCTION_REFERENCE.md](01_PRODUCTION_REFERENCE.md): isolated clean production guide.
- [02_HEAD_EXPRESSION.md](02_HEAD_EXPRESSION.md): head or expression reference.
- [03_POSE_OR_VIEW.md](03_POSE_OR_VIEW.md): one requested pose or view.
- [04_ANIMATION_KEYPOSES.md](04_ANIMATION_KEYPOSES.md): coherent strip/key poses, with separate-image fallback.
- [05_SIMPLIFICATION.md](05_SIMPLIFICATION.md): reduce detail without redesigning.
- [06_LOCAL_CORRECTION.md](06_LOCAL_CORRECTION.md): fix a specific drift in a generated reference.
- [07_USER_REQUEST_PACKET.md](07_USER_REQUEST_PACKET.md): agent-to-user fallback.

## Dimensions and background
Specify intended **logical native dimensions and character occupancy** separately from the requested generated file dimensions. Ask for crisp, deliberately simplified artwork, then measure and process the actual returned file. A nominal “128×192” prompt or “8× enlargement” is not proof of that underlying grid. Do not paint coordinate labels/grid lines into production art; add accurate guides with software later.

Request transparent PNG when supported. Verify actual alpha; a painted checkerboard is not transparency. A plain background is an acceptable intermediate when extraction can be reviewed. Avoid matching the background to a critical costume color. Keep the untouched output and never silently remove the tote, hair wisps or shoes during extraction.

## Output bookkeeping
Record attachments and roles, prompt text, tool/model if visible, output paths/hashes, requested/actual dimensions, crop/transforms, review observations and acceptance status. Unknown version/usage values stay unknown. New reference approval for a pose does not replace the original art-style authority.
