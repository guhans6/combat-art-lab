# The Quiet Keep — Current A scale playground

Open this project in Godot 4.7 and run the main scene. It is an idle/scale comparison, using the approved main-character idle-r02 and borrowed GothicVania architecture.

- **Side by side** shows A / B / C together, initially96 /128 /160 pixels tall.
- **Single** shows only the selected character in the center bay. Camera and world size stay fixed.
- Click **A / B / C**, or press1 /2 /3, to select which character the height slider edits.
- The height slider runs64–240 pixels. The sprite's source body is240 pixels tall; this changes display scale, not native resolution or detail.
- **Pause / Play**, **‹ / ›**, **Speed** and **Guides** help compare the exact same poses.
- **Reset** restores the three sizes, comparison mode, normal speed and playing idle.

Keyboard: M switches views; Space pauses; comma/period step frames; R resets; G toggles guides; F11 toggles fullscreen. No walking or combat animation is included.

The world renders at1200×480 within a1280×800 interface. Fullscreen/window resizing scales the whole view uniformly; it does not change the in-world comparison. All three actors share one animation clock. The original4entry1800ms timeline is preserved at1× speed. Character art and native source are unchanged.

Backdrop: Luis Zuno / ansimuz, GothicVania Church Pack. Only the architecture and stone floor are used. This is a temporary ruined-cloister mood/size test, not a world-design selection. See CREDITS.md and ART-LICENSE.txt. No music or third-party characters are used.

Implementation: playground.gd owns UI and a shared timeline; stage.gd draws the borrowed environment and exact character exports with nearest sampling. RUN_CHECKS is intentionally absent from this user project; a separate recorded copy ran mouse/key and render checks.
