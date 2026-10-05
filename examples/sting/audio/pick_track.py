#!/usr/bin/env python3
"""Screen candidate Mixkit tracks (numbers only — nobody can listen here).

For each mp3 given on the command line: tempo (onset autocorrelation, 100-150 BPM window),
brightness (spectral centroid), low-end share, and the best "drop" moments: a bar boundary where
the next 2 bars are much louder (short-term RMS, dB) than the previous ~2.4 s and the low band jumps.
Usage: python3 pick_track.py DIR_WITH_MP3S > pick_report.txt
"""
import glob
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audiolib import load_any  # noqa: E402

SR = 22050
NFFT, HOP = 2048, 256


def stft_mag(x):
    w = np.hanning(NFFT)
    n = 1 + (len(x) - NFFT) // HOP
    idx = np.arange(NFFT)[None, :] + HOP * np.arange(n)[:, None]
    return np.abs(np.fft.rfft(x[idx] * w, axis=1))


def analyse(path):
    x = load_any(path, sr=SR, ch=1)[:, 0].astype(np.float64)
    M = stft_mag(x)
    f = np.fft.rfftfreq(NFFT, 1 / SR)
    fps = SR / HOP
    L = np.log1p(M * 10)
    flux = np.maximum(np.diff(L, axis=0), 0).sum(1)
    flux = np.maximum(flux - np.convolve(flux, np.ones(50) / 50, "same"), 0)
    # tempo: autocorrelation of onset envelope, 100-150 BPM
    e = flux - flux.mean()
    ac = np.correlate(e, e, "full")[len(e) - 1:]
    lags = np.arange(len(ac)) / fps
    bpms = 60 / np.maximum(lags, 1e-9)
    m = (bpms > 95) & (bpms < 155)
    i = np.argmax(ac[m])
    lag0 = np.where(m)[0][i]
    # parabolic refine
    y0, y1, y2 = ac[lag0 - 1], ac[lag0], ac[lag0 + 1]
    d = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2 + 1e-12)
    bpm = 60 / ((lag0 + d) / fps)
    conf = ac[lag0] / ac[0]
    cen = (M * f).sum(1) / (M.sum(1) + 1e-9)
    low = (M[:, f < 150] ** 2).sum(1)
    tot = (M ** 2).sum(1) + 1e-12
    # short-term level (0.25 s)
    hop_s = int(0.25 * SR)
    lv = np.array([20 * np.log10(np.sqrt(np.mean(x[j:j + hop_s] ** 2)) + 1e-9) for j in range(0, len(x) - hop_s, hop_s)])
    lowlv = np.array([10 * np.log10(low[int(j * fps * 0.25):int((j + 1) * fps * 0.25)].mean() + 1e-12)
                      for j in range(len(lv))])
    drops = []
    for j in range(10, len(lv) - 8):
        pre = lv[j - 10:j].mean()
        post = lv[j:j + 8].mean()
        lpre = lowlv[j - 10:j].mean()
        lpost = lowlv[j:j + 8].mean()
        drops.append((post - pre + 0.5 * (lpost - lpre), j * 0.25, post - pre, lpost - lpre, pre, post))
    drops.sort(reverse=True)
    picked = []
    for dd in drops:
        if all(abs(dd[1] - p[1]) > 4 for p in picked):
            picked.append(dd)
        if len(picked) == 3:
            break
    return dict(dur=len(x) / SR, bpm=bpm, conf=conf, centroid=float(np.median(cen)),
                low_share=float(low.sum() / tot.sum()), rms=float(np.median(lv)), drops=picked)


def main():
    d = sys.argv[1]
    for p in sorted(glob.glob(os.path.join(d, "*.mp3")), key=lambda s: int(os.path.basename(s)[:-4])):
        r = analyse(p)
        print("%-6s dur %5.1f  bpm %6.2f (ac %.2f)  centroid %5.0f Hz  low %.2f  med %.1f dB" % (
            os.path.basename(p), r["dur"], r["bpm"], r["conf"], r["centroid"], r["low_share"], r["rms"]))
        for sc, t, dl, dlow, pre, post in r["drops"]:
            print("        drop@%6.2f s  score %5.1f  level %+5.1f dB (%.1f -> %.1f)  low %+5.1f dB" % (
                t, sc, dl, pre, post, dlow))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
