"""Shared helpers for the pyramids reference measurements (numpy + PIL only, no scipy).
All coordinates are in the 720x720 source frame, origin top-left. Frames are ref/full/f_NNNN.jpg, 0-based."""
import json, os
import numpy as np
from PIL import Image, ImageFilter

FPS = 30000 / 1001          # 29.97
N = 360
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_cache = {}

def path(F):
    return os.path.join(ROOT, 'ref', 'full', f'f_{F:04d}.jpg')

def rgb(F):
    if F not in _cache:
        if len(_cache) > 40:
            _cache.clear()
        _cache[F] = np.asarray(Image.open(path(F)).convert('RGB'), np.int16)
    return _cache[F]

def gray(F):
    return rgb(F).mean(axis=2)

def hexc(c):
    return '#%02X%02X%02X' % tuple(int(round(float(v))) for v in c)

def patch(F, x0, y0, x1, y1):
    """median colour of a patch (flat fills, backgrounds)"""
    return hexc(np.median(rgb(F)[y0:y1, x0:x1].reshape(-1, 3), axis=0))

def ink(F, x0, y0, x1, y1, dark=True, pct=4):
    """mean of the darkest (or lightest) pct % of a patch: the fill colour of text inside it"""
    p = rgb(F)[y0:y1, x0:x1].reshape(-1, 3).astype(float)
    lum = p @ np.array([0.299, 0.587, 0.114])
    sel = lum <= np.percentile(lum, pct) if dark else lum >= np.percentile(lum, 100 - pct)
    return hexc(p[sel].mean(axis=0))

def bbox(mask, ox=0, oy=0):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return [int(xs.min()) + ox, int(ys.min()) + oy, int(xs.max()) + 1 + ox, int(ys.max()) + 1 + oy]

def components(mask, min_area=1):
    """8-connected components by row-run union-find. Returns list of dicts {bbox, area, cx, cy}."""
    H, W = mask.shape
    parent = []
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    runs_prev, allruns = [], []
    for y in range(H):
        row = mask[y]
        if not row.any():
            runs_prev = []
            continue
        d = np.diff(np.concatenate([[0], row.astype(np.int8), [0]]))
        starts, ends = np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]
        cur = []
        for s, e in zip(starts, ends):
            idx = len(parent); parent.append(idx)
            for (ps, pe, pidx) in runs_prev:
                if ps <= e and pe >= s:          # 8-connectivity: [s-1, e] overlaps [ps, pe-1]
                    ra, rb = find(idx), find(pidx)
                    if ra != rb:
                        parent[ra] = rb
            cur.append((s, e, idx)); allruns.append((y, s, e, idx))
        runs_prev = cur
    comps = {}
    for (y, s, e, idx) in allruns:
        r = find(idx)
        c = comps.setdefault(r, [10**9, 10**9, -1, -1, 0, 0.0, 0.0])
        c[0] = min(c[0], s); c[1] = min(c[1], y); c[2] = max(c[2], e); c[3] = max(c[3], y + 1)
        n = e - s; c[4] += n; c[5] += n * (s + e - 1) / 2; c[6] += n * y
    out = []
    for c in comps.values():
        if c[4] >= min_area:
            out.append({'bbox': [int(c[0]), int(c[1]), int(c[2]), int(c[3])], 'area': int(c[4]),
                        'cx': round(c[5] / c[4], 1), 'cy': round(c[6] / c[4], 1)})
    return sorted(out, key=lambda c: -c['area'])

def longest_run(row):
    d = np.diff(np.concatenate([[0], row.astype(np.int8), [0]]))
    s, e = np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]
    if len(s) == 0:
        return 0, 0, 0
    k = np.argmax(e - s)
    return int(e[k] - s[k]), int(s[k]), int(e[k])

def lapvar(g):
    """variance of the 4-neighbour Laplacian: a sharpness number (higher = sharper)"""
    L = -4 * g[1:-1, 1:-1] + g[:-2, 1:-1] + g[2:, 1:-1] + g[1:-1, :-2] + g[1:-1, 2:]
    return float(L.var())

def genergy(g):
    """mean squared gradient: falls ~1/sigma^2..1/sigma under Gaussian blur and stays above the JPEG noise floor
    up to sigma ~ 25 px, unlike the Laplacian variance which saturates at sigma ~ 3"""
    g = np.asarray(g, float)
    return float((np.diff(g, axis=0)[:, :-1] ** 2 + np.diff(g, axis=1)[:-1] ** 2).mean())

def grad_xy(g):
    """mean |d/dx| and |d/dy|: ratio > 1.5 means horizontal edges survive = vertical motion blur and vice versa"""
    return float(np.abs(np.diff(g, axis=1)).mean()), float(np.abs(np.diff(g, axis=0)).mean())

def blur_sigma(F_sharp, F, roi=None, sig_max=40):
    """Gaussian sigma (px) that, applied to the sharp frame F_sharp, gives the same gradient energy as F.
    Valid only when F shows roughly the same content as F_sharp (a blur ramp inside one shot)."""
    im = Image.open(path(F_sharp)).convert('L')
    tgt = gray(F)
    if roi:
        x0, y0, x1, y1 = roi
        im = im.crop(roi); tgt = tgt[y0:y1, x0:x1]
    t = genergy(tgt)
    base = genergy(np.asarray(im, float))
    if t >= base * 0.97:
        return 0.0
    lo, hi = 0.0, float(sig_max)
    for _ in range(18):
        mid = (lo + hi) / 2
        v = genergy(np.asarray(im.filter(ImageFilter.GaussianBlur(mid)), float))
        if v > t:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2, 2)

PARTS = os.path.join(ROOT, 'measure', 'parts')

def save_part(name, obj):
    os.makedirs(PARTS, exist_ok=True)
    with open(os.path.join(PARTS, name + '.json'), 'w') as f:
        json.dump(obj, f, separators=(',', ':'))
    print('wrote', os.path.join('measure', 'parts', name + '.json'))
