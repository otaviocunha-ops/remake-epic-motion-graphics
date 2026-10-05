"""Frame by Frame: compare sheet. Run from the film folder. `render.mjs compare` calls it.

    python3 ../engine/compare.py 0 40 80

For each frame F: ref/full/fNNNN.jpg (LEFT, the reference) beside out/$OUT/stills/fNNNN.png (RIGHT, the render)
-> out/$OUT/cmp/fNNNN.jpg, plus out/$OUT/cmp/sheet.jpg with every row stacked.
Env: OUT (sub-folder), PAD (zero padding, default 4), FPS (for the time label, default 30),
     REF_DIR (default ref/full), REF_EXT (default jpg).
"""
import os
import sys

from PIL import Image, ImageDraw

FILM = os.getcwd()
PAD = int(os.environ.get('PAD', '4'))
FPS = float(os.environ.get('FPS', '30'))
REF_DIR = os.path.join(FILM, os.environ.get('REF_DIR', os.path.join('ref', 'full')))
REF_EXT = os.environ.get('REF_EXT', 'jpg')
O = os.path.join(FILM, 'out', os.environ.get('OUT', ''))
os.makedirs(os.path.join(O, 'cmp'), exist_ok=True)

rows = []
for a in sys.argv[1:]:
    F = int(a)
    name = f'f{F:0{PAD}d}'
    ours = Image.open(os.path.join(O, 'stills', name + '.png')).convert('RGB').resize((960, 540))
    rp = os.path.join(REF_DIR, f'{name}.{REF_EXT}')
    ref = Image.open(rp).convert('RGB').resize((960, 540)) if os.path.exists(rp) else Image.new('RGB', (960, 540), (235, 235, 235))
    im = Image.new('RGB', (1930, 560), 'white')
    im.paste(ref, (0, 20))
    im.paste(ours, (970, 20))
    d = ImageDraw.Draw(im)
    d.text((6, 3), f'REF f{F}  t={F / FPS:.2f}s' + ('' if os.path.exists(rp) else '  (missing)'), fill='black')
    d.text((976, 3), f'OURS f{F}', fill='black')
    im.save(os.path.join(O, 'cmp', name + '.jpg'), quality=85)
    rows.append(im)
if rows:
    S = Image.new('RGB', (1930, 560 * len(rows)), 'white')
    for i, r in enumerate(rows):
        S.paste(r, (0, 560 * i))
    if S.height > 3400:
        S = S.resize((int(1930 * 3400 / S.height), 3400))
    S.save(os.path.join(O, 'cmp', 'sheet.jpg'), quality=82)
    print('compare sheet ->', os.path.relpath(os.path.join(O, 'cmp', 'sheet.jpg'), FILM))
