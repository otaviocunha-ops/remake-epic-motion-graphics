> Archived toolkit reference. For portable commands and current policy, read [toolkit adaptations](../references/toolkit-adaptations.md) and SKILL.md.

# CRAFT SPEC, FRAME LEVEL: measured numbers from one launch film

Purpose: give frame-level numbers for pacing, hero object, lines, counters, glitches, texture, type and sound, measured from one launch film, so a code-rendered film can match them.
Requires: `CRAFT.md` (targets and critic rubric), `PIPELINE.md` (render and finish), numpy and Pillow for the finishing recipes.
Use: read before the storyboard of a hero-object launch film. Copy the numbers into your own `CRAFT_SPEC.md` and replace them with your reference's numbers when you have one.

## 0. Source and conventions

| Item | Value |
|---|---|
| Source | One 25.7 s launch film: 1920x1080, 24 fps, 617 frames, AAC stereo 48 kHz, music and sound effects, no voice-over |
| Frame numbers | 1-based, f1 to f617. At 24 fps, 12 frames = 0.5 s |
| px | Pixels at 1080p |
| Colours | sRGB medians of masked pixels |
| Methods | Per-frame numpy statistics (luma, percentiles, saturation, frame difference, histogram difference); phase correlation plus a scale search for camera moves; masks for object and text boxes; audio band energy and onsets at 10 ms resolution |
| INFERRED | Values read from pixels, not from source files: font family, 3D light rig, absence of voice-over |

To reuse a number at another length, scale frame positions by `your_frames / 617`. Keep per-frame rates (px/frame, %/frame) as they are.

## 1. Film shape

| Movement | Frames | Length | Share | Content |
|---|---|---|---|---|
| Hook | f1-104 | 4.3 s | 17% | Dark. Logo flicker, a black hero object lit by a rim light only, a caption that builds backwards, a flat white chart line |
| Hero object | f105-170 | 2.75 s | 11% | Macro of the saturated object, then an 11-frame strobe: object fixed in frame, background changes every frame |
| Data | f171-356 | 7.75 s | 30% | Dense middle: one picture event every 4 to 5 frames. Lines with glowing heads, counters that change every frame, glitch frames at cuts, a strobing collage behind big numbers |
| Tunnel | f357-454 | 4.1 s | 16% | One shot through a corridor of thumbnails. Starts desaturated and near still, accelerates into a radial zoom blur |
| End cards | f455-617 | 6.8 s | 26% | A white flash, 2 text cards and the logo on flat `#0A0A0C`, zero grain |

Rules:
1. Texture follows the arc: grain and lifted blacks in f105-357, zero grain from f455.
2. Energy hands off from cut rate to camera speed: 0 cuts for 98 frames in the tunnel, camera speed doubling every 6 to 7 frames.

## 2. Pacing

Picture-change events per second (cuts, glitch frames and flashes):

| Second | Events | What |
|---|---|---|
| 0 | 10 | Logo flicker |
| 1 | 2 | |
| 2-3 | 0 | 60-frame chart shot: the slow "before" |
| 4 | 1 | |
| 5 | 4 | |
| 6 | 17 | Strobe preview, f158-168 |
| 7-8 | 5 each | |
| 9 | 13 | Counter and curve run, f217-240 |
| 10-13 | 5 each | One event every 4.8 frames |
| 14 | 12 | Counter strobe, f340-356 |
| 15-17 | 0 | Tunnel: one shot, motion carries it |
| 18 | 2 | White flash |
| 19-25 | about 0.5 | End cards |

Readability rules while cutting at this rate:
1. Keep one anchor object still while everything else changes. The hero object holds its screen position within ±10 px through the 11-frame strobe. Captions hold x within ±1 px while charts move under them.
2. Give every readable element at least 8 frames, even when the cuts around it are 1 to 2 frames. Measured: a counter card 8 frames, a brand caption 22 frames, a tunnel caption 40 frames.
3. Make glitch frames exactly 1 or 2 frames long and place them only at cut points.
4. Change numbers every frame, but keep the digit count and the unit label fixed.
5. Limit captions to 7 words and one idea per shot.
6. Mark impacts with 2-frame holds (identical frame pairs). Measured pairs: 73/74, 97/98, 145/146, 169/170, 171/172, 217/218, 241/242, 265/266, 337/338.

## 3. Hero object

### 3.1 Model (INFERRED from f105-170)

| Part | Measure |
|---|---|
| Cap | Cylinder, flat top, top-edge bevel radius 4% of diameter. At f152: diameter 900 px on screen, side wall 156 px (height 0.17 × diameter) |
| Logo on the cap | Debossed 1 to 2% of the diameter deep. Reads through a dark shadow on the upper inner walls and a 2 to 4 px specular sliver on the lower walls |
| Collar | Chrome ring under the cap, 4% of cap diameter tall |
| Base | Polished chrome ring, 1.15 × cap diameter wide, 0.08 × tall, dark lower lip |
| Cap material | Glossy lacquer. Side face in shadow `#7C0002` (green channel clipped to 0). Lit top `#E5A5A8`; `#BB4653` after the punch-in grade |
| Chrome | Mirror, roughness 0.05 to 0.1, reflecting vertical softbox strips: dark bands 40 to 60 px wide, highlights `#E6E0D4`, underside `#1A1A18` |

### 3.2 Camera and light by shot

| Frames | Framing | Camera move | Light |
|---|---|---|---|
| f18-31 | Eye level, object 840 px wide, centre y 585 | Static f18-26, then +1%/frame scale f27-31 | Rim only: a 2 to 4 px white line (value 209 to 220) along the base, 15 px bloom. Faces near black (6,5,3). Rim p99 fades 87 to 53 over f18-28 |
| f32-44 | 25° elevation, 980 px wide | +1%/frame f33-37, then static | Key fades up on the top face: centre value 11, 15, 19, 34 over f33-39 (quadratic ease-in), fades down f40-44. Rim stays last |
| f105-120 | Macro, lens 5 to 10° above the cap, cap fills 76% of width | Linear push +0.40%/frame, centre fixed | Exposure rises linearly: mean L 40.4 to 64.6 (+1.6/frame) |
| f121-132 | Jump cut +10.6% scale | Linear push +0.37%/frame | Grade lift: mean L 87 to 101 |
| f134-142 | Low angle 3/4, 10° above the cap, 8° dutch tilt, 1340 px wide | Push +0.7%/frame, drift left 2 px/frame | Hard white key from camera right, black background |
| f143-168 | 12° elevation, centred, 827 to 914 px | Push +0.5 to 0.75%/frame, crane up (tilt +1.3°/frame) | Soft key from above. Backdrop grey gradient (centre 148, edge 70) or cream `#D7CEC5` |

Rules:
1. Depth of field: deep on the macro (near and far edges sharp). On wide shots, blur the strobed backgrounds 3 to 6 px so the object stays the subject.
2. Motion blur: none on the object. Every object move is slower than 10 px/frame.
3. In: hard cut from black with the rim at full value on the first frame. No fade.
4. Out of the dark object: dissolve from the inside over 5 frames. Face fill reaches 0 first, the rim last, then a hard off.
5. Into the macro: hard cut, with the previous chart kept as a screen-blend ghost at 40 to 60% for 16 frames, then fainter for 12.
6. Out of the strobe: the strobe shows the next 8 shots for 1 frame each, then cuts to them.

## 4. Lines and charts

| Line | Frames | Stroke | Draw |
|---|---|---|---|
| Flat "before" line | f50-104 | White `#E2DFDC`, axes 3 px, line 3 px, no glow, no head dot | Head moves at a constant 10.6 px/frame. The line is flat on purpose, with one dip at 40% |
| Axis growth | f52-104 | 3 px | x-axis length 181, 308, 443, 541, 618, 682, 736, 784, 827, 865 … 1285 px. Fit: `len = 1260 × (1 − e^(−(f − 52)/6.5))` |
| Brand line | f173-194 | Accent, 7 to 8 px, glow 6 px at 30% | 80 px/frame at mid-draw; last 3 frames add +37, +23, +8 px. Rises at 20° |
| S-curve | f206-218 | Accent, 15 px, round caps, no glow, on warm black `#070705` | Ease-in head gains per frame: 17, 27, 32, 36, 39, 42, 46, 48, 49 px. Logistic S |
| Curve close-up | f236-250 | 23 to 41 px, rendered at 1/4 resolution and upscaled nearest-neighbour | Camera pans (−50, −20) px/frame along the curve; the head leaves the frame at f246 |
| UI chart | f282-290 | 4 lines, 3 px | Leading edge sweeps 60 px/frame |
| Charged sine | f317-340 | Base 8 px; charged segment behind the head: core 3 px, 2 rails 3 px apart, bloom 60 to 120 px | Camera tracks the head, dx per frame −74, −42, −28, −28, −94, −190, −240, −464. Cut at peak speed |

Rules:
1. Push slowly on every chart that holds: +0.25%/frame about the frame centre.
2. Axis labels: 22 px, medium weight, 10 px tick marks. Y labels appear one per step (f54, f55, f59, f68).
3. Use a U-shaped camera speed on UI and chart shots: high speed at both ends, low in the middle. Measured vertical tilt per frame: 30, 22, 16, 12, 10, 10, 12, 16, 20, 28, 40 px. Cut on the frame with the highest speed.
4. Place peak labels 30 px outside each extremum, 48 px regular.
5. Join a chart to the next shot with one of: a ghost carry-over (screen blend), a 1-frame strobe preview, a font-width glitch frame, a speed match (next shot starts moving in the same direction), or an inverted white-line frame.

## 5. Counters

| Counter | Frames | Rule |
|---|---|---|
| Total | f195-204 | Linear: `round(a + b × n)`, one step per frame |
| Delta chip | f195-234 | Linear on the global frame, with commas. It keeps counting through a 14-frame cutaway |
| Icon row | f303-316 | One shared sequence; each metric uses it at a different offset |
| Currency | f293-302 | Linear, floored |
| Billions | f342-344 | Ease-out (+10, +6): the only non-linear counter |
| Giant number | f345-356 | Changes every 2 frames (on twos) |

Rules:
1. Drive every counter from the global frame, not the shot's frame: `value(F) = step × (F − F0)`. Render it in every shot that shows it.
2. Change the value every frame. Change giant numbers (cap height near 50% of frame) every 2 frames.
3. Use `font-variant-numeric: tabular-nums` so the width does not change.
4. Keep the unit label ("views", "K", a currency sign) fixed in place.

Number type (1080p, INFERRED neo-grotesk):

| Element | Size | Weight | Detail |
|---|---|---|---|
| Card number | Cap 125 px (font 170 px) | 500 | Tracking −2%; unit label weight 400, same size, 60 px gap |
| Delta chip | Pill 230x70 px, radius 35 px | 500, 30 px | Card: 5 px border, 40 px radius, fill `#0A0A08` |
| Giant number | Cap 525 to 575 px (font 750 px) | 500 | Tracking −4%, warm cream `#EDE6DA`, 1480 px wide for 4 characters |
| Billions | Cap 105 px | 500 | Ghost trail of previous values 90 to 180 px to the right at 25% and 10% |
| Currency | Numeral height 150 px | 500 | Soft outer glow; blurred ghost copies behind at 1.6x size, 25% opacity, 20 px blur |
| Icon row | Icons 60 px tall, 4 px stroke; numbers 42 px | 500 | 14 px gap after each icon |

Entries and exits:
1. Flying number (f228-234): duplicate the value as an overlay at 5x (cap 250 px) with a 40 to 60 px bloom at 60%. Hold 4 frames while the value changes. On the last frame scale it 2.1x with a 15 px blur so it passes the camera. Follow with a glitch frame.
2. Insert 1 frame of whole-frame defocus (Gaussian 12 px) inside the flying-number run.
3. Giant number: hard cut in at full size, no scale animation.
4. Strobing collage behind the giant number: 2 plates, A (dark blurred chart, mean L 52 to 66) and B (bright desaturated collage of 120 thumbnails, mean L 130 to 146). Schedule by frame: A B A B B A A B B B B, then a glitch. The irregular order is measured, not random.
5. Put collage flashes under numbers, never over them.

## 6. Glitches

| Type | Look | Length |
|---|---|---|
| G1 tape dropout | Horizontal white dashes 2 to 4 px tall, 20 to 120 px long, 20 to 60 per frame, 1 to 2 rows shifted sideways | 1 frame |
| G2 RGB speckle | Single-pixel chroma speckles over the whole frame (noise std 6 to 11), horizontal banding, text doubled 50 px to the right | 1 frame |
| G3 font-width swap | All text snaps to an ultra-condensed or ultra-extended black weight, same layout and colours, strokes 3 to 5x thicker | 1 to 2 frames |
| G4 pixel sort | Vertical streaks smeared down from bright seeds | 1 frame |
| G5 invert/threshold | Line goes white-hot; background inverted to high-contrast paper white `#F0EEE8` with black blocks; numbers embossed | 1 frame |
| G6 content flash | Another shot's plate | 1 frame |
| G7 defocus | Whole-frame Gaussian 12 px | 1 frame |
| G8 white flash | `#FFFFFF`, or cream `#F3F4EE` before the logo | 1 frame |
| G9 blank | Flat `#0A0A0C` or black | 1 frame |
| G10 low-res | Edges stair-stepped in 4 px blocks | 1 to 15 frames |
| G11 echo | Previous value or frame offset 50 to 180 px at 10 to 25% | 1 to 3 frames |
| G12 block displacement | A rectangle of the frame shifted 40 px right with a white tear | 1 frame |

Rules:
1. A glitch frame replaces the first or last frame of a shot. It never sits inside a reading moment.
2. Frequency in the data section (f133-357, 224 frames): 40 glitch or flash frames, one every 5.6 frames. Hook: 3. After f358: only the 2 flashes.
3. Chromatic split appears only in G2, G5 and G11 (fringes 2 to 4 px). No constant chromatic aberration.

## 7. Grade and texture

| Section | Black level | Palette | Notes |
|---|---|---|---|
| Hook | `#020201`, p1 luma 0.2 to 1.0 (crushed) | Warm off-white `#E2DFDC` | Blue channel near 60% of red in the blacks |
| Macro | Black surround | Selective colour: only the accent survives, the rest is monochrome | Accent green channel clipped to 0 |
| Strobe | Grey gradient (centre 148, corners 70) or cream `#D7CEC5` | Monochrome plus the accent | |
| Data | `#070705` to `#0E0E0C`, p1 4 to 7 (lifted 4 to 6 levels) | One accent colour per shot | |
| Tunnel | p1 3.9 to 10 | Saturation 2.1 and mean L 13 at start; colour from f420 (saturation 5 to 14 at f437), L 20 to 55 | Colour arrives with the acceleration |
| End | Flat `#0A0A0C`, zero grain (high-pass std 0.0) | Text `#EBEBE9` to `#F3F4F0` | |

Rules:
1. Grain: midtones only, f105-357. High-pass std 5.3 on a grey backdrop. Clumped, not per-pixel: autocorrelation 0.82 at 1 px, 0.66 at 2 px, 0.54 at 3 px (grain size 2 to 3 px). Near zero in crushed blacks (std 0.25) and clipped cream (std 0.28).
2. Vignette on light plates: 6% darker at the corners. On a lit backdrop the falloff is 53% (148 centre to 70 edge).
3. Bloom radii: object rim 15 px, charged sine 60 to 120 px, flying number 40 to 60 px, accent ring 40 px haze.
4. Text never blooms, except in inverted glitch frames.

## 8. Type

INFERRED face: a neo-grotesk with a single-storey g, a double-storey a and a flat-sided t.

| Use | Frames | Size (1080p) | Weight | Colour | Placement |
|---|---|---|---|---|---|
| Hook caption, 2 lines, 7 words | f40-100 | 60 px, leading 53 px (0.88 em), 749 px wide | 400 to 500 | `#E2DFDC` | Centred, top at y 486 (45% down); scales with the chart push |
| Short caption on the object | f134-147 | 66 px | 500 | `#F0ECE6` | On the object's front face |
| Brand caption, 4 words | f173-194 | Cap 55 px (font 75 px), 1122 px wide | 400 for the lead words, 600 for the brand | Accent | Centred at y 540, over the chart |
| Tunnel caption, 7 words | f368-426 | 80 px, 1154 px wide, 1 line | 600 | `#F2F0EC` | Baseline y 561, fixed while the tunnel moves |
| End card 1, 5 words | f456-502 | 86 px (cap 63), 1133 px wide at rest | 600 | `#EBEBE9` | Centred, baseline y 563 |
| End card 2, 3 words | f503-551 | 81 px (cap 59), 423 px wide | 600 | `#F3F4F0` | Centred, baseline y 563 |
| Logo lock-up | f3-17, f553-617 | 432 to 441 px wide, 137 to 141 px tall | | `#E4E1DB` intro, `#F3F4F0` end | Dead centre |

Rules:
1. Tracking: −1% on captions, −2 to −3% on cards of 80 px and larger.
2. Sentence case everywhere except the brand name.
3. Backwards build (hook, brand caption): reveal the last word first, 1 word per frame. Each word enters at 50% grey, 12 to 18 px below its baseline, settles over 2 to 3 frames with an ease-out, and reaches 100% in 3 frames. Words already on screen do not move. Line 2 completes before line 1 starts.
4. Forwards build (tunnel caption): 1 word every 2 frames, 35% to 100% over 8 frames, no position change. Exit: forwards, 2 frames per word, as a left-to-right fade.
5. End card 1: on its first frame (after the white flash) the words sit at 90%, 70%, 45%; the last word sweeps in through a per-character gradient mask 3 characters wide over 6 frames. The line settles from 107% to 100% scale with an ease-out over 45 frames.
6. End card 2: first words at 55%, last word at 30% two frames later; all ramp linearly to 100% over 16 frames. Drift x −47 px, y −10 px over 48 frames, ease-out, no scale change.
7. End logo: full brightness on the first frame after the cream flash. Scale 102.5% to 100% over 12 frames, ease-out, then hold 65 frames.

## 9. Tunnel

| Frames | Speed | Look |
|---|---|---|
| f359-400 | Under 0.3%/frame scale (frame diff 2.2 to 3.4) | Near still, desaturated, caption on screen |
| f401-419 | Frame diff 3.4 to 12 | Accelerating |
| f426-432 | 3.0 to 4.5%/frame | Colour arriving |
| f433-441 | 8 to 10%/frame | Full colour, card motion blur starts |
| f442-450 | Above 10%/frame, camera yaw and roll (dx up to 234 px/frame) | Streak blur 30 to 80 px |
| f451-454 | Radial zoom blur, streaks 200 to 600 px | Burst at the vanishing point |
| f455 | Pure white | Flash on the kick |

Rules:
1. Geometry (INFERRED): a rectangular corridor tiled with thumbnails (9:16, 1:1, 16:9, 30 to 200 px on screen), vanishing point at frame centre.
2. Speed doubles every 6 to 7 frames from f420. No deceleration: the shot ends at maximum speed and the white frame absorbs the cut.

## 10. Sound

Music on a 120 BPM grid = 12 frames per beat at 24 fps. Downbeats fall on frames 6 + 12k.

| Frames | Audio | Picture |
|---|---|---|
| f1-5 | Digital silence | Black, first logo flash at f3 is silent |
| f6-40 | Low drone at −26 dB, no highs | Rim-lit object |
| f28-38 | Noise swell in the 4 kHz+ band (+8 dB) | Key light fades up |
| f41-110 | Bass enters, −23 to −19 dB | Caption builds from f40 |
| f75-103 | Ticks every 1.45 frames (16.5 per second) | Line drawing |
| f111-117 | Impact or whoosh, −15 dB | 6 frames into the macro |
| f171-176 | Drop: loudest point, −3.8 dB RMS | Cut to the brand caption |
| f176-365 | Dense, −6 to −15 dB, kicks on the grid | Data montage |
| f365-376 | Second peak, then highs filtered away (−22 dB in the 4 kHz+ band) | Tunnel starts, caption types on |
| f431-448 | Bass removed, −17 to −21 dB | Tunnel accelerates |
| f455.8 | Hit, −6.6 dB | White flash |
| f466-496 | Breakdown at −25 to −28 dB | End card 1 |
| f497.8, f551.8 | Kicks | End card 2 at f503, cream flash at f552 |
| f617 | −22.7 dB with a high click | Hard out, no fade |

Rules:
1. Land flashes and card changes within 1 frame of a kick.
2. Put the brand line on the drop.
3. Match loudness to visual density: remove bass and highs when the picture turns flat and grain-free.
4. Give line draws and counters a tick at 16 per second, 1 tick per value change.
5. End on a hard out with a sound. No fade to silence.

## 11. Recipes

1. Anchor object with a strobing background: render the object once in a three.js layer on a constant push, `scale = 1 + 0.006 × (F − F0)`, crane `camera.position.y += 0.02` per frame. Swap only the background plate each frame from a list of the next shots' stills. Blur the plates 4 px.
2. Selective colour in the numpy finish:
   ```python
   def smoothstep(a, b, x):
       t = np.clip((x - a) / (b - a), 0, 1)
       return t * t * (3 - 2 * t)
   R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]   # float32, 0..255
   lum = (0.2126*R + 0.7152*G + 0.0722*B)[..., None]
   mask = smoothstep(0.35, 0.55, (R - np.maximum(G, B)) / (R + 1e-3))[..., None]
   out = lum*(1 - mask) + rgb*mask
   ```
   Then scale G and B by 0.1 inside the mask to reach a deep shadow red. Change the channel test for another accent hue.
3. Rim-only reveal: no ambient light. One spot behind and below the object (angle 0.3), a second rim behind and above. Key fade-up over 7 frames: `k = ((F − F0)/7)^2`. Exit: fade key and emissive to 0 over 5 frames, keep the rim, then hide the mesh. Bloom strength 0.6, radius 0.2, threshold 0.7, rim only.
4. Backwards caption: one `<span>` per word, revealed in reverse order at 1 frame per word; each span goes `translateY(16px)` to 0 and opacity 0.5 to 1 over 3 frames with `cubic-bezier(.2,.7,.2,1)`.
5. Counters on the global frame: `value(F) = step × (F − F0)`, `Intl.NumberFormat('en-US')`, `Math.round` (floor for currency), `Math.floor(F/2)` for giants, tabular numerals.
6. Font-width glitch: a variable font with a width axis. On the glitch frame set `font-variation-settings: 'wdth' 25, 'wght' 900` (bars) or `'wdth' 150, 'wght' 900` (slabs) and multiply SVG stroke widths by 4. Show 1 frame, then hard cut.
7. Charged line: 3 SVG paths per segment. Base stroke 8 px. Rails 3 px, drawn twice at ±3 px offset, clipped with `stroke-dasharray: len; stroke-dashoffset: len × (1 − p)`. Core 2 px, same clip. Add a bloom copy of the rails with `blur(40px)`, opacity 0.8, `screen` blend, and a radial glow sprite (radius 120 px) at `getPointAtLength`.
8. U-shaped speed: position `p(t) = t + A × sin(2πt)/(2π)` with A = 0.7. Speed is `1 + A × cos(2πt)`: high at both ends. Cut on the peak-speed frame.
9. Constant push: wrap every shot in a camera group, `scale = 1 + r × (F − F0)`, r = 0.0025 on charts, 0.004 on macros, 0.005 to 0.0075 on wides. End cards settle with `1 + 0.07 × e^(−(F − F0)/12)`.
10. Jump-cut punch-in: same render, zoom × 1.106 and exposure +25% at the cut frame, same push rate after it.
11. Holds and plate schedules: `if (HOLDS.has(F)) F = F − 1`; plate order from a literal array such as `['A','B','A','B','B','A','A','B','B','B','B']`.
12. Ghost carry-over: keep the previous graphic as a top layer with `mix-blend-mode: screen; opacity: .5` for 16 frames, then fade to 0.15 over 12 frames.
13. Texture per section: grain σ = 5 (0 to 255) blurred 1.2 px, weighted `w = 4L(1 − L)`; blacks `#020201` in the hook, `#070705` in the data section, flat `#0A0A0C` with no grain on end cards; vignette `1 − 0.06 r²` on light plates; bloom threshold 0.75, blur 25 px (60 px on glow shots), added at 0.6. G2 frames only: chroma noise σ = 20 per channel, ±8 px offsets on 5% of rows, ghost copy at x + 50 px at 25%.
14. Tunnel: 3000 `PlaneGeometry` cards in an `InstancedMesh` on the 4 walls of a 40x24x400 corridor, texture atlas of thumbnails. Speed `v = v0 × 2^((F − 420)/6.5)`. Saturation 0.05 to 1 over 20 frames; exposure 0.3 to 1. Accumulate 8 subframes per frame at high speed. Last 4 frames: radial zoom blur in numpy, 16 copies scaled `1 + k × i` about the centre, k up to 0.04. End on a pure white frame on the kick.
15. Beat grid: author on 12-frame beats at 120 BPM. Brand line on the drop; flashes and card changes on kicks.

## 12. Colour tokens

| Token | Hex |
|---|---|
| Hook black | `#020201` |
| Data page | `#070705` |
| Card | `#0E0E0C` |
| End black | `#0A0A0C` |
| Hook white | `#E2DFDC` |
| End white | `#F3F4F0` |
| Accent in shadow | `#7C0002` to `#890010` |
| Accent lit | `#BB4653` |
| Cream backdrop | `#D7CEC5` |
| Line accent | `#C16411` |
| Hot core | `#EBC499` |
| Glow | `#964221` |
| Cream flash | `#F3F4EE` |

## Check

- [ ] Every readable element in your film is on screen for 8 frames or more without glitch or blur.
- [ ] Every glitch frame is the first or last frame of a shot, 1 or 2 frames long.
- [ ] Every counter changes each frame (giants every 2) and is computed from the global frame.
- [ ] Flashes and card changes sit within 1 frame of a kick on the beat grid.
- [ ] End cards have zero grain; the data section has grain in the midtones only.
- [ ] The frame positions copied from this file were scaled by `your_frames / 617`.
