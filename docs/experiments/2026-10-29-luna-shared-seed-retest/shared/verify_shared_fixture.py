#!/usr/bin/env python3
"""Read-only equality checks for the shared source-only seed fixture."""
from __future__ import annotations
import hashlib, importlib.util, json, struct, sys, zlib
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('extract', HERE/'extract_source_seed.py')
extract=importlib.util.module_from_spec(spec); spec.loader.exec_module(extract)

def sha(data): return hashlib.sha256(data).hexdigest()

def png_rgba(path):
    blob=Path(path).read_bytes(); assert blob[:8]==b'\x89PNG\r\n\x1a\n'
    pos=8; data=b''; width=height=bit_depth=color_type=None
    while pos<len(blob):
        length=struct.unpack_from('>I',blob,pos)[0]; kind=blob[pos+4:pos+8]; value=blob[pos+8:pos+8+length]; pos+=12+length
        if kind==b'IHDR': width,height,bit_depth,color_type,compression,filtering,interlace=struct.unpack('>IIBBBBB',value); assert (bit_depth,color_type,compression,filtering,interlace)==(8,6,0,0,0)
        elif kind==b'IDAT': data+=value
    raw=zlib.decompress(data); stride=width*4; previous=bytearray(stride); out=bytearray(); q=0
    for _ in range(height):
        kind=raw[q]; q+=1; row=bytearray(raw[q:q+stride]); q+=stride
        for i in range(stride):
            left=row[i-4] if i>=4 else 0; up=previous[i]
            if kind==1: row[i]=(row[i]+left)&255
            elif kind==2: row[i]=(row[i]+up)&255
            elif kind==3: row[i]=(row[i]+((left+up)//2))&255
            elif kind==4:
                upper_left=previous[i-4] if i>=4 else 0; p=left+up-upper_left; pa,pb,pc=abs(p-left),abs(p-up),abs(p-upper_left); row[i]=(row[i]+(left if pa<=pb and pa<=pc else up if pb<=pc else upper_left))&255
            else: assert kind==0
        out+=row; previous=row
    return [width,height],bytes(out)

def main():
    old=extract.read_layer(HERE.parent.parent/'2026-10-29-luna-independent-trials/trial-a/passes/pass-01.aseprite','converted-seed')
    baseline=extract.read_layer(HERE/'shared-source-seed-baseline.aseprite','shared-source-seed')
    paths=['source-only-converted-seed.png','shared-source-seed-baseline.png','shared-source-seed-baseline-reopen.png']
    decoded={name:png_rgba(HERE/name) for name in paths}
    equality={name:{'dimensions_equal':value[0]==old['canvas'],'decoded_rgba_equal':value[1]==old['rgba'],'decoded_rgba_sha256':sha(value[1]),'file_sha256':sha((HERE/name).read_bytes())} for name,value in decoded.items()}
    assert old['rgba']==baseline['rgba'] and old['palette_entries']==baseline['palette_entries'] and all(row['dimensions_equal'] and row['decoded_rgba_equal'] for row in equality.values())
    report={'passed':True,'old_source_layer':{'file_sha256':old['source_file_sha256'],'decoded_rgba_sha256':sha(old['rgba']),'palette_chunk_sha256':old['palette_chunk_sha256'],'palette_entry_count':len(old['palette_entries'])},'shared_native':{'file_sha256':baseline['source_file_sha256'],'decoded_rgba_sha256':sha(baseline['rgba']),'palette_chunk_sha256':baseline['palette_chunk_sha256'],'palette_entry_count':len(baseline['palette_entries']),'same_ordered_palette_as_old_source':True,'layers':['shared-source-seed'],'frames':1},'pngs':equality}
    (HERE/'shared-fixture-checks.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
if __name__=='__main__': main()
