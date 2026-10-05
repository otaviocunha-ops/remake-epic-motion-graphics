#!/usr/bin/env python3
"""Measure mix.wav against the skeleton. Prints a table and writes work/verify.json.

1. format: rate, channels, samples, duration.
2. loudness: ffmpeg loudnorm (EBU R128) integrated LUFS + true peak, on the file as written.
3. SFX timing, two ways per cue:
   a) isolated: the cue re-rendered alone exactly as mix.py places it; "onset" cues = first sample whose
      1 ms peak envelope reaches 10 % of the cue's peak; "peak" cues (whooshes) = 10 ms RMS envelope peak.
   b) in the mix: for transient cues, the all-band spectral-flux local maximum of mix.wav nearest the target
      (+-40 ms, must stand >= 1.25x the median flux of +-0.5 s), frame time = window centre, 2.5 ms hop;
      prominence = that flux / the median. The 1024-pt window's centre convention reads a sharp onset
      ~2-4 ms early. "-" = no separable peak (masked).
4. music grid: all-band onset of each beat k5..k24 in the music stem vs 0.048 + k*0.48387.
"""
import json
import os
import sys
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audiolib import BEAT, GRID0, HERE, SR, lufs, place, read_wav  # noqa: E402
from mix import CUES, SFX, env_peak_index, key_ticks  # noqa: E402

WORK = os.path.join(HERE, "work")


def flux(m, nfft=1024, hop=120):
    n = 1 + (len(m) - nfft) // hop
    idx = np.arange(nfft)[None, :] + hop * np.arange(n)[:, None]
    M = np.abs(np.fft.rfft(m[idx] * np.hanning(nfft), axis=1))
    e = np.r_[0, np.maximum(np.diff(np.log1p(10 * M), axis=0), 0).sum(1)]
    return e, (np.arange(n) * hop + nfft / 2) / SR


def onset_10pct(x, lo, hi):
    a = np.abs(x).max(1)
    w = int(0.001 * SR)
    seg = a[lo:hi]
    pk = seg.max()
    i = int(np.argmax(seg >= 0.1 * pk))
    return lo + i


def main():
    w = wave.open(os.path.join(HERE, "mix.wav"))
    fmt = dict(rate=w.getframerate(), channels=w.getnchannels(), bits=8 * w.getsampwidth(), samples=w.getnframes(),
               seconds=w.getnframes() / w.getframerate())
    w.close()
    mix, _ = read_wav(os.path.join(HERE, "mix.wav"))
    mix = mix.astype(np.float64)
    I, TP = lufs(mix)
    sp = 20 * np.log10(np.abs(mix).max())
    tail = 20 * np.log10(np.sqrt(np.mean(mix[-int(0.5 * SR):-int(0.07 * SR)] ** 2)))
    print("format: %(rate)d Hz, %(channels)d ch, %(bits)d-bit, %(samples)d samples = %(seconds).4f s" % fmt)
    print("loudness: %.2f LUFS integrated, true peak %.2f dBTP, sample peak %.2f dBFS; RMS of 11.5-12.0 s %.1f dBFS"
          % (I, TP, sp, tail))

    ef, tf = flux(mix.mean(1))
    rows = []
    print("\n%-22s %-6s %9s %10s %8s %10s %8s %6s" % ("cue", "kind", "target", "isolated", "err ms", "in-mix", "err ms", "prom"))
    for name, f, t, g, pan, kind in CUES:
        clip, _ = read_wav(os.path.join(SFX, f + ".wav"))
        clip = clip.astype(np.float64)
        t0 = t - env_peak_index(clip) / SR if kind == "peak" else t
        buf = np.zeros_like(mix)
        place(buf, clip, t0, g, pan)
        if kind == "onset":
            iso = onset_10pct(buf, int((t - 0.05) * SR), int((t + 0.3) * SR)) / SR
        else:
            m = (buf ** 2).mean(1)
            k = int(0.010 * SR)
            iso = int(np.argmax(np.convolve(m, np.ones(k) / k, "same"))) / SR
        r = dict(cue=name, kind=kind, target=t, isolated=round(iso, 4), iso_err_ms=round((iso - t) * 1000, 1))
        if kind == "onset":
            ctx = (tf > t - 0.5) & (tf < t + 0.5)
            med = np.median(ef[ctx])
            # local maxima of the mix flux within +-40 ms that stand 1.25x above the local median;
            # take the one nearest the target (a louder music 16th can sit inside the window)
            idx = np.where((tf > t - 0.04) & (tf < t + 0.04))[0]
            pk = [i for i in idx if ef[i] >= ef[i - 1] and ef[i] >= ef[i + 1] and ef[i] >= 1.25 * med]
            if pk:
                j = min(pk, key=lambda i: abs(tf[i] - t))
                tm = tf[j]
                r.update(in_mix=round(float(tm), 4), mix_err_ms=round((tm - t) * 1000, 1),
                         prominence=round(float(ef[j] / med), 1))
            else:
                r.update(in_mix=None, mix_err_ms=None, prominence=None)
        rows.append(r)
        print("%-22s %-6s %9.3f %10.4f %+8.1f %10s %8s %6s" % (
            name, kind, t, iso, (iso - t) * 1000, "%.4f" % r["in_mix"] if r.get("in_mix") else "-",
            "%+.1f" % r["mix_err_ms"] if r.get("mix_err_ms") is not None else "-", r.get("prominence") or "-"))

    kt = key_ticks()
    times = np.array([a for a, *_ in kt])
    print("\nkey ticks: %d, first %.3f s, last %.3f s, mean spacing %.1f ms (min %.1f, max %.1f), gains %.1f..%.1f dB"
          % (len(kt), times[0], times[-1], np.diff(times).mean() * 1000, np.diff(times).min() * 1000,
             np.diff(times).max() * 1000, min(g for _, _, g, _ in kt), max(g for _, _, g, _ in kt)))

    mus, _ = read_wav(os.path.join(WORK, "music_stem.wav"))
    em, tm = flux(mus.mean(1).astype(np.float64), nfft=2048, hop=240)
    offs = []
    for k in range(5, 25):
        gk = GRID0 + k * BEAT
        win = (tm > gk - 0.07) & (tm < gk + 0.07)
        offs.append(float(tm[win][np.argmax(em[win])] - gk))
    offs = np.array(offs) * 1000
    lvl = lambda a, b: 20 * np.log10(np.sqrt(np.mean(mus[int(a * SR):int(b * SR)] ** 2)))  # noqa: E731
    print("music grid: beat-5 (drop) onset %.4f s (grid 2.467, brief 2.45); beats k6-k24 offset median %+.1f ms, "
          "mean |err| %.1f ms, max |err| %.1f ms" % (GRID0 + 5 * BEAT + offs[0] / 1000, np.median(offs[1:]),
                                                     np.abs(offs[1:]).mean(), np.abs(offs[1:]).max()))
    print("music RMS: intro 0.2-2.4 s %.1f dBFS, drop 2.5-3.5 s %.1f, body 3.5-10 s %.1f, end 10-12 s %.1f"
          % (lvl(0.2, 2.4), lvl(2.5, 3.5), lvl(3.5, 10), lvl(10, 12.0)))

    out = dict(format=fmt, lufs=I, true_peak_dbtp=TP, sample_peak_dbfs=sp, cues=rows,
               key_ticks=dict(n=len(kt), first=times[0], last=times[-1], mean_ms=float(np.diff(times).mean() * 1000)),
               music_grid_offsets_ms=[round(v, 1) for v in offs])
    with open(os.path.join(WORK, "verify.json"), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
