#!/usr/bin/env python3
"""Verify the mouth-only revision and render an evidence sheet."""
from __future__ import annotations

import hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "inputs/baseline-denim-cleaned.png"
CANDIDATE = ROOT / "outputs/candidate-mouth.png"
REOPENED = ROOT / "outputs/candidate-mouth-reopened.png"
SOURCE = ROOT / "inputs/generated-clean-source.png"
OUT = ROOT / "evidence"
# This rectangle was declared before the real smile stroke. Every other pixel,
# including eyes, brows, nose, jaw, hair, all body/denim, and alpha, is locked.
ALLOWED = {(68, 27), (69, 28), (70, 28)}

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def checker(size):
    im=Image.new("RGBA",size,"#1d222b"); d=ImageDraw.Draw(im)
    for y in range(0,size[1],8):
        for x in range(0,size[0],8):
            if (x//8+y//8)%2: d.rectangle((x,y,x+7,y+7),fill="#323b49")
    return im

def main():
    base=Image.open(BASELINE).convert("RGBA"); cand=Image.open(CANDIDATE).convert("RGBA"); reopened=Image.open(REOPENED).convert("RGBA")
    if base.size != (128,192) or cand.size != base.size: raise SystemExit("unexpected canvas")
    if cand.tobytes()!=reopened.tobytes(): raise SystemExit("reopened export differs")
    changed=[]; alpha=[]; outside=[]
    for y in range(192):
        for x in range(128):
            old,new=base.getpixel((x,y)),cand.getpixel((x,y))
            if old!=new:
                changed.append({"x":x,"y":y,"old":"#%02x%02x%02x%02x"%old,"new":"#%02x%02x%02x%02x"%new})
                if old[3]!=new[3]: alpha.append((x,y))
                if (x,y) not in ALLOWED: outside.append((x,y))
    if not changed or alpha or outside or { (p["x"],p["y"]) for p in changed } != ALLOWED:
        raise SystemExit(json.dumps({"changed":changed,"alpha":alpha,"outside":outside}))
    OUT.mkdir(exist_ok=True)
    report={"baseline_sha256":sha(BASELINE),"candidate_sha256":sha(CANDIDATE),"reopened_sha256":sha(REOPENED),"source_sha256":sha(SOURCE),"dimensions":[128,192],"candidate_equals_reopened_rgba":True,"changed_pixels":len(changed),"alpha_changes":0,"protected_changes":0,"mouth_mask":{"x":68,"y":26,"width":4,"height":4},"actual_changes":changed}
    (OUT/"checks.json").write_text(json.dumps(report,indent=2)+"\n")
    (OUT/"change-ledger.json").write_text(json.dumps({"allowed_mouth_mask":"x=68..71, y=26..29","actual_changes":changed,"all_other_pixels_locked":True,"alpha_locked":True},indent=2)+"\n")
    c=Image.new("RGBA",(1440,1040),"#161b23"); d=ImageDraw.Draw(c)
    d.text((20,16),"Mouth readability pass — generated cutout conversion",fill="white")
    d.text((20,38),"Only three face pixels changed inside the declared mouth mask; eyes, brows, nose, jaw, hair, body, denim and alpha are locked.",fill="#cbd5e1")
    for px,img,title in [(20,base,"Baseline — actual 1x"),(180,cand,"Smile candidate — actual 1x")]:
        p=checker(img.size);p.alpha_composite(img);c.alpha_composite(p,(px,80));d.text((px,285),title,fill="white")
    for px,img,title in [(20,base,"Baseline — 4x nearest"),(560,cand,"Smile candidate — 4x nearest")]:
        p=checker((512,768));p.alpha_composite(img.resize((512,768),Image.Resampling.NEAREST));c.alpha_composite(p,(px,420));d.text((px,1210-190),title,fill="white")
    # Tight face comparison at 24×, with changed cells marked separately.
    for px,img,title in [(1080,base,"Face before — 24x"),(1080,cand,"Face after — 24x")]:
        crop=img.crop((60,18,80,38)).resize((240,240),Image.Resampling.NEAREST);p=checker(crop.size);p.alpha_composite(crop);c.alpha_composite(p,(px,80 if img is base else 360));d.text((px,60 if img is base else 340),title,fill="white")
    mask=checker((240,240)); md=ImageDraw.Draw(mask)
    for x,y in ALLOWED: md.rectangle(((x-60)*12,(y-18)*12,(x-60)*12+11,(y-18)*12+11),fill="#ff4d6d")
    c.alpha_composite(mask,(1080,640));d.text((1080,620),"Three changed pixels — 12x",fill="white")
    c.save(OUT/"before-after-mouth.png")
if __name__=="__main__": main()
