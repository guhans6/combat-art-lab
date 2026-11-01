// Real configured-MCP integration probe. No artwork/reference inputs are opened.
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const input=JSON.parse(fs.readFileSync(0,'utf8'));
const base=input.dependencyRoot;
const {Client}=await import(pathToFileURL(path.join(base,'@modelcontextprotocol/sdk/dist/esm/client/index.js')));
const {StdioClientTransport}=await import(pathToFileURL(path.join(base,'@modelcontextprotocol/sdk/dist/esm/client/stdio.js')));
const out=input.output;fs.mkdirSync(out,{recursive:true});
const log=[];const client=new Client({name:'aseprite-startup-regression-probe',version:'1.0.0'});
const transport=new StdioClientTransport({command:input.server.command,args:input.server.args,cwd:input.server.cwd??input.workspace,env:{...process.env,...input.server.env},stderr:'pipe'});
// Keep only non-secret startup diagnostics: no environment dumps or credentials.
transport.stderr?.on('data',x=>fs.appendFileSync(path.join(out,'server-stderr.txt'),x));
let result={passed:false};
async function call(name,args={}){
 const r=await client.callTool({name,arguments:args});
 const saved={call:{name,arguments:args},result:structuredClone(r)};
 for(let i=0;i<(saved.result.content??[]).length;i++){
  const c=saved.result.content[i];if(c.type==='image'){const file=path.join(out,`${String(log.length+1).padStart(2,'0')}-${i}.png`);fs.writeFileSync(file,Buffer.from(c.data,'base64'));saved.result.content[i]={type:'saved_image',path:file,mimeType:c.mimeType};}
 }
 log.push(saved);fs.writeFileSync(path.join(out,'calls.json'),JSON.stringify(log,null,2));
 if(r.isError)throw Error(`${name}: ${r.content?.filter(x=>x.type==='text').map(x=>x.text).join(' ')}`);
 return r.structuredContent;
}
try{
 await client.connect(transport);const catalog=await client.listTools();fs.writeFileSync(path.join(out,'catalog.json'),JSON.stringify(catalog,null,2));
 const pre=await call('preflight');result={passed:false,server:client.getServerVersion(),preflight:pre};
 if(!pre?.ready)throw Error('Aseprite preflight.ready is false: '+JSON.stringify(pre));
 if(input.preflightOnly){result.passed=true;}
 else{
  await call('sprite_manage',{op:'new',width:16,height:16,colorMode:'rgb'});
  await call('sprite_info');
  await call('layer',{op:'rename',name:'Layer 1',newName:'pattern'});
  await call('layer',{op:'create',name:'protected'});
  await call('draw',{layer:'pattern',paletteLock:false,ops:[{kind:'grid',x:2,y:2,legend:{R:'#ff0000',G:'#00ff00'},rows:['R....','R....','RRRGG','...G.']}]});
  await call('draw',{layer:'protected',paletteLock:false,ops:[{kind:'pixels',color:'#0000ff',points:[{x:12,y:4}]}]});
  await call('sprite_manage',{op:'save_as',path:path.join(out,'before.aseprite')});
  await call('export',{op:'png',path:path.join(out,'before.png')});
  await call('look',{op:'preview',scale:16});
  const patch=await call('read_pixels',{region:{x:2,y:2,width:1,height:1}});if(patch.colors[patch.grid[0]]!=='#ff0000')throw Error('Pattern pixel was not red');
  await call('select',{op:'rect',rect:{x:2,y:2,width:1,height:1}});
  await call('draw',{layer:'pattern',paletteLock:false,selectionOnly:true,label:'Smoke: exactly one scoped pixel',ops:[{kind:'pixels',color:'#00ff00',points:[{x:2,y:2},{x:3,y:2}]}]});
  await call('select',{op:'none'});
  const edited=await call('read_pixels',{region:{x:2,y:2,width:2,height:1}});if(edited.colors[edited.grid[0]]!=='#00ff00'||edited.grid[1]!==0)throw Error('Scoped pixel edit did not match');
  const protectedPixel=await call('read_pixels',{layer:'protected',composite:false,region:{x:12,y:4,width:1,height:1}});if(protectedPixel.colors[protectedPixel.grid[0]]!=='#0000ff')throw Error('Protected pixel changed');
  await call('sprite_manage',{op:'save_as',path:path.join(out,'after.aseprite')});
  await call('export',{op:'png',path:path.join(out,'after.png')});
  await call('look',{op:'preview',scale:16});
  await call('sprite_manage',{op:'close'});
  await call('sprite_manage',{op:'open',path:path.join(out,'after.aseprite')});
  const reopened=await call('sprite_info');if(reopened.layers.length!==2||reopened.frameCount!==1)throw Error('Native structure not preserved');
  await call('export',{op:'png',path:path.join(out,'reopened.png')});
  await call('look',{op:'preview',scale:16});
  await call('draw',{layer:'pattern',paletteLock:false,ops:[{kind:'grid',x:2,y:2,legend:{},rows:['.'],transparent:'skip'}]});
  await call('export',{op:'png',path:path.join(out,'skip.png')});
  await call('draw',{layer:'pattern',paletteLock:false,ops:[{kind:'grid',x:2,y:2,legend:{},rows:['.']}]});
  await call('export',{op:'png',path:path.join(out,'erase.png')});
  await call('sprite_manage',{op:'save_as',path:path.join(out,'erase.aseprite')});
  await call('look',{op:'preview',scale:16});
  await call('sprite_manage',{op:'close'});
  await call('sprite_manage',{op:'open',path:path.join(out,'after.aseprite')});
  await call('draw',{layer:'pattern',paletteLock:false,ops:[{kind:'pixels',color:'#ff0000',points:[{x:15,y:15}]}]});
  await call('export',{op:'png',path:path.join(out,'intentional-outside.png')});
  await call('sprite_manage',{op:'save_as',path:path.join(out,'intentional-outside.aseprite')});
  await call('sprite_manage',{op:'close'});
  result.passed=true;result.smoke='MCP operations passed; image delivery and independent pixel/native checks still required';result.calls=log.length;
 }
}catch(e){result.error=e.message;process.exitCode=1;}finally{await client.close().catch(()=>{});fs.writeFileSync(path.join(out,'result.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));}
