"""Audio analysis of ref/audio.wav (numpy only): loudness, onset envelope, onset peaks, tempo by autocorrelation,
band energies, mid/side, voice-band check. Run from pyramids/measure: python3 audio.py"""
import json, wave
import numpy as np
from lib import ROOT, FPS, save_part
import os

w = wave.open(os.path.join(ROOT, 'ref', 'audio.wav'))
sr = w.getframerate(); n = w.getnframes(); ch = w.getnchannels()
a = np.frombuffer(w.readframes(n), np.int16).reshape(-1, ch).astype(np.float64) / 32768.0
L, R = a[:, 0], a[:, 1]
mid, side = (L + R) / 2, (L - R) / 2
res = {'sr': sr, 'channels': ch, 'duration_s': round(n / sr, 3)}

def db(x): return 20 * np.log10(max(x, 1e-9))
res['peak_dbfs'] = round(db(np.abs(a).max()), 2)
res['rms_dbfs_total'] = round(db(np.sqrt((a ** 2).mean())), 2)
res['side_to_mid_db'] = round(db(np.sqrt((side ** 2).mean())) - db(np.sqrt((mid ** 2).mean())), 2)
# first sample above -50 dBFS (music start) and last
env = np.abs(mid)
thr = 10 ** (-50 / 20)
idx = np.nonzero(env > thr)[0]
res['first_above_-50dBFS_s'] = round(idx[0] / sr, 3) if len(idx) else None
res['last_above_-50dBFS_s'] = round(idx[-1] / sr, 3) if len(idx) else None

# K-weighting is not available without scipy; approximate integrated loudness with a 2nd-order high-pass
# (RLB-like) at ~100 Hz applied via FFT, then mean-square gating at -70 LUFS (ungated for such a short clip).
def hp(x, fc):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / sr)
    Hs = (f / fc) ** 2 / np.sqrt(1 + (f / fc) ** 4)
    shelf = 1 + (10 ** (4 / 20) - 1) / (1 + (1500 / np.maximum(f, 1)) ** 2)   # +4 dB high shelf above ~1.5 kHz
    return np.fft.irfft(X * Hs * shelf, len(x))
kL, kR = hp(L, 100), hp(R, 100)
blk = int(0.4 * sr); hop = int(0.1 * sr)
ms = [((kL[i:i + blk] ** 2).mean() + (kR[i:i + blk] ** 2).mean()) for i in range(0, n - blk, hop)]
ms = np.array(ms); lk = -0.691 + 10 * np.log10(np.maximum(ms, 1e-12))
gated = ms[lk > -70]
rel = -0.691 + 10 * np.log10(gated.mean()) - 10
gated2 = ms[(lk > -70) & (lk > rel)]
res['integrated_loudness_LUFS_approx'] = round(-0.691 + 10 * np.log10(gated2.mean()), 1)
# short-term loudness per 0.5 s (approx) for the arc
arc = []
for t0 in np.arange(0, n / sr, 0.5):
    i0, i1 = int(t0 * sr), int(min((t0 + 0.5) * sr, n))
    m = ((kL[i0:i1] ** 2).mean() + (kR[i0:i1] ** 2).mean())
    arc.append([round(float(t0), 1), round(-0.691 + 10 * np.log10(max(m, 1e-12)), 1)])
res['loudness_arc_0.5s'] = arc

# spectral flux onset envelope (hop 256 = 5.33 ms)
N, H = 2048, 256
win = np.hanning(N)
frames = [mid[i:i + N] * win for i in range(0, n - N, H)]
S = np.abs(np.fft.rfft(np.array(frames), axis=1))
freqs = np.fft.rfftfreq(N, 1 / sr)
logS = np.log1p(100 * S)
flux = np.maximum(np.diff(logS, axis=0), 0).sum(axis=1)
flux = np.concatenate([[0], flux])
t_env = (np.arange(len(flux)) * H + N / 2) / sr
# band fluxes
def bandflux(lo, hi):
    sel = (freqs >= lo) & (freqs < hi)
    f = np.maximum(np.diff(logS[:, sel], axis=0), 0).sum(axis=1)
    return np.concatenate([[0], f])
low, midb, high = bandflux(20, 150), bandflux(150, 2000), bandflux(2000, 16000)
# peak picking: local max in +-50 ms, above median + 2.5*MAD over +-1 s
def peaks(env, k=2.5, win_s=0.05):
    w = int(win_s * sr / H); W = int(1.0 * sr / H); out = []
    for i in range(1, len(env) - 1):
        lo, hi = max(0, i - w), min(len(env), i + w + 1)
        if env[i] < env[lo:hi].max(): continue
        seg = env[max(0, i - W):i + W]
        med = np.median(seg); mad = np.median(np.abs(seg - med)) + 1e-9
        if env[i] > med + k * mad * 1.4826 and env[i] > 0.15 * env.max():
            out.append(i)
    return out
pk = peaks(flux)
res['onsets'] = [{'t': round(float(t_env[i]), 3), 'frame': int(round(t_env[i] * FPS)), 'strength': round(float(flux[i] / flux.max()), 3),
                  'low': round(float(low[i] / (low.max() + 1e-9)), 2), 'mid': round(float(midb[i] / (midb.max() + 1e-9)), 2),
                  'high': round(float(high[i] / (high.max() + 1e-9)), 2)} for i in pk]
# low-band (kick/impact) peaks separately
res['low_band_hits'] = [{'t': round(float(t_env[i]), 3), 'frame': int(round(t_env[i] * FPS)), 'strength': round(float(low[i] / low.max()), 3)} for i in peaks(low, 3.0)]

# tempo: autocorrelation of the onset envelope, 60..200 BPM
e = flux - flux.mean()
ac = np.correlate(e, e, 'full')[len(e) - 1:]
ac /= ac[0]
lags = np.arange(len(ac)) * H / sr
sel = (lags >= 60 / 200) & (lags <= 60 / 60)
cands = []
idx = np.nonzero(sel)[0]
for i in idx[1:-1]:
    if ac[i] > ac[i - 1] and ac[i] >= ac[i + 1]:
        cands.append((round(float(60 / lags[i]), 2), round(float(ac[i]), 3)))
cands.sort(key=lambda c: -c[1])
res['tempo_candidates_bpm_ac'] = cands[:6]
# refine best by comb over beat phases
best_bpm = cands[0][0] if cands else None
if best_bpm:
    period = 60 / best_bpm
    phases = np.linspace(0, period, 200, endpoint=False)
    sc = []
    for ph in phases:
        ts = np.arange(ph, n / sr, period)
        ii = np.clip(np.round((ts * sr - N / 2) / H).astype(int), 0, len(flux) - 1)
        sc.append(flux[ii].mean())
    ph = phases[int(np.argmax(sc))]
    res['beat_phase_s'] = round(float(ph), 3)
    res['beat_times_s'] = [round(float(t), 3) for t in np.arange(ph, n / sr, period)]

# voice check: fraction of energy in 300-3400 Hz and spectral flatness over time; harmonic pitch track (autocorr)
def band_ratio(x, lo, hi):
    X = np.abs(np.fft.rfft(x)) ** 2; f = np.fft.rfftfreq(len(x), 1 / sr)
    return float(X[(f >= lo) & (f < hi)].sum() / X.sum())
res['energy_share_300_3400Hz'] = round(band_ratio(mid, 300, 3400), 3)
res['energy_share_below_150Hz'] = round(band_ratio(mid, 20, 150), 3)
res['energy_share_above_4kHz'] = round(band_ratio(mid, 4000, 20000), 3)
# per 0.25 s: spectral centroid + band energies
seg = []
for t0 in np.arange(0, n / sr - 0.25, 0.25):
    x = mid[int(t0 * sr):int((t0 + 0.25) * sr)]
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2; f = np.fft.rfftfreq(len(x), 1 / sr)
    tot = X.sum() + 1e-12
    seg.append({'t': round(float(t0), 2), 'rms_db': round(db(np.sqrt((x ** 2).mean())), 1), 'centroid_hz': int((f * X).sum() / tot),
                'low': round(float(X[f < 150].sum() / tot), 2), 'voice': round(float(X[(f >= 300) & (f < 3400)].sum() / tot), 2),
                'high': round(float(X[f >= 4000].sum() / tot), 2)})
res['segments_0.25s'] = seg
# dominant pitch per 0.25 s (strongest spectral peak 60..1000 Hz)
pitch = []
for t0 in np.arange(0, n / sr - 0.25, 0.25):
    x = mid[int(t0 * sr):int((t0 + 0.25) * sr)]
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)), 8 * len(x))); f = np.fft.rfftfreq(8 * len(x), 1 / sr)
    s = (f >= 40) & (f <= 1000)
    pitch.append([round(float(t0), 2), round(float(f[s][np.argmax(X[s])]), 1)])
res['dominant_peak_hz_0.25s'] = pitch
res['onset_env'] = {'hop_s': H / sr, 't0_s': N / 2 / sr, 'flux': [round(float(v), 2) for v in flux]}

if __name__ == '__main__':
    for k, v in res.items():
        if k in ('onset_env', 'segments_0.25s', 'loudness_arc_0.5s', 'beat_times_s', 'dominant_peak_hz_0.25s'): continue
        print(k, v)
    print('arc', res['loudness_arc_0.5s'])
    print('beats', res.get('beat_times_s'))
    for s_ in res['segments_0.25s']: print(s_)
    print('pitch', res['dominant_peak_hz_0.25s'])
    save_part('audio', res)
