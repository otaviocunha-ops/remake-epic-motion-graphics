> Archived toolkit reference. For portable commands and current policy, read [toolkit adaptations](../references/toolkit-adaptations.md) and SKILL.md.

# CRAFT: motion, type, colour, sound and texture rules

Purpose: set measurable targets for a brand or launch film, and score a render against them.
Requires: 2 to 4 reference films; `PIPELINE.md` for render commands; a taste file (`TASTE_FILE_TEMPLATE.md`).
Use: read once before the storyboard. Keep section 3 open while building. Run section 4 after every render.

Frame maths: frame counts in this file assume 24 fps (frames per second) at 1080p. 12 frames = 0.5 s. The engine default is 30 fps (`window.FPS`). At another rate, multiply frame counts by FPS / 24.

## 0. Reference films

1. Choose 2 to 4 reference films before the storyboard. Use only films licensed for private study.
2. Extract every frame and the audio (`prompts/REMAKE_ANY_VIDEO.md`, Phase 0).
3. Make contact sheets (grids of stills at a fixed interval) for each film.
4. Measure each film with the methods in section 4 and `prompts/LAUNCH_FILM.md`, Phase 0. Write the numbers into `CRAFT_SPEC.md`.
5. Do not copy lines of dialogue or narration from a reference film.

## 1. Targets

### 1.1 Cut rate

Targets for a 55 s launch film:

| Section | Cuts per second |
|---|---|
| Cold open | 0.8 |
| Essay section | 1.0 to 1.3 |
| Product act | 1.5 to 1.8 |
| Tunnel | 0 cuts, camera accelerating |
| Ending | ≤ 0.5 |

Readability rules:
1. Hold every readable element for at least 8 frames without glitch or blur.
2. Hold a number plus its label for at least 0.4 s.
3. In a strobe section, keep one anchor object locked within ±10 px while the background changes.
4. Keep captions fixed within ±1 px while charts move under them.
5. When a section runs above 1.8 cuts/s, extend the holds on every readable element first.

### 1.2 Glitches

1. Length: 1 to 2 frames.
2. Placement: the first or last frame of a shot only. Never during a reading moment.
3. Frequency: at most 3 in a calm section; at most 1 per 5 frames in a dense section; 0 on tunnels and end cards, except planned flashes.
4. White flashes: place on section boundaries, 0 to 110 ms before a music hit.
5. Sound: every glitch cut carries a noise click of 50 ms.

Glitch vocabulary:

| Type | Appearance |
|---|---|
| Tape-dropout streaks | White horizontal dashes, 2 to 4 px tall |
| RGB speckle | Single-pixel colour noise, heavier than the film grain |
| Font-width swap | UI text switches to an ultra-condensed or ultra-wide black face, strokes 3 to 5× thicker, on a data cut |
| Pixel-sort | Columns smeared down from a bright seed |
| Invert / threshold | White-hot line on an inverted high-contrast background |
| One-frame content flash | Another shot's picture for exactly 1 frame |
| Defocus flash | Whole frame blurred 12 px |
| White or cream flash | `#FFFFFF`, or a cream such as `#F3F4EE` |
| Low-res stair-steps | Blocky edges, 4 px steps |
| Echo / ghost | Previous value offset 50 to 180 px at 10 to 25% opacity |
| Block displacement | A rectangle shifted 40 px with a white tear |

### 1.3 Counters

1. Drive counters linearly from the global frame (the film's clock, not the shot's). A counter keeps running through a cutaway.
2. Change the value every frame. Giant counters change every 2 frames.
3. Keep the digit count and the unit label ("views", "K", "$") fixed. Use tabular numerals (`font-variant-numeric: tabular-nums`, every digit the same width).
4. Ease at most one counter per film. All other counters are linear.
5. Numbers flying at the camera: duplicate at 5× with a 40 to 60 px bloom (glow), scale 2.1×, soften as they pass the lens.
6. Ghost copies: 1.6× size, 25% opacity, 20 px blur; or a trail offset 90 to 180 px.
7. Tick sound on value changes: 16 per second, where the mix allows.
8. A clock shown over footage must match the light in the footage (no "2:14 am" over a sunrise).

### 1.4 Charts

1. One axis, two lines. "Before": a flat white line, 3 px, no glow, drawn at 10 px per frame, with a small dip. "After": the accent line, 7 to 8 px with a 6 px glow, rising from the origin past the "before" line (80 px per frame at mid-draw, easing out).
2. Axes grow from the origin with a strong ease-out, for example `len = 1260·(1 − e^(−(t−t0)/6.5))`. Y labels appear in steps, one per tick.
3. S-curve: 15 px, round caps, accelerating draw (ease-in). Then a 3× jump cut (same image, instantly larger) held 2 frames.
4. Charged line: base stroke 8 px. Behind the head: a white-hot 2 to 3 px core, two 3 px rails and a 60 to 120 px bloom. Head glow 120 px across. The camera tracks the head and exits at peak speed.
5. U-shaped camera speed: accelerate in, 10 px per frame mid-shot, whip out. Cut on the speed peak; start the next shot moving in the same direction. Position curve: `p(t) = t + 0.7·sin(2πt)/(2π)`.
6. Push every chart shot at least +0.25% scale per frame.
7. "Before" chart shot: 60 frames, +0.25%/frame push, 1260 px axis, one text layer.
8. Banned: lines with amplitude under 10% of chart height and more than 2 cycles ("worm" lines); thin grey lines in empty panels; axis labels that contradict the narration (weekday labels under the word "overnight").

### 1.5 Hero object

Use for a film built around one object (a 3D button, a device, a mark).

| Phase | Settings |
|---|---|
| Intro | Rim light only: 2 to 4 px white edge with 15 px bloom, faces near black, eye level, black background. Full rim value on the first frame, no fade. The object may rise. |
| Reveal | Key light fades up with an ease-in over 7 frames (`k = ((f−f0)/7)^2`). Material: accent colour, roughness 0.4, clearcoat 1. Filmic tone mapping (for example ACES). Environment map for reflections. |
| Macro | Camera high and close, linear push +0.4% per frame, exposure rising. Only the accent colour stays saturated (selective colour). The music drop lands on this cut. |
| Jump cut | Same render, +10% scale, +25% exposure |
| Strobe | Object locked at centre ±10 px while 11 backgrounds change one per frame, each blurred 3 to 6 px |
| Material detail | Chrome or brushed-metal base (metalness 1, roughness 0.3) with softbox reflections. The real logo embossed or debossed into the surface (a blurred logo image as a displacement map) |
| Press | Cap drops on a sine over 0.4 s. The sound hit lands on the bottom-out frame. |
| Exit | Dissolve from the inside out over 5 frames with the rim last, or a hard cut |

Rule: the hero object is the only saturated colour in the film. Introduce it without colour; bring it back in colour.

### 1.6 Type (1080p)

| Role | Size | Reveal |
|---|---|---|
| Hook caption | 60 px, leading 0.88 em | Builds backwards, 1 word per frame, each word from 50% grey and 12 to 18 px low, settling over 2 to 3 frames |
| Message line | 75 px | Forwards, 2 frames per word, opacity 35% to 100% over 8 frames |
| End line | 81 to 86 px | Scale 107% to 100% over 45 frames, plus a 0.8 px/frame drift |
| Logo | per brand | Scale 102.5% to 100% over 12 frames |
| Giant number | 750 px (cap height 50% of frame) | Counter rules, section 1.3 |
| Short lowercase caption | cap height 5% of frame, ≤ 4 words | Each word blurred and faint to sharp over 4 to 6 frames |
| Word-by-word statement | cap height 3.3% of frame; emphasis line 8.4%, deflating facts 4 to 5% | From the left, 0.09 to 0.2 s per word. Hold 1 to 2 s. Erase from the left. |
| Voice-over caption | Inter 600, 34 to 40 px, y 870 to 930, over a bottom gradient | On the narrator's word timestamps: 35% grey to white over 0.2 s, blur 3 to 0 px over 0.1 s. Keyword bold with a white glow. Line breaks set by hand. |

Tracking: −1% on captions; −2% to −3% at 80 px and above. Captions: ≤ 7 words, one idea per shot. End lines use 81 to 86 px unless the client approves a smaller size.

### 1.7 End cards

| Pattern | Sequence |
|---|---|
| A | Tunnel at max speed, 1 white frame on the kick, claim line (2 s), "out now" line (2 s), 1 cream frame on a kick, logo held 2.7 s. Flat near-black `#0A0A0C`, no grain. Beat drops out under the claim. Music low-passed under the logo. Hard out mid-phrase. |
| B | Sign-off line, one-word call to action, logo lockup. Music tail fades to silence. |
| C | 1.4 s of black under a ringing chord, a bookend line, a small glowing logo in silence. No call to action. |
| D | No end card. Watermark only. |
| E | Tunnel, the claim word by word on near-black, "[Product] is live.", 1 cream flash frame, mark + wordmark + URL fading in, sub-bass hit on the flash. |

Rule: a flash is 1 frame. A 3-frame flash reads as a defect.

### 1.8 Sound and beat alignment

1. At 120 BPM and 24 fps, one beat = 12 frames.
2. Place cuts within 1 to 2 frames (80 ms) of a music onset (the start of a hit).
3. Place the drop on the brand line or the hero reveal (the loudest point).
4. Remove the beat under the claim. Low-pass the music under the logo.
5. Before a drop, a near-silent black hold of 1.2 s is allowed.
6. Voice-led films: picture events lead the spoken word by 1 to 3 frames. J-cuts (sound starting before its picture) of 0.1 to 0.35 s. Music pad 14 dB under the voice.
7. Silence: a rising tone may hard-cut to silence. A logo may sit in silence.
8. Loudness range example for a voice-led film: −12.2 LUFS integrated (LUFS = the loudness unit platforms normalise to), LRA 1.6 LU (loudness range).

Mix profile for a narrated 55 s film (RMS, the average level):

| Section | Level |
|---|---|
| Narration | −25 dBFS |
| Hero intro | −28 dBFS |
| Product act | −12 dBFS |
| Tunnel | −12 dBFS |
| End lines | −13.5 dBFS |
| Logo | −18.5 dBFS |

Bed ducked −18 dB under speech. Drop on the hero macro.

### 1.9 Texture

1. Grain: midtones only, clumps of 2 to 3 px. Grain on footage; none on pure-digital text cards or end cards.
2. Highlights: 99th-percentile brightness 230 to 237 of 255. No clipping.
3. Blacks: warm and lifted, around `#070705`, not `#000000`.
4. Vignette: corners at 0.64× the centre.
5. Halation (glow bleeding around bright edges): bright edges only.
6. Chromatic fringe (red/blue edge split): glitch frames only, or a constant 1 px edge-clamped fringe.
7. Apply one texture treatment (gate, chroma edges, halation, grain) over every source, so mixed archival sources match.

## 2. Example structure (55.1 s launch film)

Scale times proportionally for other lengths.

| # | Time (s) | Picture | Sound / words |
|---|---|---|---|
| 1 | 0 to 8.5 | Cold open: public-domain archival (for example a 1940s to 1950s training film from the Prelinger Archives) on an old TV frame: rounded screen, 2 px scanlines, inner vignette, per-frame brightness flicker 0.92 to 1.0, push 1.0 to 1.035. Two-frame glitches at segment changes. | Archival voices naming the old version of the problem. Captions on the words. |
| 2 | 8.5 to 12.4 | A real archived web page from the early internet on a CRT-style frame. Camera pushes 1.15 to 2.65× and pans to one line. A cursor glides in (ease-out), lands on it, then hops to others every 0.3 s. | Narrator: the problem has always existed online. |
| 3 | 12.4 to 16.7 | Old web pages from successive eras at 0.35 s each, then a counter ticking every frame to one sourced number, over a collage alternating brightness every frame. | The scale today, as one sourced statistic. |
| 4 | 16.7 to 20.75 | Glitch frame, then a 3D field of hundreds of real crops floating in depth, drifting toward the camera. | The item the viewer needs is in the field. |
| 5 | 20.75 to 22.65 | One real artefact on a white card, push 1.0 to 1.25. An outline and a chip snap on over 4 frames, on the key word. | The film's one coined word. |
| 6 | 22.65 to 26.3 | More archival in the same TV frame as shot 1, 1.2 s per shot. | How long the task was done by hand. |
| 7 | 26.3 to 30.2 | One cut per word of a three-part line; each shot shows its word. | A short three-beat line. This bridge keeps the narrator talking into the next act. |
| 8 | 30.2 to 31.3 | Hero object rises from black, rim light first. | The brand verb, once. |
| 9 | 31.3 to 33.75 | "Before" chart: white axes, a flat white line, a short hook caption. | Quiet bed |
| 10 | 33.75 to 35.0 | Hero macro. The music drop lands on this cut. | Drop |
| 11 | 35.0 to 36.4 | Hero locked at centre on a light backdrop; archival plates change every frame behind it. | Beat |
| 12 | 36.4 to 37.5 | "After": a steep neutral curve passes the flat line on the same axes. | Beat |
| 13 | 37.5 to 39.9 | Proof sequence: a live delta pill, an S-curve with dates, a giant glowing counter flying at the camera, a charged sine. Numbers change every 1 to 2 frames. | Beat |
| 14 | 39.9 to 41.6 | Official marks of every channel covered, 300 px with a white glow, one per 0.28 s, each with its own live counter. | Beat |
| 15 | 41.6 to 44.3 | Big number over the collage, icons counting, a charged line, a giant counter over a black-and-white collage changing every frame. | Beat |
| 16 | 44.3 to 48.4 | The 3D field returns with the platform marks. A one-line claim types in. Hyperspace from 93% of the shot: depth speed ×10, motion blur ramps. | Beat peak |
| 17 | 48.4 to 50.4 | The claim, word by word, on near-black `#0B0B0D`. | Bed thins |
| 18 | 50.4 to 52.4 | "[Product] is live." | |
| 19 | 52.4 to 55.1 | 1-frame cream flash, then mark + wordmark + URL fading in. | Sub hit on the flash; bed fades |

Film-look pass (on the rendered frames): halation 0.16; 1 px red/blue fringe with edge clamping (no wrap-around); fresh grain every frame (generated at half resolution, upscaled bilinear, midtone-weighted); vignette 0.35; 24 fps H.264. Recipe: PIPELINE.md, section 5.

Mix: speech placed on its word timestamps; a licensed music bed with its drop on the hero macro; bed ducked −18 dB under speech; normalise, then a tanh soft-clip (rounds off peaks instead of hard clipping). Recipe: PIPELINE.md, section 6.

## 3. Hard rules

Scope: original brand films (`prompts/LAUNCH_FILM.md`). A remake follows its reference. Format: trigger → action. When a critic's note conflicts with later client feedback, the client feedback wins. Log both in the feedback log.

### 3.1 Content

1. Product screens, chat UIs, job cards, feature tours, per-user quote explainers → cut.
2. Fake UI (post cards without avatars, re-typeset cards, skeleton or grey cards, invented posts, rebuilt HTML copies of real posts) → cut.
3. Generic stock footage (drone city, office desktop, person with phone) → cut. Allowed: public-domain archival, real archived web pages, official platform marks (nominative use), the film's own 3D hero object.
4. Proof from one source when the product spans several channels → show several sources, labelled.
5. Brand shown before the end → move it to the end.
6. Narrator goes silent and the film jumps into a new act → add a bridge line and a scene.
7. Same clip used twice, or three near-identical shots in a row → replace one. Exception: a planned bookend.
8. Lines borrowed from another film → cut. At most one intended homage.

### 3.2 Motion

9. Static hold → fix. A hold fails when nothing moves for more than 1.5 s: mean frame difference at 96×54 below 0.8 (grain floor 0.64) for 36 frames or more. Fix with a push of at least 0.25% per frame, or a cut. Exceptions: the logo hold and one planned held breath.
10. Worm graphs → cut. Allowed: steep exponential or S-curves; a charged sine with amplitude ≥ 25% of chart height, ≤ 2 cycles on screen, a glowing head, and a camera tracking the head.
11. Counters change every frame (giant ones every 2 frames), with a fixed unit label, tabular numerals and global-time continuity across cuts.
12. Glitches or pulses not on a cut → cut. A glitch is 1 to 2 frames, on a cut or act change, with a sound click.
13. Reading time: ≥ 8 frames without glitch or blur for text; ≥ 0.4 s for a number plus a label.
14. Radial streak: 10 to 12 stacked copies at scale 1.0 to 1.8 and opacity 0.5 to 0.05 over 5 frames, then 1 white frame. No Gaussian grey blur, no 3-copy ghosts.
15. Framing: push origins sit on the subject's centre. No card edge, chip or label crosses the frame edge unless planned.

### 3.3 Colour

16. Accent colour anywhere except the hero object → recolour to neutral (warm white `#f4f1ea`, white, silver). Other colours only where colour carries meaning (a green delta chip). Default: none.
17. No purple or indigo. No rainbow gradients.
18. Archival may be black-and-white or sepia. The film as a whole carries colour.

### 3.4 Captions and type

19. ≤ 7 words per caption, one idea per shot. Line breaks set by hand: no single-word last line, no split compound word.
20. One text layer at a time. The same sentence never appears twice on screen (typed in a UI and captioned). No voice-over caption over an on-screen headline.
21. Captions at a fixed position (y 870 to 930 over a bottom gradient), ≥ 20 px clear of any on-screen frame or bezel. Headline cards centred.
22. Keyword emphasis: weight plus a white glow. Never colour.
23. One reveal style per role: voice-over captions grey to white on word timestamps; headlines backwards 1 word per frame; end lines forwards 2 frames per word with a scale settle.

### 3.5 Truth and continuity

24. Every number, date and time on screen agrees with the words and the picture. Failure examples: "overnight" over posts dated years earlier; "2:14 am" over a sunrise; "this week" over a months-old post. Record each real statistic's source. Mark illustrative numbers as illustrative when presenting the film.
25. Anything shown as "found" or highlighted matches the claim. No duplicates.
26. Measure overlays (outlines, highlights, chips) per asset. Store `{x, y, w, h}` per screenshot. Draw outside the object, never through text. Fixed-percentage boxes are not allowed.
27. Rights: public-domain archival (for example Prelinger). Platform logos as nominative use only (naming the platform, not implying endorsement). No synthesised real-person likeness or voice. No fake testimonials.

### 3.6 Sound and encode

28. Loudness:
    - Web master: −14 LUFS integrated, true peak ≤ −1 dBTP.
    - Voice-over 10 to 15 dB over the bed while speaking. 0 to 2.5 dB over the bed buries the voice.
    - Duck the bed −18 dB, 150 ms attack, 400 ms release.
    - Narrator and any second voice level-matched (no +6 dB jump).
29. Sync: the drop on the hero reveal; hits on the action frame; flashes 0 to 1 frame before a kick; clicks on glitch cuts; ticks on counters where the mix allows.
30. Voice: narrator median pitch 85 to 105 Hz. Stock TTS voices often measure 128 to 136 Hz. Pick the lowest available voice and measure it. Mixing does not lower pitch. Read TTS keys from an environment variable and never print them.
31. Encode checks:
    - Channel shifts edge-clamp, not wrap. Wrapping draws coloured lines on the frame edges.
    - Grain is fresh every frame. A 10-frame grain bank repeats every 0.42 s at 24 fps.
    - No double grain (noise textures in the scene plus encode grain).
    - End cards may drop grain.

## 4. Check

### 4.1 Pre-flight

Before building:
- [ ] Read the taste file and feedback log (`TASTE_FILE_TEMPLATE.md`). Restate the client's request in one line. Name the approved version being built on. Do not restart a direction the client approved.
- [ ] Map every beat to a reference frame (film + timestamp). A beat with no reference match is not ready.
- [ ] Beat grid: every cut and flash sits on a music onset or a spoken word (±1 frame). The drop is assigned to the hero reveal.
- [ ] Every number is sourced (written down) or marked illustrative.

Before rendering (stills pass):
- [ ] Stills at every changed beat, on a contact sheet, viewed. One sentence per still describing its content, not "no overlap".
- [ ] Accent colour on the hero object only. No stock. No product UI. No fake cards.
- [ ] Captions: ≤ 7 words, hand-set breaks, one text layer, clear of frames and bezels.
- [ ] Overlays measured per asset. Nothing crosses the frame edge unplanned.

After rendering (measure the MP4 or its frames, not the HTML):
- [ ] Frame-difference scan: list every run where the mean difference at 96×54 stays under 0.8 for ≥ 36 frames. Each run is the logo or a planned breath.
- [ ] Cut rate per section within the targets in section 1.1.
- [ ] A 2 fps contact sheet of the whole film, viewed.
- [ ] Full-resolution frames at every glitch, flash and counter beat, viewed.
- [ ] Audio: peak ≤ −1 dBFS; voice ≥ 10 dB over the bed on every line; drop and hit times checked against cut and action frames; LUFS measured, or written as NOT CHECKED.
- [ ] Encode: no coloured columns at the frame edges, grain not looping, no double grain.
- [ ] The report lists what was checked and what was NOT CHECKED (for example listening on speakers, colour on a calibrated monitor). Deliver one file, named by its content.

Frame-difference scan (numpy + Pillow, no ffmpeg):

```python
import numpy as np, glob
from PIL import Image

FPS = 24                                 # the film's frame rate
fs = sorted(glob.glob('frames/f*.png'))  # the render's frame folder
prev = None; d = []
for f in fs:
    x = np.asarray(Image.open(f).convert('L').resize((96, 54)), np.float32)
    if prev is not None:
        d.append(np.abs(x - prev).mean())
    prev = x
d = np.array(d)
cuts = [(i + 1) / FPS for i, v in enumerate(d)
        if v > 10 and v > 2.5 * np.median(d[max(0, i - 6):i + 7])]
# still holds = runs of d < 0.8 lasting >= 36 frames
```

Loudness:

```bash
ffmpeg -i film.mp4 -af ebur128 -f null -
```

Result: integrated LUFS and true peak, if the ffmpeg build has the `ebur128` filter. Without the filter, write LUFS as NOT CHECKED.

### 4.2 Critic rubric

Run the rubric in a separate critic agent, so the builder does not grade its own work. Critic prompt: `TASTE_FILE_TEMPLATE.md`, section 3.

Inputs: the MP4's 2 fps contact sheet; the frame-difference numbers; full-resolution stills at each beat; contact sheets of the reference films.

Gates. Any failed gate caps the score at 4/10.
- G1: product UI, chat or feature tour.
- G2: fake UI or a re-typeset post.
- G3: stock footage.
- G4: accent colour outside the hero object.
- G5: a number, date or light that contradicts the words.
- G6: an unplanned still hold over 1.5 s.
- G7: a worm line.
- G8: a visible encode artefact (edge lines, looping grain).

Score out of 10 (one point per row, half points allowed):

| # | Dimension | 1 point requires |
|---|---|---|
| 1 | Genre and identity | Essay, then feeling; one idea; one coined word; brand only at the end |
| 2 | Real material | Every frame is real archival, a real page, an official mark or the film's own hero object |
| 3 | Motion | Any two frames 10 apart differ. Pushes ≥ 0.25%/frame on holds. Numbers change every frame. |
| 4 | Rhythm | Section cut rates on target. Dense middle, calm ends. Glitches only at cuts. Every readable element ≥ 8 frames. |
| 5 | Charts and counters | Flat white "before", steep lit "after" on shared axes, glowing heads, global-time counters, U-shaped camera speed with whip-out cuts |
| 6 | Hero object | Rim-first reveal, accent only on the object, real logo legible, locked at centre during the strobe, hit on the bottom-out frame |
| 7 | Type | ≤ 7 words, section 1.6 sizes for headlines, one reveal per role, one text layer, hand-set breaks |
| 8 | Colour and texture | Neutral world plus one accent object, warm lifted blacks, highlights ≤ 235, midtone grain, halation, no grain on end cards |
| 9 | Sound | Drop on the reveal, cuts and flashes on onsets, voice ≥ 10 dB over the bed, narrator 85 to 105 Hz, bed thinning into the end, −14 LUFS |
| 10 | Truth and continuity | Numbers sourced or marked, found items match the claim, no duplicates, no reused clips, time and light agree |

Output format:
- Per beat: KEEP / FIX / CUT; the reference frame it should match (film + time); the defect in plain words; the exact fix (content, motion, timing, px, frames).
- Then: the gates hit; the 5 highest-impact fixes, ranked; the score out of 10; a list of what was NOT CHECKED.
- Scoring anchors:
  - 8 = real-archival cold open with real voices, section 1.9 texture, no fake material.
  - 6 = section 1 targets met, but product UI or truth defects.
  - 4 = empty UI, a template graph, false dates.
  - A version the client approves is the floor for every later version.
