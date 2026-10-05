"""Shared helpers for the monkey example audio: I/O, ffmpeg, loudness, limiter, beat grid.

Only numpy + the stdlib `wave` module + ffmpeg (on PATH, or env FFMPEG) are used.
Raw decoding goes through a temp .wav and the limiter is numpy, so even a minimal ffmpeg build
(atempo / aresample / loudnorm / volume) is enough.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import tempfile
import wave

import numpy as np

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))

# ---- film timing (measured on ref/audio.wav by analyze.py -> analysis.json) ------------
FPS = 30
N_OUT = 364544                 # exactly the reference's sample count (7.5947 s at 48 kHz)
OUT_LEN = N_OUT / 48000.0
# The reference has no beat grid (ambient sub drone, no percussion). Its music accents are:
BASS_CHANGE_1 = 1.72           # sub note B1 -> A1 (step down), window-centre crossover
MORPH_HIT = 4.08               # sub note A1 -> D1 with a sub boom (onset 4.095), the landing-page morph
HI_DROP = 3.41                 # everything above ~150 Hz drops out 3.41-3.58, then swells into the morph
MUSIC_TAIL = 6.68              # highs stop; the sub decays to silence by ~7.52


# ---- ffmpeg --------------------------------------------------------------------------
def ff_bin():
    """env FFMPEG (path to the binary) wins, else `ffmpeg` on PATH."""
    ff = os.environ.get("FFMPEG") or shutil.which("ffmpeg")
    if not ff or not os.path.exists(ff):
        raise RuntimeError("ffmpeg not found: install it (brew install ffmpeg / apt install ffmpeg) or set FFMPEG=/path/to/ffmpeg")
    return os.path.abspath(ff)


def ffmpeg(args, capture=False, loglevel="error"):
    """Run ffmpeg. cwd = its own folder (some portable builds load their libraries from there); all paths are absolute."""
    ff = ff_bin()
    cmd = [ff, "-hide_banner", "-nostdin", "-loglevel", loglevel, "-y"] + args
    r = subprocess.run(cmd, cwd=os.path.dirname(ff), capture_output=True, text=True)
    if r.returncode != 0 and not capture:
        raise RuntimeError("ffmpeg failed: %s\n%s" % (" ".join(cmd), r.stderr[-2000:]))
    return r


def _tmp(suffix=".wav"):
    fd, p = tempfile.mkstemp(suffix=suffix, dir=os.environ.get("TMPDIR"))
    os.close(fd)
    return p


# ---- wav I/O -------------------------------------------------------------------------
def read_wav(path):
    w = wave.open(path)
    ch, sw, sr, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
    raw = w.readframes(n)
    w.close()
    if sw == 2:
        x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
    elif sw == 3:
        b = np.frombuffer(raw, np.uint8).reshape(-1, 3)
        i = (b[:, 0].astype(np.int32) | (b[:, 1].astype(np.int32) << 8) | (b[:, 2].astype(np.int32) << 16))
        i = np.where(i >= 1 << 23, i - (1 << 24), i)
        x = i.astype(np.float32) / (1 << 23)
    else:
        raise ValueError("unsupported sample width %d" % sw)
    return x.reshape(-1, ch), sr


def write_wav(path, x, sr=SR, bits=24):
    """Write float audio (n, ch) or (n,) to PCM wav. 24-bit by default, TPDF-dithered at 16."""
    x = np.asarray(x, np.float64)
    if x.ndim == 1:
        x = x[:, None]
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    w = wave.open(path, "wb")
    w.setnchannels(x.shape[1])
    w.setframerate(sr)
    if bits == 16:
        rng = np.random.default_rng(0)
        d = (rng.random(x.shape) - rng.random(x.shape)) / 32768.0
        q = np.clip(np.round((x + d) * 32767), -32768, 32767).astype("<i2")
        w.setsampwidth(2)
        w.writeframes(q.tobytes())
    else:
        q = np.clip(np.round(x * 8388607), -8388608, 8388607).astype(np.int32)
        b = np.empty((q.size, 3), np.uint8)
        f = q.reshape(-1)
        b[:, 0] = f & 255
        b[:, 1] = (f >> 8) & 255
        b[:, 2] = (f >> 16) & 255
        w.setsampwidth(3)
        w.writeframes(b.tobytes())
    w.close()


def load_any(path, sr=SR, ch=2, af=None):
    """Decode any file ffmpeg can read to float (n, ch) at `sr`, optionally through a filter chain."""
    tmp = _tmp()
    try:
        args = ["-i", os.path.abspath(path)]
        if af:
            args += ["-af", af]
        args += ["-ac", str(ch), "-ar", str(sr), "-c:a", "pcm_s16le", tmp]
        ffmpeg(args)
        x, _ = read_wav(tmp)
    finally:
        os.remove(tmp)
    return x


def stretch(x, factor, sr=SR):
    """Time-stretch by `factor` (>1 = faster/shorter) with ffmpeg atempo, pitch preserved."""
    tin, tout = _tmp(), _tmp()
    try:
        write_wav(tin, x, sr, bits=24)
        ffmpeg(["-i", tin, "-af", "atempo=%.6f" % factor, "-c:a", "pcm_s24le", tout])
        y, _ = read_wav(tout)
    finally:
        os.remove(tin)
        os.remove(tout)
    return y


# ---- loudness + dynamics -------------------------------------------------------------
def lufs(x, sr=SR):
    """Integrated loudness + true peak via ffmpeg loudnorm (EBU R128 measurement pass)."""
    tmp = _tmp()
    try:
        write_wav(tmp, x, sr, bits=24)
        r = ffmpeg(["-i", tmp, "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"], capture=True,
                   loglevel="info")
    finally:
        os.remove(tmp)
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    if not m:
        raise RuntimeError("loudnorm gave no json:\n" + r.stderr[-1500:])
    j = json.loads(m.group(0))
    return float(j["input_i"]), float(j["input_tp"])


def db(v):
    return 20 * np.log10(max(float(v), 1e-12))


def rms_db(x):
    return db(np.sqrt(np.mean(np.square(x))) if len(x) else 0)


def _running_min(g, w):
    """Sliding-window minimum (window w, centred at the window end), van Herk/Gil-Werman."""
    n = len(g)
    pad = (-n) % w
    gp = np.concatenate([g, np.ones(pad + w)])
    blocks = gp.reshape(-1, w)
    pre = np.minimum.accumulate(blocks, axis=1).reshape(-1)
    suf = np.minimum.accumulate(blocks[:, ::-1], axis=1)[:, ::-1].reshape(-1)
    idx = np.arange(n)
    # window [i, i+w-1]
    return np.minimum(suf[idx], pre[idx + w - 1])


def limiter(x, ceiling_db=-1.0, look_ms=3.0, release_ms=80.0, sr=SR):
    """Look-ahead brick-wall peak limiter (4x-oversampled peak estimate). Returns limited audio."""
    x = np.asarray(x, np.float64)
    ceil = 10 ** (ceiling_db / 20)
    # cheap inter-sample peak estimate: max of |x| and |midpoint of neighbours|*1.0 (linear) and a
    # 4-tap band-limited midpoint which approximates 2x oversampling
    pk = np.max(np.abs(x), axis=1)
    mid = np.abs(0.5625 * (x[1:-2] + x[2:-1]) - 0.0625 * (x[:-3] + x[3:])).max(axis=1)
    pk[2:-1] = np.maximum(pk[2:-1], mid)
    req = np.minimum(1.0, ceil / np.maximum(pk, 1e-12))
    if req.min() >= 1.0:
        return x
    L = max(1, int(sr * look_ms / 1000))
    g = _running_min(req, 2 * L)                   # min over [i, i+2L)
    k = np.ones(L) / L                              # smooth attack; stays under the min window
    g = np.convolve(np.concatenate([g, np.ones(L)]), k, "full")[L:L + len(g)]
    g = np.minimum(g, _running_min(req, 2 * L))
    # release: one-pole return to 1 (loop on a decimated grid for speed, then interpolate)
    dec = 16
    gd = g[::dec].copy()
    a = np.exp(-1.0 / (release_ms / 1000 * sr / dec))
    out = np.empty_like(gd)
    cur = 1.0
    for i, v in enumerate(gd):
        cur = v if v < cur else v + (cur - v) * a
        out[i] = cur
    gr = np.interp(np.arange(len(g)), np.arange(len(g))[::dec], out)
    g = np.minimum(g, gr)
    y = x * g[:, None]
    return np.clip(y, -ceil, ceil)


def fade(n, kind="in", shape="cos"):
    t = np.linspace(0, 1, max(n, 1))
    f = np.sin(t * np.pi / 2) ** 2 if shape == "cos" else t
    return f if kind == "in" else f[::-1]


def place(buf, clip, t, gain_db=0.0, pan=0.0, sr=SR):
    """Add `clip` (n, 2) into `buf` at time t with gain and constant-power pan (-1..1)."""
    if clip.ndim == 1:
        clip = np.stack([clip, clip], 1)
    g = 10 ** (gain_db / 20)
    th = (pan + 1) * np.pi / 4
    lr = np.array([np.cos(th), np.sin(th)]) * np.sqrt(2)
    i0 = int(round(t * sr))
    s0 = max(0, -i0)
    i0 = max(0, i0)
    n = min(len(clip) - s0, len(buf) - i0)
    if n > 0:
        buf[i0:i0 + n] += clip[s0:s0 + n] * g * lr[None, :]


def spec_filter(x, gain_fn, sr=SR):
    """Zero-phase FFT filter: multiply the spectrum of x (n, ch) by gain_fn(freqs_hz)."""
    x = np.asarray(x, np.float64)
    n = len(x)
    nf = 1 << int(np.ceil(np.log2(max(n, 2) + 4096)))
    X = np.fft.rfft(x, nf, axis=0)
    g = gain_fn(np.fft.rfftfreq(nf, 1 / sr))
    return np.fft.irfft(X * g[:, None], nf, axis=0)[:n]


def lowpass_gain(fc, order=2):
    return lambda f: 1.0 / np.sqrt(1.0 + (f / fc) ** (2 * order))


def highpass_gain(fc, order=2):
    return lambda f: 1.0 / np.sqrt(1.0 + (fc / np.maximum(f, 1e-3)) ** (2 * order))
