/* shots/A.js — Builder A · S1 f0–71 · Frame by Frame hub header rise → Whop hub window → cursor hover + zoom + press.
   Authored in the reference's 720-px space inside a root scaled ×1.5 (so every SPEC number is used as-is).
   Everything is a continuous function of F (fractional frames OK). Helpers are prefixed A_. */
(function () {
  const S1 = 1.5;
  // ---------- measured tables (SPEC §2.1 / measure/tables.json), 720-px space ----------
  // header centre y, f0..f37 (disc blob f0–f4, header after), then 357 flat
  const A_CY = [621.3, 554.4, 516.5, 490.2, 470.7, 454.5, 440.5, 429.5, 419.5, 411.5, 404.5, 399.0, 393.5, 389.5, 385.0, 381.5,
    378.5, 376.0, 373.5, 371.0, 369.0, 367.5, 366.0, 365.0, 363.5, 362.5, 361.5, 360.5, 360.0, 359.5, 359.0, 358.5, 358.0, 358.0, 358.0, 357.5, 357.5, 357.0];
  // pill x0 slide f5..f24 (596 → 586)
  const A_PILLX = [596, 593, 592, 591, 590, 590, 589, 589, 588, 588, 588, 588, 588, 587, 587, 587, 587, 587, 586, 586];
  // header blur σ f5..f19 (iso)
  const A_HBLUR = [1.89, 1.52, 1.22, 1.04, 0.88, 0.77, 0.64, 0.55, 0.49, 0.41, 0.38, 0.29, 0.26, 0.26, 0.2];
  // window opacity f14..f24
  const A_WIN = [0, 0.53, 0.655, 0.663, 0.66, 0.70, 0.772, 0.852, 0.908, 0.973, 1.0];
  // camera scale (from word right edge), smoothed, f44..f71; pivot (359.5, 361.7)
  const A_CAM = [1.0, 1.003, 1.008, 1.016, 1.019, 1.021, 1.031, 1.037, 1.052, 1.073, 1.12, 1.157, 1.173, 1.183, 1.189, 1.194, 1.199, 1.199,
    1.196, 1.194, 1.188, 1.183, 1.173, 1.157, 1.141, 1.12, 1.089, 1.037];
  // cursor tip f27..f71 (screen space). f52–f55 = eye reads of the motion streak (SPEC: not measurable)
  const A_TIP = [[594, 262], [577, 260], [565, 258], [556, 256], [549, 255], [543, 254], [538, 253], [533, 251], [530, 251], [526, 250], [523, 249],
    [521, 249], [519, 248], [518, 249], [516, 249], [515, 250], [514, 252], [513, 255], [513, 258], [513, 263], [513, 270], [515, 278], [518, 288],
    [523, 299], [529, 309], [522, 334], [498, 358], [468, 375], [440, 381], [419, 376], [406, 372], [398, 368], [391, 364], [386, 361], [383, 358],
    [380, 356], [377, 355], [376, 353], [374, 353], [373, 352], [373, 352], [372, 352], [372, 352], [371, 353], [370, 354]];
  // cursor extra rotation (deg, CSS sense) f27..f71: faces travel f46–f55, back to rest pose f56
  const A_ROT = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -6, -22, -40, -46, -47, -48, -54, -62, -68, -40, -12, -2, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

  // Catmull-Rom through per-frame samples (smooth, continuous in F)
  function A_cr(F, f0, arr) {
    const n = arr.length, i = F - f0;
    if (i <= 0) return arr[0]; if (i >= n - 1) return arr[n - 1];
    const k = Math.floor(i), t = i - k, g = j => arr[Math.max(0, Math.min(n - 1, j))];
    const p0 = g(k - 1), p1 = g(k), p2 = g(k + 1), p3 = g(k + 2);
    const f = (a, b, c, d) => 0.5 * ((2 * b) + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t * t + (-a + 3 * b - 3 * c + d) * t * t * t);
    return Array.isArray(p1) ? p1.map((_, j) => f(p0[j], p1[j], p2[j], p3[j])) : f(p0, p1, p2, p3);
  }
  const A_cy = F => F <= 0 ? 621.3 + (621.3 - 554.4) * 0.6 * Math.min(1, -F) : A_cr(F, 0, A_CY);

  // S1 page background (table S1_bg), top/mid colour per frame f0..f28
  const A_BGTOP = ['#B7CFEB', '#B5CDE7', '#B7CCE7', '#BAD0E8', '#C0D2EA', '#C5D5EC', '#CADAEA', '#D0DDED', '#D4E0EE', '#DAE4F0', '#DDE7F1', '#E1EAF3',
    '#E3ECF3', '#E8ECF5', '#EBF0F4', '#EEF1F6', '#EFF3F6', '#F2F3F7', '#F4F5F7', '#F5F6F8', '#F6F7F9', '#F8F8F8', '#F9F9F9', '#F9F9F9', '#FAFAFA',
    '#FAFAF8', '#FCFCFA', '#FCFCFA', '#FDFDFB'];
  const A_BGBOT = ['#CBE0F8', '#CFE4F9', '#D4E6FA', '#D6E8FB', '#D8EAFE', '#D9ECFB', '#D9ECFB', '#DAEDFC', '#DBECFC', '#DBECFC', '#DBECFC', '#DCEEFD'];
  function A_hexAt(F, arr) { const i = cl(F, 0, arr.length - 1), k = Math.min(arr.length - 2, Math.floor(i)); return mixHex(arr[k], arr[k + 1], i - k); }

  // lockup fit: "Frame by Frame" + "on Whop" pill scaled together so the pill's right edge sits where the ref pill ends (x 709)
  let A_fitC = null;
  function A_fit() {
    if (A_fitC) return A_fitC;
    const m = (txt, font, ls) => { const s = document.createElement('span'); s.style.cssText = `position:absolute;visibility:hidden;white-space:pre;font:${font};letter-spacing:${ls}`; s.textContent = txt; document.body.appendChild(s); const w = s.getBoundingClientRect().width; s.remove(); return w; };
    const w42 = m('Frame by Frame', '500 42px Inter', '-0.01em');
    const p21 = m('on Whop', '500 21px Inter', '0');
    const pillW = p21 + 32, gap = 28;
    const k = Math.min(1, (709 - 434) / (w42 + gap + pillW));
    A_fitC = { k, w42, p21, pillW, gap };
    return A_fitC;
  }

  // macOS-style arrow (symmetric head + tail, axis tilted like the ref). Tip at local (0,0). units = 720 px at scale 1.
  const A_ARROW = 'M0 0 L10.3 20.4 L2.6 17 L2.6 27.2 L-2.6 27.2 L-2.6 17 L-10.3 20.4 Z';
  function A_cursor(x, y, sc, rot, blx, bly, op) {
    const fid = 'A_cb';
    const f = (blx > 0.15 || bly > 0.15) ? `<filter id="${fid}" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="${blx.toFixed(2)} ${bly.toFixed(2)}"/></filter>` : '';
    return `<svg class="a" style="left:${x - 40}px;top:${y - 40}px;width:80px;height:80px;overflow:visible;opacity:${op}" viewBox="-40 -40 80 80">
      <defs>${f}</defs>
      <g ${f ? `filter="url(#${fid})"` : ''}><g transform="scale(${sc}) rotate(${-29 + rot})">
        <path d="${A_ARROW}" fill="rgba(0,0,0,.18)" transform="translate(0.5,1.2)" style="filter:blur(0.8px)"/>
        <path d="${A_ARROW}" fill="#050505" stroke="#fff" stroke-width="1.5" stroke-linejoin="round" paint-order="stroke"/>
      </g></g></svg>`;
  }

  // ---------- the hub window + header (world layer; y is shifted by the rise) ----------
  function A_world(F) {
    const cy = A_cy(F), dy = cy - 357;
    // page background
    const t = cl(F / 28), top = A_hexAt(F, A_BGTOP), bot = A_hexAt(F, A_BGBOT);
    const y540 = mixHex(top, bot, lerp(0.1, 0.55, t));
    let h = `<div class="a" style="left:-60px;top:-60px;width:840px;height:840px;background:linear-gradient(180deg,${top} 0%,${top} 50%,${y540} 72.5%,${bot} 90%,${bot} 100%)"></div>`;

    // window (opacity from table) — Whop hub panel
    const wa = F < 14 ? 0 : A_cr(F, 14, A_WIN);
    // rising light band inside the window (measured: centre rel. to window top 460→22 over f15→f40)
    const bandRel = kf(F, [[14, 520], [17, 361], [20, 228], [24, 113], [28, 52], [32, 29], [40, 22]], E.lin);
    const bandA = kf(F, [[14, .7], [18, 1], [28, 1], [32, .7], [36, .45], [42, .32]]);
    let win = '';
    if (wa > 0.001) {
      const icoC = (c, a, top, kind, sz) => `<div class="a" style="left:${359 - 272 - sz / 2}px;top:${top - 270 - sz / 2}px;width:${sz}px;height:${sz}px;opacity:${a}">${kind(c)}</div>`;
      const I = {
        courses: c => `<svg viewBox="0 0 20 20" width="100%" height="100%"><path d="M1.8 6.6 10 3.2l8.2 3.4L10 10z" fill="${c}"/><path d="M5 8.6v4.6c3 2.1 7 2.1 10 0V8.6L10 10.8z" fill="${c}" opacity=".75"/><path d="M18.2 6.6v5" stroke="${c}" stroke-width="1.4" stroke-linecap="round"/></svg>`,
        chat: c => `<svg viewBox="0 0 20 20" width="100%" height="100%"><path d="M4.5 3.5h11a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H9.5l-3.6 2.8v-2.8H4.5a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2z" fill="${c}"/><path d="M6.5 7.6h7M6.5 10.4h4.5" stroke="#fff" stroke-width="1.3" stroke-linecap="round" opacity=".9"/></svg>`,
        content: c => `<svg viewBox="0 0 20 20" width="100%" height="100%"><rect x="4" y="2.5" width="12" height="15" rx="2.4" fill="${c}"/><path d="M7 7h6M7 10h6M7 13h4" stroke="#fff" stroke-width="1.3" stroke-linecap="round"/></svg>`,
      };
      const card = `<div class="a" style="left:${509 - 272}px;top:${467 - 270}px;width:420px;height:420px;background:#FFFFFF;border-radius:9px;box-shadow:0 0 0 1px rgba(214,224,236,.9),0 6px 18px rgba(70,110,160,.06);overflow:hidden">
          <div class="a" style="left:19px;top:20.5px;width:40px;height:40px;border-radius:9px;background:linear-gradient(160deg,#79AEE6 0%,#4C83CB 100%);display:flex;align-items:center;justify-content:center">
            <div style="width:24px;height:24px">${I.courses('#fff')}</div></div>
          <div class="a" style="left:71px;top:14.5px;white-space:nowrap;font:500 20px/1 Inter;letter-spacing:-0.01em;color:#2E343B">Remake any launch video</div>
          <div class="a" style="left:71px;top:42.5px;white-space:nowrap;font:400 14px/1 Inter;color:#AEB7C0">Course <span style="opacity:.7">·</span> 8 lessons</div>
          <div class="a" style="left:0;top:${544 - 467}px;width:420px;height:236px;background:url(assets/cover-2.png) 0 0/420px 236px no-repeat"></div>
        </div>`;
      const search = `<div class="a" style="left:${440 - 272}px;top:${280 - 270}px;width:214px;height:23px;border-radius:7px;background:rgba(20,40,70,.045);box-shadow:inset 0 0 0 .75px rgba(20,40,70,.05);display:flex;align-items:center;padding:0 7px;gap:5px;font:500 10px/1 Inter;color:rgba(0,0,0,.45);white-space:nowrap">
          <svg width="10" height="10" viewBox="0 0 20 20"><circle cx="8.5" cy="8.5" r="5.8" fill="none" stroke="rgba(0,0,0,.42)" stroke-width="2.2"/><path d="M13 13l4.5 4.5" stroke="rgba(0,0,0,.42)" stroke-width="2.2" stroke-linecap="round"/></svg>
          <span>Search Frame by Frame</span><span style="margin-left:auto;font:500 8.5px/1 Inter;color:rgba(0,0,0,.38);background:rgba(255,255,255,.8);border-radius:4px;padding:2.5px 4px">⌘K</span></div>`;
      const fa = cl((F - 15.2) / 3.2);                              // window body/edge arrives just after its contents (ref f15: body still invisible)
      win = `<div class="a" style="left:272px;top:${270 + dy}px;width:640px;height:720px;border-radius:62px;opacity:${wa};overflow:hidden">
          <div class="a" style="inset:0;border-radius:62px;opacity:${E.outQ(fa)};background:linear-gradient(180deg,#EDF3FF 0px,#F8FAFF 14px,#FEFEFF 50px,#FCFDFF 160px,#F6FAFE 220px,#EFF8FF 250px,#E7F3FF 310px,#E1F1FE 370px,#DDEEFE 430px,#DDEEFE 720px);
          box-shadow:inset 0 0 0 1px rgba(226,233,242,.95),inset 0 1.5px 0 rgba(255,255,255,.9)"></div>
          <div class="a" style="left:0;right:0;top:${bandRel - 70}px;height:140px;opacity:${bandA * fa};background:linear-gradient(180deg,rgba(196,221,254,0) 0%,rgba(196,221,254,.85) 50%,rgba(196,221,254,0) 100%)"></div>
          <div class="a" style="left:0;width:640px;top:${448 - 24.5 - 270}px;height:1px;background:rgba(190,205,222,.55);opacity:${kf(F, [[15, .9], [18, .6], [24, 0]])}"></div>
          <div class="a" style="left:${444 - 272}px;width:1px;top:${448 - 24.5 - 270}px;height:400px;background:rgba(190,205,222,.55);opacity:${kf(F, [[15, .9], [18, .6], [24, 0]])}"></div>
          ${search}
          ${icoC('#868B93', 1, 492, I.courses, 38)}
          ${icoC('#BAC6D3', .9, 602, I.chat, 40)}
          ${icoC('#C9D4DF', .55, 712, I.content, 38)}
          ${card}
        </div>`;
    }

    // header group
    const fit = A_fit(), k = fit.k;
    const hb = F < 5 ? lerp(3.2, 1.89, cl(F / 5)) : F < 19 ? A_cr(F, 5, A_HBLUR) : 0.2 * cl(1 - (F - 19) / 4);
    const v = Math.abs(A_cy(F - 0.5) - A_cy(F + 0.5));             // px/frame rise speed
    const sy = Math.sqrt(hb * hb + Math.pow(0.2 * v, 2)), sx = hb;
    const hdrF = (sx > 0.12 || sy > 0.12) ? `<filter id="A_hb" x="-30%" y="-80%" width="160%" height="260%"><feGaussianBlur stdDeviation="${sx.toFixed(2)} ${sy.toFixed(2)}"/></filter>` : '';
    const pillX0 = F < 5 ? 596 + (5 - F) * 2.5 : A_cr(F, 5, A_PILLX);
    const pillSlide = (pillX0 - 586) * k;                          // measured slide, scaled with the lockup
    const wordA = cl((F - 1.3) / 1.2), pillA = cl((F - 3.0) / 1.4);
    const pillB = F < 4 ? 5 : Math.max(0, lerp(4.5, 0, cl((F - 4) / 6)));
    const fs = 42 * k, wordW = fit.w42 * k, gap = fit.gap * k, pw = fit.pillW * k, ph = 47 * k;
    const wordTop = 357 - 0.37 * fs - 0.35 * fs;                     // centre the cap height on the header line
    const disc = `<div class="a" style="left:316px;top:313px">${ffDisc(88)}</div>`;
    // hover ring (FF ice) from f53, expands 44→58 px radius, fades in
    const rA = cl((F - 52.6) / 3.5), rR = lerp(47, 58, E.outC(cl((F - 53) / 5)));
    const ring = rA > 0 ? `<div class="a" style="left:${360 - rR}px;top:${357 - rR}px;width:${2 * rR}px;height:${2 * rR}px;border-radius:50%;opacity:${rA};
        background:radial-gradient(circle closest-side,rgba(200,228,250,0) ${(43 / rR * 100).toFixed(1)}%,#BFE0F8 ${(45.5 / rR * 100).toFixed(1)}%,#D3E9FA ${(49 / rR * 100).toFixed(1)}%,${FF.ice} ${(53 / rR * 100).toFixed(1)}%,rgba(240,247,253,.75) 92%,rgba(246,251,255,0) 100%)"></div>` : '';
    const word = `<div class="a" style="left:434px;top:${wordTop}px;opacity:${wordA};white-space:nowrap;font:500 ${fs}px/1 Inter;letter-spacing:-0.01em;color:#0A0A0B">Frame by Frame</div>`;
    const pill = `<div class="a" style="left:${434 + wordW + gap + pillSlide}px;top:${359.5 - ph / 2}px;width:${pw}px;height:${ph}px;border-radius:${ph / 2}px;opacity:${pillA};
        ${pillB > 0.05 ? `filter:blur(${pillB.toFixed(2)}px);` : ''}background:linear-gradient(180deg,#434344 0%,#2F2E2F 12%,#2A292A 100%);display:flex;align-items:center;justify-content:center;
        font:500 ${21 * k}px/1 Inter;color:#FEFDFE;white-space:nowrap">on Whop</div>`;
    const hdr = `<svg width="0" height="0" class="a"><defs>${hdrF}</defs></svg>
      <div class="a" style="left:0;top:${dy}px;width:720px;height:720px;${hdrF ? 'filter:url(#A_hb);' : ''}">${ring}${disc}${word}${pill}</div>`;
    return h + win + hdr;
  }

  // camera scale about the logo centre
  function A_cam(F) {
    if (F < 44) return F < 18 ? lerp(1.021, 1.0, E.outQ(cl((F - 3) / 15))) + (F < 3 ? (3 - F) * 0.003 : 0) : 1.0;
    return A_cr(F, 44, A_CAM);
  }

  SHOT({
    id: 'A', f0: 0, f1: 71,
    render(lf, F) {
      const s = A_cam(F), ox = 359.5, oy = 361.7;
      const world = A_world(F);
      // zoom motion blur: average N copies across one frame of camera travel (only when the zoom is moving)
      const ds = Math.abs(A_cam(F) - A_cam(F - 1));
      const N = ds > 0.03 ? 14 : ds > 0.012 ? 10 : ds > 0.004 ? 5 : 1;
      const cb = N > 1 ? Math.min(0.9, ds * 12) : 0;
      let layers = '';
      for (let j = 0; j < N; j++) {
        const sj = N === 1 ? s : lerp(A_cam(F - 0.9), s, j / (N - 1));
        layers += `<div class="a" style="inset:0;transform-origin:${ox}px ${oy}px;transform:scale(${sj});opacity:${(1 / (j + 1)).toFixed(4)}${cb > 0.05 ? `;filter:blur(${cb.toFixed(2)}px)` : ''}">${world}</div>`;
      }
      // cursor (screen space)
      let cur = '';
      if (F >= 26.4) {
        const tip = A_cr(F, 27, A_TIP), rot = A_cr(F, 27, A_ROT);
        const p0 = A_cr(F - 0.5, 27, A_TIP), p1 = A_cr(F + 0.5, 27, A_TIP);
        const vx = p1[0] - p0[0], vy = p1[1] - p0[1];
        const grow = lerp(1, 1.57, E.ioS(cl((F - 52.5) / 7.5)));
        const press = lerp(1, 0.855, E.ioS(cl((F - 68.6) / 2.4)));
        const sc = 1.1 * grow * press * (F >= 44 ? s : 1);
        const op = F < 27 ? cl((F - 26.4) / 0.6) : 1;
        cur = A_cursor(tip[0], tip[1], sc, rot, 0.28 * Math.abs(vx), 0.28 * Math.abs(vy), op);
      }
      return `<div class="a" style="left:0;top:0;width:720px;height:720px;transform-origin:0 0;transform:scale(${S1});overflow:hidden;background:#FDFDFB">${layers}${cur}</div>`;
    },
  });
  window.EXTRA_IMGS = (window.EXTRA_IMGS || []).concat(['assets/cover-2.png']);
})();
