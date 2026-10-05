"""S3 f101-158: laptop bezel + menu bar, menu-bar dots, glass prompt box, typed text width, cursor.
Run from pyramids/measure: python3 s3_prompt.py"""
import numpy as np
from lib import *

out = {}
for F in range(101, 159):
    x = rgb(F); g = x.mean(axis=2); R, G, B = x[..., 0], x[..., 1], x[..., 2]
    r = {}
    # bezel top edge: first row (x=100 and x=360 columns) darker than 128 below the white page
    for cx in (100, 360):
        col = g[:, cx]; d = np.nonzero(col < 128)[0]
        if len(d): r[f'bezel_top_x{cx}'] = int(d[0])
    # bezel right edge: on the row 40 px below the bezel top, last column (from the right) darker than 128
    if 'bezel_top_x360' in r:
        yy = min(r['bezel_top_x360'] + 60, 719)
        d = np.nonzero(g[yy, 360:] > 200)[0]
        r['bezel_right_inner_row'] = yy
        r['bezel_right'] = int(360 + d[0]) if len(d) else None
    # menu bar band: rows whose median over x 0..500 is the menu-bar navy (R 20..60, B 55..100, B-R 25..60)
    mb = []
    for y in range(0, 720):
        m = np.median(x[y, 0:500], axis=0)
        if 20 <= m[0] <= 70 and 50 <= m[2] <= 110 and 20 <= m[2] - m[0] <= 60 and m[1] < 70:
            mb.append(y)
    if mb:
        r['menubar_y'] = [mb[0], mb[-1] + 1]
        y0, y1 = mb[0], mb[-1] + 1
        band = x[y0:y1]
        Rb, Gb, Bb = band[..., 0], band[..., 1], band[..., 2]
        dots = {'blue': (Bb > 180) & (Rb < 140) & (Bb - Gb > 60) & (Gb > 60),
                'green': (Gb > 150) & (Rb < 150) & (Bb < 140),
                'magenta': (Rb > 170) & (Bb > 170) & (Gb < 110)}
        for k, m in dots.items():
            cs = components(m, 15)
            if cs: r['dot_' + k] = {'bbox': [cs[0]['bbox'][0], cs[0]['bbox'][1] + y0, cs[0]['bbox'][2], cs[0]['bbox'][3] + y0], 'c': [cs[0]['cx'], round(cs[0]['cy'] + y0, 1)]}
        # white menu-bar ink (icons + date/time): extent
        wm = band.mean(axis=2) > 200
        b = bbox(wm, 0, y0)
        if b: r['menubar_white_ink'] = b
    # glass prompt box: pixels lighter than the wallpaper (R>58, G>60, B>140) below the menu bar
    ytop = r.get('menubar_y', [0, 300])[1] + 4
    m = (R > 58) & (G > 60) & (B > 140)
    m[:ytop] = False
    m[600:] = False                       # the box never sits this low; the wallpaper's light streak does
    rows = np.nonzero(m.sum(axis=1) >= 150)[0]
    if len(rows) > 20:
        # longest contiguous block of rows
        br = np.split(rows, np.nonzero(np.diff(rows) > 2)[0] + 1); blk = max(br, key=len)
        sub = m[blk[0]:blk[-1] + 1]
        cols = np.nonzero(sub.sum(axis=0) >= 0.4 * len(blk))[0]
        if len(cols) > 40:
            bc = np.split(cols, np.nonzero(np.diff(cols) > 3)[0] + 1); cc = max(bc, key=len)
            r['box'] = [int(cc[0]), int(blk[0]), int(cc[-1] + 1), int(blk[-1] + 1)]
    if 'box' in r:
        x0, y0, x1, y1 = r['box']; h = y1 - y0
        # typed text: near-white pixels in the upper 45 % of the box, inset 12 px
        ty0, ty1 = y0 + 8, y0 + int(0.5 * h)
        sub = g[ty0:ty1, x0 + 12:x1 - 12]
        w = sub > 200
        cols = np.nonzero(w.sum(axis=0) >= 1)[0]
        if len(cols):
            r['text_x'] = [int(x0 + 12 + cols.min()), int(x0 + 12 + cols.max() + 1)]
            rr = np.nonzero(w.any(axis=1))[0]
            r['text_y'] = [int(ty0 + rr.min()), int(ty0 + rr.max() + 1)]
            r['text_w'] = int(cols.max() - cols.min() + 1)
        # send button (cyan disc) inside the box
        cyan = (B > 200) & (G > 140) & (R < 90)
        cyan[:y0] = False; cyan[y1:] = False
        cs = components(cyan, 20)
        if cs: r['send'] = cs[0]['bbox']
        # box fill + border samples
        r['box_fill'] = patch(F, x0 + 30, y0 + int(0.62 * h), x0 + 60, y0 + int(0.62 * h) + 6)
    # menu-bar app icon: black (<= 40) pixels inside the menu-bar rows, left of the blue dot
    if 'menubar_y' in r and 'dot_blue' in r:
        y0, y1 = r['menubar_y']; bx = int(r['dot_blue']['bbox'][0])
        sub = g[y0:y1, max(bx - 70, 0):bx - 2] <= 40
        cs = components(sub, 30)
        if cs:
            c = cs[0]['bbox']; ox = max(bx - 70, 0)
            r['menubar_icon'] = [c[0] + ox, c[1] + y0, c[2] + ox, c[3] + y0]
    # cursor: black (<= 30) pixels BELOW the menu bar near the icon (the tip overlaps the black icon and is
    # hidden there, so this is the visible arrow body; tip_est = its top-left pixel, exact only when the
    # arrow is fully below the bar)
    if 'menubar_icon' in r:
        ix0, iy0, ix1, iy1 = r['menubar_icon']; y1 = r['menubar_y'][1]
        sub = g[y1:min(y1 + 90, 720), max(ix0 - 30, 0):min(ix1 + 60, 720)] <= 30
        cs = [c for c in components(sub, 15) if c['bbox'][3] - c['bbox'][1] >= 6]
        if cs:
            c = cs[0]; ox = max(ix0 - 30, 0)
            bb = [c['bbox'][0] + ox, c['bbox'][1] + y1, c['bbox'][2] + ox, c['bbox'][3] + y1]
            r['cursor_body'] = bb
            sub2 = g[bb[1]:bb[3], bb[0]:bb[2]] <= 30; ys, xs = np.nonzero(sub2); k = np.argmin(ys + xs)
            r['cursor_tip_est'] = [int(bb[0] + xs[k]), int(bb[1] + ys[k])]
            r['cursor_touches_bar'] = bool(c['bbox'][1] == 0)
    r['sharp'] = round(lapvar(g), 1); gx, gy = grad_xy(g); r['gx_gy'] = round(gx / max(gy, 1e-6), 2)
    out[F] = r

# blur vs the sharp settled frame f135 over the menu bar strip (same content, small pan)
for F in range(101, 159):
    out[F]['blur_sigma_vs_f135'] = blur_sigma(135, F, (0, 300, 720, 420))
    out[F]['page_top'] = patch(F, 300, 0, 420, 40)

if __name__ == '__main__':
    for F in out:
        r = out[F]
        print(F, {k: r[k] for k in r if k not in ('menubar_white_ink',)})
    save_part('s3_prompt', out)
