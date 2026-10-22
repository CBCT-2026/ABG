// Render the model pictures for the 2D information sheets (stage 1 only until the stage models exist).
// Usage, from the repo root: MODEL_VIEWER_JS=path/to/model-viewer.min.js node tools/sheet/render.js
// Needs Playwright (Chromium). Writes images/sheet-<view>-<lang>.png. Views and labels: VIEWS below;
// label names and positions come from H in tools/build.py (via tools/sheet/labels.json, written by build.py).
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../..');
const LABELS = JSON.parse(fs.readFileSync(path.join(__dirname, 'labels.json'), 'utf8'));
const MV = process.env.MODEL_VIEWER_JS;
const VIEWS = [
  { name: 'front-gum', orbit: '0deg 80deg auto', gum: true, labels: ['gum', 'central', 'missing'] },
  { name: 'front-bone', orbit: '0deg 80deg auto', gum: false, labels: ['gap', 'central', 'missing'] },
  { name: 'below', orbit: '0deg 165deg auto', gum: true, labels: ['palate', 'central'], w: 640, h: 560 },
  { name: 'left', orbit: '40deg 75deg 0.15m', target: '0.028m 0.006m 0.01m', gum: false, labels: ['window'], w: 640, h: 560 },
];
const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.glb': 'model/gltf-binary', '.png': 'image/png' };
const server = http.createServer((req, res) => {
  const f = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  fs.readFile(f, (e, d) => { if (e) { res.writeHead(404); res.end(); return; }
    res.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' }); res.end(d); });
}).listen(0);
(async () => {
  const port = server.address().port;
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  for (const lang of ['en', 'ja']) for (const v of VIEWS) {
    const page = await browser.newPage({ viewport: { width: v.w || 900, height: v.h || 600 }, deviceScaleFactor: 3 });
    if (MV) await page.route('**/model-viewer.min.js', r => r.fulfill({ path: MV, contentType: 'text/javascript' }));
    await page.goto(`http://localhost:${port}/tools/sheet/render.html`);
    await page.evaluate(async ({ v, lang, LABELS }) => {
      document.documentElement.lang = lang;
      const mv = document.getElementById('mv');
      mv.style.setProperty('--w', (v.w || 900) + 'px'); mv.style.setProperty('--h', (v.h || 600) + 'px');
      await new Promise(r => mv.loaded ? r() : mv.addEventListener('load', r, { once: true }));
      mv.cameraOrbit = v.orbit; mv.cameraTarget = v.target || 'auto auto auto'; mv.jumpCameraToGoal();
      if (!v.gum) { const m = mv.model.materials.find(m => m.name.replace(/\.\d+$/, '') === 'gum');
        m.setAlphaMode('BLEND'); const c = m.pbrMetallicRoughness.baseColorFactor.slice(0, 3); m.pbrMetallicRoughness.setBaseColorFactor([...c, 0]); }
      v.labels.forEach((k, i) => { const h = LABELS[k]; const d = document.createElement('div');
        d.className = 'hotspot'; d.slot = 'hotspot-' + (i + 1); d.dataset.position = h.pos; d.dataset.normal = h.normal;
        d.dataset.side = h.side; d.dataset.visibilityAttribute = 'visible'; d.style.setProperty('--len', h.len + 'px');
        d.innerHTML = `<span class="label">${h[lang][0]}${h[lang][1] ? `<small>${h[lang][1]}</small>` : ''}</span>`;
        mv.appendChild(d); });
      await new Promise(r => setTimeout(r, 1500));
    }, { v, lang, LABELS });
    const out = path.join(ROOT, 'images', `sheet-${v.name}-${lang}.png`);
    await page.locator('#mv').screenshot({ path: out });
    require('child_process').execFileSync('python3', [path.join(__dirname, 'trim.py'), out]);
    console.log('wrote', path.relative(ROOT, out));
    await page.close();
  }
  await browser.close(); server.close();
})();
