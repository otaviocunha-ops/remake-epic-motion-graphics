#!/usr/bin/env python3
"""Mix music.wav + synthesized SFX into audio/mix.wav (48 kHz stereo 24-bit, exactly 12.075 s).

Master: one static gain + look-ahead limiter (ceiling -1.3 dBFS sample/ISP-estimate), iterated until
ffmpeg loudnorm (EBU R128) reads -14.0 LUFS integrated with true peak <= -1.0 dBTP; 60 ms fade at the end.
Also writes work/sfx_stem.wav and work/music_stem.wav (same master gain, pre-limiter) for verify.py,
and work/cues.json (every placed cue with its target time).
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audiolib import HERE, N_OUT, SR, db, limiter, lufs, place, read_wav, write_wav  # noqa: E402

SFX = os.path.join(HERE, "sfx")
WORK = os.path.join(HERE, "work")

# cuts from ../BEATS.md (frame / 29.97)
CUT_F72, CUT_F101, CUT_F159, CUT_F187, CUT_F245, CUT_F301 = 2.402, 3.370, 5.305, 6.240, 8.175, 10.043

# (name, file, time, gain dB, pan, kind) — kind "onset": attack starts at `time`; "peak": envelope peak at `time`
CUES = [
    ("impact", "soft_impact", 0.100, -5.0, 0.0, "onset"),
    ("click 1 (logo press)", "click_a", 2.330, -12.0, 0.1, "onset"),
    ("whoosh -> f72", "whoosh_drop", CUT_F72, -10.0, 0.0, "peak"),
    ("whoosh -> f101", "whoosh_menu", CUT_F101, -13.0, 0.0, "peak"),
    ("click 2 (menu icon)", "click_b", 3.830, -15.0, -0.1, "onset"),
    ("whoosh -> f159", "whoosh_whip", CUT_F159, -11.0, 0.0, "peak"),
    ("hit f187", "hit_a", CUT_F187, -6.0, 0.0, "onset"),
    ("hit f245", "hit_b", CUT_F245, -6.0, 0.0, "onset"),
    ("whoosh -> f301", "whoosh_end", CUT_F301, -11.0, 0.0, "peak"),
    ("shimmer (wordmark)", "shimmer", 10.050, -11.0, 0.0, "onset"),
]
TYPE_START, TYPE_END, TYPE_STEP = 4.04, 5.00, 0.033
TICK_GAIN = -31.0


def env_peak_index(x, win_ms=10):
    """Index of the peak of a centred RMS envelope (win_ms)."""
    m = (x ** 2).mean(1)
    w = int(win_ms / 1000 * SR)
    e = np.convolve(m, np.ones(w) / w, "same")
    return int(np.argmax(e))


def key_ticks():
    rng = np.random.default_rng(4040)
    out, t = [], TYPE_START
    while t <= TYPE_END:
        out.append((round(t, 4), "tick%d" % rng.integers(1, 7), TICK_GAIN + rng.uniform(-3, 3), rng.uniform(-0.25, 0.25)))
        t += TYPE_STEP * rng.uniform(0.7, 1.3)
    return out


def build():
    music, sr = read_wav(os.path.join(HERE, "music.wav"))
    assert sr == SR and len(music) == N_OUT, (sr, len(music))
    sfx = np.zeros((N_OUT, 2))
    log = []
    for name, f, t, g, pan, kind in CUES:
        clip, _ = read_wav(os.path.join(SFX, f + ".wav"))
        clip = clip.astype(np.float64)
        t0 = t - env_peak_index(clip) / SR if kind == "peak" else t
        place(sfx, clip, t0, g, pan)
        log.append(dict(name=name, file=f, target=t, kind=kind, clip_start=round(t0, 5), gain_db=g, dur=len(clip) / SR))
    ticks = key_ticks()
    for t, f, g, pan in ticks:
        clip, _ = read_wav(os.path.join(SFX, f + ".wav"))
        place(sfx, clip.astype(np.float64), t, g, pan)
    log.append(dict(name="key ticks", n=len(ticks), times=[a for a, *_ in ticks]))
    return music.astype(np.float64), sfx, log


def master(x):
    n_f = int(0.060 * SR)
    fade = np.ones(N_OUT)
    fade[-n_f:] = np.cos(np.linspace(0, np.pi / 2, n_f)) ** 2
    g_db = 0.0
    for it in range(8):
        y = limiter(x * 10 ** (g_db / 20), ceiling_db=-1.3) * fade[:, None]
        i, tp = lufs(y)
        print("  pass %d: gain %+.2f dB -> %.2f LUFS, TP %.2f dBTP" % (it, g_db, i, tp))
        if abs(i + 14.0) < 0.05 and tp <= -1.0:
            break
        g_db += -14.0 - i
    return y, g_db, i, tp, fade


def main():
    os.makedirs(WORK, exist_ok=True)
    music, sfx, log = build()
    y, g_db, i, tp, fade = master(music + sfx)
    assert len(y) == N_OUT
    write_wav(os.path.join(HERE, "mix.wav"), y)
    gl = 10 ** (g_db / 20)
    write_wav(os.path.join(WORK, "sfx_stem.wav"), np.clip(sfx * gl * fade[:, None], -1, 1))
    write_wav(os.path.join(WORK, "music_stem.wav"), np.clip(music * gl * fade[:, None], -1, 1))
    with open(os.path.join(WORK, "cues.json"), "w") as fh:
        json.dump(dict(master_gain_db=g_db, lufs=i, tp=tp, cues=log), fh, indent=1)
    print("wrote mix.wav: %d samples (%.4f s), %.2f LUFS, TP %.2f dBTP, sample peak %.2f dBFS, master gain %+.2f dB"
          % (len(y), len(y) / SR, i, tp, db(np.abs(y).max()), g_db))


if __name__ == "__main__":
    main()
