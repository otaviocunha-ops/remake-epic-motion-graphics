#!/usr/bin/env python3
"""Measure ref/audio.wav (and the ref frames) for the monkey example. MEASUREMENT ONLY.

NEEDS ref/audio.wav (the reference soundtrack, not shipped). analysis.json from the original run is included,
so you only need this when you remake a different video.

Nothing from the reference ends up in any output file. Writes audio/analysis.json:
  tempo            beat-grid test (the ref has none: ambient sub drone, no percussion)
  loudness_025     RMS dBFS per 0.25 s, full + sub(<150) / mid(150-2500) / hi(>2500) bands
  bass_track       dominant sub note per 0.1 s, and the note-change times
  onsets           spectral-flux onsets per band (2.5 ms hop), strength x threshold
  ticks            typing-tick times (peak picking inside the typing windows)
  music_events     where the music swells / drops (from the band envelopes)
  sfx_hits         the curated hit list the mix uses (each one traced to a measured onset/envelope)
  visual           per-frame image difference peaks (ref/full, 30 fps) for cross-checking
    python3 analyze.py
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audiolib import HERE, SR, lufs, read_wav, spec_filter  # noqa: E402

REF = os.path.join(HERE, "..", "ref", "audio.wav")
FRAMES = os.path.join(HERE, "..", "ref", "full")
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def note(fr):
    m = int(round(69 + 12 * np.log2(fr / 440.0)))
    return "%s%d" % (NAMES[m % 12], m // 12 - 1)


def stft(mono, n, hop):
    nf = 1 + (len(mono) - n) // hop
    idx = np.arange(n)[None, :] + hop * np.arange(nf)[:, None]
    S = np.abs(np.fft.rfft(mono[idx] * np.hanning(n), axis=1))
    return S, np.fft.rfftfreq(n, 1 / SR), (np.arange(nf) * hop + n / 2) / SR


def band_flux(S, f, lo, hi):
    b = (f >= lo) & (f < hi)
    L = np.log1p(1000 * S[:, b])
    return np.concatenate([[0], np.maximum(0, np.diff(L, axis=0)).mean(1)])


def peaks(env, t, thr, min_gap, t0=0.0, t1=99.0):
    out, last = [], -9.0
    for i in range(1, len(env) - 1):
        if env[i] > thr and env[i] >= env[i - 1] and env[i] >= env[i + 1] and t0 <= t[i] < t1:
            if t[i] - last >= min_gap:
                out.append(i)
                last = t[i]
    return out


def tempo_test(env, fps):
    env = env - np.convolve(env, np.ones(64) / 64, "same")
    ac = np.correlate(env, env, "full")[len(env) - 1:]
    ac /= ac[0]
    lags = np.arange(len(ac)) / fps
    m = (lags > 60 / 200) & (lags < 60 / 60)
    i = np.argmax(ac[m])
    return float(60 / lags[m][i]), float(ac[m][i])


def main():
    x, sr = read_wav(REF)
    assert sr == SR
    x = x.astype(np.float64)
    mid = x.mean(1)
    n = len(x)
    rep = {"ref": "ref/audio.wav", "samples": n, "sr": SR, "duration_s": round(n / SR, 4)}
    I, TP = lufs(x)
    rep["ref_loudness"] = {"lufs_integrated": I, "true_peak_dbtp": TP,
                           "note": "our mix is normalised to -14 LUFS per the brief; the ref sits at %.1f" % I}

    # ---- tempo / beat grid ------------------------------------------------------------------
    S, f, t = stft(mid.astype(np.float32), 2048, 240)
    fps = SR / 240
    bpm, strength = tempo_test(band_flux(S, f, 20, 16000), fps)
    bpm_lo, strength_lo = tempo_test(band_flux(S, f, 20, 150), fps)
    rep["tempo"] = {"best_autocorr_bpm_fullband": round(bpm, 1), "autocorr_peak": round(strength, 3),
                    "best_autocorr_bpm_sub": round(bpm_lo, 1), "autocorr_peak_sub": round(strength_lo, 3),
                    "verdict": "no beat grid: the music is a sustained sub drone with no percussion; the sub band "
                               "envelope is flat (+-1 dB) from 0.05 to 6.6 s. Accents are bass-note changes, a sub "
                               "boom and filter drops/swells, listed in music_events."}

    # ---- loudness per 0.25 s --------------------------------------------------------------
    blk = int(0.25 * SR)
    nb = n // blk + (1 if n % blk else 0)
    Sb, fb, tb = stft(mid.astype(np.float32), 4096, 1200)          # 25 ms hop for band energies
    rows = []
    for i in range(nb):
        a, b = i * blk, min(n, (i + 1) * blk)
        full = 10 * np.log10(np.mean(x[a:b] ** 2) + 1e-12)
        m = (tb >= a / SR) & (tb < b / SR)
        E = (Sb[m] ** 2).mean(0) if m.any() else np.zeros(len(fb))
        tot = E.sum() + 1e-20
        bands = [10 * np.log10(E[(fb >= lo) & (fb < hi)].sum() / tot + 1e-12) for lo, hi in
                 ((20, 150), (150, 2500), (2500, 20000))]
        rows.append({"t": round(i * 0.25, 2), "rms_dbfs": round(full, 1), "sub_rel_db": round(bands[0], 1),
                     "mid_rel_db": round(bands[1], 1), "hi_rel_db": round(bands[2], 1)})
    rep["loudness_025"] = rows

    # ---- bass track -------------------------------------------------------------------------
    W = int(0.4 * SR)
    N = 1 << 17
    ff = np.fft.rfftfreq(N, 1 / SR)
    msk = (ff > 25) & (ff < 130)
    track = []
    for t0 in np.arange(0.0, n / SR - 0.4, 0.1):
        s = mid[int(t0 * SR):int(t0 * SR) + W] * np.hanning(W)
        F = np.abs(np.fft.rfft(s, N))
        fr = float(ff[msk][np.argmax(F[msk])])
        track.append({"t": round(t0 + 0.2, 2), "hz": round(fr, 1), "note": note(fr)})
    rep["bass_track"] = track

    def goertzel_cross(fa, fb_, t0, t1):
        """Time where tone fb_ overtakes tone fa (0.25 s windows, 10 ms hop)."""
        nn = int(0.25 * SR)
        tt = np.arange(nn) / SR
        w = np.hanning(nn)
        for tc in np.arange(t0, t1, 0.01):
            s = mid[int((tc - 0.125) * SR):int((tc - 0.125) * SR) + nn] * w
            A = abs(np.sum(s * np.exp(-2j * np.pi * fa * tt)))
            B = abs(np.sum(s * np.exp(-2j * np.pi * fb_ * tt)))
            if B > A:
                return round(float(tc), 2)
        return None

    rep["bass_changes"] = [
        {"t": goertzel_cross(61.7, 55.0, 1.2, 2.2), "from": "B1 61.7 Hz", "to": "A1 55.0 Hz"},
        {"t": goertzel_cross(55.0, 36.7, 3.6, 4.4), "from": "A1 55.0 Hz", "to": "D1 36.7 Hz (with sub boom)"},
    ]

    # ---- onsets per band (2.5 ms hop, 512-pt) ---------------------------------------------
    S2, f2, t2 = stft(mid.astype(np.float32), 512, 120)
    ons = {}
    for name, lo, hi in (("hi", 2500, 12000), ("mid", 300, 2500), ("sub", 20, 150)):
        d = band_flux(S2, f2, lo, hi)
        d2 = d - np.convolve(d, np.ones(80) / 80, "same")
        thr = np.percentile(d2, 97)
        ons[name] = [(round(float(t2[i]), 3), round(float(d2[i] / thr), 1)) for i in peaks(d2, t2, thr, 0.03)]
    rep["onsets"] = ons

    # ---- typing ticks: every local peak of the 2.5 ms band envelope that stands >= 6 dB over its +-50 ms
    # median, >= 12 ms apart, inside the typing windows. The ref typing is a dense texture (~27 ms median
    # gap in bursts), not one tick per character (the prompt types ~200 chars/s on screen).
    hop = int(0.0025 * SR)

    def dense_ticks(lo, hi, wins, thr=6.0):
        b_ = spec_filter(mid[:, None], lambda fq: ((fq > lo) & (fq < hi)).astype(float))[:, 0]
        k = len(b_) // hop
        env = 10 * np.log10((b_[:k * hop] ** 2).reshape(k, hop).mean(1) + 1e-12)
        te = (np.arange(k) + 0.5) * hop / SR
        base = np.array([np.median(env[max(0, i - 20):i + 20]) for i in range(k)])
        return [round(float(te[i]), 4) for a, z in wins for i in peaks(env - base, te, thr, 0.012, a, z)]

    ticks_prompt = dense_ticks(1000, 12000, [(0.10, 0.69), (1.00, 1.97)])
    ticks_head = dense_ticks(400, 2000, [(4.26, 5.12)])     # headline reveal: softer 800-900 Hz body
    gaps = np.diff(ticks_prompt)
    rep["ticks"] = {"prompt": ticks_prompt, "headline": ticks_head,
                    "prompt_median_gap_ms": round(float(np.median(gaps)) * 1000, 1),
                    "headline_median_gap_ms": round(float(np.median(np.diff(ticks_head))) * 1000, 1),
                    "note": "dense texture; prompt ticks bright (2.5-10 kHz), 1.0-1.97 run fuller; none between 0.69 and 1.00 s although the "
                            "text keeps typing on screen; headline ticks are softer mid-band (800-900 Hz) pops"}

    # ---- music events (from the band envelopes above; see loudness_025 and the 10 ms dump) ---
    rep["music_events"] = [
        {"t": 0.05, "what": "music + opening hit start together (onset 0.06 s in every band, 11-12x threshold)"},
        {"t": rep["bass_changes"][0]["t"], "what": "bass steps down B1 -> A1 (box has grown, typing continues)"},
        {"t": [2.45, 2.75], "what": "anticipation lull: everything but the sub drone drops to near silence "
                                    "until the send-button click"},
        {"t": [3.41, 3.58], "what": "DROP: all content above ~150 Hz cuts out (>2.5 kHz falls to -83 dBFS); "
                                    "only the sub drone remains"},
        {"t": [3.58, 4.08], "what": "SWELL: highs rise back (-60 -> -30 dBFS) into the morph"},
        {"t": rep["bass_changes"][1]["t"], "what": "MORPH HIT: new bass note D1 with a sub boom (sub +6 dB, "
                                                   "onset 4.095); music is ~1-2 dB fuller after this"},
        {"t": [5.30, 6.68], "what": "rising air swell under the pull-back, hard stop at 6.68"},
        {"t": [6.68, 7.52], "what": "tail: highs gone, sub drone decays ~-30 dB to silence by 7.52 "
                                    "(-2 dB @6.9, -3.5 @7.0, -7.6 @7.2, -10.7 @7.3, -16 @7.4, -29 @7.5)"},
    ]

    # ---- visual cross-check: per-frame difference (downscaled luma) --------------------------
    try:
        from PIL import Image
        prev, diffs = None, []
        for i in range(226):
            a = np.asarray(Image.open(os.path.join(FRAMES, "f%04d.jpg" % i)).convert("L").resize((192, 108)),
                           np.float32)
            if prev is not None:
                diffs.append(float(np.abs(a - prev).mean()))
            prev = a
        diffs = np.array(diffs)
        pk = [i + 1 for i in range(1, len(diffs) - 1) if diffs[i] > 12 and diffs[i] >= diffs[i - 1]
              and diffs[i] >= diffs[i + 1]]
        rep["visual"] = {"frame_diff_peaks": [{"frame": fr, "t": round(fr / 30, 3), "diff": round(float(diffs[fr - 1]), 1)}
                                              for fr in pk],
                         "key_frames": {"typing": "f4-f60 (0.13-2.00 s)", "zoom_flash": "f38 (1.267)",
                                        "cut_to_button": "f64 (2.133)", "button_press_flash": "f84 (2.800)",
                                        "pull_back_cut": "f97 (3.233)", "glass_morph": "f116-f130 (3.87-4.33)",
                                        "headline_typing": "f128-f156 (4.27-5.20)",
                                        "pull_back_to_card": "f160-f196 (5.33-6.53)", "static": "f196-f224"}}
    except Exception as e:                      # PIL missing: the audio analysis still stands
        rep["visual"] = {"error": str(e)}

    # ---- curated SFX hit list (what mix.py places; each traced to a measurement above) --------
    rep["sfx_hits"] = [
        {"t": 0.063, "sfx": "open hit", "evidence": "onset 0.06 in hi/mid/sub (strongest onset in the film)"},
        {"t": "prompt ticks", "sfx": "typing ticks", "evidence": "ticks.prompt (%d ticks)" % len(ticks_prompt)},
        {"t": 1.35, "sfx": "zoom whoosh (peak)", "evidence": ">2.5 kHz swell 1.30-1.45 peaking 1.35 (-20 dBFS); "
                                                           "visual zoom flash f38 = 1.267"},
        {"t": 2.18, "sfx": "zoom whoosh (peak)", "evidence": "hi onset 2.183 + swell 2.11-2.30; cut to the button f64 = 2.133"},
        {"t": 2.778, "sfx": "button click (press)", "evidence": "onset 2.778 (hi 4.3x, mid 4.0x), 463 Hz body; flash f84 = 2.800"},
        {"t": 2.825, "sfx": "button click (release)", "evidence": "onset 2.825, brighter (1.4 kHz)"},
        {"t": 3.30, "sfx": "pull-back whoosh (peak)", "evidence": "hi onset 3.305 (2.9x), swell 3.20-3.36; cut f97 = 3.233"},
        {"t": [3.58, 4.30], "sfx": "morph shimmer (rise then bloom)", "evidence": "hi rise 3.58-4.0, plateau to 4.3; morph f116-130"},
        {"t": 4.095, "sfx": "sub boom", "evidence": "sub onset 4.095 (3.1x), sub band +6 dB 4.05-4.15"},
        {"t": "headline ticks", "sfx": "soft ticks", "evidence": "ticks.headline (%d ticks)" % len(ticks_head)},
        {"t": 5.148, "sfx": "soft low pop (headline done)", "evidence": "sub onset 5.148 (6.8x), 562 Hz body"},
        {"t": [5.30, 6.68], "sfx": "settle air swell", "evidence": ">2.5 kHz rising -55 -> -26 dBFS, hard stop 6.68"},
        {"t": 6.545, "sfx": "soft settle tick", "evidence": "sub/mid onsets 6.515-6.558, air 10.9 kHz; card settles f196 = 6.53"},
    ]
    json.dump(rep, open(os.path.join(HERE, "analysis.json"), "w"), indent=1)
    print("ref %.4f s, %.2f LUFS, TP %.2f dBTP" % (n / SR, I, TP))
    print("tempo test: %.1f BPM (autocorr %.2f) full band, %.1f BPM (%.2f) sub -> %s" % (
        bpm, strength, bpm_lo, strength_lo, "no grid"))
    print("bass changes:", rep["bass_changes"])
    print("prompt ticks (%d, median gap %.0f ms):" % (len(ticks_prompt), rep["ticks"]["prompt_median_gap_ms"]),
          ticks_prompt)
    print("headline ticks (%d, median gap %.0f ms):" % (len(ticks_head), rep["ticks"]["headline_median_gap_ms"]),
          ticks_head)
    print("visual diff peaks:", rep["visual"].get("frame_diff_peaks"))
    print("wrote analysis.json")


if __name__ == "__main__":
    main()
