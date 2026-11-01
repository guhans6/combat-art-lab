import {Client} from '@modelcontextprotocol/sdk/client/index.js';
import {StdioClientTransport} from '@modelcontextprotocol/sdk/client/stdio.js';
import fs from 'node:fs';
import path from 'node:path';
const root=process.cwd(), dir=path.join(root,'docs/experiments/2026-10-26-pixel-art-pilot/backend-session');fs.mkdirSync(dir,{recursive:true});
const client=new Client({name:'codex-desktop-pilot-adapter',version:'1.0.0'});
const transport=new StdioClientTransport({command:'/Users/guhan/.local/bin/node',args:[path.join(root,'.art-tools/pebbly/node_modules/@pebbly/aseprite-ai-artist/dist/cli.js'),'serve','--headless','--aseprite','/Applications/Aseprite.app/Contents/MacOS/aseprite'],env:{...process.env,ASEPRITE_AI_ALLOW_LUA:'0',ASEPRITE_USER_FOLDER:path.join(root,'.art-tools/pebbly/user-folder')},stderr:'pipe'});
transport.stderr?.on('data',x=>fs.appendFileSync(path.join(dir,'stderr.log'),x));
await client.connect(transport);
fs.writeFileSync(path.join(dir,'catalog.json'),JSON.stringify(await client.listTools(),null,2));
fs.writeFileSync(path.join(dir,'server.json'),JSON.stringify({version:client.getServerVersion(),capabilities:client.getServerCapabilities(),instructions:client.getInstructions()},null,2));
console.log('READY');
let count=0;
while(true){
 const req=path.join(dir,'request.json');
 if(!fs.existsSync(req)){await new Promise(r=>setTimeout(r,100));continue;}
 const batch=JSON.parse(fs.readFileSync(req));fs.unlinkSync(req);
 if(batch.close){await client.close();break;}
 let summaries=[];
 for(const call of batch.calls){
  const id=String(++count).padStart(3,'0');const result=await client.callTool({name:call.name,arguments:call.arguments??{}});
  const images=[];for(let i=0;i<(result.content??[]).length;i++){const c=result.content[i];if(c.type==='image'){const p=path.join(dir,`${id}-${i}.png`);fs.writeFileSync(p,Buffer.from(c.data,'base64'));images.push(p);result.content[i]={type:'image-saved',path:p,mimeType:c.mimeType};}}
  const item={id,time:new Date().toISOString(),call,result,images};fs.writeFileSync(path.join(dir,`${id}.json`),JSON.stringify(item,null,2));summaries.push(item);
 }
 fs.writeFileSync(path.join(dir,'response.json'),JSON.stringify(summaries,null,2));console.log('DONE '+count);
}
