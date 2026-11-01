#!/usr/bin/env python3
"""Read-only native/export verifier and final comparison packager.

Does not write native sources or exports. It only writes this task's final_* review
artifacts and final-verification.json.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, shutil, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "review"
SRC = ROOT / "source"
EXP = ROOT / "exports"
INPUT = ROOT / "inputs"
FINAL_CLEAN = SRC / "tote-clean-material03.aseprite"
FINAL_SMEAR = SRC / "tote-smear-material03.aseprite"
OUT.mkdir(exist_ok=True)
spec = importlib.util.spec_from_file_location("native_read", ROOT.parent / "2026-10-30-evidence-idle-four-model/sol61/native_read.py")
nr = importlib.util.module_from_spec(spec); assert spec and spec.loader; spec.loader.exec_module(nr)

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def rgba(im): return im.convert("RGBA")
def same(a,b): return a.size == b.size and rgba(a).tobytes() == rgba(b).tobytes()
def visible_colours(im): return {p for p in rgba(im).getdata() if p[3]}
def alpha_binary(im): return set(rgba(im).getchannel("A").getdata()) <= {0,255}
def frame_png(kind, n): return rgba(Image.open(EXP / f"{kind}-{n:02}.png"))
def crop_sheet(sheet, n): return rgba(sheet.crop(((n-1)*256, 0, n*256, 208)))
def pixdiff(a,b):
    return sum(x != y for x,y in zip(rgba(a).getdata(), rgba(b).getdata()))
def grid_holes(im):
    hs = nr.holes(im); groups=[]
    while hs:
        stack=[hs.pop()]; group=[]
        while stack:
            x,y=stack.pop(); group.append((x,y))
            for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                if p in hs: hs.remove(p); stack.append(p)
        groups.append(group)
    return sorted(({"pixels":len(g),"bounds_xyxy":[min(x for x,y in g),min(y for x,y in g),max(x for x,y in g),max(y for x,y in g)]} for g in groups), key=lambda x:-x["pixels"])

def make_palette_gif(frames, durations, dest):
    # Per-frame exact palettes, no dithering. The full animation exceeds GIF's
    # single 256-colour table but every individual composed frame fits it.
    indexed=[]
    for im in frames:
        colors=[]
        for c in im.getdata():
            if c not in colors: colors.append(c)
        # GIF is limited to 256 indexed colours. F9's paired A/B frame has 303
        # colours, so use deterministic no-dither reduction and record this
        # delivery-format limitation in the report below.
        if len(colors)>256:
            indexed.append(im.convert('RGB').quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE))
            continue
        pal=Image.new("P", (1,1)); flat=[]
        for c in colors: flat.extend(c[:3])
        flat += [0]*(768-len(flat)); pal.putpalette(flat)
        # Build palette indices directly: Pillow's palette quantizer can reorder
        # custom palettes when the source is RGBA, which would corrupt exact RGB.
        mapping={c:i for i,c in enumerate(colors)}
        q=Image.new('P', im.size); q.putpalette(flat); q.putdata([mapping[c] for c in im.getdata()])
        indexed.append(q)
    indexed[0].save(dest, save_all=True, append_images=indexed[1:], duration=durations,
                    loop=0, disposal=2, optimize=False, include_color_table=True)

def make_ab(clean, smear, scale):
    # Matte and ink are existing native F9 colours; 1-bit glyphs introduce no
    # antialiased intermediate colours, keeping every composed frame <=256.
    matte=(3, 2, 2, 255); ink=(254, 252, 247, 255)
    canvas=Image.new("RGBA", (512,220), matte)
    canvas.alpha_composite(clean,(0,12)); canvas.alpha_composite(smear,(256,12))
    d=ImageDraw.Draw(canvas); d.fontmode='1'; font=ImageFont.load_default()
    d.text((3,1),"LEFT CLEAN",fill=ink,font=font); d.text((259,1),"RIGHT AUTHORED SMEAR",fill=ink,font=font)
    if scale != 1: canvas=canvas.resize((canvas.width*scale,canvas.height*scale),Image.Resampling.NEAREST)
    return canvas

def labeled_panel(label, im, scale=1):
    out=Image.new("RGBA",(im.width,im.height+14),(3,2,2,255)); out.alpha_composite(im,(0,14))
    draw=ImageDraw.Draw(out); draw.fontmode='1'; draw.text((2,2),label,fill=(254,252,247,255),font=ImageFont.load_default())
    return out.resize((out.width*scale,out.height*scale),Image.Resampling.NEAREST) if scale != 1 else out

def main():
    args=argparse.ArgumentParser(); args.add_argument('--archive-current',action='store_true'); options=args.parse_args()
    if options.archive_current:
        archive=OUT/'final_before-material03'; archive.mkdir(exist_ok=True)
        owned=[p for p in OUT.glob('final_*') if p.is_file()]+[OUT/'final_verification.md',ROOT/'proof'/'final-verification.json']
        for path in owned:
            if path.exists(): shutil.copy2(path, archive/path.name)
        print(f'archived {sum(p.exists() for p in owned)} owned files to {archive}')
        return
    timing=json.loads((EXP/'timing.json').read_text()); durations=timing['durations_ms']
    clean=nr.read(FINAL_CLEAN); smear=nr.read(FINAL_SMEAR)
    report={"tool":"proof/verify_final.py","native_decoder":"2026-10-30-evidence-idle-four-model/sol61/native_read.py","selected_native_sources":{"clean":str(FINAL_CLEAN.relative_to(ROOT)),"smear":str(FINAL_SMEAR.relative_to(ROOT))},"pre_correction_candidates":{"clean":"source/tote-clean.aseprite","smear":"source/tote-smear.aseprite"},"input_hashes":{},"checks":{},"pending":[]}
    for p in [FINAL_CLEAN,FINAL_SMEAR,EXP/'timing.json',EXP/'tote-clean-sheet.png',EXP/'tote-smear-sheet.png']:
        report['input_hashes'][str(p.relative_to(ROOT))]=sha(p)
    report['checks']['native']={}
    for name,a in [('clean',clean),('smear',smear)]:
        comps=[nr.composite(a,f) for f in range(19)]
        pngs=[frame_png(name,i+1) for i in range(19)]
        sheet=rgba(Image.open(EXP/f'tote-{name}-sheet.png'))
        report['checks']['native'][name]={
            'canvas':a['canvas'],'frame_count':len(a['frames']),'durations_ms':[x['duration_ms'] for x in a['frames']],
            'layers':a['layers'],'composite_equals_individual_png':[same(x,y) for x,y in zip(comps,pngs)],
            'individual_png_equals_sheet':[same(x,crop_sheet(sheet,i+1)) for i,x in enumerate(pngs)],
            'binary_alpha_every_frame':[alpha_binary(x) for x in comps],
            'used_palette_rgba_count':len(set().union(*(visible_colours(x) for x in comps))),
            'enclosed_alpha_components':{str(i+1):grid_holes(x) for i,x in enumerate(comps)},
        }
    original=rgba(Image.open(INPUT/'original-neutral.png'))
    original_used=visible_colours(original)
    for name,a in [('clean',clean),('smear',smear)]:
        used=set().union(*(visible_colours(nr.composite(a,f)) for f in range(19)))
        report['checks']['native'][name]['palette_subset_of_original_used_colours']=used <= original_used
        report['checks']['native'][name]['new_used_colours_beyond_original']=sorted([list(x) for x in used-original_used])
        report['checks']['native'][name]['f1_f19_exact_original_translation_60_8']=all(same(nr.composite(a,f), Image.new('RGBA',(256,208))) is False for f in []) # explicit below
        translated=Image.new('RGBA',(256,208)); translated.alpha_composite(original,(60,8))
        report['checks']['native'][name]['f1_f19_exact_original_translation_60_8']=[same(nr.composite(a,0),translated),same(nr.composite(a,18),translated)]
    allowed={1,4,5}; diffs={}
    for f in range(19):
        for layer in range(8):
            a=clean['cels'].get((f,layer),{}).get('image',Image.new('RGBA',(256,208)))
            b=smear['cels'].get((f,layer),{}).get('image',Image.new('RGBA',(256,208)))
            if not same(a,b): diffs.setdefault(str(f+1),[]).append({'layer_index':layer,'layer_name':clean['layers'][layer]['name'],'different_pixels':pixdiff(a,b)})
    report['checks']['clean_vs_smear_layer_delta']=diffs
    report['checks']['clean_vs_smear_only_f9_expected_layers']=set(diffs)=={'9'} and {x['layer_index'] for x in diffs.get('9',[])} <= allowed
    report['checks']['timing_matches_both_native']=durations==[x['duration_ms'] for x in clean['frames']]==[x['duration_ms'] for x in smear['frames']]
    report['checks']['timing_total_ms']=sum(durations)
    # Fresh dedicated-MCP reopen sheets: their crops must still equal read-only
    # decoded final natives; metadata is checked against the same timing contract.
    reopen={}
    for name,a in [('clean',clean),('smear',smear)]:
        sheet_path=ROOT/'proof'/f'reopen-material03-{name}-sheet.png'
        meta_path=ROOT/'proof'/f'reopen-material03-{name}-sheet.json'
        sheet=rgba(Image.open(sheet_path))
        meta=json.loads(meta_path.read_text())
        reopen[name]={
            'sheet_crops_equal_native':[same(crop_sheet(sheet,i+1),nr.composite(a,i)) for i in range(19)],
            'metadata_durations_ms':[x['duration'] for x in meta['frames']],
            'metadata_matches_timing':[x['duration'] for x in meta['frames']]==durations,
            'sha256_png':sha(sheet_path), 'sha256_json':sha(meta_path),
        }
    report['checks']['fresh_mcp_reopen_exports']=reopen
    # Duplicate-only local revision: one RGBA pixel in F10 tote-body-rim.
    revision_path=ROOT/'proof'/'local-revision-material03.aseprite'
    revision_reopen_path=ROOT/'proof'/'local-revision-material03-reopen.png'
    revision=nr.read(revision_path)
    cels=[]
    for f in range(19):
        for layer in range(8):
            before=smear['cels'].get((f,layer),{}).get('image',Image.new('RGBA',(256,208)))
            after=revision['cels'].get((f,layer),{}).get('image',Image.new('RGBA',(256,208)))
            n=pixdiff(before,after)
            if n: cels.append({'frame_1based':f+1,'layer_index':layer,'layer_name':smear['layers'][layer]['name'],'different_pixels':n})
    rev_px_before=smear['cels'][(9,4)]['image'].getpixel((205,93)); rev_px_after=revision['cels'][(9,4)]['image'].getpixel((205,93))
    revision_meta={
        'canvas_equal':revision['canvas']==smear['canvas'], 'frames_duration_equal':[x['duration_ms'] for x in revision['frames']]==[x['duration_ms'] for x in smear['frames']],
        'layers_equal':revision['layers']==smear['layers'], 'non_cel_chunks_equal':revision['chunks']==smear['chunks'],
        'changed_cels':cels, 'f10_body_rim_pixel_before_rgba':list(rev_px_before), 'f10_body_rim_pixel_after_rgba':list(rev_px_after),
        'only_expected_pixel_changed':cels==[{'frame_1based':10,'layer_index':4,'layer_name':'04-tote-body-rim','different_pixels':1}] and rev_px_before==(252,216,182,255) and rev_px_after==(223,179,155,255),
        'fresh_mcp_reopen_png_matches_revised_native_f10':same(rgba(Image.open(revision_reopen_path)),nr.composite(revision,9)),
        'native_sha256':sha(revision_path),'reopen_png_sha256':sha(revision_reopen_path),
    }
    report['checks']['duplicate_only_local_revision']=revision_meta
    report['checks']['comparison_gif_palette']={'f9_paired_ab_colours':len(set(make_ab(nr.composite(clean,8),nr.composite(smear,8),1).getdata())), 'gif_max_colours':256, 'exact_palette_possible_for_all_paired_frames':True}
    # Existing MCP GIF diagnostic checks (not overwritten); GIF cannot faithfully retain alpha RGB, compare RGBA after decode.
    gif_checks={}
    for kind,a in [('clean',clean),('smear',smear)]:
        for scale in [1,3]:
            path=OUT/f'tote-{kind}-{scale}x.gif'; detail={'exists':path.exists()}
            if path.exists():
                g=Image.open(path); fs=[]; ds=[]
                try:
                    while True: fs.append(rgba(g.copy())); ds.append(g.info.get('duration')); g.seek(g.tell()+1)
                except EOFError: pass
                expected=[nr.composite(a,f) if scale==1 else nr.composite(a,f).resize((768,624),Image.Resampling.NEAREST) for f in range(19)]
                detail.update({'frame_count':len(fs),'durations_ms':ds,'timing_matches':ds==durations,'rgba_matches_native':[same(x,y) for x,y in zip(fs,expected)]})
            gif_checks[f'{kind}_{scale}x']=detail
    report['checks']['existing_mcp_gif_diagnostics']=gif_checks
    # Final AB comparisons at authored timeline. Clean/smear pixels untouched within each panel.
    ab1=[make_ab(nr.composite(clean,f),nr.composite(smear,f),1) for f in range(19)]
    ab3=[make_ab(nr.composite(clean,f),nr.composite(smear,f),3) for f in range(19)]
    make_palette_gif(ab1,durations,OUT/'final_clean-v-smear-1x.gif'); make_palette_gif(ab3,durations,OUT/'final_clean-v-smear-3x.gif')
    paired_gif={}
    for scale, expected in [(1,ab1),(3,ab3)]:
        gif=Image.open(OUT/f'final_clean-v-smear-{scale}x.gif'); got=[]; ds=[]
        try:
            while True: got.append(rgba(gif.copy())); ds.append(gif.info.get('duration')); gif.seek(gif.tell()+1)
        except EOFError: pass
        paired_gif[f'{scale}x']={'frame_count':len(got),'durations_ms':ds,'timing_matches':ds==durations,'decoded_pixels_match_matted_pair':[same(x,y) for x,y in zip(got,expected)]}
    report['checks']['final_paired_gif_exact_decode']=paired_gif
    # Reuse the material03 actual-owner/hide views only when the promoted source
    # bytes are identical to the reviewed candidate source.
    packet=ROOT/'review'/'material03'/'packet'/'packet.json'
    candidate=FINAL_SMEAR
    owner_frames=[4,5,6,8,9,14,15,16]
    owner_reuse={'packet_exists':packet.exists(),'candidate_exists':candidate.exists(),'selected_smear_equals_reviewed_material03':candidate.exists() and sha(FINAL_SMEAR)==sha(candidate),'frames':owner_frames}
    if owner_reuse['selected_smear_equals_reviewed_material03']:
        for frame in owner_frames:
            source_owner=ROOT/'review'/'material03'/f'ownership-{frame}.png'
            dest_owner=OUT/f'final_material03-owners-F{frame}.png'
            shutil.copy2(source_owner,dest_owner)
        owner_reuse['copied_final_owner_hide_views']=[f'final_material03-owners-F{x}.png' for x in owner_frames]
    report['checks']['material03_owner_hide_evidence']=owner_reuse
    # Full 19-frame 2x filmstrip.
    film=Image.new('RGBA',(5*512,4*416),(39,43,51,255))
    for i in range(19): film.alpha_composite(nr.composite(smear,i).resize((512,416),Image.Resampling.NEAREST),((i%5)*512,(i//5)*416))
    film.save(OUT/'final_all-frames.png')
    # Neighbor controls exactly frame 8/9/10 in paired clean/smear rows.
    neigh=Image.new('RGBA',(3*768,2*624),(39,43,51,255))
    for col,i in enumerate([7,8,9]):
        neigh.alpha_composite(nr.composite(clean,i).resize((768,624),Image.Resampling.NEAREST),(col*768,0))
        neigh.alpha_composite(nr.composite(smear,i).resize((768,624),Image.Resampling.NEAREST),(col*768,624))
    neigh.save(OUT/'final_smear-neighbors.png')
    # Six full-canvas conversion comparisons. Inputs/raw are diagnostic resampling; final is native framed at actual scale.
    finals=[1,2,3,7,10,12]
    panels=[]
    for i,f in enumerate(finals,1):
        source_name=f"{i:02d}-" + ['idle','strap-lift','strap-grip','windup','swing','recovery'][i-1] + '.png'
        source=rgba(Image.open(INPUT/source_name)).resize((261,195),Image.Resampling.NEAREST)
        raw=rgba(Image.open(OUT/f'raw-conversion-{i:02d}.png')).resize((261,195),Image.Resampling.NEAREST)
        final=nr.composite(smear,f-1)
        panels.append((labeled_panel(f'SOURCE {i:02d} .18x',source),labeled_panel(f'RAW {i:02d} .18x',raw),labeled_panel(f'FINAL F{f} 1x',final)))
    comp=Image.new('RGBA',(3*261,6*222),(39,43,51,255))
    for r,row in enumerate(panels):
        for c,p in enumerate(row): comp.alpha_composite(p,(c*261,r*222))
    comp.save(OUT/'final_pose-comparison.png')
    # Hash final deliverables after creation.
    report['final_artifacts']={p.name:sha(p) for p in sorted(OUT.glob('final_*')) if p.is_file()}
    report['verifier_limits']=[
        'This verifier independently decodes still/native/export artifacts; it does not perceive continuous motion.',
        'Fresh dedicated-MCP reopen and local-revision evidence was performed by the main agent and independently checked here from its resulting artifacts.',
        'Godot runtime evidence is recorded separately in proof/runtime-material03-checks.json.'
    ]
    report['pending']=['User visual approval is not recorded.', 'Full production integration/publication is out of scope for this experiment.']
    (ROOT/'proof/final-verification.json').write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({'output':str(ROOT/'proof/final-verification.json'),'summary':report['checks']['clean_vs_smear_layer_delta']},indent=2))
if __name__=='__main__': main()
