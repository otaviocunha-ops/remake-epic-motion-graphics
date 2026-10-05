#!/usr/bin/env python3
"""Build audio/music.wav: Mixkit "Voxscape" (Eugenio Mininni) conformed to the reference's music map.

Source: https://assets.mixkit.co/music/571/571.mp3 (listed on https://mixkit.co/free-stock-music/ambient/),
Mixkit Stock Music Free License, https://mixkit.co/license/#musicFree. Nothing from ref/audio.wav is used.

Why this track: the reference bed is an ambient sub drone with no percussion (analysis.json: no beat grid,
flat sub envelope). Its only musical accents are two bass-note changes: a step down (B1 -> A1 at 1.72 s)
and a fall of a fifth onto the home note with a sub boom at the morph (A1 -> D1 at 4.08 s). Voxscape is a
slow ambient pad over sustained bass notes with the same shape in the same order: C -> Bb (a step down,
source 38.76 s) -> F (down a fourth to the home note, a fresh bass attack, source 47.30 s). No time-stretch is
needed (no grid); the conform is two cuts that land those two source bass changes on the ref's two:

  out 0.000-3.410   <- source 37.04-40.45   (C pad, then Bb enters at out 1.72 = source 38.76)
  out 3.410-7.595   <- source 46.66-50.84   (Bb continues, F attack lands at out 4.11 = source 47.36)
  The 3.41 splice sits inside the ref's own drop (everything above ~150 Hz cuts out 3.41-3.58), and is
  phase-aligned on the sub (+-8 ms search) with a 60 ms equal-power crossfade.

Filter/level automation copied from the ref's band envelopes (analysis.json music_events):
  0.061        music starts (3 ms fade-in) with the opening hit (ref audio starts at 0.0607)
  2.40-2.78    anticipation lull: low-pass closes to 400 Hz, snaps open on the send click (2.778)
  3.41-3.58    DROP: low-pass 150 Hz (sub only)
  3.58-4.08    SWELL: low-pass sweeps 150 Hz -> open (log-exponential, u^3: ~560 Hz at 3.90), open on the hit
  6.62-6.70    highs stop: low-pass closes to 150 Hz
  6.65-7.53    sub decays on the ref's measured curve (-2 dB @6.9 ... -29 dB @7.5), silent from 7.53
Tone: +5 dB low shelf under 100 Hz and a gentle 3 kHz roll-off so the bed reads as the ref's dark sub
drone and leaves the top end to the SFX.
"""
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audiolib import (HERE, N_OUT, SR, db, highpass_gain, load_any, lowpass_gain, rms_db,  # noqa: E402
                      spec_filter, write_wav)

SRC_URL = "https://assets.mixkit.co/music/571/571.mp3"
SRC = os.path.join(HERE, "src", "mixkit-voxscape-571.mp3")

REF_CHANGE_1, SRC_CHANGE_1 = 1.72, 38.76     # bass step down (ref B1->A1, source C->Bb), note onsets
REF_MORPH = 4.08                             # ref A1->D1: D swells in from 3.96, sub boom onset 4.095, steepest
REF_F_ATTACK, SRC_MORPH = 4.11, 47.36        # rise 4.12-4.14; our F attack (0.1 s probe, verify_music.py) goes here
SPLICE = 3.41                                # inside the ref's hi drop
MUSIC_START = 0.061                          # ref: first sample above -80 dBFS at 0.0607, full level by 0.064
TAIL = [(6.65, 0.0), (6.90, -2.0), (7.00, -3.5), (7.20, -7.6), (7.30, -10.7), (7.40, -16.4), (7.50, -29.0),
        (7.53, -60.0)]
BANK = [150, 212, 300, 400, 600, 850, 1200, 1700, 2400, 3400, 4800, 6800, 9600, 13500, 24000]


def ensure_source():
    if not os.path.exists(SRC):
        os.makedirs(os.path.dirname(SRC), exist_ok=True)
        subprocess.run(["curl", "-sSL", "-o", SRC, SRC_URL], check=True)
    return SRC


def tone(x):
    shelf = lambda f: 1 + (10 ** (5 / 20) - 1) / (1 + (f / 100.0) ** 4)          # noqa: E731  +5 dB < 100 Hz
    return spec_filter(x, lambda f: shelf(f) * lowpass_gain(3000, 1)(f) * highpass_gain(28, 2)(f))


def fc_curve(t):
    """Low-pass cutoff (Hz) over time; 24000 = open."""
    fc = np.full(len(t), 24000.0)
    lull = (t >= 2.40) & (t < 2.778)
    fc[lull] = np.exp(np.interp(t[lull], [2.40, 2.50], [np.log(24000), np.log(400)]))
    fc[(t >= SPLICE) & (t < 3.58)] = 150.0
    sw = (t >= 3.58) & (t < REF_MORPH)
    u = (t[sw] - 3.58) / (REF_MORPH - 3.58)
    fc[sw] = 150.0 * (24000 / 150.0) ** (u ** 3.0)       # ref mids stay down until ~3.9, highs are SFX
    end = t >= 6.62
    fc[end] = np.exp(np.interp(t[end], [6.62, 6.70], [np.log(24000), np.log(150)]))
    return fc


def tv_lowpass(x, fc):
    """Time-varying zero-phase low-pass: crossfade between a bank of fixed zero-phase low-passes
    (sample-accurate, so the 3.41 drop is as sharp as the ref's)."""
    lf = np.log(np.clip(fc, BANK[0], BANK[-1]))
    lb = np.log(np.array(BANK, float))
    pos = np.interp(lf, lb, np.arange(len(BANK)))
    out = np.zeros_like(x)
    for i, c in enumerate(BANK):
        w = np.clip(1 - np.abs(pos - i), 0, 1)
        if not w.any():
            continue
        y = x if c >= 24000 else spec_filter(x, lowpass_gain(c, 4))
        out += y * w[:, None]
    return out


def main():
    ensure_source()
    src = load_any(SRC, sr=SR, ch=2).astype(np.float64)
    src -= src.mean(0)
    dA = SRC_CHANGE_1 - REF_CHANGE_1                  # 37.04
    dC = SRC_MORPH - REF_F_ATTACK                     # 43.25

    # phase-align the splice on the sub band (both sides are the same Bb note)
    sub = spec_filter(src[int((dA + SPLICE - 0.2) * SR):int((dC + SPLICE + 0.3) * SR) + SR], lowpass_gain(150, 4))
    a0 = int(0.2 * SR)
    ref_blk = sub[a0:a0 + int(0.06 * SR)].mean(1)
    base_c = int((dC - dA) * SR) + a0
    best, best_k = -1e9, 0
    for k in range(-int(0.0086 * SR), int(0.0086 * SR) + 1, 4):   # +-half a period of Bb1 (58.3 Hz)
        c = sub[base_c + k:base_c + k + len(ref_blk)].mean(1)
        v = float(np.dot(ref_blk, c))
        if v > best:
            best, best_k = v, k
    dC_adj = dC + best_k / SR
    print("splice phase alignment: %+.1f ms (F onset lands at %.3f s)" % (best_k / SR * 1000, SRC_MORPH - dC_adj))

    t = np.arange(N_OUT) / SR
    xf = int(0.06 * SR)
    sp = int(SPLICE * SR)
    A = src[int(round(dA * SR)):int(round(dA * SR)) + sp + xf // 2]
    C0 = int(round((dC_adj + SPLICE) * SR)) - xf // 2
    C = src[C0:C0 + (N_OUT - sp) + xf // 2]
    out = np.zeros((N_OUT, 2))
    ga = np.cos(np.linspace(0, np.pi / 2, xf))[:, None]
    gc = np.sin(np.linspace(0, np.pi / 2, xf))[:, None]
    out[:sp - xf // 2] = A[:sp - xf // 2]
    out[sp - xf // 2:sp + xf // 2] = A[sp - xf // 2:sp + xf // 2] * ga + C[:xf] * gc
    out[sp + xf // 2:] = C[xf:xf + N_OUT - (sp + xf // 2)]

    out = tone(out)
    out = tv_lowpass(out, fc_curve(t))

    # level automation
    g = np.interp(t, [a for a, _ in TAIL], [b for _, b in TAIL], left=0.0, right=-120.0)
    g += np.interp(t, [REF_MORPH + 0.05, 4.60], [0.0, -4.0])      # F section sits ~5.5 dB hotter than C/Bb in
    g += np.interp(t, [3.40, 3.43, 3.95, REF_MORPH], [0.0, -2.5, -2.5, 0.0])   # the drop: ref loses ~2.5 dB
    g = 10 ** (g / 20)                                           # the source; ref is only ~1-2 dB fuller (verify_mix)
    g *= np.clip((t - MUSIC_START) / 0.003, 0, 1)
    g[t >= TAIL[-1][0]] = 0.0
    out *= g[:, None]

    out *= 10 ** ((-20.0 - rms_db(out[int(0.5 * SR):int(3.4 * SR)])) / 20)   # bed at -20 dBFS RMS pre-mix
    write_wav(os.path.join(HERE, "music.wav"), out)
    secs = [("0.05-1.72 C", 0.05, 1.72), ("1.72-3.41 Bb", 1.72, 3.41), ("3.41-3.58 drop", 3.41, 3.58),
            ("3.58-4.08 swell", 3.58, 4.08), ("4.08-6.65 F", 4.08, 6.65), ("6.65-7.53 tail", 6.65, 7.53)]
    print("RMS:", {n: round(rms_db(out[int(a * SR):int(b * SR)]), 1) for n, a, b in secs},
          "| peak %.1f dBFS" % db(np.abs(out).max()))
    print("wrote music.wav (%.4f s, %d samples, 48 kHz stereo 24-bit)" % (len(out) / SR, len(out)))


if __name__ == "__main__":
    main()
