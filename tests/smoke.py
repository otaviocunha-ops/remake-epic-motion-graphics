"""End-to-end pipeline test; requires bootstrapped dependencies and FFmpeg."""
import subprocess,sys,tempfile,json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def call(*args):subprocess.run([sys.executable,str(root/'scripts/remake.py'),*map(str,args)],check=True)
with tempfile.TemporaryDirectory(prefix='epic motion smoke ') as t:
    film=Path(t)/'film with spaces'
    call('doctor');call('demo','--output',film);call('analyze',film)
    call('render',film,'--frames','0,12,24,36,48,59');call('render',film,'--full');call('verify',film);call('encode',film);call('sync',film)
    for video,width in [(film/(film.name+'.mp4'),640),(film/'out/side-by-side.mp4',1280)]:
        d=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-count_frames','-show_entries','stream=width,height,nb_read_frames,r_frame_rate','-of','json',str(video)],text=True))['streams'][0]
        assert (d['width'],d['height'],int(d['nb_read_frames']),d['r_frame_rate'])==(width,360,60,'30/1'),d
    # The same seek must return identical pixels after rendering another frame.
    first=(film/'out/stills/f0024.png').read_bytes();call('render',film,'--frames','59,0,24');assert first==(film/'out/stills/f0024.png').read_bytes()
    # Stale frames must block encoding.
    (film/'frames/f9999.png').write_bytes((film/'frames/f0000.png').read_bytes())
    result=subprocess.run([sys.executable,str(root/'scripts/remake.py'),'verify',str(film)],capture_output=True)
    assert result.returncode!=0
print('Smoke PASS: outputs/count/FPS/aspect/repeated-seek/stale-frame rejection')
