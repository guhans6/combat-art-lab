# Image-generation prompt pack

Compiled from `prompts/` for convenient copying. The per-task files remain the editable source. Read the attachment instructions first; an image filename alone is not an attachment.


---

# Image-generation and editing prompt pack

These are reusable requests, not promises of exact output. The next agent selects and completes one for a specific reference gap. No new images were generated while creating this pack.

## Before sending
1. Attach actual canonical image files. For this character, prefer the workspace's approved scene/close-up; the bundled `references/approved_concept_upload.png` is a portable fallback. Include the approved full-body reference for full-body requests. An old reconstruction is not automatically the design authority.
2. Attach an accepted native sprite when matching an established production treatment. Label identity/style and pose-only references explicitly; a pose-only image must not replace costume or identity.
3. Combine the style anchor below with **one** task prompt. Fill bracketed variables with observed/selected values. Remove irrelevant alternatives. Do not send raw placeholders or several conflicting pose requests.
4. Use available generation/editing tools and their actual schemas. Existing subscription access is preferred; no new API purchase/key usage is implied. If unavailable, use the user-request packet.
5. Inspect the generated output, record its provenance and decide its role before converting it. Repeat generations only within a declared budget.

## Prompt files
- [00_STYLE_ANCHOR.md](prompts/00_STYLE_ANCHOR.md): common identity/style instructions.
- [01_PRODUCTION_REFERENCE.md](prompts/01_PRODUCTION_REFERENCE.md): isolated clean production guide.
- [02_HEAD_EXPRESSION.md](prompts/02_HEAD_EXPRESSION.md): head or expression reference.
- [03_POSE_OR_VIEW.md](prompts/03_POSE_OR_VIEW.md): one requested pose or view.
- [04_ANIMATION_KEYPOSES.md](prompts/04_ANIMATION_KEYPOSES.md): coherent strip/key poses, with separate-image fallback.
- [05_SIMPLIFICATION.md](prompts/05_SIMPLIFICATION.md): reduce detail without redesigning.
- [06_LOCAL_CORRECTION.md](prompts/06_LOCAL_CORRECTION.md): fix a specific drift in a generated reference.
- [07_USER_REQUEST_PACKET.md](prompts/07_USER_REQUEST_PACKET.md): agent-to-user fallback.

## Dimensions and background
Specify intended **logical native dimensions and character occupancy** separately from the requested generated file dimensions. Ask for crisp, deliberately simplified artwork, then measure and process the actual returned file. A nominal “128×192” prompt or “8× enlargement” is not proof of that underlying grid. Do not paint coordinate labels/grid lines into production art; add accurate guides with software later.

Request transparent PNG when supported. Verify actual alpha; a painted checkerboard is not transparency. A plain background is an acceptable intermediate when extraction can be reviewed. Avoid matching the background to a critical costume color. Keep the untouched output and never silently remove the tote, hair wisps or shoes during extraction.

## Output bookkeeping
Record attachments and roles, prompt text, tool/model if visible, output paths/hashes, requested/actual dimensions, crop/transforms, review observations and acceptance status. Unknown version/usage values stay unknown. New reference approval for a pose does not replace the original art-style authority.


---

# Common style anchor — prepend to one task prompt

Use the attached approved images as the canonical identity and art-style references. This is the **same original character**, not a new character inspired by her. Preserve her recognizable face shape and eye relationships, tied brown hair with its distinctive swept crown and loose fringe, pale hair tie, natural long-legged proportions, olive hooded jacket, off-white shirt, wide blue jeans, pale shoes and cream tote wherever those parts are visible in the requested framing.

Match the source's expressive contemporary anime-influenced pixel-art aesthetic: deliberate connected color shapes, selective dark material-colored contours, readable planes of light and shadow, warm skin and the same material-color relationships. Keep its restrained, human expression and overall visual personality. Preserve the relevant palette/lighting relationships rather than merely putting the same outfit on a generic character.

Small differences needed for the requested pose or a cleaner, lower-detail production treatment are acceptable. Keep identity-bearing features and the art style stable. Simplify secondary strands, tiny folds and incidental texture before changing the face, hairstyle silhouette or body proportions. The requested action/expression may change naturally, but it must still read as this person. Keep the illustration grounded rather than chibi, glossy 3D, photorealistic or generically smooth vector art.

Only make the changes specified in the task below. Use canonical references for identity/style, and any separately labeled pose reference only for its pose. Do not treat a new pose as permission to redesign clothing or accessories.


---

# Clean production reference

## Agent preparation
Attach the original scene, approved close-up and an approved full-body view if the request is full-body. Choose `head-and-shoulders` or `full body`; use only that framing in the final prompt. Fill native size/occupancy from the current test, not a guessed permanent game setting.

## Prompt
Create one clean **[FRAMING]** production reference of the same character in the attached originals. Keep **[POSE/FACING/CAMERA]** and **[EXPRESSION]**. This is a faithful production adaptation, not a redesign or a new art-style exploration.

Use simplified but intentional pixel-art shapes that can support a later **[NATIVE_WIDTH]×[NATIVE_HEIGHT]** native study with **[CHARACTER_OR_HEAD_OCCUPANCY]**. Those are the downstream drawing constraints; preserve identity and readable clusters even if the generated file is larger. Make hair masses, eye/lid relationships, cheek/jaw, major clothing planes and accessories easy to distinguish. Retain the approved style and color relationships while reducing nonessential strand/fold texture.

Show one complete subject within the requested framing, with comfortable margins around hair and all included limbs/accessories. Use a plain unobtrusive background or genuine transparency if supported. Keep the subject clearly separated without a white fringe. Keep lighting **[MATCHED SOURCE LIGHTING OR SPECIFIC APPROVED PRODUCTION LIGHTING]**. Include no scenery, typography, borders, palette swatches, grid lines or repeated character panels.

## Review
Compare head shape, hairstyle and face against the original before processing. Check that simplifying the reference did not shift it into another pixel-art style. Reject unexpected changes to camera, costume, proportions or expression. Preserve the raw output, then document any extraction/cleanup.


---

# Head / expression reference

## Agent preparation
Attach the approved close-up and scene. For the immediate likeness study, use the same rightward three-quarter orientation and shallow relaxed smile. For later actions, replace the expression with the intended phase-specific emotion. Request one head first; use a short matched sheet only when multiple expressions are genuinely needed.

## Prompt
Create a head-and-shoulders reference of the **same character** shown in the attached approved images. Preserve her distinctive facial proportions, near/far-eye relationship, cheek/jaw, swept crown, fringe openings, tied-hair shape and pale tie. Keep **[VIEW/FACING]** and show **[TARGET EXPRESSION]**, expressed with restrained eyelid, brow and mouth changes that fit her existing personality.

Match the original's pixel-art rendering and material colors. Make the important hair and face shapes readable rather than increasing texture or smoothing everything into a painted portrait. Keep sufficient margin around the full tied hair and shoulders. Use **[MATCH SOURCE LIGHTING / APPROVED LIGHTING]**, with a plain background. Draw only this one view; omit text, labels and guide grids.

This should look like a closely matched view of the original person, with only the requested expression or production simplification changed. Avoid replacing her eyes with a different anime-eye design or making both eyes identical in a three-quarter view.

## Optional sheet variant
Only after one convincing view exists, request **[N]** equally framed heads for **[ORDERED EXPRESSIONS]**, retaining the same camera, head scale, hairstyle and palette. Measure the actual layout afterward. The sheet is reference material, not automatically an animation.


---

# One additional pose or view

## Agent preparation
Attach canonical identity/style references, an accepted native style sample if available, and an optional pose-only sketch. Identify which parts are newly visible. Do not request a turnaround simply because it is customary; request the actual view needed next.

## Prompt
Draw the same original character from the attached canonical references in **[SPECIFIC POSE OR VIEW]**. Use **[CAMERA / FACING / VIEW ANGLE]** and **[EXPRESSION]**. Preserve her identity, outfit construction, hair/tie, body proportions, material colors and the original pixel-art aesthetic. Any attached pose-only guide controls body placement, not character design or rendering style.

Show **[FRAMING]** with all necessary limbs, hair and accessories inside the canvas. Keep the cream tote and strap physically consistent with the chosen pose unless the brief explicitly authorizes a different accessory state. Newly visible surfaces should be a conservative continuation of the approved design, not new decorations.

Use the same apparent character scale and lighting treatment as **[ACCEPTED BASE REFERENCE]**, with clear readable large planes and restrained small details suitable for **[TARGET NATIVE STUDY / OCCUPANCY]**. Return one image with a plain background or actual transparency when supported. No text, scenic environment or multiple unrelated poses.

## Review
Check identity and style before pose utility. A new back/side view is a proposed interpretation, not observed ground truth from the original. Review hair attachment, coat/tote overlap and anatomy. If only one body region failed, request a bounded correction rather than discarding all correct design information.


---

# Coherent animation/key-pose reference

## Agent preparation
Decide the action before generation. Attach canonical identity/style references plus the accepted native base and any approved key poses. Fill ordered phases, count, layout, camera, scale and root-motion intent. A short technical motion test may precede combat, but do not choose an unapproved weapon/action or call a blink a combat proof.

## Prompt — one sheet
Using the attached canonical references and accepted base, create one coherent **[N]-pose** reference sheet for **[ACTION]**. Every pose must be the same original character in the same art style, outfit, hairstyle and palette family. Maintain **[CAMERA/FACING]** and a consistent character scale; changes in limb reach must not change the person's size.

Arrange the poses in **[EXACT REQUESTED LAYOUT]**, in this order: **[NUMBERED PHASE DESCRIPTIONS]**. Keep every body part/accessory within its slot with enough action margin. Show **[IN-PLACE MOTION OR INTENDED ROOT TRAVEL]**. Expression should follow each phase while preserving the character's identity. Retain the approved pixel-art cluster/shading language rather than giving each pose a different illustration finish.

Use a plain background or actual transparency where supported. Include no typography, borders, drawn grid lines, scenery or extra alternative poses. Keep effects separate from the readable body action; show the contact pose clearly. These are key poses for later native cleanup and timing, not a request to redesign the character.

## Alternative — separate image request
Use `03_POSE_OR_VIEW.md` for one missing/corrected phase. Attach the canonical identity/style images and accepted neighboring poses. Specify the exact phase, camera, scale and outfit invariants. Do not generate each frame from a text-only description of the character.

## Required review
Measure actual pose count and crop positions. Inspect every pose for identity/style/anatomy changes and accessory continuity. Convert/trace using one approved native treatment, then establish timing and in-betweens as needed. A contact sheet is not proof of smooth motion. Normalize using explicit anchors, preserving intentional displacement, and validate played output.


---

# Lower-detail adaptation without redesign

## Prompt
Adapt the attached approved character/reference into a simpler production version for a **[NATIVE_WIDTH]×[NATIVE_HEIGHT]** study with **[CHARACTER/HEAD PIXEL OCCUPANCY]**. Preserve the same recognizable face, expression, hairstyle silhouette, body proportions, outfit and pixel-art aesthetic. The goal is fewer details in the same visual language, not a different character or a generic retro/chibi style.

Keep the identity-bearing hair masses and fringe openings, near/far eyelid relationships, cheek shape and mouth character. Combine minor hair strands into readable clumps, reduce tiny fabric creases, and use broader coherent light/shadow shapes. Preserve material-color relationships and selective outlines. Add colors only when they help readability; do not manufacture a tiny palette at the expense of likeness.

Retain **[POSE/FACING/CROP]** and **[APPROVED LIGHTING]**. Use **[PLAIN BACKGROUND / ACTUAL TRANSPARENCY]**, with no scenery or text. The generated file may be larger than the intended native study, but design it for that detail budget. Omit painted grids, artificial checkerboards and labels.

## Agent checks
Do not infer compliance from the prompt. Measure actual dimensions, inspect logical pixel consistency and compare expression/style against the original. Deterministic reduction creates the final candidate dimensions. Keep the high-resolution original available as the identity/style anchor; a simplified proposal is not automatically authoritative.


---

# Correct drift in a generated reference

## Agent preparation
Attach the actual generated candidate to edit plus the canonical original. Name exactly one coherent mismatch and what should remain stable. Do not claim the model sees a file that has not been attached. For native pixel corrections, prefer scoped Aseprite operations rather than this generation prompt.

## Prompt
Edit the attached **candidate** to correct **[SPECIFIC OBSERVED MISMATCH]**, using the attached **canonical original** as the identity and art-style reference.

Change **[PRECISE FEATURE/REGION AND DESIRED RELATIONSHIP]**. Preserve **[POSE, CAMERA, EXPRESSION EXCEPT REQUESTED CHANGE, CLOTHING, COLOR RELATIONSHIPS AND OTHER LOCKED FEATURES]**. Keep the same pixel-art rendering treatment and level of detail. This is a focused repair, not a new composition or character redesign. Return the same framing with the requested correction.

## Agent review
Compare the entire returned image, not only the requested region. Generative editing can alter surrounding features. Keep the unedited candidate and canonical original. Accept the useful correction only after checking identity, style and unintended changes. Exact protection for final native pixels must use verified local edits, not trust a selection prompt.


---

# User-side generation request template

The agent completes this packet when direct generation is unavailable or blocked. Deliver the completed message in an editable writing block. Use one focused request at a time; do not ask the user to assemble a complex workflow.

## Message template

Please generate **[ONE SPECIFIC IMAGE OR SHORT SHEET]** in ChatGPT Images or your available image generator, using the attached originals.

**Attach:**
- **[EXACT CANONICAL FILE PATH/NAME]** — identity and art style.
- **[EXACT CLOSE-UP / ACCEPTED NATIVE FILE]** — expression or production treatment.
- **[OPTIONAL POSE-ONLY REFERENCE]** — pose only, not character design.

**Paste this image prompt:**

[COMPLETED STYLE ANCHOR + ONE TASK PROMPT, WITH ALL VARIABLES RESOLVED]

Return the original generated image file rather than a screenshot of the editor. The result should preserve the same recognizable character and aesthetic; small pose-appropriate differences are acceptable. The agent will check the actual dimensions, background/alpha, layout and consistency, then process and construct the native asset.

**Why it is needed:** [NAMED EVIDENCE GAP].

**Save/return as:** [PROPOSED REFERENCE FILENAME, NOT A CLAIM THAT IT ALREADY EXISTS].

## Agent continuation
Record the request as pending. Continue unrelated preparation where useful. Once the actual returned file is accessible, register it and inspect it against the originals before using it. Never report generation or acceptance as complete just because a prompt was delivered.
