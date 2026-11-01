"""Minimal red/green regression probe for the reported Aseprite startup abort."""
import subprocess,json,sys,time
exe='/Applications/Aseprite.app/Contents/MacOS/aseprite'
start=time.monotonic();p=subprocess.run([exe,'--version'],capture_output=True,text=True,timeout=10)
result={'command':[exe,'--version'],'passed':p.returncode==0 and p.stdout.strip().startswith('Aseprite '),'returncode':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()[:1500],'elapsed_seconds':round(time.monotonic()-start,3)}
print(json.dumps(result,indent=2));sys.exit(0 if result['passed'] else 1)
