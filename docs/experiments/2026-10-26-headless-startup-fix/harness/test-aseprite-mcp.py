"""Exercise the actual project MCP configuration and assert Aseprite readiness."""
from pathlib import Path
import argparse,tomllib,subprocess,json,sys
p=argparse.ArgumentParser();p.add_argument('--workspace',type=Path,required=True);p.add_argument('--config',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--preflight-only',action='store_true');a=p.parse_args()
if a.output.exists():p.error('--output must name a new scratch directory; existing evidence is preserved')
config=a.config or a.workspace/'.codex/config.toml';d=tomllib.loads(config.read_text());server=d['mcp_servers']['aseprite-ai-artist']
packageRoot=a.workspace/'aseprite-reconstruction-2026-10-26/.tools/pebbly'
if not packageRoot.exists():packageRoot=a.workspace/'.tools/pebbly'
request={'server':server,'workspace':str(a.workspace),'dependencyRoot':str(packageRoot/'node_modules'),'output':str(a.output),'preflightOnly':a.preflight_only}
run=subprocess.run(['/Users/guhan/.local/bin/node',str(Path(__file__).with_name('smoke.mjs'))],input=json.dumps(request),text=True,timeout=90)
sys.exit(run.returncode)
