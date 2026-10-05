> Archived toolkit reference. For portable commands and current policy, read [toolkit adaptations](../references/toolkit-adaptations.md) and SKILL.md.

# PIPELINE: from HTML page to MP4

Purpose: render a film page to frames, add the film finish and the soundtrack, encode the MP4, and verify it.
Requires: setup from `../README.md`; craft rules in `CRAFT.md`; prompts in `../prompts/`; worked example in `../example-monkey/`.

## 0. Overview

```
my-film/page.html + shots/*.js   (a web page that draws any frame on request)
   │   window.seekFrame(F) paints frame F on a 1920×1080 stage
   ▼
engine/render.mjs   (Playwright driving headless Chromium)
   │   for each frame F: seekFrame(F) → screenshot → frames/f0000.png …
   ▼
film finish (optional, Python: numpy + Pillow; not included in encode.py)
   │   halation → 1 px colour fringe → vignette → fresh grain, per frame
   ▼
audio mix (Python)   voice-over + music bed + ducking + SFX → audio/mix.wav
   ▼
engine/encode.py   (ffmpeg: PNG frames → H.264 MP4, muxes audio/mix.wav if present)
   ▼
my-film.mp4
```

## 1. Setup

### 1.1 Node and Playwright
1. Install Node 20+.
2. Install Playwright in the toolkit root (`frame-by-frame/`): `npm i playwright && npx playwright install chromium`. `engine/render.mjs` resolves `playwright` from `engine/` upward, so an install inside a film folder is not found.
3. Import it as `import { chromium } from 'playwright';` in any extra script placed in `engine/`.
4. If `node` is missing in Claude Code's shell but present in a terminal, Node comes from nvm (a Node version manager) and the shell did not load the profile. Prefix commands with:
   ```bash
   export NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh";
   ```

### 1.2 Chromium outside the OS sandbox
- On macOS, Claude Code runs Bash commands inside a sandbox (Seatbelt). Chromium exits there with `bootstrap_check_in … Permission denied`.
- Run every command that launches Chromium (`render.mjs` in any mode) unsandboxed. In Claude Code, approve the unsandboxed run, or instruct it to run the render unsandboxed.

### 1.3 WebGL (3D shots only)
- Headless Chromium has no GPU. For three.js or any WebGL canvas, run with `WEBGL=1`:
  ```bash
  WEBGL=1 node ../engine/render.mjs frames 0,40
  ```
  `WEBGL=1` adds `--use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist` (SwiftShader is Chrome's software GPU).
- Do not add `--disable-gpu`. With it, WebGL draws nothing, every 3D frame is black, and the render still exits without error.
- Create the WebGL renderer with `preserveDrawingBuffer: true`, so the canvas holds the picture when the screenshot is taken.

### 1.4 ffmpeg
- The Python scripts use `ffmpeg` from PATH, or the path in env `FFMPEG`. Check with `ffmpeg -version`.
- Some bundled or static ffmpeg builds are stripped. Run `ffmpeg -filters` once. If `fps`, `select`, `tile`, `tmix` or `drawtext` are missing, or `-f rawvideo` input fails with `Unknown input format`:
  - feed frames as PNG over a pipe: `-f image2pipe -vcodec png -i -` (the engine already does this);
  - change the frame rate with the output option `-r N`, not the `fps` filter;
  - build contact sheets in Pillow, not with `tile`;
  - do frame blending (motion blur, crossfades) in numpy, not with `tmix`.
- Some bundled builds load their libraries relative to their own folder (`Library not loaded: libavdevice.dylib`). `engine/ffmpeg_path.py` runs ffmpeg from its own folder and passes absolute paths. Do the same in any new script (`os.path.abspath`).

### 1.5 Python
- Python 3 with numpy and Pillow. The toolkit scripts need no scipy, opencv, librosa or pydub. Blur and resize come from Pillow; the rest is numpy.
- Read any audio file into numpy: decode to WAV on stdout, then find the `data` chunk. ffmpeg writes a LIST chunk first, so a fixed 44-byte header skip reads the wrong bytes.
  ```python
  raw = subprocess.run([FF, '-v', 'error', '-i', path, '-ac', '2', '-ar', '44100', '-f', 'wav', '-'],
                       capture_output=True, check=True).stdout
  di = raw.find(b'data'); a = np.frombuffer(raw[di + 8:], np.int16).astype(np.float32).reshape(-1, 2) / 32768
  ```

### 1.6 Machine load
- Render time: 0.5 to 1 s per frame at 1080p. The 226-frame example renders in 2 minutes.
- Run one render at a time. Before a new render, stop leftover renders:
  ```bash
  pkill -f render.mjs
  ```

## 2. Film folder

```
my-film/
  page.html          copy of engine/page.html (the stage)
  shots/             one .js file per shot group, loaded in the order listed in page.html
  assets/            every image, SVG, footage frame and font the page uses
  audio/             vo/*.mp3, vo/words.js, music, sfx, mix.wav (the final mix)
  ref/               reference frames to match (optional)
  out/               stills and compare sheets
  frames/            full-render frames
```

Rules:
1. Keep every asset inside the film folder and reference it as `assets/…`. No `../` paths. Copy files in.
2. The page loads over `file://`. `fetch()` fails there, including in `render.mjs`. ES modules load in `render.mjs` (it passes `--allow-file-access-from-files`) but fail when the page is opened in a default browser. Put data (caption timings, crop lists) in a plain `.js` file that sets a global, for example `window.VO = [...]`, loaded before the shots.
3. Store footage as JPG sequences (`assets/v/<clip>_001.jpg …`) at the film's fps and 1920×1080. Record each clip's frame count next to it. Decode with ffmpeg `-r <fps>` and a cover-crop scale. Save with Pillow at quality 90.
4. Record the source and licence of every asset. Use platform logos nominatively (to name the platform). Record the source of public-domain archival film.

## 3. Page contract

`engine/core.js` defines the contract. Every frame is a pure function of the frame number F.

```js
SHOT({ id: 'title', f0: 120, f1: 240, render(lf, F) {   // lf = frame within this shot, F = global frame
  const o = inv(0, 30, lf);                              // 0..1 progress over the first 30 frames
  return `<div class="a" style="inset:0;background:#0B0B0D;opacity:${o}">` +
    `<div class="a" style="left:200px;top:480px;font:600 90px Inter">` +
    emberLine(lf, [['Every', 10], ['frame,', 14], ['on', 18], ['purpose.', 22]], { ink: '#FFFFFF' }) + `</div></div>`;
}});
```

- `window.FPS` sets the frame rate (default 30). `window.seekFrame(F)` draws frame F. `window.seek(t)` draws the frame at t seconds: F = t × FPS, rounded to 0.001 frame. Fractional frames are allowed.
- A shot covers frames `f0` to `f1 + 0.999`. Frames with no shot render `window.MISSING(F)` if the page defines it.
- Helpers in `core.js`:

| Group | Names |
|---|---|
| Math and easing | `cl`, `lerp`, `inv` (clamp, blend, inverse-blend), easing table `E` (`lin`, `inQ`, `outQ`, `inC`, `outC`, `ioC`, `outX`, `inX`, `ioS`, `back`) |
| Keyframes | `kf(F, [[f, v], …], ease)`, `samples(F, f0, arr)` (per-frame measured arrays) |
| Utilities | `hash(i, seed)`, `mixHex(a, b, t)` |
| Camera and blur | `cam(inner, s, tx, ty, {ox, oy, blur, rot, opacity})`, `edgeFade(inner, side, w)`, `mbx(px)` / `mby(px)` (blur ids 4, 8, 16, 24, 40, 60 from `mblurDefs()`) |
| Pointer | `cursor(x, y, size, pressAge, opacity)`, `ripple(x, y, age)`, `grabHand(x, y, px)` |
| Type | `emberLine(lf, [[word, entryFrame], …], opts)`, `emberStyle(age, opts)`, `gradText(grad)` |
| Brand | `BRAND` tokens, `mark(px, fill)` (logo as a mask), `tileLight`, `tileColor`, `tileChip`, `avatarByHandle`, `avatarN` |
| Background | `BG(F, opts)` (grid background) |
| Palette swap | `RECOLOR(html)`, applied only when `window.PALETTE_SWAP = true` |

Determinism rules. Breaking one makes re-renders differ.
1. Redraw everything from F. The shot returns the whole HTML for the frame. No state carried from the previous frame.
2. No timers, no CSS transitions or `@keyframes` animations, no `requestAnimationFrame`. These run on wall-clock time, which the screenshot does not wait for.
3. No `Math.random()`, no `Date`. Use `hash(i, seed)`. For per-frame jitter (flicker, grain, glitch slices), seed with F.
4. Preload every image. `seekFrame` is synchronous and the screenshot follows at once; an undecoded `<img>` paints nothing. `page.html` sets `window.ready` after fonts and the images in its `imgs` list (plus `window.EXTRA_IMGS`) load. `render.mjs` waits up to 90 s for `window.ready`. Add every image a shot creates to that list.
5. Fonts: load with `font-display: block`, or ship font files in `assets/` with `@font-face`. Google Fonts need the network during the render.
6. Grep a name before declaring it at top level. All shot files share one global scope. A second top-level `const cap` throws `Identifier 'cap' has already been declared`, the page stops, `window.ready` never becomes true, and the render fails after the 90 s timeout. Wrap each shot file in an IIFE (`(() => { … })();`) to avoid this.
7. Use tabular numerals (`font-variant-numeric: tabular-nums`, class `.tn` in `page.html`) on counters.

With these rules, frame 900 rendered alone matches frame 900 inside a full render. Stills, partial re-renders and comparisons depend on this.

## 4. Render commands

Run from the film folder, unsandboxed (section 1.2).

1. Render stills of chosen frames.
   ```bash
   PAGE=page.html OUT=v1 node ../engine/render.mjs frames 0,40,80,240,600
   ```
   Result: `out/v1/stills/f0000.png` …
2. Compare against reference frames in `ref/full/`.
   ```bash
   PAGE=page.html OUT=v1 node ../engine/render.mjs compare 0,40,80
   ```
   Result: `out/v1/cmp/sheet.jpg` (LEFT = reference, RIGHT = render) and `out/v1/cmp/fNNNN.jpg`.
3. Render the whole film.
   ```bash
   rm -rf frames && PAGE=page.html LAST=1321 node ../engine/render.mjs full > render.log 2>&1
   ls frames | wc -l
   ```
   Result: the count equals LAST + 1 (here 1322).
4. Re-render one stretch (frames 725 to 900) into the existing folder.
   ```bash
   PAGE=page.html node ../engine/render.mjs full 725 900
   ```

Env vars: `PAGE` (page file), `OUT` (stills sub-folder), `FRAMES` (full-render folder, default `frames`), `LAST` (last frame if the page does not set `window.LAST_FRAME`), `PAD` (zero padding in file names, default 4), `W` / `H` (viewport, default 1920×1080), `WEBGL`, `CHROMIUM_ARGS`, `PYTHON`. Rendering is by frame number and does not depend on FPS. The page's `window.FPS` defines a second.

Rules:
- Check changed beats as stills before any full render.
- Partial re-render: keep the frames folder. Delete it (or its tail) when the new cut is shorter than the old one. `encode.py` encodes every `f*.png` in the folder, including stale frames from a longer cut.

## 5. Film finish

`engine/encode.py` has no film finish. The monkey example is a UI film and uses none. For a cinematic film, add a finish function to a copy of `encode.py` in the film folder, applied to each frame before the pipe to ffmpeg. Apply the steps per frame, on float32 arrays (0..255), in this order:

1. Halation (glow around bright areas): take pixels with luma above 0.72, tint them (1, 0.42, 0.18), blur at quarter resolution with radius 18, scale up, add back at strength 0.16.
2. 1 px chromatic fringe, edge-clamped (red shifted one pixel right, blue one pixel left):
   ```python
   x[:, 1:, 0] = x[:, :-1, 0].copy(); x[:, :-1, 2] = x[:, 1:, 2].copy()
   ```
   Do not use `np.roll`. It wraps the last column onto the first and draws a coloured line down both frame edges.
3. Vignette: multiply by `1 − 0.35·(nx² + ny²)/2`, where nx, ny run −1..1 across the frame (corners end at 65%).
4. Fresh grain every frame: `rng = np.random.default_rng(1000 + i)`; normal noise at half resolution, `×30 + 128` → uint8 → bilinear resize to full size → `−128`; weight by midtones `0.35 + 0.65·4L(1−L)` (L = luma 0..1); scale by 0.55. A repeating grain cycle is visible as a static overlay.

Strength rule: if the finish is identifiable in a single still, reduce it. For UI product films: vignette plus grain at ×0.9, no halation, no fringe.

Encode settings used by `encode.py`: `libx264 -preset slow -crf 16 -pix_fmt yuv420p -movflags +faststart`, input `-f image2pipe -vcodec png -i -`, audio AAC 256 kb/s with `-shortest`. A finish step that writes frames into the pipe PNG-encodes each frame with `compress_level=1`.

```bash
FPS=24 python3 ../engine/encode.py my-film
```

Result: `my-film.mp4` in the film folder. Options: argument NAME (default `film`); env `FPS` (default 30), `FRAMES` (default `frames`), `AUDIO` (default `audio/mix.wav`), `EXPECT` (assert the frame count), `CRF` (default 16), `FFMPEG`. Set `FPS` to the page's `window.FPS`.

## 6. Audio mix

Build the soundtrack as one numpy array at 44.1 kHz stereo float, then write `audio/mix.wav` (16-bit). Helpers: `load(path)` (section 1.5), `place(buf, a, t, gain)` (add clip `a` at t seconds), `faded(a, 0.03)` (30 ms fade in and out; removes clicks at clip edges). `example-monkey/audio/audiolib.py` contains working versions at 48 kHz.

1. Speech bus: place each voice-over line at its start time, faded. Archival voices: gain 1.6.
2. Music bed, aligned to the drop: find the second in the track where the beat drops (listen, or find the energy jump). Choose the film moment it lands on. `start = drop_in_film − drop_in_file`. Place the track at `start` with a 1 s fade-in. For music before `start`, place an earlier copy of the track under the opening and crossfade it out across `start ± 0.5 s`.
3. Ducking (lowering music under speech): envelope = 250 ms moving average of |speech|; music gain 0.126 (−18 dB) where the envelope is above 0.008, else 1; average that gain over a 200 ms window. Mix: `speech + bed × 0.85 × duck`.
4. Music out: fade the bed to zero over 2.2 s, ending before the end card.
5. SFX, generated in numpy:
   - Glitch click: 50 ms noise burst, amplitude 0.25, 12 ms decay, on each glitch frame's time.
   - Hit (final flash or logo): 0.9 s sine sweep 62 → 38 Hz, decay 0.22 s, gain 0.6.
6. Loudness: RMS-normalise to −15 dBFS, then soft-clip with `tanh(mix/0.95)·0.95`. For web platforms, target −14 LUFS integrated, true peak ≤ −1 dBTP. Measure:
   ```bash
   ffmpeg -i audio/mix.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2>&1 | tail -12
   ```
   Result: JSON with `input_i` and `input_tp`. Adjust overall gain until `input_i` is near −14 and `input_tp` is below −1.

Rule: every sound time is also a picture time. Glitch clicks equal the glitch frames; the drop equals its beat; the hit equals the flash. Keep all times in one table at the top of the mix script and in a comment in the page. Change both together.

## 7. Voice-over

### 7.1 Generate a line
Use a text-to-speech (TTS) service whose API returns per-character timestamps with the audio. Word-synced captions need the timestamps.

1. Store the key in an env var or a `.env` file as `TTS_KEY`. Do not print it, put it on a command line, or commit it. Pass it through a header file readable only by the current user, and delete the file after the call:
   ```bash
   K=$(grep '^TTS_KEY=' .env | cut -d= -f2- | tr -d '"'"'"); umask 077
   printf '<auth-header-name>: %s\nContent-Type: application/json\n' "$K" > "$TMPDIR/h.txt"
   curl -sS -X POST "<tts-endpoint-with-timestamps>" -H @"$TMPDIR/h.txt" \
     --data-binary @audio/vo/L01.req.json -o audio/vo/L01.json -w '%{http_code}\n'
   rm "$TMPDIR/h.txt"
   ```
   Replace `<auth-header-name>` and the endpoint with the provider's. Keep the request body in `L01.req.json` so each line can be regenerated.
2. Use curl for the network call. Python's urllib can fail in sandboxed shells where curl works. Inside Claude Code's sandbox, allow the TTS host for that command.
3. Decode the audio from the JSON reply (usually a base64 field) into `L01.mp3`.
4. Starting voice settings: stability 0.55, similarity 0.85, style 0.25, speed 0.95 (names vary by provider).
5. Generate each line standalone. Passing the previous or next line as context leaks 40 to 60 ms of the neighbouring line into the audio.
6. For a line that starts with an "s" sound, prepend a short break (a 0.25 s pause tag) and drop that token from the word list. Without it, the line can start mid-hiss.
7. Audition 5 to 8 stock voices. Free tiers often block community voices (HTTP 402), voice design and voice listing.
8. Measure pitch. Stock male narrators: 128 to 136 Hz median. Documentary register: 85 to 105 Hz. For lower, use a paid voice or a human read.

### 7.2 Word timings to captions
Convert character timestamps to words (a word = characters between spaces; its time = the start of its first character; `dur` = end of the last character):
```python
def entry(id, path):
    al = json.load(open(path))['alignment']; words, cur, st = [], '', None
    for c, s in zip(al['characters'], al['character_start_times_seconds']):
        if c.isspace():
            if cur: words.append([cur, round(st, 3)]); cur = ''
            continue
        if not cur: st = s
        cur += c
    if cur: words.append([cur, round(st, 3)])
    return {'id': id, 'dur': round(al['character_end_times_seconds'][-1], 3), 'words': words}
```
Write all entries into `audio/vo/words.js` as `window.VO = [...]`. Look lines up by id, not by position; position lookups break when a line is inserted.

Caption rules:
- One phrase at a time. Split at punctuation, at 7 words, or by explicit word counts per line.
- Each word appears at its spoken time with a blur-in of 3 px → 0.
- Bottom captions at y 870 to 880 on the 1080 stage, over a dark gradient.
- Emphasis: weight and a glow, not colour.
- Picture cuts keyed to a word land 50 ms before that word.

### 7.3 Swap a line
1. Generate the line, listen, and rebuild its `words.js` entry in place.
2. If its length changed, re-time: the caption offset in the page, any cuts keyed to its words, and its `place()` time in the mix.
3. Render stills at the line's start, middle and end. Then full render, mix, encode.

## 8. Change the film

Re-time a boundary. One time can live in up to six places. Change them together:
1. the shot's `f0` / `f1`, and local progress ranges inside it;
2. every later shot;
3. caption offsets in that stretch;
4. glitch frame lists in the shots and the click list in the mix;
5. the mix: VO `place()` times, the music drop, the music fade-out, the hit;
6. `LAST` (or `window.LAST_FRAME`) for the render.

When time is trimmed by shifting the clock inside a shot, audio-locked items (captions, glitch clicks) keep the unshifted time. Otherwise they drift late.

Add a beat: register a new `SHOT` with its frame range, build it from `lf` / `F` and the helpers only, preload its assets, shift every later shot, then stills → contact sheet → full render → mix → encode → verify.

Colour: write the accent rule in the taste file, for example "the accent colour appears on the hero object only; every 2D accent is warm white". After every edit, grep the page for the accent's hex and rgb forms and confirm each hit is allowed.

Glitches: only on act changes, 1 frame each (2 at most), each with a click. After an FPS change, re-check them: a glitch window sized for 1 frame at 24 fps can catch 0, 1 or 2 frames at another rate.

## 9. Check

Name the tool used to inspect each item and whether it renders the item. Playwright screenshots with SwiftShader render WebGL; a `--disable-gpu` run does not. A file existing does not show its content.

1. Frame count: `ls frames | wc -l` = LAST + 1 = duration × FPS. The encoder's reported duration matches. No leftover frames from a longer cut.
2. Stills of every changed beat, viewed.
3. Reference comparison: `render.mjs compare` (reference left, render right). For motion, `engine/sync.py` builds a side-by-side video with audio:
   ```bash
   python3 ../engine/sync.py
   ```
   Result: `out/side-by-side.mp4`.
4. Contact sheet of the MP4 at 2 fps (a grid of thumbnails of the whole film), viewed beat by beat against the shot list:
   ```python
   raw = subprocess.run([FF, '-v', 'error', '-i', mp4, '-r', '2', '-vf', 'scale=384:216',
                         '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True, check=True).stdout
   sig = b'\x89PNG\r\n\x1a\n'; ims = [Image.open(io.BytesIO(sig + p)).convert('RGB') for p in raw.split(sig)[1:]]
   cols = 10; sheet = Image.new('RGB', (cols * 384, ((len(ims) + cols - 1) // cols) * 216))
   for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * 384, (i // cols) * 216))
   sheet.save('sheet.jpg', quality=85)
   ```
5. Glitch frames: open the exact frames. Each is one full glitch picture with unaffected neighbours. Number test: mean luma jumps (for example from < 40 to > 140) on those frames only. Clicks sit at the same times.
6. Colour rule holds (grep from section 8, plus the contact sheet).
7. Captions vs voice: stills at known word times (line start + word offset) show the word lit as it is spoken.
8. Audio numbers: audio duration = video duration; true peak ≤ −1 dBTP; loudness near −14 LUFS (or RMS near −15.5 dBFS); the drop on its beat; speech above the bed; music gone by the end card.
   ```python
   a = subprocess.run([FF, '-v', 'error', '-i', mp4, '-vn', '-ac', '2', '-ar', '44100', '-f', 'wav', '-'],
                      capture_output=True, check=True).stdout
   x = np.frombuffer(a[a.find(b'data') + 8:], np.int16).astype(np.float32) / 32768
   print('s', len(x) / 2 / 44100, 'peak dBFS', 20 * np.log10(np.abs(x).max()), 'rms dBFS', 20 * np.log10(np.sqrt((x ** 2).mean())))
   ```
9. Edges: zoom on the left and right columns of a bright frame. No 1 px coloured line (the `np.roll` fringe defect).
10. Frame diffs after a "no visual change" edit: render the same frames before and after and diff them in numpy (`np.abs(a − b).max()`). Any value above 0 means the edit changed the picture.
11. End: the last frame is the end card, not black and not cut off.
12. Deliver one file, named by its content (`launch-film-with-voiceover.mp4`), not a version number.
13. When presenting the film, label on-screen numbers that are illustrative.

## 10. Problems

| Symptom | Cause | Fix |
|---|---|---|
| Chromium does not launch: `bootstrap_check_in … Permission denied` | The macOS sandbox blocks a port Chromium needs | Run the render unsandboxed |
| Render waits 90 s, then times out | A script error stopped the page, so `window.ready` never became true (often a duplicate top-level name) | Read the `PAGE ERROR` lines in the render output; grep names before declaring them |
| 3D frames all black | `--disable-gpu`, or no `preserveDrawingBuffer` | `WEBGL=1` (section 1.3); `preserveDrawingBuffer: true` |
| An image missing on the first frames it appears | Not preloaded; the screenshot came before it decoded | Add it to the preload list |
| Images blank or 404 | Path outside the film folder (`../…`), or data loaded with `fetch()` over `file://` | Copy assets into `assets/`; load data as a `.js` global |
| Frame N differs alone vs inside the full render | State carried between frames, `Math.random()`, `Date`, a CSS transition or a timer | Derive everything from F; use `hash()` |
| Old shots at the end, or the film is too long | Frames folder not cleared after a shorter re-render | `rm -rf frames` before a full render; check the count |
| MP4 plays at the wrong speed | `encode.py` default `FPS=30` differs from the page's `window.FPS` | Set `FPS=` on the encode command |
| Thin coloured line down the frame edges | Colour fringe done with `np.roll` | Edge-clamped slice copies (section 5) |
| Captions and clicks drift late after a trim | Picture clock shifted; audio-locked items used the shifted time | Captions and clicks use the unshifted time |
| `Unknown input format: 'rawvideo'`, missing `fps` / `tile` / `tmix` | Stripped ffmpeg build | PNG over image2pipe; `-r`; Pillow sheets; numpy blends |
| `Library not loaded: libavdevice.dylib` | Bundled ffmpeg looks for its libraries relative to the working directory | Run it from its own folder with absolute paths, or set `FFMPEG` to a standard ffmpeg |
| Audio load gives noise or a click at the start | Fixed 44-byte WAV header skip | Find the `data` chunk (section 1.5) |
| VO line starts mid-"s" or contains part of the next line | TTS behaviour | Leading break tag; generate lines standalone |
| Glitches not aligned to cuts | Placed on a timer | Glitch only on act changes, with a click |
| 3D field of posts reads as invented | Invented cards with fake names and stats | Use captured real material (section 11, `CRAFT.md` 3.1) |
| Machine stalls | Several renders and agents at once | One render at a time; `pkill -f render.mjs` |

## 11. Capture real material

- Archived web pages: screenshot `web.archive.org` URLs with Playwright at a fixed viewport. Add `if_` after the timestamp in the URL (`/web/20000816005701if_/http://…`) to hide the Wayback toolbar.
- Single posts as crops: load the page at `deviceScaleFactor: 2`, select one element per post (a row, a paragraph), keep elements with real text and a height that fits the layout, and save each as its own PNG. Record each crop's aspect ratio.
- Archival footage: decode to a JPG sequence at the film's fps (section 2). Cut its original audio to separate WAVs to use the real voices.
