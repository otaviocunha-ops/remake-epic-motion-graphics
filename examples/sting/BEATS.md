# BEATS — frame-sync skeleton (pyramids reference → remake)

29.97 fps, 360 frames (f0–f359), 12.01 s picture / 12.075 s audio. Music 124.0 BPM: **beat k = 0.048 + 0.4838·k s = frame 1.44 + 14.50·k** (8th = 7.25 frames). Keep every **frame** below; swap only what is drawn. Details: `SPEC.md` (picture), `AUDIO.md` (sound), numbers: `measure/tables.json`.

| Time (s) | Frame | Beat | Event (picture) | Sound |
|---|---|---|---|---|
| 0.000 | f0 | — | S1 opens mid-motion: pale blue haze `#B7CFEB`, logo disc smeared at y≈621, rising | silence 0–0.1 s |
| 0.100 | f3 | b0 (+53 ms) | header rise at full speed; "Manus" in at f2, pill in at f4–5 (blurred, slides left 10 px) | **opening impact** (strongest onset) |
| 0.50 | f15 | b1 | window fades in around the header (opacity 0.5 at f15 → 1.0 at f24); haze → white by f28 | intro pulse |
| 0.80 | f24 | — | header settled (expo-out, 13–16 %/frame) | |
| 0.90 | f27 | b2 −3 f | cursor appears top-right (594,262), glides left | intro pulse 0.98 s |
| 1.07 | f32 | b2 | — | bright noise swell (0.68) |
| 1.47 | f44 | b3 | cursor turns down toward the logo, rotates to face travel | intro pulse |
| 1.57 | f47 | b3 | camera zoom-in to 1.2× about (360,360) begins (ease-in-out to f60) | |
| 1.77 | f53 | — | hover ring lights on the logo | build 1.8–2.4 s |
| 1.97 | f59 | **b4** | cursor lands on logo, grown ×1.55; zoom at 1.2× | |
| 2.14 | f64 | — | zoom-out begins, accelerating | |
| 2.30–2.37 | f69–f71 | — | cursor press (shrinks ≈15 %) | |
| **2.402** | **f72** | b5 −2 f | **HARD CUT → S2**: black app icon (184 px, shrinking) + 4 squares spinning CCW, blurred | **DROP** (kick 2.43–2.48 s) |
| 2.87 | f86 | b6 −2 f | icon 119 px, squares locked in a cross (r 139–150) | 8th grid now locked (±5 ms) |
| 2.94 | f88 | b6 | collapse begins: icon shrinks accelerating, squares slide right, blur ramps to σ 11 | |
| **3.370** | **f101** | b7 −2 f | **HARD CUT → S3**: blurred laptop menu bar (icon + 3 dots) settling | low hit 3.35 s |
| 3.40 | f102 | — | cursor rises from below toward the menu-bar icon | |
| 3.57 | f107 | — | cursor on the icon | |
| 3.77–3.90 | f113–f117 | **b8** (f117) | click; camera pans left (+83 px, f115–f130); glass box springs out of the icon (f116–f126, overshoot peak f126) | onset 3.915 s |
| 4.04 | f121 | — | first legible text "Tell " | groove |
| 4.07–5.01 | f122–f150 | b9 f132, b10 f146 | typing "Tell me about the pyramids", 0.75 char/frame | groove (no key clicks found) |
| 5.005 | f150 | — | prompt complete | |
| 4.54–5.27 | f136–f158 | — | scene drifts up, accelerating = whip-tilt; blur σ → 8.4; page tints `#E6F4FE` from f154 | onset 5.11 s |
| **5.305** | **f159** | b11 −2 f | **HARD CUT → S4**: answer text smeared (σ 16), 280 px low, blue flash peak `#E2F4FE` | onset 5.37 s |
| 5.51 | f165 | — | flash gone; scroll at 16–19 %/frame | |
| 5.85 | f175 | **b12** | answer nearly settled (dy 9 px); cursor under "Pyramid" | onset 0.58 |
| 6.006 | f180 | — | answer settled (dy 0), key phrase black bold | |
| **6.240** | **f187** | b13 −3 f | **HARD CUT → S5**: photo card rising from the bottom (blurred σ 2.5 at f189); answer behind blurs to σ ≈1.7 | **off-grid hit exactly on the cut (transition SFX)** |
| 6.82 | f204 | **b14** | card settled (photo top y 232) | onset 0.56 |
| 6.91–7.14 | f207–f214 | — | card shrinks slightly + drifts up; whole frame blurs σ 0.5 → 4.9 | low swell 7.08–7.33 s |
| **7.174** | **f215** | b15 −4 f | **CUT (inside blur-dissolve) → S6**: two cards blurred σ 7.9, de-blur to sharp by f224 while rising (bottom card staggered) | |
| 7.54 | f226 | — | cards settled, slow drift up | |
| 7.79 | f233 | **b16** | cards at rest-drift | onset 0.57 |
| 7.97–8.14 | f239–f244 | — | cards accelerate up, blur σ → 1.2 | |
| **8.175** | **f245** | b17 −3 f | **HARD CUT → S7**: logo disc rising into the centre (σ 2.4), expo-out | **off-grid hit exactly on the cut (transition SFX)** |
| 8.98 | f269 | — | disc at rest, (360,360), ⌀112 — the only frozen hold (to f287) | onset 0.69 at 9.00 s |
| 9.61 | f288 | b20 −3 f | disc starts shrinking, accelerating (111 → 82 px by f300) | |
| **10.043** | **f301** | b20½ +2 f | **HARD CUT → S8**: black end card, "dnyxstudios" huge + horizontally smeared, zooming out | low hit 10.22 s |
| 10.38 | f311 | — | word sharp, width 452 px, still shrinking (ease-out) | |
| 10.69 | f320 | b22 | word 375 px, glow steady | onset |
| 11.48 | f344 | — | word 342 px, ≈1 px/frame drift | |
| 11.66 | f349–f350 | **b24** | collapse begins (ease-in): 328 → 178 px by f359, blur → σ 2.3 | onset |
| 12.012 | end of f359 | — | picture ends mid-collapse | music continues to 12.075 s, no fade |

**Rules the grid implies:** hard cuts f72, f101, f159 each lead a beat by 2 frames; S5/S6/S7 transitions carry their own off-grid hits on the cut frames (f187, f245); settles land on beats (f59 b4, f86≈b6, f117 b8, f175 b12, f204 b14, f233 b16, f349 b24). A remake that keeps these frames and a 124 BPM track with its drop at 2.45–2.47 s stays in sync.
