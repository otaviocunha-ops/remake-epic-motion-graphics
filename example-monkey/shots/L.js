// Monkey example, shot L: frames 0–225 (prompt box over goat → button zoom → click → glass morph → Monke landing page → pull-back)
// Pure function of F. All geometry measured from ref/full (numpy) unless noted.
(function () {
  // ---- words you can change (see README) ----
  const L_TXT = Object.assign({ model: 'Frame 1.0', pill: 'Made with Frame by Frame', logos: ['BANANA CO.', 'JUNGLE', 'FRAME 1.0'] }, window.FILM_TEXT || {});
  const L_PROMPT = 'Build a premium, modern meme-tech landing page for a monkey who takes selfies. Create a full-screen cinematic hero featuring a grinning macaque in sport sunglasses, positioned on the right side with generous negative space on the left. Use a bold white headline about taking better selfies, a short supporting paragraph, and a clean rounded “Get the Banana” CTA.\n\nAdd a minimal top navigation with logo.';
  const L_N = L_PROMPT.length;
  const L_tab = (F, f0, arr) => samples(F, f0, arr);
  const L_esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

  // ---------- typing cadence (ref chars typed per frame) ----------
  // f4 'B' … f26 'sports-' (30) stall … f40–48 burst to the end (ref prompt = 424 chars)
  const L_NT = [[0, 0], [3, 0], [4, 1], [5, 3], [6, 5], [7, 7], [8, 9], [9, 11], [10, 13], [11, 15], [12, 17], [13, 18.5], [14, 20], [15, 21.5], [16, 23], [17, 24], [18, 25], [19, 26], [20, 27], [22, 28], [24, 29], [26, 30], [39, 30], [40, 53], [41, 113], [42, 180], [43, 233], [44, 290], [45, 346], [46, 390], [47, 409], [48, 430]];
  const L_nTyped = F => Math.floor(kf(F, L_NT));
  const L_tauOf = i => { // frame at which char i was typed (inverse of L_NT)
    for (let k = 1; k < L_NT.length; k++) if (L_NT[k][1] > i) { const [f0, v0] = L_NT[k - 1], [f1, v1] = L_NT[k]; return f0 + (f1 - f0) * (i + 1 - v0) / Math.max(1e-6, v1 - v0); }
    return 48;
  };
  // colour shimmer: slow wave through the first 30 chars, age palette for the burst
  const L_W = [[4, 5], [14, 5.5], [16, 6.5], [18, 7.5], [20, 12], [22, 15], [24, 17], [26, 21], [28, 24], [30, 27], [36, 31], [39, 34], [40, 38], [41, 41], [42, 44], [43, 48]];
  const L_P1 = [[0, '#24249a'], [5, '#24249a'], [6.5, '#3c62c8'], [8, '#7fa5d8'], [9.8, '#7a7766'], [11.5, '#7a3048'], [13.5, '#121212']];
  const L_P2 = [[0, '#2638a8'], [1.5, '#3558b8'], [2.8, '#6f7fa8'], [4, '#8a4a62'], [5.5, '#6e2840'], [9, '#5e2638'], [12, '#141414']];
  const L_pal = (P, d) => { if (d <= P[0][0]) return P[0][1]; for (let k = 1; k < P.length; k++) if (d <= P[k][0]) return mixHex(P[k - 1][1], P[k][1], (d - P[k - 1][0]) / (P[k][0] - P[k - 1][0])); return P[P.length - 1][1]; };
  function L_charColor(i, F) {
    if (F >= 62) return '#121212';
    if (i < 30) { const d = kf(F, L_W) - i; return d < 0 ? '#121212' : L_pal(L_P1, d); }
    return L_pal(L_P2, F - L_tauOf(i));
  }
  // coloured spans (grouped by colour) for the first n chars
  function L_promptHTML(n, F, caret) {
    let out = '', cur = null, buf = '';
    const flush = () => { if (buf) out += `<span style="color:${cur}">${L_esc(buf)}</span>`; buf = ''; };
    for (let i = 0; i < Math.min(n, L_N); i++) { const c = L_charColor(i, F); if (c !== cur) { flush(); cur = c; } buf += L_PROMPT[i]; }
    flush();
    if (caret) out += `<span style="display:inline-block;width:2px;height:.9em;margin-left:4px;vertical-align:-.1em;background:#222"></span>`;
    return out;
  }

  // ---------- box geometry, segment A (measured bbox per frame) ----------
  const L_BOXA = [[884,635,1593,747],[839,613,1558,726],[792,589,1520,703],[758,572,1493,688],[732,559,1472,675],[711,548,1455,665],[693,539,1441,657],[678,532,1428,650],[665,525,1417,643],[654,519,1408,638],[644,514,1400,633],[635,510,1393,629],[627,505,1386,625],[620,502,1380,621],[614,499,1375,618],[608,496,1370,616],[603,493,1366,613],[599,491,1362,611],[595,489,1359,609],[591,487,1356,608],[588,485,1353,606],[585,484,1351,605],[583,483,1349,604],[581,482,1348,603],[580,481,1346,602],[578,480,1345,601],[576,480,1345,602],[574,479,1346,603],[571,478,1347,605],[570,477,1348,607]];
  // 30–63 keyframes (box grows into the tall prompt, 3D tilt 33–41)
  const L_BOXK = [[29, [570, 477, 1348, 607]], [30, [564, 474, 1352, 610]], [32, [556, 466, 1360, 624]], [34, [546, 456, 1370, 640]], [36, [541, 425, 1374, 677]], [38, [540, 320, 1380, 784]], [40, [548, 276, 1368, 820]], [42, [556, 258, 1358, 832]], [44, [568, 248, 1351, 842]], [47, [572, 235, 1346, 848]], [51, [575, 227, 1341, 853]], [55, [569, 223, 1336, 855]], [57, [564, 223, 1331, 856]], [58, [560, 223, 1328, 856]], [59, [555, 223, 1323, 856]], [60, [549, 223, 1317, 856]], [61, [541, 223, 1309, 856]], [62, [530, 223, 1298, 856]], [63, [514, 223, 1281, 856]]];
  const L_BTNA = [51,52,53,54,55,55,60,64,66,68,68,69,70,71,72,72,73,74,74,75,74,75,75,75,75,75,75,75,75,75];
  function L_boxA(F) { return F <= 29 ? L_tab(F, 0, L_BOXA.map(b => b)) && L_BOXA[Math.min(29, Math.round(F))] : kf(F, L_BOXK, E.ioS); }

  // ---------- prompt box renderer ----------
  // o: {x,y,w,h, n, F, btn, caret, bg, textOp, btnFill, arrowT, label, tilt, radius, shade}
  const L_FS = 34.8, L_LH = 44.4, L_PADL = 42, L_PADT = 45;
  function L_box(o) {
    const { x, y, w, h } = o, r = o.radius ?? 18, bs = o.btn;
    const bx = w - 23 - bs, by = o.single ? (h - bs) / 2 : h - 25 - bs;
    const arrowT = o.arrowT ?? 1;
    const aw = bs * 0.30, ah = bs * 0.40;
    const arrow = arrowT <= 0 ? '' : `<svg class="a" style="left:${bs / 2 - aw}px;top:${bs / 2 - ah / 2 + (1 - arrowT) * bs * .55}px;width:${aw * 2}px;height:${ah}px;overflow:visible;opacity:${cl(arrowT * 1.5)}" viewBox="0 0 20 26"><path d="M10 25 V2 M1.5 10.5 L10 2 L18.5 10.5" fill="none" stroke="#fff" stroke-width="${2.6}" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
    const btn = `<div class="a" style="left:${bx}px;top:${by}px;width:${bs}px;height:${bs}px;border-radius:${bs * .24}px;background:${o.btnFill || '#000'};overflow:hidden;${o.btnExtra || ''}">${arrow}</div>`;
    // model label: left of the send button (single line) / on the blank row just above-left (tall prompt)
    const lt = cl((h - 160) / 300), lfs = 17;
    const labelCY = by + bs / 2 - lt * (bs / 2 + 14);
    const label = o.label === false ? '' : `<div class="a" style="right:${w - bx + 14}px;top:${labelCY - lfs * .62}px;font:500 ${lfs}px/1.24 Inter;color:#8b8b90;white-space:nowrap;letter-spacing:-.1px;opacity:${o.labelOp ?? 1}">${L_TXT.model} <span style="font-size:${lfs * .8}px;position:relative;top:-1px">&#8964;</span></div>`;
    const tH = o.single ? `top:${(h - L_LH) / 2}px` : `top:${o.padT ?? L_PADT}px`;
    const text = `<div class="a" style="left:${L_PADL}px;${tH};width:${o.textW ?? 683}px;font:400 ${L_FS}px/${L_LH}px Inter;letter-spacing:0;white-space:pre-wrap;color:#121212;opacity:${o.textOp ?? 1};${o.textMask ? `-webkit-mask-image:${o.textMask};mask-image:${o.textMask};` : ''}">${L_promptHTML(o.n, o.F, o.caret)}</div>`;
    const tilt = o.tilt ? `transform-origin:50% 0%;transform:perspective(1400px) rotateX(${o.tilt}deg);` : '';
    return `<div class="a" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;${tilt}">
      <div class="a" style="inset:0;border-radius:${r}px;background:${o.bg || '#fff'};overflow:hidden;box-shadow:${o.shadow || '0 10px 40px rgba(20,30,70,.10)'}">${o.shade || ''}${text}${label}${btn}${o.over || ''}</div></div>`;
  }

  // ---------- goat background (segment A/B) ----------
  // goat pose in "f0 frame": mirrored so it runs the runner's way; photo scale .8, head at (1750,350)
  const L_GS = 0.75, L_GL = 720, L_GT = -150; // goat image box in f0 frame (2560×1440 × .55, mirrored); goat centre ≈ (1530,300)
  // photo camera: similarity (s, mid) measured from 2 runner keypoints 0–30; 40–63 push-in re-aimed so the goat stays right of the prompt
  const L_PC = [[0, [1, 1562.5, 555]], [1, [.9876, 1537.9, 544.4]], [2, [.9747, 1510.5, 532.5]], [3, [.9652, 1491.4, 524.7]], [4, [.9587, 1476.6, 519]], [6, [.948, 1453.8, 509]], [8, [.9414, 1437.1, 503.1]], [10, [.937, 1423.7, 498]], [12, [.932, 1413, 494.2]], [16, [.9264, 1398, 488.2]], [20, [.9273, 1388.4, 484.9]], [25, [.9265, 1381.9, 484]], [30, [.93, 1378.4, 485.9]], [40, [.93, 1378, 486]], [50, [.97, 1505, 571]], [63, [1.0, 1560.5, 605]]];
  function L_photoPose(F) { const [s, mx, my] = kf(F, L_PC); return { s, tx: mx - s * 1562.5, ty: my - s * 555 }; }
  // hand-traced goat silhouette (goat_bg.jpg px, un-mirrored), used as a 2–3 px feathered mask → crisp opaque cut-out
  const L_GOATPOLY = [[1008,785],[1020,720],[1035,620],[1050,570],[1090,535],[1150,525],[1175,500],[1175,400],[1185,310],[1200,265],[1225,270],[1250,330],[1255,430],[1270,490],[1290,480],[1285,530],[1350,530],[1450,490],[1530,450],[1630,410],[1730,365],[1830,340],[1950,332],[2050,350],[2150,385],[2195,415],[2240,450],[2280,390],[2320,365],[2345,380],[2330,430],[2280,490],[2260,530],[2250,620],[2235,700],[2210,800],[2200,900],[2175,980],[2120,1060],[2075,1140],[2050,1210],[2010,1260],[1960,1250],[1945,1215],[1900,1225],[1885,1200],[1905,1130],[1950,1060],[1990,990],[2000,930],[1985,860],[1940,840],[1850,770],[1770,780],[1650,820],[1510,900],[1410,980],[1350,1060],[1320,1130],[1310,1200],[1280,1240],[1220,1230],[1215,1190],[1250,1140],[1255,1075],[1245,1030],[1275,995],[1330,930],[1360,860],[1385,790],[1330,770],[1300,760],[1200,790],[1100,840],[1050,850],[1020,820]];
  const L_GOATSVG = (() => {
    const pts = L_GOATPOLY.map(([x, y]) => `${x},${y}`).join(' ');
    return (filt, id) => `<svg class="a" style="left:0;top:0;width:2560px;height:1440px;overflow:visible" viewBox="0 0 2560 1440">
      <defs><filter id="Lgf${id}" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="2.6"/></filter>
      <mask id="Lgm${id}" maskUnits="userSpaceOnUse" x="0" y="0" width="2560" height="1440"><polygon points="${pts}" fill="#fff" stroke="#fff" stroke-width="6" stroke-linejoin="round" filter="url(#Lgf${id})"/></mask></defs>
      <g transform="translate(2560 0) scale(-1 1)"><g mask="url(#Lgm${id})"><image href="assets/goat_bg.jpg" x="0" y="0" width="2560" height="1440" style="${filt}"/></g></g></svg>`;
  })();
  function L_goatImg(pose, extraFilter = '', id = 'a') {
    return `<div class="a" style="left:0;top:0;width:1920px;height:1080px;transform-origin:0 0;transform:translate(${pose.tx}px,${pose.ty}px) scale(${pose.s})">
      <div class="a" style="left:${L_GL}px;top:${L_GT}px;width:2560px;height:1440px;transform-origin:0 0;transform:scale(${L_GS})">${L_GOATSVG(`filter:saturate(1.08) contrast(1.06) brightness(1.03) ${extraFilter}`, id)}</div></div>`;
  }
  const L_SKY = 'linear-gradient(180deg,#294376 0%,#35598f 25%,#42699d 46%,#5a82b4 68%,#6891c0 84%,#769cc2 100%)';

  // overlay graphics (circles, grid lines, sparkles, diagonals, dots, rainbow glow) in f0 frame, moved by overlay transform
  // overlay transform from the measured grid lines: y_top, y_bot (h lines) and x_v (v line)
  const L_OV = [[0, [410.2, 833.2, 948.3]], [1, [398.9, 817.7, 927.7]], [2, [381, 797.7, 895]], [3, [359.4, 778.5, 856.5]], [4, [338.8, 761.3, 819.9]], [5, [321.8, 747.3, 789.6]], [6, [308, 735.7, 764.8]], [7, [296.4, 726.1, 744.4]], [8, [286.7, 717.6, 727]], [9, [278.3, 710.4, 712.1]], [10, [271.1, 704.1, 699.1]], [12, [259, 693.6, 677.6]], [14, [249.4, 685.2, 660.7]], [16, [241.9, 678.5, 647.1]], [18, [235.8, 673.2, 636.1]], [20, [230.8, 669.1, 627.4]], [22, [227, 665.6, 620.5]], [24, [223.9, 663.1, 615.1]], [26, [221.7, 661.2, 611.2]], [28, [220, 660, 608.2]], [30, [219, 659.4, 606.5]], [34, [218, 659, 605]], [40, [218.3, 658.6, 603.3]], [44, [218.5, 657.3, 598.2]], [48, [218.4, 654.9, 588.9]], [50, [218.2, 652.9, 582.3]], [52, [217.8, 650.2, 573.8]], [54, [217.1, 647.1, 562.7]], [56, [216.1, 642.7, 548.2]], [58, [214.7, 636.7, 528.8]], [60, [212.4, 628.2, 501.1]], [61, [210.8, 622.4, 482.6]], [62, [208.8, 615.1, 459.1]], [63, [206.1, 605.8, 429.8]]];
  function L_ovPose(F) { const [yt, yb, xv] = kf(F, L_OV); const s = (yb - yt) / 423; return { s, tx: xv - s * 948.3, ty: yt - s * 410.2 }; }
  function L_overlay(F, op = 1) {
    const p = L_ovPose(F);
    const ln = 'rgba(235,242,255,.55)';
    const star = (x, y) => `<svg class="a" style="left:${x - 22}px;top:${y - 22}px;width:44px;height:44px;overflow:visible" viewBox="-22 -22 44 44"><path d="M0-20 C1.2-3 3-1.2 20 0 C3 1.2 1.2 3 0 20 C-1.2 3 -3 1.2 -20 0 C-3-1.2 -1.2-3 0-20Z" fill="rgba(255,255,255,.95)"/><circle r="5" fill="rgba(255,255,255,.35)"/></svg>`;
    return `<div class="a" style="left:0;top:0;width:1920px;height:1080px;transform-origin:0 0;transform:translate(${p.tx}px,${p.ty}px) scale(${p.s});opacity:${op}">
      <div class="a" style="left:780px;top:-260px;width:1100px;height:760px;background:radial-gradient(closest-side at 22% 42%,rgba(150,110,190,.55),transparent),radial-gradient(closest-side at 45% 45%,rgba(215,215,140,.55),transparent),radial-gradient(closest-side at 62% 55%,rgba(110,215,190,.6),transparent),radial-gradient(closest-side at 75% 68%,rgba(90,190,230,.45),transparent);filter:blur(40px)"></div>
      <div class="a" style="left:860px;top:20px;width:300px;height:170px;background-image:radial-gradient(rgba(255,255,255,.5) 1px,transparent 1.3px);background-size:9px 9px;-webkit-mask-image:radial-gradient(closest-side,#000,transparent);mask-image:radial-gradient(closest-side,#000,transparent);opacity:.6"></div>
      <svg class="a" style="left:0;top:0;width:1920px;height:1080px;overflow:visible" viewBox="0 0 1920 1080">
        <g fill="none" stroke="${ln}" stroke-width="1.6">
          <line x1="-400" y1="410.2" x2="2400" y2="410.2"/><line x1="-400" y1="833.2" x2="2400" y2="833.2"/>
          <line x1="948.3" y1="-400" x2="948.3" y2="1500"/><line x1="1906" y1="-400" x2="1906" y2="1500"/>
          <circle cx="657" cy="118" r="290"/><circle cx="1565" cy="615" r="208"/>
          <line x1="560" y1="398" x2="1120" y2="648" stroke-width="1.2"/><line x1="945" y1="-10" x2="1920" y2="590" stroke-width="1.2"/>
        </g></svg>
      ${star(948.3, 410.2)}${star(948.3, 833.2)}${star(1906, 410.2)}
    </div>`;
  }
  const L_GRAIN = op => `<svg class="a" style="left:0;top:0;width:1920px;height:1080px;opacity:${op};mix-blend-mode:overlay" viewBox="0 0 1920 1080"><filter id="Lgr"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 .5  0 0 0 0 .5  0 0 0 0 .5  0 0 0 1.2 -.1"/></filter><rect width="1920" height="1080" filter="url(#Lgr)"/></svg>`;

  // ascii glyph field (%, @, #, slashed boxes), edge-masked
  function L_ascii(op, mask, dy = 0) {
    if (op <= 0.01) return '';
    const rows = []; const G = ['%', '%', '%', '%', '%', '%', '%', '@', '@', '@', '@', '@', '#', '#', '#', '#', '#', '#', '#', '⨸', '⨸', '⨸', '⨸', '%', '%', '%', '%', '#', '#', '#', '#', '#', '#', '#', '#', '#'];
    for (let r = 0; r < 36; r++) rows.push(Array(64).fill(G[r % G.length]).join(' '));
    return `<div class="a" style="inset:0;overflow:hidden;opacity:${op};-webkit-mask-image:${mask};mask-image:${mask}"><div class="a" style="left:6px;top:${-4 + dy}px;font:700 24.4px/30.2px Menlo,monospace;letter-spacing:0;color:rgba(222,228,255,.72);white-space:pre">${rows.join('\n')}</div></div>`;
  }

  // ---------- selection handles ----------
  const L_HK = [[29, [556, 462]], [31, [523, 430]], [32, [504, 414]], [33, [474, 389]], [34, [414, 341]], [35, [290, 236]], [36, [162, 135]], [37, [112, 98]], [38, [89, 75]], [39, [68, 58]], [41, [41, 35]], [43, [30, 28]], [47, [12, 10]], [52, [-40, -40]]];
  const L_HS = [[0, 0], [1, 8], [2, 14], [4, 22], [8, 28], [20, 32], [29, 34], [32, 40], [36, 48], [40, 52], [43, 54], [50, 56]];
  function L_handles(F, b) {
    if (F < 1 || F > 51) return '';
    const s = kf(F, L_HS);
    let pts;
    if (F <= 29) pts = [[b[0] - 12, b[1] - 19], [b[2] + 15, b[1] - 19], [b[0] - 12, b[3] + 10], [b[2] + 15, b[3] + 10]];
    else { const [x, y] = kf(F, L_HK, E.lin); const X2 = 1914 - x, Y2 = 1080 - y; pts = [[x, y], [X2, y], [x, Y2], [X2, Y2]]; }
    return pts.map(([x, y], i) => `<div class="a" style="left:${x - s / 2}px;top:${y - s / 2}px;width:${s}px;height:${s}px;background:#fff;${i >= 2 && F > 33 ? `filter:blur(${cl((F - 33) / 4) * 3}px);box-shadow:0 0 18px 6px rgba(255,255,255,.35);` : ''}"></div>`).join('');
  }

  // ---------- purple solarise wash (29–42) ----------
  const L_WASH = [[28, 0], [29, .12], [31, .35], [33, .6], [35, .88], [36, 1], [37, 1], [38, .85], [39, .6], [40, .38], [41, .18], [42, .06], [44, 0]];

  // ---------- cursor (macOS arrow, tip at x,y; len = tip→tail px; rot = deg about the tip) ----------
  function L_cursor(x, y, len, rot = 0, white = false, op = 1) {
    const k = len / 232;   // glyph measured on ref f88 (inner black arrow, 17 px white outline), ~232 px tall there
    return `<svg class="a" style="left:${x - 30 * k}px;top:${y - 30 * k}px;width:${220 * k}px;height:${270 * k}px;overflow:visible;opacity:${op};transform-origin:${30 * k}px ${30 * k}px;transform:rotate(${rot}deg);filter:drop-shadow(0 ${2 * k}px ${4 * k}px rgba(0,0,0,.25));z-index:40" viewBox="-30 -30 220 270"><path d="M0 0 L34 178 L73 128 L123 200 L143 190 L95 113 L154 95 Z" fill="${white ? '#fff' : '#000'}" stroke="${white ? '#000' : '#fff'}" stroke-width="${white ? 18 : 34}" stroke-linejoin="round" style="paint-order:stroke"/></svg>`;
  }
  // measured tip path [x, y, len, rot]: A appears f55 on the runner's arm pointing left; B swings into the button
  const L_CUR = [[55, [1455, 595, 49, -36]], [57, [1452, 597, 59, -36]], [59, [1450, 602, 67, -36]], [61, [1448, 618, 85, -36]], [63, [1437, 650, 112, -37]], [64, [1420, 683, 140, -39]], [65, [1355, 720, 173, -29]], [66, [1248, 745, 201, -14]], [67, [1202, 723, 220, 3]], [68, [1172, 724, 232, 0]], [69, [1149, 721, 232, 0]], [70, [1131, 716, 232, 0]], [71, [1117, 710, 232, 0]], [72, [1106, 704, 232, 0]], [73, [1097, 698, 232, 0]], [74, [1090, 693, 232, 0]], [75, [1085, 689, 232, 0]], [76, [1081, 685, 232, 0]], [77, [1077, 681, 232, 0]], [78, [1073, 677, 232, 0]], [79, [1069, 673, 232, 0]], [80, [1064, 668, 232, 0]], [81, [1058, 663, 227, 0]], [82, [1049, 656, 215, 0]], [83, [1045, 654, 207, 0]], [84, [1050, 657, 217, 0]], [85, [1058, 662, 229, 0]], [86, [1063, 665, 232, 0]], [87, [1066, 667, 232, 0]], [88, [1068, 668, 232, 0]], [91, [1069, 669, 232, 0]]];

  // ---------- segment A: 0–63 ----------
  function L_segA(F) {
    const wash = kf(F, L_WASH);
    const pose = L_photoPose(F);
    const sol = wash > .01 ? `url(#Lsol)` : '';
    let h = `<div class="a" style="inset:0;background:${L_SKY}"></div>`;
    h += wash > .01 ? `<svg width="0" height="0" style="position:absolute"><filter id="Lsol" color-interpolation-filters="sRGB"><feComponentTransfer><feFuncR type="table" tableValues="${[0, .5, .9, .55, .8].map(v => lerp(0, v, 1) * wash + 0).join(' ')}"/><feFuncG type="table" tableValues="0 .45 .8 .5 .75"/><feFuncB type="table" tableValues="0 .6 1 .8 1"/></feComponentTransfer></filter></svg>` : '';
    h += L_GRAIN(.2 + wash * .2);
    h += L_goatImg(pose, wash > .3 ? `url(#Lsol)` : '');
    h += L_overlay(F);
    // faint glyph lattice inside the right circle 14–30 and full edge fields 28–42
    const asc = kf(F, [[26, 0], [29, .55], [33, 1], [38, 1], [41, .5], [44, 0]]);
    h += L_ascii(asc, 'linear-gradient(90deg,#000 0,rgba(0,0,0,.8) 16%,transparent 34%,transparent 80%,rgba(0,0,0,.8) 92%,#000 100%)');
    if (wash > .01) h += `<div class="a" style="inset:0;background:linear-gradient(180deg,#5f5ad8 0%,#4b3fe0 55%,#5a55ee 100%);mix-blend-mode:color;opacity:${wash * .85}"></div><div class="a" style="inset:0;background:linear-gradient(180deg,rgba(90,80,220,.0),rgba(80,70,230,.35));opacity:${wash}"></div><div class="a" style="left:-200px;top:100px;width:1500px;height:360px;background:radial-gradient(closest-side,rgba(40,30,150,.45),transparent);opacity:${wash}"></div>`;
    if (wash > .05) h += L_GRAIN(wash * .25);
    // box
    const b = F <= 29 ? L_BOXA[Math.min(29, Math.round(F))] : kf(F, L_BOXK, E.lin);
    const bw = b[2] - b[0], bh = b[3] - b[1];
    const btn = F <= 29 ? L_BTNA[Math.min(29, Math.round(F))] : 75;
    const n = L_nTyped(F);
    const tilt = kf(F, [[32, 0], [34, 7], [36, 12], [38, 9], [40, 3], [42, 0]]);
    const tint = wash > .01 ? `linear-gradient(180deg,rgba(214,214,255,${wash * .9}),rgba(170,170,245,${wash * .9}))` : null;
    const bg = tint ? `${tint},#fff` : (F > 40 && F < 52 ? `linear-gradient(20deg,rgba(215,205,245,${cl((52 - F) / 10) * .7}) 0%,rgba(255,255,255,0) 45%),#fff` : '#fff');
    h += L_handles(F, b);
    h += L_box({ x: b[0], y: b[1], w: bw, h: bh, n, F, btn, single: bh < 140, caret: F >= 4 && (F < 52 || Math.floor(F / 8) % 2 === 0) && F < 58, bg, arrowT: cl((F - 3.5) / 4), tilt: tilt ? -tilt : 0, textW: 640 });
    // cursor
    if (F >= 55) { const [cx, cy, cl_, cr] = kf(F, L_CUR); h += L_cursor(cx, cy, cl_, cr); }
    return h;
  }

  // ---------- segment B/C: 64–96 (zoom on the send button, click, pull-out) ----------
  const L_K = 3.19;             // zoom of the tall prompt (button 75 → 239 px)
  const L_TX = [[64, 963], [65, 926], [66, 889], [67, 868.9], [68, 852.7], [69, 839.3], [70, 827.2], [71, 816.8], [72, 807.9], [73, 799.7], [74, 792.4], [75, 785], [76, 778.6], [77, 773], [78, 767.4], [79, 761.6], [80, 756.6], [81, 751.5], [82, 748.6], [83, 746.9], [84, 745.3], [85, 745], [96, 745]];
  const L_TY = [[91, 0], [92, 1.7], [93, 7.5], [94, 17.5], [95, 31.4], [96, 48.6]];
  function L_segB(F) {
    const dx = kf(F, L_TX) - 963, dy = kf(F, L_TY);
    const BW = 767, BH = 633;
    const ox = 1398 - L_K * BW + dx, oy = 770 - L_K * BH + dy;    // box origin (screen): right/bottom edge at (1398,770) on f64
    // goat behind: f63 pose zoomed about the button
    const p63 = L_photoPose(63), bcx = 1330, bcy = 640, ncx = 1640 + dx, ncy = 520 + dy;
    const gp = { s: p63.s * L_K, tx: ncx + L_K * (p63.tx - bcx), ty: ncy + L_K * (p63.ty - bcy) };
    let h = `<div class="a" style="inset:0;background:${L_SKY}"></div>` + L_goatImg(gp, 'blur(2px)');
    // fine 108px grid (×3.19)
    const gs = 108 * L_K, gx = ((ox % gs) + gs) % gs, gy = ((oy % gs) + gs) % gs;
    h += `<div class="a" style="inset:0;background-image:linear-gradient(90deg,rgba(235,240,255,.28) 1.5px,transparent 1.5px),linear-gradient(0deg,rgba(235,240,255,.28) 1.5px,transparent 1.5px);background-size:${gs}px ${gs}px;background-position:${gx + 55}px ${gy + 30}px"></div>`;
    h += L_GRAIN(.2);
    // click: button inflates (squircle) and flashes terracotta
    const pr = kf(F, [[79, 0], [80, .25], [81, .6], [82, .9], [83, 1], [84, 1], [85, .85], [86, .65], [88, .35], [90, .15], [93, 0]]);
    const col = mixHex('#000000', F < 84 ? '#D97757' : '#D97757', F < 83 ? pr * (F >= 82 ? 1 : .55) : pr);
    const infl = kf(F, [[79, 0], [80, .4], [81, .9], [82, 1], [84, 1], [86, .6], [88, .28], [90, .1], [92, 0]]);
    const bs = 75;
    const shade = "";
    const inner = L_box({ x: 0, y: 0, w: BW, h: BH, n: L_N, F: 99, btn: bs, caret: false, radius: 16, btnFill: `linear-gradient(180deg,${mixHex(col, '#000000', .15)},${col})`, btnExtra: infl ? `transform:scale(${1 + infl * .12},${1 + infl * .1});border-radius:${bs * (.24 + infl * .12)}px;` : '', shade, textW: 640, shadow: 'none' });
    // gooey bulge of the box bottom edge under the button during the press
    const bulge = infl > 0 ? `<div class="a" style="left:${BW - 23 - bs - 30}px;top:${BH - 40}px;width:${bs + 60}px;height:${40 + infl * 20}px;background:#fff;border-radius:0 0 50% 50%/0 0 100% 100%"></div>` : '';
    h += `<div class="a" style="left:0;top:0;width:${BW}px;height:${BH}px;transform-origin:0 0;transform:translate(${ox}px,${oy}px) scale(${L_K})">${bulge}${inner}</div>`;
    h += `<div class="a" style="inset:0;background:linear-gradient(180deg,rgb(224,205,212) 0,rgb(240,228,232) 150px,rgb(250,246,247) 350px,#fff 470px);mix-blend-mode:multiply"></div>`;
    // cursor
    const [cx, cy, cln, crt] = kf(F, L_CUR);
    h += L_cursor(cx, cy + (F > 91 ? dy : 0), cln, crt, F < 64.5, 1);
    // pull-out: lavender wash + blur
    const wo = kf(F, [[93, 0], [94, .35], [95, .62], [96, .78]]);
    if (wo > 0) h = `<div class="a" style="inset:0;filter:blur(${wo * 6}px)">${h}</div><div class="a" style="inset:0;background:linear-gradient(180deg,rgba(215,200,240,${wo * .75}),rgba(170,150,225,${wo * .85}))"></div>` + L_GRAIN(.25 * wo);
    return h;
  }

  // ---------- hero (monkey + drawn sport sunglasses) ----------
  // monkey.jpg 2912×4030; eyes at (1530,1110) & (2020,1340) → centre (1775,1225), eye line 25.1°
  const L_EX = 1775, L_EY = 1225;
  const L_GLASS = (() => {
    const streaks = Array.from({ length: 40 }, (_, i) => { const x = -680 + i * 34 + ((i * 53) % 17), w = 5 + ((i * 29) % 13), o = .05 + ((i * 41) % 11) / 55; return `<rect x="${x}" y="-200" width="${w}" height="460" fill="${i % 3 === 0 ? '#3a0014' : '#fff'}" opacity="${o.toFixed(3)}"/>`; }).join('');
    const lens = 'M-660 -95 C-420 -140 -150 -135 0 -118 C150 -135 420 -140 660 -95 C700 -20 690 90 610 160 C520 230 330 235 200 170 C120 128 70 70 0 64 C-70 70 -120 128 -200 170 C-330 235 -520 230 -610 160 C-690 90 -700 -20 -660 -95Z';
    const bar = 'M-706 -78 C-684 -152 -420 -182 -150 -168 C-60 -163 -22 -153 0 -151 C22 -153 60 -163 150 -168 C420 -182 684 -152 706 -78 C712 -56 694 -50 668 -74 C420 -126 150 -122 0 -106 C-150 -122 -420 -126 -668 -74 C-694 -50 -712 -56 -706 -78Z';
    return `<svg style="position:absolute;left:0;top:0;width:2912px;height:4030px;overflow:visible" viewBox="0 0 2912 4030">
      <defs>
        <linearGradient id="LlensG" x1="-660" y1="0" x2="660" y2="0" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#ffe14a"/><stop offset=".14" stop-color="#ff9a1f"/><stop offset=".32" stop-color="#ff3b2a"/><stop offset=".47" stop-color="#e5125a"/><stop offset=".56" stop-color="#ff2f45"/><stop offset=".74" stop-color="#ff7a18"/><stop offset=".9" stop-color="#ffc62e"/><stop offset="1" stop-color="#fff07a"/></linearGradient>
        <linearGradient id="LlensV" x1="0" y1="-140" x2="0" y2="235" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#ffffff" stop-opacity=".38"/><stop offset=".18" stop-color="#ffffff" stop-opacity=".06"/><stop offset=".55" stop-color="#40000f" stop-opacity=".12"/><stop offset="1" stop-color="#1c0008" stop-opacity=".62"/></linearGradient>
        <linearGradient id="LframeG" x1="0" y1="-182" x2="0" y2="-50" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#eef2f6"/><stop offset="1" stop-color="#a9b4c0"/></linearGradient>
        <clipPath id="LlensC"><path d="${lens}"/></clipPath>
        <filter id="Lgsh" x="-40%" y="-60%" width="180%" height="220%"><feGaussianBlur stdDeviation="26"/></filter>
        <filter id="Lgsh2" x="-40%" y="-60%" width="180%" height="220%"><feGaussianBlur stdDeviation="6"/></filter>
      </defs>
      <g transform="translate(${L_EX} ${L_EY}) rotate(25.1)">
        <path d="${lens}" fill="#000" opacity=".55" filter="url(#Lgsh)" transform="translate(18 58) scale(1.04)"/>
        <path d="M-760 -40 C-740 -60 -720 -72 -700 -78" fill="none" stroke="#000" stroke-width="36" opacity=".3" filter="url(#Lgsh2)" transform="translate(6 24)"/>
        <path d="M-752 -44 C-736 -62 -720 -74 -700 -80" fill="none" stroke="url(#LframeG)" stroke-width="32" stroke-linecap="round"/>
        <g clip-path="url(#LlensC)">
          <rect x="-720" y="-200" width="1440" height="460" fill="url(#LlensG)"/>
          ${streaks}
          <rect x="-720" y="-200" width="1440" height="460" fill="url(#LlensV)"/>
          <path d="M-660 -60 C-300 -110 300 -110 660 -60 L660 -20 C300 -70 -300 -70 -660 -20Z" fill="#fff" opacity=".28"/>
          <path d="M-520 150 C-380 60 -250 40 -120 60" fill="none" stroke="#fff" stroke-width="10" opacity=".35" stroke-linecap="round"/>
        </g>
        <path d="${lens}" fill="none" stroke="#2a0710" stroke-width="5" opacity=".55"/>
        <path d="M-40 66 C-24 48 24 48 40 66 L34 98 C14 88 -14 88 -34 98Z" fill="#e3e8ee" stroke="#8d99a6" stroke-width="3"/>
        <path d="${bar}" fill="url(#LframeG)" stroke="#8793a0" stroke-width="3"/>
        <path d="M-660 -150 C-420 -174 -170 -160 -60 -152" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round"/>
        <path d="M150 -160 C380 -172 600 -154 680 -118" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".8"/>
      </g></svg>`;
  })();
  // hand-traced monkey silhouette (monkey.jpg px) → soft cut-out over the ref's steel-blue sky (the ref hero is athlete-over-sky)
  const L_MKPOLY = [[-40,1740],[213,1627],[427,1547],[613,1440],[773,1333],[907,1227],[1040,1120],[1147,1013],[1227,907],[1280,800],[1387,733],[1547,699],[1733,699],[1920,720],[2107,800],[2240,893],[2347,1013],[2387,1147],[2387,1280],[2373,1387],[2400,1493],[2380,1707],[2362,1867],[2335,2133],[2295,2400],[2255,2667],[2215,2933],[2188,3200],[2148,3467],[2108,3733],[2080,4100],[-40,4100]];
  const L_MKSVG = (id) => `<svg class="a" style="left:0;top:0;width:2912px;height:4030px;overflow:visible" viewBox="0 0 2912 4030"><defs>
      <linearGradient id="Lmkfade${id}" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".34" stop-color="#fff" stop-opacity="1"/></linearGradient>
      <filter id="Lmkf${id}" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="9"/></filter>
      <mask id="Lmkm${id}" maskUnits="userSpaceOnUse" x="-100" y="0" width="3100" height="4200"><polygon points="${L_MKPOLY.map(p => p.join(',')).join(' ')}" fill="url(#Lmkfade${id})" filter="url(#Lmkf${id})"/></mask></defs>
      <image href="assets/monkey.jpg" x="0" y="0" width="2912" height="4030" mask="url(#Lmkm${id})"/></svg>`;
  let L_uid = 0;
  // hero at image scale s with the eye-centre at screen (cx,cy)
  function L_hero(s, cx, cy, extra = '', glasses = true) {
    return `<div class="a" style="left:0;top:0;width:2912px;height:4030px;transform-origin:0 0;transform:translate(${(cx - L_EX * s).toFixed(2)}px,${(cy - L_EY * s).toFixed(2)}px) scale(${s.toFixed(5)});${extra}">${L_MKSVG('h' + (L_uid++))}${glasses ? L_GLASS : ''}</div>`;
  }
  const L_HSKY = 'linear-gradient(180deg,#3b5876 0%,#4b6f8d 30%,#5d8aa6 55%,#6b99b8 78%,#75a2c4 100%)';
  // landing hero composition in page space: sharp cut-out monkey right (eyes at 1560,330 × .4), left = horizontal motion smear of the photo
  const L_HS0 = .46;
  function L_heroComp(dx, dy, blurAmt, dark) {
    const cx = 1520 + dx, cy = 335 + dy, ax = 1250 + dx;
    const mb = blurAmt > .45 ? 60 : 40;
    const trail = `<div class="a" style="inset:0;filter:url(#mbx${mb});opacity:.95;-webkit-mask-image:linear-gradient(90deg,#000 0,#000 ${48 + blurAmt * 6}%,transparent ${68 + blurAmt * 4}%);mask-image:linear-gradient(90deg,#000 0,#000 ${48 + blurAmt * 6}%,transparent ${68 + blurAmt * 4}%)"><div class="a" style="inset:0;transform-origin:${ax}px 0;transform:scaleX(${2.5 + blurAmt * .9})">${L_hero(L_HS0, cx, cy, '', true)}</div></div>`;
    const faceBlur = blurAmt > 0 ? `<div class="a" style="inset:0;filter:url(#mbx16);opacity:${blurAmt * .55};-webkit-mask-image:linear-gradient(90deg,#000 0,#000 55%,transparent 72%);mask-image:linear-gradient(90deg,#000 0,#000 55%,transparent 72%)">${L_hero(L_HS0, cx - 30, cy, '', true)}</div>` : '';
    return `<div class="a" style="inset:0;overflow:hidden;background:${L_HSKY}">${trail}
      <div class="a" style="inset:0">${L_hero(L_HS0, cx, cy)}</div>
      ${faceBlur}
      <div class="a" style="inset:0;background:linear-gradient(90deg,rgba(30,50,78,.3) 0%,rgba(30,50,78,.12) 38%,rgba(30,50,78,0) 60%),linear-gradient(180deg,rgba(24,40,64,.16),rgba(24,40,64,0) 24%,rgba(24,40,64,0) 76%,rgba(24,40,64,.2))"></div>
      ${dark ? `<div class="a" style="inset:0;background:${dark}"></div>` : ''}</div>`;
  }

  // ---------- landing page content (final layout at f160, 1920×1080) ----------
  // each element eases from its f121 position (inside the prompt box) to final with global progress p
  const L_PT = [[121, 0], [122, .03], [123, .06], [124, .095], [125, .128], [126, .21], [127, .29], [128, .369], [129, .432], [130, .49], [131, .538], [132, .581], [133, .62], [134, .655], [135, .687], [136, .715], [137, .741], [138, .763], [139, .786], [140, .806], [141, .825], [142, .842], [143, .858], [144, .872], [145, .886], [146, .897], [147, .908], [148, .92], [149, .931], [150, .94], [151, .948], [152, .955], [153, .963], [154, .97], [155, .976], [156, .981], [157, .985], [158, .991], [159, .994], [160, .998], [161, 1]];
  const L_H1 = 'Smile Harder. Selfie', L_H2 = 'Smarter, Week by Week';
  const L_HN1 = [[122, 0], [123, 1], [124, 2], [125, 3], [126, 4], [127, 6], [128, 7], [129, 9], [130, 10], [131, 11], [132, 11.5], [133, 12], [135, 14], [136, 14], [138, 15], [140, 16], [142, 17], [144, 17], [146, 18], [150, 19], [156, 19.5], [158, 20]];
  const L_HN2 = [[122, 0], [123, 1], [124, 2], [125, 3], [126, 4], [127, 6], [128, 8], [129, 9], [130, 10], [131, 11], [132, 12], [133, 13], [135, 13.5], [136, 15], [138, 16], [140, 16], [144, 18], [146, 19], [150, 19], [152, 20], [158, 21]];
  const L_SUB = 'Monke tracks grins, bananas, selfies and naps—then turns every photo into clear, motivating progress you’ll actually feel.';
  const L_SN = [[124, 0], [125, 16], [127, 36], [130, 57], [135, 82], [140, 100], [150, 112], [160, 118], [172, 130]];
  const L_FE = ['Grin zones (Z1–Z5 time & trends)', 'Banana scores (coach-ready)', 'Auto-sync from any camera you steal'];
  const L_FN = [[125, 0], [127, 10], [130, 16], [135, 23], [140, 26], [150, 31], [160, 34], [172, 40]];
  const L_typed = (s, n) => L_esc(s.slice(0, Math.max(0, Math.floor(n))));
  const L_ICONS = [
    '<svg width="22" height="16" viewBox="0 0 22 16"><path d="M1 14 L8 7 L12 11 L20 3 M15 3 H20 V8" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    '<svg width="18" height="18" viewBox="0 0 18 18"><path d="M2 17V9 M7 17V4 M12 17V7 M16 17V1" stroke="currentColor" stroke-width="3"/></svg>',
    '<svg width="22" height="14" viewBox="0 0 22 14"><path d="M5 13 H17 A4 4 0 0 0 17 5 A6 6 0 0 0 6 4 A4.5 4.5 0 0 0 5 13Z" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'];
  function L_pageContent(F, p) {
    const q = 1 - p;
    const at = (sx, sy, x, y) => `left:${x + sx * q}px;top:${y + sy * q}px`;
    let h = '';
    // header
    h += `<div class="a" style="${at(537, 223, 108, 58)};font:700 37px/44px Inter;color:#fff;letter-spacing:-.2px">Monke</div>`;
    h += `<div class="a row" style="${at(54, 86, 727, 83)};font:600 23.3px/28px Inter;color:#fff;gap:0;white-space:nowrap"><span style="position:absolute;left:0">Features</span><span style="position:absolute;left:143px">Pricing</span><span style="position:absolute;left:267px">FAQ</span><span style="position:absolute;left:368px">Download</span></div>`;
    h += `<div class="a" style="${at(-529, 215, 1481, 68)};width:336px;height:53px;border:1.5px solid rgba(255,255,255,.62);border-radius:27px;font:500 20px/50px Inter;color:#fff;text-align:center;letter-spacing:-.3px;white-space:nowrap">${L_TXT.pill}</div>`;
    // hero copy
    const n1 = kf(F, L_HN1), n2 = kf(F, L_HN2);
    h += `<div class="a" style="${at(525, 88, 107, 290)};font:700 63.4px/60px Inter;color:#fff;letter-spacing:0;white-space:pre">${L_typed(L_H1, n1)}\n${L_typed(L_H2, n2)}</div>`;
    const sn = Math.floor(kf(F, L_SN));
    const subA = L_SUB.slice(0, Math.max(0, sn - 12)), subB = L_SUB.slice(Math.max(0, sn - 12), sn);
    h += `<div class="a" style="${at(523, 86, 107, 449)};width:505px;font:600 23.3px/30px Inter;color:#fff;letter-spacing:0">${L_esc(subA)}<span style="color:rgba(255,255,255,.62)">${L_esc(subB)}</span></div>`;
    const cs = lerp(.88, 1, p);
    h += `<div class="a" style="${at(537, 53, 108, 562)};width:249px;height:76px;transform-origin:0 0;transform:scale(${cs});background:#fff;border-radius:38px;font:700 23.4px/76px Inter;color:#111;text-align:center;letter-spacing:0">Get the Banana</div>`;
    const fn = kf(F, L_FN);
    L_FE.forEach((t, i) => { h += `<div class="a row" style="${at(532, 50, 108, 655 + i * 43.5)};font:500 20px/24px Inter;color:rgba(255,255,255,.55);white-space:nowrap;gap:12px"><span style="display:inline-flex;width:24px;justify-content:center;color:rgba(255,255,255,.6)">${L_ICONS[i]}</span>${L_typed(t, fn)}</div>`; });
    // logo row (muted wordmarks)
    const lw = (t, x, st) => `<div class="a" style="${at(620, -353, x, 948)};font:${st};color:rgba(255,255,255,.52);white-space:nowrap">${t}</div>`;
    h += lw(L_TXT.logos[0], 96, "800 23px/34px Inter;letter-spacing:.5px");
    h += lw(L_TXT.logos[1], 270, "800 25px/34px Poppins;letter-spacing:1.5px");
    h += lw(L_TXT.logos[2], 480, "500 25px/34px Inter;letter-spacing:2.5px");
    return h;
  }

  // ---------- segment D: 97–120 (wide: prompt over the hero, box greys, glass morph begins) ----------
  const L_BTOP = [[97, 60], [98, 91], [99, 118], [100, 141], [101, 161], [102, 178], [103, 192], [104, 205], [105, 215], [106, 224], [107, 231], [108, 237], [109, 241], [110, 243], [112, 245], [121, 245]];
  // background hero pose (monkey eye-centre and scale): zooms ~1.1 %/frame, drifts down-left
  function L_bgHeroPose(F) { const s = .25 * Math.pow(1.0114, F - 100); return { s, cx: 1450 + (F - 100) * -3.2, cy: 215 + (F - 100) * 5.6 }; }
  function L_bgHero(F) {
    const hp = L_bgHeroPose(F);
    const fade = '-webkit-mask-image:linear-gradient(180deg,#000 62%,transparent 92%);mask-image:linear-gradient(180deg,#000 62%,transparent 92%);';
    const ax = hp.cx - 560 * hp.s / .4;
    return `<div class="a" style="inset:0;background:linear-gradient(180deg,#2a426e 0%,#3c5f8a 28%,#5278a5 56%,#6c8ab6 83%,#7d92bc 100%)"></div>
      <div class="a" style="inset:0;-webkit-mask-image:linear-gradient(90deg,#000 0,#000 ${ax - 40}px,transparent ${ax + 60}px);mask-image:linear-gradient(90deg,#000 0,#000 ${ax - 40}px,transparent ${ax + 60}px)"><div class="a" style="inset:0;transform-origin:${ax}px 0;transform:scaleX(2.6);filter:url(#mbx40);opacity:.8">${L_hero(hp.s, hp.cx, hp.cy, fade, false)}</div></div>
      ${L_hero(hp.s, hp.cx, hp.cy, fade)}`;
  }
  function L_segD(F) {
    let h = L_bgHero(F);
    // fine grid 137×84
    h += `<div class="a" style="inset:0;background-image:linear-gradient(90deg,rgba(235,240,255,.22) 1.5px,transparent 1.5px),linear-gradient(0deg,rgba(235,240,255,.22) 1.5px,transparent 1.5px);background-size:137px 84px;background-position:0 -5px;opacity:${kf(F, [[97, 1], [106, .8], [110, 0]])}"></div>`;
    const lav = kf(F, [[97, 1], [98, .72], [99, .52], [100, .38], [103, .22], [106, .1], [108, 0]]);
    if (lav > 0) h += `<div class="a" style="inset:0;background:linear-gradient(180deg,rgba(185,175,235,${lav * .35}) 0%,rgba(180,168,238,${lav * .45}) 50%,rgba(182,165,245,${lav * .62}) 100%)"></div><div class="a" style="left:0;top:${540 + (1 - lav) * 300}px;width:1920px;height:600px;background-image:radial-gradient(rgba(235,230,255,.55) 1.1px,transparent 1.5px);background-size:8px 8px;-webkit-mask-image:linear-gradient(180deg,transparent,#000 40%);mask-image:linear-gradient(180deg,transparent,#000 40%);opacity:${lav}"></div>`;
    h += L_GRAIN(.14);
    const top = kf(F, L_BTOP), BW = 763, BH = 596;
    // box surface: white → grey (107–112) → dark with a cyan band sweeping up (113–120)
    const g = kf(F, [[106, 0], [108, .5], [110, 1]]);
    const d = kf(F, [[111, 0], [114, .5], [117, 1], [121, 1]]);
    const band = kf(F, [[112, -.12], [113, 0], [115, .08], [116, .15], [117, .25], [118, .38], [119, .5], [121, .62]]);   // cyan band sweeps down from the top
    const bp = v => (v * 100).toFixed(1) + '%';
    let bg = `linear-gradient(180deg,rgba(255,255,255,.97),rgba(247,244,250,.97))`;
    if (g > 0) bg = `linear-gradient(180deg,rgba(${lerp(250, 200, g)},${lerp(248, 200, g)},${lerp(252, 204, g)},.97),rgba(${lerp(245, 160, g)},${lerp(245, 160, g)},${lerp(248, 164, g)},.97))`;
    if (d > 0) bg = `linear-gradient(180deg,rgba(255,255,255,${d}) 0%,rgba(250,254,255,${d}) ${bp(band - .1)},rgba(150,232,255,${d}) ${bp(band - .02)},rgba(120,190,225,${d}) ${bp(band + .04)},rgba(120,122,128,${d}) ${bp(band + .14)},rgba(40,40,44,${d}) ${bp(band + .5)},rgba(8,8,10,${d}) 100%),${bg}`;
    // text wiped out from the top by the band
    const tm = d > 0 ? `linear-gradient(180deg,transparent 0,transparent ${bp(band - .05)},rgba(0,0,0,.5) ${bp(band)},#000 ${bp(band + .08)})` : null;
    const txtCol = false;
    const btnF = '#000';
    const bxOp = kf(F, [[118, 1], [120, .0]]);
    h += L_box({ x: 576, y: top, w: BW, h: BH, n: L_N, F: 99, btn: 75, caret: false, bg, textMask: tm, textOp: kf(F, [[116, 1], [119, .6], [120, 0]]), btnFill: btnF, label: true, labelOp: bxOp, padT: 27, textW: 640, shadow: '0 16px 50px rgba(15,25,60,.18)' }).replace('color:#121212', txtCol ? 'color:#e8eef8' : 'color:#121212');
    if (F >= 120) h += L_segE(F, true);
    return h;
  }

  // ---------- segment E/F: 119–160 (card = glass page morph; page content slides into place) ----------
  const L_CARD = [[119, [576, 245, 1339, 841]], [121, [573, 243, 1341, 842]], [123, [520, 225, 1395, 870]], [125, [433, 183, 1485, 905]], [127, [290, 122, 1620, 964]], [130, [166, 72, 1746, 1018]], [135, [66, 28, 1846, 1060]], [140, [18, 6, 1898, 1076]], [145, [0, 0, 1920, 1080]]];
  function L_segE(F, onlyCard) {
    const p = kf(F, L_PT);
    let h = onlyCard ? '' : L_bgHero(F);
    if (!onlyCard) {
      const asc = kf(F, [[121, 0], [123, .8], [126, 1], [133, .8], [140, 0]]);
      h += L_ascii(asc, 'linear-gradient(90deg,#000 0,rgba(0,0,0,.9) 22%,rgba(0,0,0,.25) 40%,rgba(0,0,0,.25) 62%,rgba(0,0,0,.9) 80%,#000 100%)');
      h += L_GRAIN(.12);
    }
    const c = kf(F, L_CARD, E.lin);
    const cw = c[2] - c[0], ch = c[3] - c[1];
    const r = kf(F, [[121, 18], [140, 24], [145, 0]]);
    // card fill: 120–121 opaque glass (white/cyan/steel), then dark veil at top → cyan band → white, band sweeping down and out
    const band = kf(F, [[122, .22], [123, .38], [124, .46], [125, .56], [126, .64], [127, .72], [130, .88], [135, 1.0], [140, 1.12], [145, 1.35]]);
    const white = kf(F, [[122, 1], [135, .9], [140, .45], [145, 0]]);
    const veil = kf(F, [[121.5, .5], [123, .93], [127, .9], [130, .78], [135, .58], [140, .4], [145, .26], [150, .14], [155, .06], [160, 0]]);
    const bp = v => (v * 100).toFixed(1) + '%';
    let fill = `linear-gradient(180deg,rgba(6,8,12,${veil}) 0%,rgba(10,14,22,${veil * .92}) ${bp(band - .2)},rgba(50,110,165,${.85 * white}) ${bp(band - .07)},rgba(165,236,255,${white}) ${bp(band)},rgba(255,255,255,${white}) ${bp(band + .1)},rgba(255,255,255,${white}) 100%)`;
    const g0 = `linear-gradient(180deg,#fbfdff 0%,#ffffff 35%,#b0eaff 50%,#6aa6cf 72%,#4a78a4 100%)`, g1 = `linear-gradient(180deg,#6ea6dc 0%,#bfeeff 14%,#ffffff 30%,#ffffff 58%,#b8ecff 72%,#5d93c2 92%,#4b7aa8 100%)`;
    const heroOp = kf(F, [[121.5, 0], [123, .35], [127, .8], [130, 1]]);
    const glass = F < 122 ? `<div class="a" style="inset:0;background:${g0}"></div><div class="a" style="inset:0;background:${g1};opacity:${kf(F, [[120, 0], [121, 1]])}"></div><div class="a" style="inset:0;background:${fill};opacity:${kf(F, [[121, 0], [122, 1]])}"></div>` : `<div class="a" style="inset:0;background:${fill}"></div>`;
    const content = `<div class="a" style="left:${-c[0]}px;top:${-c[1]}px;width:1920px;height:1080px">
        <div class="a" style="inset:0;opacity:${heroOp}">${L_heroComp(-500 * (1 - p), 100 * (1 - p), 0, null)}</div>
        <div class="a" style="inset:0;background:linear-gradient(90deg,rgba(10,20,40,${veil * .25}),rgba(10,20,40,0) 60%)"></div>
      </div>
      ${glass}
      <div class="a" style="left:${-c[0]}px;top:${-c[1]}px;width:1920px;height:1080px;opacity:${kf(F, [[120.2, 0], [121, 1]])}">${L_pageContent(F, p)}</div>`;
    h += `<div class="a" style="left:${c[0]}px;top:${c[1]}px;width:${cw}px;height:${ch}px;border-radius:${r}px;overflow:hidden;box-shadow:0 20px 60px rgba(0,10,30,.25)">${content}</div>`;
    // the nav sits outside the card early (above the box), draw it unclipped until the card covers it
    if (F < 131) {
      const q = 1 - p;
      h += `<div class="a" style="left:${727 + 54 * q}px;top:${83 + 86 * q}px;font:600 23.3px/28px Inter;color:#fff;white-space:nowrap;opacity:${kf(F, [[120.2, 0], [121, 1]])};width:520px;height:30px"><span style="position:absolute;left:0">Features</span><span style="position:absolute;left:143px">Pricing</span><span style="position:absolute;left:267px">FAQ</span><span style="position:absolute;left:368px">Download</span></div>`;
    }
    // leftover send arrow fading (121)
    if (F < 123) h += `<svg class="a" style="left:${1264}px;top:${778}px;width:36px;height:40px;opacity:${kf(F, [[119, 1], [123, 0]])}" viewBox="0 0 20 26"><path d="M10 25 V2 M1.5 10.5 L10 2 L18.5 10.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/></svg>`;
    return h;
  }

  // ---------- segment G: 161–225 (pull back to a card on #ddd) ----------
  const L_CW = [[160, 1920], [162, 1920], [164, 1915], [165, 1904], [166, 1887], [167, 1865], [168, 1836], [169, 1788], [170, 1746], [171, 1704], [172, 1668], [173, 1634], [174, 1606], [175, 1581], [176, 1559], [177, 1540], [178, 1522], [179, 1506], [180, 1492], [182, 1468], [184, 1448], [186, 1430], [188, 1416], [190, 1404], [192, 1392], [194, 1384], [196, 1376], [198, 1368], [200, 1362], [202, 1358], [204, 1354], [206, 1350], [208, 1348], [210, 1346], [212, 1345], [214, 1344]];
  function L_segG(F) {
    const s = kf(F, L_CW) / 1920;
    const blurAmt = kf(F, [[163, 0], [170, .45], [177, .9], [182, 1]]);
    const hdx = kf(F, [[160, 0], [175, -12], [190, -24], [210, -30]]), hdy = kf(F, [[160, 0], [190, 16], [210, 17]]);
    const inner = `${L_heroComp(hdx, hdy, blurAmt, null)}<div class="a" style="inset:0">${L_pageContent(F, 1)}</div>`;
    return `<div class="a" style="inset:0;background:#dddddd"></div>
      <div class="a" style="left:0;top:0;width:1920px;height:1080px;transform-origin:960px 540px;transform:scale(${s});overflow:hidden">${inner}</div>`;
  }

  function L_render(F) {
    if (F >= 225) return '<div class="a" style="inset:0;background:#000"></div>';
    if (F < 64) return L_segA(F);
    if (F < 97) return L_segB(F);
    if (F < 121) return L_segD(F);
    if (F <= 160) return L_segE(F, false);
    return L_segG(F);
  }
  SHOT({ id: 'L', f0: 0, f1: 225, render: (lf, F) => L_render(F) });
})();
