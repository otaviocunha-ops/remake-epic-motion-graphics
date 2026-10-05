"""Frame by Frame: side-by-side sync check video. Run from the film folder.

    python3 ../engine/sync.py [NAME]     -> out/NAME.mp4 (default out/side-by-side.mp4)

Frame-locked: reference frame F (ref/full/fNNNN.jpg, LEFT, labelled "original") next to rendered frame F
(frames/fNNNN.png, RIGHT, labelled "remake") on a 1920x1080 canvas, with audio/mix.wav as sound if present.
If the two panels drift apart when scrubbed, the timing is off.
Env: FPS (30), PAD (4), LAST (last frame; default = number of frames in frames/ minus 1), REF_DIR (ref/full),
     REF_EXT (jpg), LABELS ("original,remake"), AUDIO (audio/mix.wav), FFMPEG.
"""
import glob
import io
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ffmpeg_path import ffmpeg_bin, ffmpeg_cwd  # noqa: E402

FILM = os.getcwd()
FF = ffmpeg_bin()
FPS = os.environ.get('FPS', '30')
PAD = int(os.environ.get('PAD', '4'))
REF_DIR = os.path.join(FILM, os.environ.get('REF_DIR', os.path.join('ref', 'full')))
REF_EXT = os.environ.get('REF_EXT', 'jpg')
LABELS = os.environ.get('LABELS', 'original,remake').split(',')
LAST = int(os.environ['LAST']) if os.environ.get('LAST') else len(glob.glob(os.path.join(FILM, 'frames', 'f*.png'))) - 1
if LAST < 0:
    raise SystemExit('no frames/ found: run `node ../engine/render.mjs full` first')
name = sys.argv[1] if len(sys.argv) > 1 else 'side-by-side'

W, P = 912, 513                       # each panel (16:9); 32 px gutters; canvas 1920x1080
GX, Y0 = 32, (1080 - 513) // 2 + 24


def load_font(size):
    for f in ('/System/Library/Fonts/Supplemental/Arial Bold.ttf', '/Library/Fonts/Arial Bold.ttf',
              '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 'C:/Windows/Fonts/arialbd.ttf'):
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    try:
        return ImageFont.load_default(size)
    except TypeError:
        return ImageFont.load_default()


font = load_font(26)


def tag(d, x, y, t):
    b = d.textbbox((0, 0), t, font=font)
    w, h = b[2] - b[0] + 28, b[3] - b[1] + 20
    d.rounded_rectangle([x, y, x + w, y + h], 12, fill=(15, 20, 25))
    d.text((x + 14, y + 8 - b[1]), t, fill='white', font=font)


os.makedirs(os.path.join(FILM, 'out'), exist_ok=True)
vid = os.path.join(FILM, 'out', '_sync_video.mp4')
p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', FPS, '-vcodec', 'png', '-i', '-',
                      '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', vid],
                     cwd=ffmpeg_cwd(), stdin=subprocess.PIPE)
for F in range(LAST + 1):
    c = Image.new('RGB', (1920, 1080), (242, 243, 245))
    d = ImageDraw.Draw(c)
    n = f'f{F:0{PAD}d}'
    for i, src in enumerate((os.path.join(REF_DIR, f'{n}.{REF_EXT}'), os.path.join(FILM, 'frames', f'{n}.png'))):
        x = GX + i * (W + GX)
        d.rounded_rectangle([x - 2, Y0 - 2, x + W + 1, Y0 + P + 1], 18, fill=(222, 225, 229))
        im = Image.open(src).convert('RGB').resize((W, P), Image.LANCZOS) if os.path.exists(src) else Image.new('RGB', (W, P), (200, 200, 200))
        m = Image.new('L', (W, P), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, W - 1, P - 1], 16, fill=255)
        c.paste(im, (x, Y0), m)
        tag(d, x, Y0 - 66, LABELS[i] if i < len(LABELS) else '')
    b = io.BytesIO()
    c.save(b, 'PNG', compress_level=1)
    p.stdin.write(b.getvalue())
p.stdin.close()
if p.wait() != 0:
    raise SystemExit('ffmpeg encode failed')
out = os.path.join(FILM, 'out', f'{name}.mp4')
aud = os.path.join(FILM, os.environ.get('AUDIO', os.path.join('audio', 'mix.wav')))
if os.path.exists(aud):
    subprocess.run([FF, '-v', 'error', '-y', '-i', vid, '-i', aud, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', '-movflags', '+faststart', out], cwd=ffmpeg_cwd(), check=True)
    os.remove(vid)
else:
    os.replace(vid, out)
print('wrote', os.path.relpath(out, FILM), os.path.getsize(out) // 1024, 'KB')
