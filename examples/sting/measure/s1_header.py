"""S1 f0-71: header row (logo circle, 'Manus' word, 'AI Helper' pill), window edge, hover ring, cursor, background.
Run from pyramids/: python3 measure/s1_header.py"""
import numpy as np
from lib import *

out = {}
for F in range(0, 72):
    x = rgb(F); g = x.mean(axis=2)
    r = {}
    # pill: rows whose longest dark run (lum<90) is >= 35 px
    rows = []
    for y in range(120, 700):
        n, s, e = longest_run(g[y] < 90)
        if n >= 35:
            rows.append((y, s, e))
    if rows:
        ys = [a[0] for a in rows]
        # keep the biggest contiguous row block
        blocks, cur = [], [rows[0]]
        for a in rows[1:]:
            if a[0] == cur[-1][0] + 1: cur.append(a)
            else: blocks.append(cur); cur = [a]
        blocks.append(cur)
        b0 = max(blocks, key=len)
        b = [a for blk in blocks for a in blk if abs(a[0] - b0[0][0]) < 70]
        if len(b0) >= 6:
            r['pill'] = [min(a[1] for a in b), b[0][0], max(a[2] for a in b), b[-1][0] + 1]
    if 'pill' in r:
        px0, py0, px1, py1 = r['pill']
        cy = (py0 + py1) // 2
        band = g[py0 - 30:py1 + 30, :max(px0 - 4, 1)]
        cols = np.nonzero((band < 110).any(axis=0))[0]
        # cluster ink columns by gaps >= 14 px -> [glyph, Manus] (cursor may merge into the glyph f56-71)
        cl = []
        for c in cols:
            if cl and c - cl[-1][-1] < 14: cl[-1].append(c)
            else: cl.append([c])
        cl = [c for c in cl if len(c) >= 4]
        if len(cl) >= 2:
            m = cl[-1]
            sub = band[:, m[0]:m[-1] + 1] < 110
            yy = np.nonzero(sub.any(axis=1))[0]
            r['manus'] = [int(m[0]), int(py0 - 30 + yy.min()), int(m[-1] + 1), int(py0 - 30 + yy.max() + 1)]
            gl = cl[-2]
            r['glyph_x'] = [int(gl[0]), int(gl[-1] + 1)]
            # logo circle: along the header centre row, from glyph outward, first pixel brighter than 251
            row = g[cy]
            lx = gl[0]
            while lx > 0 and row[lx - 1] < 251.5: lx -= 1
            rx = gl[-1]
            while rx < r['manus'][0] - 2 and row[rx + 1] < 251.5: rx += 1
            ccx = (lx + rx + 1) // 2
            d = rx + 1 - lx
            ty = cy - d // 2
            r['logo_circle_x'] = [int(lx), int(rx + 1)]   # horizontal extent on the header centre row (includes the blue hover ring when lit)
            # window left edge: darkest column left of the logo on row cy+70 (1-px border ~#F4F4F4 on #FAFAFA)
            yy2 = min(cy + 70, 719)
            seg = g[yy2, :max(lx - 8, 2)]
            if len(seg) > 10:
                k = int(np.argmin(seg))
                if np.median(seg) - seg[k] >= 4: r['win_left'] = k
            # window top edge: first row above the logo (column ccx) that drops >= 5 below the rows above it
            seg = g[:max(ty - 6, 2), ccx]
            ref = np.median(seg[:40]) if len(seg) > 40 else None
            if ref is not None:
                d = np.nonzero(seg < ref - 5)[0]
                if len(d): r['win_top'] = int(d[0])
            # hover ring: light-blue pixels (b - r > 20) on the header centre row, left of 'Manus'
            seg = x[cy, max(lx - 40, 0):r['manus'][0]]
            blue = np.nonzero(seg[:, 2] - seg[:, 0] > 20)[0]
            if len(blue) >= 6:
                r['ring_x'] = [int(max(lx - 40, 0) + blue.min()), int(max(lx - 40, 0) + blue.max() + 1)]
                r['ring_b_minus_r'] = int((seg[:, 2] - seg[:, 0]).max())
    # ink relative to the row median (works on the blue gradient and for the blurred rise f0-11)
    rm = np.median(g, axis=1, keepdims=True)
    for name, m in (('dark', rm - g > 35), ('bright', g - rm > 10)):
        b = bbox(m)
        if b and m.sum() > 30:
            ys, xs = np.nonzero(m)
            r[name + '_box'] = b; r[name + '_c'] = [round(float(xs.mean()), 1), round(float(ys.mean()), 1)]; r[name + '_px'] = int(m.sum())
    r['sharp'] = round(lapvar(g), 1); gx, gy = grad_xy(g); r['gx_gy'] = round(gx / max(gy, 1e-6), 2)
    # background samples
    r['bg_top'] = patch(F, 0, 0, 40, 40); r['bg_mid'] = patch(F, 0, 340, 40, 380); r['bg_bot'] = patch(F, 0, 680, 40, 720)
    r['bg_top_r'] = patch(F, 680, 0, 720, 40)
    out[F] = r

# cursor: pure-black (<=35) connected blob, 60..900 px, not the pill; tip = top-left-most pixel of the blob
for F in range(0, 72):
    g = gray(F)
    comps = components(g <= 35, 40)
    best = None
    for c in comps:
        x0, y0, x1, y1 = c['bbox']
        w, h = x1 - x0, y1 - y0
        p = out[F].get('pill')
        if p and x0 >= p[0] - 2 and x1 <= p[2] + 2 and y0 >= p[1] - 2 and y1 <= p[3] + 2: continue
        # letters of 'Manus' are pure black too: drop blobs right of the logo circle inside the pill's row band
        lc = out[F].get('ring_x') or out[F].get('logo_circle_x')
        if p and x0 >= 428 and y0 >= p[1] - 12 and y1 <= p[3] + 12: continue   # cursor never sits on the word except blurred f50-55
        if 10 <= h <= 70 and 8 <= w <= 60 and 0.2 < c['area'] / (w * h) < 0.75:
            if best is None or c['cy'] < best['cy']:
                best = c
    if best:
        x0, y0, x1, y1 = best['bbox']
        sub = g[y0:y1, x0:x1] <= 35
        ys, xs = np.nonzero(sub)
        k = np.argmin(ys + xs)
        out[F]['cursor_tip'] = [int(x0 + xs[k]), int(y0 + ys[k])]
        out[F]['cursor_box'] = best['bbox']

# header blur: Gaussian sigma that turns the sharp f36 header strip into frame F's strip (same content, shifted)
def hdr_strip(F, cy):
    cy = int(round(cy)); return (300, max(cy - 45, 0), 720, min(cy + 45, 720))
ref_cy = 357.5
for F in range(0, 72):
    m = out[F].get('manus')
    if m and (m[3] - m[1]) < 40:
        out[F]['header_cy'] = (m[1] + m[3]) / 2
for F in range(0, 20):
    cy = out[F].get('header_cy')
    if cy:
        roi_t = hdr_strip(F, cy); roi_s = hdr_strip(36, ref_cy)
        # crop the sharp frame at its own header position, target at its header position
        from PIL import Image, ImageFilter
        im = Image.open(path(36)).convert('L').crop(roi_s)
        tg = gray(F)[roi_t[1]:roi_t[3], roi_t[0]:roi_t[2]]
        t = genergy(tg); lo, hi = 0.0, 30.0
        if t < genergy(np.asarray(im, float)) * 0.97:
            for _ in range(16):
                mid = (lo + hi) / 2
                if genergy(np.asarray(im.filter(ImageFilter.GaussianBlur(mid)), float)) > t: lo = mid
                else: hi = mid
        out[F]['header_blur_sigma'] = round((lo + hi) / 2, 2) if hi < 30 else None
        gx, gy = grad_xy(tg); out[F]['header_gx_gy'] = round(gx / max(gy, 1e-6), 2)

# window body opacity during the reveal: projection of F-f12 onto f24-f12 in the lower-right card region
A, B = gray(12)[450:720, 500:720], gray(24)[450:720, 500:720]
for F in range(8, 30):
    v = gray(F)[450:720, 500:720] - A
    out[F]['win_alpha'] = round(float((v * (B - A)).sum() / ((B - A) ** 2).sum()), 3)

if __name__ == '__main__':
    for F in range(0, 72):
        r = out[F]
        print(F, {k: r[k] for k in r if not k.startswith('bg') and k not in ('dark_px','bright_px')})
    save_part('s1_header', out)
