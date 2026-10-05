"""Side-by-side sync video at 60p: LEFT original (ref frame N//2, 29.97 -> doubled), RIGHT remake (frames60/fN).
Run from examples/sting: python3 sync60.py -> out/side-by-side.mp4 (1920x1080, our audio/mix.wav)."""
import glob, io, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'engine')); from ffmpeg_path import ffmpeg_bin, ffmpeg_cwd
FF = os.environ.get('FFMPEG') or ffmpeg_bin()
N = len(glob.glob('frames60/f*.png')); P = 930; Y = 100
try: font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 30)
except Exception: font = ImageFont.load_default()
vid = 'out/side-by-side.video.mp4'
p = subprocess.Popen([FF, '-v', 'error', '-y', '-f', 'image2pipe', '-framerate', '60000/1001', '-vcodec', 'png', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', os.path.abspath(vid)], cwd=ffmpeg_cwd(), stdin=subprocess.PIPE)
for n in range(N):
    C = Image.new('RGB', (1920, 1080), (12, 12, 14)); d = ImageDraw.Draw(C)
    L = Image.open(f'ref/fr/f{min(n // 2, 359):04d}.jpg').convert('RGB').resize((P, P), Image.LANCZOS)
    R = Image.open(f'frames60/f{n:04d}.png').convert('RGB').resize((P, P), Image.LANCZOS)
    C.paste(L, (20, Y)); C.paste(R, (1920 - 20 - P, Y))
    d.text((20, 40), 'original', fill=(200, 200, 205), font=font); d.text((1920 - 20 - P, 40), 'Frame by Frame remake', fill=(200, 200, 205), font=font)
    b = io.BytesIO(); C.save(b, 'PNG', compress_level=1); p.stdin.write(b.getvalue())
p.stdin.close(); assert p.wait() == 0
subprocess.run([FF, '-v', 'error', '-y', '-i', os.path.abspath(vid), '-i', os.path.abspath('audio/mix.wav'), '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', os.path.abspath('out/side-by-side.mp4')], cwd=ffmpeg_cwd(), check=True)
os.remove(vid); print('wrote out/side-by-side.mp4', N, 'frames')
