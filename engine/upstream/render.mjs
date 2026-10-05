/* Frame by Frame: frame renderer (Playwright + headless Chromium).
   Run from the film folder (the folder that holds page.html, shots/, assets/).

     node ../engine/render.mjs frames 0,40,80     -> out/$OUT/stills/fNNNN.png
     node ../engine/render.mjs compare 0,40,80    -> stills + out/$OUT/cmp/sheet.jpg (LEFT = ref/full, RIGHT = render)
     node ../engine/render.mjs full [F0] [F1]     -> frames/fNNNN.png for F0..F1 (default 0..window.LAST_FRAME)

   Env (all optional):
     PAGE=page.html   page to load, relative to the film folder
     OUT=             sub-folder of out/ for stills; one per parallel builder (OUT=A, OUT=B)
     FRAMES=frames    output folder for `full`
     PAD=4            zero padding of frame numbers in file names (5 for films over 9,999 frames)
     W=1920 H=1080    viewport size
     LAST=            last frame for `full` if the page does not set window.LAST_FRAME
     WEBGL=1          software WebGL (SwiftShader) for three.js or canvas 3D shots; do not add --disable-gpu
     CHROMIUM_ARGS=   extra Chromium flags, space-separated
     PYTHON=python3   interpreter that runs compare.py in `compare` mode

   The page loads over file:// (no server). Chromium does not start inside the macOS sandbox:
   in Claude Code, run this command unsandboxed. */
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const ENGINE = path.dirname(fileURLToPath(import.meta.url));
const FILM = process.cwd();
const mode = process.argv[2] || 'frames';
if (!['frames', 'compare', 'full'].includes(mode)) { console.error('usage: node render.mjs frames|compare|full ...'); process.exit(1); }
const PAD = +(process.env.PAD || 4), W = +(process.env.W || 1920), H = +(process.env.H || 1080);
const pagePath = path.resolve(FILM, process.env.PAGE || 'page.html');
if (!fs.existsSync(pagePath)) { console.error('page not found:', pagePath, '(run from your film folder or set PAGE=)'); process.exit(1); }

const args = ['--allow-file-access-from-files', '--font-render-hinting=none'];
if (process.env.WEBGL === '1') args.push('--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist');
if (process.env.CHROMIUM_ARGS) args.push(...process.env.CHROMIUM_ARGS.split(/\s+/).filter(Boolean));
const b = await chromium.launch({ args });
const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
p.on('pageerror', e => console.log('PAGE ERROR', e.message));
await p.goto('file://' + pagePath);
await p.waitForFunction(() => window.ready, null, { timeout: 90000 });

let list;
if (mode === 'full') {
  const last = process.env.LAST !== undefined ? +process.env.LAST : await p.evaluate(() => window.LAST_FRAME);
  if (last === undefined || last === null || Number.isNaN(+last)) { console.error('set window.LAST_FRAME in the page or LAST= in the env'); process.exit(1); }
  const a = +(process.argv[3] ?? 0), z = +(process.argv[4] ?? last);
  list = Array.from({ length: z - a + 1 }, (_, i) => a + i);
} else list = (process.argv[3] || '').split(',').filter(Boolean).map(Number);
if (!list.length) { console.error('no frames given, e.g. node render.mjs frames 0,40,80'); process.exit(1); }

const dir = mode === 'full' ? path.resolve(FILM, process.env.FRAMES || 'frames') : path.join(FILM, 'out', process.env.OUT || '', 'stills');
fs.mkdirSync(dir, { recursive: true });
const t0 = Date.now();
for (const F of list) {
  await p.evaluate(F => window.seekFrame(F), F);
  await p.screenshot({ path: path.join(dir, `f${String(F).padStart(PAD, '0')}.png`) });
  if (mode === 'full' && F % 100 === 0) console.log('frame', F);
}
await b.close();
console.log('rendered', list.length, 'frame(s) ->', path.relative(FILM, dir) || '.', `(${((Date.now() - t0) / 1000).toFixed(1)} s)`);

if (mode === 'compare') {
  execFileSync(process.env.PYTHON || 'python3', [path.join(ENGINE, 'compare.py'), ...list.map(String)],
    { stdio: 'inherit', cwd: FILM, env: { ...process.env, OUT: process.env.OUT || '', PAD: String(PAD) } });
}
