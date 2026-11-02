from pathlib import Path
import json,hashlib,shutil
from PIL import Image
r=Path('/Users/guhan/Guhan/Projects/combat-art-lab-learning');w=Path('/private/tmp/stealth-fighter-idle-r02');lead=Path('/private/tmp/fighter-r02-lead');eng=Path('/private/tmp/fighter-r02-godot-preview');e=r/'docs/experiments/2026-11-02-stealth-fighter-idle-r02';s=r/'assets/source/stealth-fighter/idle-r02';x=r/'assets/export/stealth-fighter/idle-r02';p=r/'assets/previews/stealth-fighter/idle-r02'
sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
assert json.loads((w/'delivery/checks.json').read_text())['passed']
assert json.loads((lead/'independent-native-checks.json').read_text())['passed']
assert json.loads((eng/'evidence/pixel-checks.json').read_text())['passed']
assert sha(w/'delivery/idle-r02.aseprite')=='f4cb8fff0a460cde6845fb15bc0c5e3271259d9d38d5f3efa051e4970b2e6127'
# Preserve exact tested engine textures and prove equivalence to final native exports.
equiv=[]
for i in range(4):
 a=Image.open(w/'delivery'/f'idle-{i}.png').convert('RGBA');b=Image.open(eng/'textures'/f'idle-{i}.png').convert('RGBA');assert a.tobytes()==b.tobytes();equiv.append({'frame':i,'final_native_export_equal_tested_engine_texture':True})
(eng/'evidence/final-export-equivalence.json').write_text(json.dumps(equiv,indent=2))
for q in [e,s,x,p]:q.mkdir(parents=True,exist_ok=False)
shutil.copytree(w,e/'native-work');shutil.copytree(lead,e/'lead-review');shutil.copytree(eng,e/'godot-preview',ignore=shutil.ignore_patterns('.godot'))
shutil.copy2(w/'delivery/idle-r02.aseprite',s/'idle.aseprite');shutil.copy2(w/'observations.md',s/'construction-notes.md');shutil.copy2(w/'final-key-ops.json',s/'key-ops.json');shutil.copy2(w/'editable-upper-frozen.png',s/'editable-mask.png');(x/'frames').mkdir()
for i in range(4):shutil.copy2(w/'delivery'/f'idle-{i}.png',x/'frames'/f'idle-{i:02}.png')
for f in ['idle-sheet.png','idle-sheet.json','timings.json']:shutil.copy2(w/'delivery'/f,x/f)
shutil.copy2(lead/'idle-exact-native.gif',x/'idle.gif')
for f in ['idle-2x.gif','idle-environment-2x.gif','idle-gameplay-128px-2x.gif']:shutil.copy2(lead/f,p/f)
shutil.copy2(lead/'cycle-2x.png',p/'contact-2x.png');shutil.copy2(eng/'evidence/runtime-frame-02.png',p/'godot-context.png')
record=(lead/'record-draft.md').read_text()
record+='''

## Constructed result and review

Native: assets/source/stealth-fighter/idle-r02/idle.aseprite. SHA256 f4cb8fff0a460cde6845fb15bc0c5e3271259d9d38d5f3efa051e4970b2e6127. Four timeline entries, three drawings, [700,260,500,340] milliseconds, total1800ms. Nine semantic layers and36cels. Shoulder apex approximately up4/back2 native pixels; rigid head, face, neck and long hair up2/back2; near elbow, guard and hand up2/back2. Sleeve joins the more mobile shoulder to the quieter distal arm. Torso contours lean toward an unchanged waist, retaining source row widths and material sequences. This transfers motion relationships and screen-space amplitude; it does not copy sample appearance or deform the rigid guard like a cloth forearm.

The first key pass exposed inner-arm/body/hip and collar alpha seams. One named attachment repair supplies source-colored backing only at listed newly exposed sites; all attempts and point inventories are retained. Lead inspection of actual native owner/hide images then caught indigo split-hem cloth mixed into the old far-hand owner. The original Current A crop confirms this is a hanging coat panel in front of the partly occluded hand.89 indigo pixels plus one disconnected trim pixel were reassigned to far-hem-fixed, above the44 connected warm/dark arm pixels. REST composite stayed exact. The panel is fixed; the moving hand can be occluded by it. Hidden far elbow remains inferred from this single view, not proven anatomy.

Lead received Current A original and source/native comparison, actual initial and repaired key images at1x/3x, magenta upper-body contrast at5x, marked apex anatomy, head/near sleeve/rigid guard/far hand owner-isolated and hidden views. Final four-entry contact at2x covers rest, both neighbors and transition-to-rest return. Proportions, attachments and still continuity support continuation after correction: collar meets the neck beneath rigid hair; shoulder overlaps upper sleeve, sleeve meets exposed elbow and guard; wrist and hand retain their rigid source shape; waist, sword, legs and feet stay quiet. No double skin branches or remaining open attachment seams observed. Material review retains broad indigo/charcoal/armor value roles, understated face and source rendering density. No new eye detail, relighting or chest-width puff. Temporal relaxed-versus-shrug reading remains for the user's GIF review.

Native and exported checks: source REST exact; all36nativecels match cleared keys; lower-body-fixed and sword-belt exact native source pixels; far hem exact every frame; composite rows153+ exact; head registered exact at authored offsets; palette exact source, alpha binary, zero enclosed holes; sheet and all4fresh MCP-reopen exports exact. Duplicate-only3pixel buckle edit proves useful native revision while preserving all other native pixels, metadata and palette. Lead independently repeated native/PNG/rest/protection/head/timing checks. Callable backend validate is unavailable; these are observed focused checks, not an invented validate result. Producer used GPT-6.1SolHigh; lead reviewed independently. All owned Aseprite documents closed.

Raw MCP GIF has known near-black palette encoding remaps on89/91/91/91 opaque pixels, despite correct timing/alpha. Raw file preserved for diagnosis. Delivered native-size and2xGIFs use an explicit palette from exact PNGs; decoded visibleRGBA and1800ms timing match. Preview packaging does not repaint the sprite. Full native work, scripts, operations, masks, failed passes, local edit and reopen evidence are archived here.

Final comparison packet SHA2561205a85feec3872b84a397365675c95c5a12a8dc8c4796b5cbc9e8921442c374. Fresh mechanical verification passed; separate lead target/regression decisions bound to this packet and final native are in lead-review/manual-review.json. Historical temporary paths in packets map to identical files archived in native-work.

## Runtime evidence

Dedicated GodotMCP ran /private/tmp/fighter-r02-godot-preview on Godot4.7.2.stable.official.ed1daf0bf, OpenGLCompatibility, AppleM3Pro. Target: local macOS preview,640x360viewport/1280x720window, nearest filtering. Native actor at(130,47), root/feet row300; second actor at fixed128/240scale for128pxRESTbody projection. Fixed doorway/floor/contact shadow provides environmental registration. A first scene run exposed a sample-sized contact shadow extending past the smaller fighter; background geometry alone was corrected and the scene rerun. Earlier captures are preserved in lead-review/runtime-before-shadow-alignment. Final run recorded all4frames and at least3loops,18loops by stop, finalErrors[]. Engine stopped. All four opaque native-actor RGB captures match exact exports. Final delivery PNG pixels equal the tested engine textures.

Environment GIFs reconstruct real Godot pose captures at authored durations; they are not continuous video. Native close scene crop[90,35,280,326] is shown at2x; gameplay crop[405,135,565,326] shows the128pxbody projection at2x. These are presentation scales, not production grid approval. The full real engine capture is godot-context.png. Lead inspected still frames, not continuously perceived playback; event timings and pixel checks establish runtime behavior, not naturalness or complete gameplay validation.

## Outcome and remaining boundary

Implementation, native editability, exports, protection and scoped runtime playback pass. The transferred Current A idle is a separate candidate for human review; the user's approval of sample motion does not preapprove this main-character application. Native grid/camera/face choices remain provisional as previously recorded. No attack, production replacement, public release, install, commit or push was performed. Next owner: user reviews the main-character motion; agent owns any feedback-driven native correction. Earlier concept, main idle-r01 and all disposable samples are retained unchanged.
'''
(e/'record.md').write_text(record)
entry='''## Accepted sample idle applied to Current A — 2 November 2026

User says r04 looks good and asks to apply it to the main character. Sample motion direction is accepted; sample design is not selected. New separate main native: assets/source/stealth-fighter/idle-r02/idle.aseprite, SHA256 f4cb8fff0a460cde6845fb15bc0c5e3271259d9d38d5f3efa051e4970b2e6127. Current A appearance and exact source REST retained. Nine layers, four entries/three drawings,1800ms. Connected shoulder/head/arm gesture scales to240pxmainbody; legs, waist, sword and far indigo panel fixed. Lead caught far coat pixels on movinghand owner and corrected ownership; native/PNG/reopen/protected/alpha/palette/localedit and independent checks pass. Godot4.7.2 all4captures/>=3loops/finalErrors[]; engine stopped/editor closed. Preview assets/previews/stealth-fighter/idle-r02/idle-gameplay-128px-2x.gif and idle-environment-2x.gif. Main transfer awaits user motion approval; still-only agent review, no continuous perception claim. Grid/camera provisional; no commit/publication. Record docs/experiments/2026-11-02-stealth-fighter-idle-r02/record.md. All earlier assets unchanged.

'''
for rel in ['docs/characters/stealth-fighter/brief.md','docs/characters/stealth-fighter/decisions.md']:
 q=r/rel;q.write_text(q.read_text()+'\n\n'+entry)
q=r/'docs/handoff.md';q.write_text(entry+q.read_text())
before=json.loads((lead/'preservation-before.json').read_text());changed=[rel for rel,h in before.items()if sha(r/rel)!=h];assert not changed,changed
(e/'preservation.json').write_text(json.dumps({'protected_prior_assets':len(before),'unchanged':len(before),'unexpected_changes':changed,'intended_document_updates':['docs/handoff.md','docs/characters/stealth-fighter/brief.md','docs/characters/stealth-fighter/decisions.md']},indent=2))
manifest={}
for base in [e,s,x,p]:
 for q in base.rglob('*'):
  if q.is_file()and q.name!='artifact-hashes.json':manifest[str(q.relative_to(r))]={'sha256':sha(q),'bytes':q.stat().st_size}
(e/'artifact-hashes.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'new_artifacts':len(manifest),'preserved_assets':len(before),'native':str(s/'idle.aseprite'),'preview':str(p/'idle-gameplay-128px-2x.gif')}))
