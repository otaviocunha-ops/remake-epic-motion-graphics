> Archived toolkit reference. For portable commands and current policy, read [toolkit adaptations](../references/toolkit-adaptations.md) and SKILL.md.

# Viral post: a launch film and the post that carries it

Purpose: produce a launch film and a ready-to-post text (hook, tagged prompt, link for the first reply) from one prompt pasted into Claude Code.
Requires: setup from `../README.md`; `../playbook/CRAFT.md`, `../playbook/CRAFT_SPEC_FRAME_LEVEL.md` and `../playbook/PIPELINE.md`; `SCRIPT_TEMPLATE.md` and `BUILDER_BRIEF_TEMPLATE.md` in this folder. Mode B also needs a reference MP4 licensed for use as a reference.

Two modes. The prompt asks which one to run.

| Mode | Makes | Same method as |
|---|---|---|
| A, original film | A 55 s brand film at 24 fps: archival cold open, the scale of the problem, a narrated bridge, a 3D hero object, the brand at the end | `LAUNCH_FILM.md`, short prompt |
| B, remake | A frame-locked remake of a launch video you supply, with your brand, logo, colours, faces and UI | `REMAKE_ANY_VIDEO.md` |

Tagged prompt: a prompt split into sections wrapped in tags such as `<inputs>` and `</inputs>`. The post carries this prompt, so the section order is fixed: inputs, direction, structure, build, gotchas, start.

Rights: remake only videos licensed for use as a reference. Do not reuse the reference's music, voice, footage, logos or people. Do not synthesise a real person's face or voice.

## Prompt

```text
<inputs>
Ask me first: Mode A (original launch film) or Mode B (frame-locked remake of a launch video I supply).
Both modes: brand name [BRAND], logo [path to SVG or high-res PNG], one end-card line [LINE], the URL for the first reply [URL].
Mode A also: one line of what [BRAND] becomes in 5 years (not today's features); one coined word the film teaches [WORD]; a public-domain archival clip of the old way of doing it (archive.org Prelinger collection); an archived web page from about 2000 that shows the old way (Wayback Machine); a royalty-free song at 100-120 BPM with a drop, licensed for commercial use; a text-to-speech service with word timestamps (premade voices only; the API key stays in an env var and is never printed).
Mode B also: the reference video [path/to/reference.mp4]; my colours [hex list] or "derive from logo"; what to swap [e.g. one platform's UI for another's]; profile pictures for any faces [folder].
Stop and ask for anything missing. Record every asset's URL and licence in SOURCES.md.
</inputs>

<direction>
Mode A: a 55 s brand film, 1920x1080, 24 fps. It sells one feeling and one idea, never features. Real archival footage and real archived web pages only. One hero object: a 3D button with the logo embossed into it, the only saturated colour in the film. Everything else white, silver, cream and archival black. Small white captions that light up word by word on the narrator's timestamps. Film texture: fresh grain every frame, halation on bright edges, vignette, warm lifted blacks. [BRAND] appears at the end, never before.
Mode A bans: stock footage, product screens, dashboards, chat UIs, feature tours, post cards without real profile pictures, low-amplitude wobbly graph lines, random glitches, any hold over 1.5 s (36 frames) except the logo hold, purple or indigo, rainbow gradients, the accent colour on anything but the hero object.
Mode B: a frame-locked 1:1 remake. Played side by side with the reference, every frame matches: layout, sizes, positions, timing, easing, camera moves, cuts, blur, cursor path, typing speed. Only brand, logo, colours, faces and the swapped UI change. Acceptance: cuts 0 frames off; positions and sizes within 1% of the frame; typing, cursor and camera on the same frames. Where a swap forces a difference (a shorter brand name), keep everything around it on the reference's positions and list the difference.
Mode B bans: eyeballing, "close enough", random particles where the reference has specific ones, the reference's music or voice.
The post: a hook of 1 or 2 lines that says what the video shows and that it was made from the prompt below; the video; this prompt in tagged sections; the link only in the first reply. No hashtags, emojis, claims about views or sales, link shorteners, or names of people who did not agree to be named.
</direction>

<structure>
Mode A, 55 s:
- Cold open (0-8 s): the archival clip plays on a glowing old CRT TV with its real dialogue, captions word by word.
- The past (8-17 s): push into the real archived web page; a cursor lands on one real post; old pages strobe one per frame; a counter ticks every frame up to today's scale. Narrator: "[one line: people have always done X]" / "[one line: today's scale, a sourced number]".
- Bridge (17-30 s): a 3D field of real old examples. One snaps to a white outline with a chip of the coined word ("We call that a [WORD]."). Archival of people doing it by hand on the TV. Cut on each word of a 3-beat line: "[By hand. By hand. By hand.]". The narrator talks across every act change.
- Hero object (30 s): the button rises out of black, rim light first, colourless. "[BRAND] [does the one thing]." A flat grey line: "this is how you do it by hand". Hard cut to a macro of the button: the colour comes on and the music drop lands on this frame. "and this... is with [BRAND]": a steep lit curve, counters changing every frame, a glowing sine with a bright head the camera chases, then quick source strikes each with its own counter, then the 3D field again with glowing source marks. A hyperspace push.
- End: [LINE] word by word, then "[BRAND] is live.", one cream frame on the kick, then logo + [URL] text in silence.
Mode B:
1. Make a film folder next to example-monkey/ and copy engine/page.html into it as page.html. Extract every frame (0-based, ref/full/fNNNN.jpg) and the audio (ref/audio.wav) with ffmpeg. Find the cuts from frame-difference spikes. Write SPEC.md: every shot with its first and last frame, what is on screen, colours sampled from pixels, font sizes from cap height, cursor tip position per frame, camera keyframes (examples/GOJI_SPEC.md shows the level of detail).
2. Measure with numpy on the reference frames (ink bounding boxes, flood fills, template matching). Store per-frame arrays for every large move. The reference frames are the truth; the spec is a guide.
3. Audio: transcribe the voice-over with word timings; measure music BPM, beat phase, the drop, the silences and every sound-effect hit. Write SCRIPT.md from prompts/SCRIPT_TEMPLATE.md.
4. Split the shots across up to 4 builder agents, each with a brief from prompts/BUILDER_BRIEF_TEMPLATE.md. Each writes only its own shots/<G>.js and compares every shot with the reference frames until it matches.
5. A 5th agent builds the audio: a royalty-free track conformed to the reference BPM with the drop on the same beat, synthesised sound effects on the same hits, the new voice-over on the reference line start times.
6. Run the side-by-side sync check, fix drift, re-render.
Post (both modes): post.txt = hook, a blank line, "Prompt:", then this prompt with its sections in the order inputs, direction, structure, build, gotchas, start, each closed. The first reply = [URL].
</structure>

<build>
1. One HTML page from engine/page.html. Mode A: 1920x1080, window.FPS = 24. Mode B: the reference's resolution and fps. seekFrame(F) draws any frame as a pure function of the frame number: no CSS transitions, no timers, no Math.random (use hash()), no state between frames.
2. Shared helpers come from engine/core.js: easing, kf() keyframes, samples() over measured arrays, cam() camera, motion blur, cursor(), ripple(), word reveals, mark() logo as a mask. Put film-specific helpers in the film folder, not in core.js.
3. Mode A hero object: three.js MeshPhysicalMaterial (clearcoat 1, roughness 0.4), ACES filmic tone mapping, cool and warm rim spots, a room environment map. Emboss the logo by displacing a dense disc with a blurred mask of the logo, folded into the rim. Brushed-metal base.
4. Mode A counters: linear on the film's global frame, so they keep running through cutaways. Tabular numerals, fixed unit label. Change every frame, giant numbers every 2.
5. Mode A captions: 7 words or fewer, one idea per shot, hand-placed line breaks, one text layer on screen at a time. Grey to white over 5 frames on the TTS word timestamps.
6. Glitch = 1 or 2 frames, only on a real cut, always with a click. Readable things stay on screen for 8 frames or more without glitch or blur.
7. Mode B palette: set window.PALETTE_SWAP = true and window.PALETTE_HUE so one filter re-hues every warm colour in the rendered HTML (lightness kept). Photos stay untouched.
8. Render with engine/render.mjs from the film folder, outside the OS sandbox. Mode A sets WEBGL=1 (SwiftShader) so WebGL renders headless. Check stills first: node ../engine/render.mjs frames <list>; Mode B uses node ../engine/render.mjs compare <list>.
9. Mode A finish in numpy (playbook/PIPELINE.md section 5): fresh grain per frame, halation, vignette with corners at 65%, 1 px chroma fringe with edge-clamped shifts. Encode with FPS=24 python3 ../engine/encode.py.
10. Mix: narrator 10-15 dB over the music, music ducked -18 dB under speech, hits on the exact action frame, -14 LUFS integrated, true peak at or below -1 dBTP. Mode B: FPS=<ref fps> python3 ../engine/sync.py for the side-by-side check.
</build>

<gotchas>
np.roll wraps pixels and draws coloured lines on the frame edges: clamp the shift. A 10-pattern grain bank loops visibly: generate fresh grain every frame. Measure text widths only after fonts load, or words collide. Headless Chromium with --disable-gpu renders WebGL blank. Counters that step every 3 frames read as fake. A narrator who goes quiet between acts breaks the film: write a bridge line for every act change. A shorter brand name shifts centred layouts: absorb the difference in the swapped word. Randomised bursts never line up with a reference: drive the visible pieces from measured tracks. Some whips in a reference are crisp: check before adding motion blur. Never mark a shot done without viewing it next to its reference frame.
</gotchas>

<start>
Ask me the mode and the inputs. Mode A: show me the script with timings (prompts/SCRIPT_TEMPLATE.md) and 6 stills (cold open, past, bridge, hero reveal, macro on the drop, end card) before the full render. Mode B: show me the shot table and a side-by-side of 6 frames (open, a typing shot, a camera move, a UI swap, a transition, the end card) before building every shot. After every render, send me one 2 fps contact sheet and fix what I flag. After I approve the final render: write post.txt, search post.txt for local file paths, API keys, tokens and email addresses and remove every hit, print wc -m < post.txt, and run curl -sL -o /dev/null -w '%{http_code} %{num_redirects}\n' [URL]. Mode B also lists every remaining difference from the reference with frame numbers. Do not publish anything; I post it myself.
</start>
```

## Output

| File | Content |
|---|---|
| `film.mp4` | Mode A: 1920x1080, 24 fps, H.264 and AAC. Mode B: the reference's resolution and fps |
| `out/side-by-side.mp4` | Mode B only: reference left, remake right, frame-locked |
| `SOURCES.md` | Every asset with URL and licence |
| `post.txt` | Hook, a blank line, `Prompt:`, the tagged prompt |
| First reply | `[URL]`, checked with curl: `200 0` |
