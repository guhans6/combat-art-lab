#!/usr/bin/env python3
"""Read-only, standard-library Aseprite layer extractor for the shared seed."""
from __future__ import annotations
import argparse, hashlib, json, struct, zlib
from pathlib import Path

def sha(data): return hashlib.sha256(data).hexdigest()

def read_layer(path, wanted):
    blob=Path(path).read_bytes()
    size,magic,frames,w,h,depth=struct.unpack_from('<I5H',blob)
    assert size==len(blob) and magic==0xA5E0 and frames==1 and depth==32
    pos=128; length,frame_magic,old_count,_=struct.unpack_from('<I3H',blob,pos)
    assert frame_magic==0xF1FA
    count=struct.unpack_from('<I',blob,pos+12)[0] or old_count; pos+=16
    layers=[]; cels={}; palette=[]; palette_bytes=b''
    for _ in range(count):
        chunk_len,kind=struct.unpack_from('<IH',blob,pos); data=blob[pos+6:pos+chunk_len]
        if kind==0x2004:
            name_len=struct.unpack_from('<H',data,16)[0]; layers.append(data[18:18+name_len].decode())
        elif kind==0x2005:
            layer,x,y,opacity,cel_type,z=struct.unpack_from('<HhhBHh',data)
            assert cel_type in (0,2), 'linked/tilemap cel unsupported'
            cw,ch=struct.unpack_from('<HH',data,16); raw=data[20:] if cel_type==0 else zlib.decompress(data[20:])
            assert len(raw)==cw*ch*4; cels[layer]=(x,y,cw,ch,opacity,z,raw)
        elif kind==0x2019:
            palette_bytes=data; entries,first,last=struct.unpack_from('<III',data); assert entries>=last+1 and first<=last
            q=20
            for index in range(first,last+1):
                flags=struct.unpack_from('<H',data,q)[0]; rgba=tuple(data[q+2:q+6]); q+=6
                if flags&1: label_len=struct.unpack_from('<H',data,q)[0]; q+=2+label_len
                palette.append({'index':index,'rgba':rgba})
        pos+=chunk_len
    assert pos==128+length and wanted in layers
    index=layers.index(wanted); assert index in cels
    x,y,cw,ch,opacity,z,raw=cels[index]; assert opacity==255
    canvas=bytearray(w*h*4)
    for row in range(ch): canvas[((y+row)*w+x)*4:((y+row)*w+x+cw)*4]=raw[row*cw*4:(row+1)*cw*4]
    return {'source_file_sha256':sha(blob),'canvas':[w,h],'layer':wanted,'layer_index':index,'cel_geometry':[x,y,cw,ch],'cel_raw_sha256':sha(raw),'rgba':bytes(canvas),'palette_chunk_sha256':sha(palette_bytes),'palette_entries':palette}

def png(w,h,rgba):
    def chunk(kind,data): return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
    scan=b''.join(b'\0'+rgba[row*w*4:(row+1)*w*4] for row in range(h))
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(scan,9))+chunk(b'IEND',b'')

def detail(native):
    rgba=native['rgba']; colors={tuple(rgba[i:i+3]) for i in range(0,len(rgba),4) if rgba[i+3]}; alphas=sorted(set(rgba[3::4]))
    return {key:value for key,value in native.items() if key!='rgba'}|{'decoded_rgba_sha256':sha(rgba),'visible_pixel_count':sum(1 for i in range(3,len(rgba),4) if rgba[i]),'visible_rgb_color_count':len(colors),'visible_rgb_sha256':sha(b''.join(bytes(c) for c in sorted(colors))),'alpha_values':alphas,'binary_alpha':set(alphas)<={0,255}}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--source',type=Path,required=True); p.add_argument('--compare',type=Path,required=True); p.add_argument('--layer',default='converted-seed'); p.add_argument('--out-png',type=Path,required=True); p.add_argument('--out-json',type=Path,required=True); a=p.parse_args()
    source=read_layer(a.source,a.layer); compare=read_layer(a.compare,a.layer); equal=source['rgba']==compare['rgba']; assert equal, 'same named layer differs'
    a.out_png.write_bytes(png(*source['canvas'],source['rgba'])); sd,cd=detail(source),detail(compare)
    report={'purpose':'Deterministic source-only layer extraction; no art modification, overlay, or raster copy.','source':{'path':str(a.source),**sd},'comparison_source':{'path':str(a.compare),**cd},'same_named_layer_decoded_rgba_equal':equal,'output_png':{'path':str(a.out_png),'file_sha256':sha(a.out_png.read_bytes()),'decoded_rgba_sha256':sd['decoded_rgba_sha256']}}
    a.out_json.write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
if __name__=='__main__': main()
