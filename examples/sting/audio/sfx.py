#!/usr/bin/env python3
"""Synthesise every SFX for the pyramids sting into audio/sfx/*.wav (48 kHz stereo 24-bit, peak -1 dBFS).

Pure numpy, deterministic (fixed seeds), no downloads. Helpers copied from ../x3d/audio/sfx.py.
Pitched elements use D#-minor pentatonic pitches (D#, F#, G#, A#, C#) so they sit in the key of the bed
(Mixkit "Rising Forest", chroma-estimated D# minor / F# major).
Every transient sound starts its attack at sample 0, so placing a clip at time t puts its onset at t.
Whooshes are built as (pre, post): the envelope peak is at sample int(pre*SR), and mix.py places them so
that peak lands on the cut.
Levels in the film are set by the cue table in mix.py, not here.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audiolib import HERE, SR, write_wav  # noqa: E402

OUT = os.path.join(HERE, "sfx")
PENTA = [622.25, 739.99, 830.61, 932.33, 1108.73]          # D#5 F#5 G#5 A#5 C#6


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
        # frame i is shaped by centre/amp evaluated at i/SR but its window centre sits n/2 later;
        # drop the first n/2 samples so the envelope lands at the time it was asked for
        chans.append(y[n // 2:n // 2 + int(dur * SR)])
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


# ---- sounds ---------------------------------------------------------------------------
def click(seed=1, body=2300.0, snap=6200.0, dur=0.06):
    """Trackpad/UI click: contact transient + plastic body, soft release click 22 ms later."""
    t = tt(dur)
    y = 0.8 * bandnoise(len(t), 1800, 7000, seed) * np.exp(-t / 0.0008)
    y += 0.55 * np.sin(2 * np.pi * body * t) * np.exp(-t / 0.004)
    y += 0.35 * np.sin(2 * np.pi * snap * t) * np.exp(-t / 0.0018)
    r = int(0.022 * SR)
    y2 = np.zeros_like(y)
    y2[r:] = 0.18 * y[:len(y) - r]
    return norm(y + y2)


def tick(seed, f=3600.0):
    """Very light key tick (laptop key)."""
    t = tt(0.025)
    y = 0.7 * bandnoise(len(t), 1500, 6500, seed) * np.exp(-t / 0.0006)
    y += 0.35 * np.sin(2 * np.pi * f * t) * np.exp(-t / 0.0018)
    y += 0.12 * np.sin(2 * np.pi * 700 * t) * np.exp(-t / 0.003)
    return norm(y)


def soft_impact(dur=1.6):
    """Opening impact, soft: rounded sub drop + warm body + airy tail, no crunch."""
    t = tt(dur)
    sub = sine_glide(t, 62, 34, 0.10) * env_ad(t, 0.003, 0.34)
    body = shaped_noise(dur, lambda tc: 160 + 320 * np.exp(-tc / 0.06), lambda tc: 1.3,
                        lambda tc: np.exp(-tc / 0.12), 11)
    snapn = bandnoise(len(t), 1200, 6000, 12) * np.exp(-t / 0.004)
    air = shaped_noise(dur, lambda tc: 4200 * np.exp(-tc / 1.0) + 1500, lambda tc: 1.6,
                       lambda tc: np.exp(-tc / 0.45) * min(1.0, tc / 0.03), 13)
    y = np.stack([sub, sub], 1) + 0.45 * body / np.abs(body).max() + 0.28 * np.stack([snapn, snapn], 1) \
        + 0.22 * air / np.abs(air).max()
    y *= np.minimum(1, (dur - t) / 0.25)[:, None]
    return norm(y)


def air_whoosh(pre, post, f0, f1, f2, seed, pan_from=-0.4, pan_to=0.4, bw=1.5, curve=2.4):
    """Airy whoosh that swells for `pre` s (accelerating) to a peak, then falls away over `post` s.
    Centre frequency sweeps f0 -> f1 at the peak -> f2. Peak sample = int(pre*SR)."""
    dur = pre + post

    def centre(tc):
        return f0 * (f1 / f0) ** min(tc / pre, 1) if tc < pre else f1 * (f2 / f1) ** ((tc - pre) / post)

    def amp(tc):
        return (tc / pre) ** curve if tc < pre else np.exp(-(tc - pre) / post * 5)

    y = shaped_noise(dur, centre, lambda tc: bw, amp, seed, n=512, hop=64)
    t = tt(dur)
    y = y[:len(t)]
    p = np.interp(t, [0, dur], [pan_from, pan_to])
    th = (p + 1) * np.pi / 4
    y = y * np.stack([np.cos(th), np.sin(th)], 1) * np.sqrt(2)
    y[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))[:, None]
    return norm(y)


def transition_hit(seed=301, tone=None):
    """Off-grid transition hit: tight sub thump + bright snap + short airy tail + a quiet pitched ping.
    Attack at sample 0."""
    dur = 0.9
    t = tt(dur)
    sub = sine_glide(t, 105, 46, 0.035) * env_ad(t, 0.0015, 0.12)
    snapn = bandnoise(len(t), 1800, 11000, seed) * np.exp(-t / 0.006)
    body = bandnoise(len(t), 200, 1400, seed + 1) * np.exp(-t / 0.03)
    tail = shaped_noise(dur, lambda tc: 5200 * np.exp(-tc / 0.5) + 1800, lambda tc: 1.2,
                        lambda tc: np.exp(-tc / 0.16), seed + 2)
    y = np.stack([sub, sub], 1) + 0.55 * np.stack([snapn, snapn], 1) + 0.25 * np.stack([body, body], 1) \
        + 0.22 * tail / np.abs(tail).max()
    if tone:
        ping = sum(bell(t, f, decay=0.35, bright=0.5) for f in tone) / len(tone)
        y += 0.18 * np.stack([ping, ping], 1)
    y *= np.minimum(1, (dur - t) / 0.15)[:, None]
    return norm(y)


def shimmer(dur=1.9, seed=61, grains=40):
    """Soft shimmer for the end wordmark: high D#-minor-pentatonic grains + air + a soft bell chord.
    4 ms attack starting at sample 0 (the bell chord leads)."""
    rng = np.random.default_rng(seed)
    t = tt(dur)
    out = np.zeros((len(t), 2))
    notes = [f * m for f in PENTA for m in (2, 4, 8) if 1800 < f * m < 9500]
    for i in range(grains):
        st = rng.exponential(0.35)
        if st > dur - 0.2:
            continue
        ln = rng.uniform(0.08, 0.25)
        tb = tt(min(ln, dur - st))
        f = rng.choice(notes) * (1 + 0.01 * np.sin(2 * np.pi * rng.uniform(6, 10) * tb))
        g = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tb / tb[-1]) ** 2
        a = rng.uniform(0.3, 1.0) * np.exp(-st / 0.8)
        i0 = int(st * SR)
        out[i0:i0 + len(g)] += pan2(g * a, rng.uniform(-0.7, 0.7))
    out *= 0.5 / max(np.abs(out).max(), 1e-9)
    chord = sum(bell(t, f, decay=0.9, bright=0.5) for f in (PENTA[0] * 2, PENTA[1] * 2, PENTA[3] * 2)) / 3
    out += np.stack([chord, chord], 1) / np.abs(chord).max()          # the bell chord is the onset, at sample 0
    air = shaped_noise(dur, lambda tc: 7500, lambda tc: 0.8, lambda tc: np.exp(-tc / 0.6), seed + 7)
    out += 0.18 * air / np.abs(air).max()
    out *= np.minimum(1, t / 0.004)[:, None]
    out *= np.minimum(1, (dur - t) / 0.4)[:, None]
    return norm(out)


# whoosh designs, (name, pre, post, f0, f1, f2, seed, pan_from, pan_to, bw, curve)
WHOOSHES = {
    "whoosh_drop": (0.62, 0.10, 400, 7200, 3000, 401, -0.5, 0.5, 1.6, 2.8),    # into f72, the drop
    "whoosh_menu": (0.34, 0.09, 700, 6000, 2500, 402, 0.4, -0.4, 1.4, 2.2),     # into f101
    "whoosh_whip": (0.55, 0.08, 500, 8000, 3200, 403, 0.3, -0.3, 1.5, 3.2),     # into f159 (whip-tilt up)
    "whoosh_end": (0.48, 0.12, 450, 6500, 2600, 404, -0.3, 0.3, 1.6, 2.6),      # into f301, end card
}


def build_all():
    os.makedirs(OUT, exist_ok=True)
    sounds = {
        "soft_impact": soft_impact(),
        "click_a": click(1),
        "click_b": click(2, body=2600, snap=5900),
        "hit_a": transition_hit(301, tone=(PENTA[0] * 2, PENTA[3] * 2)),
        "hit_b": transition_hit(311, tone=(PENTA[1] * 2, PENTA[4] * 2)),
        "shimmer": shimmer(),
    }
    for name, a in WHOOSHES.items():
        sounds[name] = air_whoosh(*a[:5], seed=a[5], pan_from=a[6], pan_to=a[7], bw=a[8], curve=a[9])
    for i in range(6):
        sounds["tick%d" % (i + 1)] = tick(100 + i, f=[3400, 3700, 3900, 3550, 4100, 3300][i])
    for name, x in sounds.items():
        write_wav(os.path.join(OUT, name + ".wav"), x)
    return sorted(sounds)


if __name__ == "__main__":
    names = build_all()
    print("wrote %d sfx to %s: %s" % (len(names), OUT, ", ".join(names)))
