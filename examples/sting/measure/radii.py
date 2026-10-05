"""Corner radius of rounded rectangles: fit a circular top-left corner to the first mask pixel per row.
Run from pyramids/measure: python3 radii.py   (writes parts/radii.json)"""
import numpy as np
from lib import *

def fit_radius(mask, x0, y0, rmax=80):
    xs = []
    for dy in range(0, rmax):
        row = np.nonzero(mask[y0 + dy, x0:x0 + rmax + 5])[0]
        xs.append(row[0] if len(row) else np.nan)
    xs = np.array(xs, float); best = None
    for r in range(3, rmax):
        dy = np.arange(len(xs)); pred = np.where(dy < r, r - np.sqrt(np.maximum(r * r - (r - dy) ** 2, 0)), 0)
        ok = ~np.isnan(xs)
        e = np.abs(xs[ok][:r + 5] - pred[ok][:r + 5]).mean()
        if best is None or e < best[0]: best = (e, r)
    return best[1], round(best[0], 2)

R = {}
x = rgb(205); sat = x.max(axis=2) - x.min(axis=2); g = x.mean(axis=2)
R['S5_photo_f205'] = fit_radius((sat > 18) | (g < 120), 151, 232)
x = rgb(230); sat = x.max(axis=2) - x.min(axis=2); g = x.mean(axis=2)
R['S6_top_photo_f230'] = fit_radius((sat > 18) | (g < 120), 180, 112)
x = rgb(150); R['S3_box_f150'] = fit_radius((x[..., 0] > 58) & (x[..., 1] > 60) & (x[..., 2] > 140), 131, 379)
g = gray(86); R['S2_icon_tile_f86'] = fit_radius(g < 60, 300, 300)
x = rgb(86); R['S2_blue_square_f86'] = fit_radius((x[..., 2] > 170) & (x[..., 0] < 150) & (x[..., 2] - x[..., 1] > 50), 339, 187, 30)
R['S7_disc_f270'] = fit_radius(gray(270) < 248.5, 304, 304, 60)
x = rgb(40); g = x.mean(axis=2)
R['S1_window_f40'] = fit_radius(g < 247.5, 272, 270)     # 1-px border ~#F4F4F4 on #FDFDFB page
R['S1_pill_f40'] = fit_radius(g < 90, 586, 336)
g = gray(64); x = rgb(64)
for k, v in R.items(): print(k, 'radius px', v[0], 'mean err', v[1])
save_part('radii', {k: {'radius_px': int(v[0]), 'fit_err_px': v[1]} for k, v in R.items()})
