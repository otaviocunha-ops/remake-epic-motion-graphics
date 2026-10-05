"""S2 f72-100: black app-icon tile, grey halo disc, and the four coloured squares (yellow/blue/green/magenta).
Run from pyramids/measure: python3 s2_orbit.py"""
import numpy as np
from lib import *

def colour_masks(x):
    R, G, B = x[..., 0], x[..., 1], x[..., 2]
    return {
        'yellow':  (R > 190) & (G > 150) & (B < 120) & (R - B > 110),
        'blue':    (B > 170) & (R < 150) & (B - G > 50),
        'green':   (G > 150) & (R < 150) & (B < 150) & (G - R > 60),
        'magenta': (R > 150) & (B > 150) & (G < 110),
    }

out = {}
for F in range(72, 101):
    x = rgb(F); g = x.mean(axis=2); r = {}
    for name, m in colour_masks(x).items():
        comps = components(m, 30)
        if comps:
            c = comps[0]
            r[name] = {'bbox': c['bbox'], 'c': [c['cx'], c['cy']], 'px': c['area']}
    # black icon tile: largest blob of lum < 60
    comps = components(g < 60, 200)
    if comps:
        c = comps[0]; r['icon'] = {'bbox': c['bbox'], 'c': [c['cx'], c['cy']], 'px': c['area']}
        # halo disc: along the icon centre row, grey pixels (lum 200..247) left and right of the tile
        cy = int(round(c['cy'])); row = g[cy]
        x0, x1 = c['bbox'][0], c['bbox'][2]
        L = x0 - 1
        while L > 0 and 195 < row[L - 1] < 247.5 or (L > 0 and row[L - 1] < 60): L -= 1
        Rr = x1
        while Rr < 719 and (195 < row[Rr + 1] < 247.5 or row[Rr + 1] < 60): Rr += 1
        if x0 - L > 5 or Rr - x1 > 5:
            r['halo_x'] = [int(L), int(Rr + 1)]
    r['sharp'] = round(lapvar(g), 1)
    gx, gy = grad_xy(g); r['gx_gy'] = round(gx / max(gy, 1e-6), 2)
    r['bg'] = patch(F, 0, 0, 40, 40)
    out[F] = r
# blur sigma against the sharpest settled frame f86 (same layout, only small drift)
for F in range(72, 101):
    out[F]['blur_sigma_vs_f86'] = blur_sigma(86, F, (150, 150, 570, 570))

if __name__ == '__main__':
    for F in out:
        r = out[F]
        print(F, 'icon', r.get('icon', {}).get('bbox'), 'halo', r.get('halo_x'), ' '.join(f"{k}:{r[k]['c']}/{r[k]['px']}" for k in ('yellow', 'blue', 'green', 'magenta') if k in r), 'blur', r['blur_sigma_vs_f86'], 'gxgy', r['gx_gy'])
    save_part('s2_orbit', out)
