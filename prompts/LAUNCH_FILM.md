> Archived toolkit reference. For portable commands and current policy, read [toolkit adaptations](../references/toolkit-adaptations.md) and SKILL.md.

# Launch film: an original brand film

Purpose: produce a 25 to 60 s brand or launch film built on one idea, from a prompt pasted into Claude Code.
Requires: `../playbook/CRAFT.md` (craft rules and critic rubric), `../playbook/PIPELINE.md` (page to MP4), a taste file and feedback log (`../playbook/TASTE_FILE_TEMPLATE.md`), 2 to 4 reference films.

Two versions:
- Short prompt: a fixed recipe (archival cold open, the scale of the problem, a narrated bridge, a 3D hero object, the brand at the end). Fill the brackets.
- Full prompt: the method behind the recipe, for any genre taken from the reference films.

## Short prompt

```text
<inputs>
Ask me for: a brand name, its logo (SVG or high-res PNG), one line of what it becomes in 5 years (not today's features), one coined word the film should teach (e.g. "[WORD]"), a public-domain archival clip of the old way of doing it (archive.org Prelinger collection), an archived web page from ~2000 that shows the old way (Wayback Machine), a royalty-free song ~100–120 BPM with a real drop (e.g. Mixkit, free for commercial use), and a text-to-speech service with word timestamps for the narrator (premade voices only; the API key lives in an env var and is never printed).
</inputs>

<direction>
A ~55 s brand film. It sells one feeling and one idea, never features. Real archival and real web pages, never stock footage, never product screens, never fake UI. One hero object: a 3D button with the logo embossed into it, the ONLY saturated colour in the film. Everything else white, silver, cream and archival black. Small white captions that light up word by word on the narrator's timestamps. Film texture: fresh grain every frame, halation on bright edges, soft vignette, warm lifted blacks. The brand appears at the end, never before.
Banned: stock footage, dashboards, chat UIs, feature tours, cards without real profile pictures, wobbly "worm" graph lines, random glitches, any hold longer than 1.5 s, purple, rainbow gradients, the accent colour on anything but the hero object.
</direction>

<structure>
Cold open (0–8 s): the archival clip plays on a glowing old CRT TV with its real dialogue, captions word by word.
The past (8–17 s): push into the real ~2000 web page, a cursor lands on one real post, old pages strobe one per frame, a counter ticks EVERY frame up to today's scale. Narrator: "[one line: people have always done X]" / "[one line: today's scale, a sourced number]".
Bridge (17–30 s): a 3D field of real old examples. One snaps to a white outline with a chip of the coined word ("We call that a [WORD]."). Archival of people doing it by hand on the TV. Cut on each word: "[By hand. By hand. By hand.]": three short beats. The narrator never stops talking between acts.
Hero object (30 s): the button rises out of black, rim light first, colourless. "[Brand] [does the one thing]." A flat grey line: "this is how you do it by hand". Hard cut to a button macro, the colour comes alive, the music drop lands on this exact frame. "and this... is with [Brand]": a steep lit curve, counters changing every frame, a glowing sine with a comet head the camera chases, then quick platform/source strikes each with its own counter, then the 3D field again with glowing source marks. Hyperspace.
End: the tagline word by word, then "[Brand] is live.", ONE cream frame on the kick, then logo + URL in silence.
</structure>

<build>
1. One HTML page, 1920x1080 (start from engine/page.html). Everything is computed from the frame number inside seekFrame(F): no CSS transitions, no timers, no Math.random (seeded hash), no state between frames.
2. Hero object: three.js MeshPhysicalMaterial (clearcoat 1, roughness ~0.4), ACES filmic tone mapping, cool + warm rim spots, room environment map. Emboss the real logo by displacing a dense disc with a blurred mask of the logo, folded into the rim so corners don't show. Brushed-metal base.
3. Counters: linear on the film's global clock, so they keep running through cutaways. Tabular numerals, fixed unit label.
4. Captions: ≤7 words, one idea per shot, hand-placed line breaks, one text layer on screen at a time. Grey to white over 0.2 s on the word timestamps from the TTS service.
5. Glitch = 1–2 frames, only on a real cut, always with a click. Readable things stay on screen ≥ 8 frames without glitch or blur.
6. Render with engine/render.mjs (WEBGL=1, which launches Chromium with --use-angle=swiftshader so WebGL renders headless), finish in numpy: fresh grain per frame, halation, vignette ~0.65x at the corners, 1 px chroma fringe with EDGE-CLAMPED shifts. Pipe PNGs into ffmpeg, h264, 24 fps (FPS=24 for engine/encode.py).
7. Mix: narrator 10–15 dB over the music, duck -18 dB while speaking, hits on the exact action frame, -14 LUFS.
</build>

<gotchas>
np.roll wraps pixels and draws coloured lines on the frame edges, so clamp instead. A 10-pattern grain bank loops visibly, generate fresh grain every frame. Measure text only after fonts load or the widths are wrong. Headless Chromium with --disable-gpu renders WebGL blank. Counters that step every 3 frames read as fake. If the narrator goes quiet between acts, the film breaks, so write a bridge line for every act change.
</gotchas>

<start>
Ask me for the inputs, then show me the script with timings (prompts/SCRIPT_TEMPLATE.md) and 6 stills (cold open, past, bridge, hero reveal, macro on the drop, end card) before you render the full film. After every render, send me one 2 fps contact sheet and fix what I flag.
</start>
```

## Full prompt

```text
TASK: make a brand/launch film for [BRAND] that matches REFS on every CRAFT.md measure.
REQUIRED INPUTS (stop and ask if any missing): REFS = 2–4 reference films (mp4 paths or URLs) that define the bar. LOGO = [path, vector or high-res PNG]. IDENTITY = one sentence of the long-term vision (what the brand is in 5 years, not the current feature set). COINED WORD (optional) = the one noun the film teaches the viewer. LENGTH = [25–60 s]. TASTE = the user's standing likes/dislikes, if any (playbook/TASTE_FILE_TEMPLATE.md).
OUTPUT: film.mp4 (1080p, h264+AAC, -14 LUFS, TP ≤ -1 dBTP), SOURCES.md (every asset: URL, licence, in/out), TASTE.md (living critic model), FEEDBACK_LOG.md (every user note verbatim → what changed).

PHASE 0: STUDY REFS (measure, don't describe)
- Download REFS you are allowed to study, extract all frames + audio. Per ref, measure: cuts (per-frame mean-abs-diff spikes) → average shot length, median, cuts/s per section; type sizes (cap height % of frame), caption position, words per caption, reveal method + frames per word; counters (step rate, units, tabular); hero object lighting phases; end-card sequence frame by frame; music BPM, drop time, loudness per section (RMS), where silence is used; texture (grain size/where, black level, highlight p99, vignette ratio, halation).
- Write CRAFT_SPEC.md with numbers + frame refs. Identify the GENRE (archival essay / hero-object product film / kinetic type / etc). The film clones the refs' genre and brand-making mechanics with [BRAND]'s identity, not their content.

PHASE 1: CONCEPT (before any code)
- One idea, one feeling, one hero object/metaphor that carries the brand (the only saturated colour in the film). Brand appears at the END; the body carries the feeling + the coined word.
- Structure template (adapt to refs): cold open that is REAL (public-domain archival, real archived web pages, real sound bites) → the scale of the problem (live counter changing every frame, sourced number) → narrated bridge ("for a hundred years, doing X meant doing it by hand") → hero object reveal (rim light first, music drop on the macro) → the "after" act at the refs' cut density → claim line word by word → "[BRAND] is live." → 1-frame flash on a kick → logo + URL.
- Script (prompts/SCRIPT_TEMPLATE.md): VO lines ≤7 words per caption, narrator bridges EVERY act change (no silent hard jumps). Show the user a storyboard of real key frames (not UI mockups) before building.

PHASE 2: BUILD
- One HTML page (engine/page.html), 1920×1080 stage, seekFrame(F) = pure function of the frame (no timers/random; seeded hash). three.js for the hero object (MeshPhysical, ACES filmic, rim spots, logo displaced into the surface from a blurred mask; WebGL via WEBGL=1, i.e. --use-angle=swiftshader, when headless). HTML/SVG overlays for type, counters, captions.
- Render per frame with engine/render.mjs → finish in numpy/PIL: fresh grain every frame (midtones, none on end cards), halation on bright edges only, vignette ~0.65× corners, edge-CLAMPED 1 px chroma fringe (never np.roll wrap), warm lifted blacks → ffmpeg image2pipe → h264.
- VO: TTS per line with word timestamps; captions reveal on those timestamps (35% grey → white, blur 3→0 px). Music: licensed/royalty-free, drop on the hero macro. VO 10–15 dB over bed, duck -18 dB (150 ms attack / 400 ms release). Hits on the ACTION frame (bottom-out), flashes 0–1 frame before a kick, clicks on glitch cuts, ticks on counters.

HARD RULES
- NO product screens, chat UIs, dashboards, feature tours, "here's what they said" explainers. The film carries a feeling + one idea.
- NO generic stock footage. Public-domain archival and real web captures only.
- NO fake UI (post cards without real profile pictures, re-typeset posts, grey skeleton cards).
- NO static holds >1.5 s (mean frame diff at 96×54 < 0.8 for ≥36 frames) except the logo hold. Every shot moves (push ≥0.25%/frame) or cuts.
- NO worm graphs (low-amplitude high-frequency wobble). Only steep S/exponential curves or a charged sine (amp ≥25% height, ≤2 cycles, glowing head, camera tracks it).
- Counters change every frame (giants every 2), fixed unit label, tabular numerals, continue through cutaways (global clock).
- Glitches: 1–2 frames, only on a real cut, always with a sound click. Never random pulses.
- Readable elements get ≥8 frames without glitch or blur; number+label ≥0.4 s. One text layer at a time. Keyword emphasis = weight + white glow, never colour.
- Only the hero object is saturated. Everything else neutral (white/silver/cream). Not pure B&W overall. No purple/indigo, no rainbow gradients.
- Never show one platform as "the" source if the identity is broader; vary and label sources.
- Every number/date/time must agree with the words and the picture. Sourced stats → SOURCES.md; illustrative numbers flagged as illustrative.
- No real person's likeness or voice synthesised. Logos of other platforms = nominative use only.

PHASE 3: LOOP
- Stills first: render every beat as stills, contact-sheet them, look, fix. Then full render → 2 fps contact sheet of the MP4 → look.
- Critic agent loaded with TASTE.md + CRAFT_SPEC.md, anchored ONLY to REFS: per beat KEEP/FIX/CUT, the ref frame it should match (file + time), what's wrong in plain words, exact fix (px, frames). Apply, re-render, repeat until critic ≥9/10 AND no hard-rule violations.
- Show the user one file per round, named by meaning ("with-bridge", "fixed"), not v12. Every user note → FEEDBACK_LOG.md verbatim + a TASTE.md rule. Never restart a direction the user approved; build on the approved source.
- Budget: first watchable cut within minutes, not hours. Don't run many agents + renders at once on one machine; kill orphan renders.

DELIVER the MP4 + a short list of what is real vs illustrative and any open questions.
```
