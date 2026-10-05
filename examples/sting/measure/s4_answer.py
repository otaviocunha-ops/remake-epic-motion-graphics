"""S4 f159-186 (+ backdrop under S5 f187-214): answer text block y-scroll, bold line box, cursor, tint, blur.
Scroll = 1-D shift of the row-darkness profile against f180 (works through the motion blur).
Run from pyramids/measure: python3 s4_answer.py"""
import numpy as np
from lib import *

def profile(F, axis):
    g = gray(F)
    return (255 - g[:, 60:520]).mean(axis=1) if axis == 'y' else (255 - g[60:700, :]).mean(axis=0)

def best_shift(p, q, rng):
    """shift s such that p[y] ~ q[y - s] (content of q moved by +s px lands on p)"""
    best, bs = 1e18, 0
    for s in rng:
        if s >= 0: a, b = p[s:], q[:len(q) - s]
        else: a, b = p[:s], q[-s:]
        if len(a) < 200: continue
        e = ((a - a.mean()) - (b - b.mean())) ** 2
        e = e.mean()
        if e < best: best, bs = e, s
    return bs, best

REF = 180
qy, qx = profile(REF, 'y'), profile(REF, 'x')
out = {}
for F in range(159, 215):
    r = {}
    if F <= 186:
        sy, ey = best_shift(profile(F, 'y'), qy, range(-360, 361))
        sx, ex = best_shift(profile(F, 'x'), qx, range(-60, 61))
        r['dy_vs_f180'] = int(sy); r['dx_vs_f180'] = int(sx)
    g = gray(F)
    # bold 'Pyramid of Khufu' = black glyph blobs (lum < 70) no taller than 26 px; the cursor is taller/denser
    cs = components(g < 70, 20)
    letters = [c for c in cs if c['bbox'][3] - c['bbox'][1] <= 26 and c['bbox'][2] - c['bbox'][0] <= 30]
    cur = [c for c in cs if c not in letters and 20 < c['bbox'][3] - c['bbox'][1] <= 60 and c['bbox'][2] - c['bbox'][0] <= 40]
    if len(letters) >= 5:
        xs0 = min(c['bbox'][0] for c in letters); ys0 = min(c['bbox'][1] for c in letters)
        xs1 = max(c['bbox'][2] for c in letters); ys1 = max(c['bbox'][3] for c in letters)
        r['bold_box'] = [xs0, ys0, xs1, ys1]
    if cur:
        c = max(cur, key=lambda c: c['area'])
        x0, y0, x1, y1 = c['bbox']
        sub = g[y0:y1, x0:x1] < 70; ys, xs = np.nonzero(sub)
        k = np.argmin(ys)                       # arrow points UP in this shot: tip = top-most pixel
        r['cursor_tip'] = [int(x0 + xs[k]), int(y0 + ys[k])]; r['cursor_box'] = c['bbox']
    r['bg_top'] = patch(F, 0, 0, 40, 40); r['bg_bot'] = patch(F, 0, 680, 40, 720); r['bg_right'] = patch(F, 680, 300, 720, 340)
    r['sharp'] = round(lapvar(g), 1); gx, gy = grad_xy(g); r['gx_gy'] = round(gx / max(gy, 1e-6), 2)
    out[F] = r
for F in range(159, 187):
    out[F]['blur_sigma_vs_f180'] = blur_sigma(180, F, (60, 60, 700, 700))

if __name__ == '__main__':
    for F in out: print(F, out[F])
    save_part('s4_answer', out)
