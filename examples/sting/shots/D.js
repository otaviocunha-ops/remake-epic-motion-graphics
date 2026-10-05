/* shots/D.js — Builder D: S7 f245–300 (logo disc) + S8 f301–359 (end card).
   All spec numbers are 720-px; multiplied by S (1.5) here. Every value is a continuous function of F. */

// linear interpolation through per-frame samples starting at f0, with linear extrapolation past both ends
function D_samp(F, f0, arr) {
  const i = F - f0, n = arr.length;
  if (i <= 0) return arr[0] + (arr[1] - arr[0]) * i;
  if (i >= n - 1) return arr[n - 1] + (arr[n - 1] - arr[n - 2]) * (i - (n - 1));
  const k = Math.floor(i); return lerp(arr[k], arr[k + 1], i - k);
}
// inline SVG gaussian with independent x/y sigma (continuous values, unlike core's fixed mbx/mby set)
const D_filter = (id, sx, sy) => `<svg width="0" height="0" style="position:absolute"><filter id="${id}" x="-50%" y="-50%" width="200%" height="200%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="${sx.toFixed(2)} ${sy.toFixed(2)}"/></filter></svg>`;

// ---------------- S7 · f245–300 · Frame by Frame disc alone on white ----------------
// disc centre y (720 space) from measure/tables.json S7_disc bbox midpoints f245–f269, then held
const D_S7_CY = [437.5, 414, 402, 394, 388, 383.5, 380, 376, 374, 372, 370, 368, 368, 367, 365.5, 364.5, 364, 363, 362.5, 362.5, 361.5, 361, 361, 360.5, 360.5];
// vertical smear sigma f245–f256 (vertical motion blur on the rise)
const D_S7_BLUR = [2.38, 1.33, 0.92, 0.76, 0.59, 0.51, 0.43, 0.37, 0.24, 0.27, 0.2, 0.0];
// shrink: diameter f287–f300 (spec: 112 hold, 111 f288 … 82 f300; plateaus smoothed ≤0.7 px)
const D_S7_D = [112, 111, 110, 109.3, 108.7, 108, 107, 106, 104.7, 103.3, 101, 98, 92, 82];
const D_S7_SH = [0, 0, 0, 0, 0.18, 0.18, 0.19, 0.2, 0.23, 0.24, 0.27, 0.3, 0.4, 0.7];

SHOT({ id: 'S7', f0: 245, f1: 300, render(lf, F) {
  const cy = (F <= 269 ? D_samp(F, 245, D_S7_CY) : 360) * S;
  const d = (F <= 287 ? 112 : D_samp(F, 287, D_S7_D)) * S;
  const sy = (F <= 256 ? D_samp(F, 245, D_S7_BLUR) : 0) * S;       // vertical smear on the rise
  const sh = (F >= 287 ? Math.max(0, D_samp(F, 287, D_S7_SH)) : 0) * S; // soft blur on the collapse
  const K = 168;                                                      // disc drawn at 168 px (112×1.5), scaled for the shrink
  const sc = d / K;
  const filt = sy > 0.05 ? `filter:url(#D_s7v)` : sh > 0.05 ? `filter:blur(${sh.toFixed(2)}px)` : '';
  // motion trail: full-frame shutter, copies spread over where the disc was one frame earlier (below it)
  // (length read off the ref: long streak on the cut frame, nearly gone two frames later; centred on the position)
  const trail = kf(F, [[245, 24], [246, 9], [247, 4], [249, 0]]);
  const N = trail > 1 ? 10 : 1, disc = ffDisc(K, '#F6F6F6', '#EFEFEF', '#353333');
  let copies = '';
  for (let i = 0; i < N; i++) copies += `<div class="a" style="left:0;top:${N === 1 ? 0 : (trail * (i / (N - 1) - 0.5)).toFixed(2)}px;opacity:${(1 / N).toFixed(3)};mix-blend-mode:plus-lighter">${disc}</div>`;
  return `<div class="a" style="inset:0;background:#FDFDFB"></div>
    ${sy > 0.05 ? D_filter('D_s7v', sy * 0.25, sy) : ''}
    <div class="a" style="left:${540 - K / 2}px;top:${cy - K / 2}px;width:${K}px;height:${K}px;transform:scale(${sc.toFixed(4)});transform-origin:50% 50%;isolation:isolate;${filt}">
      ${copies}
    </div>`;
}});

// ---------------- S8 · f301–359 · black end card, glowing "Frame by Frame" ----------------
// word width (lum>200 bbox, 720 space): f301–303 eye reads, f304–359 measured (tables.json S8_endcard word_w)
const D_S8_W = [1100, 900, 740, 699, 642, 588, 552, 520, 489, 469, 452, 438, 426, 416, 406, 398, 390, 384, 380, 375,
  372, 368, 366, 362, 360, 358, 356, 356, 355, 354, 352, 351, 350, 350, 350, 348, 348, 348, 346, 346, 344, 344, 344, 342,
  340, 338, 336, 334, 332, 328, 325, 321, 314, 306, 300, 288, 270, 243, 178];
// gaussian-equivalent blur (720 space): entry smear, sharp hold, collapse ramp
const D_S8_BLUR = [2.65, 1.13, 0.89, 0.98, 0.64, 0.58, 0.4, 0.29, 0.2, 0.1, 0, 0];
const D_S8_BLUR_OUT = [0, 0, 0, 0.3, 0.58, 0.58, 0.5, 0.7, 0.9, 2.3];   // f350–f359
const D_FS = 80;             // base font px (scale 1 ≈ f320)
const D_W0 = 555;            // lum>200 ink width of the word at scale 1 (calibrated from our own render)

SHOT({ id: 'S8', f0: 301, f1: 359, render(lf, F) {
  const W = D_samp(F, 301, D_S8_W) * S;
  const sc = W / D_W0;
  // zoom smear = how much larger the word was half a frame earlier (180° shutter)
  // entry: zoom-smear keyframes read off the ref (strong radial streaks f301, gone by f306);
  // collapse: half the frame-to-frame size ratio (the ref ghosts on f357–f359)
  const zIn = kf(F, [[301, 0.40], [302, 0.20], [303, 0.08], [304, 0.03], [306, 0]]);
  const zOut = F >= 350 ? 0.5 * Math.max(0, D_samp(F - 1, 301, D_S8_W) / D_samp(F, 301, D_S8_W) - 1) : 0;
  const z = zIn + zOut;
  const sg = (F < 312 ? D_samp(F, 301, D_S8_BLUR) : F >= 350 ? D_samp(F, 350, D_S8_BLUR_OUT) : 0) * S;
  const sx = sg * (F < 312 ? 0.35 : 0.8), sy = sg * (F < 312 ? 0.25 : 0.5);   // the zoom copies carry most of the smear                            // smear is horizontal-first
  const N = z > 0.15 ? 28 : z > 0.01 ? 16 : 1;
  const gk = Math.min(1, 1 / sc);                                   // glow keeps its on-screen size while the word is oversized
  const word = `<div style="font:600 ${D_FS}px/1 Inter;letter-spacing:-0.02em;white-space:nowrap;color:#F3F3F5;
      text-shadow:0 0 ${(4 * gk).toFixed(2)}px rgba(255,255,255,.9),0 0 ${(14 * gk).toFixed(2)}px rgba(255,255,255,.6),0 0 ${(36 * gk).toFixed(2)}px rgba(255,255,255,.38)">Frame by Frame</div>`;
  let copies = '';
  for (let i = 0; i < N; i++) {
    const k = N === 1 ? 1 : 1 + z * i / (N - 1);
    copies += `<div class="a" style="left:0;top:0;width:0;height:0;display:flex;align-items:center;justify-content:center;transform:scale(${(sc * k).toFixed(4)});opacity:${(1 / N).toFixed(3)};mix-blend-mode:plus-lighter">
      <div style="position:absolute;transform:translate(-50%,-50%);left:0;top:${-D_FS * 0.08}px">${word}</div></div>`;
  }
  // broad halo: the word's box blurred very wide (scales with the word)
  const halo = (w, h, blur, a) => `<div class="a" style="left:${-w / 2}px;top:${-h / 2}px;width:${w}px;height:${h}px;border-radius:${h / 2}px;background:rgba(255,255,255,${a});filter:blur(${blur}px)"></div>`;
  return `<div class="a" style="inset:0;background:#020204"></div>
    ${D_filter('D_s8', sx, sy)}
    <div class="a" style="left:540px;top:540px;width:0;height:0;transform:scale(${Math.pow(sc, 0.35).toFixed(4)})">
      ${halo(560, 100, 90, 0.42)}${halo(720, 240, 210, 0.36)}
    </div>
    <div class="a" style="inset:0;isolation:isolate;${sx + sy > 0.1 ? 'filter:url(#D_s8)' : ''}"><div class="a" style="left:540px;top:540px;width:0;height:0">${copies}</div></div>`;
}});
