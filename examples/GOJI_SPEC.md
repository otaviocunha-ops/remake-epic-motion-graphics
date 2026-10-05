> **Example spec.** Frame-level spec of a public launch film (a 65 s product ad), written by an agent. It shows the level of detail a remake needs: shot table with exact frames, measured colours, type sizes, per-frame cursor tracks, camera keyframes, verbatim text, audio timings. The reference video itself is not included. Use it as a model for your own `SPEC.md` (see `../prompts/REMAKE_ANY_VIDEO.md`, Phase 0).

# GOJI_SPEC: frame-accurate replication spec of the Gojiberry launch film

Source: `ref/goji.mp4` · 1920×1080 · 24 fps · 1,557 frames (f0–f1556) · 64.94 s · AAC 48 kHz stereo.
Stills: `ref/stills/<start-time>s_<shot>_f<frame>.png` (one per shot, full-res PNG, frame-verified against the decoded stream).

Measurement method (reliability of each number):
- Every frame was decoded (full-res JPEG q2 + 480×270 copies). Cuts come from mean abs frame-difference; positions/sizes from ink bounding boxes (non-white pixels) measured per frame; colours are pixel samples or the mean of the darkest 4 % of a text region (text "ink"). Anti-aliasing makes thin-stroke colours read slightly lighter than the true fill.
- Cursor positions come from a connected-component detector (pure-black blob with ~0.4 fill ratio), so they are the cursor's **top-left-most black pixel ≈ the tip**, ±4 px.
- Audio: mid (L+R) and side (L−R) were separated. The narrator is dead-centre mono, so the **side channel is music/SFX only**. Tempo and the loudness arc were measured without the voice.
- The audio was not listened to. Every sound value comes from numbers (spectra, onsets, pitch tracking). Items marked **NOT PINNED** are estimates.

Conventions: `fN` = 0-based frame index; time = N/24 s. Positions are on the 1920×1080 canvas (x right, y down, origin top-left). "Camera" = one transform (scale + translate, sometimes a small rotate) applied to the whole scene layer. The background is pure `#FFFFFF` for the entire film: no gradients, no vignette, no grain.

---

## 0. The film in one paragraph

A white, Apple-keynote-style product film. A single virtual camera never stops moving: almost every cut is a **motion-matched cut**: the outgoing shot accelerates (ease-in) in some direction/zoom and the incoming shot continues that same motion decelerating (ease-out), so the eye reads one continuous move. Words land one at a time in a **hot orange that cools to near-black** (the "ember reveal"). Brand phrases get a **crimson→coral→peach gradient**. UI is rebuilt flat and oversized (ChatGPT composer, LinkedIn DM, calendar), shot at extreme close-up with soft edge-fade masks. Transitions use motion blur, a pixel burst, a halftone iris and a zoom through the counter of an "o". Edit is locked to a **104 BPM** grid (8th-note resolution).

---

## 1. Global style system

### 1.1 Colour tokens (sampled)

| Token | Hex | Where sampled |
|---|---|---|
| bg | `#FFFFFF` | every frame corner |
| ink (final kinetic text) | `#151514` | f640 "Brings…" |
| ink-2 (UI body) | `#1D1D1D` / `#2B2B2B` | person-card name / phone |
| ink-3 (bold UI name in bubble) | `#3C4044` | f506 "Gojiberry" |
| grey text (labels) | `#929292` | card "Founder at…", "Email:" |
| placeholder | `#9D9D9D` | "Ask anything" f47 |
| prompt grey (typed, un-highlighted) | `#969696` → fresh chars `#D8D8D8` | f300 "hiring sale" |
| ember-hot (word enter) | `#EE8319` | f623 "the" |
| ember-mid | `#C7620B` → `#AB6219` → `#4C3115` | f905 / f623 / f626 |
| goji crimson | `#EA485A` (text), `#EB4C5E` (mark facet) | f20 wordmark, f104 mark |
| goji coral | `#F4816F` (mark), `#F07E72` (text gradient mid) | f104, f340 |
| goji peach | `#F9C08B` (mark), `#F0BA8A` (text gradient end) | f104, f340 |
| prompt-rose (first typed state) | `#BA968A` → `#EA6666` | f250 "Find 1", f290 "founders" |
| brand gradient (text) | `linear-gradient(90deg,#EA485A 0%,#F07E72 55%,#F0BA8A 100%)` | f340 "enrich their contact details" |
| app-icon orange tile | TL `#F9BF91` → BR `#F4806F` (diag. 135°) | f155 |
| composer chip tile | top `#EF5766` → bottom `#F8B990` (vertical) | f975 |
| explosion tile orange | `#F29433` (range `#F09030`–`#F09840`) | f868 |
| feature-icon orange | `#F29535` core, `#F2AD5F` body, `#FFE1C0` rim light | f1250 |
| halftone dots | `#E89030`, `#E8B880`, `#D8A060`, pale `#FCEACC` | f171–172 |
| pixel-burst squares | `#F69C8A`, `#F6B4A8`, `#F6C6BA`, `#F6D2CC` | f478 |
| click ripple | `#F2A49A` (blurred ring) | f64–f72 |
| caret | coral `#F0806F` | f64, f88 |
| ChatGPT user bubble | fill `#CDE7FE`, border `#3C404B` (≈3 px) | f506 |
| composer border | `#A4A4A4` (2 px) at 1× | f47 |
| composer warm fill (late film) | white → `#FAF9F5`, radial glow `#FBEFDD` right side | f975, f1395 |
| Launch / Install pill | fill `#FDFAF1`, bottom edge `#F6EDDE`, pressed glow `#F8D89C` | f860, f1328 |
| LinkedIn blue (logo) | `#0A66C2` (sampled `#2A79C8`, card icon `#067EB4`) | f730, f700 |
| DM outgoing bubble | `#2A6DE2` | f730, f1090, f1300 |
| DM incoming bubble | `#EDF1F4` | f1050 |
| DM window | fill `#FDFDFD` → `#FBFAF6` (bottom-right warm), hairline `#F0F0F0` | f730 |
| typing indicator | pill `#E6E7E9`, dots `#9D9EA2` | f820 |
| online dot | `#13CC29` | f730 |
| approve check | `#1CC628` | f1090 |
| calendar event | `#13A7DE` (settled), `#A2DEF6` (drag start) | f1135, f1121 |
| calendar grid lines | `#E3E4E8` | f1135 |
| graph lines + nodes | `#393939` | f1250 |
| end wordmark | `#111619` | f1520 |

### 1.2 Typography

All UI and kinetic type is a neo-grotesk that matches **SF Pro Display/Text** (Apple) closely: single-storey "g", slanted terminal on "t", round "@". Use **SF Pro** if licensed; otherwise **Inter Display** (tracking −0.01 em) is the closest free match. Family = guess from letterforms; weights and sizes are measured.

| Use | Weight | Size on canvas (cap height → px) | Tracking | Notes |
|---|---|---|---|---|
| Kinetic sentence lines ("Brings…", "Goji flags…", "From one prompt", "Right here in ChatGPT") | Semibold 600 | cap 59–64 px → **82–89 px** | −0.02 em | centred, single line |
| "Right here" hero | Semibold 600 | cap 236 px → **≈330 px** | −0.02 em | two words, baseline-offset entry |
| "ChatGPT" hero (S32) | Medium 500 | cap 136 px → **≈190 px** | −0.01 em | |
| "ChatGPT is the interface" | Medium 500 | cap 68 px → **≈94 px** | −0.01 em | |
| Feature chips ("Intent Signals"…) | Medium 500 | cap 68–69 px → **≈95 px** | −0.02 em | |
| Prompt text, extreme close-up (S06–S10) | Regular 400 ("@Gojiberry" Bold 700) | "F" cap 85 px → **≈118 px**; "@Gojiberry" ≈150 px bold | 0 | grows with camera |
| Final prompt bar text (S39) | Regular 400 | cap 78 px → **≈108 px** | −0.01 em | |
| ChatGPT heading "What can I help with?" | Regular 400 | cap 49 px @ f47 → **≈68 px** | −0.01 em | |
| Composer placeholder | Regular 400 | 26 px @ f47 | 0 | `#9D9D9D` |
| Pill buttons "Launch" / "Install Plugin" | Medium 500 | cap 44–46 px → **≈62 px** | 0 | `#010100` |
| Person card name | Regular 400 | ≈44 px @ f700 | 0 | `#1D1D1D` |
| End wordmark "gojiberry" | brand logotype (geometric, single-storey g; closest: Plus Jakarta Sans / DM Sans Medium) | box 540×128 px | (none) | replace with the remake's logo |
| Tagline "Your AI go-to-market team" | Medium 500 | cap 43 px → **≈56 px** | 0 | `#131313` |

### 1.3 Recurring motion motifs (implement once, reuse)

**M1 · Ember word reveal** (S02 heading, S17, S21-type lines, S24, S25, S27, S32, S33, S36, chips).
Each word enters separately, one per ~2–3 frames (synced ahead of the spoken word):
- frame 0: opacity 0, blur 8 px, x +24 px (words start with *extra* spacing to the right), colour `#EE8319`
- frames 0→4: opacity →1, blur →0 (ease-out cubic)
- frames 0→10: colour `#EE8319` → `#C7620B` (f3) → `#4C3115` (f6) → `#151514` (f10) (ease-in-out)
- the whole line re-centres as words are added: left edge moves left with ease-out (S17: left edge x 574→275 over f623→f640, then a slow drift of −3 px/frame to f672)
- word gaps start wide (≈1.6× normal) and close to normal over ~6 frames.

**M2 · Brand gradient sweep** (S07–S10 prompt words, card email, "Analysing Lead…", "Working…").
Fresh text is light grey `#D8D8D8`; a gradient (M1.1 brand gradient) is revealed across it left→right with a soft 80 px feathered edge; after ~20 frames non-key words cool to `#969696`, key phrases keep the gradient.

**M3 · Motion-matched cut.** Outgoing move ends in ease-in (accelerating); incoming shot starts mid-motion with ease-out. Measured examples: f24→f36 lockup shrinks accelerating (width 1231→908), f37 ChatGPT UI enters already at scale 1.31 and decelerates to 1.0 by f44. f198→f210 window zoom-in accelerates; f211 cut to 6× close-up still zooming, decelerating to f238.

**M4 · Edge-fade masks.** Close-up UI never shows a hard frame edge: a linear alpha mask fades content to white over the last ~15 % of the frame on the side the camera is travelling from (right edge fade in S02/S06; left edge fade in S07–S10 so scrolled-off text dissolves).

**M5 · Whip blur.** Horizontal/zoom exits use directional motion blur ≈ velocity × 0.5 frame (e.g. f673–f683 text slides left 40→150 px/frame with matching horizontal blur and ~5 % x-squash).

**M6 · Cursor press.** Cursor scale 1 → 0.52 (1 frame) → 0.75 → 0.9 → 1.05 overshoot → 1.0 over ~7 frames; click ripple (§5).

**M7 · Camera drift.** Holds are never static: typical 0.3–0.6 %/frame scale drift or 2–12 px/frame pan.

---

## 2. Shot table (40 shots, f0–f1556, no gaps)

Beat grid for reference: beat k at t = 0.34 + k·0.5767 s (104.05 BPM); a beat ≈ 13.84 frames, an 8th ≈ 6.9 frames. "On-beat" = cut within ±1 frame of a beat.

| # | Frames | Time (s) | Still | Content | Out-transition |
|---|---|---|---|---|---|
| S01 | 0–36 | 0.000–1.500 | `00.000s_S01_f0024.png` | OpenAI × Gojiberry co-brand lockup builds, then shrinks | motion-matched zoom-out cut (on-beat, beat 2) |
| S02 | 37–103 | 1.542–4.292 | `01.542s_S02_f0088.png` | ChatGPT home: heading + composer; cursor clicks; types "Run my outbound"; camera pans right | whip-pan cut (on-beat, beat 7) |
| S03 | 104–135 | 4.333–5.625 | `04.333s_S03_f0120.png` | Gojiberry app tile slides in; wordmark "Gojiberry" letters in; wordmark tucks behind tile | continuous (same object) |
| S04 | 136–167 | 5.667–6.958 | `05.667s_S04_f0155.png` | Tile shrinks, re-skins white→orange gradient icon, holds | halftone iris burst |
| S05 | 168–210 | 7.000–8.750 | `07.000s_S05_f0200.png` | Halftone dot ring expands, revealing ChatGPT desktop window; sidebar history populates; accelerating push-in | zoom-through cut |
| S06 | 211–246 | 8.792–10.250 | `08.792s_S06_f0238.png` | 6× close-up of composer corner; types "@Gojiberry" | continuous pan |
| S07 | 247–318 | 10.292–13.250 | `10.292s_S07_f0300.png` | " Find 100 SaaS founders hiring salespeople" types; camera tracks caret | whip-left |
| S08 | 319–361 | 13.292–15.042 | `13.292s_S08_f0340.png` | "enrich their contact details" (brand gradient) | vertical scroll-up |
| S09 | 362–399 | 15.083–16.625 | `15.083s_S09_f0385.png` | "write a personalised message" rises from below | whip-left |
| S10 | 400–450 | 16.667–18.750 | `16.667s_S10_f0420.png` | "and launch the campaign." (campaign in accent) slow drift left | whip-left + send button enters (on-beat, beat 32) |
| S11 | 451–470 | 18.792–19.583 | `18.792s_S11_f0466.png` | Black send button slides in from right, grows to centre; cursor arrives | click |
| S12 | 471–488 | 19.625–20.333 | `19.625s_S12_f0478.png` | Press; pink pixel burst ring; button drops out bottom revealing chat bubble | reveal (continuous) |
| S13 | 489–516 | 20.375–21.500 | `20.375s_S13_f0506.png` | ChatGPT user bubble with Gojiberry prompt + "Working…" shimmer | zoom-through |
| S14 | 517–527 | 21.542–21.958 | `21.542s_S14_f0524.png` | Zoom-blur into the "o" of "Working"; avatar cloud visible through the counter | zoom-through (off-beat) |
| S15 | 528–575 | 22.000–23.958 | `22.000s_S15_f0530.png` | Avatar cloud (6 leads, "Analysing Lead…"), camera pushes to Maya | continuous push |
| S16 | 576–620 | 24.000–25.833 | `24.000s_S16_f0612.png` | Maya person card: fields type in; card accelerates left | whip-left to white (2 white frames) |
| S17 | 621–685 | 25.875–28.542 | `25.875s_S17_f0640.png` | f621–622 white; "Brings the right context into every message" ember reveal; whip-left blur exit; f684–685 white | hard cut (on-beat, beat 49) |
| S18 | 686–711 | 28.583–29.625 | `28.583s_S18_f0700.png` | Person card again (larger); cursor enters, clicks LinkedIn icon | blur zoom-in |
| S19 | 712–750 | 29.667–31.250 | `29.667s_S19_f0730.png` | LinkedIn DM window focuses in from blur; bubble "Hi Maya!"; text back-spaces to empty | push-in cut |
| S20 | 751–802 | 31.292–33.417 | `31.292s_S20_f0790.png` | Close-up: empty bubble retypes "Saw you're growing your sales team" | whip-up (off-beat) |
| S21 | 803–851 | 33.458–35.458 | `33.458s_S21_f0825.png` | Maya avatar + typing indicator "•••" + "Write a message…"; blur/fade out | fade-through-white (on-beat, beat 61) |
| S22 | 852–866 | 35.500–36.083 | `35.500s_S22_f0860.png` | "Launch" pill pops in; cursor clicks (on "launch") | tile explosion (on-beat, beat 62) |
| S23 | 867–903 | 36.125–37.625 | `36.125s_S23_f0872.png` | Orange tiles burst from pill, become ~30 avatar photos flying outward; camera pushes on pill | hard cut |
| S24 | 904–916 | 37.667–38.167 | `37.667s_S24_f0912.png` | "Right here" huge, ember reveal | hard cut (scale jump) |
| S25 | 917–942 | 38.208–39.250 | `38.208s_S25_f0938.png` | "Right here in ChatGPT" small; words part; a pill grows into a composer | morph + zoom |
| S26 | 943–982 | 39.292–40.917 | `39.292s_S26_f0975.png` | Composer; grab-hand drags Gojiberry chip in; prompt types | hard cut (off-beat) |
| S27 | 983–1013 | 40.958–42.208 | `40.958s_S27_f0995.png` | "Goji flags interested prospects" ember reveal, drifts up | hard cut |
| S28 | 1014–1031 | 42.250–42.958 | `42.250s_S28_f1028.png` | Orange bubble shapes unfold into LinkedIn DM; Maya's reply types | continuous |
| S29 | 1032–1065 | 43.000–44.375 | `43.000s_S29_f1050.png` | "Thinking of the best reply" pill slides in over DM | blur push (off-beat) |
| S30 | 1066–1110 | 44.417–46.250 | `44.417s_S30_f1090.png` | Pill becomes green check; suggested blue reply types | hard cut |
| S31 | 1111–1153 | 46.292–48.042 | `46.292s_S31_f1135.png` | Calendar day view; cursor drags to create "meeting with Maya" block | hard cut |
| S32 | 1154–1175 | 48.083–48.958 | `48.083s_S32_f1170.png` | "Chat" → "ChatGPT" hero word | continuous (off-beat) |
| S33 | 1176–1199 | 49.000–49.958 | `49.000s_S33_f1196.png` | "ChatGPT is the interface" + capsule outlines draw around it + connector line | camera pan right |
| S34 | 1200–1222 | 50.000–50.917 | `50.000s_S34_f1212.png` | Pan along line to "gojiberry" node; node line forks | continuous |
| S35 | 1223–1251 | 50.958–52.125 | `50.958s_S35_f1250.png` | Fork → 3 chips: Intent Signals / Lead Scoring / AI Outreach | hard cut |
| S36 | 1252–1281 | 52.167–53.375 | `52.167s_S36_f1266.png` | "From one prompt" ember reveal, then reverse-ember + blur shrink | hard cut to blur (on-beat, beat 92) |
| S37 | 1282–1311 | 53.417–54.625 | `53.417s_S37_f1300.png` | Blur-in DM close-up: "Perfect, booked. See you then!" | hard cut |
| S38 | 1312–1343 | 54.667–55.958 | `54.667s_S38_f1326.png` | "Install Plugin" pill; cursor clicks; pill stretches into composer | morph + zoom |
| S39 | 1344–1455 | 56.000–60.625 | `56.000s_S39_f1395.png` | Big prompt bar types "Find 50 ideal prospects, personalize the messages, and start the outreach"; send clicked (on-beat, beat 103); arrow rotates up | shrink-to-logo |
| S40 | 1456–1556 | 60.667–64.833 | `60.667s_S40_f1520.png` | End card: Gojiberry mark + "gojiberry" + "Your AI go-to-market team"; audio stops at 63.74 s | end |

### 2.1 Shot detail

#### S01 · f0–36 · Co-brand lockup
- Layout (settled f24): OpenAI blossom + "OpenAI" wordmark, grey "x" separator, Gojiberry mark + "Gojiberry" wordmark, all on one baseline, centred at y≈540. Ink bbox f24: x 376–1607, y 465–614 (1231×149).
- Build: f0 blossom + "O" already present at left (x 242–545); the Goji mark is spinning in 3D about its vertical axis (edge-on at f0, f8; face-on f2–6, f12); roughly 1–1.5 turns over f0–f13 (turn count estimated from 2-frame samples), decelerating. "OpenAI" types one letter per ~2 frames: "O" f2, "Op" f4, "Open" f8, "OpenA" f10, "OpenAI" f12. Group recentres (left edge 242→368 by f15, ease-out).
- f14: separator "x" (thin, `#BBBBBB`, ≈24 px) fades in; mark settles in full colour (coral→crimson gradient `#F05A5A`–`#F06C60`).
- f17–20: "Goji" → "Gojiberry" types in crimson `#EA485A`, letters spaced; f21–23 the wordmark tightens ("Goji berry" gap closes) and **mark + wordmark crossfade to black** (`#111`); co-brand monochrome.
- f24–36: whole lockup scales down accelerating (ease-in): width 1231, 1223, 1213, 1202, 1188, 1172, 1153, 1130, 1103, 1071, 1031, 979, 908 (f24…f36).
- Out: M3 cut at f37 (1.54 s, on beat 2) into S02 already zoomed 1.31× and still shrinking.
- Audio: sparkle/shimmer SFX visible in spectrum ≈0.6–1.5 s (high 7–10 kHz warbling line) under the wordmark type-on. Narration "What if you could run your outbound directly from ChatGPT?" 0.68–3.84 s.

#### S02 · f37–103 · ChatGPT home → composer → "Run my outbound"
- Settled layout (f44–47, scale 1.0): heading "What can I help with?" centred, ink x 681–1276, y 259–320; composer x 302–1687, y 452–627 (1385×175), radius 44 px, 2 px border `#A4A4A4`, white fill. Inside: placeholder "Ask anything" at (341, 492) 26 px `#9D9D9D`; "+" icon at (≈350, 575) and a "sliders/tune" icon to its right (both `#2C2C2C`, ≈22 px); right side: mic icon in a 38 px white circle with 1 px `#DDD` border, then a 38 px black circle with white voice-waveform bars.
- f37–44: zoom-out from 1.31× to 1.0× (composer widths 1807, 1663, 1540, 1467, 1424, 1398, 1387, 1375); expo-out, ~60 % of remaining distance per frame. Heading words use M1 ember reveal ("help", "with?" still orange/blurred at f37, black by f42).
- f45–56: camera push-in onto the left half of the composer (≈2.3× by f56; composer left edge lands at x≈288, top y≈386; heading now huge and cropped top-right at y≈560–610 on the canvas top). Right side of composer fades out (M4). Ease-in-out, 11 frames.
- Cursor (§5 path C1) comes up from the bottom-centre: f50 tip (882, 820) → f55 (734, 548) → f60 (722, 470); press f61 (scale 0.52), ripple f61–f75. Caret (coral, 3 px × 44 px) appears f64 at text start.
- Typing "Run my outbound" (Regular, ≈46 px on canvas at this zoom, `#111`): "R" f65, "Ru" f66, "Run" f67, "Run m" f71, "Run my" f72, "Run my o" f75, "Run my ou" f77, "…outb" f78, "…outbo" f80, "…outbou" f81, "…outboun" f82, "Run my outbound" f84. Mean ≈1.3 frames/char with a 3-frame pause at the word gap.
- During typing: slow push 1.0→1.12 (composer height 332 → 372 px, f64→f88), cursor leaves up-left accelerating f71–f80 (tip (708,454) → (240,158)), fading out at f80–81.
- f96–103: camera pans right (text slides left through a left-edge fade mask; "Run my outbound" → "…outbound" → gone by f103). ~70 px/frame, ease-in.
- Out: whip-pan hard cut f104 (4.33 s, on beat 7); incoming tile continues leftward motion.
- Audio: low-band hit at 4.55 s (tile arrival).

#### S03 · f104–135 · Gojiberry app tile + wordmark
- Tile: white squircle 440 px (with soft shadow bbox 463), radius ≈22 %, fill gradient `#FFFFFF` (top) → `#EEEEEE` (bottom), shadow 0 20 40 rgba(0,0,0,.06). Mark centred inside at ~50 % tile width: three facets: peach square top-left `#F9C08B`, coral left chevron arm `#F4816F`, crimson right arm `#EB4C5E`.
- Motion: f104 tile at x 998–1215 (mark bbox), f105 826–1042, … slides left to x≈502 by f117 (expo-out, 13 frames) while scale drops from ≈1.0 to 0.47 (tile 463 → ≈218 px). Wordmark "Gojiberry" (Medium, ≈130 px, `#333`) appears to the right letter-by-letter: each letter fades in pink `#F2A09A` with wide tracking (+0.3 em) and cools to `#333`, tracking closing to 0; "G" f106, "o" f107, "j" f108, "i" f109, "b" f110, "e" f112, "r" f114, "r" f115, "y" f116; fully dark by f120.
- f117–126: group drifts left/down-scales slightly (right edge 1717 → 1450).
- f126–133: wordmark slides left *behind* the tile (masked by it), tile moves to centre (x 621–1233 → 719–1092), so only the tile remains.
- Out: continuous into S04.
- Narration: "Meet Gogi," 4.78–5.52 s; wordmark completes at f116 (4.83 s) exactly on "Meet".

#### S04 · f136–167 · White tile → orange app icon
- f130–140: tile shrinks to 253 px (bbox 830–1083); ease-out.
- f141–147: re-skin: the tile fills with orange gradient (TL `#F9BF91` → BR `#F4806F`) while the mark turns white (the three facets whiten, peach facet last), and tile grows to 333 px (f147, bbox 785–1133 incl. glow) = overshoot; f147–158 settles to ≈307 px (f155: 806–1113 × 385–693, centred (960,539)), radius ≈70 px (squircle; straight edge begins 56 px in).
- f158–167: slow shrink to 257 px (anticipation).
- Audio: second sparkle SFX ≈5.5–6.3 s; narration "your entire outbound engine inside ChatGPT" 5.90–8.90 s.
- Out: f167 the icon dissolves into halftone dots (dot grid visible inside it at f167), f168 burst.

#### S05 · f168–210 · Halftone iris → ChatGPT desktop window
- Halftone: square grid of round dots, pitch ≈16 px, dot Ø 4–10 px, colours `#E89030`/`#E8B880`/`#D8A060`/pale `#FCEACC`. It is a ring (annulus) whose hole reveals the ChatGPT window underneath. Orange extent per frame (bbox width): f167 242 · f168 470 · f169 720 · f170 968 · f171 1172 · f172 1376 (then clipped to the window rect 1376×~980). Hole radius grows faster than outer radius (the ring thins). f172–181 dots vanish randomly (count 174k → 1.1k pixels by f181); gone f182.
- Window (macOS app, light): f178 bbox 271–1648 × 32–1046 (1377×1014). Contents (at f206 scale, window left ≈301): traffic lights (red/yellow/green 20 px) top-left; sidebar ≈260 px wide, fill `#F9F9F9`, items "New chat" (pencil icon), "Search chats ⌘K" (highlighted row `#EFEFEF`, radius 10), "Library 11"; bottom history list appears one item per ~3 frames f186–208: "Gourmet Food Truck Trends", "Digital Art Techniques", "Virtual Reality Experiences", "Local Music Scene Highlights", "Culinary Heritage Preservation", "Sustainable Fashion Innovations", "Community Gardening Initiatives" (last one lighter), sparkle icon bottom-left. Top bar: OpenAI blossom + "ChatGPT ⌄" (left), "Temporary" with dashed-clock icon + round avatar (right). Centre: "What can I help with?" and composer (placeholder "Ask me anything", "+", "⇆ Tools", mic circle, black circle with white →).
- Camera: f178→f197 slow linear zoom-out (width 1376 → 1316, −0.23 %/frame); f198→f210 accelerating zoom-in towards the composer's left end (ease-in; bbox 1316 → 1523+ wide, top edge leaves frame f208).
- Out: f211 zoom-through cut (M3) into 6× close-up. Cut lands 5 frames before beat 15.

#### S06 · f211–246 · "@Gojiberry" close-up
- Composer corner at extreme scale: border 3 px `#4A4A4A`, corner radius ≈120 px at f214; "+" glyph lower-left. Right side fades out (M4). Camera still zooming in (left edge x 492 f211 → 104 f238, decelerating) and drifting up.
- Typing (Bold, `#545454`, ≈150 px): "@" f213, "@G" f215, "@Go" f217, "@Goj" f219, "@Goji" f221, "@Gojib" f222, "@Gojibe" f224, "@Gojiber" f226, "@Gojiberr" f228, "@Gojiberry" f229 (~2 frames/char). Holds f229–238.
- Narration: "Just ask." 9.60–10.20 s → "@Gojiberry" completes at 9.54 s.

#### S07 · f247–318 · "Find 100 SaaS founders hiring salespeople"
- Text continues on the same line after "@Gojiberry " in Regular. The camera tracks the caret: the text's rightmost ink stays around x 830–1250 while typing and the line scrolls left through a left-edge fade (M4). "@Gojiberry" exits left by f262.
- Colour: characters arrive rose `#BA968A`, then within ~6 frames "Find 100 SaaS founders" becomes crimson→coral (`#EA6666` → `#F06C66`) while "hiring salespeople" settles to grey `#969696`.
- Type-on: "F" f239 … "Find 100" f254 … "SaaS" f266 … "founders" f282 … "hiring" f291 … "salespeople" f311 (≈1.8 frames/char, 41 chars in 73 frames).
- f313–318: whip left (≈120 px/frame, blur); "salespeople" exits.
- Narration "Find one hundred SaaS founders hiring salespeople" 10.66–13.40 s: text leads the voice by ~0.6 s.

#### S08 · f319–361 · "enrich their contact details"
- Words fade in (not typed) left→right at y≈490–592 (cap ≈80 px): "enrich" f316–317, "their" f319, "contact" f321, "details" f323–325; fresh words light grey, then the brand gradient (M2) sweeps across the whole phrase f325–333 (crimson at "enrich" → coral → peach at "details").
- Hold f333–345 with slow leftward drift (right edge 1807 → 1755, −4 px/frame) and ~0.5 % shrink.
- f346–361: phrase scrolls **up** out of frame accelerating (ink top y 488 → 344 by f361; 2, 7, 14, 21, 35, 68 px/frame), fading.
- Narration "Enrich their contact details," 13.84–15.36 s.

#### S09 · f362–399 · "write a personalised message"
- Enters from below while the previous phrase leaves (vertical push): ink top y 603 (f364) → 556 → 529 → 512 → 502 → 497 → 495 (f382), expo-out. Line is rotated ≈ −1.5° (left end higher) and straightens by f380.
- Colour: "write a" crimson, "personalised" coral, "message" peach→grey (M2), sweep f365–378.
- Hold drift f382–391 (≈−12 px/frame), f392–399 whip left and out.
- Note spelling on screen is British "personalised"; narration says "personalized" (15.66–16.96 s).

#### S10 · f400–450 · "and launch the campaign."
- f400 white; words fade in grey from centre-left: "and" f401, "launch" f403, "the" f405, "campaign" f407–409 (ink x 238–1271 at f406 → 143–1778 at f409). "campaign." in coral/orange gradient (`#F07E72` → `#F0A27E`), rest `#969696`.
- f409–448: constant leftward drift ≈12 px/frame (right edge 1798 → 1248); no scale change.
- f449–450: whip left, "campaign." exits; send button enters from the right edge.
- Narration "and launch the campaign." 17.24–18.30 s.

#### S11 · f451–470 · Send button
- Black circle (`#000`), white "→" arrow (stroke ≈9 % of Ø, rounded caps). Diameter / left x per frame: f452 210/1510 · f453 214/1364 · f454 222/1257 · f455 232/1172 · f456 245/1101 · f457 263/1039 · f458 284/984 · f459 310/934 · f460 342/887 · (cursor overlaps) · f464 496/733 · f465 527/708 · f466 551/689 · f467 566/678 · f468 573/673 (centre ≈(960,537)). Horizontal travel is expo-out; size growth is ease-in then ease-out (a camera push).
- Cursor C2 enters bottom-right: f461 tip (1582,798) → f462 (1270,688) → f463 (1118,622) → f464 (1036,580) → f465 (988,554) → f466 (966,540) → rests at (956,538) f467–469. Cursor is large here (≈110 px).
- Narration "Gogi finds prospects…" 18.78 s; the button lands on "Gogi" (on-beat, beat 32 at 18.79 s).

#### S12 · f471–488 · Press → pixel burst → drop
- Press: button Ø 569 (f469) → 531 (f470) → 397 (f471) → 357 (f472) → 351 (f473, min, 0.61×) → 356 → 368 → 389 → 425 → 483 → 541 → 579 (f480) → 601 → 613 → 619 → 621 (f484). Cursor presses f471 (scale 0.74).
- Inside the button f471–473 the black fill briefly pixelates (16 px blocks, dark reds); the burst is born from the button.
- Pixel burst: square tiles ≈40–48 px, colours `#F69C8A`/`#F6B4A8`/`#F6C6BA`/`#F6D2CC`, random opacity 0.3–1, arranged as a ring expanding from the button: ring radius ≈190 px (f472) → ≈290 (f474) → ≈520 (f476) → ≈800 (f478) → off-frame by f482; tiles fade randomly f478–487.
- Drop: from f480 the button centre moves down (y 736 → 1059 → off-frame bottom at f488) while the chat bubble (S13) slides down from above (camera tilts up to it). Cursor rides down with it (tip y 656 → 960, f480–492) and leaves the bottom f493–495.
- Audio: low-band hit at 20.37 s (f489).

#### S13 · f489–516 · User bubble + "Working…"
- Bubble (f506): x 78 → beyond right edge, y 371–727, radius ≈90 px, fill `#CDE7FE`, border 3 px `#3C404B`. Content: app tile 72 px (white tile, mark) at (160, 430); text Regular ≈64 px in three lines: **"Gojiberry"** (Bold `#3C4044`) + "Find 100 SaaS founders currently hiring salespeople, enrich / their contact details, write a personalized message and launch the / campaign." (`#5F646B`; line 1 runs off the right edge; full sentence reconstructed; **NOT PINNED** beyond what is visible). Below bubble: "Working..." Regular ≈58 px `#9A9A9A` at (160, 785).
- Motion: bubble arrives blurred from the top f486–495 (blur 6 → 0), camera drifts left/down; the prompt text in the bubble gets a red highlight sweep (M2 in `#E0485A`) f509–516 over "Find 100 SaaS founders…".
- "Working…" shimmer: a crimson band sweeps left→right across the grey letters; "Wo" red at f490, "rking" red at f496; period ≈ 12–14 frames (~1 beat). **Shimmer period NOT PINNED**.

#### S14 · f517–527 · Zoom-through the "o"
- f517–523 violent zoom into "Working" (radial/zoom blur growing to ≈40 px, letters stretch), camera centre on the "o". f522: the counter of "o" already shows avatar photos inside. f524–527: the "o" ring (crimson `#E84458`, zoom-blurred) passes the camera; the avatar scene is behind it at full sharpness. f528 ring gone.
- Cut 7 frames after beat 37 (off-beat). Side-channel shows a noise swell/riser 20–22 s peaking here.

#### S15 · f528–575 · Avatar cloud → Maya
- Six square headshots, corner radius ≈22 %, each with a centred label "Analysing Lead..." below it (Semibold ≈20–30 px, brand gradient crimson→peach). Positions at f530 (tile boxes, approx): older Black man in suit 265–650 × 700–1005 (top-left, biggest); blonde woman 1045–1420 × 560–880 (top-right); **Maya** 870–1050 × 845–1030 (centre, small ≈180 px); older white man laughing 1320–1605 × 820–1115; young Asian man 590–845 × 1100–1395; Black man with beard 1110–1585 × 1250–1570 (these last extend below frame).
- Camera: steady push toward Maya (Maya tile 180 px f530 → 231 f545 → 294 f565 → 330 f576), others slide outward and exit edges (parallax: bigger = closer = faster).
- Narration "…showing real buying signals, like founders building their sales teams," 20.10–23.86 s. Music: beat percussion starts ≈23.4 s.

#### S16 · f576–620 · Maya person card
- Final layout (f620, card still moving): photo 426×≈490, radius ≈120 px; right column starts ≈70 px right of photo:
  1. Gojiberry chip (tile 28 px + "Gojiberry" Medium `#3D3D3D`)
  2. "Maya Estêvão" (Regular, `#1D1D1D`)
  3. "Founder at OpenBundle" (`#929292`)
  4. "Email:" (`#929292`) / "[email redacted]" (gradient tan `#C9A184` → rose `#B85D6C`)
  5. "Phone:" / "[phone redacted]" (`#2B2B2B`)
  6. "LinkedIn" (`#929292`) + LinkedIn "in" square icon (`#0A66C2`, radius 6)
  7. "[url redacted]" (`#929292`)
  8. three icons: copy, thumbs-up, thumbs-down (`#0D0D0D`, outline 2 px)
  (Proportions at f700: photo 583×666 at x 415–998, y 213–880; text column x 1057; row baselines y≈253, 333, 380, 471, 514, 591, 643, 712, 795, 860.)
- Reveal order: "Analysing Lead…" label under Maya fades f576–583; chip + name type f576–584 (name typed "Maya Estêv…"); title f584–588; email label + address f588–600 (typed, M2 gradient); phone f600–607 (digits type, trailing digits light); LinkedIn row f607–612 (icon pops scale 0→1); url + icons f612–616.
- Camera: slow push (photo 330 → 426 px f576→f620) with the card translating left; from f612 the card **accelerates left** (photo left x 464 f616 → 424 → 376 → 304 → 208 f620).
- Out: whip to white (f621–622 blank), 4 frames before beat 44.
- Narration "enriches their contact details," 24.08–25.70 s.

#### S17 · f621–685 · "Brings the right context into every message"
- M1 ember reveal, Semibold ≈82 px, single line centred at y 498–575. Word timing: "Brings the" f623, "right" f625, "context" f627, "into" f629, "every" f631, "message" f633 (right edge 1919 overshoot → settles 1816 by f640). Full black by f640. Line ink width 1540 at f640 (x 275–1815).
- f640–672: slow drift left ≈3 px/frame (x 275 → 182).
- f673–683: whip left (left edge 172, 151, 119, 73, 13, −, …; right edge 1703 → 572) with horizontal motion blur and x-squash; f684–685 white.
- Narration "and brings the right context into every message." 26.06–28.94 s (text leads ~0.3 s).

#### S18 · f686–711 · Card + LinkedIn click
- Hard cut to the card larger (photo 583 px, layout listed in S16) with slow push.
- Cursor C3 enters from bottom-right: f698 tip (1544,1008) → (1456,952) → (1384,902) → (1332,858) → (1292,824) → (1264,800) → (1244,784) → f705 (1230,778); press f706 (scale 0.7) on the LinkedIn icon (1210, 712).
- f707–711: camera zooms toward the icon with gaussian blur ramp (0 → ≈12 px); out to S19.
- Narration "So, 'Hi, Maya,'" 29.38–30.48 s.

#### S19 · f712–750 · LinkedIn DM window
- Window (settled f730): x 395–1500, y 135–897 (1105×762), radius ≈70 px, fill `#FDFDFD` with a faint warm bottom-right tint `#FBFAF6`, 1 px hairline `#F0F0F0`, very soft shadow. Header: LinkedIn logo tile 76 px (`#0A66C2`, white "in") at (470,190); avatar 104 px circle with green online dot (`#13CC29`, 24 px, white ring) at (612,165); "Maya Estevão" Semibold ≈40 px `#141516`; "Founder at OpenBundle" ≈28 px `#54555E`; right icons video-camera, "•••", "✕" (`#414852`, ≈50 px); divider y 300 `#F4F4F4`. Message: blue bubble "Hi Maya!" (fill `#2A6DE2`, text white Medium ≈40 px, pill radius 50, box 1037–1295 × 371–468) + sender avatar 108 px circle (young man, suit) at (1343,388). Composer: rounded rect 443–1478 × 757–857, radius 50, border `#EBEBEB`, placeholder "Write a message..." `#7F838B` ≈36 px, icons paperclip, smiley (`#555`), send arrow (`#2A6DE2`).
- f712–716: blur-in from ≈14 px to 0 while scale settles (window bbox 574–1393 at f716 → 395–1500 f730: ease-out zoom-out).
- f740–747: backspace "Hi Maya!" → "Hi May" → … → "" (≈1 char/frame); bubble shrinks to a 44 px blue dot (f747–756).
- f745–750: camera push-in accelerating toward the bubble (bbox 339 → 135 left).
- Narration "becomes," 30.80–31.30 s = deletion.

#### S20 · f751–802 · "Saw you're growing your sales team"
- Close-up (≈2.3×): blue dot bubble at right with avatar; header cropped at top ("…ounder at OpenBundle"). Typing, white text Regular ≈64 px: "S" f757, "Saw" f760, "Saw y" f761, "Saw you" f762, "Saw you'" f763, "Saw you're" f764, "…g" f766, "…gro" f767, "…growing" f770, line 2 "yo" f772, "you" f773, "your" f774, "your sa" f776, "your sal" f777, "your sales" f778, "your sales t" f780, "…tea" f781, "your sales team" f782. Each new glyph enters at 40 % opacity with a light-blue tint and settles in 3 frames. Bubble width/height grow with content (spring, no overshoot visible).
- f782–802: slow push + drift right (bubble 83–656 at f790 in half-scale grid → ≈1150 px wide on canvas).
- Narration "'Saw you're growing your sales team.'" 31.64–33.08 s.

#### S21 · f803–851 · Maya typing
- f803–806 whip down/left (the bubble exits top-right, blurred) revealing the left/lower part of the DM: Maya avatar 120 px, grey typing pill (`#E6E7E9`, ≈135×80, radius 40) with three dots (`#9D9EA2`, Ø 18, gap 10) and a tail circle Ø 10; composer "Write a message..." below. The blue "…your sales team" bubble corner peeks top-right.
- Hold f806–845 with slow push; dots animate (sequential pulse; **period NOT PINNED**).
- f845–851: zoom-in + gaussian blur + fade to white.
- Narration "A real reason to reach out." 33.46–35.08 s.

#### S22 · f852–866 · "Launch" pill
- f852 pill pops from scale ≈0.1 at centre: bbox width f853 379 (incl. cursor) … settled pill ≈370×98 at x 774–1144, y ≈505–603; fill `#FDFAF1`, radius 20, bottom edge 2 px `#F6EDDE` + soft drop shadow; text "Launch" Medium ≈64 px `#010100`.
- Cursor C4 from bottom: f854 tip (1066,706) → (1036,654) → (1020,622) → (1008,602) → (998,588) → (992,578) → (988,570) → (984,564) → (982,560) → (980,556) → f864 (978,554); expo-out. Press f865 (scale 0.66) → release f866. Pill lights up warm (`#F8D89C` glow) on press.
- Narration "Then launch your campaign" 35.68–36.92 s; press lands on "launch" (35.98–36.24) = beat 62 (36.09 s). Music drops into full energy here (+8 dB side level, §6).

#### S23 · f867–903 · Tile explosion → avatar storm
- f866–870: ~30 orange squircles (`#F29433`, 70–140 px, radius 22 %) burst from behind the pill radially, overlapping, ease-out; each has a photo underneath: the orange overlay wipes off top→bottom (f868–880) revealing a diverse headshot (the tile keeps a faint orange tint at the bottom edge while wiping).
- f870–903: camera pushes in on the pill (pill width ≈430 f872 → 464 f892 → 570 f900) while tiles fly past and outward (parallax, tiles near centre small, edges big), some exiting frame. Pill drifts up (centre y ≈560 → ≈600 then up to 600→?).
- Cursor leaves up-left accelerating f866–878 (tip (978,550) → (638,240)).
- Audio: strongest low-band impact of the film 36.83 s (f884); dense music begins.

#### S24 · f904–916 · "Right here"
- f903 "Right" appears small bottom-right in orange; f904–911: "Right" zooms in from bottom-right (Semibold ≈330 px) while "here" enters lower (baseline +60 px) and rises; ember colour: "Right" `#C7620B` f905 → brown f907 → `#1E1406` f912. Settled ink f912: x 204–1683, y 441–745.
- Narration "right here" 37.76–38.40 s.

#### S25 · f917–942 · "Right here in ChatGPT" → composer
- f917 cut down in scale: "Right here" black ≈88 px, "in" (f917) and "ChatGPT" (f919–921) ember-orange → black by f928; line x 534–1410 at f925, y 499–582.
- f930–940: the line splits: "Right here" moves left, "in ChatGPT" right, and a tiny pill outline (composer, 2 px `#999`) grows in the gap from width 0 to ≈250 px (f940).
- f941–942: the pill balloons (scale ×3) into the composer, words exit sideways; motion-matched into S26.

#### S26 · f943–982 · Drag-in + prompt
- Composer (f975): x 152–1776, y 347–760 (1624×413), radius ≈205 px (fully rounded ends), border 2 px `#878787`, fill white → `#FAF9F5` (right) with warm cream glow. Contents: chip tile 102 px (vertical `#EF5766`→`#F8B990`, white mark) at (231,402); text Regular ≈66 px: **"Gojiberry"** (Semibold `#121212`) " launch a LinkedIn outbound / campaign targeting SaaS founders in the US." (`#2E2E2B`); new words arrive in ember/orange (`#F5A623`-ish) and cool to ink; "+" and sliders icons `#595959` at (260,640) and (422,640); mic outline circle 124 px at (1478,640); black send circle 124 px with white "↑" at (1640,640).
- f943–957: camera settles on the composer (zoom-out from S25 move); a **grab hand** cursor (white glove, black outline, ≈70 px) carries a Gojiberry chip tile (≈60 px) from below the composer (f944: (1550,265) in S25's scale) to the text start (f952 ≈(160,520)); f957 drop; tile snaps into the chip slot, "Gojiberry" label appears in orange f958 and turns black.
- f958–976: prompt types word-by-word (≈1 word/frame): "launch" f959, "a" f960, "LinkedIn" f961, "outbound" f962, line 2 "campaign" f964, "targeting" f965, "SaaS" f966, "founders" f967, "in" f968, "the" f970, "US." f971. Hand exits up f962–964.
- Camera: slow zoom-out through the shot (composer grows from off-frame to fully visible), slight upward drift f976–982.
- Narration "right here in ChatGPT." ends 39.52 s; "Gogi flags interested prospects" 40.02–42.04 s.

#### S27 · f983–1013 · "Goji flags interested prospects"
- M1 ember reveal, Semibold ≈89 px; words stagger with baseline offsets on entry ("interested" +10 px, "prospects" +30 px at f983) rising into line by f988. Ink f1000: x 370–1557, y 517–598. Black by f991.
- f1005–1013: drifts up (y −3 → −12 px/frame).
- Note the on-screen text says "Goji", narration says "Gogi" (brand "Goji").

#### S28 · f1014–1031 · Orange unfold → DM with Maya's reply
- f1014: pale-orange (`#F5C28E`) rounded shapes shaped like a chat bubble + tail, Maya avatar (orange-tinted) and her name/title float at centre-right. f1016–1022 they expand into the full DM window (x 1240–1627 at f1018 in half-grid → window ≈780 px wide) while an orange gradient overlay fades bottom-up (top clears first).
- Incoming grey bubble (`#EDF1F4`, radius 30) types Maya's reply: "Mostly." f1016, "What" f1018, "do" f1023, "you" f1027, line 2 "guys offer?" f1030. New words arrive peach/orange, then ink `#151E1F`.
- Window settles f1031 (at f1050 window x 1150–1717 in half-grid ⇒ canvas ≈380–1520 at 0.8× of S19 size).

#### S29 · f1032–1065 · "Thinking of the best reply"
- Pill (white, radius 60, 1 px `#EEE` border, soft shadow; ≈380×110 at the f1050 scale) slides in from off-frame left (f1036 partially visible at x≈0 → settles f1044 at ≈(1035,918) in the half grid ⇒ bottom-left of the DM, overlapping the composer). Contents: coral circle (56 px, gradient `#F28571`→`#EE5A60`) with white Gojiberry mark; two-line text "Thinking of the / best reply" Regular ≈40 px `#797979` with a shimmer (grey→white highlight sweep, period ≈1 beat).
- Slow push on the window f1044–1065.
- Narration "and instantly suggests a reply" 42.08–43.84 s.

#### S30 · f1066–1110 · Approved reply
- f1063–1070: camera jump-zooms (≈2×) toward the composer area with gaussian blur up to ≈10 px (f1066–1068) clearing by f1071; during the blur the pill **turns green and collapses into a circle**: green `#1CC628` Ø ≈108 px, white check stroke 8 px (f1070).
- Outgoing blue bubble (`#2A6DE2`, radius 40, tail bottom-right) types white Regular ≈46 px: "We help" f1070, "teams scale" f1072, "content" f1076, "without" f1077, "hiring." f1078, "Worth a" f1080, "quick" f1082, "chat?" f1083. New words enter orange `#F5A55A` then white.
- Maya's grey bubble "…What do you / …offer?" cropped top-left; composer icons (paperclip, smiley, blue send) under.
- f1085–1110: slow drift up (≈3 px/frame), push-in slight.
- Narration "for you to review and approve." 43.92–45.54 s; "All that's left is to book the meeting." 46.08–47.90 s.

#### S31 · f1111–1153 · Calendar
- Day view: hour labels "1 PM", "2 PM", "3 PM" (Regular ≈46 px `#808080`) right-aligned at x≈1095 (f1135); horizontal lines `#E3E4E8` 2 px at hour marks (spacing ≈172 px); vertical column line at x≈1132 and ≈1795.
- Cursor C5: enters bottom f1111 tip (994,798) → (976,774) → (964,758) → (956,746) → presses f1115 (scale 0.65) at (950,734) and **drags up** keeping pressed: (948,722) f1116 → (944,694) f1118 → (942,642) f1120 → (942,548) f1122 → (942,486) f1124 → (942,466) f1125; release f1126–1127 (scale back 0.8 → 1.0).
- Event block: appears f1121 as a thin light bar on the 2 PM line (`#A2DEF6`, ≈630×30, radius 16), grows upward with the drag to 1:15 (≈630×165 by f1127), colour saturating to `#13A7DE`. Text white: "meeting with Maya - Founder" / "@OpenBundle" (Medium ≈40 px) and "1:15-2:15pm" (≈30 px, 80 % white).
- Cursor exits up-left f1131–1137 accelerating ((938,404) → (776,190)).
- Camera: slow zoom-out f1140–1153 (reveals "3 PM" and a 4th label that reads **"4 AM"**: a typo in the source; use "4 PM" unless matching 1:1).
- Narration: "book" 47.18–47.40 s ≈ release f1126 (46.92 s).

#### S32 · f1154–1175 · "Chat" → "ChatGPT"
- "Chat" ember-orange Medium ≈190 px enters f1154 from slightly below/right, cools (f1154 `#EE8319`… f1160 ink); "GPT" appears f1161 in orange with +30 px baseline drop and rises/cools by f1168. Ink f1170: x 584–1290, y 475–619.
- f1168–1175: shrink ≈0.6 %/frame (prepares next shot).
- Narration "ChatGPT" 48.24–49.12 s.

#### S33 · f1176–1199 · "ChatGPT is the interface" + capsule
- f1176 scale jump down (≈94 px text); "is" f1176, "the" f1178, "interface" f1180 (ember). Line centred.
- f1179–1196: capsule outlines draw around the line: strokes 3 px `#3A3A3A`→`#666`, drawn as paths (stroke-dashoffset) that start at the right end, run left along the bottom, round the left end and return along the top (clockwise on screen), 1 → 5 concentric capsules offset ≈15–60 px apart, each slightly lighter/larger (f1183 two, f1188 four, f1196 five with outermost ≈1580×455). A connector exits the right end: dot Ø 36 (`#5A4A3A`→`#393939`) at the capsule's right apex, then a 3 px line → further dot.
- Camera: slight zoom-out f1183–1199; starts panning right at f1197.
- Narration "ChatGPT is the interface." 48.24–50.04 s.

#### S34 · f1200–1222 · Line to the gojiberry node
- Camera pans right (ease-in-out, ≈230 px/frame at peak f1203–1207): the capsule exits left; the line runs to a node Ø 36 at x≈(718 in f1212 canvas) then the small Gojiberry lockup (mark 34 px + "gojiberry" ≈70 px `#1E2226`) with a short line + dot Ø 20 continuing right.
- f1216–1222: the lockup slides left and **fades**, leaving the line; the right line end morphs into a fork (a vertical arc with two dots ±130 px, drawn f1219–1223).
- Narration "Gogi is the engine." 50.42–51.72 s (the node lands on "Gogi").

#### S35 · f1223–1251 · Feature chips
- Three parallel lines (3 px `#393939`, fading to transparent at left) ending in dots Ø 36 at x≈530 (top), 449 (middle), 530 (bottom) at y 256, 538, 828 (f1250). Chips to the right: orange circle icons Ø 150 (radial `#F2AD5F` body, `#F69632` edge-bottom, rim light `#FFE1C0`) with dark-brown glyph overlays; target/dart (Intent Signals), person + star badge (Lead Scoring), paper plane (AI Outreach). Labels Medium ≈95 px `#010000`.
- Order: "Lead Scoring" first (f1224, centre, typed left→right with per-letter M1: letters arrive orange `#D28328` and turn black), "Intent Signals" f1230, "AI Outreach" f1236. Icon pops in scale 0.6→1.0 (ease-out back, 5 frames) before its label.
- Camera slow zoom-in (≈0.4 %/frame).
- Narration "From one prompt" 52.14 s → cut to S36 at f1252 (52.17 s).

#### S36 · f1252–1281 · "From one prompt"
- M1: "From" f1252, "one" f1254, "prompt" f1256 (Semibold ≈86 px) ink x 669–1282; black by f1263.
- f1270–1281: **reverse ember**: text turns orange again, shrinks (≈3 %/frame) and blurs out (blur 0 → 6 px), opacity → 0.4.
- Out: hard cut to a heavily blurred bubble (on-beat, beat 92).

#### S37 · f1282–1311 · "Perfect, booked. See you then!"
- f1282 gaussian blur ≈20 px → sharp by f1289 (ease-out). Close-up of the DM: outgoing blue bubble (`#2A6DE2`, radius ≈50, tail) with white Regular ≈64 px text; avatar right; Maya's grey bubble cropped top-left showing only "…ay at 2?" (full text **NOT PINNED**: likely "Tuesday at 2?"); composer icons bottom.
- Typing: "Perfect," f1283, "booked." f1287, "See" f1291, "you" f1294, "then!" f1296 (new words orange → white).
- f1300–1311: slow drift up/right.
- Narration "to booked meetings." 53.24–54.08 s.

#### S38 · f1312–1343 · Install Plugin → composer
- "Install Plugin" pill (same style as Launch, ≈300×95 at f1316, text Medium ≈62 px `#111`) at centre, drifting slightly.
- Cursor C6 from bottom-right: f1314 (1100,764) → (1056,698) → (1028,658) → (1010,630) → (996,610) → (984,594) → (976,582) → (970,572) → (964,564) → (960,558) → (958,552) → (956,548) f1325; press f1327 (scale 0.5), pill turns warm gold `#F8D89C`; release f1328–1330; cursor exits up-left f1330–1337 ((938,534) → (374,268)).
- f1334–1343: the pill **stretches horizontally** into a composer (width ×4, height ×0.7): "Install Plugin" text fades, "+", sliders icons and a black send dot fade in; border becomes 2 px grey.
- Narration "Install the plugin using the link below the video" 54.92–57.46 s (click on "plugin" 55.48 s).

#### S39 · f1344–1455 · Final prompt + send
- Composer grows (camera push, ease-out) f1344–1374 until it fills the width (bbox x 14–1907, y 277–1017 by f1374). Border 3 px `#666`, radius ≈170, fill white→cream (`#FBEFDD` radial glow right-centre).
- Typing (Regular ≈108 px): starts f1349 "F" (ember orange), "Find" f1351, "Find 50" f1352, "ideal" f1354, "prospects," f1360–1367, "personalize" f1370–1375, "the messages," f1376–1379, "and start the" f1380–1383, "outreach" f1384–1399. Words arrive orange then cool to ink `#1B1B1B`. Camera pans right with the caret from f1368 (line scrolls left through left-edge fade).
- Send button (black circle Ø ≈130 at f1400, white "→") slides in from the right edge f1388–1392.
- f1400–1416: camera push-in toward the bottom-right corner of the composer (corner radius visible, border thickens to ≈5 px).
- Cursor C7 (large, ≈190 px) enters bottom-right f1413–1418, settles on the button f1428 (tip ≈(1000,570)); **press f1433–1434** (button greys to `#555` and scales 0.9), release f1435–1438.
- f1440–1455: arrow rotates −90° from "→" to "↑" (ease-in-out, ≈12 frames) and the button returns to black with a 4 px grey ring `#555`; cursor exits up-left accelerating f1444–1454.
- Narration "and run your outbound directly from ChatGPT." 57.64–60.42 s; press on "from" (59.34–59.50); beat 103.

#### S40 · f1456–1556 · End card
- f1456: the button collapses; f1457–1458 the crimson and coral facets of the mark flip in (3D Y rotation, edge-on at f1457), peach square last; f1459 wordmark "gojiberry" appears with wide tracking and tightens: lockup width 866 (f1459) → 827 → 794 → 775 → 763 → 754 → 748 → 742 → 738 → 734 → 731 (f1469) → 718 (f1476) → 710 (f1480); expo-out.
- f1480–1490: tagline "Your AI go-to-market team" rises from below word by word ("Your" f1480, "AI" f1482, "go-to-" f1484, "market" f1486, "team" f1488), each from +20 px / 0 opacity; lockup shifts up 30 px (y 463 → 433) ease-out.
- Final layout (f1520): mark x 629–717, y 462–560 (88×98); wordmark x 763–1303, y 436–564 (`#111619`); tagline x 631–1307, y 607–660 (`#131313`). Whole block x 629–1307 (678 wide, centred at 968), y 436–660.
- f1500–1556: slow linear zoom-out (block width 694 → 678 f1520 → 651 f1556, ≈−0.11 %/frame).
- Audio stops dead at 63.74 s (f1530); f1530–1556 are silent. No fade to black; the last frame is the white end card.
- Narration "Gogi Berry," 60.94–61.58 s (logo appears 60.79 s); "your AI go-to-market team." 61.92–63.68 s (tagline appears 61.67–62.00 s, ahead of the voice).

---

## 3. Component inventory (build each as an HTML/CSS component)

Sizes are "at 1×" = the size in the most frontal, settled frame noted; the camera scales them afterwards.

1. **Cursor (arrow)**: see §5. Black fill `#000`, white 5 px outer stroke (at ~96 px size), drop shadow `0 6px 10px rgba(0,0,0,.28)`. Rotated ≈ −12° from the standard macOS arrow (tip up-left, tail down-right, no stem notch).
2. **Grab-hand cursor**: macOS closed/grab hand, white glove fill, 3 px black outline, ≈70 px; carries an app tile under the palm (S26).
3. **Click ripple**: ring stroke ≈14 px, colour `#F2A49A`, gaussian blur 3 → 10 px, radius 19 → 38 → 56 → 75 → 94 → 106 → 119 → 131 → 144 px on frames +0, +1, +2, +3, +5, +7, +9, +11, +13 after press; opacity 0.9 → 0 (linear from +4). Centre = cursor tip.
4. **Co-brand lockup**: OpenAI blossom (black), "OpenAI" wordmark, "x" separator (`#BBB`, light), Gojiberry mark (colour → black), "Gojiberry" wordmark (Medium). Height ≈150 px, width 1231 at f24.
5. **Gojiberry mark**: three flat facets on a 1:1.1 box: peach square (top-left, `#F9C08B`), coral left arm going down to a centre point (`#F4816F`), crimson right arm rising to top-right (`#EB4C5E`), forming a ribbon "check/heart" shape. White version on orange tile. Monochrome black version in S01.
6. **App tile (light)**: 440 px squircle (iOS icon curve, radius ≈22 %), gradient `#FFFFFF`→`#EEEEEE`, 1 px `#EDEDED` border, shadow `0 20px 40px rgba(0,0,0,.06)`, mark ≈50 % width.
7. **App tile (orange)**: 307 px squircle, radius ≈70, gradient 135° `#F9BF91`→`#F4806F`, white mark (facets as white at 100/90/80 % opacity).
8. **Composer chip tile**: 102 px squircle, radius 24, vertical gradient `#EF5766`→`#F8B990`, white mark.
9. **Halftone iris**: dot grid pitch 16 px, dot radius driven by a noise field (2–5 px), colours `#E89030`/`#E8B880`/`#D8A060`/`#FCEACC`, masked by an expanding annulus and clipped to the window rect; dots die randomly over 9 frames.
10. **ChatGPT home (simple)**: heading + composer (§2 S02). Composer: 1385×175, radius 44, border 2 px `#A4A4A4`; icons "+", sliders; right: mic-in-circle (38 px, border `#DDD`), black voice circle (38 px) with 5 white vertical bars.
11. **ChatGPT desktop window**: macOS window (see S05) 1376×1014, radius 24, 1 px `#E5E5E5`, shadow `0 30px 80px rgba(0,0,0,.08)`; sidebar 260 px `#F9F9F9`; composer 890×110 radius 30 with "Ask me anything", "+", "⇆ Tools", mic circle, black → circle.
12. **Prompt pill/composer (late style)**: radius = height/2, 2 px `#878787` border, fill white with a right-side radial cream glow `radial-gradient(circle at 85% 60%, #FBEFDD 0%, rgba(251,239,221,0) 55%)`; mic outline circle + black send circle (white ↑ or →).
13. **Send button**: black circle, white arrow (stroke 9 % of Ø, round caps). Pressed: `#555`, scale 0.9. After send: 4 px `#555` ring, arrow "↑".
14. **Pixel burst**: 40–48 px squares on a 48 px grid, pink palette (§1.1), random alpha, ring-shaped spawn mask expanding ≈+150 px/frame, random per-tile death.
15. **ChatGPT user bubble**: fill `#CDE7FE`, 3 px `#3C404B` border, radius 90 (at 355 px height), inline app tile 72 px + bold "Gojiberry" + prompt text `#5F646B`.
16. **"Working…" status**: Regular, `#9A9A9A`, crimson shimmer band 120 px wide sweeping left→right.
17. **Avatar tile + "Analysing Lead..."**: square photo, radius 22 %, no border; label centred below, Semibold, brand gradient crimson→peach, ellipsis.
18. **Person card**: see S16 list; photo radius ≈20 % of width; label/value pairs: label `#929292` ≈30 px, value ≈44 px.
19. **LinkedIn DM window**: see S19. Outgoing bubble `#2A6DE2` (radius 50, tail bottom-right on multi-line), incoming `#EDF1F4` (tail bottom-left), avatars 104–120 px circles, online dot `#13CC29`.
20. **Typing indicator**: grey pill `#E6E7E9` ≈135×80, three `#9D9EA2` dots Ø18, tail circle Ø10 bottom-left.
21. **"Thinking of the best reply" pill**: white, radius 60, 1 px `#EEE`, shadow `0 10px 30px rgba(0,0,0,.08)`, coral Gojiberry circle icon 56 px, two-line grey shimmer text.
22. **Approve check**: circle `#1CC628` Ø108, white check 8 px round caps.
23. **Launch / Install Plugin pill**: fill `#FDFAF1`, radius 20, bottom border 2 px `#F6EDDE`, shadow `0 6px 14px rgba(120,90,40,.10)`, text Medium `#010100`; pressed: fill/glow `#F8D89C`, scale 0.96.
24. **Orange explosion tile**: squircle 70–140 px, `#F29433` overlay that wipes down to reveal a headshot beneath.
25. **Calendar day view**: labels right-aligned `#808080`, hour lines `#E3E4E8`, event block `#13A7DE` radius 16 with white text, drag-state `#A2DEF6`.
26. **Capsule ellipse graphic**: 5 nested stadium outlines around a text line, 3 px strokes `#3A3A3A`→`#777`, drawn with stroke-dashoffset, plus a connector: dot Ø36 + 3 px line.
27. **Node line + fork**: 3 px `#393939`, dots Ø36 (end) / Ø20 (small); fork = a semicircular arc, radius ≈130, with dots at both ends.
28. **Feature chip**: orange sphere icon Ø150 (radial gradient light top-left `#F2AD5F`, darker `#F69632` bottom, 3 px rim highlight `#FFE1C0`), dark-brown glyph, label Medium ≈95 px.
29. **End card**: mark 88×98 + "gojiberry" wordmark (540×128) + tagline Medium ≈56 px.

---

## 4. On-screen text (verbatim, in order)

Highlight = colour a word holds for more than a transient reveal. "Ember" = the transient orange-to-black reveal (M1) every kinetic word gets.

| t (s) | Frames | Text | Highlight |
|---|---|---|---|
| 0.00–1.50 | 0–36 | `OpenAI` `x` `Gojiberry` | "Gojiberry" crimson f17–22 → black |
| 1.54–2.2 | 37–53 | `What can I help with?` | ember on "help", "with?" |
| 1.54–4.3 | 37–103 | `Ask anything` (placeholder) | (none) |
| 2.71–4.29 | 65–103 | `Run my outbound` | (none) |
| 4.4–5.4 | 106–133 | `Gojiberry` | letters pink → dark |
| 7.3–8.75 | 176–210 | `ChatGPT` · `Temporary` · `New chat` · `Search chats` `⌘K` · `Library` `11` · `What can I help with?` · `Ask me anything` · `Tools` · `Gourmet Food Truck Trends` · `Digital Art Techniques` · `Virtual Reality Experiences` · `Local Music Scene Highlights` · `Culinary Heritage Preservation` · `Sustainable Fashion Innovations` · `Community Gardening Initiatives` | (none) |
| 8.9–10.9 | 213–262 | `@Gojiberry` | bold grey |
| 9.96–13.2 | 239–318 | `Find 100 SaaS founders hiring salespeople` | "Find 100 SaaS founders" crimson/coral; "hiring salespeople" grey |
| 13.2–15.0 | 316–361 | `enrich their contact details` | whole phrase brand gradient |
| 15.1–16.6 | 362–399 | `write a personalised message` | brand gradient (write a → message) |
| 16.7–18.8 | 401–451 | `and launch the campaign.` | "campaign." coral/orange |
| 20.3–21.9 | 486–527 | `Gojiberry Find 100 SaaS founders currently hiring salespe[ople, enrich]` / `their contact details, write a personalized message and lau[nch the]` / `campaign.` | "Gojiberry" bold; red sweep over "Find 100 SaaS founders" f509–516 |
| 20.3–21.9 | 486–527 | `Working...` | crimson shimmer |
| 22.0–24.3 | 528–583 | `Analysing Lead...` (×6) | brand gradient |
| 24.0–28.5 | 576–711 | `Gojiberry` · `Maya Estêvão` · `Founder at OpenBundle` · `Email:` · `[email redacted]` · `Phone:` · `[phone redacted]` · `LinkedIn` · `[url redacted]` | email tan→rose gradient |
| 25.96–28.5 | 623–683 | `Brings the right context into every message` | ember only |
| 29.7–31.2 | 712–750 | `Maya Estevão` (no circumflex in this shot) · `Founder at OpenBundle` · `Hi Maya!` · `Write a message...` | (none) |
| 31.5–33.4 | 757–802 | `Saw you're growing your sales team` | (none; white on blue) |
| 33.5–35.4 | 803–851 | `Write a message...` | (none) |
| 35.5–37.6 | 852–903 | `Launch` | pressed gold |
| 37.67–38.17 | 903–916 | `Right here` | ember |
| 38.2–39.2 | 917–942 | `Right here in ChatGPT` | ember on "in ChatGPT" |
| 39.3–39.5 | 943–950 | `Ask anything` | (none) |
| 39.9–40.9 | 958–982 | `Gojiberry launch a LinkedIn outbound campaign targeting SaaS founders in the US.` | "Gojiberry" semibold; ember on arriving words ("US." still warm at f975) |
| 40.96–42.2 | 983–1013 | `Goji flags interested prospects` | ember |
| 42.25–44.4 | 1014–1065 | `Maya Estevão` · `Founder at OpenBundle` · `Mostly. What do you guys offer?` · `Write a message...` | ember on arriving words |
| 43.2–44.4 | 1036–1065 | `Thinking of the best reply` | grey shimmer |
| 44.5–46.2 | 1070–1110 | `We help teams scale content without hiring. Worth a quick chat?` | ember on arriving words |
| 46.3–48.0 | 1111–1153 | `1 PM` `2 PM` `3 PM` `4 AM` · `meeting with Maya - Founder` `@OpenBundle` · `1:15-2:15pm` | (none) |
| 48.08–48.96 | 1154–1175 | `Chat` → `ChatGPT` | ember |
| 49.0–50.3 | 1176–1207 | `ChatGPT is the interface` | ember on "is the interface" |
| 50.2–50.9 | 1204–1220 | `gojiberry` (node label) | (none) |
| 51.0–52.1 | 1224–1251 | `Lead Scoring` · `Intent Signals` · `AI Outreach` | per-letter ember sweep |
| 52.17–53.38 | 1252–1281 | `From one prompt` | ember in, reverse-ember out |
| 53.4–54.6 | 1282–1311 | `…ay at 2?` (cropped) · `Perfect, booked. See you then!` | ember on arriving words |
| 54.7–55.9 | 1312–1343 | `Install Plugin` | pressed gold |
| 56.2–60.6 | 1349–1455 | `Find 50 ideal prospects, personalize the messages, and start the outreach` | ember on arriving words |
| 60.79–64.94 | 1459–1556 | `gojiberry` · `Your AI go-to-market team` | (none) |

---

## 5. Cursor

- Glyph: macOS-style arrow, black `#000` fill, white outline ≈5 px at the ~96 px size, soft shadow `0 6 10 rgba(0,0,0,.28)`; tilted so the tip points up-left with the body leaning right (≈ −12° vs system arrow). Screen-space size varies with the shot: 90–98 px (S02), 110–124 px (S11–S12), 68 px (S18), 100 px (S22), 104 px (S31), 80 px (S38), 180–195 px (S39).
- Motion grammar: **enter** from off-frame bottom/bottom-right with expo-out (each frame covers ~45 % of the remaining distance); **press** = M6 (scale to 0.5–0.7 for one frame, back with slight overshoot) + ripple (§3.3, S02 only; later clicks use the button's own reaction instead); **exit** to the upper-left with ease-in (accelerating; last step 100–240 px/frame) and a 1-frame fade.

| Path | Enter frames (tip start → rest) | Press (frame, t) | Exit |
|---|---|---|---|
| C1 (S02 composer) | f50 (882,820) → f60 (722,470) | f61, 2.54 s | f71–80 → (240,158) |
| C2 (S11 send) | f461 (1582,798) → f467 (956,538) | f471, 19.62 s | rides down f480–492, off bottom f495 |
| C3 (S18 LinkedIn icon) | f698 (1544,1008) → f705 (1230,778) | f706, 29.42 s | lost in blur-zoom f707–711 |
| C4 (S22 Launch) | f854 (1066,706) → f864 (978,554) | f865, 36.04 s | f866–878 → (638,240) |
| C5 (S31 calendar drag) | f1111 (994,798) → f1114 (956,746) | pressed f1115–1125 while dragging up to (942,466); release f1126 | f1131–1137 → (776,190) |
| C6 (S38 Install) | f1314 (1100,764) → f1325 (956,548) | f1327, 55.29 s | f1330–1337 → (374,268) |
| C7 (S39 send) | f1413 (≈1650,870) → f1430 (≈996,566) | f1433–1434, 59.71 s | f1444–1454 → (≈450,240) |
| Hand H1 (S26 drag) | f943 from below composer → f952 text start | drop f957, 39.88 s | up and out f962–964 |

---

## 6. Audio

### 6.1 Narration (speech-to-text word times, `ref/stt.json`)

| Line | Start–end (s) | Picture at that moment |
|---|---|---|
| "What if you could run your outbound directly from ChatGPT?" | 0.68–3.84 | S01 lockup → S02 ChatGPT, click 2.54, typing 2.71–3.50 |
| "Meet Gogi, your entire outbound engine inside ChatGPT." | 4.78–8.90 | S03 wordmark done 4.83 ("Meet"); S04 orange icon; S05 window reveal 7.0 ("inside ChatGPT" 7.6–8.9) |
| "Just ask." | 9.60–10.20 | S06 "@Gojiberry" done 9.54 |
| "Find one hundred SaaS founders hiring salespeople." | 10.66–13.40 | S07 typing 9.96–13.0 (text leads 0.5–0.7 s) |
| "Enrich their contact details," | 13.84–15.36 | S08 13.29–15.04 |
| "write a personalized message," | 15.66–16.96 | S09 15.08–16.63 |
| "and launch the campaign." | 17.24–18.30 | S10 16.67–18.75 |
| "Gogi finds prospects showing real buying signals," | 18.78–21.56 | S11 send lands 18.79; click 19.62; bubble + Working 20.3–21.5 |
| "like founders building their sales teams," | 22.00–23.86 | S15 avatar cloud 22.0–24.0 |
| "enriches their contact details," | 24.08–25.70 | S16 person card 24.0–25.8 |
| "and brings the right context into every message." | 26.06–28.94 | S17 25.96–28.5 |
| "So, 'Hi, Maya,'" | 29.38–30.48 | S18 click 29.42; S19 "Hi Maya!" 29.67 |
| "becomes," | 30.80–31.30 | S19 backspace 30.83–31.13 |
| "'Saw you're growing your sales team.'" | 31.64–33.08 | S20 typing 31.54–32.58 |
| "A real reason to reach out." | 33.46–35.08 | S21 typing indicator |
| "Then launch your campaign" | 35.68–36.92 | S22 press 36.04 on "launch"; S23 explosion |
| "right here in ChatGPT." | 37.76–39.52 | S24 "Right here" 37.67; S25 "in ChatGPT" 38.2–38.4 |
| "Gogi flags interested prospects" | 40.02–42.04 | S26 prompt typing 39.9–40.9; S27 text 40.96 |
| "and instantly suggests a reply" | 42.08–43.84 | S28 reply types; S29 Thinking pill 43.2 |
| "for you to review and approve." | 43.92–45.54 | S30 check 44.58, reply types 44.6–45.1 |
| "All that's left is to book the meeting." | 46.08–47.90 | S31 calendar 46.3, drag 46.46–46.92 |
| "ChatGPT is the interface." | 48.24–50.04 | S32 "Chat" 48.08; S33 capsule 49.0–50.0 |
| "Gogi is the engine." | 50.42–51.72 | S34 node 50.2–50.5; S35 chips from 51.0 |
| "From one prompt to booked meetings." | 52.14–54.08 | S36 "From" 52.17 (lead 0.03 s); S37 "Perfect, booked" 53.42 ("booked" 53.42) |
| "Install the plugin using the link below the video" | 54.92–57.46 | S38 pill 54.67, click 55.29; S39 composer 56.0 |
| "and run your outbound directly from ChatGPT." | 57.64–60.42 | S39 typing ends ~58.3; send 59.71 |
| "Gogi Berry, your AI go-to-market team." | 60.94–63.68 | S40 logo 60.79; tagline 61.67–62.00 |

Rule the editor followed: on-screen words land **0–0.6 s before** the spoken word, never after.

### 6.2 Voice (for picking a TTS voice)

- Gender: **female** (median F0 **219 Hz**, 10th–90th percentile 168–348 Hz; the upper tail is partly pitch-tracker octave error). Pick a voice centred around 200–225 Hz.
- Pace: 147 words in 63.0 s = **2.33 words/s (140 wpm)** overall; **3.44 words/s** inside phrases, with 0.3–0.8 s pauses between phrases (the pauses set the edit points).
- Tone (inferred from the script and pacing): upbeat, confident, conversational "product-launch" read. Accent and timbre: **NOT CHECKED** (not listened to; judge by ear). The name is pronounced "Goji" but transcribed "Gogi".
- Level: voice sits at ≈ −15 dBFS RMS (mid channel) throughout; peak −3.1 dBFS.

### 6.3 Music (measured on the side channel = music only)

- Tempo **104.05 BPM** (beat 0.5767 s = 13.84 frames), first beat phase 0.34 s. Beat grid t = 0.34 + k·0.5767. Autocorrelation gives the same 104 BPM in 0–20 s, 20–40 s and 40–65 s, so the tempo is constant. Downbeat (bar 1) **NOT PINNED**.
- Loudness arc (side-channel RMS per second, dBFS; voice stays ≈ −15):
  - 0–21 s: sparse, −37 to −33 (music ≈ 20 dB under the voice). Swell/spike at 4 s (−26.7, tile arrival) and 13 s (−27.9).
  - 21–22 s: noise swell/riser into the zoom-through (−26.8).
  - 23.4–35 s: steady percussion on every beat (onsets at 23.97, 24.55, 25.12, 25.71 … every 0.577 s), −35 to −29.
  - **36 s: drop**: full-energy section begins on the Launch press (−26.5 → −24 by 48–54 s, ≈10 dB louder than the intro).
  - 55 s: breakdown on "Install the plugin" (−31 → −37).
  - 59.7–63.7 s: low outro bed (−37 to −41); **hard stop at 63.74 s**, silence to the end.
- Cuts vs beats (±1 frame = on-beat): on-beat cuts at f37, f104, f313, f451, f575, f672, f686, f852, f866, f1032, f1282, f1336, f1433; off-beat (8th) cuts at f471, f486, f527, f803, f983, f1066, f1344. The rest fall within 3–5 frames of a beat.
- Low-frequency impacts (side <150 Hz): 4.55 s (f109), 6.47 s (f155), 7.46 s (f179, halftone), 9.10 s, 20.37 s (f489, after the click burst), **36.83 s (f884, strongest, explosion)**, 41.17 s, 45.41 s (f1090), 50.35 s (f1208).

### 6.4 Sound effects (spectral evidence only, NOT verified by ear)

| t (s) | Frame | Probable SFX | Evidence |
|---|---|---|---|
| 0.6–1.5 | 14–36 | sparkle/shimmer chime | warbling 7–10 kHz line in both channels under the lockup |
| 2.25 | 54 | soft whoosh (camera push) | hi-band transient in a speech gap |
| 2.54 | 61 | mouse click | transient at the press frame |
| 4.33–4.55 | 104–109 | whoosh + low thump (tile) | side low-band peak |
| 5.5–6.3 | 132–151 | sparkle chime (icon re-skin) | same warbling line as 0.6 s |
| 7.0–7.5 | 168–179 | dust/whoosh (halftone) | low peak 7.46 s |
| 18.72 | 449 | whoosh (whip to send button) | hi transient, speech gap |
| 19.62–19.69 | 471–472 | click + digital burst | hi-band 5.3 kHz centroid |
| 20–22 | 480–527 | riser/noise swell into zoom-through | broadband side-channel wash |
| 29.2–29.3 | 700–702 | click (LinkedIn) | 7.4 kHz transient, speech gap |
| 29.66 | 711 | whoosh (blur zoom) | |
| 35.51 | 852 | pop (Launch pill appears) | transient, speech gap |
| 36.09 | 866 | click + impact (explosion) | + low peak 36.83 |
| 39.96 | 959 | drop/snap (chip into composer) | transient, speech gap |
| 46.35 | 1112 | click (calendar) | 5.9 kHz transient |
| 55.37 | 1328 | click (Install) | |
| 55.5–57 | 1332–1368 | bright riser / chime run | striated high band in side channel |
| 59.67 | 1432 | click (send) | |
| 60.87 | 1461 | logo sting | transient, speech gap |

---

## 7. Brand elements to swap

**Gojiberry identity**
- Mark (3-facet ribbon: peach `#F9C08B` / coral `#F4816F` / crimson `#EB4C5E`): S01 (colour → black), S03, S04 (white on orange tile), S05 halftone colour source, S13 bubble tile, S16 card chip, S26 composer chip (white on crimson→peach), S29 Thinking pill icon, S34 node, S40 end card.
- Wordmark "Gojiberry" (title case, Medium): S01, S03. Lowercase logotype "gojiberry": S34, S40.
- Text "Gojiberry": S01, S03, S06 ("@Gojiberry"), S13 bubble, S16 card chip, S26 composer ("Gojiberry launch…"). Text "Goji": S27 ("Goji flags interested prospects"). Voice: "Gogi" ×6, "Gogi Berry" ×1.
- Brand palette used as the film accent: crimson/coral/peach gradient (M2), orange tile/icons (`#F29433`/`#F9BF91`→`#F4806F`), ember orange `#EE8319`. Swap all of these together for the new brand's accent.
- Tagline "Your AI go-to-market team" (S40).

**LinkedIn**
- Spoken/typed: "LinkedIn outbound campaign" (S26 prompt: "launch a LinkedIn outbound campaign targeting SaaS founders in the US.").
- Logo: "in" square on the person card (S16/S18, `#067EB4`), DM window header tile (S19, S28–S30, `#0A66C2`).
- DM window chrome imitating LinkedIn messaging: header (avatar + online dot + name + title), video / ••• / ✕ controls, blue outgoing bubbles, "Write a message..." composer with paperclip/smiley/send (S19–S21, S28–S30, S37).
- Card row "LinkedIn" label (S16/S18).

**OpenAI / ChatGPT** (third-party marks; keep only if the remake is also a ChatGPT plugin): OpenAI blossom + wordmark (S01, S05 top bar), "ChatGPT" UI (S02, S05), text "ChatGPT" (S25, S32, S33).

**Other named content**: "OpenBundle", "Maya Estêvão"/"Maya Estevão" (spelled both ways in the source), "[email redacted]", "[phone redacted]", "[url redacted]", the ChatGPT history titles (S05), all stock headshots (S15, S16, S19–S23, S28–S30, S37). Replace with a fictional persona set.

---

## 8. Not pinned down

1. Anything that needs ears: accent/timbre of the narrator, exact SFX identities, music genre/instrumentation, bar downbeat. Tempo, loudness arc and hit times are measured; SFX are spectral guesses.
2. Fonts are identified by eye (SF Pro / Inter Display for UI and kinetic type; the "gojiberry" logotype is custom). Sizes and colours are measured.
3. Hidden text: the full first line of the S13 bubble (cropped at the right edge) and Maya's message in S37 ("…ay at 2?").
4. Periods of the "Working…" and "Thinking…" shimmers and of the typing-indicator dots.
5. Camera moves are given as measured keyframes (sizes/positions per frame for the major moves: S01, S02, S04, S05, S11, S12, S15–S17, S19, S39, S40); for shorter moves only start/end and curve type are given. A pixel-exact camera track for every frame was not extracted.
6. The "4 AM" calendar label (S31) and the two spellings of "Estêvão" are in the source; decide whether to copy them.
