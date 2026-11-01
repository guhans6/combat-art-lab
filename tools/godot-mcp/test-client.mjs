import {Client} from '../../.art-tools/godot-mcp/node_modules/@modelcontextprotocol/sdk/dist/client/index.js';
import {StdioClientTransport,getDefaultEnvironment} from '../../.art-tools/godot-mcp/node_modules/@modelcontextprotocol/sdk/dist/client/stdio.js';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import path from 'node:path';
const root='/Users/guhan/Guhan/Projects/combat-art-lab';
const project=path.join(root,'godot/standing-idle-lab');
const out=path.join(root,'docs/experiments/2026-10-27-standing-idle-godot/godot-mcp-install');
const report={date:'2026-10-27',method:'real MCP stdio initialization and tools/call through MCP SDK; no direct Godot CLI calls by test client',package:'@coding-solo/godot-mcp',packageVersion:'0.1.1',project,started:new Date().toISOString(),calls:[],nativeCodexToolExposure:'not present in active chat catalog; project configuration recognized by codex mcp get'};
const client=new Client({name:'combat-art-lab-install-smoke',version:'1.0.0'},{capabilities:{}});
const transport=new StdioClientTransport({command:'/Users/guhan/.local/bin/node',args:[path.join(root,'.art-tools/godot-mcp/node_modules/@coding-solo/godot-mcp/build/index.js')],env:{...getDefaultEnvironment(),GODOT_PATH:'/Applications/Godot.app/Contents/MacOS/Godot',DEBUG:'false'},stderr:'pipe'});
let running=false;
function extract(result){return (result.content??[]).filter(c=>c.type==='text').map(c=>c.text).join('\n');}
async function call(name,args){
 const result=await client.callTool({name,arguments:args});
 report.calls.push({name,arguments:args,isError:!!result.isError,text:extract(result)});
 if(result.isError)throw new Error(name+': '+extract(result));
 return extract(result);
}
try{
 await client.connect(transport);report.serverInfo=client.getServerVersion();
 const listed=await client.listTools();report.serverTools=listed.tools.map(t=>({name:t.name,inputSchema:t.inputSchema}));
 for(const name of ['get_godot_version','get_project_info','run_project','get_debug_output','stop_project'])if(!listed.tools.some(t=>t.name===name))throw new Error('Missing required tool '+name);
 const version=await call('get_godot_version',{});if(!version.includes('4.7.2'))throw new Error('Unexpected installed engine version');
 await call('get_project_info',{projectPath:project});
 await call('run_project',{projectPath:project,scene:'res://main.tscn'});running=true;
 let stdout='',stderr='';const deadline=Date.now()+15000;
 while(Date.now()<deadline){
  await new Promise(resolve=>setTimeout(resolve,1000));
  const debug=await call('get_debug_output',{});report.runtime=JSON.parse(debug);
  stdout=report.runtime.output.join('\n');stderr=report.runtime.errors.join('\n');
  if(stdout.includes('ART_LAB_LOOP 2')||stderr.trim())break;
 }
 report.ready=stdout.includes('ART_LAB_READY')&&stdout.includes('frames=8');
 report.loopTwoObserved=stdout.includes('ART_LAB_LOOP 2');
 report.allNativeFrameCapturesObserved=Array.from({length:8},(_,i)=>`ART_LAB_CAPTURE frame-${String(i).padStart(2,'0')} error=0`).every(s=>stdout.includes(s));
 report.runtimeErrorText=stderr.trim();
 const stopped=await call('stop_project',{});running=false;report.stopResult=JSON.parse(stopped);
 if(!report.ready||!report.loopTwoObserved||!report.allNativeFrameCapturesObserved||stderr.trim())throw new Error('Runtime proof incomplete or errors observed');
 report.captureFiles=[];
 for(let i=0;i<8;i++){
  const file=path.join(project,'evidence',`runtime-frame-${String(i).padStart(2,'0')}.png`);const bytes=await readFile(file);
  report.captureFiles.push({path:path.relative(root,file),sha256:createHash('sha256').update(bytes).digest('hex')});
 }
 report.passed=true;
}catch(error){report.passed=false;report.failure=String(error);process.exitCode=1;}
finally{
 if(running){try{report.cleanup=await client.callTool({name:'stop_project',arguments:{}});}catch(error){report.cleanupError=String(error);}}
 await client.close();await mkdir(out,{recursive:true});report.completed=new Date().toISOString();
 await writeFile(path.join(out,'mcp-smoke.json'),JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify({passed:report.passed,serverInfo:report.serverInfo,ready:report.ready,loopTwoObserved:report.loopTwoObserved,allNativeFrameCapturesObserved:report.allNativeFrameCapturesObserved,runtimeErrorText:report.runtimeErrorText,failure:report.failure,report:path.relative(root,path.join(out,'mcp-smoke.json'))},null,2));
}
