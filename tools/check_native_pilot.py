"""Independent, fail-closed native RGBA Aseprite reader for this one-frame pilot.
Spec: https://github.com/aseprite/aseprite/blob/main/docs/ase-file-specs.md
All non-cel chunks compared byte-for-byte; cel pixels compared in canvas space.
Not a general purpose Aseprite decoder: linked/tilemap cels are refused.
"""
from pathlib import Path
import struct as s,zlib,hashlib,json,sys
from PIL import Image

def digest(b): return hashlib.sha256(b).hexdigest()
def read(p):
 b=Path(p).read_bytes();size,magic,n,w,h,depth=s.unpack_from('<I5H',b)
 assert size==len(b) and magic==0xA5E0 and depth==32
 out={'canvas':[w,h],'frames':[],'layers':[],'cels':{},'header':b[8:128].hex()};pos=128
 for f in range(n):
  length,magic,old,duration=s.unpack_from('<I3H',b,pos);assert magic==0xF1FA
  count=s.unpack_from('<I',b,pos+12)[0] or old;q=pos+16;chunks=[]
  for _ in range(count):
   ln,kind=s.unpack_from('<IH',b,q);data=b[q+6:q+ln];assert ln>=6
   if kind==0x2005:
    layer,x,y,opacity,typ,z=s.unpack_from('<HhhBHh',data);assert typ in [0,2],typ
    cw,ch=s.unpack_from('<HH',data,16);raw=data[20:] if typ==0 else zlib.decompress(data[20:]);assert len(raw)==cw*ch*4
    im=Image.new('RGBA',(w,h));im.paste(Image.frombytes('RGBA',(cw,ch),raw),(x,y))
    out['cels'][(f,layer)]={'geometry':[x,y,cw,ch], 'opacity':opacity,'z':z,'image':im,'raw_sha256':digest(raw)}
   else:
    chunks.append({'type':hex(kind),'sha256':digest(data)})
    if kind==0x2004:
     flags,typ,level,_,_,blend=s.unpack_from('<6H',data);name_len=s.unpack_from('<H',data,16)[0]
     out['layers'].append({'name':data[18:18+name_len].decode(),'flags':flags,'type':typ,'level':level,'blend':blend,'opacity':data[12]})
   q+=ln
  assert q==pos+length
  out['frames'].append({'duration_ms':duration,'non_cel_chunks':chunks});pos+=length
 assert pos==len(b)
 return out

def compare(before,after,allowed_names,mask):
 a,b=read(before),read(after);fail=[];rows=[]
 for k in ['canvas','header','frames','layers']:
  if a[k]!=b[k]:fail.append(k+' changed')
 if a['cels'].keys()!=b['cels'].keys():fail.append('cel set changed')
 for key,c in a['cels'].items():
  d=b['cels'][key];name=a['layers'][key[1]]['name']
  # Saving can losslessly trim transparent borders. Require original geometry here.
  if {k:c[k] for k in ['geometry','opacity','z']}!={k:d[k] for k in ['geometry','opacity','z']}:fail.append(name+' cel metadata changed')
  ap=list(c['image'].get_flattened_data());bp=list(d['image'].get_flattened_data())
  changed=[i for i,(x,y) in enumerate(zip(ap,bp)) if x!=y]
  outside=[i for i in changed if not mask[i] or name not in allowed_names]
  if outside:fail.append(name+' protected native pixels changed')
  rows.append({'name':name,'changed_pixels':len(changed),'protected_changed_pixels':len(outside),'before_cel':c['geometry'],'after_cel':d['geometry']})
 return {'passed':not fail,'failures':fail,'layers':rows,'frame_metadata_equal':a['frames']==b['frames'],'layer_metadata_equal':a['layers']==b['layers'],'header_equal':a['header']==b['header']}

if __name__=='__main__':
 before,after,profile,mask,out=sys.argv[1:]
 p=json.loads(Path(profile).read_text());m=list(Image.open(mask).convert('L').get_flattened_data())
 r=compare(before,after,p['editable_layers'],m);Path(out).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));sys.exit(0 if r['passed'] else 1)
