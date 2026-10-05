"""S5 f187-214 single photo card (Khufu) and S6 f215-244 two stacked cards (Khufu / Khafre).
Photo = saturated or dark pixels (sat > 18 or lum < 120), largest connected regions.
Card (S5) = pure-white pixels (all channels >= 253, blue >= 254) - the page behind is #FDFDFB.
Run from pyramids/measure: python3 s5_cards.py"""
import numpy as np
from lib import *

out = {}
for F in range(187, 245):
    x = rgb(F); g = x.mean(axis=2)
    sat = x.max(axis=2) - x.min(axis=2)
    photo = (sat > 18) | (g < 120)
    cs = components(photo, 400)
    r = {}
    if F <= 214:
        if cs:
            c = cs[0]; r['photo'] = c['bbox']; r['photo_px'] = c['area']
            x0, y0, x1, y1 = c['bbox']
            # caption: black ink (lum < 90) below the photo, within the photo's x range
            sub = g[y1 + 4:min(y1 + 120, 720), x0:x1] < 90
            b = bbox(sub, x0, y1 + 4)
            if b: r['caption'] = b
        card = (x.min(axis=2) >= 253) & (x[..., 2] >= 254)
        cc = components(card, 2000)
        if cc:
            r['card_white'] = cc[0]['bbox']
    else:
        two = [c for c in cs[:4] if c['area'] > 2000]
        two = sorted(two[:2], key=lambda c: c['cy'])
        for name, c in zip(('top', 'bottom'), two):
            r['photo_' + name] = c['bbox']; r['photo_' + name + '_px'] = c['area']
    r['bg'] = patch(F, 0, 0, 40, 40); r['bg_bot'] = patch(F, 0, 680, 40, 720)
    r['sharp'] = round(lapvar(g), 1); gx, gy = grad_xy(g); r['gx_gy'] = round(gx / max(gy, 1e-6), 2)
    out[F] = r
for F in range(187, 215):
    out[F]['blur_sigma_vs_f205'] = blur_sigma(205, F, (150, 230, 570, 590))
    out[F]['backdrop_blur_sigma'] = blur_sigma(180, F, (0, 100, 130, 600))   # answer text left of the card vs sharp f180
for F in range(215, 245):
    out[F]['blur_sigma_vs_f230'] = blur_sigma(230, F, (170, 100, 550, 610))

if __name__ == '__main__':
    for F in out: print(F, out[F])
    save_part('s5_cards', out)
