// Portable adapter. Original toolkit renderer is retained in engine/upstream.
import {chromium} from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const film=path.resolve(process.argv[2]||'.');
const c=JSON.parse(fs.readFileSync(path.join(film,'film.json'),'utf8'));
const mode=process.argv[3]||'frames';
let frames;
if(mode==='full') frames=Array.from({length:c.frame_count},(_,i)=>i);
else if(mode==='frames') frames=(process.argv[4]||'').split(',').filter(Boolean).map(Number);
else throw Error('Mode must be frames or full');
if(!frames.length || frames.some(f=>!Number.isInteger(f)||f<0||f>=c.frame_count)) throw Error('Invalid frame range');
if(mode==='frames'&&frames.length>15) throw Error('At most 15 diagnostic frames per call');
const args=['--allow-file-access-from-files','--font-render-hinting=none'];
if(process.env.WEBGL==='1') args.push('--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist');
const browser=await chromium.launch({args});
try {
  const p=await browser.newPage({viewport:{width:c.width,height:c.height},deviceScaleFactor:1});
  let pageError=null; p.on('pageerror',e=>{pageError=e;});
  await p.goto(pathToFileURL(path.join(film,'page.html')).href);
  await p.waitForFunction(()=>window.ready||window.loadError,null,{timeout:90000});
  const failure=await p.evaluate(()=>window.loadError); if(failure) throw Error(failure);
  const coverage=await p.evaluate(()=>window.SHOTS.map(s=>({id:s.id,f0:s.f0,f1:s.f1})));
  fs.mkdirSync(path.join(film,'measure'),{recursive:true});
  fs.writeFileSync(path.join(film,'measure/shot-coverage.json'),JSON.stringify(coverage,null,2));
  const dir=path.join(film,mode==='full'?'frames':'out/stills'); fs.mkdirSync(dir,{recursive:true});
  for(const f of frames) {
    await p.evaluate(async F=>{await window.seekFrame(F); if(!window.SHOTS.some(s=>F>=s.f0&&F<=s.f1)) throw Error(`Missing shot at frame ${F}`);},f);
    if(pageError) throw pageError;
    await p.screenshot({path:path.join(dir,`f${String(f).padStart(c.pad,'0')}.png`)});
  }
  console.log(`Rendered ${frames.length} frames to ${dir}`);
} finally {await browser.close();}
