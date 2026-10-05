> Archived toolkit reference. For portable commands and current policy, read [toolkit adaptations](../references/toolkit-adaptations.md) and SKILL.md.

# Remake any video, frame for frame

Purpose: remake a reference video (a launch ad, a product reveal, a social post) with a different brand, logo, colours, faces and words, frame-locked to the original.
Requires: the reference MP4; setup from `../README.md`; `../playbook/CRAFT.md` and `../playbook/PIPELINE.md`; `BUILDER_BRIEF_TEMPLATE.md` and `SCRIPT_TEMPLATE.md` in this folder.

Frame-locked: the original and the remake, played side by side, show the same pose on every frame.

Two versions:
- Short prompt: paste it into Claude Code and answer its questions.
- Full prompt: the same job phase by phase. Use it when the short prompt drifts, or when several agents run in parallel.

Both prompts assume the toolkit layout: the engine in `engine/`, the film in its own folder next to `example-monkey/`.

Rights: remake only videos licensed for use as a reference. Do not reuse the original's music, voice, footage or logos in the output. The remake copies the choreography only.

## Short prompt

```text
<inputs>
Ask me for: the video I want to copy (mp4), my brand name, my logo (SVG or high-res PNG), my colours (or derive them from the logo), what to swap (e.g. one platform's UI for another's), profile pictures for any faces, and one line for the end card.
</inputs>

<direction>
A frame-locked 1:1 remake. Play the original and mine side by side and every frame matches: same layout, sizes, positions, timing, easing, camera moves, cuts, blur, cursor path and typing speed. Only brand, logo, colours, faces and the swapped UI change.
Acceptance: cuts land on the exact same frame, positions and sizes within 1% of the frame, typing, cursor and camera on the same frames. If a swap forces a difference (a shorter brand name), keep everything around it on the original's positions and tell me.
Banned: eyeballing, "close enough", random particles where the original has specific ones, reusing the original's music or voice.
</direction>

<method>
1. Make a film folder next to example-monkey/ (copy engine/page.html in as page.html). Pull every frame (0-based, ref/full/fNNNN.jpg) and the audio (ref/audio.wav) out with ffmpeg. Find the cuts from frame-difference spikes. Write SPEC.md: every shot with its start and end frame, what's on screen, exact colours sampled from pixels, font sizes from cap height, cursor tip position per frame, camera keyframes.
2. Measure everything with numpy on the original frames (ink bounding boxes, flood fills, template matching) and store per-frame arrays for every big move. The original frames are the truth, the spec is a guide.
3. Audio: transcribe the voiceover with word timings, measure the music BPM and beat phase, the drop, the silences and every sound-effect hit.
4. Use the shared engine in engine/core.js, then split the shots across up to 4 agents in parallel. Each one only writes its own shots/<G>.js and checks every shot next to the original frames (node ../engine/render.mjs compare ...) until it matches. Give each agent a brief built from prompts/BUILDER_BRIEF_TEMPLATE.md.
5. A 5th agent does audio: a royalty-free track conformed to the original's BPM with the drop on the same beat, synthesised sound effects on the same hits, and the voiceover placed on the original's word timings.
6. Final check: python3 ../engine/sync.py (original and mine side by side, frame-locked). Fix anything that drifts and re-render.
</method>

<build>
1. One HTML page at the original's resolution. seekFrame(F) draws any frame as a pure function of the frame number: no CSS transitions, no timers, no Math.random, no state between frames.
2. Shared core (engine/core.js): easing, keyframes, interpolation over measured arrays, camera (scale, pan, blur), directional motion blur, a cursor glyph (measure the original's; draw your own if it differs), click ripple, word reveals, logo as a mask so any fill works.
3. Swap colours with ONE filter over the rendered HTML (window.PALETTE_SWAP = true + PALETTE_HUE), so no hard-coded colour in a shot can leak the old brand. Photos stay untouched.
4. Render with engine/render.mjs, encode with engine/encode.py at the original fps, mux the mix.
</build>

<gotchas>
Measure text widths only after fonts load, or words collide. Shorter brand names shift centred layouts, so absorb the difference in the swapped word. Randomised bursts never line up, drive the visible pieces from measured tracks. Some whips in the original are crisp, check before adding motion blur. Never mark a shot done without looking at it next to the original.
</gotchas>

<start>
Ask me for the inputs, then show me the shot table and a side-by-side of 6 frames (open, a typing shot, a camera move, a UI swap, a transition, the end card) before you build the whole film. At the end, list every place mine still differs, with frame numbers.
</start>
```

## Full prompt

```text
TASK: frame-locked 1:1 remake of REF=[path/to/reference.mp4]. Swap ONLY: brand name→[NAME], logo→[path/to/logo.png|svg], palette→[hex list or "derive from logo"], platform UI→[e.g. platform A→platform B], faces/screens→[source]. All else identical: layout, sizes, positions, timing, easing, camera, cuts, blur, cursor path, typing cadence, audio beat grid.
ACCEPTANCE: REF and remake side by side + frame-locked → same pose every frame. Cuts 0 frames off. Position/size error ≤1% of frame. Typing char-count, cursor, camera on the same frames. Differences allowed only where the swap forces them (word widths); report each.

SETUP
- Toolkit layout: engine/ (core.js, page.html, render.mjs, compare.py, sync.py, encode.py). Make films/<name>/ (or a folder next to example-monkey/), copy engine/page.html → page.html, set window.FPS and window.LAST_FRAME.
- All render commands run from the film folder: node ../engine/render.mjs frames|compare|full ...; python3 ../engine/sync.py; python3 ../engine/encode.py <name>.
- Chromium must run outside any OS sandbox (in Claude Code: run that Bash command unsandboxed).

PHASE 0: ANALYSIS (no building yet)
- ffprobe fps/res/duration. Extract ALL frames 0-based to ref/full/fNNNN.jpg (PAD=5 if over 9,999 frames) + audio to ref/audio.wav. 1 fps contact sheets for overview.
- Detect cuts via per-frame mean-abs-diff spikes; confirm visually. Write SPEC.md: shot table (id, f0–f1, content, transition in/out), per-shot detail, component inventory, verbatim on-screen text in order, colour tokens sampled from pixels, font sizes from cap height, cursor paths (tip xy per frame), camera keyframes. See examples/GOJI_SPEC.md for the level of detail.
- MEASURE with numpy on ref frames (ink bounding boxes, flood fills, template match), never eyeball. Store per-frame sample arrays for every major move; the spec's prose is a guide, ref/full is truth.
- Audio: speech-to-text with word timestamps (narration table: line, start, end, text). Music BPM + beat phase (onset autocorrelation), drop time, loudness arc per section, hard-stop time. SFX hit times from onset/spectral analysis. Voice pitch / words per minute.
- If there is narration, write SCRIPT.md from prompts/SCRIPT_TEMPLATE.md: each new line starts on the original line's start time.

PHASE 1: ENGINE (you, before any agents)
- Stage at REF native resolution. window.seekFrame(F) renders frame F as a PURE function of F: no timers, no Date, no Math.random (use hash()), no CSS transitions/animations. Shots register SHOT({id,f0,f1,render(lf,F)}) returning HTML. window.ready=true only after document.fonts loaded + all images decoded.
- engine/core.js already has: easing E, kf(F,keys,ease), samples(F,f0,arr), hash, mixHex, cam(), edgeFade(), mbx/mby motion blur, cursor(), ripple(), emberLine() word reveal, BG() grid background, BRAND tokens, mark() logo-as-mask, avatar pickers. Add film-specific helpers in your page or a shots/_shared.js; keep core.js generic.
- Palette swap: set window.PALETTE_SWAP = true and PALETTE_HUE to re-hue every warm colour in the rendered HTML in one pass (lightness kept), so hard-coded colours in shots can't leak the old brand. Bitmaps untouched. Write your own map() in core.js if your old brand is not warm.

PHASE 2: PARALLEL BUILD
- Split shots into up to 4 contiguous groups; one agent each; each writes ONLY shots/<G>.js (IIFE, helpers prefixed <G>_), never edits core.js (it requests changes from you). Give each a brief from prompts/BUILDER_BRIEF_TEMPLATE.md + its SPEC.md sections + the core.js API.
- Verify loop per shot: OUT=<G> node ../engine/render.mjs compare <frames> → out/<G>/cmp/sheet.jpg. Check first/last frame, every keyframe, 2 frames into each transition; iterate until within tolerance. ≤15 frames per render call; one render at a time per agent.
- Report table: shot | frames | MATCHES/CLOSE/ROUGH | residual diff | frames that would drift side by side | spec errors found vs ref.
- 5th agent = audio: royalty-free, commercial-OK track (record URL + licence), conformed to REF BPM, cut on beats so drop/breaks/silences land on REF times; SFX synthesised in numpy on REF hit times; mix script with a VO slot table (REF start times, text swapped) that fits each line (≤8% stretch), ducks music under voice, loudness-normalises (-14 LUFS, true peak ≤ -1 dBTP). Never reuse REF music or voice. example-monkey/audio/ is a working template.

PHASE 3: INTEGRATE
- Unify shared glyphs/components across groups (cursor, windows, logo): one definition, every group uses it.
- Full render (node ../engine/render.mjs full, 2–3 parallel chunks max), encode with the mix, run python3 ../engine/sync.py, build a 1-per-second ref|ours contact sheet + sheets at every group seam (last 2 / first 2 frames). Inspect. Fix drift. Re-render. Scan all frames for leftover old-brand colour.
- VO: generate per line (any TTS), trim silence, place on slots, re-mix.

PITFALLS
- Measure text widths only AFTER fonts load (measureText before load caches fallback widths → words collide). Lazy-init any width tables.
- Word-length changes from the brand swap shift centred layouts; keep shared elements on ref positions, absorb the delta in the swapped word, report it.
- Randomised bursts/particles won't match side by side; drive the visible ones from measured tracks.
- Ref whips may be crisp (no blur); check before adding motion blur.
- Headless Chromium must run outside any OS sandbox; use --use-angle=swiftshader if WebGL is involved (never --disable-gpu: WebGL renders blank).
- Never claim a shot matches without viewing ref|ours side by side for it.

DELIVER: remake.mp4 (with audio), side-by-side.mp4, SPEC.md, source, and a list of every remaining difference vs REF with frame numbers.
```
