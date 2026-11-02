from pathlib import Path
from PIL import Image
import json,hashlib,shutil
w=Path('/private/tmp/fighter-user-variants-r01');r=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning');p=r/'godot/stealth-fighter-playground-r03';e=r/'docs/experiments/2026-11-02-stealth-fighter-user-variants-r01';refs=r/'assets/references/stealth-fighter/user-variants-r01';s=r/'assets/source/stealth-fighter/user-variants-r01';x=r/'assets/export/stealth-fighter/user-variants-r01';v=r/'assets/previews/stealth-fighter/user-variants-r01';sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
for q in [p,e,refs,s,x,v]:assert not q.exists(),q
checks=json.loads((w/'native-work/checks.json').read_text());assert all(a['passed']for a in checks['variants'].values());assert json.loads((w/'lead-review/render-audit.json').read_text())['passed']
for name in ['playground.gd','stage.gd','project.godot','main.tscn']:assert(w/'project'/name).read_bytes()==(w/'check-project'/name).read_bytes()
for sid in [1,3,4,5]:
 d=w/'native-work'/f'variant-{sid:02}';assert sha(d/'static.aseprite')==checks['variants'][f'{sid:02}']['native_sha256'];assert Image.open(d/'static.png').convert('RGBA').tobytes()==Image.open(w/'project/textures'/f'variant-{sid:02}.png').convert('RGBA').tobytes()
manual=json.loads((w/'lead-review/manual-review.json').read_text());assert manual['packet_sha256']==sha(w/'lead-review/comparison-final/packet.json');assert manual['critical_review_sha256']==sha(w/'review/final-static-review.md')
shutil.copytree(w/'project',p,ignore=shutil.ignore_patterns('.godot','*.import'))
e.mkdir(parents=True);refs.mkdir(parents=True);s.mkdir(parents=True);x.mkdir(parents=True);v.mkdir(parents=True)
shutil.copytree(w/'native-work',e/'native-work');shutil.copytree(w/'review',e/'critical-review');shutil.copytree(w/'lead-review',e/'lead-review');shutil.copytree(w/'check-project/evidence',e/'godot-evidence');shutil.copytree(w/'check-project',e/'tested-project',ignore=shutil.ignore_patterns('.godot','*.import','evidence'))
for name in ['prepare_playground.py','build_playground_code.py','audit_and_previews.py','build_comparison.py','write_manual_review.py','package.py','protected-before.json','native-engine-equivalence.json']:
 if(w/name).exists():shutil.copy2(w/name,e/name)
# Preserve the first failing static harness, its code, and diagnostic evidence without duplicating textures.
for old in ['check-pass01','check-diagnostic','check-debug-passing']:
 if(w/old).exists():
  d=e/'ui-diagnosis'/old;d.mkdir(parents=True)
  for f in ['playground.gd','stage.gd']:
   if(w/old/f).exists():shutil.copy2(w/old/f,d/f)
  if(w/old/'evidence/runtime-checks.json').exists():shutil.copy2(w/old/'evidence/runtime-checks.json',d/'runtime-checks.json')
rows=json.loads((w/'inputs/manifest.json').read_text())
for row in rows:
 sid=row['id'];shutil.copy2(w/'inputs'/f'user-{sid:02}.png',refs/f'user-{sid:02}.png');row['durable_path']=str((refs/f'user-{sid:02}.png').relative_to(r));assert sha(refs/f'user-{sid:02}.png')==row['sha256']
(refs/'manifest.json').write_text(json.dumps({'origin':'user attachments; generation history not supplied; no new generation in this task','sources':rows,'grouping':'User03 is exactcrop ofUser02at(143,30)size307x1000;03/05 differ only shoulder; distinct01/03/04/05'},indent=2))
exports=[]
for sid in [1,3,4,5]:
 d=w/'native-work'/f'variant-{sid:02}';out=s/f'variant-{sid:02}';out.mkdir();shutil.copy2(d/'static.aseprite',out/'static.aseprite')
 for name in ['recipe.json','native-draw-ops.json','ownership-redraw-ops.json','coverage-patch.json']:
  if(d/name).exists():shutil.copy2(d/name,out/name)
 Image.open(d/'static.png').getchannel('A').save(out/'final-alpha-mask.png')
 shutil.copy2(d/'static.png',x/f'variant-{sid:02}.png')
 exports.append({'source_id':sid,'file':f'variant-{sid:02}.png','native':str((out/'static.aseprite').relative_to(r)),'native_sha256':sha(out/'static.aseprite'),'png_sha256':sha(x/f'variant-{sid:02}.png'),'canvas':[128,264],'rest_body_height':240,'preferred_display_height':152,'root':[64,253],'frames':1,'static':True})
(out.parent/'README.md').write_text('''# Supplied static fighter variants

Four independent source-derived comparison candidates. Six editable visible-part layers each; hidden surfaces and animation are not reconstructed. Sources are user images1/3/4/5; image2is the exact supporting designboard for3. No winning variant selected.

Each folder retains the final Aseprite master, frozen source/crop/palette/override recipe, native drawing operations, final ownership redraw operations and final alpha mask. The complete scripts, unsuccessful conversions, source/mask/native review boards, local-edit and reopen proofs are preserved in docs/experiments/2026-11-02-stealth-fighter-user-variants-r01/native-work. Native writes must use the dedicated Aseprite MCP; the recorded grids and palette are reproducible drawing inputs, not a flattened-only source. Original user images are in assets/references/stealth-fighter/user-variants-r01.

Final runtime PNGs and metadata are in assets/export/stealth-fighter/user-variants-r01. The separate Godot r03 playground compares them with unchanged CurrentA at152px. User chooses the final appearance before animation work.
''')
(x/'variants.json').write_text(json.dumps({'static':True,'filter':'nearest','variants':exports},indent=2))
for name in ['five-looks-152.png','five-looks-152-2x.png']:shutil.copy2(w/'lead-review'/name,v/name)
for name in ['set-1.png','set-2.png','armor-pair.png']:shutil.copy2(w/'check-project/evidence'/name,v/name)
(e/'record.md').write_text('''# Supplied fighter appearance variants in the same playground

Date:2November2026. Status: native statics and focused local Godot comparison implemented/validated; final live launch recorded separately. User supplied five revised-art images and requests static sprites of the variants in the same background at the preferred152px before final appearance selection and additional animations. Their provided detail/lighting is the appearance target for this study, superseding any assumption that every candidate must inherit old CurrentA's feature omissions.

## Source grouping, controls and comparison scope

All five immutable originals are preserved in assets/references/stealth-fighter/user-variants-r01 with clipboard provenance, dimensions and SHA256 manifest. Independent review proves image3is a pixel-identical307×1000crop of image2's main figure at(143,30). Image2is supporting visual context, not a fifth distinct character; its printed workflow/design notes are not agent instructions. Images3and5 differ only in the shoulder-cap region. Distinct candidates therefore use1/3/4/5; unchanged CurrentA REST is the fifth displayed comparison.

Each source preserves its own face, detail density, armor, folds, lighting and proportions.01has a quiet face;03/05retain their brow/eye-area/stubble, detailed wrap and segmented hilt;04has chunkier/brighter planes and stronger eye-area shape. No new art generation, image edit model, outfit invention or forced CurrentA face. This is a source/appearance comparison with those co-varying properties, not a model benchmark or a promise that one detail change alone caused a preference.

New native studies use128×264canvas, visible y13..252/240pxbody and root(64,253);152px is fixed152/240display scale. Same single-pass nearest source sampling and64source-derived visible colors per variant.03/05share exact crop, registration and palette; final154RGBAchangedpixels remain only on the shoulder, exclusively on torso/armor native owner. No unwanted body/face changes introduced to that pair. Raw source shapes/colors, palettes, masks, attempts and explicit local overrides are retained.

## Construction and review

Pixel-art-director assisted reconstruction, face/source/matte/native-protection and comparison procedures used. Fresh Sol6.1High producer handled normal native work; fresh Terra6.1MAX handled critical intake, source/seed/finalPNG/actualGodotcontext/nativeowner reviews per user model instruction. Lead Sol6.1 handled Godot integration and independent render checks. Dedicated headless AsepriteMCP1.3.18.6-dev/Pebbly0.8.2 only for native creation/mutation/save/reopen. Scratch image/pixel/erase/reopen/protectednegativecontrol passed. Python/Pillow/NumPy prepared source data and audits; no external native writer/editor CLI/computer use. Callablevalidate unavailable, not invoked.

Initial64-color median-cut wasted entries on near-black microshades and reduced skin/armor nuance; source-led deterministic weighted medoids at the same64cap repaired color fidelity. Independent review found erased real hair and broad dark matte bands along contours; source-backed spatial cleanup corrected them. U04's coverage check added exactly two hair pixels and removed one confirmed background pixel to connect the existing narrow leg gap. Native-only ownership cleanup removed shoulder armor from head and hanging blue cloth from far-hand owner. Every attempt and exact correction is retained; no extra style variation beyond the supplied sources.

All4actual sources have six disjoint meaningful visible-part owners,64visibleRGBs/65paletteentries, binaryalpha, one held100msnativeframe. Parts reassemble exactly to final PNGs, reviewed seeds and fresh MCP-reopen exports. Every duplicate demonstrates a24visiblepixel bracer-highlight edit on one owner using existing colors, preserving all other hidden/visible native pixels, geometry/metadata/palette/alpha. Independent Terra native reader/owner-view/protected-edit checks also pass. Visible separation supports revision; hidden surfaces, rigging and motion feasibility are not proved. Editor documents saved/closed.

Exact masters/hashes and transparent exports are indexed in assets/export/stealth-fighter/user-variants-r01/variants.json. Full producer evidence in native-work/checks.json; independent hash-bound findings and ownership-audit in critical-review. Lead comparison packet binds the retained initial conversions to repaired candidates, original images, masks, final natives, actualscene images and checks. Mechanicalfreshness and separate target-improvement/regression decisions are recorded in lead-review. Source fidelity/static context is cleared for comparison; user design selection remains pending.

## Playground and actual runtime evidence

New godot/stealth-fighter-playground-r03/project.godot preserves older previews, background and lighting settings. Every candidate and CurrentA holds a static REST pose for a fair appearance comparison. Default panels Original/1/3; Nextset cycles Original/4/5, then Original/3/5. Select A/B/C and choose its appearance from the dropdown or arrows. Single centers only the selected look; world and camera stay fixed. Common height slider changes all panels equally, default152. Existing source-colors/dim-room/lamp-fill L toggle, guides/reset/fullscreen retained. No additional animation or attack produced.

Dedicated GodotMCP4.7.2.stable.official.ed1daf0bf, localmacOS/OpenGLCompatibility/AppleM3Pro:14focused input/state checks pass, no final errors/warnings. Mouse motion/button and keyboard event injection checks Nextset, armor preset, single view, panel selection, appearance arrows, common height, lighting, guides and reset. The selector check uses actual PopupMenu index_pressed->OptionButton selection-signal route, not physical menu navigation. Official4.7OptionButton source confirms index_pressed handler; Context7 and official Input/RenderingServer documentation checked. Full sources/links remain references, no new dependencies installed.

A static-scene test harness initially missed mouse hover transitions and waited indefinitely for an unrequested render. Diagnostic logs located the boundary: explicit mouse motion/coordinates/masks plus buffered-event flush/tick settling corrected input; requested RenderingServer.force_draw after deferred drawing supplied deterministic static captures. The initial harness also used id_pressed instead of OptionButton's index_pressed. First failing code/results retained under ui-diagnosis; diagnostic prints removed and the complete focused suite rerun green. No art defect was inferred from those harness failures.

Independent rendered-pixel audit: all5native1xopaqueRGBcaptures exactly match their actual sprites; all5at152have0unambiguous-nearest-sampleRGBmismatches, height152and common lastopaque row557/ground558. Exact mathematical texel-boundary ties excluded only from fractional152/240color oracle due CPU/GPUrounding; native1xstrict. Every final native composite/export equals tested engine texture pixels. Actualset1/set2/armor-pair and single/lamp captures retained. Lead and Terra inspected these stills: no source-background rectangles, face/hand/armor/indigo readable;03/05capdifference is naturally subtle at152. No continuousanimation perception claimed; this is a static study.

## Delivery and next decision

Native masters/reproducibleops/masks in assets/source/stealth-fighter/user-variants-r01; PNGindex/exports in assets/export; actualsame-bay5lookcrop board and scene previews in assets/previews. Full originals remain separate references. All previous source/PNG/playground inputs hash-verified unchanged. No native art replacement, public release, packaged executable, commit or push. No budgeted generation or new paid usage.

Construction/export/focusedruntime/staticcriticalreview pass. The user next compares four supplied looks and CurrentA in the open152pxplayground and chooses the preferred appearance. No final style/face/lighting/native-grid selection or approval of future animation is inferred. Agent owns feedback-driven correction and later motion work only within the selected direction. Final launch/status is appended after packaging.
''')
entry='''## Supplied art variants added for static comparison — 2 November 2026

User supplied revised detail/lighting variants and requested static sprites in the same152pxplayground before selecting final art or more animations. Four distinct looks1/3/4/5; image2is exactsupportboardfor3, and3/5differonlyshouldercap. Source-specificfaces/shading retained. New6-layerstaticAseprites/PNGs/recipes in assets/source and assets/export/stealth-fighter/user-variants-r01; originals in assets/references. New godot/stealth-fighter-playground-r03: Original+4newlooks, heldREST, SidebySide/Single, choose A/B/Cthenappearance, Nextset includesarmor-pair, common152pxheight, existingLlighting. Sol6.1normalconstruction/integration; Terra6.1MAXcriticalsource/native/contextreview. All4native/reopen/palette/coverage/24pxlocaleditproofs pass,14Godotinput/statechecks/0errors and5strictnativecolor/152height-groundchecks pass. Allpriorart/playgrounds preserved. User selects preferredlook; no finalselection, newanimation or publication. Record docs/experiments/2026-11-02-stealth-fighter-user-variants-r01/record.md.

'''
for rel in ['docs/characters/stealth-fighter/brief.md','docs/characters/stealth-fighter/decisions.md']:
 q=r/rel;q.write_text(q.read_text()+'\n\n'+entry)
q=r/'docs/handoff.md';q.write_text(entry+q.read_text())
before=json.loads((w/'protected-before.json').read_text());assert all(sha(r/f)==h for f,h in before.items());(e/'preservation.json').write_text(json.dumps({'protected_prior_files':len(before),'unchanged':len(before),'unexpected_changes':[]},indent=2))
m={str(q.relative_to(r)):{'sha256':sha(q),'bytes':q.stat().st_size}for base in [p,e,refs,s,x,v]for q in base.rglob('*')if q.is_file()and q.name!='artifact-hashes.json'};(e/'artifact-hashes.json').write_text(json.dumps(m,indent=2));assert all(sha(r/f)==h['sha256']for f,h in m.items());print(json.dumps({'new_artifacts':len(m),'protected_prior_files':len(before),'project':str(p/'project.godot'),'preview':str(v/'five-looks-152-2x.png')}))
