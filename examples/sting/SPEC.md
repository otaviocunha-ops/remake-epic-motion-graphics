# SPEC — frame-accurate replication spec of the "pyramids" reference (Manus AI-helper promo)

Source: `ref/src.mp4` · 720×720 · 29.97 fps (30000/1001) · 360 frames (f0–f359) · 12.07 s container, last frame ends 12.012 s · AAC stereo 48 kHz (`ref/audio.wav`).
Frames: `ref/full/f_0000.jpg … f_0359.jpg` (0-based, `fN` = `f_000N.jpg`, time = N / 29.97 s). Contact sheet `ref/sheet.jpg`.

How this was measured (so you know what to trust):
- Cuts: mean abs grey difference at 96×96 (`measure/cuts.py`, rule of lesson 2.3: diff > 10 and > 2.5 × local median), every candidate opened and confirmed by eye on full frames and montages.
- Positions and sizes: per-frame masks + connected regions (`measure/lib.py` has a numpy-only labeller; no scipy on this Mac). One script per shot: `measure/s1_header.py`, `s2_orbit.py`, `s3_prompt.py`, `s4_answer.py`, `s5_cards.py`, `s7_end.py`. Colours and cap heights: `measure/style.py` (every value names its frame and box). Corner radii: `measure/radii.py` (circle fit to the corner's edge pixels, fit error ≤ 0.8 px). All per-frame numbers are in `measure/tables.json` (built by `measure/build_tables.py`; re-run everything with `measure/run_all.sh`, ≈40 s).
- Blur amounts are **Gaussian-σ equivalents in px**: the σ that, applied to a sharp frame of the same shot, gives the same gradient energy as the blurred frame (`lib.blur_sigma`). Motion blur reads as a σ too; its direction is given from the x/y gradient ratio (`gx_gy`) and by eye. Values under ≈0.35 are JPEG noise, read them as 0.
- Cursor tips: top-left-most pure-black (lum ≤ 35) pixel of the cursor blob, ±2 px. Where the cursor overlaps the black menu-bar icon (S3) the tip is hidden and only the arrow body is measured.
- Audio: numpy only (spectral-flux onsets, autocorrelation tempo, grid fit, band energies). **I could not listen.** Sound identities are guesses from numbers; see `AUDIO.md`.
- Items marked **NOT PINNED** were not measured or are estimates by eye.

Conventions: positions on the 720×720 canvas, origin top-left, boxes `[x0, y0, x1, y1]` with x1/y1 exclusive. "Camera" = one scale + translate applied to the whole shot layer. **REPLACE** marks every brand element of the reference (Manus identity, the "AI Helper" pill, the "dnyxstudios" end card, the third-party site card, and the pyramid subject matter).

---

## 0. The film in one paragraph

A 12-second, square, Apple-style "AI helper" product sting. Everything is soft, white and bright-blue, and the camera never cuts on a static frame: every shot enters already moving (exponential ease-out, 12–16 % of the remaining distance per frame) and leaves on an accelerating move or a blur ramp. Story: the app's header (logo disc + "Manus" + "AI Helper" pill) rises out of a pale blue haze inside a glassy window → a cursor glides in, turns to face its direction of travel, grows on hover over the logo, and clicks → hard cut on the music drop to the black app icon with four coloured squares orbiting into a cross → the icon collapses into a Mac menu bar → the cursor clicks the menu-bar icon, a frosted-glass prompt box springs out of it and "Tell me about the pyramids" types at ~1 char/frame → whip-tilt up through a light-blue flash into the AI's answer (grey text, the key phrase in black bold) scrolling up into place → a photo card of the Great Pyramid rises over the blurred answer → blur-dissolve to two stacked "Khufu" / "Khafre" cards with frosted glass titles → blur-dissolve to the lone logo disc → hard cut to a black end card with a glowing white wordmark that zooms out and collapses. Music: 124 BPM electronic track, soft intro to 2.4 s, drop on the cut at f72.

---

## 1. Global style system

### 1.1 Colour tokens (sampled; `measure/parts/style.json`)

| Token | Hex | Where sampled |
|---|---|---|
| page (white, warm) | `#FDFDFB` | f40/f86/f150/f180/f270 corners |
| page, pure white (S5 card, S6 page) | `#FFFFFF` | f205 card, f230 page |
| opening haze, top→bottom | `#B7CFEB` → `#B9D1ED` (y540) → `#CDE1F8` (y700) | f0, x0–30 |
| haze mid-fade | top `#CADAEA` / bottom `#DAEDFC` (f6); top `#E3ECF3` / bottom `#DBEEFD` (f12); top `#F6F7F9` (f20) | x0–30 |
| settled S1 page gradient | top `#FDFDFB`, y360 `#FCFCFA`, y540 `#EBF5FD`, y700 `#DBEEFD` (blue floor glow stays for the whole shot) | f40 |
| window fill | `#FCFDFF`; top band `#F1F6FF`; lower-left `#DDEFFE` (blue glow inside the window) | f40 |
| window hairline border | `#F5F7F8` (1 px) | f40 x271–274 |
| logo disc fill / rim | `#FBFCFE` / `#E8E8EA` | f40 |
| logo glyph (dark grey, not black) | `#383737` (S1), `#353333` (S7) | f40, f270 |
| "Manus" text | `#010000` (black) | f40 |
| "AI Helper" pill fill | `#2F2E2F` (body), `#424343` (top edge highlight) | f40 |
| pill text | `#FEFDFE` | f40 |
| hover ring (logo) | inner `#D5F3FF`, outer halo `#F7FEFF` | f64 |
| cursor fill | `#000000`-`#010000`, white outline | f40 |
| sidebar icons | bolt `#81858D`, chat `#BAC8D5` (faded) | f40 |
| site card (REPLACE) | fill `#F7FBFE`, globe tile `#66C3FB`, title `#3F454C`, meta `#BCC5CC`, screenshot `#C1D8F2` | f40 |
| app icon tile | `#000000`, glyph `#FFFFFF` | f86 |
| icon halo disc / inner ring | `#E9E9E7` / `#DEDEDE` | f86 |
| square yellow | TL `#F9D927`, centre `#FAE120`, BR `#FBC527` | f86 |
| square blue | TL `#384DF8`, centre `#254CF6`, BR `#3294FA` (lighter cyan lower-right) | f86 |
| square green | TL `#4DE221`, centre `#49E81A`, BR `#5CE424` | f86 |
| square magenta | TL `#DB00FD`, centre `#E000F7`, BR `#BA00FA` | f86 |
| laptop bezel | `#050505`, top-edge highlight `#686866` | f150 |
| menu bar | `#232149` | f150 |
| menu-bar text/icons | `#CAD1F7` (anti-aliased; true fill ≈ white) | f150 |
| menu-bar dots | blue `#2E55F7`, green `#4DE525`, magenta `#DC00F9` | f150 |
| wallpaper | TL `#170D71`, centre `#262EAC`, BR `#4651C7`, light streak `#3131AC` (diagonal streaks lower-left → upper-right) | f150 |
| glass prompt box | fill top `#525EC5`, bottom `#404DAB`, top border highlight `#5A6BC0` | f150 |
| prompt text / icons | `#F1FCFF` / `#F1F9FF` | f150 |
| send button | `#1EB3FA` disc, white arrow | f150 |
| blue flash (whip into answer) | `#E6F4FE` (f158) → `#E2F4FE` (f159 peak) → `#F0F9FC` (f161) → `#FDFDFB` (f165) | corners |
| answer body text | `#BCBCBA` (ink sample; true fill ≈ `#B0B0AE`) | f180 |
| answer key phrase | `#000000` bold | f180 |
| card caption / sub-caption | `#000000` / `#969696` | f205 |
| card grabber bar | `#62707C` | f205 |
| "Explore" pill | frosted `#8D99AC`, text `#ECF3FE` | f230 |
| "•••" button | frosted `#808497` | f230 |
| glass title text ("Khufu") | lightened blur of the photo: `#E3D3BF` over sand, `#9A9283` mid "Khafre" | f230 |
| S7 disc | `#F6F6F6` | f270 |
| end card bg | corners `#020204`, around word `#272729` (above) / `#232325` (below), radial falloff | f320 |
| end card word | `#F3F3F5` core, white glow | f320 |

### 1.2 Typography

All UI type is **SF Pro** (Apple system font; single-storey "a" absent — double-storey a, straight-legged R, round dots). Closest free match: **Inter** (tracking −0.01 em). Family is identified by eye; sizes are measured cap heights ÷ 0.705 (SF cap-height ratio).

| Use | Weight | Cap height → size (at that frame's camera) | Where |
|---|---|---|---|
| "Manus" app name (REPLACE) | Regular 400 | "M" cap 30 px → **≈42 px** | f40, ink x434–551, y342–372 |
| "AI Helper" pill (REPLACE) | Medium 500 | "A" cap 15 px → **≈21 px** | f40 |
| Site card title "California Orchid…" (REPLACE) | Medium 500 | "C" 14 px → ≈20 px | f40 |
| Site card meta "Not published • Ju…" | Regular | "N" 10 px → ≈14 px | f40 |
| Menu bar "Mon Jun 22  9:41 AM" | Regular | "M" 16 px → **≈23 px** | f150 |
| Prompt "Tell me about the pyramids" | Regular | "T" 18 px → **≈25.5 px** | f150 |
| Answer body + heading | Regular | "T"/"B" cap 22–23 px → **≈31–32 px**; line pitch **38.7 px** (tops 191, 229, 268, …); paragraph gap = one empty line (77 px) | f180 |
| Answer key phrase "Pyramid of Khufu" | Semibold 600 (black) | "P" 23 px → ≈32.6 px | f180 |
| Card caption "Pyramid of Khufu" | Semibold 600 | "P" 18 px → **≈25.5 px** | f205, x262–458, y643–666 |
| Card sub-caption "Cairo, Egypt" | Regular | "C" 11 px → ≈15.6 px | f205 |
| "Explore" pill | Medium | "E" 9 px → ≈13 px | f230 |
| Glass titles "Khufu"/"Khafre" | Bold 700 | cap top y262, clipped by the photo's bottom edge at y341 (≥ 79 px visible) → **≥ 112 px**; full cap NOT PINNED | f230 |
| End wordmark "dnyxstudios" (REPLACE) | Medium 500, lowercase | "d" ascender 40 px (÷0.74) → **≈54 px**; word 375 px wide at f320 | f320 |

### 1.3 Recurring motion motifs (implement once, reuse)

**M1 · Expo ease-out arrival.** Every element that enters covers a near-constant share of its remaining distance per frame: header rise 13–16 %/frame (f3–f23), answer scroll 16–19 %/frame (f161–f173), photo card rise 11–16 %/frame (f189–f203), S6 cards and S7 disc the same family. Implement as `x += (target − x) · 0.14` per frame, or `easeOutExpo`, starting mid-motion on the cut frame (the first frame is already 25–40 % of the way).

**M2 · Blur tied to speed.** Moving layers carry Gaussian-equivalent blur roughly proportional to speed: header σ 1.9 → 0.3 px over f5–f16; answer text σ 16 → 1.0 over f159–f166; card σ 2.5 → 0.4 over f189–f199. Direction follows motion (vertical for the rises/tilt, horizontal for the end-card zoom smear).

**M3 · Blur-dissolve transition.** Outgoing shot ramps blur up (σ 0.5 → 5–8 px over 5–6 frames, accelerating) while it drifts/zooms; hard cut at the blur peak to an incoming shot that is already blurred (σ ≈ 8) and de-blurs over 8–10 frames. Used S5→S6 (f209–f224) and S6→S7 (f239–f247).

**M4 · Direction-facing cursor.** Black macOS arrow with white outline. It rotates to point along its travel direction (points left while moving left/down-left f47–f51, points up while moving up in S4) and returns to the normal up-left pose when it stops. It grows ≈1.5× while hovering a target (S1) and shrinks ≈15 % for one press (f69–f71).

**M5 · Pop with overshoot.** The glass prompt box springs out of the menu-bar icon: width 318 → 402 → 449 → 474 → 486 → 494 → 496 (peak f126) → 495 → 492 → 488 → 485 → 483 → 481 (f140) px. One overshoot ≈ 2.5 %, settled in ≈ 14 frames.

**M6 · Whip-tilt + flash.** S3 exits by tilting the camera up with accelerating speed (content y −2 → −17 px/frame f150–f158, σ 0.3 → 8.4) while the page tints light blue (`#FDFDFB` → `#E6F4FE`); S4 enters already moving the same way with the tint at its peak (`#E2F4FE` f159) and fading out by f165.

**M7 · Slow living drift on holds.** Nothing is ever frozen except S7 f269–f287: the header drifts up 6 px over f24–f37, the answer creeps −4 px after settling, cards keep rising 2–3 px/frame, the end word keeps shrinking ≈1 px/frame.

---

## 2. Shot table (8 shots, f0–f359, no gaps)

Beat grid (see `AUDIO.md`): beat k at t = 0.048 + k·0.4838 s (124.0 BPM), one beat = 14.50 frames, 8th = 7.25 frames. "On-beat" = within ±1 frame.

| # | Frames | Time (s) | Key still | Content | Out-transition |
|---|---|---|---|---|---|
| S1 | 0–71 | 0.000–2.402 | `f_0040.jpg`, `f_0064.jpg` | Pale blue haze; logo disc + "Manus" + "AI Helper" pill rise in; window fades in around them; cursor enters top-right, curves down to the logo, hover ring + camera zoom 1.2×, press | **hard cut** f72 (diff 29.8), 1.9 f before beat 5 = the drop |
| S2 | 72–100 | 2.402–3.370 | `f_0086.jpg` | Black app icon on grey halo, 4 coloured squares orbit CCW into a cross; then icon shrinks accelerating and squares slide to its right, blur ramps | **hard cut** f101 (diff 112.8) into the blurred menu bar (match-cut: icon + dots row) |
| S3 | 101–158 | 3.370–5.305 | `f_0117.jpg`, `f_0150.jpg` | Laptop top edge + menu bar; cursor rises, clicks the menu-bar icon; camera pans left; glass prompt box pops out; "Tell me about the pyramids" types; whip-tilt up + blue flash | **hard cut** f159 (diff 109.2) mid-whip (motion-matched) |
| S4 | 159–186 | 5.305–6.240 | `f_0180.jpg` | Answer text arrives scrolling up (smeared), settles; key phrase black bold; cursor (pointing up) under it | **hard cut** f187 (diff 24.8): card enters over the same backdrop |
| S5 | 187–214 | 6.240–7.174 | `f_0205.jpg` | Photo card "Pyramid of Khufu / Cairo, Egypt" rises from below; the answer behind blurs; then the whole frame blurs out | **blur-dissolve** (M3): blur ramp f209–f214, cut f215 (diff 14.6 at f215, 15.0 at f216) |
| S6 | 215–244 | 7.174–8.175 | `f_0230.jpg` | Two stacked cards "Khufu" / "Khafre" de-blur and rise into place, drift up, then accelerate up and blur out | **blur-dissolve** (M3): cut f245 (diff 29.3) |
| S7 | 245–300 | 8.175–10.043 | `f_0270.jpg` | Logo disc alone on white rises (blurred) into the centre, holds, then shrinks accelerating | **hard cut** f301 (diff 180.3) to black |
| S8 | 301–359 | 10.043–12.012 | `f_0320.jpg` | Black end card; "dnyxstudios" glowing white, enters huge + horizontally smeared, zooms out, slow shrink, then collapses on the last 10 frames | end of file (no fade; audio runs to 12.056 s) |

Hard-cut candidates from the detector: 72, 73, 101, 159, 187, 215, 216, 245, 301, 302. f73, f216 and f302 are the second frame of fast motion after the cut (confirmed by eye), not cuts. No cross-dissolves (no frame blends two shots).

### 2.1 Shot detail

#### S1 · f0–71 · Header rise → window → cursor hover + press (REPLACE: logo, "Manus", "AI Helper", site card)

- **Background:** f0 is a flat haze `#B7CFEB` with a lighter floor (`#CDE1F8` at y700). It fades toward the warm white page over f0–f28 (top: `#B7CFEB` f0, `#CADAEA` f6, `#E3ECF3` f12, `#F6F7F9` f20, `#FDFDFB` f28), while the bottom keeps a blue floor glow `#DBEEFD` (y700) / `#EBF5FD` (y540) for the whole shot. Table `S1_bg`.
- **Header group** (logo disc, word, pill on one centre line). Settled (f36–f47): logo disc x316–404 (⌀ 88), centre (360, 358); "Manus" ink x434–551, y342–372; pill [586, 336, 709, 383] = 123×47, capsule (radius ≈ 23; circle fit 20). Gaps: disc→word 30 px, word→pill 35 px.
- **Rise (M1):** the group moves straight up, centre y by frame (disc blob f0–f4, word centre after): 621, 554, 517, 490, 471, 455, 441, 430, 420, 412, 405, 399, 394, 390, 385, 382, 379, 376, 374, 371, 369, 368, 366, 365, 364 (f24), 363, 362, 361, 360, 360, 359, 359, 358 … 357 (f37). Share of remaining distance per frame: 25 %, 19 %, 16 %, then 12–15 % steady → exponential ease-out that started before f0. x stays at 434–435 (no horizontal move; scale 1.02 → 1.00 over f5–f40).
- **Stagger inside the rise:** f0–f1 only the disc (white on the haze, smeared vertically: blob 117 px tall vs 88); "Manus" appears f2 (blurred); pill appears f4–f5 heavily blurred and slides left 10 px (x0 596 f5 → 593 → 592 → 591 → 590 … 586 by f24) as it sharpens. Header blur σ: 1.9 (f5), 1.5, 1.2, 1.0, 0.9, 0.8, 0.6, 0.55, 0.5, 0.4 (f14), ≈0 from f16.
- **Window reveal:** a large glassy window, top-left corner at (272, 270) f40, extends off the right and bottom edges; corner radius **62 px**; 1 px hairline `#F5F7F8`; fill near-white `#FCFDFF` with a pale-blue top band `#F1F6FF` and blue lower glow `#DDEFFE`. It fades in around the already-placed header: opacity (projection method, ±0.05) ≈0 f8–f14, 0.53 f15, 0.66 f16–18, 0.70 f19, 0.77 f20, 0.85 f21, 0.91 f22, 0.97 f23, 1.0 f24 (table `S1_window_alpha`). Inside: a left column of icons (centred x≈358) — a grey bolt icon (≈(358, 493)) and a faded chat icon (≈(358, 600)), and a site card at x510→off-frame, y467→off-frame: blue globe tile (547, 507), "California Orchid…", "Not published • Ju…", a website screenshot below (Framer nav, "The in… your…" hero). **REPLACE** the site card with your own product content.
- **Cursor** (M4), table `S1_cursor`: appears f27 at tip (594, 262) above the window, glides left decelerating: (577,260) f28, (565,258), (556,256) f30, (543,254) f32, (533,251) f34, (526,250) f36, (521,249) f38, (518,249) f40, (515,250) f42, (513,255) f44 — then turns down: (513,263) f46, (515,278) f48, (523,299) f50, (529,309) f51; f52–f55 it is a fast motion-blurred streak heading down-left over "Manus" (not measurable); lands (419,376) f56, (406,372) f57, (398,368) f58, (391,364) f59, (383,358) f61, (377,355) f63, (374,353) f65, (372,352) f68, (370,354) f71 — on the lower-right of the logo disc. Orientation: normal (tip up-left) f27–f45, rotated to point left / down-left f47–f51, back to normal from f56. Size: 21×26 px box at f40; 37×49 at f64 (= 31×41 after dividing by the camera zoom → **cursor grows ≈1.55× on hover**); shrinks to 27×36 at f71 (press).
- **Hover ring:** light-blue ring around the logo disc from f53 (ring x302–417 f54 → 291–430 f59–f64, i.e. ring outer ⌀ ≈ 139 px at camera 1.2 = 116 px unzoomed, 14 px beyond the disc). Colour `#D5F3FF` inner → `#F7FEFF` soft outer. Stays until the cut.
- **Camera zoom** about the frame centre (360, 360) = logo centre (pivot solved from the word's left edge and the window's corner: x 359.5, y 361.7). Scale (from the word's right edge, table `S1_header.camera_scale_from_x1`): 1.00 f44–f46, 1.016 f47, 1.021 f49, 1.031 f50, 1.037, 1.052, 1.073 (f53), 1.12, 1.157, 1.173, 1.183 (f57), 1.194 f59, **1.199 f60–f61**, 1.194, 1.194, 1.188 (f64), 1.183, 1.173, 1.157, 1.141, 1.12 (f69), 1.089, 1.037 (f71). Zoom-in = ease-in-out over f47–f60 (peak speed f54); zoom-out = ease-in accelerating f64 → f71 into the cut. Window edge confirms: x 272 → 254 (f60) → 267 (f71).
- **Press:** cursor shrinks f69–f71 while the camera pulls out; cut at f72.
- Out: hard cut f72 (2.402 s), 2 frames before the music drop (beat 5, 2.467 s).

#### S2 · f72–100 · App icon + orbiting squares → collapse (REPLACE: icon glyph; keep or recolour the four squares)

- Settled layout f86: black rounded-square icon [300, 300, 419, 420] (119 px, radius **33**), white hand glyph; grey halo disc `#E9E9E7` ⌀ 217 (x251–468) with a darker inner ring `#DEDEDE` hugging the icon; four rounded squares ≈61 px (radius **17**), vertical/diagonal gradients (§1.1): yellow centre (221, 351) left, blue (370, 217) top, green (509, 367) right, magenta (356, 506) bottom → orbit radius 139–150 px around (359.5, 359.5).
- **Enter (f72, already moving, motion-blurred σ 1.2):** icon 184 px wide, shrinking ease-out: 184, 158, 147, 140, 136, 132, 130, 128, 126, 125, 124, 122, 122, 120, 119 (f86). Squares arrive rotating counter-clockwise (screen), decelerating, each into its own slot: angle (0° = right, −90° = up) blue −33° f72 → −62 f74 → −72 f76 → −81 f80 → −86 f86; magenta 136 → 118 → 108 → 99 → 91; green 32 → 21 → 16 → 9 → 3.5; yellow −154 → −159 → −165 → −172 → −177. Radii settle 110–163 → 139–150. Halo grows ⌀ 160 (f75) → 200 (f80) → 217 (f86). Table `S2_orbit` has every frame (centre, bbox, r, deg).
- **Collapse f88–f100:** icon shrinks accelerating (ease-in): 116, 115, 112, 110, 107, 104, 99, 95, 89, 81, 71, 59, 25 (f100); from f96 it drifts up-left (centre (352, 350) at f100). Squares slide toward a horizontal line y≈356 to the icon's right: yellow passes behind the icon (r 139 → 59), blue drops (217 → 305 y), magenta rises (506 → 436 y), green holds (509–518, 360). Blur σ 0.2 (f88) → 0.5 (f92) → 1.0 (f94) → 2.0 (f96) → 3.0 (f97) → 4.6 → 7.1 → **11.2 (f100)**.
- Out: hard cut f101 into the blurred menu bar showing the icon followed by blue, green, magenta dots — a match-cut (the yellow square does not reappear in the menu bar).

#### S3 · f101–158 · Menu bar → click → glass prompt → typing → whip-tilt (REPLACE: icon; menu-bar dots follow the squares)

- **Layout (f150, settled):** white page above (`#FDFDFB`); laptop bezel black band y283–317 (top edge highlight `#686866`); menu bar y318–359 `#232149`; wallpaper below, deep blue-violet gradient with lighter diagonal streaks. Menu-bar right cluster (white, ≈23 px type): Wi-Fi (≈199, 339), battery (≈257, 339), control toggles (≈314, 339), **app icon tile [354, 320, 389, 355]** (35 px black, white glyph), dots ⌀ ≈24: blue (408, 337), green (441, 337), magenta (473, 337) (pitch 32.6 px), "Mon Jun 22" x515–628, "9:41 A…" x657→off-frame.
- **Enter (f101–f110):** camera settles from the cut's motion: blur σ 2.1 (f101) → 1.5 (f104) → 0.9 (f107) → 0 (f110); bezel top y 305 → 300 (f108); menu-bar dot spacing 37 → 33 px (slight zoom-out 1.12 → 1.0). The laptop's top-right corner is visible at x≈680–707 (rounded bezel corner, radius NOT PINNED ≈60) until the pan.
- **Cursor:** enters from below: arrow body top-left (333, 428) f102 → (315, 406) f103 → (308, 395) f104 → (306, 384) f105 → (306, 377) f106, reaching the icon's lower edge f107; the tip then sits on the black icon (hidden) f107–f117 while the visible body shrinks (body bottom y 420 f106 → 387 f117 = **press ≈ f113–f117**). Hidden in the pan blur f118–f120; body visible again f121–f132 (just right of the icon, (366→384, 376)); gone from f133.
- **Camera pan:** content moves right +83 px (blue dot x 325 f112 → 329 f114 → 336 f116 → 351 f118 → 367 f119 → 382 f120 → 391 → 396 → 399 → 401 → 403 → 405 → 406 → 407 → 408 f130): starts f115, peak 16 px/frame f118–f120, ease-out to f130. Blur during pan σ ≤ 1.0.
- **Glass prompt box (M5):** grows out from under the menu-bar icon: a faint blurred ghost at ≈(220–395, 385–510) f117, measurable from f119: [167,386,485,537] f119, [144,392,546,544] f120, [129,397,578,549] f121, [122,399,596,551] f122, [120,400,616,552] f125, peak width 496 at f126, settles [131,379,615,531] = **484×152**, radius **40** by f138. Frosted glass: fill `#525EC5` → `#404DAB` (top → bottom), 1–2 px light border `#5A6BC0` brighter on the top edge, soft blur of the wallpaper behind. Inside: text line left x169, cap top y415; bottom row of three white outline icons at y≈490 (waveform x≈179, paperclip ≈243, image ≈309); send button: cyan `#1EB3FA` disc [558, 474, 592, 508] (⌀ 34) with a white up-arrow.
- **Typing** (read per frame from crops; caret "|" visible on every frame, no blink): first legible f121 "Tell |" (5 chars, already typed while the box was blurred), then "Tell m" f123, "Tell me" f124–125, "Tell me " f126, "…a" f127, "…ab" f128–129, "…abo" f130, "…abou" f131, "…about" f132–133, "…about " f134, "…t" f135–136, "…th" f137, "…the" f138, "…the " f139–140, "…p" f141, "…py" f142–143, "…pyr" f144, "…pyra" f145, "…pyram" f146–147, "…pyrami" f148, "…pyramid" f149, **"Tell me about the pyramids" complete f150**. Cadence: 21 chars over f122–f150 = **0.75 char/frame (≈22 char/s)**, pattern ≈ 1 char per frame with a 1-frame hold every 2–3 chars. Keyframe track (frame, chars): `[[121,5],[123,6],[124,7],[126,8],[127,9],[128,10],[130,11],[131,12],[132,13],[134,14],[135,15],[137,16],[138,17],[139,18],[141,19],[142,20],[144,21],[145,22],[146,23],[148,24],[149,25],[150,26]]` (table `S3_typing`). Text right edge (caret) x: 195 f122 … 425 f150.
- **Exit whip-tilt (M6):** from f136 the whole scene drifts up, accelerating: menu-bar dot y 354 (f130) → 352 (f136) → 350 (f140) → 347 (f144) → 343 (f147) → 337 (f150) → 332 (f152) → 324 (f154) → 312 (f156) → 302 (f157) → 285 (f158); bezel top 299 → 283 → 234. Blur σ 0.3 (f150) → 0.6 (f152) → 1.0 (f154) → 1.9 (f156) → 3.5 (f157) → **8.4 (f158)**, vertical. Page tint begins f154 (`#FCFCFC`) → `#F9FAFC` → `#F5F9FD` → `#EEF7FE` → `#E6F4FE` (f158).
- Out: hard cut f159 while still moving.

#### S4 · f159–186 · The answer scrolls in (REPLACE: all answer text — pyramid content)

- **Layout (f180, settled):** left-aligned text column at x = 80, cut off by the right edge (lines run past x 720); line tops 0 (partial), 43, 113, 191, 229, 268, 345, 394/423, 461, 501, 539, 578, 617, 656, 695 → pitch 38.7 px, one blank line between paragraphs. All body text grey `#BCBCBA` (≈31–32 px); only "**Pyramid of Khufu**" is black semibold, box [231, 346, 471, 374]. Top and bottom lines fade out (they are lighter/softer at y<60 and y>640: an edge fade, strength NOT PINNED).
- **Scroll-in (M1 + M6):** text block y offset vs f180 (`dy`, px): **280 f159, 210 f160** (eye, bold-line centre on smeared frames), 140 f161, 113, 93, 77, 64, 54 (f166), 45, 38, 32, 26 (f170), 22, 18, 14, 11, 9 (f175), 6, 4, 3, 1, **0 f180**, then keeps drifting −1 … −4 (f185–f186). Share of remaining distance 16–19 %/frame = expo-out. dx = 0 throughout.
- Blur σ: 16.0 (f159, vertical streaks), 9.9, 6.2, 3.7, 2.5, 1.9, 1.5 (f165), 1.2, 1.0, 0.8, 0.65, 0.6 (f170), ≤0.5 after.
- Light-blue flash: page `#E2F4FE` (f159) → `#E7F5FE` → `#F0F9FC` → `#F8F9FD` → `#FAFAFC` → `#FCFBFC` → `#FDFDFB` (f165).
- **Cursor** (black arrow rotated to point **up**, body 14–18 × 30–33 px): tip (334, 490) f166 → (336, 482) → (337, 475) → (336, 468) → (335, 462) f170 → (332, 457) → (328, 451) → (322, 444) → (314, 435) → (307, 424) f175 → (302, 415) → (300, 407) → (299, 401) → (299, 397) → **(300, 394) f180** (just under "Pyramid") → (301, 392) → (303, 390) → (307, 388) → (310, 387) → (316, 387) f185. It rides up with the text, then drifts right.
- Out: hard cut f187 — the card appears already rising over the same text.

#### S5 · f187–214 · Photo card rises over the blurred answer (REPLACE: photo, "Pyramid of Khufu", "Cairo, Egypt")

- **Card:** pure white `#FFFFFF` panel x135–585 (450 wide), bottom runs off-frame; no visible drop shadow (edge is only `#FFFFFF` vs `#FDFDFB`). Photo inset 16 px left/right: photo [151, 232, 569, 589] at f205 = **418×357**, radius **43**; a grey grabber bar `#62707C` ≈40×5 at the photo's top centre (x340–380, y250–255 f205). Caption "Pyramid of Khufu" black semibold centred x262–458, y643–666 (baseline ≈666); sub-caption "Cairo, Egypt" `#969696` y684–695.
- **Rise (M1):** photo top y 428 (f187, clipped at frame bottom) → 364 → 339 → 320 → 304 (f191) → 292 → 282 → 274 → 268 → 263 (f196) → 258 → 254 → 250 → 246 (f200) → 243 → 240 → 237 → 235 → 232 (f205) → 230 → 227 → 225 → 223 (f209) → … (11–16 %/frame, then a constant ≈2.5 px/frame drift). x stays 150–152.
- Card blur σ: 1.2 (f187), 1.8, **2.5 (f189)**, 2.2, 1.8, 1.3, 1.2, 1.0, 0.8, 0.6, 0.5 … ≈0 by f201.
- **Backdrop blur:** the answer text behind blurs as the card arrives: σ 0.9 (f187) → 1.3 (f190) → 1.6 (f194) → **1.7 (f198–f208)** (gradient-energy estimate on the text left of the card; visually it reads as ≈2 px).
- **Exit (M3):** from f207 the card shrinks slightly and drifts up (photo 416 → 397 px wide f207–f214) while the whole frame blurs: σ 0.55 (f207), 0.6, 0.9, 1.5 (f210), 2.1, 2.9, 3.7, **4.9 (f214)**; backdrop σ 2.2 → 6.9.
- Out: hard cut f215 at the blur peak.

#### S6 · f215–244 · Two stacked cards "Khufu" / "Khafre" (REPLACE: photos, titles, "Explore")

- **Layout (f230):** page `#FFFFFF`. Top card photo [180, 112, 539, 344] = 359×232, radius **38**; bottom card [181, 368, 539, 598] = 358×230; gap 24 px; both centred on x = 360. Each card: frosted "Explore" pill top-left (≈ x206–287, y128–156, fill `#8D99AC`, text `#ECF3FE` ≈13 px), frosted round "•••" button top-right (⌀ ≈26 at (500, 142)), and a huge bold title set along the bottom edge in **frosted glass** (backdrop-blurred, lightened photo; letters clipped by the card's bottom edge): "Khufu" on the top card, "Khafre" on the bottom card.
- **Enter:** cut in blurred σ 7.9 (f215) → 6.0 → 4.7 → 3.4 → 2.4 → 1.7 (f220) → 1.2 → 0.9 → 0.7 → 0.3 (f224) → sharp. Top card enters slightly large (387 px wide f215 → 367 f218 → 363 f222 → 359 f230) and rises: y0 176 → 161 → 152 → 145 → 140 (f219) → 136 → 132 → 129 → 127 → 123 → 121 (f225) → 119 → 117 → 116 → 114 → 112 (f230). Bottom card rises from further down (y0 618 f215 → 504 → 501 → 445 → 429 → 417 (f220) → 400 → 393 → 387 → 382 (f225) → 378 → 368 (f230)), i.e. staggered behind the top card.
- **Drift then exit:** both drift up ≈2 px/frame f230–f238 (112 → 99), then accelerate up (ease-in): top y0 96 (f239), 91, 86, 80, 71, **54 (f244)**; blur σ 0.36 (f239) → 0.5 → 0.65 → 0.8 → **1.2 (f244)**, vertical (`gx_gy` 1.0 → 1.63).
- Out: hard cut f245 to the blurred logo disc (M3 second half).

#### S7 · f245–300 · Logo disc alone (REPLACE: logo)

- Page `#FDFDFB`; disc `#F6F6F6` ⌀ **112** (radius fit 56), glyph `#353333` 54×69 px [332, 325, 386, 394] at rest; rest centre (360, 360).
- **Rise:** disc top y 379 (f245) → 358 → 346 → 338 → 332 → 327 (f250) → 324 → 320 → 319 → 316 → 314 (f255) → 312 → 312 → 311 → 310 → 309 (f260) → 308 → 307 … 304 (f269), hold f269–f287 (the only frozen stretch). Blur σ 2.4 (f245, vertical smear) → 1.3 → 0.9 → 0.8 → 0.6 → 0.5 (f250) → 0.4 → 0.2 → 0 (f256).
- **Shrink:** from f288, accelerating (ease-in): disc ⌀ 111 (f288), 109, 109, 109, 108, 107, 106, 104, 104, 101 (f297), 98, 92, **82 (f300)**; blur σ 0.2 → 0.7 (f300).
- Out: hard cut f301 to black.

#### S8 · f301–359 · End card (REPLACE: "dnyxstudios")

- Black radial bg: corners `#020204`, ≈`#272729` just above the word, `#232325` below, falling off over ≈220 px; the glow halo (lum > bg + 12) spans ≈x8–704, y144–576 at f320.
- Word "dnyxstudios" white `#F3F3F5`, centred (360, 359), with a soft white outer glow (≈20–30 px spread, NOT PINNED exactly).
- **Motion:** enters oversized and smeared horizontally (f301: only "…yxstud…" fits the frame, ≈1100 px wide by eye; f302 ≈900; f303 ≈740), then ease-out zoom-out: word width 699 (f304), 642, 588, 552, 520, 489, 469 (f310), 452, 438, 426, 416, 406 (f315), 398, 390, 384, 380, 375 (f320), 372 … 360 (f325) … 350 (f334) … 342 (f344), slow shrink ≈1 px/frame; then collapse (ease-in) f350–f359: 328, 325, 321, 314, 306, 300, 288, 270, 243, **178 (f359)**. Blur σ 2.7 (f301) → 1.1 → 0.9 → 1.0 → 0.6 → 0.6 → 0.4 → 0.3 (f308) → 0 … → 0.6 (f353) → 0.8 (f357) → 1.0 (f358) → 2.3 (f359).
- The file ends on f359 mid-collapse; there is no black hold.

---

## 3. Component inventory (build each as an HTML/CSS component)

Sizes at 1× = the settled frame named.

1. **Haze background** — full-frame `#B7CFEB` with a floor gradient to `#CDE1F8`, cross-fading to the warm page `#FDFDFB` over f0–f28 while keeping a bottom glow (`#EBF5FD` at y540 → `#DBEEFD` at y700).
2. **App window** — 62 px corner radius, 1 px `#F5F7F8` hairline, fill `#FCFDFF`, top band `#F1F6FF`, blue inner floor glow `#DDEFFE`; a left column of two faint icons (centred x≈358; column width NOT PINNED); content card with a globe tile + title + meta + site screenshot. No drop shadow measured.
3. **Header row** — logo disc ⌀ 88 (`#FBFCFE`, 1 px rim `#E8E8EA`, dark-grey glyph `#383737`, ≈40 px wide (x340–379)), app name 42 px Regular black, capsule pill 123×47 `#2F2E2F` with white 21 px Medium label.
4. **Hover ring** — 14 px wide soft ring `#D5F3FF` → `#F7FEFF` around the disc (outer ⌀ ≈116 at 1×).
5. **Cursor** — macOS arrow, black fill, white outline, ≈21×26 px at rest (S1), ≈31×41 on hover; rotates to face travel direction; S4 version points straight up (≈15×32).
6. **App icon (large)** — 119 px black squircle, radius 33, white glyph; halo disc ⌀ 217 `#E9E9E7` with a `#DEDEDE` inner ring.
7. **Orbit squares** — 61 px, radius 17, per-square gradient (see §1.1), orbit radius 139–150 around the icon centre.
8. **Laptop + menu bar** — black bezel band 34 px with `#686866` top highlight; menu bar 41 px `#232149`; white SF glyphs; 35 px black app tile; three ⌀24 dots at 32.6 px pitch; date/time text 23 px.
9. **Wallpaper** — deep blue-violet (`#170D71` TL → `#262EAC` mid → `#4651C7` BR) with soft diagonal light streaks.
10. **Glass prompt box** — 484×152, radius 40, frosted fill `#525EC5`→`#404DAB`, light 1–2 px border (top brighter), white 25.5 px text + caret, three 20 px white line icons, cyan ⌀34 send button with white ↑.
11. **Answer text column** — x = 80, 31–32 px Regular grey, line pitch 38.7, key phrase black semibold, soft top/bottom fade.
12. **Photo card (S5)** — white panel 450 wide, photo 418×357 radius 43 with a 40×5 grabber, centred semibold caption 25.5 px + grey 15.6 px sub-caption.
13. **Explore card (S6)** — 359×232 photo card, radius 38, frosted "Explore" pill, frosted "•••" circle, bottom-anchored frosted-glass title ≥112 px bold clipped by the card edge.
14. **Logo disc (S7)** — ⌀ 112 `#F6F6F6`, glyph `#353333`.
15. **End card** — black radial bg, 54 px white wordmark with outer glow.

---

## 4. On-screen text (verbatim, in order)

Brackets = cut off by the frame edge or blur, completion NOT PINNED.

| t (s) | Frames | Text | Notes |
|---|---|---|---|
| 0.07–2.40 | 2–71 | `Manus` | app name — **REPLACE** |
| 0.13–2.40 | 4–71 | `AI Helper` | pill — **REPLACE** |
| 0.50–2.40 | 15–71 | `California Orchi[d…]` · `Not published • Ju[…]` · site screenshot: `Framer`, `Features`, `Resources`, `Support`, `The in[…]` `your[…]` | third-party site card — **REPLACE** |
| 3.37–5.30 | 101–158 | `Mon Jun 22` `9:41 A[M]` | menu bar clock (keep or change) |
| 4.04–5.30 | 121–158 | `Tell me about the pyramids` | typed prompt — subject **REPLACE** |
| 5.31–6.97 | 159–209 | `[I'd be] happy to tell you about the py[ramids…]` / `[…] overview:` / `The Great Pyramids of Egypt` / `The most famous pyramids are the pyramids o[f …]` / `built during Egypt's Old Kingdom` / `(roughly 2686–2181 BC). The three largest are` / `The Great **Pyramid of Khufu** (also called Cheo[ps])` / `Built around 2589 BC for Pharaoh Khufu` / `Originally 481 feet tall; now 455 feet (erosion` / `removed the polished limestone outer layer)` / `Built with approximately 2.3 million stone bloc[ks]` / `each weighing 2–70 tons` / `One of the Seven Wonders of the Ancien[t World]` / `[The] only one still largely intact` / `[…] an elaborate tomb for the p[haraoh]` | AI answer — subject **REPLACE**; key phrase in black bold |
| 6.24–7.17 | 187–214 | `Pyramid of Khufu` / `Cairo, Egypt` | card caption — **REPLACE** |
| 7.17–8.17 | 215–244 | `Explore` `•••` `Khufu` · `Explore` `•••` `Khafre` | explore cards — **REPLACE** titles |
| 10.04–12.01 | 301–359 | `dnyxstudios` | end card — **REPLACE** (studio/brand) |

---

## 5. Cursor

- Glyph: standard macOS arrow, pure black fill (`#000`), white outline ≈2 px, faint shadow (NOT PINNED). It is a "smart" cursor: it rotates to face its travel direction and returns to the up-left pose at rest (M4).

| Path | Frames | Tip path (px) | Event |
|---|---|---|---|
| C1 (S1) | f27–f71 | (594,262) f27 → decel. left to (513,255) f44 → turns down (515,278) f48 → (529,309) f51 → blurred dash f52–55 → (419,376) f56 → (391,364) f59 → (376,353) f64 → (370,354) f71 | hover grow ×1.55 f56–f59 (ring from f53), press (shrink ≈15 %) f69–f71, cut f72 |
| C2 (S3) | f102–f132 | arrow body top-left (333,428) f102 → (306,377) f106 → tip on the icon f107–f117 (hidden) → body (366,376) f122 → (384,376) f127–f129 → (380,375) f132, gone f133 | click ≈ f113–f117 (body shrinks; box pops f116–f119) |
| C3 (S4) | f166–f185 | points **up**: (334,490) f166 → (300,394) f180 → (316,387) f185 | rides the scroll, stops under "Pyramid", drifts right |

---

## 6. Audio

Summary (details and tables in `AUDIO.md`, per-onset data in `measure/tables.json → audio`):
- Music only, **no voice** (voice-band energy 7.9 % of total; no 3–7 Hz syllable modulation; every onset sits on the musical grid).
- **124.0 BPM** (beat 0.4838 s = 14.50 frames; 8th = 7.25 frames), grid phase 0.048 s, fit error ±5 ms over 35 strong onsets. Onsets on every 8th, hats on 16ths.
- Soft intro 0–2.4 s (≈ −16 LUFS short-term, noise swells at 0.0–0.1 s and ≈1.0–1.1 s, build 1.8–2.4 s); **drop at 2.47 s (beat 5, f74)** — the picture cuts at f72; body −9 to −11 LUFS; gentle decline 10–12 s to −14.7; the file ends mid-music at 12.056 s (no fade to silence).
- Integrated loudness ≈ **−11.5 LUFS** (approximate K-weighting, numpy), peak 0.0 dBFS (limited), side/mid −11 dB (near-mono).
- Opening impact at **0.10 s (f3)**, the strongest onset of the file (all bands).

---

## 7. Brand elements to swap (REPLACE list)

**Manus identity**
- Hand/"snap" glyph logo: S1 logo disc (f0–f71), S2 large black icon (f72–f100), S3 menu-bar tile (f101–f158), S7 disc (f245–f300).
- App name "Manus": S1 header.
- "AI Helper" pill: S1 header.
- Palette tie-in: the four squares (yellow `#FAE120`, blue `#254CF6`, green `#49E81A`, magenta `#E000F7`) reappear as the menu-bar dots — recolour both together to the new brand (Athra: ember `#D3602C` family; purple/magenta banned by house taste).
- Blue product tint (haze `#B7CFEB`, window glow, flash `#E2F4FE`, hover ring `#D5F3FF`, send button `#1EB3FA`, wallpaper) — the film's accent; swap as one family.

**Third-party / content**
- Site card "California Orchid…" + Framer website screenshot (S1).
- Subject matter: prompt "Tell me about the pyramids", the whole answer text (Egypt, Khufu, 2589 BC…), photo of the Great Pyramid, captions "Pyramid of Khufu", "Cairo, Egypt", explore cards "Khufu"/"Khafre" with their photos.
- macOS chrome (menu bar, Wi-Fi/battery/Control Center glyphs, "Mon Jun 22 9:41 AM") — generic, keep only if the remake is a Mac app.

**End card**
- "dnyxstudios" (the studio that made the reference) — replace with the new brand wordmark.

---

## 8. Not pinned down

1. Anything that needs ears: instrument identities, whether the 0.10 s and 1.0 s events are whooshes or synth swells, whether a click SFX exists under f70/f114 (no off-grid onset was found there, so any click is mixed into the music or absent).
2. Fonts by eye (SF Pro / Inter). "dnyxstudios" weight and glow radius by eye.
3. f159–f160 answer-scroll offsets (280, 210 px) are eye reads; the profile matcher fails on the vertical smear.
4. f52–f55 cursor path (motion blur) and the S3 cursor tip f107–f120 (hidden on the black icon); the exact press frames are inferred from size changes.
5. Glass-box ghost geometry f116–f118 (too faint to segment); box first measured f119.
6. Full cap height of the "Khufu"/"Khafre" glass titles (clipped by the card edge); the answer text's top/bottom fade strength; the S5 card's top inset above the photo; laptop bezel corner radius.
7. Shadows: no drop shadow was measurable on the window or cards (edges are only `#FFFFFF` vs `#FDFDFB`); a very soft shadow below 2 levels would not be detected.
8. The window opacity table (f15–f29) mixes opacity with the header's 1 px/frame drift; ±0.05.
9. Blur σ values are Gaussian equivalents; directional motion blur in the source is streakier than a Gaussian (see f159, f301).
10. Cut-to-beat offset: the three clean hard cuts (f72, f101, f159) all land 65 ms (≈2 frames) **before** a beat; this is either deliberate anticipation or uncompensated AAC encoder delay — the remake should cut on the same frames, not re-snap to the grid.
