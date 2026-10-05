#!/usr/bin/env python3
"""Build audio/music.wav: Mixkit "Rising Forest" (Diego Nava, House) conformed to the pyramids skeleton.

Source: https://assets.mixkit.co/music/471/471.mp3, Mixkit Stock Music Free License
(https://mixkit.co/license/#musicFree). Nothing from ref/audio.wav is used in the output; the reference is
only measured (in ../measure) to get the beat grid in BEATS.md, which is what this file aligns to.

Why this track (pick_track.py -> work/pick_report.txt): measured 124.008 BPM (kick-grid fit, beat 0.48384 s),
brightest centroid of the screened tracks (3.3 kHz), and a clean breakdown -> drop at source 46.444 s
(beats k82-94: bass out, hats/highs rising +5 dB = a build; k95: full band, +9 dB, low band +31 dB).

Conform (one continuous excerpt, no splices):
  1. atempo 124.0/124.008 (x0.999936) -> exactly 124 BPM.
  2. place the source drop downbeat (k95) on ref beat 5 (0.048 + 5*0.48387 = 2.467 s), then nudge so the
     median all-band onset of beats k6-k24 sits exactly on the ref grid (the grid in BEATS.md was measured
     the same way; the ref sits at -0.2 ms on it). The kick band alone was tried first and rejected: the
     ref's kick-band flux is too weak/noisy (peaks 0.8-4) to align against.
     The out window starts ~5 beats into the build, so 0-2.45 s is the soft rising intro.
  3. music fades in 0.090-0.110 s (ref is silent to 0.101, the opening impact), intro +2 dB so the
     intro->drop step is ~7 dB like the ref, gentle -2.5 dB over the end card 10.0-12.0 s,
     no fade at the end (the master adds 60 ms).
"""
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audiolib import BEAT, GRID0, HERE, N_OUT, SR, db, load_any, rms_db, stretch, write_wav  # noqa: E402

SRC_URL = "https://assets.mixkit.co/music/471/471.mp3"
SRC = os.path.join(HERE, "src", "mixkit-rising-forest-471.mp3")
SRC_BPM = 60.0 / 0.48384           # 124.0079, measured
SRC_DROP = 0.479 + 95 * 0.48384    # 46.444 s, source beat k95
TEMPO = 124.0 / SRC_BPM
T_DROP = GRID0 + 5 * BEAT          # 2.467 s = ref beat 5


def ensure_source():
    if not os.path.exists(SRC):
        os.makedirs(os.path.dirname(SRC), exist_ok=True)
        subprocess.run(["curl", "-sSL", "-o", SRC, SRC_URL], check=True)
    return SRC


def onset_env(m, sr=SR, nfft=2048, hop=240):
    """All-band log spectral-flux onset envelope (same method the ref grid was measured with),
    frame time = window centre."""
    n = 1 + (len(m) - nfft) // hop
    idx = np.arange(nfft)[None, :] + hop * np.arange(n)[:, None]
    M = np.abs(np.fft.rfft(m[idx] * np.hanning(nfft), axis=1))
    L = np.log1p(10 * M)
    e = np.r_[0, np.maximum(np.diff(L, axis=0), 0).sum(1)]
    e = np.maximum(e - np.convolve(e, np.ones(100) / 100, "same"), 0)
    return e, (np.arange(n) * hop + nfft / 2) / sr


def cut(src, t_drop):
    i0 = int(round((SRC_DROP / TEMPO - t_drop) * SR))
    return src[i0:i0 + N_OUT].copy()


def grid_offsets(m):
    """Per-beat offset (s) of the strongest onset within +-70 ms of ref beats k5..k24."""
    e, t = onset_env(m)
    out = []
    for k in range(5, 25):
        g = GRID0 + k * BEAT
        w = (t > g - 0.07) & (t < g + 0.07)
        out.append(t[w][np.argmax(e[w])] - g)
    return np.array(out)


def align_lag(src):
    """Shift that puts our post-drop beat onsets on the ref's measured grid (median over k6..k24).
    The ref itself sits at -0.2 ms median on that grid by the same measurement."""
    return -float(np.median(grid_offsets(cut(src, T_DROP).mean(1))[1:]))


def main():
    ensure_source()
    src = load_any(SRC, sr=SR, ch=2).astype(np.float64)
    src -= src.mean(0)
    src = stretch(src, TEMPO)
    lag = align_lag(src)
    t_drop = T_DROP + lag
    print("tempo factor %.6f (%.3f -> 124.000 BPM); grid nudge %+.1f ms -> drop at %.4f s"
          % (TEMPO, SRC_BPM, lag * 1000, t_drop))
    out = cut(src, t_drop)
    t = np.arange(N_OUT) / SR
    g = np.interp(t, [0, 2.30, 2.44], [2.0, 2.0, 0.0])               # intro lift (dB)
    g += np.interp(t, [10.0, 12.0], [0.0, -2.5])                      # end-card decline
    g = 10 ** (g / 20) * np.clip((t - 0.090) / 0.020, 0, 1)            # silent until the opening impact
    out *= g[:, None]
    out *= 10 ** ((-16.0 - rms_db(out[int(2.5 * SR):int(10 * SR)])) / 20)   # body at -16 dBFS RMS pre-master
    write_wav(os.path.join(HERE, "music.wav"), out)
    with open(os.path.join(HERE, "work", "music_drop.txt"), "w") as fh:
        fh.write("%.5f\n" % t_drop)
    print("intro RMS %.1f dB, body RMS %.1f dB, peak %.1f dBFS, %d samples"
          % (rms_db(out[int(0.2 * SR):int(2.4 * SR)]), rms_db(out[int(2.5 * SR):int(10 * SR)]),
             db(np.abs(out).max()), len(out)))


if __name__ == "__main__":
    main()
