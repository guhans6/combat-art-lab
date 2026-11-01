"""Public delivered-file checks; original defect and corrupted exports go red."""
from pathlib import Path
import sys,tempfile,unittest
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from verify_contract import inspect

class DeliveredContractTests(unittest.TestCase):
 def test_finite_loop_is_rejected(self):
  with tempfile.TemporaryDirectory() as temp:
   with Image.open(ROOT/'exports/idle-1x.gif') as image:
    frames=[];times=[]
    for i in range(image.n_frames):
     image.seek(i);frames.append(image.copy());times.append(image.info['duration'])
   path=Path(temp)/'finite-loop.gif';frames[0].save(path,save_all=True,append_images=frames[1:],duration=times,loop=2,optimize=False,disposal=2)
   result=inspect(ROOT/'source/coherent-idle-v02.aseprite',gif_path=path)
   self.assertFalse(result['passed'])
   self.assertIn('GIF must loop indefinitely',result['errors'])

 def test_original_exposes_disconnected_primary_anatomy(self):
  result=inspect(ROOT/'baseline/sol-original.aseprite')
  self.assertFalse(result['passed'])
  self.assertTrue(any('F3:' in e and 'disconnected' in e for e in result['errors']))
  self.assertTrue(any('F6:' in e and 'disconnected' in e for e in result['errors']))

 def test_corrected_native_and_real_exports_meet_declared_contract(self):
  result=inspect(ROOT/'source/coherent-idle-v02.aseprite',ROOT/'reopen/sheet.png',ROOT/'exports/idle-1x.gif')
  self.assertTrue(result['passed'],result['errors'])

 def test_exported_foot_drift_is_rejected(self):
  with tempfile.TemporaryDirectory() as temp:
   image=Image.open(ROOT/'reopen/sheet.png').convert('RGBA')
   image.putpixel((128+48,180),(0,0,0,0))
   path=Path(temp)/'bad-foot-sheet.png';image.save(path)
   result=inspect(ROOT/'source/coherent-idle-v02.aseprite',path)
   self.assertFalse(result['passed'])
   self.assertIn('F2: exported sheet differs from native',result['errors'])

 def test_altered_gif_timing_is_rejected(self):
  with tempfile.TemporaryDirectory() as temp:
   frames=[];times=[]
   with Image.open(ROOT/'exports/idle-1x.gif') as image:
    for i in range(image.n_frames):
     image.seek(i);frames.append(image.copy());times.append(image.info['duration'])
   times[0]+=10
   path=Path(temp)/'bad-timing.gif';frames[0].save(path,save_all=True,append_images=frames[1:],duration=times,loop=0,optimize=False,disposal=2)
   result=inspect(ROOT/'source/coherent-idle-v02.aseprite',gif_path=path)
   self.assertFalse(result['passed'])
   self.assertTrue(any('GIF cycle duration differs' in e for e in result['errors']))

if __name__=='__main__':unittest.main()
