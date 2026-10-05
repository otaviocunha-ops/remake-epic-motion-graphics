> Archived toolkit reference. For portable commands and current policy, read [toolkit adaptations](../references/toolkit-adaptations.md) and SKILL.md.

# Replicate any video: the full method in one prompt

Purpose: replicate a reference video frame for frame with a new brand, from one self-contained prompt that carries every command, measurement table and check.
Requires: the reference MP4, licensed for use as a reference; setup from `../README.md`; `../playbook/CRAFT.md` and `../playbook/PIPELINE.md`; `BUILDER_BRIEF_TEMPLATE.md` and `SCRIPT_TEMPLATE.md` in this folder; `../examples/GOJI_SPEC.md` as the spec format.

Frame-locked: the reference and the replica, played side by side, show the same pose on every frame.

Relation to `REMAKE_ANY_VIDEO.md`: same job. That file has a short prompt and a phase summary. This file is one block with the exact extraction commands, the measurement table formats and the report formats written out. Use it when builders drift, or when the run is split across several sessions.

Rights: replicate only videos licensed for use as a reference. Do not reuse the reference's music, voice, footage, logos or people. The replica copies the choreography only.

## Prompt

```text
TASK: frame-locked 1:1 replica of REF=[path/to/reference.mp4] in a film folder named [FILM] next to example-monkey/.
SWAP ONLY: brand name → [NAME]; logo → [path/to/logo.svg or .png]; palette → [hex list, or "derive from logo"]; platform UI → [e.g. platform A → platform B]; faces and screens → [folder of profile pictures or screenshots]; end-card line → [LINE].
KEEP IDENTICAL: layout, sizes, positions, timing, easing, camera, cuts, blur, cursor path, typing cadence, audio beat grid.
ACCEPTANCE: REF and replica side by side, frame-locked, show the same pose on every frame. Cuts 0 frames off. Position and size error at or below 1% of the frame. Typed character count, cursor and camera on the same frames. Differences are allowed only where a swap forces them (word widths); list each one.
Stop and ask me for any input still in brackets before Phase 0.

SETUP
- Toolkit layout: engine/ holds core.js, page.html, render.mjs, compare.py, sync.py, encode.py. Create the film folder: mkdir -p [FILM]/shots [FILM]/assets [FILM]/audio [FILM]/ref/full [FILM]/measure, then cp engine/page.html [FILM]/page.html, then cd [FILM].
- Run every later command from [FILM]. Chromium does not start inside the OS sandbox: run render commands unsandboxed.

PHASE 0: ANALYSIS (no building)
1. Probe: ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_frames -of csv=p=0 REF. Record width, height, fps, frame count, duration in SPEC.md. Set window.FPS and window.LAST_FRAME in page.html to match.
2. Extract every frame, 0-based: ffmpeg -i REF -fps_mode passthrough -start_number 0 -q:v 2 ref/full/f%04d.jpg (use %05d and PAD=5 if the film has more than 9,999 frames). Count the files; the count must equal the probed frame count.
3. Extract the audio: ffmpeg -i REF -vn -ac 2 -ar 48000 ref/audio.wav.
4. Contact sheets for an overview: ffmpeg -i REF -vf "fps=1,scale=384:-1,tile=6x5" ref/sheet_%02d.jpg.
5. Cuts: in numpy, load each frame as greyscale at 96x54, compute the mean absolute difference to the previous frame, and write measure/cuts.csv with columns frame,diff,cut. Flag a cut where diff is above 5 times the median of the previous 12 frames. Confirm every flagged frame by eye on the frames either side; fix the cut column by hand.
6. Write SPEC.md in the format of examples/GOJI_SPEC.md:
   - Shot table: id, f0, f1, content, transition in, transition out. Shots cover every frame, no gaps.
   - Per-shot detail: positions and sizes in px, camera keyframes, typing frames.
   - Component inventory: every repeated element (cursor, windows, cards, logo), defined once.
   - On-screen text, verbatim, in order.
   - Colour tokens sampled from pixels, with the frame each was sampled on.
   - Font sizes from cap height, weights, tracking.
   - Cursor paths: tip x,y per frame, press frames.
   - A "not pinned" list: every value that is an estimate, not a measurement.
7. Measure, never eyeball. For each large move, write a per-frame table to measure/<shot>_<element>.csv with columns frame,x0,y0,x1,y1,cx,cy,w,h,scale. Methods: ink bounding box (threshold against the background colour), flood fill from a seed pixel, template matching of a crop from the settled frame. scale = measured width / settled width. The reference frames are the truth; the spec prose is a guide.
8. Audio analysis, written to SPEC.md:
   - Narration table: line, start s, end s, words (speech-to-text with word timestamps).
   - Music: BPM and beat phase (onset autocorrelation), drop time, loudness per section, hard-stop time.
   - Sound effects: every hit time from onset and spectral analysis.
   - Voice: pitch and words per minute.
9. If there is narration, write SCRIPT.md from prompts/SCRIPT_TEMPLATE.md. Each new line starts on the reference line's start time.
10. Show me the shot table and a 6-frame compare plan (open, a typing shot, a camera move, a UI swap, a transition, the end card). Wait for my go.

PHASE 1: ENGINE (you, before any builder)
- Stage at REF resolution. window.seekFrame(F) renders frame F as a pure function of F: no timers, no Date, no Math.random (use hash()), no CSS transitions or animations. Shots register SHOT({id, f0, f1, render(lf, F)}) and return HTML. window.ready becomes true only after document.fonts and every image have loaded.
- Use engine/core.js as is: easing E, kf(F, keys, ease), samples(F, f0, arr) for the measure/*.csv arrays, hash, mixHex, cam(), edgeFade(), mbx/mby motion blur, cursor(), ripple(), emberLine() word reveal, BG(), BRAND tokens, mark() logo as a mask, avatar pickers. Put film-specific helpers in shots/_shared.js; keep core.js generic.
- In page.html, replace the inline example shot with script tags for shots/_data.js, shots/_shared.js and shots/A.js to shots/D.js, in that order. Add every image path to window.EXTRA_IMGS so window.ready waits for it.
- Convert each measure/*.csv into a JS array in shots/_data.js (a plain script that sets globals; fetch() fails over file://).
- Cursor: measure the reference cursor glyph and its press-scale curve; draw your own if it differs.
- Palette: set window.PALETTE_SWAP = true and window.PALETTE_HUE so one filter re-hues every warm colour in the rendered HTML, lightness kept. Photos stay untouched. Write your own map in shots/_shared.js if the old brand is not warm.

PHASE 2: PARALLEL BUILD
- Split the shots into up to 4 contiguous groups, A to D. One builder agent per group. Each writes ONLY shots/<G>.js (wrapped in an IIFE, helpers prefixed <G>_) and never edits core.js or _shared.js; it asks you for changes.
- Give each builder BRIEF_<G>.md filled from prompts/BUILDER_BRIEF_TEMPLATE.md, its SPEC.md sections, its measure/*.csv files and the core.js API.
- Verify loop per shot: OUT=<G> node ../engine/render.mjs compare <frames> writes out/<G>/cmp/sheet.jpg (reference left, render right). Check the first and last frame, every keyframe, and 2 frames into each transition. Iterate until within tolerance. At most 15 frames per render call; one render at a time per builder.
- Each builder returns a table: shot | frames | MATCHES / CLOSE / ROUGH | residual difference in px | frames that drift side by side | spec errors found against the reference.
- Builder 5 = audio: a royalty-free track licensed for commercial use (record URL and licence in SOURCES.md), conformed to the REF BPM and cut on beats so the drop, breaks and silences land on REF times; sound effects synthesised in numpy on REF hit times; a mix script with a voice-over slot table (REF start times, new text) that fits each line within 8% stretch, ducks music under voice, and normalises to -14 LUFS integrated, true peak at or below -1 dBTP. example-monkey/audio/ is a working template. Never reuse REF music or voice.

PHASE 3: INTEGRATE
- Unify shared components across groups (cursor, windows, logo): one definition in shots/_shared.js, used by every group.
- Full render: node ../engine/render.mjs full, in 2 or 3 parallel chunks at most (node ../engine/render.mjs full F0 F1). Count frames/: the count must equal the REF frame count.
- Voice-over: generate each line with any TTS, trim silence, place on its slot, re-mix to audio/mix.wav.
- Encode: FPS=<REF fps> python3 ../engine/encode.py [FILM].
- Sync check: FPS=<REF fps> python3 ../engine/sync.py writes out/side-by-side.mp4, reference left, replica right, frame-locked.
- Contact sheets: one reference|replica pair per second, plus the last 2 and first 2 frames at every group seam. Inspect every sheet. Fix drift. Re-render the affected range.
- Scan every frame for leftover old-brand colour: count pixels within the old brand hue band per frame and list frames above 0.1% of the frame.

PITFALLS
- Measure text widths only after fonts load. measureText before load caches fallback widths and words collide. Build width tables lazily.
- A brand name of a different length shifts centred layouts. Keep shared elements on the reference positions, absorb the difference in the swapped word, and report it.
- Randomised bursts and particles never match side by side. Drive the visible ones from measured tracks.
- Some whips in the reference are crisp. Check the reference frames before adding motion blur.
- Headless Chromium must run outside the OS sandbox. Use WEBGL=1 (SwiftShader) if WebGL is involved; never --disable-gpu, which renders WebGL blank.
- A frame folder left over from a longer cut is encoded too. Delete frames/ before a full re-render of a shorter cut.
- Never claim a shot matches without viewing reference|replica side by side for it.

DELIVER: [FILM].mp4 with audio, out/side-by-side.mp4, SPEC.md, measure/, SCRIPT.md (if narrated), SOURCES.md, the source, and a table of every remaining difference from REF: frame range | element | difference in px or frames | cause.
```

## Output

| File | Content |
|---|---|
| `[FILM]/SPEC.md` | Shot table, per-shot detail, components, text, colours, type, cursor paths, audio, not-pinned list |
| `[FILM]/measure/*.csv` | `cuts.csv` and one per-frame table per large move |
| `[FILM]/shots/*.js` | `_shared.js`, `_data.js`, one file per builder group |
| `[FILM]/[FILM].mp4` | The replica with audio |
| `[FILM]/out/side-by-side.mp4` | Reference left, replica right, frame-locked |
| Difference table | Every remaining difference with frame numbers |
