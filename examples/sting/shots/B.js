/* shots/B.js — Builder B: S2 (f72–100) app tile + orbit squares, S3 (f101–158) menu bar → glass prompt → whip-tilt.
   Authored in the ref's 720-px space inside one wrapper scaled by 1.5 (so every spec number is used as-is).
   Every value is a continuous function of F (tables interpolate linearly, extrapolate past the last sample). */
(function () {
  const B_PAGE = '#FDFDFB';
  // sampler over per-frame arrays starting at f0; linear between samples, linear extrapolation past the ends
  const B_s = (F, f0, arr, ext = true) => {
    const n = arr.length, i = F - f0;
    if (i <= 0) return arr[0];
    if (i >= n - 1) { if (!ext) return arr[n - 1]; const d = arr[n - 1] - arr[n - 2]; return arr[n - 1] + d * (i - (n - 1)); }
    const k = Math.floor(i); return lerp(arr[k], arr[k + 1], i - k);
  };
  const B_col = (tbl, j) => tbl.map(r => r[j]);
  const B_wrap = (inner, extra = '') => `<div class="a" style="left:0;top:0;width:720px;height:720px;transform-origin:0 0;transform:scale(1.5);${extra}">${inner}</div>`;
  let B_fid = 0;
  // SVG gaussian filter with independent x/y sigma (720-space), returns [defs, css]
  const B_blur = (sx, sy, pad = 30) => {
    sx = Math.max(0, sx); sy = Math.max(0, sy);
    if (sx < 0.05 && sy < 0.05) return ['', ''];
    const id = 'Bf' + (B_fid++);
    return [`<svg width="0" height="0" style="position:absolute"><filter id="${id}" x="-${pad}%" y="-${pad}%" width="${100 + 2 * pad}%" height="${100 + 2 * pad}%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="${sx.toFixed(2)} ${sy.toFixed(2)}"/></filter></svg>`, `filter:url(#${id});`];
  };
  const B_tile = (px) => `<div style="width:${px}px;height:${px}px;border-radius:${px * .277}px;background:linear-gradient(160deg,#294376,#1E2F52);display:flex;align-items:center;justify-content:center;box-shadow:inset 0 0 0 ${Math.max(.5, px * .006)}px rgba(255,255,255,.06)">${ffMark(px * .78, '#fff')}</div>`;

  // ======================= S2 · f72–100 =======================
  // measured tables (measure/tables.json S2_orbit), [cx, cy, size] per frame f72..f100, 720 space
  const ICON = [[359, 359.5, 184], [360, 360, 158], [359.5, 360, 147.5], [360, 360, 141], [360, 360, 137], [360, 360, 133], [360, 360, 131], [360, 360, 129], [360, 360, 127], [360.5, 360, 125.5], [360, 360, 124], [360, 360, 123], [360, 360, 122], [360, 360, 121], [359.5, 360, 119.5], [360, 360, 118], [360, 360, 116], [359.5, 360, 115.5], [359, 359.5, 112.5], [359, 359.5, 110.5], [358.5, 360, 107.5], [359, 359.5, 104.5], [359.5, 359, 99.5], [357.5, 359.5, 95], [353.5, 360.5, 89], [349.5, 361.5, 81], [347.5, 361, 72], [348.5, 358.5, 64], [352, 350, 56]];   // f99–f100 sizes read by eye (blurred bbox under-reads)
  const SQ = {
    // yellow slot → white square (passes behind the tile in the collapse, like the ref)
    y: [[252.0, 298.9, 76], [246.4, 304.6, 67.5], [234.5, 309.1, 67.0], [227.4, 314.7, 66.5], [223.0, 320.1, 66.5], [219.9, 325.0, 66.0], [218.0, 329.5, 65.0], [216.4, 333.3, 64.0], [215.7, 336.7, 63.5], [215.2, 339.7, 63.0], [215.4, 342.6, 62.5], [216.2, 345.1, 62.5], [217.4, 347.1, 62.0], [218.8, 348.9, 61.5], [221.0, 350.6, 61.0], [223.9, 351.8, 61.0], [227.2, 353.0, 61.0], [231.2, 354.2, 60.5], [236.3, 355.0, 60.5], [242.2, 355.9, 60.0], [249.4, 356.2, 60.0], [259.2, 356.5, 59.0], [271.3, 356.4, 58.0], [281.5, 356.9, 57], [294.5, 357.7, 55.5], [311.5, 357.6, 53.5], [334, 357.5, 51.5], [366, 358, 49], [410, 356, 45.5]],
    b: [[474.3, 266.6, 74.5], [439.5, 250.6, 69.5], [423.1, 239.5, 68.0], [411.7, 232.3, 66.0], [402.9, 227.4, 65.5], [396.0, 223.7, 65.0], [390.5, 221.0, 64.5], [385.7, 219.1, 64.0], [382.0, 217.7, 63.0], [378.7, 216.7, 63.0], [376.0, 216.0, 63.0], [373.8, 215.8, 62.5], [372.2, 215.8, 62.5], [370.7, 216.2, 62.0], [369.7, 216.8, 61.5], [369.1, 217.5, 61.5], [368.9, 218.6, 61.0], [368.7, 220.0, 61.0], [368.9, 221.9, 61.0], [369.6, 224.3, 60.0], [370.6, 227.1, 60.0], [373.4, 230.1, 59.5], [377.0, 234.0, 58.5], [378.9, 239.5, 57.0], [379.5, 247.2, 55.5], [381.5, 256.6, 53.5], [388.7, 267.7, 51.5], [401.8, 283.1, 49.0], [421.0, 304.8, 45.5]],
    g: [[479.0, 426.3, 95], [500.1, 422.9, 84.0], [505.9, 414.6, 78.5], [508.3, 406.5, 75.0], [509.2, 399.7, 72.0], [509.7, 393.9, 70.5], [509.7, 388.7, 68.5], [510.0, 384.6, 67.0], [509.7, 380.7, 66.5], [509.4, 377.7, 65.0], [509.5, 374.8, 64.5], [509.2, 372.3, 63.5], [509.1, 370.6, 63.0], [508.8, 368.7, 62.5], [508.7, 367.1, 62.0], [508.7, 365.9, 62.0], [508.6, 364.5, 62.0], [508.3, 363.7, 61.0], [508.3, 362.8, 61.0], [507.9, 362.0, 60.5], [508.1, 361.4, 59.5], [509.3, 360.7, 59.0], [510.8, 359.8, 57.5], [510.3, 359.7, 57.0], [507.4, 360.7, 55.0], [505.2, 361.3, 53.0], [506.9, 361.2, 50.0], [512.2, 360.8, 46.0], [518.1, 359.2, 43.0]],
    m: [[233.3, 460.4, 90], [267.0, 485.2, 82.0], [287.1, 496.4, 78.5], [301.1, 502.4, 75.0], [311.9, 505.8, 73.0], [320.0, 507.9, 72.0], [326.5, 508.9, 69.5], [331.9, 509.3, 68.5], [336.5, 509.6, 67.0], [340.6, 509.4, 66.5], [344.1, 509.0, 65.5], [347.1, 508.4, 65.0], [350.2, 507.9, 63.5], [353.2, 506.8, 63.5], [355.9, 505.7, 62.5], [358.8, 504.5, 62.5], [361.8, 503.2, 62.0], [364.9, 501.5, 61.5], [368.3, 499.5, 61.0], [371.8, 497.2, 60.5], [376.0, 494.6, 60.0], [381.9, 491.3, 58.5], [388.8, 487.0, 58.0], [394.5, 482.7, 57.5], [399.2, 478.6, 56.0], [405.8, 472.7, 54.0], [418.7, 464.1, 51.0], [438.5, 452.7, 48.5], [463.8, 435.5, 46.0]],
  };
  // Frame by Frame square fills (ref yellow/blue/green/magenta → white/electric blue/cyan/mint)
  const SQFILL = {
    y: 'linear-gradient(160deg,#FFFFFF 0%,#FBFCFE 55%,#EEF2F7 100%)',
    b: 'linear-gradient(160deg,#2556EE 0%,#2F6BFF 50%,#5AA0FF 100%)',
    g: 'linear-gradient(160deg,#27AFE3 0%,#3CC8F0 50%,#7BE0F8 100%)',
    m: 'linear-gradient(160deg,#35BF88 0%,#4ED6A0 50%,#86E8C2 100%)',
  };
  // whole-layer blur σ f72..f100 (S2_orbit.blur_sigma; <0.35 = JPEG noise → 0)
  const S2BLUR = [1.2, .45, .25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, .31, .46, .57, .72, .99, 1.25, 1.7, 2.2, 2.8, 3.5, 4.4];   // ref σ 3.0→11.2 over f97–f100 is inflated by the shrink; these match the ref by eye
  // halo disc diameter: grows out from under the tile (160 f75 → 200 f80 → 217 f86), then holds
  const HALO = [110, 128, 145, 160, 172, 182, 188, 194, 200, 204, 208, 209, 212, 215, 217, 217, 217, 217, 217, 218, 218, 219, 219, 220, 220, 220, 220, 220, 220];

  function B_square(k, F) {
    const tb = SQ[k], cx = B_s(F, 72, B_col(tb, 0)), cy = B_s(F, 72, B_col(tb, 1)), s = B_s(F, 72, B_col(tb, 2)) + kf(F, [[98, 0], [99, 3], [100, 7]]);
    // velocity → directional motion blur along travel (tangential to the orbit)
    const cx2 = B_s(F + 1, 72, B_col(tb, 0)), cy2 = B_s(F + 1, 72, B_col(tb, 1));
    const vx = cx2 - cx, vy = cy2 - cy, sp = Math.hypot(vx, vy), ang = Math.atan2(vy, vx) * 180 / Math.PI;
    const collapse = F > 93; // in the collapse the global blur carries it
    const sig = collapse ? 0 : Math.max(0, (sp - 4) * .24);
    const iso = kf(F, [[72, 5.5], [73, 2], [74, .6], [75, 0]]);   // the cut frame is smeared all round, like the ref
    const [defs, css] = B_blur(sig + iso, iso, 60);
    const edge = k === 'y' ? `box-shadow:inset 0 0 0 1px #E3E8EF,0 1px 4px rgba(30,47,82,.16);` : '';
    const sq = `<div style="width:${s}px;height:${s}px;border-radius:${s * 17 / 61}px;background:${SQFILL[k]};${edge}transform:rotate(${-ang}deg)"></div>`;
    return `${defs}<div class="a" style="left:${cx}px;top:${cy}px;width:0;height:0"><div class="a" style="left:${-s / 2}px;top:${-s / 2}px;width:${s}px;height:${s}px;transform:rotate(${ang}deg);${css}">${sq}</div></div>`;
  }

  SHOT({
    id: 'S2', f0: 72, f1: 100, render(lf, F) {
      B_fid = 0;
      const ic = B_s(F, 72, B_col(ICON, 2)), icx = B_s(F, 72, B_col(ICON, 0)), icy = B_s(F, 72, B_col(ICON, 1));
      const hd = B_s(F, 72, HALO), inner = hd * .765;
      const halo = `<div class="a" style="left:${360 - hd / 2}px;top:${360 - hd / 2}px;width:${hd}px;height:${hd}px;border-radius:50%;background:#E9EAEC;filter:blur(1.6px)"></div>
        <div class="a" style="left:${360 - inner / 2}px;top:${360 - inner / 2}px;width:${inner}px;height:${inner}px;border-radius:50%;background:#DEDFE2;filter:blur(1.4px)"></div>`;
      // icon: zoom-blur on the fast shrink at the cut (σ from table, scaled by shrink speed)
      const shrink = B_s(F, 72, B_col(ICON, 2)) - B_s(F + 1, 72, B_col(ICON, 2));
      const icb = F < 76 ? Math.max(0, shrink * .12) : 0;
      const icon = `<div class="a" style="left:${icx - ic / 2}px;top:${icy - ic / 2}px;${icb ? `filter:blur(${icb.toFixed(2)}px);` : ''}">${B_tile(ic)}</div>`;
      // depth: white + blue behind the tile, cyan + mint in front (as the ref's f72 overlaps read)
      const back = B_square('y', F) + B_square('b', F), front = B_square('g', F) + B_square('m', F);
      const g = B_s(F, 72, S2BLUR);
      const [defs, css] = B_blur(g, g, 20);
      return `<div class="a" style="inset:0;background:${B_PAGE}"></div>` + defs +
        B_wrap(`<div class="a" style="inset:0;${css}">${halo}${back}${icon}${front}</div>`);
    }
  });

  // ======================= S3 · f101–158 =======================
  const f3 = 101;
  // camera x (pan) = blue dot x − 408, camera y = dot y − 354.7 (S3_laptop), f101..f158
  const PAN = [-84.5, -84.5, -84.5, -84.5, -84.5, -84.5, -84.5, -84.5, -85.2, -84.7, -83.5, -82.5, -80.9, -78.7, -76.0, -72.1, -66.6, -57.4, -41.1, -25.9, -17.5, -12.5, -9.0, -6.6, -4.7, -3.4, -2.4, -1.5, -0.8, -0.5, -0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
  const TILT = [-4.5, -5.0, -4.4, -2.6, -1.5, -1.1, -1.0, -1.0, -0.8, -0.6, -0.2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.1, -0.1, -0.2, -0.2, -0.3, -0.5, -0.7, -0.9, -1.1, -1.3, -1.6, -1.9, -2.5, -2.9, -3.5, -4.1, -4.7, -5.7, -6.5, -7.5, -8.6, -9.9, -11.5, -13.1, -15.0, -17.3, -19.9, -22.8, -26.4, -30.7, -36.1, -43.2, -52.9, -69.1];
  const BL3 = [2.08, 1.99, 1.79, 1.54, 1.32, 1.06, .85, .63, .42, 0, 0, 0, 0, 0, .35, .48, .72, .87, .97, .84, .62, .48, .31, .2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, .34, .49, .58, .75, .96, 1.3, 1.92, 3.53, 8.36];
  // icon + dots arrive sliding left into the bar (the S2 collapse continues): extra x offsets f101..f110
  const SLIDE = [25, 8.5, 3, 1.5, .8, .4, .2, 0, 0, 0];
  const GAP1 = [48, 46.7, 39.5, 37.3, 36, 35, 34.7, 34.1, 33.9, 33.4, 33.4, 33.2, 32.8, 32.6];   // blue→cyan pitch
  const GAP2 = [36, 34.8, 34.6, 34.3, 34, 33.6, 33.2, 33.3, 33, 32.9, 32.7, 32.5, 32.4, 32.3];     // cyan→mint pitch
  // glass box: width f116..f150 (spring, peak f125–126), top relative to the dots
  const BOXW = [120, 175, 228, 318, 402, 449, 474, 486, 494, 496, 496, 495, 492, 488, 485, 482, 481, 481, 481, 481, 482, 483, 484, 485, 485, 485, 485, 485, 485, 485, 485, 485, 484, 484, 484];
  const BOXT = [26, 26, 25, 31.3, 37.2, 42.4, 44.4, 45.4, 46.3, 45.4, 44.4, 43.5, 41.8, 40.8, 40.5, 40.3, 40.4, 40.6, 40.9, 41.2, 41.6, 42, 42.2, 42.2, 42, 42, 41.9, 41.8, 41.8, 41.6, 41.6, 41.5, 41.5, 41.5, 41.6];
  const BOXH = [110, 128, 148, 151, 152];
  // typing: "Make a launch video for my app" (30 chars) — first legible f121 ("Make "), complete f150
  const TXT = 'Make a launch video for my app';
  const CH = { 121: 5, 122: 5, 123: 6, 124: 7, 125: 8, 126: 9, 127: 10, 128: 11, 129: 12, 130: 13, 131: 14, 132: 14, 133: 15, 134: 16, 135: 17, 136: 18, 137: 19, 138: 20, 139: 20, 140: 21, 141: 22, 142: 23, 143: 24, 144: 24, 145: 25, 146: 26, 147: 27, 148: 28, 149: 29, 150: 30 };
  const chars = F => { const f = Math.floor(F + 1e-6); return f < 121 ? 5 : f > 150 ? 30 : CH[f]; };
  // cursor tip path f101..f110 (S3_laptop cursor_tip_est + hidden-tip reads)
  const CUR = [[362, 452], [333, 428], [315, 406], [308, 395], [306, 384], [305, 377], [302, 369.5], [299, 364.5], [298, 361.5], [297, 360.5]];
  const B_arrow = (x, y, h, o = 1, extra = '') => {
    // macOS arrow, tip at (x,y), overall height h (720 space)
    const k = h / 25;
    return `<svg class="a" style="left:${x - 1.6 * k}px;top:${y - 1.6 * k}px;width:${19 * k}px;height:${27 * k}px;overflow:visible;opacity:${o};${extra}" viewBox="-1.6 -1.6 19 27"><path d="M0 0 L0 19.2 L4.6 14.9 L7.6 21.9 L10.6 20.6 L7.7 13.9 L13.7 13.9 Z" fill="#000" stroke="#fff" stroke-width="1.5" stroke-linejoin="round" style="filter:drop-shadow(0 .6px .9px rgba(0,0,0,.35))"/></svg>`;
  };

  // menu-bar glyphs (white, generic shapes)
  const wifi = (cx, cy) => `<svg class="a" style="left:${cx - 14}px;top:${cy - 10}px;width:28px;height:20px" viewBox="0 0 28 20"><path d="M2 7.2a17 17 0 0 1 24 0" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/><path d="M6.6 11.4a10.5 10.5 0 0 1 14.8 0" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/><path d="M11 15.4a4.2 4.2 0 0 1 6 0L14 18.6z" fill="#fff" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>`;
  const battery = (cx, cy) => `<div class="a" style="left:${cx - 19}px;top:${cy - 8.5}px;width:34px;height:17px;border:2px solid rgba(255,255,255,.55);border-radius:5.5px;padding:2px"><div style="width:100%;height:100%;background:#fff;border-radius:3px"></div></div><div class="a" style="left:${cx + 16}px;top:${cy - 3.5}px;width:3px;height:7px;border-radius:0 2px 2px 0;background:rgba(255,255,255,.55)"></div>`;
  const toggles = (cx, cy) => `<div class="a" style="left:${cx - 10}px;top:${cy - 12}px;width:20px;height:24px">
      <div class="a" style="left:0;top:0;width:20px;height:10.5px;border-radius:6px;border:1.8px solid #fff"></div><div class="a" style="left:3px;top:3px;width:4.5px;height:4.5px;border-radius:50%;background:#fff"></div>
      <div class="a" style="left:0;top:13.5px;width:20px;height:10.5px;border-radius:6px;background:#fff"></div><div class="a" style="left:12.5px;top:16.5px;width:4.5px;height:4.5px;border-radius:50%;background:#1a2745"></div></div>`;
  const dot = (cx, cy, c1, c2, c3, o = 1) => `<div class="a" style="left:${cx - 12}px;top:${cy - 12}px;width:24px;height:24px;border-radius:50%;opacity:${o};background:radial-gradient(circle at 34% 30%,${c1} 0%,${c2} 55%,${c3} 100%)"></div>`;
  // glass-box line icons (white, 20 px)
  const wave = `<svg viewBox="0 0 20 20" width="20" height="20"><path d="M3 8v4M6.5 5v10M10 3v14M13.5 6v8M17 8.5v3" stroke="#fff" stroke-width="1.7" stroke-linecap="round"/></svg>`;
  const clip = `<svg viewBox="0 0 20 20" width="20" height="20"><path d="M15.5 9.2 9.6 15.1a3.6 3.6 0 0 1-5.1-5.1l6.4-6.4a2.4 2.4 0 0 1 3.4 3.4l-6.2 6.2a1.2 1.2 0 0 1-1.7-1.7l5.6-5.6" fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
  const img = `<svg viewBox="0 0 20 20" width="20" height="20"><rect x="2.5" y="2.5" width="15" height="15" rx="3" fill="none" stroke="#fff" stroke-width="1.6"/><circle cx="7.2" cy="7.4" r="1.6" fill="#fff"/><path d="M3 15.2l4.6-4.4 3.3 3 2.4-2.1 4 3.6" fill="none" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>`;

  // wallpaper = Frame by Frame sky with the brand's thin white line art (world coords, pan-final)
  function wallpaper() {
    const L = 'rgba(255,255,255,.42)';
    const sparkle = (x, y, r) => `<svg class="a" style="left:${x - r}px;top:${y - r}px;width:${2 * r}px;height:${2 * r}px" viewBox="-10 -10 20 20"><path d="M0-10C.9-2.6 2.6-.9 10 0 2.6.9.9 2.6 0 10-.9 2.6-2.6.9-10 0-2.6-.9-.9-2.6 0-10Z" fill="#fff"/></svg>`;
    return `<div class="a" style="left:-300px;top:335px;width:1400px;height:1100px;background:linear-gradient(180deg,#263F72 0%,#2F4F86 12%,#3A6199 26%,#4A72A8 40%,#5A82B4 54%,#6891C0 70%,#769CC2 100%)"></div>
      <div class="a" style="left:430px;top:190px;width:560px;height:420px;border-radius:50%;background:radial-gradient(closest-side,rgba(127,174,158,.85),rgba(110,170,160,.35) 55%,rgba(110,170,160,0));filter:blur(18px)"></div>
      <div class="a" style="left:-120px;top:452px;width:560px;height:560px;border-radius:50%;box-shadow:inset 0 0 0 1px ${L}"></div>
      <div class="a" style="left:-300px;top:590px;width:1400px;height:1px;background:${L}"></div>
      <div class="a" style="left:-300px;top:706px;width:1400px;height:1px;background:${L}"></div>
      <div class="a" style="left:452px;top:335px;width:1px;height:1100px;background:${L}"></div>
      ${sparkle(452.5, 590.5, 13)}`;
  }

  SHOT({
    id: 'S3', f0: 101, f1: 158, render(lf, F) {
      B_fid = 0;
      const P = B_s(F, f3, PAN), T = B_s(F, f3, TILT);
      const slide = B_s(F, f3, SLIDE, false);
      const g1 = B_s(F, f3, GAP1, false), g2 = B_s(F, f3, GAP2, false);
      const DY = 354.7;                                 // settled dot row (world)
      const icx = 371.5 + slide, bx = 408 + slide, cx2 = bx + g1, cx3 = cx2 + g2;
      const dotsO = cl((F - 101.2) / .8);               // cyan + mint appear at f102
      const pressed = cl((F - 112.5) / 1.5);            // menu-extra highlight after the click

      // ---- world (moves with the camera) ----
      let w = '';
      // bezel: black band y300–335 with a grey top highlight, rounded top-right corner (outer r 62) at x≈796
      w += `<div class="a" style="left:-300px;top:300px;width:1096px;height:1200px;background:#050505;border-radius:0 62px 0 0;box-shadow:inset 0 2px 0 #5E5F60"></div>`;
      // screen, clipped to the inner bezel edge (right edge x≈764, inner corner r 30)
      w += `<div class="a" style="left:-300px;top:335px;width:1064px;height:1200px;border-radius:0 30px 0 0;overflow:hidden"><div class="a" style="left:300px;top:-335px;width:0;height:0">
          ${wallpaper()}
          <div class="a" style="left:-300px;top:335px;width:1400px;height:39.5px;background:linear-gradient(180deg,rgba(14,22,44,.80),rgba(18,28,54,.72))"></div>
        </div></div>`;
      // menu-bar cluster (white glyphs, 23 px type)
      w += wifi(199, DY) + battery(255, DY) + toggles(314, DY);
      w += `<div class="a" style="left:${icx - 17.5}px;top:${DY - 17.5}px;width:35px;height:35px;border-radius:9px;background:rgba(255,255,255,${.2 * pressed})"></div>`;
      w += `<div class="a" style="left:${icx - 17.5}px;top:${DY - 17.5}px">${ffMark(35, '#fff')}</div>`;
      w += dot(bx, DY, '#7FB0FF', '#2F6BFF', '#2556EE') + dot(cx2, DY, '#A6EBFA', '#3CC8F0', '#27AFE3', dotsO) + dot(cx3, DY, '#A5EFD2', '#4ED6A0', '#35BF88', dotsO);
      w += `<div class="a" style="left:517px;top:${DY - 14}px;font:400 23px/28px Inter;letter-spacing:-.01em;color:#fff;white-space:nowrap">Mon Jun 22</div>`;
      w += `<div class="a" style="left:659px;top:${DY - 14}px;font:400 23px/28px Inter;letter-spacing:-.01em;color:#fff;white-space:nowrap">9:41 AM</div>`;

      // ---- glass prompt box (springs out of the menu-bar icon, centred under it) ----
      if (F >= 116) {
        const bw = B_s(F, 116, BOXW, false), bt = DY + B_s(F, 116, BOXT, false), bh = B_s(F, 116, BOXH, false);
        const bo = cl((F - 116) / 2.2), co = cl((F - 117) / 3);
        const pb = kf(F, [[116, 9], [117, 7], [118, 4.5], [119, 3.2], [120, 2.2], [121, 1.1], [122, .4], [123, 0]]);
        const n = chars(F), s = TXT.slice(0, n);
        const tx = 371.5 - 202.5, ty = bt + 36 - 3.5;
        const content = `<div class="a" style="left:${tx}px;top:${ty}px;font:400 25.5px/25.5px Inter;letter-spacing:-.012em;color:#F4F8FF;white-space:pre">${s}<span style="display:inline-block;width:1.6px;height:27px;margin-left:1px;vertical-align:-5px;background:#F4F8FF"></span></div>
            <div class="a" style="left:${371.5 - 192.5 - 10}px;top:${bt + 101}px">${wave}</div>
            <div class="a" style="left:${371.5 - 128.5 - 10}px;top:${bt + 101}px">${clip}</div>
            <div class="a" style="left:${371.5 - 62.5 - 10}px;top:${bt + 101}px">${img}</div>
            <div class="a" style="left:${371.5 + 203.5 - 17}px;top:${bt + 112 - 17}px;width:34px;height:34px;border-radius:50%;background:radial-gradient(circle at 40% 30%,#4F86FF,#2F6BFF 70%);display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 20 20" width="18" height="18"><path d="M10 15.5V4.8M5.2 9.4 10 4.6l4.8 4.8" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>`;
        const panel = `<div class="a" style="left:${icx - bw / 2}px;top:${bt}px;width:${bw}px;height:${bh}px;border-radius:40px;opacity:${bo};${pb ? `filter:blur(${pb}px);` : ''}
            background:linear-gradient(165deg,rgba(255,255,255,.34) 0%,rgba(255,255,255,.20) 38%,rgba(230,240,255,.14) 100%);
            -webkit-backdrop-filter:blur(10px) saturate(1.15);backdrop-filter:blur(10px) saturate(1.15);
            box-shadow:inset 0 1.5px 0 rgba(255,255,255,.62),inset 0 0 0 1.2px rgba(255,255,255,.38),inset 0 -1px 0 rgba(255,255,255,.22),0 10px 28px rgba(12,24,52,.22)"></div>`;
        w += panel + `<div class="a" style="inset:0;opacity:${co};${pb ? `filter:blur(${pb * .8}px);` : ''}">${content}</div>`;
      }

      // ---- camera blur: isotropic settle at the cut, horizontal on the pan, vertical on the whip-tilt ----
      const b = B_s(F, f3, BL3);
      let sx = 0, sy = 0;
      if (F < 112) { sx = b * 2; sy = b * 1.6; }
      else if (F < 140) { sx = b * 2.2; sy = b * .3; }
      else { sy = Math.min(b * 1.3, 3 + b * .35); sx = Math.min(b * .6, 3.5); }
      const [defs, css] = B_blur(sx, sy, 25);
      const zs = kf(F, [[101, 1.05], [103, 1.035], [106, 1.008], [108, 1]], E.outQ);   // slight zoom-out settle about the right of the bar
      const world = `<div class="a" style="left:0;top:0;width:720px;height:720px;transform-origin:600px 354px;transform:translate(${P}px,${T}px) scale(${zs});${css}">${w}</div>`;

      // ---- cursor (screen space) ----
      let cur = '';
      if (F < 133) {
        let x, y, sc = 1, o = 1;
        if (F <= 110) { x = B_s(F, f3, B_col(CUR, 0)); y = B_s(F, f3, B_col(CUR, 1)); }
        else { x = 371.5 + P + 10.6; y = 360 + T; }
        sc = kf(F, [[112.5, 1], [117, .62], [121, .64], [130, .78]], E.ioS);
        o = kf(F, [[130.5, 1], [132.8, 0]]);
        // motion blur along travel (fast rise at the cut)
        const x2 = F <= 110 ? B_s(F + 1, f3, B_col(CUR, 0)) : x, y2 = F <= 110 ? B_s(F + 1, f3, B_col(CUR, 1)) : y;
        const sp = Math.hypot(x2 - x, y2 - y), ang = Math.atan2(y2 - y, x2 - x) * 180 / Math.PI;
        const [cd, cc] = B_blur(Math.max(0, (sp - 5) * .3), 0, 80);
        cur = cd + `<div class="a" style="left:${x}px;top:${y}px;width:0;height:0;transform:rotate(${ang}deg);${cc}"><div class="a" style="left:0;top:0;width:0;height:0;transform:rotate(${-ang}deg)">${B_arrow(0, 0, 50 * sc, o)}</div></div>`;
      }

      // ---- page above the laptop: warm white, tints to the flash blue on the way out ----
      const tint = F < 153 ? B_PAGE : mixHex(B_PAGE, '#E6F4FE', kf(F, [[153, 0], [154, .1], [155, .22], [156, .38], [157, .62], [158, 1]]));
      return `<div class="a" style="inset:0;background:${tint}"></div>` + defs + B_wrap(world + cur);
    }
  });
})();
