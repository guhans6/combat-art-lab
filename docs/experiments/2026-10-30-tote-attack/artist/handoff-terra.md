# Terra artist handoff — tote attack

The native candidate is `terra/source/tote-attack.aseprite` with 13 frames, a 60 ms initial ready pose (to avoid adding a 220 ms input delay), and a 220 ms final rest pose. It has five normal, opaque flat layers: the source-derived composite plus named neck/collar, arms/grip, handle, and tote-inertia construction layers. Frame 9 contains the localized neck/collar repair; its collar overlaps the skin column rather than leaving the rejected open throat/olive shelf.

Dedicated Aseprite MCP saved, closed, freshly reopened, and re-exported the native asset. The untrimmed horizontal fresh-export sheet is `terra/checkpoints/reopen-sheet.png`; frame exports are in `terra/frames/`.

Important limit: this remains an exploratory converted-seed candidate, not a user-approved animation. The main-six source crop itself visibly truncates the far-right tote mass in committed frames, and frames 9/10 retain source-island contamination. I shifted source cels enough to keep pixels inside the 256×192 canvas for mechanical inspection, but this does **not** repair those cropped/source-art defects. Do not represent this as a completed art repair or visual approval. A follow-up must rebuild those keys from wider same-scale source crops/components and redraw the arrest/recovery arm/handle/bag chain substantially before visual acceptance.

Parent owns independent metadata validation, review packaging, runtime playback, and user review.
