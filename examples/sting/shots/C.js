/* shots/C.js — Builder C: S4 f159–186 (lesson page scrolls in), S5 f187–214 (module card sheet),
   S6 f215–244 (two stacked module cards with glass titles).
   Spec numbers are 720-px (SPEC.md / measure/tables.json) and multiplied by S (1.5) here.
   Every value is a continuous function of F (fractional frames interpolate the per-frame samples). */

// samples with linear extrapolation past both ends
function C_samp(F, f0, arr) {
  const i = F - f0, n = arr.length;
  if (i <= 0) return arr[0];
  if (i >= n - 1) return arr[n - 1];
  const k = Math.floor(i); return lerp(arr[k], arr[k + 1], i - k);
}
// inline SVG gaussian with independent x/y sigma (1080-px units)
const C_filter = (id, sx, sy) => `<svg width="0" height="0" style="position:absolute"><filter id="${id}" x="-20%" y="-30%" width="140%" height="160%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="${Math.max(0, sx).toFixed(2)} ${Math.max(0, sy).toFixed(2)}"/></filter></svg>`;
const C_blurStyle = (id, sx, sy) => (sx < 0.3 && sy < 0.3) ? '' : `filter:url(#${id});`;
const C_IMG = ['assets/cover-2.png', 'assets/cover-3.png', 'assets/cover-5.png'];
window.EXTRA_IMGS = (window.EXTRA_IMGS || []).concat(C_IMG);

// ---------------- the lesson page (S4, and the blurred backdrop of S5/S6) ----------------
// Rows are cap-top y in 720 space (ref line tops f180). Inter metrics: ascent .96875, capHeight .727.
const C_FS = 46.5;                       // body size (ref cap 22–23 px ×1.5 / .727)
const C_capOff = fs => fs * (0.96875 - 0.727);   // line-height:normal-free: we set line-height = 1.2109 (content box)
const C_GREY = '#AEAEAC', C_TITLE = '#A2A2A0';
const C_ROWS = [
  // [capTop720, html, extraStyle] — the black key phrase sits on the ref's key-phrase row (cap top 345, x 231)
  [0, 'Frame by Frame'],
  [43, 'Courses &nbsp;›&nbsp; Remake any launch video'],
  [113, '2.1 Choose a reference', `font-weight:600;color:${C_TITLE}`],
  [152, 'Module 2 · Lesson 1'],
  [229, 'Pick one launch video you want to match.'],
  [268, 'Download it, count its frames, and write'],
  [306.5, 'down every cut. The agent'],
  [345, '<span style="letter-spacing:.03em">rebuilds it</span> <b style="font-weight:600;color:#000">frame for frame</b> with your brand,'],
  [384, 'your colours and your words, then checks it'],
  [423, 'side by side against the original.'],
  [501, 'What you need', `font-weight:600;color:${C_TITLE}`],
  [539, '·&nbsp; The launch video you picked'],
  [578, '·&nbsp; Its frame count and every cut'],
  [617, '·&nbsp; Your brand colours, logo and words'],
  [656, '·&nbsp; Claude Code, open in your project'],
  [695, '·&nbsp; This lesson, open next to it'],
];
function C_page(dy720, opts = {}) {
  const lh = C_FS * 1.2109, off = C_capOff(C_FS);
  const rows = C_ROWS.map(([y, h, st]) => {
    const top = (y + dy720) * S - off;
    return `<div class="a" style="left:${80 * S}px;top:${top.toFixed(2)}px;white-space:nowrap;font:400 ${C_FS}px/${lh}px Inter;letter-spacing:-.005em;color:${C_GREY};${st || ''}">${h}</div>`;
  }).join('');
  // soft edge fades like the ref: top (y<60), bottom (y>640) and the right edge where lines run off
  const mv = `linear-gradient(180deg,rgba(0,0,0,.12) 0px,rgba(0,0,0,.55) 45px,#000 ${120}px,#000 ${920}px,rgba(0,0,0,.2) 1080px)`;
  const mh = `linear-gradient(90deg,#000 0,#000 ${990}px,rgba(0,0,0,.15) 1080px)`;
  return `<div class="a" style="inset:0;-webkit-mask-image:${mv};mask-image:${mv}"><div class="a" style="inset:0;-webkit-mask-image:${mh};mask-image:${mh}">${rows}</div></div>`;
}

// ---------------- cursor pointing up (S4) ----------------
// drawn in 720 units pointing straight up, tip at (0,0); angle in degrees (neg = up-left)
function C_cursor(x720, y720, ang, blur = 0) {
  const k = S;
  const path = 'M0 0 L9.2 18.5 L3.1 16.4 L3.1 31.5 L-3.1 31.5 L-3.1 16.4 L-9.2 18.5 Z';
  return `<svg style="position:absolute;left:${x720 * k}px;top:${y720 * k}px;width:1px;height:1px;overflow:visible;z-index:40" viewBox="0 0 1 1">
    <g transform="scale(${k}) rotate(${ang})" style="${blur > 0.3 ? `filter:blur(${blur / k}px)` : ''}">
      <path d="${path}" fill="#000" stroke="#fff" stroke-width="1.4" stroke-linejoin="round" style="filter:drop-shadow(0 .6px .8px rgba(0,0,0,.25))"/></g></svg>`;
}

// ---------------- S4 · f159–186 ----------------
const C_S4_DY = [280, 210, 140, 113, 93, 77, 64, 54, 45, 38, 32, 26, 22, 18, 14, 11, 9, 6, 4, 3, 1, 0, -1, -2, -2.7, -3.3, -3.8, -4.2];
const C_S4_BLUR = [16.02, 9.86, 6.24, 3.74, 2.54, 1.95, 1.5, 1.19, 1.0, .82, .65, .6, .52, .45, .38, .3, .2, .1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
const C_S4_BG = ['#E2F4FE', '#E7F5FE', '#F0F9FC', '#F8F9FD', '#FAFAFC', '#FCFBFC', '#FDFDFB'];
const C_S4_WASH = [.62, .52, .3, .12, .04, 0];     // bg-colour wash over the text on the flash frames
// cursor tip (720) f159–f187; f159–f165 read by eye from the smeared frames, f166–f185 from tables.json
const C_S4_CX = [226, 268, 296, 311, 322, 329, 331, 334, 336, 337, 336, 335, 332, 328, 322, 314, 307, 302, 300, 299, 299, 300, 301, 303, 307, 310, 316, 322, 327];
const C_S4_CY = [612, 590, 566, 546, 526, 512, 501, 490, 482, 475, 468, 462, 457, 451, 444, 435, 424, 415, 407, 401, 397, 394, 392, 390, 388, 387, 387, 386, 386];
const C_S4_CA = [-18, -20, -22, -22, -22, -22, -22, -22, -22, -22, -21, -19, -16, -12, -8, -4, 0, 3, 6, 8, 9, 10, 10, 9, 8, 6, 4, 2, 1];
const C_S4_CB = [5, 2.5, 1.2, .6, .3, 0];            // cursor's own smear on the flash frames (720 px)

function C_bgHex(F) {                               // continuous flash colour f159–f165
  const i = cl(F - 159, 0, 6), k = Math.min(5, Math.floor(i));
  return mixHex(C_S4_BG[k], C_S4_BG[k + 1], i - k);
}

SHOT({ id: 'S4', f0: 159, f1: 186, render(lf, F) {
  const dy = C_samp(F, 159, C_S4_DY), sg = C_samp(F, 159, C_S4_BLUR);
  // vertical streaks while the tilt is fast, isotropic as it settles
  const aniso = cl((sg - 1.5) / 8);                               // 1 at σ≥9.5, 0 at σ≤1.5
  const sy = sg * S * (1 + 0.35 * aniso), sx = sg * S * (1 - 0.6 * aniso);
  const bg = C_bgHex(F), wash = C_samp(F, 159, C_S4_WASH);
  const cx = C_samp(F, 159, C_S4_CX), cy = C_samp(F, 159, C_S4_CY), ca = C_samp(F, 159, C_S4_CA);
  return `<div class="a" style="inset:0;background:${bg}">
    ${C_filter('C_s4', sx, sy)}
    <div class="a" style="inset:0;${C_blurStyle('C_s4', sx, sy)}">${C_page(dy)}</div>
    <div class="a" style="inset:0;background:${bg};opacity:${wash}"></div>
    ${C_cursor(cx, cy, ca, C_samp(F, 159, C_S4_CB) * S)}
  </div>`;
} });

// ---------------- S5 · f187–214 · module card sheet over the blurred lesson ----------------
// photo box (720) per frame: y0 from tables until f204; f205–f214 full box (blur spread removed ≈0.9σ per side)
const C_S5_Y0 = [428, 364, 339, 320, 304, 292, 282, 274, 268, 263, 258, 254, 250, 246, 243, 240, 237, 235];   // f187–f204
const C_S5_BOX = [   // f205–f214 [x0,y0,x1,y1] raw
  [151, 232, 569, 589], [152, 230, 568, 586], [152, 227, 568, 582], [152, 225, 568, 578], [153, 223, 567, 573],
  [154, 220, 566, 567], [155, 218, 564, 559], [158, 214, 564, 549], [161, 208, 560, 536], [162, 198, 559, 513]];
const C_S5_SIG = [1.15, 1.78, 2.51, 2.21, 1.8, 1.34, 1.17, .97, .81, .61, .51, .5, .43, .39, .27, .3, .29, .31, 0, .15, .55, .58, .87, 1.46, 2.1, 2.85, 3.69, 4.9];
const C_S5_BSIG = [.89, 1.06, 1.13, 1.27, 1.34, 1.44, 1.51, 1.59, 1.6, 1.6, 1.64, 1.65, 1.65, 1.66, 1.66, 1.68, 1.68, 1.69, 1.69, 1.73, 1.76, 1.77, 1.85, 2.2, 2.65, 3.38, 4.28, 6.87];
const C_S5_ZOOM = [1.42, 1.28, 1.18, 1.11, 1.07, 1.045, 1.03, 1.02, 1.012, 1.006, 1.002, 1];               // in-photo zoom settle
const C_S5_WHITE = [0, .35, .65, .88, 1];                                                                     // card panel fades in f187–f191

function C_s5box(F) {   // returns [x0,y0,w,h] in 720 px, blur spread removed
  if (F <= 204) { const y0 = C_samp(F, 187, C_S5_Y0); return [151, y0, 418, 357]; }
  const i = cl(F - 205, 0, 9), k = Math.min(8, Math.floor(i)), t = i - k;
  const b = C_S5_BOX[k].map((v, j) => lerp(v, C_S5_BOX[k + 1][j], t));
  const c = 0.9 * Math.max(0, C_samp(F, 187, C_S5_SIG) - 0.4);
  // tie the f204→f205 join: before f205 y0/size come from the rise table
  return [b[0] + c, b[1] + c, b[2] - b[0] - 2 * c, b[3] - b[1] - 2 * c];
}

function C_card(F, x0, y0, w, h, zoom, capAlpha = 1) {
  // everything in 1080 px
  const r = 43 * S, pad = 16 * S;
  const img = `<div class="a" style="left:0;top:0;width:${w}px;height:${h}px;border-radius:${r}px;overflow:hidden;background:#294376">
      <img src="assets/cover-2.png" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:14% 50%;transform:scale(${zoom});transform-origin:45% 50%">
      <div class="a" style="left:${w / 2 - 20 * S}px;top:${18 * S}px;width:${40 * S}px;height:${5 * S}px;border-radius:${2.5 * S}px;background:rgba(230,238,248,.72)"></div>
    </div>`;
  const cap = `<div class="a" style="left:${-60}px;width:${w + 120}px;top:${h + 54 * S - C_capOff(38.25) - 38.25 * 0.1}px;text-align:center;font:600 38.25px/${38.25 * 1.2109}px Inter;letter-spacing:-.01em;color:#000;opacity:${capAlpha}">Remake any launch video</div>
    <div class="a" style="left:${-60}px;width:${w + 120}px;top:${h + 95 * S - C_capOff(23.4)}px;text-align:center;font:400 23.4px/${23.4 * 1.2109}px Inter;color:#969696;opacity:${capAlpha}">Module 2 · 8 lessons</div>`;
  return `<div class="a" style="left:${x0}px;top:${y0}px;width:${w}px;height:${h}px">${img}${cap}</div>`;
}

SHOT({ id: 'S5', f0: 187, f1: 214, render(lf, F) {
  const [bx, by, bw, bh] = C_s5box(F).map(v => v * S);
  const sg = C_samp(F, 187, C_S5_SIG), bsg = C_samp(F, 187, C_S5_BSIG);
  // rise frames: vertical smear; exit frames: isotropic
  const rise = cl((196 - F) / 9), fast = cl((189 - F) / 2);     // fast = first frames of the rise: streaky vertical smear
  const sy = sg * S * (1 + 0.5 * rise + 4 * fast), sx = sg * S * (1 - 0.6 * rise);
  const bs = bsg * S * lerp(0.6, 1.45, cl((F - 187) / 8));   // table σ under-reads the settled backdrop (reads ≈2 px)
  const white = C_samp(F, 187, C_S5_WHITE);
  const zoom = C_samp(F, 187, C_S5_ZOOM);
  const pad = 16 * S;
  // backdrop keeps creeping up like the ref (−4 f186 → ≈ −6 by f214)
  const pdy = -4.2 - 0.07 * (F - 186);
  const cur = F < 188 ? C_cursor(C_samp(F, 159, C_S4_CX), C_samp(F, 159, C_S4_CY), C_samp(F, 159, C_S4_CA)) : '';
  return `<div class="a" style="inset:0;background:#FDFDFB">
    ${C_filter('C_s5b', bs, bs)}${C_filter('C_s5c', sx, sy)}
    <div class="a" style="inset:0;${C_blurStyle('C_s5b', bs, bs)}">${C_page(pdy)}${cur}</div>
    <div class="a" style="inset:0;${C_blurStyle('C_s5c', sx, sy)}">
      <div class="a" style="left:${bx - pad}px;top:${by - pad}px;width:${bw + 2 * pad}px;height:${1080 - by + pad + 200}px;border-radius:${(43 + 16) * S}px;background:#FFFFFF;opacity:${white}"></div>
      ${C_card(F, bx, by, bw, bh, zoom)}
    </div>
  </div>`;
} });

// ---------------- S6 · f215–244 · two module cards with glass titles ----------------
// [y0, w, h] per frame in 720 px (tables.json boxes with the blur spread removed, bottom card smoothed on f216–f217)
const C_S6_TOP = [[184, 371, 277], [167, 361, 255], [157, 360, 245], [148, 361, 241], [142, 362, 238], [138, 362, 236], [133, 362, 234], [130, 361, 234], [128, 361, 232.5], [123.5, 361, 232.5], [121.5, 360.5, 232], [119, 360, 232], [117, 360, 232], [116, 360, 232], [114, 360, 232], [112, 359, 232], [111.5, 359, 231.5], [110, 359, 231], [108, 358.5, 231], [106, 358.5, 231], [105, 358.5, 231], [103.5, 358.5, 231], [101, 358, 231], [99, 358, 231], [96, 358, 231], [91, 358, 231], [86, 358, 231], [80, 358, 231], [71, 358, 231], [55, 358, 231]];
const C_S6_BOT = [[626, 313, 238], [522, 324, 236], [474, 330, 232], [448, 338, 229], [431, 342, 227], [418, 347, 227], [408, 350, 227], [401, 351, 227], [394, 353, 227.5], [387, 355, 228], [382, 356, 229], [378, 357, 230], [375, 357, 230], [372, 358, 230], [369, 358, 230], [368, 358, 230], [365, 358, 230], [364, 358, 230], [362, 358, 230], [360, 358, 230], [358, 358, 230], [357, 358, 230], [354, 358, 230], [352, 358, 230], [348, 358, 230], [344, 358, 230], [339, 358, 230], [332, 358, 230], [322, 358, 230], [305, 358, 230]];
const C_S6_SIG = [7.89, 6.03, 4.67, 3.4, 2.43, 1.73, 1.19, .86, .67, .33, .2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, .36, .4, .51, .65, .81, 1.22];

function C_s6at(F, T) { const i = cl(F - 215, 0, 29), k = Math.min(28, Math.floor(i)), t = i - k; return T[k].map((v, j) => lerp(v, T[k + 1][j], t)); }

// one module card: cover photo, frosted "Module N" pill, frosted "•••", bottom-anchored glass title
function C_modCard(id, src, pill, title, y0, w, h) {
  const X = (360 - w / 2) * S, Y = y0 * S, W = w * S, H = h * S, r = 38 * S;
  const fs = 140, ls = -0.04 * fs;             // title size (1080 px): letters sit under the cover's white card
  const base = H + 0.1 * fs;                    // baseline below the card edge → letters clipped by it, like the ref
  const tx = 11 * S;
  // same placement as the <img> below (object-fit:cover; object-position:30% 50%) so the glass shows what is under it
  const sc = Math.max(W / 1280, H / 720), iw = 1280 * sc, ih = 720 * sc, ix = (W - iw) * 0.3, iy = (H - ih) * 0.5;
  const T = (extra, inner = title) => `<text x="${tx}" y="${base}" font-family="Inter" font-weight="700" font-size="${fs}" letter-spacing="${ls}" ${extra}>${inner}</text>`;
  const svg2 = `<svg class="a" style="left:0;top:0" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
    <defs>
      <clipPath id="${id}c">${T('')}</clipPath>
      <filter id="${id}g" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
        <feGaussianBlur stdDeviation="18" edgeMode="duplicate"/>
        <feComponentTransfer><feFuncR type="linear" slope=".52" intercept=".45"/><feFuncG type="linear" slope=".52" intercept=".46"/><feFuncB type="linear" slope=".5" intercept=".49"/></feComponentTransfer>
      </filter>
      <filter id="${id}s" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="7"/></filter>
      <linearGradient id="${id}l" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".30"/><stop offset=".45" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#0b1e3f" stop-opacity=".10"/></linearGradient>
    </defs>
    <g transform="translate(0 4)">${T('fill="rgba(10,28,60,.28)" filter="url(#' + id + 's)"')}</g>
    <g clip-path="url(#${id}c)">
      <image href="${src}" x="${ix}" y="${iy}" width="${iw}" height="${ih}" preserveAspectRatio="none" filter="url(#${id}g)"/>
      <rect x="0" y="${base - 0.8 * fs}" width="${W}" height="${0.8 * fs}" fill="url(#${id}l)"/>
    </g>
    ${T('fill="none" stroke="rgba(255,255,255,.32)" stroke-width="1.2"')}
  </svg>`;
  const pillW = 81 * S;
  return `<div class="a" style="left:${X}px;top:${Y}px;width:${W}px;height:${H}px;border-radius:${r}px;overflow:hidden;background:#294376;transform:translateZ(0)">
    <img src="${src}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:30% 50%">
    ${svg2}
    <div class="a" style="left:${26 * S}px;top:${16 * S}px;height:${28 * S}px;padding:0 ${15 * S}px;border-radius:${14 * S}px;background:rgba(255,255,255,.26);box-shadow:inset 0 0 0 1px rgba(255,255,255,.28);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);display:flex;align-items:center;font:500 19.5px/1 Inter;color:#F2F7FF;white-space:nowrap">${pill}</div>
    <div class="a" style="left:${W - 39 * S - 13 * S}px;top:${30 * S - 13 * S}px;width:${26 * S}px;height:${26 * S}px;border-radius:50%;background:rgba(255,255,255,.26);box-shadow:inset 0 0 0 1px rgba(255,255,255,.28);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);display:flex;align-items:center;justify-content:center;gap:${2.2 * S}px">
      <i style="width:${3.2 * S}px;height:${3.2 * S}px;border-radius:50%;background:#F2F7FF"></i><i style="width:${3.2 * S}px;height:${3.2 * S}px;border-radius:50%;background:#F2F7FF"></i><i style="width:${3.2 * S}px;height:${3.2 * S}px;border-radius:50%;background:#F2F7FF"></i>
    </div>
  </div>`;
}

SHOT({ id: 'S6', f0: 215, f1: 244, render(lf, F) {
  const [ty, tw, th] = C_s6at(F, C_S6_TOP), [by, bw, bh] = C_s6at(F, C_S6_BOT);
  const sg = C_samp(F, 215, C_S6_SIG);
  const exit = cl((F - 238) / 6);                       // vertical smear on the accelerating exit
  const sy = sg * S * (1 + 2 * exit), sx = sg * S * (1 - 0.6 * exit);
  // the S5 page still dissolving away behind (blurred lesson text + the sheet's white panel)
  const ghost = kf(F, [[215, .75], [218, .35], [222, 0]], E.outQ);
  const gb = (7 + 1.2 * (F - 215)) * S;
  return `<div class="a" style="inset:0;background:#FFFFFF">
    ${C_filter('C_s6g', gb, gb)}${C_filter('C_s6', sx, sy)}
    ${ghost > 0.01 ? `<div class="a" style="inset:0;opacity:${ghost};${C_blurStyle('C_s6g', gb, gb)}">${C_page(-6.2)}<div class="a" style="left:${78 * S}px;top:${72 * S}px;width:${555 * S}px;height:${760 * S}px;border-radius:${70 * S}px;background:#fff"></div></div>` : ''}
    <div class="a" style="inset:0;${C_blurStyle('C_s6', sx, sy)}">
      ${C_modCard('C_b', 'assets/cover-5.png', 'Module 5', 'Sound', by, bw, bh)}
      ${C_modCard('C_t', 'assets/cover-3.png', 'Module 3', 'Launch', ty, tw, th)}
    </div>
  </div>`;
} });
