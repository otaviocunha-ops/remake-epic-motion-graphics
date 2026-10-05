#!/usr/bin/env python3
"""NEEDS ref/audio.wav (not shipped).
Measure mix.wav against ref/audio.wav with the same detectors analyze.py uses. Numbers only - no one
has listened. Writes the results into mix_report.json["verify"] and prints them.

  1. format: samples / rate / channels, LUFS, true peak
  2. hit alignment: every ref onset (per band, >= 1.5x threshold) matched to our nearest onset in the
     same band within +-60 ms; median / max |dt|, and the misses
  3. envelope match: RMS per 0.25 s and >2.5 kHz envelope per 50 ms, ours vs ref shifted by the
     integrated-loudness difference; correlation + worst blocks
"""
import json
import os
import sys
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import band_flux, peaks, stft  # noqa: E402
from audiolib import HERE, N_OUT, SR, highpass_gain, lufs, read_wav, spec_filter  # noqa: E402

BANDS = (("hi", 2500, 12000), ("mid", 300, 2500), ("sub", 20, 150))


def onsets(mono):
    S, f, t = stft(mono.astype(np.float32), 512, 120)
    out = {}
    for name, lo, hi in BANDS:
        d = band_flux(S, f, lo, hi)
        d2 = d - np.convolve(d, np.ones(80) / 80, "same")
        thr = np.percentile(d2, 97)
        out[name] = [(float(t[i]), float(d2[i] / thr)) for i in peaks(d2, t, thr, 0.03)]
    return out


def main():
    w = wave.open(os.path.join(HERE, "mix.wav"))
    fmt = dict(samples=w.getnframes(), sr=w.getframerate(), channels=w.getnchannels(), bits=8 * w.getsampwidth())
    w.close()
    mix, _ = read_wav(os.path.join(HERE, "mix.wav"))
    ref, _ = read_wav(os.path.join(HERE, "..", "ref", "audio.wav"))
    mix, ref = mix.astype(np.float64), ref.astype(np.float64)
    I, TP = lufs(mix)
    Ir, _ = lufs(ref)
    fmt.update(lufs=I, true_peak_dbtp=TP, ref_samples=len(ref), exact_length=(fmt["samples"] == len(ref) == N_OUT))
    print("format:", fmt)

    om, orf = onsets(mix.mean(1)), onsets(ref.mean(1))
    align = {}
    for name, _, _ in BANDS:
        ours = np.array([t for t, _ in om[name]])
        rows, miss = [], []
        for t, s in orf[name]:
            if s < 1.5:
                continue
            j = np.argmin(np.abs(ours - t)) if len(ours) else None
            if j is not None and abs(ours[j] - t) <= 0.06:
                rows.append((round(t, 3), round(float(ours[j] - t) * 1000, 1), round(s, 1)))
            else:
                miss.append((round(t, 3), round(s, 1)))
        dts = np.abs([r[1] for r in rows]) if rows else np.array([0.0])
        align[name] = dict(matched=len(rows), missed=len(miss), median_abs_ms=round(float(np.median(dts)), 1),
                           max_abs_ms=round(float(dts.max()), 1), within_1_frame=int((dts <= 33.4).sum()),
                           hits=rows, misses=miss)
        print("%-3s ref onsets >=1.5x: %2d matched (median |dt| %4.1f ms, max %4.1f ms), %d missed %s" % (
            name, len(rows), align[name]["median_abs_ms"], align[name]["max_abs_ms"], len(miss), miss))

    off = I - Ir
    blk = int(0.25 * SR)
    nb = N_OUT // blk
    rm = 10 * np.log10(np.mean(mix[:nb * blk].reshape(nb, blk, 2) ** 2, axis=(1, 2)) + 1e-12)
    rr = 10 * np.log10(np.mean(ref[:nb * blk].reshape(nb, blk, 2) ** 2, axis=(1, 2)) + 1e-12) + off
    hm = spec_filter(mix.mean(1)[:, None], highpass_gain(2500, 4))[:, 0]
    hr = spec_filter(ref.mean(1)[:, None], highpass_gain(2500, 4))[:, 0]
    b5 = int(0.05 * SR)
    n5 = N_OUT // b5
    em = 10 * np.log10(np.mean(hm[:n5 * b5].reshape(n5, b5) ** 2, 1) + 1e-12)
    er = 10 * np.log10(np.mean(hr[:n5 * b5].reshape(n5, b5) ** 2, 1) + 1e-12) + off
    act = er > (er.max() - 45)
    env = dict(level_offset_db=round(off, 2),
               rms025_corr=round(float(np.corrcoef(rm, rr)[0, 1]), 3),
               rms025_mean_abs_db=round(float(np.mean(np.abs(rm - rr))), 1),
               rms025_rows=[(round(i * 0.25, 2), round(float(rr[i]), 1), round(float(rm[i]), 1)) for i in range(nb)],
               hi050_corr=round(float(np.corrcoef(em[act], er[act])[0, 1]), 3),
               hi050_worst=sorted([(round(i * 0.05, 2), round(float(em[i] - er[i]), 1)) for i in np.where(act)[0]],
                                  key=lambda r: -abs(r[1]))[:8])
    print("RMS/0.25 s: corr %.3f, mean |diff| %.1f dB (ref shifted %+.1f dB to our loudness)" % (
        env["rms025_corr"], env["rms025_mean_abs_db"], off))
    print("   t    ref  ours")
    for r in env["rms025_rows"]:
        print("  %5.2f %6.1f %6.1f" % r)
    print(">2.5 kHz env/50 ms: corr %.3f; worst blocks (t, ours-ref dB): %s" % (env["hi050_corr"], env["hi050_worst"]))

    p = os.path.join(HERE, "mix_report.json")
    rep = json.load(open(p))
    rep["verify"] = dict(format=fmt, alignment=align, envelope=env,
                         caveat="all numbers are measurements; nothing has been heard by ear")
    json.dump(rep, open(p, "w"), indent=1)
    print("wrote verify section to mix_report.json")


if __name__ == "__main__":
    main()
