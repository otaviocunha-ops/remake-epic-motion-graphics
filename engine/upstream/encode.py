"""Frame by Frame: encode frames to MP4. Run from the film folder after `node ../engine/render.mjs full`.

    python3 ../engine/encode.py [NAME]          -> NAME.mp4 (default: film.mp4)

Reads frames/f*.png in order, encodes H.264 (yuv420p, CRF 16, +faststart), and muxes audio/mix.wav if it exists.
Env: FPS (default 30), FRAMES (default frames), AUDIO (default audio/mix.wav), EXPECT (frame count to assert),
     CRF (default 16), FFMPEG (path to ffmpeg; default: ffmpeg on PATH).
"""
import glob
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ffmpeg_path import ffmpeg_bin, ffmpeg_cwd  # noqa: E402

FILM = os.getcwd()
FF = ffmpeg_bin()
name = sys.argv[1] if len(sys.argv) > 1 else 'film'
fps = os.environ.get('FPS', '30')
frames = sorted(glob.glob(os.path.join(FILM, os.environ.get('FRAMES', 'frames'), 'f*.png')))
if not frames:
    raise SystemExit('no frames found: run `node ../engine/render.mjs full` first')
if os.environ.get('EXPECT'):
    assert len(frames) == int(os.environ['EXPECT']), f"expected {os.environ['EXPECT']} frames, found {len(frames)}"
os.makedirs(os.path.join(FILM, 'out'), exist_ok=True)
vid = os.path.join(FILM, 'out', f'{name}.video.mp4')
p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', fps, '-vcodec', 'png', '-i', '-',
                      '-c:v', 'libx264', '-preset', 'slow', '-crf', os.environ.get('CRF', '16'), '-pix_fmt', 'yuv420p',
                      '-movflags', '+faststart', vid], cwd=ffmpeg_cwd(), stdin=subprocess.PIPE)
for f in frames:
    with open(f, 'rb') as fh:
        p.stdin.write(fh.read())
p.stdin.close()
if p.wait() != 0:
    raise SystemExit('ffmpeg video encode failed')
aud = os.path.join(FILM, os.environ.get('AUDIO', os.path.join('audio', 'mix.wav')))
out = os.path.join(FILM, f'{name}.mp4')
if os.path.exists(aud):
    subprocess.run([FF, '-v', 'error', '-y', '-i', vid, '-i', aud, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k',
                    '-shortest', '-movflags', '+faststart', out], cwd=ffmpeg_cwd(), check=True)
    os.remove(vid)
else:
    os.replace(vid, out)
    aud = None
print('wrote', os.path.relpath(out, FILM), f'({len(frames)} frames @ {fps} fps, audio: {os.path.relpath(aud, FILM) if aud else "none"})')
