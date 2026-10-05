"""Merge measure/parts/*.json into measure/tables.json: per-frame arrays keyed by frame for the main moving
elements, plus derived values (camera scale, orbit angles, typing cadence, beat grid).
Run from pyramids/measure after the part scripts:  python3 build_tables.py
Conventions: frames are 0-based (f0 = ref/full/f_0000.jpg), boxes are [x0, y0, x1, y1] in 720x720 px, x1/y1 exclusive."""
import json, math, os
import numpy as np
from lib import ROOT, FPS

P = os.path.join(ROOT, 'measure', 'parts')
def load(n): return json.load(open(os.path.join(P, n + '.json')))
s1, s2, s3, s4, s5, s7, au, st = (load(n) for n in ('s1_header', 's2_orbit', 's3_prompt', 's4_answer', 's5_cards', 's7_end', 'audio', 'style'))
diff = np.load(os.path.join(ROOT, 'measure', 'diff.npy'))

def keyed(src, f0, f1, fn):
    out = {}
    for F in range(f0, f1 + 1):
        r = src.get(str(F))
        if r is None: continue
        v = fn(r)
        if v is not None: out[str(F)] = v
    return out

T = {'_about': __doc__.strip().splitlines()[0:3], 'fps': FPS, 'frames': 360, 'size': [720, 720]}
T['frame_diff_96px'] = [round(float(v), 2) for v in diff]
T['cuts'] = [{'frame': F, 'time_s': round(F / FPS, 3), 'diff': round(float(diff[F]), 1)} for F in (72, 101, 159, 187, 215, 245, 301)]

# ---------------- S1 ----------------
REF_W = 116.5            # 'Manus' ink width at rest, median of f33-f47
logo_rise = {0: 621.3, 1: 554.4, 2: 516.5, 3: 490.2, 4: 470.7}   # centre y of the (white) logo disc blob, f0-f4 (s1 bright-blob pass)
def s1_header(r):
    o = {k: r[k] for k in ('pill', 'manus', 'logo_circle_x', 'ring_x', 'win_left', 'win_top', 'header_cy') if k in r}
    m = r.get('manus')
    if m and 3.6 < (m[2] - m[0]) / max(m[3] - m[1], 1) < 4.2:   # clean word box (cursor not merged)
        o['camera_scale'] = round((m[2] - m[0]) / REF_W, 3)
    if m and 5 <= int(r.get('_F', 0)) or m:
        o['camera_scale_from_x1'] = round((m[2] - 360) / 191.0, 3)   # right edge of 'Manus' about the pivot x=360 (valid when the cursor dirties the left side)
    return o or None
T['S1_header'] = keyed(s1, 0, 71, s1_header)
for F, y in logo_rise.items():
    T['S1_header'].setdefault(str(F), {})['logo_disc_cy'] = y
T['S1_cursor'] = keyed(s1, 0, 71, lambda r: {'tip': r['cursor_tip'], 'box': r['cursor_box']} if 'cursor_tip' in r else None)
T['S1_bg'] = keyed(s1, 0, 71, lambda r: {'top': r['bg_top'], 'mid': r['bg_mid'], 'bottom': r['bg_bot']})
T['S1_window_alpha'] = keyed(s1, 8, 29, lambda r: r.get('win_alpha'))
T['S1_header_blur_sigma'] = keyed(s1, 0, 19, lambda r: r.get('header_blur_sigma'))

# ---------------- S2 ----------------
def s2_row(r):
    o = {}
    if 'icon' in r: o['icon'] = r['icon']['bbox']
    if 'halo_x' in r: o['halo_x'] = r['halo_x']
    ic = r['icon']['c'] if 'icon' in r else [360, 360]
    for k in ('yellow', 'blue', 'green', 'magenta'):
        if k in r:
            cx, cy = r[k]['c']
            ang = math.degrees(math.atan2(cy - ic[1], cx - ic[0]))      # 0 deg = right, +90 = down (screen)
            o[k] = {'c': [round(cx, 1), round(cy, 1)], 'bbox': r[k]['bbox'], 'r': round(math.hypot(cx - ic[0], cy - ic[1]), 1), 'deg': round(ang, 1)}
    o['blur_sigma'] = r.get('blur_sigma_vs_f86')
    return o
T['S2_orbit'] = keyed(s2, 72, 100, s2_row)

# ---------------- S3 ----------------
typed = {121: 5, 122: 5, 123: 6, 124: 7, 125: 7, 126: 8, 127: 9, 128: 10, 129: 10, 130: 11, 131: 12, 132: 13, 133: 13, 134: 14,
         135: 15, 136: 15, 137: 16, 138: 17, 139: 18, 140: 18, 141: 19, 142: 20, 143: 20, 144: 21, 145: 22, 146: 23, 147: 23,
         148: 24, 149: 25, 150: 26}
PROMPT = 'Tell me about the pyramids'
def s3_row(r):
    o = {k: r[k] for k in ('bezel_top_x100', 'bezel_top_x360', 'menubar_y', 'menubar_icon', 'box', 'text_x', 'text_y', 'send', 'cursor_body', 'cursor_tip_est') if k in r and r[k] is not None}
    for k in ('dot_blue', 'dot_green', 'dot_magenta'):
        if k in r: o[k] = r[k]['c']
    o['blur_sigma'] = r.get('blur_sigma_vs_f135'); o['page_top'] = r.get('page_top')
    return o
T['S3_laptop'] = keyed(s3, 101, 158, s3_row)
T['S3_typing'] = {'text': PROMPT, 'source': 'chars read by eye from per-frame crops (scratch type.png); caret "|" shown every frame f121-f158',
                  'chars_by_frame': {str(F): n for F, n in typed.items()},
                  'visible_by_frame': {str(F): PROMPT[:n] for F, n in typed.items()}}

# ---------------- S4 ----------------
eye_dy = {159: 280, 160: 210}     # bold line centre read by eye on the smeared frames (profile match fails there)
def s4_row(r):
    o = {k: r[k] for k in ('dy_vs_f180', 'bold_box', 'cursor_tip', 'cursor_box', 'bg_top') if k in r}
    o['blur_sigma'] = r.get('blur_sigma_vs_f180')
    return o
T['S4_answer'] = keyed(s4, 159, 186, s4_row)
for F, v in eye_dy.items():
    T['S4_answer'][str(F)]['dy_vs_f180'] = v; T['S4_answer'][str(F)]['dy_source'] = 'eye (bold line centre on smeared frame)'
T['S4_answer']['_note'] = 'text block y = its f180 position + dy. f180 bold "Pyramid of Khufu" box [231,346,471,374]; left text edge x=80 all frames'

# ---------------- S5 / S6 ----------------
T['S5_card'] = keyed(s5, 187, 214, lambda r: {'photo': r.get('photo'), 'caption': r.get('caption'), 'card_white': r.get('card_white'), 'blur_sigma': r.get('blur_sigma_vs_f205'), 'backdrop_blur_sigma': r.get('backdrop_blur_sigma')})
T['S6_cards'] = keyed(s5, 215, 244, lambda r: {'photo_top': r.get('photo_top'), 'photo_bottom': r.get('photo_bottom'), 'blur_sigma': r.get('blur_sigma_vs_f230')})

# ---------------- S7 / S8 ----------------
T['S7_disc'] = keyed(s7, 245, 300, lambda r: {'disc': r.get('disc'), 'glyph': r.get('glyph'), 'blur_sigma': r.get('blur_sigma_vs_f270')})
T['S8_endcard'] = keyed(s7, 301, 359, lambda r: {'word': r.get('word'), 'word_w': (r['word'][2] - r['word'][0]) if r.get('word') else None,
                                                 'halo': r.get('halo'), 'bg_corner': r.get('bg_corner'), 'bg_below_word': r.get('bg_centre_below'),
                                                 'blur_sigma': r.get('blur_sigma_vs_f320')})

# ---------------- audio ----------------
BPM, EIGHTH, PH = 124.03, 0.2419, 0.048
beats = [round(PH + k * 2 * EIGHTH, 3) for k in range(0, 26) if PH + k * 2 * EIGHTH < 12.07]
T['audio'] = {k: au[k] for k in ('sr', 'duration_s', 'peak_dbfs', 'rms_dbfs_total', 'integrated_loudness_LUFS_approx', 'first_above_-50dBFS_s', 'tempo_candidates_bpm_ac', 'loudness_arc_0.5s')}
T['audio']['tempo_bpm_fit'] = BPM
T['audio']['beat_grid_s'] = beats
T['audio']['beat_grid_frames'] = [round(b * FPS, 2) for b in beats]
T['audio']['onsets'] = au['onsets']
T['audio']['low_band_hits'] = au['low_band_hits']
T['style'] = st
T['radii'] = load('radii')

json.dump(T, open(os.path.join(ROOT, 'measure', 'tables.json'), 'w'), indent=1)
print('wrote measure/tables.json', os.path.getsize(os.path.join(ROOT, 'measure', 'tables.json')), 'bytes')

# --- quick easing readouts for the spec ---
def share(vals):
    end = vals[-1]; out = []
    for a, b in zip(vals[:-1], vals[1:]):
        out.append(round(100 * (1 - (b - end) / (a - end)), 0) if a != end else None)
    return out
if __name__ == '__main__':
    hy = [T['S1_header'][str(F)].get('header_cy', T['S1_header'][str(F)].get('logo_disc_cy')) for F in range(0, 38)]
    print('S1 header cy f0-37', hy); print('  share %', share(hy))
    sc = [T['S1_header'].get(str(F), {}).get('camera_scale') for F in range(40, 72)]
    print('S1 camera scale f40-71', sc)
    print('S2 icon w', [ (F, T['S2_orbit'][str(F)]['icon'][2] - T['S2_orbit'][str(F)]['icon'][0]) for F in range(72, 101)])
    print('S2 deg', {F: {k: T['S2_orbit'][str(F)][k]['deg'] for k in ('yellow', 'blue', 'green', 'magenta') if k in T['S2_orbit'][str(F)]} for F in range(72, 101, 2)})
    print('S2 r', {F: {k: T['S2_orbit'][str(F)][k]['r'] for k in ('yellow', 'blue', 'green', 'magenta') if k in T['S2_orbit'][str(F)]} for F in range(72, 101, 2)})
    dy = [T['S4_answer'][str(F)]['dy_vs_f180'] for F in range(159, 187)]
    print('S4 dy', dy); print('  share %', share(dy[:22]))
    py = [T['S5_card'][str(F)]['photo'][1] for F in range(189, 210)]
    print('S5 photo y0 f189-209', py); print('  share', share(py))
    t6 = [T['S6_cards'][str(F)]['photo_top'][1] for F in range(215, 245)]
    print('S6 top y0', t6)
    d7 = [T['S7_disc'][str(F)]['disc'][1] for F in range(245, 301)]
    print('S7 disc y0', d7)
    w8 = [T['S8_endcard'][str(F)]['word_w'] for F in range(301, 360)]
    print('S8 word w', w8)
