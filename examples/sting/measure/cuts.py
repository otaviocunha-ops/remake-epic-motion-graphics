"""Per-frame difference table and cut list (96x96 grey; the source is square).
A cut = diff > 10 and > 2.5 x median of the 13 frames around it (lesson 2.3 rule).
Run from pyramids/measure: python3 cuts.py   -> prints candidates + every frame's diff, saves measure/diff.npy"""
import glob, os
import numpy as np
from PIL import Image
from lib import ROOT, FPS

fs = sorted(glob.glob(os.path.join(ROOT, 'ref', 'full', 'f_*.jpg')))
small = [np.asarray(Image.open(f).convert('L').resize((96, 96)), np.float32) for f in fs]
d = np.array([0.0] + [np.abs(small[i] - small[i - 1]).mean() for i in range(1, len(small))])
np.save(os.path.join(ROOT, 'measure', 'diff.npy'), d)
cuts = [i for i in range(1, len(d)) if d[i] > 10 and d[i] > 2.5 * np.median(d[max(1, i - 6):i + 7])]
print(len(fs), 'frames, hard-cut candidates', cuts)
for i in range(len(d)):
    print(f'f{i:03d} t={i / FPS:.3f} d={d[i]:.2f}' + ('  <== CUT' if i in cuts else ''))
