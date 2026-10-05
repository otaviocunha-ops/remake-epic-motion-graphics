"""S7 f245-300 logo disc on white; S8 f301-359 end card: glowing white word on black.
Run from pyramids/measure: python3 s7_end.py"""
import numpy as np
from lib import *

out = {}
for F in range(245, 360):
    x = rgb(F); g = x.mean(axis=2); r = {}
    if F <= 300:
        cs = components(g < 120, 30)
        if cs:
            b = [min(c['bbox'][0] for c in cs[:6]), min(c['bbox'][1] for c in cs[:6]), max(c['bbox'][2] for c in cs[:6]), max(c['bbox'][3] for c in cs[:6])]
            r['glyph'] = b
        # disc: pixels darker than the page by >= 4 levels (page #FDFDFB, disc ~#F3F3F3)
        disc = g < 248.5
        cs2 = components(disc, 200)
        if cs2:
            r['disc'] = cs2[0]['bbox']; r['disc_c'] = [cs2[0]['cx'], cs2[0]['cy']]
        r['page'] = patch(F, 0, 0, 60, 60)
    else:
        # word: bright core (lum > 200); glow halo: lum > bg + 12
        core = g > 200
        b = bbox(core)
        if b:
            r['word'] = b; r['word_px'] = int(core.sum())
            ys, xs = np.nonzero(core); r['word_c'] = [round(float(xs.mean()), 1), round(float(ys.mean()), 1)]
        bgc = float(np.median(g[:40, :40]))
        halo = g > bgc + 12
        hb = bbox(halo)
        if hb: r['halo'] = hb
        r['bg_corner'] = patch(F, 0, 0, 40, 40); r['bg_centre_below'] = patch(F, 340, 470, 380, 490)
        r['bg_bottom'] = patch(F, 340, 690, 380, 720)
        r['peak_lum'] = int(g.max())
    r['sharp'] = round(lapvar(g), 1); gx, gy = grad_xy(g); r['gx_gy'] = round(gx / max(gy, 1e-6), 2)
    out[F] = r
for F in range(245, 301):
    out[F]['blur_sigma_vs_f270'] = blur_sigma(270, F, (260, 260, 460, 460))
for F in range(301, 360):
    out[F]['blur_sigma_vs_f320'] = blur_sigma(320, F, (120, 280, 600, 440))

if __name__ == '__main__':
    for F in out: print(F, out[F])
    save_part('s7_end', out)
