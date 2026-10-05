"""Shared helpers for the pyramids remake audio (copied from ../lordy/audio): I/O, ffmpeg, loudness, limiter, beat grid.

Only numpy + the stdlib `wave` module + Remotion's bundled (stripped) ffmpeg are used.
The bundled ffmpeg has atempo / aresample / loudnorm / volume, but no s16le muxer and no
limiter, so raw decoding goes through a temp .wav and the limiter is numpy.
"""
import glob
import json
import os, shutil
import re
import subprocess
import tempfile
import wave

import numpy as np

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))

# ---- film timing (from ../AUDIO.md + ../BEATS.md, measured on ref/audio.wav) -------------
FPS = 29.97
N_OUT = 579600                 # exactly 12.075 s at 48 kHz (the reference's length)
OUT_LEN = N_OUT / 48000.0
BPM = 124.0
BEAT = 60.0 / BPM              # 0.48387 s
GRID0 = 0.048                  # beat k at GRID0 + k*BEAT
DROP = 2.45                    # the drop (cut f72 at 2.402, ref kick 2.43-2.48, beat 5 = 2.467)


def beat_t(k):
    return GRID0 + k * BEAT


# ---- ffmpeg --------------------------------------------------------------------------
_FF_CANDIDATES = [
    os.environ.get("FFMPEG_DIR", ""),
    os.path.dirname(shutil.which("ffmpeg") or ""),
]


def ff_dir():
    for d in _FF_CANDIDATES:
        if d and os.path.exists(os.path.join(d, "ffmpeg")):
            return d
    raise RuntimeError("ffmpeg not found: install it (brew install ffmpeg) or set FFMPEG_DIR to the folder holding it")


def ffmpeg(args, capture=False, loglevel="error"):
    """Run the bundled ffmpeg with cwd = its folder (its dylibs load relative to cwd)."""
    cmd = ["./ffmpeg", "-hide_banner", "-nostdin", "-loglevel", loglevel, "-y"] + args
    r = subprocess.run(cmd, cwd=ff_dir(), capture_output=True, text=True)
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
    """Sliding-window minimum (window w, centred at the window end) — van Herk/Gil-Werman."""
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
