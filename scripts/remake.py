"""Portable frame-analysis/render/verification CLI. Paths never depend on cwd."""
import argparse, csv, hashlib, json, math, shutil, subprocess, sys, wave
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def run(args,**kwargs):
    return subprocess.run([str(x) for x in args],check=True,**kwargs)

def binary(name,override=None):
    path=override or shutil.which(name)
    if not path or not Path(path).is_file(): raise ValueError(f'{name} not found. Install it or pass --{name} PATH.')
    return str(Path(path).resolve())

def load(film):
    film=Path(film).expanduser().resolve()
    c=json.loads((film/'film.json').read_text(encoding='utf-8'))
    for k in ['width','height','frame_count','pad']:
        if not isinstance(c[k],int) or c[k]<1: raise ValueError(f'Invalid {k}')
    if Fraction(c['fps'])<=0: raise ValueError('Invalid FPS')
    if abs(c['duration']-c['frame_count']/float(Fraction(c['fps'])))>0.000001: raise ValueError('Duration does not match frame count/FPS')
    return film,c

def probe(ref,ffprobe):
    args=[ffprobe,'-v','error','-select_streams','v:0','-count_frames','-show_streams','-show_frames','-show_entries','stream=width,height,r_frame_rate,avg_frame_rate,nb_frames,nb_read_frames,duration:stream_tags=rotate:stream_side_data=rotation:frame=best_effort_timestamp_time','-of','json',ref]
    d=json.loads(run(args,capture_output=True,text=True).stdout)
    if not d.get('streams'): raise ValueError('Reference has no video stream')
    s=d['streams'][0]; fps=Fraction(s['r_frame_rate']); count=int(s.get('nb_read_frames') or s.get('nb_frames') or 0)
    if count<1 or fps<=0: raise ValueError('Invalid frame count/FPS')
    rotation=float(s.get('tags',{}).get('rotate',0))
    for sd in s.get('side_data_list',[]): rotation=float(sd.get('rotation',rotation))
    if rotation%360: raise ValueError('Rotated reference: normalize deliberately and record a frame mapping first.')
    pts=[float(f['best_effort_timestamp_time']) for f in d.get('frames',[]) if 'best_effort_timestamp_time' in f]
    if len(pts)!=count: raise ValueError('Missing reference timestamps; exact frame timing cannot be certified.')
    period=1/float(fps)
    if any(abs((b-a)-period)>max(0.00001,period*0.001) for a,b in zip(pts,pts[1:])):
        raise ValueError('Variable-rate reference: normalize explicitly and record a frame mapping before reconstruction.')
    return {'width':int(s['width']),'height':int(s['height']),'fps':str(fps),'frame_count':count,'duration':count/float(fps),'pad':max(4,len(str(count-1)))},pts

def settings(film,c):
    (film/'film-settings.js').write_text('window.WIDTH='+str(c['width'])+';window.HEIGHT='+str(c['height'])+';window.FPS='+repr(float(Fraction(c['fps'])))+';window.LAST_FRAME='+str(c['frame_count']-1)+';window.BRAND='+json.dumps(c['brand'],ensure_ascii=False)+';window.EXTRA_IMGS=[];\n',encoding='utf-8')

def scaffold(film,c):
    if film.exists(): raise ValueError(f'Refusing to overwrite existing directory: {film}')
    for d in ['shots','assets','audio','ref/full','measure','out']: (film/d).mkdir(parents=True,exist_ok=True)
    shutil.copy2(ROOT/'engine/page.html',film/'page.html');shutil.copy2(ROOT/'engine/core.js',film/'assets/core.js')
    (film/'film.json').write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');settings(film,c)
    for name in ['_data','_shared','A','B','C','D']: (film/f'shots/{name}.js').write_text('// Film-specific '+name+'\n',encoding='utf-8')
    (film/'SPEC.md').write_text('# Film specification\n\n'+json.dumps({k:c[k] for k in ['width','height','fps','frame_count','duration']},indent=2)+'\n\n## Shots\n\nid | f0 | f1 | content | in | out\n---|---|---|---|---|---\n\n## Not pinned\nAll scene measurements await reference inspection.\n',encoding='utf-8')
    (film/'SOURCES.md').write_text('# Sources\n\nRecord every asset, audio policy, URL/license and modifications here.\n',encoding='utf-8')
    (film/'DIFFERENCES.md').write_text('# Remaining differences\n\nframe range | element | difference px/frames | cause | status\n---|---|---|---|---\nAll | All | Unmeasured | Not inspected | NOT CHECKED\n',encoding='utf-8')

def init(a):
    ref=Path(a.reference).expanduser().resolve()
    if not ref.is_file(): raise ValueError('Reference file does not exist')
    c,pts=probe(ref,binary('ffprobe',a.ffprobe))
    c.update(reference=str(ref),reference_sha256=hashlib.sha256(ref.read_bytes()).hexdigest(),brand={'name':a.name},mode='strict',language='pt-BR',swaps={'logo':None,'palette':None,'interface':None,'faces_screens':None,'end_card':None},audio={'policy':None})
    film=Path(a.output).expanduser().resolve();scaffold(film,c)
    (film/'measure/timestamps.json').write_text(json.dumps(pts),encoding='utf-8');print(film)

def analyze(a):
    import numpy as np
    from PIL import Image,ImageDraw
    film,c=load(a.film);ref=Path(c['reference']); ff=binary('ffmpeg',a.ffmpeg)
    if not ref.is_file(): raise ValueError('Reference path unavailable; update film.json')
    actual,pts=probe(ref,binary('ffprobe',a.ffprobe))
    if any(actual[k]!=c[k] for k in ['width','height','fps','frame_count']): raise ValueError('Reference metadata changed')
    if c.get('reference_sha256') and hashlib.sha256(ref.read_bytes()).hexdigest()!=c['reference_sha256']: raise ValueError('Reference changed (SHA256)')
    dest=film/'ref/full';old=list(dest.glob('f*.jpg'))
    if old: raise ValueError('Reference frames already exist; use a fresh project or deliberately clear ref/full.')
    run([ff,'-v','error','-i',ref,'-fps_mode','passthrough','-start_number','0','-q:v','2',dest/f'f%0{c["pad"]}d.jpg'])
    files=sorted(dest.glob('f*.jpg'))
    if len(files)!=c['frame_count']: raise ValueError('Extracted count does not match reference')
    streams=json.loads(run([binary('ffprobe',a.ffprobe),'-v','error','-show_streams','-of','json',ref],capture_output=True,text=True).stdout)['streams']
    if any(s.get('codec_type')=='audio' for s in streams): run([ff,'-v','error','-i',ref,'-vn','-ac','2','-ar','48000',film/'ref/audio.wav'])
    diffs=[0.0]; prev=None
    with (film/'measure/cuts.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f);w.writerow(['frame','diff','cut'])
        for i,p in enumerate(files):
            with Image.open(p) as im: gray=np.asarray(im.convert('L').resize((96,54)),dtype=np.float32)
            diff=0.0 if prev is None else float(np.abs(gray-prev).mean())
            median=float(np.median(diffs[max(1,i-12):])) if i>1 else diff
            cut=int(i>1 and diff>5*max(median,0.1));w.writerow([i,diff,cut]);diffs.append(diff);prev=gray
    fps=float(Fraction(c['fps'])); candidates=list(range(0,c['frame_count'],max(1,round(fps))))
    tw=384;th=round(tw*c['height']/c['width']); cellh=th+24
    for page in range(math.ceil(len(candidates)/30)):
        sheet=Image.new('RGB',(tw*6,cellh*5),'#e7e7e7');draw=ImageDraw.Draw(sheet)
        for j,F in enumerate(candidates[page*30:(page+1)*30]):
            x=j%6*tw;y=j//6*cellh
            with Image.open(files[F]) as im: sheet.paste(im.resize((tw,th)),(x,y))
            draw.text((x+5,y+th+4),f'frame {F} / {F/fps:.3f}s',fill='black')
        sheet.save(film/f'ref/sheet_{page:02}.jpg')
    (film/'measure/timestamps.json').write_text(json.dumps(pts),encoding='utf-8')
    plan=[0,round((c['frame_count']-1)*.2),round((c['frame_count']-1)*.4),round((c['frame_count']-1)*.6),round((c['frame_count']-1)*.8),c['frame_count']-1]
    (film/'measure/compare-plan.json').write_text(json.dumps({'suggested_frames':plan,'status':'Provisional; choose opening, typing, camera, UI, transition, end card after inspection.'},indent=2),encoding='utf-8')
    print('Extracted',len(files),'frames. Inspect sheets/cuts; complete SPEC.md before building.')

def csv_to_js(a):
    film,c=load(a.film);data={}
    for p in sorted((film/'measure').glob('*.csv')):
        if p.stem=='cuts':continue
        with p.open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
        required=['frame','x0','y0','x1','y1','cx','cy','w','h','scale']
        if not rows or any(k not in rows[0] for k in required): raise ValueError(f'{p.name}: expected {required}')
        values=[[float(r[k]) for k in required] for r in rows]
        if any(not math.isfinite(v) for row in values for v in row): raise ValueError('Non-finite CSV value')
        frames=[r[0] for r in values]
        if any(F!=int(F) or F<0 or F>=c['frame_count'] for F in frames): raise ValueError('CSV frame out of range')
        if any(b!=a+1 for a,b in zip(frames,frames[1:])): raise ValueError('CSV tracks need contiguous ascending frames')
        data[p.stem]={'f0':int(frames[0]),'columns':required[1:],'samples':[r[1:] for r in values]}
    (film/'shots/_data.js').write_text('window.MEASURE='+json.dumps(data,ensure_ascii=False)+';\n',encoding='utf-8'); print('Converted',len(data),'tracks')

def validate_sequence(film,c):
    from PIL import Image
    expected=[f'f{i:0{c["pad"]}d}.png' for i in range(c['frame_count'])]
    actual=sorted(p.name for p in (film/'frames').glob('*.png'))
    if actual!=expected: raise ValueError('Missing, extra or stale render frames')
    for name in expected:
        with Image.open(film/'frames'/name) as im:
            if im.size!=(c['width'],c['height']): raise ValueError('Frame dimension mismatch: '+name)
    coverage=json.loads((film/'measure/shot-coverage.json').read_text(encoding='utf-8'))
    validate_coverage(coverage,c['frame_count'])

def validate_coverage(shots,count):
    end=-1;ids=set()
    for s in sorted(shots,key=lambda s:s['f0']):
        if s['id'] in ids or type(s['f0']) is not int or type(s['f1']) is not int or s['f0']!=end+1 or s['f1']<s['f0']: raise ValueError('Shot gap, overlap, invalid range or duplicate id')
        end=s['f1'];ids.add(s['id'])
    if end!=count-1: raise ValueError('Shots do not cover the full film')

def verify(a):
    film,c=load(a.film);validate_sequence(film,c);print('Counts, dimensions and coverage PASS. Visual match NOT CHECKED by this command.')

def comparison(film,c,frames):
    from PIL import Image,ImageDraw,ImageOps
    tw=min(c['width'],960);th=round(tw*c['height']/c['width']); cellh=th+28
    for page in range(math.ceil(len(frames)/5)):
        group=frames[page*5:(page+1)*5];sheet=Image.new('RGB',(tw*2+10,cellh*len(group)),'#202020');draw=ImageDraw.Draw(sheet)
        for row,F in enumerate(group):
            ref=film/f'ref/full/f{F:0{c["pad"]}d}.jpg';rep=film/f'out/stills/f{F:0{c["pad"]}d}.png'
            if not ref.is_file() or not rep.is_file(): raise ValueError('Comparison requires both reference and rendered frames')
            for x,p in [(0,ref),(tw+10,rep)]:
                with Image.open(p) as im: sheet.paste(ImageOps.contain(im.convert('RGB'),(tw,th)),(x,row*cellh+28))
            draw.text((5,row*cellh+6),f'F{F}: REFERENCE left | REPLICA right',fill='white')
        target=film/'out/cmp';target.mkdir(parents=True,exist_ok=True);sheet.save(target/f'sheet_{page:02}.jpg')
    print('Comparison sheets:',film/'out/cmp')

def render(a):
    film,c=load(a.film)
    if a.full and (film/'frames').exists() and any((film/'frames').iterdir()):
        if not a.replace_frames: raise ValueError('Existing frames found. --replace-frames explicitly clears this generated folder.')
        shutil.rmtree(film/'frames')
    env=__import__('os').environ.copy();env['WEBGL']='1' if a.webgl else '0'
    run([binary('node',a.node),ROOT/'engine/render.mjs',film,'full' if a.full else 'frames',a.frames or ''],cwd=film,env=env)
    if not a.full and (film/'ref/full').exists() and any((film/'ref/full').glob('*.jpg')): comparison(film,c,[int(f) for f in a.frames.split(',')])

def encode(a):
    film,c=load(a.film);validate_sequence(film,c);ff=binary('ffmpeg',a.ffmpeg)
    args=[ff,'-v','error','-y','-framerate',c['fps'],'-start_number','0','-i',film/f'frames/f%0{c["pad"]}d.png']
    audio=film/'audio/mix.wav'
    if audio.exists(): args+=['-i',audio,'-af',f'apad,atrim=duration={c["duration"]:.12f}','-c:a','aac','-b:a','256k']
    args+=['-frames:v',str(c['frame_count']),'-c:v','libx264','-crf','16','-preset','slow','-pix_fmt','yuv420p','-movflags','+faststart',film/(film.name+'.mp4')]
    if c['width']%2 or c['height']%2: raise ValueError('H.264 yuv420p requires even dimensions. Choose an explicit padding/codec policy; no silent resize.')
    run(args); print(film/(film.name+'.mp4'))

def sync(a):
    film,c=load(a.film);validate_sequence(film,c)
    refs=list((film/'ref/full').glob('f*.jpg'))
    if len(refs)!=c['frame_count'] or any(not (film/f'ref/full/f{i:0{c["pad"]}d}.jpg').exists() for i in range(c['frame_count'])): raise ValueError('Incomplete reference frames')
    if c['height']%2: raise ValueError('Side-by-side H.264 needs even height; choose explicit padding.')
    run([binary('ffmpeg',a.ffmpeg),'-v','error','-y','-framerate',c['fps'],'-i',film/f'ref/full/f%0{c["pad"]}d.jpg','-framerate',c['fps'],'-i',film/f'frames/f%0{c["pad"]}d.png','-filter_complex','[0:v][1:v]hstack=inputs=2[v]','-map','[v]','-frames:v',str(c['frame_count']),'-c:v','libx264','-crf','18','-pix_fmt','yuv420p',film/'out/side-by-side.mp4']);print(film/'out/side-by-side.mp4')

def doctor(a):
    for name in ['node','ffmpeg','ffprobe']:
        exe=binary(name,getattr(a,name));r=run([exe,'--version' if name=='node' else '-version'],capture_output=True,text=True);print(r.stdout.splitlines()[0])
    import numpy,PIL
    print('Python',sys.version.split()[0],'numpy',numpy.__version__,'Pillow',PIL.__version__)
    if not (ROOT/'node_modules/playwright').exists(): raise ValueError('Playwright missing; run bootstrap')
    run([binary('node',a.node),'--input-type=module','-e',"import {chromium} from 'playwright'; import fs from 'node:fs'; if(!fs.existsSync(chromium.executablePath())) throw Error('Chromium missing'); console.log('Chromium installed');"],cwd=ROOT)

def demo(a):
    import numpy as np
    from PIL import Image,ImageDraw
    film=Path(a.output).expanduser().resolve()
    c={'width':640,'height':360,'fps':'30','frame_count':60,'duration':2.0,'pad':4,'brand':{'name':'Epic'},'mode':'demo','audio':{'policy':'original synthesis'},'swaps':{}}
    scaffold(film,c)
    source=film/'assets/demo-source';source.mkdir()
    for F in range(60):
        t=min(1,F/24);e=1-(1-t)**3;x=round(40+360*e)
        im=Image.new('RGB',(640,360),'#081229');d=ImageDraw.Draw(im)
        d.rounded_rectangle((x,100,x+140,240),radius=24,fill='#348fff');d.ellipse((x+40,145,x+52,160),fill='white');d.ellipse((x+88,145,x+100,160),fill='white')
        im.save(source/f'f{F:04}.png')
    ff=binary('ffmpeg',a.ffmpeg)
    wav=film/'audio/mix.wav';seconds=np.arange(96000)/48000;tone=(np.sin(2*np.pi*220*seconds)*.04*np.minimum(1,seconds*20)*np.minimum(1,(2-seconds)*20)*32767).astype('<i2')
    with wave.open(str(wav),'wb') as f: f.setnchannels(1);f.setsampwidth(2);f.setframerate(48000);f.writeframes(tone.tobytes())
    ref=film/'assets/demo-reference.mp4'
    run([ff,'-v','error','-framerate','30','-i',source/'f%04d.png','-i',wav,'-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-frames:v','60','-c:a','aac',ref])
    c.update(reference=str(ref),reference_sha256=hashlib.sha256(ref.read_bytes()).hexdigest());(film/'film.json').write_text(json.dumps(c,indent=2),encoding='utf-8')
    # Independent HTML geometry recreates the generated PIL reference.
    (film/'shots/A.js').write_text("SHOT({id:'demo',f0:0,f1:59,render(lf,F){const t=Math.min(1,F/24),e=1-(1-t)**3,x=Math.round(40+360*e);return `<div style=\"position:absolute;inset:0;background:#081229\"></div><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"640\" height=\"360\"><rect x=\"${x}\" y=\"100\" width=\"141\" height=\"141\" rx=\"24\" fill=\"#348fff\"/><ellipse cx=\"${x+46}\" cy=\"152.5\" rx=\"6\" ry=\"7.5\" fill=\"white\"/><ellipse cx=\"${x+94}\" cy=\"152.5\" rx=\"6\" ry=\"7.5\" fill=\"white\"/></svg>`;}});",encoding='utf-8')
    (film/'SOURCES.md').write_text('# Demo sources\n\nOriginal procedural PIL/SVG geometry and synthesized sine-wave tone. No third-party media. The demo checks pipeline execution, not exact PIL/Chromium edge rasterization.\n',encoding='utf-8')
    print(film)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    common=argparse.ArgumentParser(add_help=False)
    for b in ['ffmpeg','ffprobe','node']: common.add_argument('--'+b)
    sub=p.add_subparsers(dest='command',required=True)
    q=sub.add_parser('init',parents=[common]);q.add_argument('--reference',required=True);q.add_argument('--output',required=True);q.add_argument('--name',required=True)
    q=sub.add_parser('demo',parents=[common]);q.add_argument('--output',required=True)
    sub.add_parser('doctor',parents=[common])
    for cmd in ['analyze','csv-to-js','verify','encode','sync']:
        q=sub.add_parser(cmd,parents=[common]);q.add_argument('film')
    q=sub.add_parser('render',parents=[common]);q.add_argument('film');g=q.add_mutually_exclusive_group(required=True);g.add_argument('--frames');g.add_argument('--full',action='store_true');q.add_argument('--replace-frames',action='store_true');q.add_argument('--webgl',action='store_true')
    a=p.parse_args()
    try: globals()[a.command.replace('-','_')](a)
    except (ValueError,FileNotFoundError,subprocess.CalledProcessError) as e: p.exit(1,str(e)+'\n')

if __name__=='__main__': main()
