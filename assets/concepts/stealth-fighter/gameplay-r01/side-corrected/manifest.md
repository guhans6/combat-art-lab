# Side correction — raw generated concept

Date: 2026-11-01. One built-in imagegen edit, transparent_background=true. Raw output copied unchanged from `/Users/guhan/.codex/generated_images/01a197f5-157d-70e2-b517-4fd8bf32366f/exec-0c317d17-79aa-4fd5-a670-0e0f4e2c2e36.png` to `cutout.png`.

Inputs in order:
1. Edit target: `assets/concepts/stealth-fighter/gameplay-r01/views/side.png`, SHA-256 `4a4ab8abf0cdd252cb7923cdd0e034e274a508969b422bed1cecf648d5346368`.
2. Identity/style reference: `assets/concepts/stealth-fighter/atmosphere-r01/A/simplified-01.png`, SHA-256 `e1dcf18e72ce22b8b6c6031d0f00da91259dcbf4c2bfbb0e0c12c8d1c56b6e1e`.

Exact prompt:

> Use case: precise-object-edit / background-extraction. Asset: single full-body gameplay character concept cutout. Image 1 is the edit target: retain its character identity, costume and idle stance while correcting the camera angle and removing background atmosphere. Image 2 is the identity and style reference: preserve the same lean young adult brown-skinned male, long dark half-tied hair, light stubble, indigo split-hem shirt, charcoal light shoulder armor, steel forearm guard, brown waist wrap and buckle, and compact sheathed one-hand sword. Show him facing RIGHT in a TRUE 90-degree side profile at eye level, as in a 2D side-scrolling game: head, torso, shoulders, hips, legs and boots all aligned in profile; no front-facing chest or three-quarter torso. The near arm overlays the torso naturally. No visible top planes of shoes or shoulders, no overhead view. Full head, hair, sword and both complete boots visible with breathing room on every edge. Quiet deliberate pixel-style illustration with flat color clusters and broad shadows, preserving the character's proportions and details; no realistic, anime or chibi treatment and no invented outfit details. Keep neutral body colors legible, with modest light only on the figure. Genuine transparent background with alpha zero immediately outside the character silhouette; NO halo, aura, vignette, smoke, ground, contact shadow or backdrop. One character only, no text.

Output: `cutout.png`, 1024×1536 RGBA, SHA-256 `20906495d146e9d6aea48962fa652d250aeddc3a5700e28a358c8ed48e5cb5c4`.

Alpha inspection via ffmpeg decoded RGBA: four corner alpha values 0; 1,231,649 zero-alpha pixels, 341,215 partial-alpha pixels, zero fully opaque pixels. Bounding box of alpha >0: (33,46)–(987,1493); alpha >1: (326,46)–(695,1486); alpha >128: (330,49)–(692,1484), inclusive coordinates. This reveals faint alpha far beyond the figure, and visual inspection shows a glow. It fails the clean-cutout requirement. The broad visible chest and boot top planes still read three-quarter rather than strict side profile. Complete head and boots are present and identity cues broadly survive. This is a concept only; no native sprite, animation, Godot playback, or user visual approval is established. No retry was made.
