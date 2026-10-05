> Archived toolkit reference. For portable commands and current policy, read [toolkit adaptations](../references/toolkit-adaptations.md) and SKILL.md.

# Builder brief template

Purpose: give each builder agent a complete contract when a lead agent splits a film across several builders.
Requires: `SPEC.md` for the film; the film folder with `page.html` and `ref/full/`.

The brief defines: the acceptance bar, the one file the builder may edit, the verify loop, and the report format.

## Steps

1. Copy the block below into the film folder as `BRIEF_<G>.md` (G = the shot group letter).
2. Fill every [BRACKET].
3. Give the builder the brief and its sections of `SPEC.md`.

```markdown
# Brief: [FILM NAME], shot group [G] (frames [F0]–[F1]). Read fully before coding.

## THE BAR: SYNC-ALIGNABLE
The finished film will be played side by side with the reference ([ref/src.mp4], [DURATION] s, [FPS] fps, frames 0…[LAST]), both frame-locked.
Same frame number = same pose: every element in the same place, same size, same moment, same easing, same cut frame. Only [what changes: brand, colours, logo, faces, platform UI, words] differ.
- Cut frames EXACT (0 frames off).
- Element positions/sizes within ~1% of the frame.
- Typing reaches the same character count on the same frame (only character-count differences forced by new words are allowed; keep the caret/line end in the same place).
- Cursor on the same path, camera moves on the same frames.
(For an original film with no reference, replace this section with the storyboard frames and the CRAFT.md rules that apply.)

## What changes (apply exactly)
- Text "[OLD NAME]" → "[NEW NAME]" (handles, lowercase logotypes and voice lines likewise).
- Old logo → `mark(px, fill)` (your mark as a mask; coloured versions use BRAND.grad).
- Old accent colours → BRAND tokens, or draw with the ref's colours and let the palette swap convert them (window.PALETTE_SWAP = true).
- [Platform A UI] → [Platform B UI]: keep the SAME window size/position/motion; only chrome, colours and labels change.
- People: [persona names and which avatar file is whose]. Fictional contact details only, never real ones.
- Everything else 1:1.

## Files
- `SPEC.md`: the frame-accurate spec (style tokens, shot table, per-shot detail, components, verbatim text, cursor paths, swap list). Your sections: [§…].
- `ref/full/fNNNN.jpg`: EVERY reference frame (0-based). This is the truth; the spec is a guide. Open them and look.
- `../engine/core.js`: shared engine. DO NOT EDIT. If you need a helper, define it inside your own file, prefixed with your group letter (e.g. `[G]_bubble`). If you need a shared change, ask the lead.
  Provides: BRAND, cl/lerp/inv/E/kf/samples/hash/mixHex, emberStyle/emberLine/gradText, mark(px,fill), tileLight/tileColor/tileChip, avatarByHandle/avatarN, cursor(x,y,size,pressAge,opacity), ripple(), grabHand(), cam(inner,s,tx,ty,{ox,oy,blur,rot,opacity}), edgeFade(), mbx()/mby(), BG(), SHOT({id,f0,f1,render(lf,F)}).
- `page.html`: the stage (1920×1080). Loads `shots/*.js` in order.
- YOUR FILE: `shots/[G].js` ONLY. Wrap it in an IIFE `(() => { … })();`. Register each shot with `SHOT({id:'S07', f0:247, f1:318, render(lf, F){ return '<div class="a" …>…</div>'; }})`.
  render must be a PURE function of the frame: no Date, no timers, no Math.random (use hash()), no CSS transitions. F can be fractional.

## How to verify (mandatory, per shot)
1. Render + side-by-side vs the reference. From the film folder (Chromium must run outside any OS sandbox):
   `OUT=[G] node ../engine/render.mjs compare 247,260,280,300,318`
   → `out/[G]/cmp/sheet.jpg` (LEFT = reference, RIGHT = ours) and per-frame `out/[G]/cmp/fNNNN.jpg`. Open the images and LOOK.
2. Check at least: first frame, last frame, every keyframe the spec gives, and 2 frames into each transition.
3. Measure, don't eyeball: numpy on ref/full for positions, sizes, colours, per-frame tracks.
4. Iterate until each shot reads as the same shot. Max ~15 frames per render call; one render at a time (other builders share the machine: never run a full render, never kill processes you didn't start).
5. Read the `PAGE ERROR` lines in the render output and fix them.

## Report back (final message)
- Table: Shot | frames | status (MATCHES / CLOSE / ROUGH) | what differs from the reference.
- Path to your final compare sheet(s) covering every shot (3 frames per shot).
- Frames that would visibly drift side by side.
- Anything in the spec you found wrong vs the reference frames.
Don't claim MATCHES for a shot you didn't view side by side. Anything not checked is labelled NOT CHECKED.
```

## Rules for the lead

1. Split by contiguous frame ranges, not by component. After integration, render the last 2 and first 2 frames of every seam between groups.
2. Keep one shared definition per component. If two builders each draw the cursor, keep one definition and delete the other.
3. Give each builder its own `OUT=` so stills do not overwrite each other.
4. Frame-level example of a finished spec: `REBUILD_THIS_VIDEO_FULL.md` (the monkey film in `../example-monkey/`).
