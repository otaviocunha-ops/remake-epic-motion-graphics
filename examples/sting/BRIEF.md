# BRIEF — "Frame by Frame on Whop" remake of the pyramids sting

Goal: a 12 s square sting (1080x1080) that stays **frame-locked** to `ref/src.mp4` (same cut frames, same beats, same camera moves and easing) but where **everything you can see is Frame by Frame living inside the Whop hub UI**. Nobody should be able to call it a copy: new brand, new subject, new UI, new end card. Our hub is real: whop.com/frame-by-frame-1d6c — a $50 Whop course that teaches making launch videos with Claude Code.

Read first, in this order: `BEATS.md` (the frame skeleton), `SPEC.md` (every measured number; 720-px coords → multiply by `S` = 1.5), `measure/tables.json` (per-frame tables), `shots/common.js` (brand + Whop tokens + ffMark/ffTile/ffDisc), `engine/core.js` (kf, samples, E easings, cam, cursor, mblur). Motion rules: every shot enters already moving and leaves on an accelerating move or blur ramp, exactly like the ref.

## Stage / render
- `page.html` = 1080x1080 at reference rate (FPS 30000/1001), frame numbers == reference frames 0–359. Shots register with `SHOT({id,f0,f1,render(lf,F)})`. lf/F may be fractional (the 60p master renders half frames) — every value must be a continuous function of F; no Math.floor on motion.
- Render stills + compare (run from `motion/pyramids`, unsandboxed, with nvm node):
  `export NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh"; nvm use --lts >/dev/null; W=1080 H=1080 REF_DIR=ref/fr OUT=<your letter> node engine/render.mjs compare 10,40,60`
  → `out/<letter>/cmp/sheet.jpg` (LEFT ref, RIGHT ours). Look at the sheet every iteration.
- Write ONLY your own `shots/<letter>.js`. Need something in common.js? Put it in your file with a prefix (e.g. `A_`), and mention it in your report.
- Colours: Frame by Frame blues (common.js FF), white, Whop greys. **No purple, violet, indigo or magenta anywhere** (ref's magenta squares/dots → brand colours). No orange.
- Privacy: never draw a wallet balance, other businesses, real avatars, member counts, or invented stats/reviews.
- Type: Inter (loaded). Use the ref's sizes ×1.5 unless the mapping says otherwise.

## Shot mapping (ref → ours). Keep every frame number, position, size, easing and blur from SPEC.

**Builder A — S1 f0–71 (the hub header + window + cursor + zoom + press)**
- Blue haze open → Frame by Frame sky tones (`#B7CFEB`-ish haze is fine, it's already blue) fading to white.
- Header: ref logo disc → `ffDisc`; "Manus" → **"Frame by Frame"** (Inter 500; it is longer: keep the ref's cap height, let the pill sit after it; if it overflows the window, reduce size to fit with the same left edge); "AI Helper" pill → dark pill **"on Whop"**.
- Window = a light **Whop hub** panel: thin top bar with the search pill "Search Frame by Frame ⌘K"; left sidebar column where the ref has its icons (bolt → Courses icon, chat → Chat icon, faded like the ref); where the ref has the "California Orchid" site card → a **Whop course card** (`assets/cover-2.png` cover, title "Remake any launch video", meta "8 lessons") positioned/cropped exactly where the ref card is.
- Cursor path, turn-to-travel, hover ring (use `FF.ice` ring), grow ×1.55, zoom 1.2× about centre, press f69–71: all from SPEC tables.

**Builder B — S2 f72–100 + S3 f101–158**
- S2: black app icon → `ffTile` (navy); its halo disc/ring as ref; 4 orbit squares → colours `FF.squares` (electric blue, cyan, mint, white with a 1px #E3E8EF edge), same orbit/lock/collapse/blur numbers.
- S3: laptop bezel + menu bar as ref; menu bar icon → small white `ffMark`; the 3 dots → `#2F6BFF`, `#3CC8F0`, `#4ED6A0`; wallpaper → `FF.sky` gradient with the brand's thin white line art (one large circle, two thin horizontal and one vertical line, a 4-point sparkle at a crossing, a soft teal glow top-right) instead of the ref's indigo streaks.
- Glass prompt box: same shape/spring/overshoot; fill = frosted white-blue over the sky (rgba(255,255,255,.18) + backdrop look via a lighter gradient, border highlight); typed text **"Make a launch video for my app"** — the ref's 26 chars arrive f121–f150; ours has 30, so type at the same start/end frames (≈1 char/frame, real keystroke rhythm, first legible f121, complete f150). Send button → `#2F6BFF` disc, white arrow.
- Whip-tilt + light-blue flash `#E6F4FE` as ref.

**Builder C — S4 f159–186 + S5 f187–214 + S6 f215–244**
- S4: the AI answer → a **Whop course lesson page** (light): breadcrumb "Courses › Remake any launch video", title **"2.1 Choose a reference"**, body text in the ref's grey at the ref's size/leading, with one key phrase in black bold at the ref's key-phrase position: body = "Pick one launch video you want to match. Download it, count its frames, and write down every cut. The agent rebuilds it **frame for frame** with your brand, your colours and your words, then checks it side by side against the original." Scroll/settle/blur numbers from SPEC; cursor under the bold phrase like the ref.
- S5: the pyramid photo card → a **module card** sheet: cover image `assets/cover-2.png` in the photo slot (crop to the ref's photo box), caption **"Remake any launch video"** (black), sub-caption **"Module 2 · 8 lessons"** (grey), grabber bar as ref. Answer behind blurs as ref.
- S6: "Khufu"/"Khafre" cards → top card `assets/cover-3.png` with glass title **"Launch"**, bottom card `assets/cover-5.png` with glass title **"Sound"**; "Explore" pill → **"Module 3"** / **"Module 5"**; "•••" stays. Glass-title treatment = a lightened blur of the cover under the letters, like the ref.

**Builder D — S7 f245–300 + S8 f301–359**
- S7: logo disc → `ffDisc` at the ref's size, same rise/hold/shrink.
- S8: black end card, glowing white wordmark **"Frame by Frame"** (Inter 600, tracking −0.02em) — enters huge + horizontally smeared, zooms out, drifts, collapses from f349, exactly the ref's size curve relative to its width (ref word width 452 px at f311 in 720 space → match the *width* curve ×1.5). Glow as ref. Optional tiny line under it from f320: "on Whop" at 30% white — only if it does not break the ref's composition.

## Verify loop (every builder)
1. Build → render compare at your shot's first, middle, last frame + every cut-adjacent frame (e.g. A: 0,15,24,40,59,64,71).
2. Open the sheet image and check: positions match within ~6 px (×1.5 space), timing identical, blur present where ref blurs, nothing clipped, no purple, text legible where ref is legible.
3. Iterate until it matches. Then render 8 evenly spaced frames of your range and look at them as a sequence.
4. Report back (short): frames covered, what matches, what deliberately differs, any number from SPEC you could not hit, and the path of your final compare sheet.
