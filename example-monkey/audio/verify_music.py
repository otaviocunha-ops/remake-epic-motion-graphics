#!/usr/bin/env python3
"""Measure music.wav with the same probes analyze.py uses on the ref: bass-note crossovers, band envelope
around the drop/swell/tail. Prints ref vs ours."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audiolib import HERE, SR, highpass_gain, read_wav, spec_filter  # noqa: E402


def cross(x, fa, fb, t0, t1, W=0.25):
    nn = int(W * SR)
    tt = np.arange(nn) / SR
    w = np.hanning(nn)
    for tc in np.arange(t0, t1, 0.005):
        s = x[int((tc - W / 2) * SR):int((tc - W / 2) * SR) + nn] * w
        if abs(np.sum(s * np.exp(-2j * np.pi * fb * tt))) > abs(np.sum(s * np.exp(-2j * np.pi * fa * tt))):
            return round(float(tc), 3)


def onset(x, f, t0, t1, W=0.1):
    """Time the tone f rises through half its (t0..t1) max amplitude (note attack)."""
    nn = int(W * SR)
    tt = np.arange(nn) / SR
    w = np.hanning(nn)
    ts = np.arange(t0, t1, 0.005)
    a = np.array([abs(np.sum(x[int((tc - W / 2) * SR):int((tc - W / 2) * SR) + nn] * w * np.exp(-2j * np.pi * f * tt)))
                  for tc in ts])
    return round(float(ts[np.argmax(a > 0.5 * a.max())]), 3)


def hi_env(x, ts):
    h = spec_filter(x[:, None], highpass_gain(2500, 4))[:, 0]
    b = int(0.01 * SR)
    return [round(10 * np.log10(np.mean(h[int(t * SR):int(t * SR) + b] ** 2) + 1e-12), 1) for t in ts]


r, _ = read_wav(os.path.join(HERE, "..", "ref", "audio.wav"))
m, _ = read_wav(os.path.join(HERE, "music.wav"))
r, m = r.mean(1).astype(np.float64), m.mean(1).astype(np.float64)
print("samples: ref %d, music %d" % (len(r), len(m)))
print("bass change 1  ref B1->A1 crossover %.3f | ours C->Bb crossover %.3f (Bb 116.5 Hz attack %.3f)" % (
    cross(r, 61.7, 55.0, 1.2, 2.2), cross(m, 130.8, 116.5, 1.2, 2.2), onset(m, 116.5, 1.4, 2.1)))
print("morph change   ref A1->D1 crossover %.3f | ours Bb->F crossover %.3f (F 87.3 Hz attack %.3f)" % (
    cross(r, 55.0, 36.7, 3.6, 4.4), cross(m, 116.5, 87.3, 3.6, 4.4), onset(m, 87.3, 3.8, 4.5)))
ts = [3.30, 3.38, 3.43, 3.50, 3.57, 3.65, 3.75, 3.85, 3.95, 4.05, 4.15, 6.50, 6.62, 6.70, 6.80]
print("music-only >2.5k env dBFS at", ts)
print("   ours", hi_env(m, ts))
print("   (ref mix incl. SFX)", hi_env(r, ts))
blk = int(0.1 * SR)
e = lambda x, t: 10 * np.log10(np.mean(x[int(t * SR):int(t * SR) + blk] ** 2) + 1e-12)  # noqa: E731
for t in [6.6, 6.9, 7.0, 7.2, 7.3, 7.4, 7.45, 7.5]:
    print("tail %.2f  ref %.1f  ours %.1f dBFS" % (t, e(r, t), e(m, t)))
