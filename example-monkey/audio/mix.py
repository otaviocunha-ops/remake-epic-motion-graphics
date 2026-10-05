#!/usr/bin/env python3
"""Final audio mix for the monkey example (frame-locked to the reference: 7.5947 s, 364,544 samples at 48 kHz).

    python3 mix.py              # -> audio/mix.wav (music + SFX) and audio/mix_report.json
    python3 mix.py --rebuild    # regenerate music.wav (build_music.py) and sfx/*.wav (sfx.py) first
    python3 mix.py --stems      # also write stems/{music,sfx}.wav

Every cue time is a hit measured on ref/audio.wav (analysis.json). Every cue LEVEL is calibrated, not guessed:
the ref's level in the cue's band and window, moved onto our scale by K (our bed minus the ref bed in the
ref's music-only windows), minus what our music and the already-placed SFX already contribute there.
So each hit sits over our bed the way the ref's hit sits over its bed. Then the sum is normalised to
-14 LUFS integrated and limited to <= -1 dBTP. Nothing from the reference audio is copied into the output.
"""
import argparse
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audiolib import HERE, N_OUT, SR, db, limiter, lufs, place, read_wav, spec_filter, write_wav  # noqa: E402

TARGET_LUFS = -14.0
CEILING_DB = -1.0
AN = json.load(open(os.path.join(HERE, "analysis.json")))
HI = (2500, 12000)

# ---- cue table: (name, time s, anchor, calibration band Hz, calibration window s, pan) ----------------
# anchor: "start" = file start at t (minus a 1 ms pre-roll for ticks), "peak" = loudness peak at t,
#         "rise" = end of the shimmer's rise at t, "end" = file end at t.
# Order = calibration order (dense ticks first, so later cues see them as already present).
CUES = []
BROAD = (300, 12000)
_strong = [t for t, k in AN["onsets"]["hi"] if k >= 2.0 and (0.10 <= t < 0.69 or 1.00 <= t < 1.97)]
PROMPT_TICKS = sorted(AN["ticks"]["prompt"] + [t for t in _strong
                                               if min(abs(t - u) for u in AN["ticks"]["prompt"]) > 0.012])
for i, t in enumerate(PROMPT_TICKS):                      # ref typing cadence (dense texture, analysis.json)
    run2 = t > 0.9                                                  # the 1.00-1.97 run has more body
    CUES.append((("tickb%d" if run2 else "tick%d") % (i % 6 + 1), t - 0.001, "start", BROAD,
                 (t - 0.003, t + 0.009), 0.15 * ((i % 3) - 1), "ticks_b" if run2 else "ticks_a"))
for i, t in enumerate(AN["ticks"]["headline"]):                    # landing-page headline reveal
    CUES.append(("soft_tick%d" % (i % 4 + 1), t - 0.001, "start", (400, 12000), (t - 0.003, t + 0.012), 0.0,
                 "soft_ticks"))
_head_bright = [t for t, k in AN["onsets"]["hi"] if k >= 1.5 and 4.26 <= t < 5.15]   # 4.948 / 5.105: bright
for i, t in enumerate(_head_bright):                                                  # hits in the headline
    CUES.append(("tick%d" % (i % 6 + 1), t - 0.001, "start", HI, (t - 0.003, t + 0.009), 0.0, "head_bright"))
CUES += [
    ("open_hit", 0.0625, "start", (20, 20000), (0.05, 0.15), 0.0, None),       # ref audio starts 0.0607, onset 0.063 every band
    ("whoosh_push", 1.35, "peak", BROAD, (1.29, 1.44), 0.0, None),               # swell peak 1.35; zoom flash f38
    ("whoosh_cut", 2.18, "peak", BROAD, (2.13, 2.40), 0.0, None),                # hi 2.183; cut to button f64
    ("button_click", 2.776, "start", (300, 2500), (2.772, 2.86), 0.1, None),  # press 2.778 + release 2.825
    ("whoosh_pull", 3.30, "peak", BROAD, (3.22, 3.40), 0.0, None),               # hi 3.305; pull-back cut f97
    ("morph_shimmer", 4.08, "rise", HI, (3.85, 4.30), 0.0, None),             # rise 3.58-4.08, bloom to 4.3
    ("sub_boom", 4.088, "start", (20, 150), (4.10, 4.30), 0.0, None),         # sub onset 4.095
    ("low_pop", 5.146, "start", (300, 1000), (5.14, 5.19), 0.0, None),        # sub onset 5.148, 562 Hz body
    ("settle_swell", 6.81, "end", (2000, 20000), (6.00, 6.60), 0.0, None),               # air 5.30-6.68, -18 dB step, gone by 6.81
    ("settle_tick", 6.540, "start", (7000, 16000), (6.535, 6.575), 0.0, None),  # 6.515-6.558; settle f196
]
GROUP_SPREAD_DB = 6.0          # a grouped tick may differ from the group's median gain by at most this
MUSIC_ONLY = [(2.45, 2.72), (5.30, 5.50)]   # ref windows with no SFX (analysis.json loudness_025 / 10 ms dump)


def load_sfx():
    out = {}
    for f in glob.glob(os.path.join(HERE, "sfx", "*.wav")):
        x, sr = read_wav(f)
        assert sr == SR, f
        out[os.path.splitext(os.path.basename(f))[0]] = x.astype(np.float64)
    return out


def anchor(kind, x):
    if kind == "end":
        return len(x) / SR
    if kind == "rise":
        return 0.50                                    # morph_shimmer's rise length (sfx.py)
    if kind == "peak":
        hop = int(0.005 * SR)
        k = len(x) // hop
        e = np.convolve((x[:k * hop] ** 2).mean(1).reshape(k, hop).mean(1), np.ones(4) / 4, "same")
        return (np.argmax(e) + 0.5) * hop / SR
    return 0.0


_band_cache = {}


def band(x, lo_hi, key=None):
    if key is not None and (key, lo_hi) in _band_cache:
        return _band_cache[(key, lo_hi)]
    lo, hi = lo_hi
    y = spec_filter(x, lambda f: ((f >= lo) & (f < hi)).astype(float))
    if key is not None:
        _band_cache[(key, lo_hi)] = y
    return y


def energy(xb, win):
    a, b = int(win[0] * SR), int(win[1] * SR)
    return float(np.mean(xb[a:b] ** 2))


def e_db(e):
    return 10 * np.log10(max(e, 1e-20))


def build(music, sfx, ref):
    """Place every cue with a calibrated gain. Returns (sfx buffer, per-cue report, K)."""
    refm = ref.mean(1, keepdims=True)
    K = np.mean([e_db(energy(music, w)) - e_db(energy(ref, w)) for w in MUSIC_ONLY])
    buf = np.zeros((N_OUT, 2))
    rep = []
    groups = {}
    for idx, (name, t, kind, bnd, win, pan, grp) in enumerate(CUES):
        clip = sfx[name]
        t0 = t - anchor(kind, clip)
        unit = np.zeros((N_OUT, 2))
        place(unit, clip, t0, 0.0, pan)
        ref_e = energy(band(refm, bnd, "ref"), win)
        target = ref_e * 10 ** (K / 10)
        present = energy(band(music + buf, bnd), win)          # our bed + SFX already placed
        own = energy(band(unit, bnd), win)
        need = target - present
        if need > 0 and own > 0:
            g = e_db(need) - e_db(own)
            status = "ok"
        else:
            g = e_db(present) - e_db(max(own, 1e-20)) - 12.0      # masked in the ref: keep it 12 dB under
            status = "masked"
        g = float(np.clip(g, -40.0, 12.0))
        rep.append(dict(i=idx, name=name, t=round(t, 3), start=round(t0, 4), band=bnd, win=win, group=grp,
                        ref_band_db=round(e_db(ref_e), 1), target_db=round(e_db(target), 1),
                        bed_db=round(e_db(present), 1), gain_raw_db=round(g, 1), status=status, pan=pan))
        if grp:
            groups.setdefault(grp, []).append(len(rep) - 1)
            continue                                   # group gains are settled below
        buf += unit * 10 ** (g / 20)
        rep[-1]["gain_db"] = round(g, 1)
    for grp, ids in groups.items():
        raw = np.array([rep[i]["gain_raw_db"] for i in ids])
        med = float(np.median(raw))
        for i in ids:
            g = float(np.clip(rep[i]["gain_raw_db"], med - GROUP_SPREAD_DB, med + GROUP_SPREAD_DB))
            name, t, kind, bnd, win, pan, _ = CUES[rep[i]["i"]]
            place(buf, sfx[name], rep[i]["start"], g, pan)
            rep[i]["gain_db"] = round(g, 1)
        print("group %-10s %2d cues, median gain %.1f dB (raw spread %.1f..%.1f)" % (grp, len(ids), med,
                                                                                    raw.min(), raw.max()))
    return buf, rep, K


def master(music, fx, label):
    """-14 LUFS, <= -1 dBTP. The ref's peak-to-loudness ratio is ~20 dB (TP -3.2 at -23.6 LUFS), ours must be
    13 dB, so transients have to lose ~6 dB. That is done on the SFX bus first (fast 1.5 ms look-ahead,
    15 ms release, so tick peaks are shaved without pumping the bed), then a gentle full-mix limiter."""
    i0, _ = lufs(music + fx)
    g = TARGET_LUFS - i0
    ceil = CEILING_DB - 0.3
    for _ in range(8):
        fxl = limiter(fx * 10 ** (g / 20), ceil - 0.7, look_ms=1.5, release_ms=15.0)
        x = limiter(music * 10 ** (g / 20) + fxl, ceil, look_ms=3.0, release_ms=60.0)
        i2, tp2 = lufs(x)
        if abs(i2 - TARGET_LUFS) < 0.1 and tp2 <= CEILING_DB:
            break
        g += TARGET_LUFS - i2
        if tp2 > CEILING_DB:
            ceil -= 0.3
    pre = music * 10 ** (g / 20) + fx * 10 ** (g / 20)
    gr = db(np.abs(pre).max()) - db(np.abs(x).max())
    print("%s: %.2f LUFS integrated, true peak %.2f dBTP, sample peak %.2f dBFS (pre-master %.1f LUFS, "
          "make-up %+.1f dB, peak reduction %.1f dB)" % (label, i2, tp2, db(np.abs(x).max()), i0, g, gr))
    return x, i2, tp2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rebuild", action="store_true")
    ap.add_argument("--stems", action="store_true")
    a = ap.parse_args()
    if a.rebuild or not os.path.exists(os.path.join(HERE, "music.wav")):
        import build_music
        build_music.main()
    if a.rebuild or not glob.glob(os.path.join(HERE, "sfx", "*.wav")):
        import sfx as sfxmod
        sfxmod.build_all()

    music, sr = read_wav(os.path.join(HERE, "music.wav"))
    assert sr == SR and len(music) == N_OUT, "music.wav must be exactly %d samples" % N_OUT
    music = music.astype(np.float64)
    ref_path = os.path.join(HERE, "..", "ref", "audio.wav")
    gains_path = os.path.join(HERE, "cue_gains.json")
    if os.path.exists(ref_path):                       # calibrate every cue against the reference (measurement only)
        ref, _ = read_wav(ref_path)
        fx, rep, K = build(music, load_sfx(), ref.astype(np.float64))
        print("K (our bed - ref bed, music-only windows) = %+.1f dB" % K)
        for r in rep:
            if not r["group"]:
                print("  %-14s t=%.3f  ref %6.1f dB -> target %6.1f over bed %6.1f : gain %+5.1f dB %s" % (
                    r["name"], r["t"], r["ref_band_db"], r["target_db"], r["bed_db"], r["gain_db"], r["status"]))
        json.dump(dict(note="Calibrated SFX gains saved from a run of mix.py with the reference audio present. "
                            "mix.py uses these when ref/audio.wav is absent.", K_db=round(K, 2),
                       cues=[dict(name=r["name"], start=r["start"], gain_db=r["gain_db"], pan=r["pan"]) for r in rep]),
                  open(gains_path, "w"), indent=1)
    else:                                              # no reference shipped: replay the saved calibration
        saved = json.load(open(gains_path))
        sfx, K = load_sfx(), saved["K_db"]
        fx = np.zeros((N_OUT, 2))
        rep = []
        for c in saved["cues"]:
            place(fx, sfx[c["name"]], c["start"], c["gain_db"], c["pan"])
            rep.append(dict(c, source="cue_gains.json"))
        print("no ref/audio.wav: placed %d cues from cue_gains.json" % len(rep))
    mix, I, TP = master(music, fx, "mix.wav")
    assert len(mix) == N_OUT
    write_wav(os.path.join(HERE, "mix.wav"), mix)
    json.dump(dict(lufs=round(I, 2), true_peak_dbtp=round(TP, 2), samples=N_OUT, sr=SR, K_db=round(K, 2),
                   music_source=dict(title="Voxscape", artist="Eugenio Mininni", site="Mixkit",
                                     url="https://assets.mixkit.co/music/571/571.mp3",
                                     listing="https://mixkit.co/free-stock-music/ambient/",
                                     license="Mixkit Stock Music Free License",
                                     license_url="https://mixkit.co/license/#musicFree",
                                     file="audio/src/mixkit-voxscape-571.mp3", checked="2026-09-27"),
                   cues=rep), open(os.path.join(HERE, "mix_report.json"), "w"), indent=1)
    if a.stems:
        os.makedirs(os.path.join(HERE, "stems"), exist_ok=True)
        write_wav(os.path.join(HERE, "stems", "music.wav"), music)
        write_wav(os.path.join(HERE, "stems", "sfx.wav"), fx)


if __name__ == "__main__":
    main()
