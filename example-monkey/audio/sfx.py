#!/usr/bin/env python3
"""Synthesise every SFX for the monkey example into audio/sfx/*.wav (48 kHz stereo 24-bit, peak -1 dBFS).

Pure numpy, deterministic (fixed seeds), no downloads, nothing taken from the reference audio.
Pitched elements use F-major pitches
(F, A, C) because the music bed lands on F at the morph (Mixkit "Voxscape", C -> Bb -> F).
Each sound's spectral shape follows the measured ref event (analysis.json, sfx_hits); levels and times
are set by the cue table in mix.py, not here.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audiolib import HERE, SR, write_wav  # noqa: E402

OUT = os.path.join(HERE, "sfx")
F_MAJ = [349.23, 440.00, 523.25]                          # F4, A4, C5


def tt(dur):
    return np.arange(int(dur * SR)) / SR


def norm(x, peak_db=-1.0):
    x = np.asarray(x, np.float64)
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    p = np.abs(x).max()
    return x * (10 ** (peak_db / 20) / p) if p > 0 else x


def shaped_noise(dur, centre, bw_oct, amp, seed, stereo=True, n=1024, hop=256):
    """Noise through a time-varying log-gaussian band-pass. centre/bw_oct/amp are f(t) callables."""
    rng = np.random.default_rng(seed)
    N = int(dur * SR) + n
    f = np.fft.rfftfreq(n, 1 / SR)
    lf = np.log2(np.maximum(f, 1.0))
    w = np.hanning(n)
    chans = []
    for c in range(2 if stereo else 1):
        x = rng.standard_normal(N)
        y = np.zeros(N + n)
        norm_w = np.zeros(N + n)
        for i in range(0, N - n, hop):
            tc = i / SR
            spec = np.fft.rfft(x[i:i + n] * w)
            g = np.exp(-0.5 * ((lf - np.log2(centre(tc))) / max(bw_oct(tc), 0.05)) ** 2) * amp(tc)
            y[i:i + n] += np.fft.irfft(spec * g, n) * w
            norm_w[i:i + n] += w ** 2
        y = y[:N] / np.maximum(norm_w[:N], 1e-3)
        chans.append(y[:int(dur * SR)])
    out = np.stack(chans, 1) if stereo else chans[0]
    return out


def bandnoise(n, lo, hi, seed):
    """Static band-limited noise (FFT mask with soft 1-octave skirts), unit peak."""
    rng = np.random.default_rng(seed)
    X = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    lf = np.log2(np.maximum(f, 1.0))
    g = np.clip(1 - np.maximum(np.log2(lo) - lf, 0), 0, 1) * np.clip(1 - np.maximum(lf - np.log2(hi), 0), 0, 1)
    y = np.fft.irfft(X * g, n)
    return y / np.abs(y).max()


def env_ad(t, a, d):
    """Attack (linear, a s) then exponential decay (time-constant d s)."""
    return np.where(t < a, t / max(a, 1e-6), np.exp(-(t - a) / d))


def sine_glide(t, f0, f1, tau):
    """Sine whose frequency glides exponentially from f0 toward f1 with time-constant tau."""
    f = f1 + (f0 - f1) * np.exp(-t / tau)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def bell(t, f0, decay=0.9, bright=1.0):
    parts = [(1.0, 1.0, 1.0), (2.0, 0.45 * bright, 0.6), (2.76, 0.25 * bright, 0.45), (5.4, 0.12 * bright, 0.25)]
    y = np.zeros_like(t)
    for r, a, dm in parts:
        if f0 * r < SR / 2 - 1000:
            y += a * np.sin(2 * np.pi * f0 * r * t) * np.exp(-t / (decay * dm))
    return y * np.minimum(1, t / 0.002)


def pan2(x, p):
    th = (p + 1) * np.pi / 4
    return np.stack([x * np.cos(th), x * np.sin(th)], 1) * np.sqrt(2)




def whoosh(dur=0.45, f0=500, f1=3800, f2=1400, peak=0.6, seed=3, pan_from=-0.5, pan_to=0.5, bw=1.0):
    def centre(tc):
        u = tc / dur
        return f0 * (f1 / f0) ** (u / peak) if u < peak else f1 * (f2 / f1) ** ((u - peak) / (1 - peak))

    def amp(tc):
        u = tc / dur
        return (u / peak) ** 2 if u < peak else np.exp(-(u - peak) / (1 - peak) * 4)

    y = shaped_noise(dur, centre, lambda tc: bw, amp, seed)
    t = tt(dur)
    p = np.interp(t, [0, dur], [pan_from, pan_to])
    th = (p + 1) * np.pi / 4
    y = y * np.stack([np.cos(th), np.sin(th)], 1) * np.sqrt(2)
    return norm(y)


# ---- sounds (each names the ref event it is modelled on) -------------------------------
def tick(seed, f=3600.0, dur=0.035, body=0.35):
    """Keyboard tick. Ref typing ticks are bright (2.5-10 kHz) with a 1-2.5 kHz body; `body` scales the
    body (the 1.0-1.97 s run is fuller, 450 Hz thock included, than the 0.10-0.69 s run)."""
    t = tt(dur)
    y = 0.8 * bandnoise(len(t), 2500, 9000, seed) * np.exp(-t / 0.0007)
    y += 0.35 * np.sin(2 * np.pi * f * t) * np.exp(-t / 0.0025)
    y += body * (0.8 * bandnoise(len(t), 900, 2600, seed + 50) * np.exp(-t / 0.0015)
                 + 0.5 * np.sin(2 * np.pi * 1600 * t) * np.exp(-t / 0.003)
                 + 0.35 * np.sin(2 * np.pi * 450 * t) * env_ad(t, 0.0005, 0.005))
    return norm(y)


def soft_tick(seed, f=850.0, dur=0.05):
    """Softer text-reveal tick for the landing-page headline (ref body 800-900 Hz)."""
    t = tt(dur)
    y = 0.6 * np.sin(2 * np.pi * f * t) * env_ad(t, 0.0008, 0.007)
    y += 0.6 * bandnoise(len(t), 1500, 10000, seed) * np.exp(-t / 0.0008)   # ref 4.79 / 4.95: bright tops too
    return norm(y)


def open_hit(seed=301):
    """Film-open hit (ref 0.063: sub + mid + 5-10 kHz air at once): soft sub puff + air flick."""
    dur = 0.5
    t = tt(dur)
    sub = sine_glide(t, 90, 44, 0.04) * env_ad(t, 0.003, 0.09)
    air = shaped_noise(dur, lambda tc: 6500, lambda tc: 0.9, lambda tc: np.exp(-tc / 0.03) * min(1, tc / 0.002), seed)
    body = bandnoise(len(t), 400, 2500, seed + 1) * np.exp(-t / 0.012)
    y = 0.9 * np.stack([sub, sub], 1) + 0.6 * air / np.abs(air).max() + 0.25 * np.stack([body, body], 1)
    y *= np.minimum(1, (dur - t) / 0.05)[:, None]
    return norm(y)


def zoom_whoosh(dur=0.34, peak=0.55, f0=500, f1=6000, f2=1800, seed=311, pan_from=-0.25, pan_to=0.25, cut=None,
                snap=0.0):
    """Camera push/pull whoosh. The ref's are broadband (300 Hz-12 kHz, e.g. 1.35: mid 31 / hi 34 dB) with a
    fast rise; `snap` adds the short air transient the ref has right at the peak (hi onsets 2.183 / 3.305);
    `cut` (s) hard-stops the tail (the 3.30 pull-back ends in the 3.41 drop)."""
    w = whoosh(dur, f0, f1, f2, peak, seed, pan_from, pan_to, bw=1.6)
    t = tt(dur)
    tp = peak * dur
    low = sine_glide(t, 140, 70, 0.06) * np.exp(-np.abs(t - tp) / 0.06) * 0.25
    y = w + np.stack([low, low], 1)
    if snap:
        i0 = int((tp - 0.003) * SR)
        ts = tt(0.03)
        sn = bandnoise(len(ts), 2500, 11000, seed + 7) * env_ad(ts, 0.0015, 0.006) * snap
        y[i0:i0 + len(ts)] += np.stack([sn, sn], 1)
    if cut is not None:
        c0, c1 = int((cut - 0.008) * SR), int(cut * SR)
        y[c0:c1] *= np.linspace(1, 0, c1 - c0)[:, None]
        y[c1:] = 0
    return norm(y)


def button_click(seed=321):
    """Send-button press (ref 2.778: 463 Hz body, mid heavy) + release (ref 2.825, brighter 1.4 kHz)."""
    dur = 0.16
    t = tt(dur)
    press = 0.8 * np.sin(2 * np.pi * 460 * t) * env_ad(t, 0.0006, 0.010)
    press += 0.45 * bandnoise(len(t), 300, 1500, seed) * np.exp(-t / 0.0025)
    press += 0.25 * bandnoise(len(t), 2500, 7000, seed + 1) * np.exp(-t / 0.0006)
    rel = np.zeros_like(t)
    r = int(0.047 * SR)                                       # 2.825 - 2.778
    tr = t[:len(t) - r]
    rel[r:] = 0.65 * np.sin(2 * np.pi * 1400 * tr) * env_ad(tr, 0.0005, 0.006) \
        + 0.45 * bandnoise(len(tr), 1000, 5000, seed + 2) * np.exp(-tr / 0.0015)
    return norm(press + rel)


def morph_shimmer(dur=0.95, seed=331):
    """Glass -> page morph: air + F-major glass grains rising 3.58 -> 4.08 (0.50 s) then a bloom that
    fades by ~4.45 (ref >2.5 kHz rises -60 -> -30 dBFS, plateau to 4.3)."""
    rise = 0.50
    rng = np.random.default_rng(seed)
    t = tt(dur)

    def amp(tc):
        return (tc / rise) ** 2.2 if tc < rise else np.exp(-(tc - rise) / 0.16)

    air = shaped_noise(dur, lambda tc: 2500 * (4.0 ** min(tc / rise, 1.0)), lambda tc: 0.9, amp, seed)
    out = air / np.abs(air).max() * 0.55
    notes = [f * m for f in F_MAJ for m in (4, 8) if 1300 < f * m < 4500]
    for i in range(30):
        st = rise * (1 - rng.power(2.5)) if i < 18 else rise + rng.exponential(0.10)
        if st > dur - 0.05:
            continue
        ln = rng.uniform(0.05, 0.16)
        tb = tt(min(ln, dur - st))
        f = rng.choice(notes)
        g = np.sin(2 * np.pi * f * tb) * np.sin(np.pi * tb / tb[-1]) ** 2
        a = rng.uniform(0.3, 1.0) * float(amp(st + ln / 2)) ** 0.5
        i0 = int(st * SR)
        out[i0:i0 + len(g)] += pan2(g * a * 0.35, rng.uniform(-0.7, 0.7))
    ts = tt(0.12)                                             # start glint (ref hi onset 3.598)
    gl = bell(ts, 2793.83, decay=0.06, bright=0.3) * 0.06 + 0.04 * bandnoise(len(ts), 4000, 11000, seed + 3) \
        * np.exp(-ts / 0.003)
    i0 = int(0.018 * SR)
    out[i0:i0 + len(ts)] += np.stack([gl, gl], 1)
    out *= np.minimum(1, (dur - t) / 0.08)[:, None]
    return norm(out)


def sub_boom(seed=341):
    """Morph sub boom (ref sub onset 4.095, sub band +6 dB 4.05-4.15), tuned to the bed's F (43.65 Hz)."""
    dur = 0.9
    t = tt(dur)
    y = sine_glide(t, 66, 43.65, 0.05) * env_ad(t, 0.003, 0.28)
    y += 0.08 * bandnoise(len(t), 150, 900, seed) * np.exp(-t / 0.02)
    y *= np.minimum(1, (dur - t) / 0.15)
    return norm(y)


def low_pop(seed=351):
    """Soft rounded pop as the headline completes (ref 5.148: sub onset, 562 Hz body, no highs)."""
    dur = 0.2
    t = tt(dur)
    y = sine_glide(t, 380, 560, 0.01) * env_ad(t, 0.0015, 0.03)
    y += 0.8 * sine_glide(t, 120, 70, 0.03) * env_ad(t, 0.001, 0.05)
    return norm(y)


def settle_swell(dur=1.51, seed=361):
    """Pull-back air swell 5.30 -> 6.68 (ref >2.5 kHz rises -55 -> -26 dBFS, plateau ~6.0-6.5), then at 6.68
    the ref's highs drop ~18 dB at once and die out by 6.81: same here (file ends at 6.81)."""
    main = 1.38
    y = shaped_noise(dur, lambda tc: 3800 * (2.4 ** min(tc / 0.9, 1.0)), lambda tc: 0.6,
                     lambda tc: 10 ** ((-30 + 30 * min(tc / 0.85, 1.0) ** 0.8) / 20), seed)
    y = y / np.abs(y).max()
    t = tt(dur)
    g = np.where(t < main, 1.0, 0.12 * np.clip((dur - t) / (dur - main), 0, 1) ** 1.5)
    c = int(0.006 * SR)
    i0 = int(main * SR)
    g[i0 - c:i0] = np.linspace(1.0, 0.12, c)
    y *= g[:, None]
    y[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))[:, None]
    return norm(y)


def settle_tick(seed=371):
    """Soft landing as the card settles (ref 6.515-6.558: faint low + 10.9 kHz air)."""
    dur = 0.2
    t = tt(dur)
    y = 0.5 * sine_glide(t, 110, 60, 0.03) * env_ad(t, 0.004, 0.07)
    y += 0.5 * bandnoise(len(t), 7000, 14000, seed) * np.exp(-t / 0.004)
    y += 0.2 * bell(t, 1396.91 * 2, decay=0.06, bright=0.3)       # F6 glint, gone by ~6.68 like the ref's highs
    y *= np.minimum(1, (dur - t) / 0.03)
    return norm(y)


def build_all():
    os.makedirs(OUT, exist_ok=True)
    sounds = {
        "open_hit": open_hit(),
        "whoosh_push": zoom_whoosh(0.34, 0.60, 500, 6500, 2000, 311, -0.2, 0.2),            # rise ~200 ms
        "whoosh_cut": zoom_whoosh(0.60, 0.12, 700, 7500, 1500, 312, 0.2, -0.2, snap=2.0),             # rise ~70 ms, long tail
        "whoosh_pull": zoom_whoosh(0.30, 0.37, 450, 6000, 2000, 313, -0.1, 0.3, cut=0.211, snap=3.5),  # rise 110 ms, cut
        "button_click": button_click(),
        "morph_shimmer": morph_shimmer(),
        "sub_boom": sub_boom(),
        "low_pop": low_pop(),
        "settle_swell": settle_swell(),
        "settle_tick": settle_tick(),
    }
    for i in range(6):
        sounds["tick%d" % (i + 1)] = tick(100 + i, f=[3400, 3700, 3900, 3550, 4100, 3300][i], body=0.3)
        sounds["tickb%d" % (i + 1)] = tick(120 + i, f=[3300, 3600, 3800, 3450, 4000, 3200][i], body=0.9)
    for i in range(4):
        sounds["soft_tick%d" % (i + 1)] = soft_tick(200 + i, f=[820, 860, 900, 840][i])
    for name, x in sounds.items():
        write_wav(os.path.join(OUT, name + ".wav"), x)
    return sorted(sounds)


if __name__ == "__main__":
    names = build_all()
    print("wrote %d sfx to %s: %s" % (len(names), OUT, ", ".join(names)))
