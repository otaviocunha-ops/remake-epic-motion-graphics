window.FPS = window.FPS || 30;
/* Frame by Frame: shared motion engine.
   Every frame is a pure function of the global frame number F (window.FPS frames per second).
   No timers, no Math.random, no CSS transitions, no state carried between frames.
   Shots register themselves with SHOT({id, f0, f1, render(lf, F)}): lf = F - f0 (local frame, may be fractional).
   render returns an HTML string laid out on the 1920x1080 #stage (absolute positioning).
   Set window.FPS before this file loads to change the frame rate (default 30).
   Set window.LAST_FRAME in the page so `render.mjs full` knows the last frame. */

// ---------- brand tokens (override window.BRAND in your page or first shot file) ----------
window.BRAND = Object.assign({
  name: 'Brand', handle: '@brand',
  deep: '#C8461F', mid: '#E0622C', light: '#F2A36B',
  grad: 'linear-gradient(90deg,#C8461F 0%,#E0622C 55%,#F2A36B 100%)',
  tileGrad: 'linear-gradient(135deg,#F2A36B 0%,#E0622C 100%)',
  chipGrad: 'linear-gradient(180deg,#D84E24 0%,#F2A36B 100%)',
  ember: { hot: '#EE8319', mid1: '#C7620B', mid2: '#4C3115', ink: '#151514' },  // word-reveal colour ramp
  ripple: '#F2A98A', caret: '#E8703A',
  mark: 'assets/mark.png',   // white-on-transparent PNG of your logo mark (used as a mask by mark())
}, window.BRAND || {});

// ---------- math / easing ----------
const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, t) => a + (b - a) * t;
const inv = (a, b, x) => cl((x - a) / (b - a));
const E = {
  lin: t => t,
  inQ: t => t * t, outQ: t => 1 - (1 - t) * (1 - t),
  inC: t => t * t * t, outC: t => 1 - Math.pow(1 - t, 3), ioC: t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2,
  outX: t => t >= 1 ? 1 : 1 - Math.pow(2, -10 * t), inX: t => t <= 0 ? 0 : Math.pow(2, 10 * t - 10),
  ioS: t => t * t * (3 - 2 * t),
  back: (t, s = 1.7) => 1 + (s + 1) * Math.pow(t - 1, 3) + s * Math.pow(t - 1, 2),
};
// keyframes: kf(F, [[f,v],[f,v],...], easeFn): piecewise, easing applied per segment; values may be numbers or arrays
function kf(F, keys, ease = E.lin) {
  if (F <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) {
    const [f0, v0] = keys[i], [f1, v1] = keys[i + 1];
    if (F <= f1) { const t = (ease)((F - f0) / (f1 - f0)); return Array.isArray(v0) ? v0.map((a, j) => lerp(a, v1[j], t)) : lerp(v0, v1, t); }
  }
  return keys[keys.length - 1][1];
}
// linear interpolation through measured per-frame samples (spec tables): samples at consecutive frames from f0
function samples(F, f0, arr) { const i = F - f0; if (i <= 0) return arr[0]; if (i >= arr.length - 1) return arr[arr.length - 1]; const k = Math.floor(i); return lerp(arr[k], arr[k + 1], i - k); }
function hash(i, s = 1) { const x = Math.sin(i * 127.1 + s * 311.7) * 43758.5453; return x - Math.floor(x); }
function mixHex(a, b, t) { const p = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16)); const A = p(a), B = p(b); return '#' + A.map((v, i) => Math.round(lerp(v, B[i], cl(t))).toString(16).padStart(2, '0')).join(''); }

// ---------- ember word reveal (words arrive hot, blur in, cool to ink) ----------
// age = frames since this word's entry. Returns inline style for a word span.
function emberStyle(age, opts = {}) {
  if (age < 0) return 'opacity:0';
  const o = E.outC(cl(age / 4)), blur = 8 * (1 - E.outC(cl(age / 4))), dx = (opts.dx ?? 24) * (1 - E.outC(cl(age / 6)));
  const e = BRAND.ember, c = age < 3 ? mixHex(e.hot, e.mid1, age / 3) : age < 6 ? mixHex(e.mid1, e.mid2, (age - 3) / 3) : mixHex(e.mid2, opts.ink || e.ink, (age - 6) / 4);
  const dy = (opts.dy || 0) * (1 - E.outC(cl(age / 6)));
  return `opacity:${o};filter:blur(${blur}px);transform:translate(${dx}px,${dy}px);color:${c}`;
}
// render a line of words with per-word entry frames: words = [[text, entryFrame, extraStyle?], ...]
function emberLine(lf, words, opts = {}) {
  return words.map(([w, f, st]) => `<span style="display:inline-block;white-space:pre;${emberStyle(lf - f, opts)};${st || ''}">${w}</span>`).join(opts.gap ?? ' ');
}
// brand-gradient text (static)
const gradText = (grad = BRAND.grad) => `background:${grad};-webkit-background-clip:text;background-clip:text;color:transparent`;

// ---------- marks & tiles ----------
const ASSET = 'assets/';
// Your logo mark: a white PNG used as a mask so any fill/gradient can be applied (BRAND.mark)
function mark(px, fill = '#fff', extra = '') {
  const u = BRAND.mark;
  return `<div style="width:${px}px;height:${px}px;background:${fill};-webkit-mask:url(${u}) center/contain no-repeat;mask:url(${u}) center/contain no-repeat;${extra}"></div>`;
}
// app-icon style tiles around the mark
const tileLight = (px) => `<div style="width:${px}px;height:${px}px;border-radius:${px * .225}px;background:linear-gradient(180deg,#fff,#eee);border:1px solid #EDEDED;box-shadow:0 ${px * .045}px ${px * .09}px rgba(0,0,0,.06);display:flex;align-items:center;justify-content:center">${mark(px * .5, BRAND.grad)}</div>`;
const tileColor = (px) => `<div style="width:${px}px;height:${px}px;border-radius:${px * .23}px;background:${BRAND.tileGrad};display:flex;align-items:center;justify-content:center">${mark(px * .5, '#fff')}</div>`;
const tileChip = (px) => `<div style="width:${px}px;height:${px}px;border-radius:${px * .235}px;background:${BRAND.chipGrad};display:flex;align-items:center;justify-content:center">${mark(px * .52, '#fff')}</div>`;

// ---------- avatars ----------
// window.AVATARS = [{handle:'someone', file:'avatars/someone.jpg'}, ...] (files live in assets/avatars/)
const AV = () => window.AVATARS || [];
const avatarByHandle = h => { const a = AV().find(a => a.handle === h) || AV()[0]; return a ? `${ASSET}avatars/${a.file.split('/').pop()}` : ''; };
const avatarN = i => { const L = AV(); if (!L.length) return ''; return `${ASSET}avatars/${L[((i % L.length) + L.length) % L.length].file.split('/').pop()}`; };

// ---------- cursor (press squash) + ripple ----------
// tip at (x,y); size = on-screen height px; pressAge = frames since press (null if none)
function cursor(x, y, size = 96, pressAge = null, opacity = 1) {
  // stem-less navigation arrow, tip up-left (tip = x,y; size = on-screen height)
  let s = 1;
  if (pressAge !== null && pressAge >= 0 && pressAge < 6) s = [0.74, 0.8, 0.9, 1.04, 1.02, 1][Math.floor(pressAge)];
  const k = size / 117;
  return `<svg style="position:absolute;left:${x - 12 * k}px;top:${y - 12 * k}px;width:${160 * k}px;height:${150 * k}px;overflow:visible;opacity:${opacity};transform-origin:${12 * k}px ${12 * k}px;transform:scale(${s});filter:drop-shadow(0 ${6 * k}px ${7 * k}px rgba(0,0,0,.3));z-index:50" viewBox="-12 -12 160 150"><path d="M0 0 L43 117 L70 69 L123 40 Z" fill="#000" stroke="#fff" stroke-width="7" stroke-linejoin="round"/></svg>`;
}
function ripple(x, y, age) {
  if (age < 0 || age > 14) return '';
  const R = [19, 38, 56, 75, 84, 94, 100, 106, 112, 119, 125, 131, 137, 144, 150][Math.floor(age)], o = age < 4 ? .9 : cl(.9 * (1 - (age - 4) / 10));
  return `<div style="position:absolute;left:${x - R}px;top:${y - R}px;width:${2 * R}px;height:${2 * R}px;border-radius:50%;border:14px solid ${BRAND.ripple};opacity:${o};filter:blur(${3 + age * .5}px);box-sizing:border-box"></div>`;
}
// grab hand cursor
const grabHand = (x, y, px = 70) => `<svg style="position:absolute;left:${x}px;top:${y}px;width:${px}px;height:${px}px;z-index:50;filter:drop-shadow(0 4px 6px rgba(0,0,0,.25))" viewBox="0 0 32 32"><path d="M9 14 V9.5 a2 2 0 0 1 4 0 V13 V8 a2 2 0 0 1 4 0 v5 V9 a2 2 0 0 1 4 0 v5 v-2.5 a2 2 0 0 1 4 0 V19 c0 5-3 9-8.5 9 S10 26 8 22 l-3-5 a2 2 0 0 1 3.4-2 Z" fill="#fff" stroke="#000" stroke-width="1.6" stroke-linejoin="round"/></svg>`;

// ---------- camera wrapper ----------
// cam(inner, s, tx, ty, {ox,oy,blur,rot}) scales about (ox,oy) then translates
const cam = (inner, s = 1, tx = 0, ty = 0, o = {}) => `<div class="a" style="inset:0;transform-origin:${o.ox ?? 960}px ${o.oy ?? 540}px;transform:translate(${tx}px,${ty}px) scale(${s}) rotate(${o.rot || 0}deg);${o.blur ? `filter:blur(${o.blur}px);` : ''}${o.opacity !== undefined ? `opacity:${o.opacity};` : ''}">${inner}</div>`;
// edge-fade: wrap content with a horizontal alpha mask (side = 'left'|'right'|'both', width fraction)
const edgeFade = (inner, side = 'right', w = .15) => {
  const g = side === 'left' ? `linear-gradient(90deg,transparent 0,#000 ${w * 100}%)` : side === 'right' ? `linear-gradient(90deg,#000 ${100 - w * 100}%,transparent 100%)` : `linear-gradient(90deg,transparent 0,#000 ${w * 100}%,#000 ${100 - w * 100}%,transparent 100%)`;
  return `<div class="a" style="inset:0;-webkit-mask-image:${g};mask-image:${g}">${inner}</div>`;
};
// directional motion blur approximation: SVG filter id by px
function mblurDefs() { let s = ''; for (const b of [4, 8, 16, 24, 40, 60]) s += `<filter id="mbx${b}" x="-20%" y="0" width="140%" height="100%"><feGaussianBlur stdDeviation="${b} 0"/></filter><filter id="mby${b}" x="0" y="-20%" width="100%" height="140%"><feGaussianBlur stdDeviation="0 ${b}"/></filter>`; return s; }
const mbx = v => { if (v < 2) return ''; const b = [4, 8, 16, 24, 40, 60].reduce((p, c) => Math.abs(c - v) < Math.abs(p - v) ? c : p); return `filter:url(#mbx${b})`; };
const mby = v => { if (v < 2) return ''; const b = [4, 8, 16, 24, 40, 60].reduce((p, c) => Math.abs(c - v) < Math.abs(p - v) ? c : p); return `filter:url(#mby${b})`; };

// ---------- optional palette swap (OFF by default) ----------
// Set window.PALETTE_SWAP = true in your page to re-hue every warm colour (reds/oranges/ambers/peaches/creams)
// in the rendered HTML into one hue family around window.PALETTE_HUE, keeping lightness. Handy when you remake a
// reference whose palette is not yours: build with the ref's colours, then flip one switch.
// Bitmaps (photos) are untouched; greys and non-warm hues are kept.
window.PALETTE_HUE = window.PALETTE_HUE ?? 211;   // centre hue of the target family (211 = calm blue)
(function () {
  const toHsl = (r, g, b) => { r /= 255; g /= 255; b /= 255; const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2; let h = 0, s = 0;
    if (mx !== mn) { const d = mx - mn; s = l > .5 ? d / (2 - mx - mn) : d / (mx + mn); h = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; h *= 60; } return [h, s, l]; };
  const toRgb = (h, s, l) => { h /= 360; if (!s) return [l, l, l].map(v => Math.round(v * 255)); const q = l < .5 ? l * (1 + s) : l + s - l * s, p = 2 * l - q;
    const f = t => { t = (t + 1) % 1; return t < 1 / 6 ? p + (q - p) * 6 * t : t < .5 ? q : t < 2 / 3 ? p + (q - p) * (2 / 3 - t) * 6 : p; }; return [f(h + 1 / 3), f(h), f(h - 1 / 3)].map(v => Math.round(v * 255)); };
  const map = (r, g, b) => { const [h, s, l] = toHsl(r, g, b); const warm = (h <= 62 || h >= 335);
    if (!warm || s < .2 || (l < .12)) return null;                       // greys, near-black warm inks, non-warm hues: keep
    const hh = h >= 335 ? h - 360 : h;                                   // −25…62
    const nh = window.PALETTE_HUE + (hh - 25) * 0.18;                    // tiny spread (~±7°) so gradients keep some life
    return toRgb(nh, Math.min(s, .82) * .92, l); };
  const hex2 = n => n.toString(16).padStart(2, '0');
  window.RECOLOR = html => html
    .replace(/#([0-9a-fA-F]{6})\b/g, (m, x) => { const v = [0, 2, 4].map(i => parseInt(x.slice(i, i + 2), 16)); const o = map(...v); return o ? '#' + o.map(hex2).join('') : m; })
    .replace(/#([0-9a-fA-F]{3})\b(?![0-9a-fA-F])/g, (m, x) => { const v = [...x].map(c => parseInt(c + c, 16)); const o = map(...v); return o ? '#' + o.map(hex2).join('') : m; })
    .replace(/rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(,\s*[\d.]+\s*)?\)/g, (m, r, g, b, a) => { const o = map(+r, +g, +b); return o ? (a ? `rgba(${o.join(',')}${a})` : `rgb(${o.join(',')})`) : m; });
})();



// ---------- shared tile background (the ref's 160 px grid over a soft gradient) ----------
// BG(F, o): o.base = CSS gradient under the grid (warm by default; PALETTE_SWAP re-hues it),
// o.ox/o.oy = grid offset px (the ref's grid shifts per scene), o.tile = tile size (160),
// o.line = grid-line alpha, o.var = max extra white per tile, o.seed = tile pattern seed,
// o.flick = 0..1 how much tiles slowly breathe over time, o.opacity.
function BG(F, o = {}) {
  const T = o.tile || 160, ox = ((o.ox || 0) % T + T) % T, oy = ((o.oy || 0) % T + T) % T, seed = o.seed || 1;
  const base = o.base || 'radial-gradient(120% 90% at 50% 0%,#FFFFFF 0%,#FFF8F4 45%,#FCE3D6 100%)';
  let tiles = '';
  const cols = Math.ceil(1920 / T) + 2, rows = Math.ceil(1080 / T) + 2;
  for (let r = -1; r < rows; r++) for (let c = -1; c < cols; c++) {
    const h = hash(c * 131 + r * 17, seed), br = (o.flick ? 0.5 + 0.5 * Math.sin(F / 60 * (0.6 + h) + h * 40) : 1);
    const a = (h > 0.62 ? (h - 0.62) / 0.38 : 0) * (o.var ?? 0.45) * br;
    if (a > 0.01) tiles += `<div class="a" style="left:${c * T + ox}px;top:${r * T + oy}px;width:${T}px;height:${T}px;background:rgba(255,255,255,${a.toFixed(3)})"></div>`;
  }
  const la = o.line ?? 0.55;
  const grid = `background-image:linear-gradient(90deg,rgba(255,255,255,${la}) 2px,transparent 2px),linear-gradient(0deg,rgba(255,255,255,${la}) 2px,transparent 2px);background-size:${T}px ${T}px;background-position:${ox - 1}px ${oy - 1}px`;
  return `<div class="a" style="inset:0;background:${base};${o.opacity !== undefined ? `opacity:${o.opacity};` : ''}">${tiles}<div class="a" style="inset:0;${grid}"></div>${o.fadeTop ? `<div class="a" style="inset:0;background:linear-gradient(180deg,#fff 0%,rgba(255,255,255,0) ${o.fadeTop}%)"></div>` : ''}</div>`;
}

// ---------- registry + router ----------
window.SHOTS = [];
function SHOT(s) { SHOTS.push(s); SHOTS.sort((a, b) => a.f0 - b.f0); }
window.seek = (t) => {
  const F = Math.round(t * FPS * 1000) / 1000;
  const s = SHOTS.find(s => F >= s.f0 && F <= s.f1 + 0.999) || null;
  const html = s ? s.render(F - s.f0, F) : (window.MISSING ? MISSING(F) : '');
  document.getElementById('stage').innerHTML = (window.PALETTE_SWAP && window.RECOLOR) ? RECOLOR(html) : html;
  return true;
};
window.seekFrame = (F) => window.seek(F / FPS);


