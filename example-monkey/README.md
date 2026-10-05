# Example: the monkey film

Purpose: render a complete 7.5 s film and use its files as a template.
Requires: setup from the main `README.md` (Node 20+, Playwright + Chromium in `frame-by-frame/`, Python 3 + numpy + Pillow, ffmpeg).
Time: 2 minutes for the frame render (226 frames at 0.5 s per frame).

Format: 1920×1080, 30 fps, 226 frames (f0 to f225), one shot in code. Content:

1. A prompt types into a white box over a blue-graded sky with a leaping baby goat.
2. Hard cut to a giant send button. The cursor presses it.
3. The box turns to glass and morphs into a landing page for "Monke" (a grinning macaque in sport sunglasses).
4. The page pulls back to a card on light grey. f225 is black.

The film is a frame-for-frame remake of a reference ad. Positions, sizes and timings were measured from the reference with numpy and are stored in `shots/L.js`. The reference video is not included.

## Steps

Run every command from `example-monkey/`. On macOS inside Claude Code, run steps 1 and 2 unsandboxed: Chromium does not start inside the sandbox.

1. Render three stills.
   ```bash
   node ../engine/render.mjs frames 0,80,140
   ```
   Result: `out/stills/f0000.png`, `f0080.png`, `f0140.png`.
2. Render every frame.
   ```bash
   node ../engine/render.mjs full
   ```
   Result: `frames/f0000.png` to `frames/f0225.png`.
3. Build the soundtrack (optional).
   ```bash
   cd audio && python3 mix.py && cd ..
   ```
   Result: `audio/mix.wav` and `audio/mix_report.json`. The first run downloads the Mixkit track and synthesises every sound effect.
4. Encode the MP4.
   ```bash
   python3 ../engine/encode.py monkey
   ```
   Result: `monkey.mp4` (H.264 + AAC). Without `audio/mix.wav`, the MP4 is silent.

## Check

- f0: empty white prompt box, black send button, "Frame 1.0" label, goat on the right.
- f80: giant send button under the cursor.
- f140: Monke landing page, headline typing.
- `ls frames | wc -l` prints 226.

## Edit points

| Element | Location |
|---|---|
| Model label, "Made with …" pill, the three wordmarks | Uncomment `window.FILM_TEXT` in `page.html` |
| Prompt text, headline, paragraph, CTA, feature rows | `L_PROMPT` near the top of `shots/L.js`, and the landing-page section (search for `Monke`) |
| Background photo / hero photo | Replace `assets/goat_bg.jpg` (2560×1440) / `assets/monkey.jpg` (2912×4030). The cut-out masks in `L.js` are traced for these photos. A new subject needs a new mask polygon; ask Claude Code to trace it. |
| Timing, camera, easing | Keyframe tables in `shots/L.js` (`kf(F, [[frame, value], …], ease)`) |
| Frame rate / length | `window.FPS` and `window.LAST_FRAME` in `page.html` |

To change the film through Claude Code, open it in this folder, give it `../prompts/REBUILD_THIS_VIDEO_FULL.md` as the spec, and state the change:

```text
Change the landing page to a coffee brand called [BRAND]. Keep every timing. Show me frames 20, 82, 125, 200 before rendering everything.
```

## Files

```
page.html          stage: loads ../engine/core.js, then shots/L.js; sets FPS, LAST_FRAME, FILM_TEXT
shots/L.js         the film: one shot, 226 frames, a pure function of the frame number
assets/            goat_bg.jpg (baby goat, CC0 / public domain), monkey.jpg (macaque self-portrait, public domain)
audio/
  mix.py           final mix: music + SFX, -14 LUFS, true peak ≤ -1 dBTP  ->  mix.wav, mix_report.json
  build_music.py   downloads Mixkit "Voxscape" and conforms it to the film (two cuts, filter sweeps)  ->  music.wav
  sfx.py           synthesises every sound effect in numpy (fixed seeds)  ->  sfx/*.wav
  audiolib.py      shared audio helpers (wav I/O, ffmpeg, loudness, limiter)
  cue_gains.json   calibrated level of every sound effect (saved from a run against the reference)
  analysis.json    measurements of the reference soundtrack (hit times, loudness, bass notes)
  analyze.py, verify_mix.py, verify_music.py
                   measurement tools; they need the reference soundtrack at example-monkey/ref/audio.wav
                   (not included). Use them as templates for a remake.
```

## Credits and licences

- Baby goat photo: Wikimedia Commons, "Baby goat jumping", public domain / CC0. Mirrored and cropped.
- Macaque photo: Wikimedia Commons, "Macaca nigra self-portrait", public domain.
- Music: "Voxscape" by Eugenio Mininni, Mixkit Stock Music Free License (https://mixkit.co/license/#musicFree). Not included. `build_music.py` downloads it from `https://assets.mixkit.co/music/571/571.mp3` on the first run.
- Fonts: Inter and Poppins from Google Fonts (SIL Open Font License), loaded at render time. Rendering needs an internet connection.
- The on-screen brand "Monke" and all copy are fictional.

## Problems

| Symptom | Cause | Fix |
|---|---|---|
| Browser launch error on macOS inside Claude Code | Chromium does not start inside the sandbox | Run the render unsandboxed |
| `mix.py` fails on the first run | No network access to `assets.mixkit.co` for the music download | Allow the host, or skip step 3 for a silent MP4 |
| `analyze.py` or `verify_*.py` fails | `ref/audio.wav` is not included | Use these scripts only on a remake that has its own `ref/audio.wav` |
