from pathlib import Path
import hashlib,json,shutil
w=Path('/private/tmp/fighter-playground-r01');r=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning');p=r/'godot/stealth-fighter-playground-r01';e=r/'docs/experiments/2026-11-02-stealth-fighter-playground-r01';sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
assert not p.exists()and not e.exists()
audit=json.loads((w/'check-project/evidence/render-audit.json').read_text());assert audit['passed']
for name in ['playground.gd','stage.gd','project.godot','main.tscn']:
 assert (w/'project'/name).read_bytes()==(w/'check-project'/name).read_bytes()
shutil.copytree(w/'project',p)
(p/'.gitignore').write_text('.godot/\n*.import\n')
e.mkdir(parents=True);shutil.copytree(w/'check-project/evidence',e/'evidence');shutil.copytree(w/'check-project',e/'tested-project',ignore=shutil.ignore_patterns('.godot','evidence','*.import'))
shutil.copy2(w/'audit.py',e/'audit.py');shutil.copy2(w/'package.py',e/'package.py');shutil.copy2(w/'build.py',e/'build.py');shutil.copy2(w/'protected-before.json',e/'protected-before.json')
shutil.copy2(w/'church-page.html',e/'asset-page.html')
provenance={'retrieved':'2026-11-02','creator':'Luis Zuno / ansimuz','source':'https://opengameart.org/content/gothicvania-church-pack','download':'https://opengameart.org/sites/default/files/gothicvania%20church%20files.zip','archive_sha256':sha(w/'church.zip'),'license_file_sha256':sha(p/'ART-LICENSE.txt'),'used':{n:sha(p/'textures'/n)for n in ['backgrounds.png','tileset.png']},'excluded':'audio, characters, game code, PSDs','generation_calls':0}
(e/'provenance.json').write_text(json.dumps(provenance,indent=2))
(e/'record.md').write_text('''# Main character scale playground — r01

Date:2November2026. Status: implemented and locally validated; final live launch recorded separately. User says the main idle looks good and asks for an actual themed playground with different sizes, side-by-side or single views. This accepts main idle-r02 as the motion baseline for this placement study; production grid, final display size and world art remain open.

## Scope and baseline

Approved main native assets/source/stealth-fighter/idle-r02/idle.aseprite, SHA256 f4cb8fff0a460cde6845fb15bc0c5e3271259d9d38d5f3efa051e4970b2e6127. Exact4PNG exports,128×264canvas/240pxrestbody, [700,260,500,340]ms timeline, shared1800ms phase. No character edit, new pose, recolor, generation or native-source mutation. Existing studies, main sources and prior environments preserved.

New project godot/stealth-fighter-playground-r01/project.godot. Temporary theme: The Quiet Keep, a ruined stone cloister using Luis Zuno's public-domain GothicVania Church artwork. Verified artist's primary OpenGameArt listing and archive public-license.txt; original license, download URL/hash and exact used texture hashes retained. Only unchanged background/tileset textures used; runtime crops repeat the same stone window bay and floor blocks at integer2×. No audio, enemy/player sprites or pack game code. Primary URLs in CREDITS.md; retrieval2026-11-02. Existing modern street assets were available but did not fit the current character setting. Cold Corridors investigated but not used. No new purchases or services.

## Playground behavior

One1200×480world inside1280×800viewport. Three actors default96/128/160scene pixels tall, synchronized on one clock, identical repeated architecture and ground. Side-by-side displays all three; Single hides other actors and centers the selected one without changing the world, camera or character scale. A/B/C selection and a64–240height slider allow changing one candidate while retaining the others. Pause/play, frame step,0.5×/1×/2×speed, measurement guides and reset. Mouse controls plus M/1/2/3/Space/comma/period/R/G/F11 shortcuts. Resizing/fullscreen uniformly changes display magnification, not the in-world ratios. No walking/combat/playable-game claim.

## Focused proof

Current Godot4.7 documentation checked through Context7: draw_texture_rect_region, SubViewport sizing (considered, not used), input event injection and RenderingServer.frame_post_draw screenshot capture. Primary documentation sources: github.com/godotengine/godot-docs/blob/4.7/classes/class_canvasitem.rst ; tutorials/inputs/inputevent.rst ; classes/class_viewport.rst. Actual runtime through dedicated GodotMCP only, Godot4.7.2.stable.official.ed1daf0bf, localmacOS/OpenGLCompatibility/AppleM3Pro. No direct editor CLI or computer use.

Separate test project ran15 focused checks through actual injected mouse/keyboard events and state observations: >=3authored loops, Single button, A selection, slider change, keyboard B, pause hold, next/previous frame, resume and time advance,2×speed, guides, keyboard comparison and both reset paths. All pass. Initial run had two local parameter-shadowing warnings; renamed those parameters and reran the same focused suite, final errors/warnings[]. Test instance stopped. Main project has no RUN_CHECKS marker, so no automatic test manipulations occur for the user.

Independent pixel audit of actual Godot captures: all4native-scale source poses have0opaqueRGB mismatches. At all3default scales, independently calculated nearest samples match exact source colors (1584/2825/4419opaque pixels tested), drawn heights exactly96/128/160, common bottom opaque row557/groundline558. No camera change between modes. Original artwork has no tint/filter blur. Source PNGs equal approved exports. Compare and Single screenshots visually inspected: joint/feet registration retained, labels/controls clear and no clipping; this is still pose/UI evidence, not continuous model temporal perception or user approval of background/scale.

## Completion and handoff

Implementation and focused local input/render checks pass. Native source unchanged; public release, export to a packaged executable, combat integration and final art/size selection are not performed. The agent launches the saved Godot project for direct user interaction and leaves that final instance running. Next owner: user compares sizes and gives a preference; agent owns any preview corrections. The128px middle option is a comparison baseline, not a chosen production size. Existing source/PNG protection hashes and delivered file manifest accompany this record.
''')
entry='''## Main idle accepted; scale playground — 2 November 2026

User says main idle-r02 looks good and requests a themed interactive size comparison. Exact approved main art preserved. New godot/stealth-fighter-playground-r01/project.godot: The Quiet Keep, borrowed public-domain GothicVania stone arches/floor by Luis Zuno; no new art generation. Default96/128/160px characters share one fixed world/camera and animation phase; Side by side / Single buttons, A/B/C selection,64–240height slider, pause/step/speed/guides/reset and keyboard controls. Actual Godot4.7.2 separate test:15mouse/key/state checks pass, zero final warnings/errors, all4native-scale source captures exact, all3projected heights and sampled colors exact, feet share bottom row557. Main sprite/native untouched. Final project launch/status recorded in experiment. User next compares sizes/theme; neither display size nor world art selected. No commit/publish. Record docs/experiments/2026-11-02-stealth-fighter-playground-r01/record.md.

'''
for rel in ['docs/characters/stealth-fighter/brief.md','docs/characters/stealth-fighter/decisions.md']:
 q=r/rel;q.write_text(q.read_text()+'\n\n'+entry)
q=r/'docs/handoff.md';q.write_text(entry+q.read_text())
before=json.loads((w/'protected-before.json').read_text());assert all(sha(r/f)==h for f,h in before.items())
(e/'preservation.json').write_text(json.dumps({'prior_fighter_files':len(before),'unchanged':len(before),'unexpected_changes':[]},indent=2))
manifest={str(q.relative_to(r)):{'sha256':sha(q),'bytes':q.stat().st_size}for b in [p,e]for q in b.rglob('*')if q.is_file()and q.name!='artifact-hashes.json'}
(e/'artifact-hashes.json').write_text(json.dumps(manifest,indent=2));assert all(sha(r/f)==v['sha256']for f,v in manifest.items());print(json.dumps({'project':str(p/'project.godot'),'artifacts_verified':len(manifest),'protected_prior_fighter_files':len(before)}))
