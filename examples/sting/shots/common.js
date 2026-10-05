/* Shared pieces for every builder. Do not edit without telling the lead; A/B/C/D all depend on it.
   Stage is 1080x1080. Spec coordinates are 720-px: multiply by S (1.5). */

// ---------- Frame by Frame brand ----------
window.FF = {
  sky: 'linear-gradient(180deg,#294376 0%,#35598f 25%,#42699d 46%,#5a82b4 68%,#6891c0 84%,#769cc2 100%)',
  navy: '#1E2F52', deep: '#294376', mid: '#5A82B4', light: '#769CC2', ice: '#E6F0FA',
  glowTeal: '#7FAE9E',              // the soft teal glow top-right of the logo (NOT purple)
  // four orbit squares for S2 (replace the ref's yellow/blue/green/magenta; no purple/magenta allowed)
  squares: ['#2F6BFF', '#3CC8F0', '#4ED6A0', '#FFFFFF'],
};

// The Frame by Frame mark: viewfinder corner brackets + bold "FF". px = box size. color = stroke/text colour.
function ffMark(px, color = '#fff', extra = '') {
  const k = px / 100, t = 5.5 * k, L = 22 * k, m = 12 * k;
  const br = (l, tp, bl, bt) => `<div class="a" style="left:${l}px;top:${tp}px;width:${L}px;height:${L}px;border-${bl}:${t}px solid ${color};border-${bt}:${t}px solid ${color}"></div>`;
  return `<div style="position:relative;width:${px}px;height:${px}px;${extra}">
    ${br(m, m, 'left', 'top')}${br(px - m - L, px - m - L, 'right', 'bottom')}${br(m, px - m - L, 'left', 'bottom')}
    <div class="a" style="inset:0;display:flex;align-items:center;justify-content:center;font:700 ${40 * k}px/1 Inter;letter-spacing:-.04em;color:${color}">FF</div>
  </div>`;
}
// App icon tile (dark navy squircle, white mark) and light disc variant (white disc, navy mark) like the ref's logo disc.
const ffTile = (px) => `<div style="width:${px}px;height:${px}px;border-radius:${px * .23}px;background:linear-gradient(160deg,#294376,#1E2F52);display:flex;align-items:center;justify-content:center">${ffMark(px * .78, '#fff')}</div>`;
const ffDisc = (px, fill = '#FBFCFE', rim = '#E8E8EA', ink = '#2B3F63') => `<div style="width:${px}px;height:${px}px;border-radius:50%;background:${fill};box-shadow:inset 0 0 0 ${Math.max(1, px * .012)}px ${rim};display:flex;align-items:center;justify-content:center">${ffMark(px * .62, ink)}</div>`;

// ---------- Whop hub UI (light theme), measured from the live hub 2026-09-27 ----------
// Font Inter everywhere. Page bg #FFFFFF, body text rgb(32,32,32).
// Sidebar nav items: Inter 500, 16px/24px (at 1x), colour rgba(0,0,0,.61); active item has a light grey pill bg #F0F0F0 and text #202020.
// Section labels ("Chat", "Preview as"): Inter 500 14px/20px rgba(0,0,0,.49).
// Top bar: centred search pill "Search Frame by Frame  ⌘K" (bg #F3F3F3, radius 10, text rgba(0,0,0,.45)).
// Hub header (top of sidebar): 28px rounded-square hub icon + "Frame by Frame" Inter 600 15px #202020.
// Course cards: white, 1px #E8E8E8 border, radius 12, cover image 16:9 on top (assets/cover-N.png),
//   title Inter 600 15px #202020, 2-line description 13px rgba(0,0,0,.55), meta "1 chapter · 8 lessons" 12px rgba(0,0,0,.45).
// Lesson page: breadcrumb 13px grey, title Inter 700 28px #111, body Inter 400 16px/1.6 #3a3a3a.
// PRIVACY: never draw a wallet balance, other businesses in the left rail, a real avatar photo, or member counts.
const WHOP = {
  bg: '#FFFFFF', ink: '#202020', nav: 'rgba(0,0,0,.61)', label: 'rgba(0,0,0,.49)', line: '#ECECEC',
  pill: '#F0F0F0', search: '#F3F3F3', card: '#FFFFFF', cardLine: '#E8E8E8', radius: 12,
};
// Simple nav icons (stroke 1.6 at 20px) — generic shapes, not Whop's icon set.
const icon = {
  home: c => `<svg viewBox="0 0 20 20" width="100%" height="100%"><path d="M3 9 10 3l7 6v8H12v-5H8v5H3z" fill="none" stroke="${c}" stroke-width="1.6" stroke-linejoin="round"/></svg>`,
  courses: c => `<svg viewBox="0 0 20 20" width="100%" height="100%"><path d="M2 6l8-3 8 3-8 3z M5 8v5c3 2 7 2 10 0V8" fill="none" stroke="${c}" stroke-width="1.6" stroke-linejoin="round"/></svg>`,
  content: c => `<svg viewBox="0 0 20 20" width="100%" height="100%"><rect x="4" y="2.5" width="12" height="15" rx="2" fill="none" stroke="${c}" stroke-width="1.6"/><path d="M7 7h6M7 10h6M7 13h4" stroke="${c}" stroke-width="1.6"/></svg>`,
  chat: c => `<svg viewBox="0 0 20 20" width="100%" height="100%"><path d="M3 4h14v9H8l-4 3v-3H3z" fill="none" stroke="${c}" stroke-width="1.6" stroke-linejoin="round"/></svg>`,
  play: c => `<svg viewBox="0 0 20 20" width="100%" height="100%"><path d="M6 4l10 6-10 6z" fill="${c}"/></svg>`,
};
