"""Read-only RGBA Aseprite evidence decoder. No native-file writing support.
Aseprite public binary layout; raw/compressed/linked cels, flat normal layers only.
"""
from pathlib import Path
import struct as s,zlib,hashlib
from PIL import Image

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(path):
 b=Path(path).read_bytes(); size,magic,n,w,h,depth=s.unpack_from('<I5H',b)
 assert size==len(b) and magic==0xA5E0 and depth==32
 out={'canvas':[w,h],'frames':[],'layers':[],'cels':{},'chunks':[],'header':b[:128].hex()};pos=128
 for f in range(n):
  ln,magic,old,duration=s.unpack_from('<I3H',b,pos);assert magic==0xF1FA
  count=s.unpack_from('<I',b,pos+12)[0] or old;q=pos+16;chunks=[]
  for _ in range(count):
   cl,kind=s.unpack_from('<IH',b,q);data=b[q+6:q+cl];assert cl>=6
   if kind==0x2005:
    l,x,y,opacity,typ,z=s.unpack_from('<HhhBHh',data)
    if typ in (0,2):
     cw,ch=s.unpack_from('<HH',data,16);raw=data[20:] if typ==0 else zlib.decompress(data[20:]);assert len(raw)==cw*ch*4
     small=Image.frombytes('RGBA',(cw,ch),raw)
    elif typ==1:
     ref=s.unpack_from('<H',data,16)[0];prev=out['cels'][(ref,l)];small=prev['small'].copy();cw,ch=small.size
    else: raise AssertionError(('unsupported cel',typ))
    im=Image.new('RGBA',(w,h));im.paste(small,(x,y))
    out['cels'][(f,l)]={'geometry':[x,y,cw,ch],'opacity':opacity,'z':z,'image':im,'small':small,'type':typ}
   else:
    chunks.append({'type':kind,'sha256':hashlib.sha256(data).hexdigest(),'bytes':data.hex()})
    if kind==0x2004:
     flags,typ,level,_,_,blend=s.unpack_from('<6H',data);nl=s.unpack_from('<H',data,16)[0]
     out['layers'].append({'name':data[18:18+nl].decode(),'flags':flags,'type':typ,'level':level,'blend':blend,'opacity':data[12]})
   q+=cl
  assert q==pos+ln
  out['frames'].append({'duration_ms':duration,'chunks':chunks});out['chunks']+=chunks;pos+=ln
 assert pos==len(b)
 return out

def composite(a,f):
 im=Image.new('RGBA',tuple(a['canvas']))
 for l,meta in enumerate(a['layers']):
  if not meta['flags']&1:continue
  assert meta['blend']==0 and meta['opacity']==255
  if (f,l) in a['cels']:
   c=a['cels'][(f,l)];assert c['opacity']==255
   im.alpha_composite(c['image'])
 return im

def rgba_equal(a,b):return a.size==b.size and a.tobytes()==b.tobytes()
def holes(im):
 w,h=im.size;alpha=im.getchannel('A');seen=set();todo=[]
 for x in range(w):todo.extend([(x,0),(x,h-1)])
 for y in range(h):todo.extend([(0,y),(w-1,y)])
 while todo:
  x,y=todo.pop()
  if (x,y) in seen or x<0 or y<0 or x>=w or y>=h or alpha.getpixel((x,y)):continue
  seen.add((x,y));todo.extend([(x+1,y),(x-1,y),(x,y+1),(x,y-1)])
 return {(x,y) for y in range(h) for x in range(w) if not alpha.getpixel((x,y)) and (x,y) not in seen}
