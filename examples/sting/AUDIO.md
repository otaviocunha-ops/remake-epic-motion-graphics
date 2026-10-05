# AUDIO — pyramids reference (`ref/audio.wav`)

File: `ref/audio.wav`, PCM 16-bit, **48 kHz stereo**, 12.075 s, extracted from `ref/src.mp4` with the stripped ffmpeg (`-vn -acodec pcm_s16le -ar 48000`).
Analysis: `measure/audio.py` (numpy only) → `measure/parts/audio.json`, merged into `measure/tables.json → audio`. Frame = round(t × 29.97).
**I could not listen to it.** Everything below is from numbers (spectral-flux onsets, band energies, autocorrelation, grid fitting). Sound *identities* are guesses and are labelled as such.

## 1. Headline numbers

| Item | Value | How |
|---|---|---|
| Music start | first sample above −50 dBFS at **0.109 s** (f3); 0–0.1 s is silence | abs(mid) threshold |
| First hit | **0.101 s (f3)** — the strongest onset in the file (all bands: low 0.38, mid 0.89, high 1.00) | spectral flux |
| Tempo | **124.0 BPM** (beat 0.4838 s = **14.50 frames**, 8th = 0.2419 s = 7.25 frames) | onset autocorrelation peak 123.6 BPM (0.69), half-tempo 61.8 (0.66); refined by fitting 35 strong onsets after 2.5 s to an 8th grid: mean error **±10.7 ms**, most within ±5 ms |
| Beat grid | t_k = **0.048 + 0.4838·k s** (k = 0…24); low-band energy lands on the even 8ths, so these are the beats | grid fit + low-band (<150 Hz) peaks at 2.5, 3.0, 3.5, 5.4, 5.9, 6.4, 7.3, 8.3, 8.8, 9.3 s |
| Drop | **≈2.45 s (beat 5 = 2.467 s, f74)**: short-term loudness jumps from ≈ −16 to ≈ −9 LUFS; 50 ms level −11 dB (2.4 s) → −5 dB (2.5 s); low band −13.8 → −5.3 dB | 0.1 s level scan |
| Voice | **No** | voice band (300–3400 Hz) = 7.9 % of energy; low band (<150 Hz) = 70.9 %; no 3–7 Hz syllabic modulation (envelope modulation peak 2.3 Hz in the intro, 8.3 Hz = 16th notes after the drop); every post-drop onset sits on the musical grid |
| Integrated loudness | **≈ −11.5 LUFS** (approximate K-weighting: 100 Hz high-pass + +4 dB shelf above 1.5 kHz, 400 ms blocks, −70/−10 gating) | numpy approximation of BS.1770 — treat as ±1 LU |
| Peak / RMS | **0.0 dBFS** peak (limited/clipped master), −11.2 dBFS RMS | |
| Stereo | side/mid = −11.1 dB → narrow, near-mono mix | L−R vs L+R |
| End | music is still playing at the last sample (12.056 s above −50 dBFS); no fade to silence — the file just stops | |

## 2. Loudness arc (short-term, 0.5 s blocks, approx. LUFS)

| t (s) | 0.0 | 0.5 | 1.0 | 1.5 | 2.0 | 2.5 | 3.0 | 3.5 | 4.0 | 4.5 | 5.0 | 5.5 | 6.0 | 6.5 | 7.0 | 7.5 | 8.0 | 8.5 | 9.0 | 9.5 | 10.0 | 10.5 | 11.0 | 11.5 | 12.0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LUFS | −15.4 | −17.5 | −15.9 | −16.4 | −9.8 | −8.9 | −10.7 | −11.4 | −10.7 | −10.5 | −10.5 | −12.0 | −10.9 | −11.0 | −9.5 | −10.7 | −10.4 | −10.9 | −11.2 | −11.2 | −12.2 | −13.0 | −13.5 | −14.8 | −14.7 |

Shape: soft intro (f0–f71) → full level from the drop (f72+) → steady body → gentle 2–3 LU decline over the end card (10–12 s, f300–f359).

## 3. Structure (inferred from the numbers)

- **0.0–2.4 s intro (S1).** Bright/noisy events: spectral flatness 0.38 at 0.0–0.25 s and 0.40 at 1.0–1.25 s (noise-like = whoosh/riser/cymbal-type sounds — NOT verified by ear); tonal peaks 116–323 Hz in between. Onsets run at the same 124 BPM period but are **offset from the main grid**: one layer on 0.101 + 0.2419·n (≈ +55 ms late vs the main grid: 0.101, 0.357, 0.592, 0.832, 1.072, 1.328, 1.557, 1.803, 2.043 s), another on the beats −40 ms (0.491, 0.976, 1.456, 1.947 s). The intro was probably spliced/edited onto the track; keep its own timings in a remake. A build from 1.8 s (50 ms level −24 → −11 dB by 2.4 s).
- **2.45 s drop (cut to S2 at f72).** Low-band hits at 2.368 (f71), 2.427 (f73), 2.480 (f74); the loudest low-end region of the file starts here.
- **2.95–10.0 s groove.** Onsets on every 8th note (±5 ms), 16th-note hats (modulation peak 8.3 Hz), low end on the beats. Bass-heavy (70 % of energy < 150 Hz; dominant spectral peaks 54–78 Hz).
- **10.0–12.06 s outro (end card).** Same groove, level falling 2–3 LU, fewer strong onsets; stops mid-bar.

## 4. Hits and probable SFX (onset peaks)

Grid slot = nearest 8th of the main grid (beat n or the 8th after it); off-grid ≠ 0 by more than ≈ ±20 ms after 2.5 s suggests a sound that is not part of the loop (an SFX or edit point). Strength = normalised flux.

| t (s) | Frame | Strength | Low / mid / high | Grid slot | Off (ms) | Probable meaning (guess) |
|---|---|---|---|---|---|---|
| 0.101 | f3 | **1.00** | 0.38 / 0.89 / 1.00 | beat 0 | +53 | **opening impact / whoosh-hit** as the header rises (strongest in file) |
| 0.357 | f11 | 0.21 | 0.04 / 0.18 / 0.21 | 8th | +67 | intro pulse |
| 0.491 | f15 | 0.23 | 0.05 / 0.23 / 0.22 | beat 1 | −41 | intro pulse (window fades in f15) |
| 0.592 | f18 | 0.36 | 0.00 / 0.27 / 0.37 | beat 1 | +60 | intro pulse |
| 0.832 | f25 | 0.35 | 0.03 / 0.34 / 0.35 | 8th | +58 | intro pulse |
| 0.976 | f29 | 0.41 | 0.04 / 0.37 / 0.41 | beat 2 | −40 | intro pulse (cursor appears f27) |
| 1.072 | f32 | **0.68** | 0.06 / 0.39 / 0.65 | beat 2 | +56 | bright noise swell/swish (flatness 0.40) |
| 1.328 | f40 | 0.23 | | 8th | +70 | intro pulse |
| 1.456 | f44 | 0.36 | 0.13 / 0.26 / 0.36 | beat 3 | −43 | intro pulse (cursor turns down f44) |
| 1.557 | f47 | 0.43 | 0.03 / 0.16 / 0.48 | beat 3 | +58 | intro pulse (zoom-in starts f47) |
| 1.803 | f54 | 0.21 | | 8th | +62 | (hover ring appears f53) |
| 1.947 | f58 | 0.23 | | beat 4 | −36 | (cursor lands on logo f56–59) |
| 2.043 | f61 | 0.26 | | beat 4 | +60 | |
| 2.363 / 2.432 / 2.496 | f71 / f73 / f75 | 0.16–0.18 | low-heavy | beat 5 | −104 / −35 / +29 | **drop**: press f69–71 → cut f72 → kick |
| 2.949 | f88 | 0.33 | | beat 6 | −2 | squares settled (f86–88) |
| 3.349 (low) | f100 | low hit | | | | icon collapse end / cut f101 |
| 3.435 | f103 | 0.33 | | beat 7 | 0 | menu bar settling |
| 3.915 | f117 | 0.47 | 0.00 / 0.19 / 0.50 | beat 8 | −3 | glass box pops (f116–119) |
| 4.160–4.885 | f125–f146 | 0.30–0.40 | | 8ths | ±4 | groove under the typing (no separate key-click onsets found) |
| 5.109 | f153 | 0.36 | | 8th | −19 | whip-tilt starting |
| 5.371 | f161 | 0.37 | 0.09 / 0.32 / 0.37 | beat 11 | +1 | just after the cut to the answer (f159) |
| 5.851 | f175 | 0.58 | | beat 12 | −3 | answer settles |
| 6.240 | **f187** | 0.40 | 0.04 / 0.25 / 0.40 | beat 13 | **−97** | **off-grid, exactly on the cut to the photo card → transition SFX (whoosh/pop) likely** |
| 6.816 | f204 | 0.56 | | beat 14 | −5 | card settled |
| 7.077–7.328 (low) | f212–f220 | low hits | | | | blur-dissolve S5→S6 (cut f215): low swell/whoosh likely |
| 7.787 | f233 | 0.57 | | beat 16 | −2 | cards settled |
| 8.176 | **f245** | 0.30 | 0.02 / 0.23 / 0.30 | beat 17 | **−97** | **off-grid, exactly on the cut to the logo disc → transition SFX likely** |
| 8.997 | f270 | 0.69 | 0.08 / 0.42 / 0.72 | 8th | −1 | strongest post-drop onset, disc at rest |
| 9.723 | f291 | 0.53 | | beat 20 | −1 | disc shrink under way (from f288) |
| 10.224 (low) | f306 | low hit | | | | end card landing (cut f301) |
| 11.659 | f349 | 0.36 | | beat 24 | 0 | end-word collapse starts (f350) |
| 12.043 | f361 | 0.46 | | | −100 | past the last video frame (f359); file ends 12.075 s |

Full onset list (74 peaks, with band shares) and all low-band hits: `measure/tables.json → audio.onsets`, `audio.low_band_hits`. The onset envelope itself (5.33 ms hop) is in `measure/parts/audio.json → onset_env`.

## 5. What a remake must do with the sound

- Use a 124 BPM track (or retime this one) whose drop lands at **2.45–2.47 s**; the picture cut is at f72 (2.402 s).
- Put a transition hit on **f187 (6.240 s)** and **f245 (8.176 s)** — these are the only strong off-grid events after the drop and they sit exactly on cut frames.
- Opening impact at **0.10 s (f3)**.
- Target ≈ −11.5 LUFS integrated, peaks limited to about −1 dBTP (the reference hits 0.0 dBFS; do not copy the clipping).
- No voice-over.

## 6. Not pinned

- Instrument/SFX identities (needs ears).
- Whether the intro offset (+55 ms / −40 ms vs the main grid) is musical (a separate intro stem) or an edit artefact.
- AAC encoder delay: the three clean hard cuts (f72, f101, f159) sit 65 ms before beats 5, 7 and 11. If the file's audio is delayed by the encoder's priming samples (typically ≈ 21–46 ms), the true cut-to-beat lead is smaller. The remake should keep the **frame** numbers.
