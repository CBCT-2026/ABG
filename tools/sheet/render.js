// Render the model pictures for the 2D information sheets, one set per stage.
// Usage, from the repo root: node tools/sheet/render.js  (uses vendor/model-viewer and vendor/draco)
// Needs Playwright (Chromium). Writes images/sheet-<view>-<lang>.png. Views and labels: VIEWS below;
// label names and positions come from H in tools/build.py (via tools/sheet/labels.json, written by build.py).
// A view can hide the gum, show removable parts (`show`: material names) and add labels for parts
// the web page only names on its buttons (`extra`: text at an existing label's position).
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../..');
const LABELS = JSON.parse(fs.readFileSync(path.join(__dirname, 'labels.json'), 'utf8'));
const MV = process.env.MODEL_VIEWER_JS || path.join(ROOT, 'vendor/model-viewer/model-viewer.min.js');
// The models are Draco-compressed; the decoder comes from vendor/draco (DRACO_DIR overrides).
const DRACO = process.env.DRACO_DIR || path.join(ROOT, 'vendor/draco');
const EXTRA = {
  implant: { at: 'space', en: ['Implant', 'with a crown'], ja: ['インプラント', 'クラウン'] },
  bridge: { at: 'space', en: ['Bridge', 'one wing'], ja: ['ブリッジ', '一まいの羽'] },
  plate: { at: 'space', en: ['Plate', 'false tooth you can take out'], ja: ['入れ歯', '取り外しできる'] },
  gap2: { at: 'space', en: ['Gap for the missing tooth', 'lateral incisor'], ja: ['ない歯のすき間', ''] },
};
const OPTIONS = ['option-none', 'option-implant', 'option-bridge', 'option-denture'];
const S1 = 'abg-1-pre-op', S2 = 'abg-2-short-term', S3 = 'abg-3-long-term';
const VIEWS = [
  { name: 'front-gum', model: S1, orbit: '0deg 80deg auto', gum: true, labels: ['gum', 'central', 'missing'] },
  { name: 'front-bone', model: S1, orbit: '0deg 80deg auto', gum: false, labels: ['gap', 'central', 'missing'] },
  { name: 'below', model: S1, orbit: '0deg 165deg auto', gum: true, labels: ['palate', 'central'], w: 640, h: 560 },
  { name: 'left', model: S1, orbit: '40deg 75deg 0.15m', target: '0.028m 0.006m 0.01m', gum: false, labels: ['window'], w: 640, h: 560 },
  { name: 's2-braces', model: S2, orbit: '0deg 80deg auto', gum: true, show: ['braces'], labels: ['braces', 'false', 'central'] },
  { name: 's2-off', model: S2, orbit: '0deg 80deg auto', gum: true, hide: ['braces'], labels: ['canine', 'central'], extra: ['gap2'], tweak: { central: { side: 'left', len: 40 } } },
  { name: 's2-bone', model: S2, orbit: '0deg 80deg auto', gum: false, hide: ['braces'], labels: ['graft', 'canine'], tweak: { graft: { len: 130 } } },
  { name: 's2-below', model: S2, orbit: '0deg 165deg auto', gum: true, show: ['braces'], labels: ['palate'], w: 640, h: 560 },
  { name: 's3-implant', model: S3, orbit: '0deg 80deg auto', gum: true, option: 'option-implant', labels: ['central'], extra: ['implant'] },
  { name: 's3-bridge', model: S3, orbit: '0deg 80deg auto', gum: true, option: 'option-bridge', labels: ['central'], extra: ['bridge'] },
  { name: 's3-plate', model: S3, orbit: '0deg 80deg auto', gum: true, option: 'option-denture', labels: ['central'], extra: ['plate'] },
  { name: 's3-bone', model: S3, orbit: '0deg 80deg auto', gum: false, hide: OPTIONS, labels: ['healed', 'canine'], tweak: { healed: { len: 130 } } },
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
    if (DRACO) await page.route('https://www.gstatic.com/draco/**', r => r.fulfill({ path: path.join(DRACO, path.basename(new URL(r.request().url()).pathname)) }));
    await page.goto(`http://localhost:${port}/tools/sheet/render.html`);
    await page.evaluate(async ({ v, lang, LABELS, EXTRA, OPTIONS }) => {
      document.documentElement.lang = lang;
      const mv = document.getElementById('mv');
      mv.style.setProperty('--w', (v.w || 900) + 'px'); mv.style.setProperty('--h', (v.h || 600) + 'px');
      await new Promise(r => { mv.addEventListener('load', r, { once: true }); mv.src = `../../models/${v.model}.glb`; });
      mv.cameraOrbit = v.orbit; mv.cameraTarget = v.target || 'auto auto auto'; mv.jumpCameraToGoal();
      const show = (name, on) => { const m = mv.model.materials.find(m => m.name.replace(/\.\d+$/, '') === name); if (!m) return;
        const c = m.pbrMetallicRoughness.baseColorFactor.slice(0, 3);
        m.setAlphaMode(on ? 'OPAQUE' : 'BLEND'); m.pbrMetallicRoughness.setBaseColorFactor([...c, on ? 1 : 0]); };
      if (!v.gum) show('gum', false);
      (v.show || []).forEach(n => show(n, true)); (v.hide || []).forEach(n => show(n, false));
      if (v.option) OPTIONS.forEach(n => show(n, n === v.option));
      const labels = v.labels.map(k => ({ ...LABELS[k], ...((v.tweak || {})[k]) })).concat((v.extra || []).map(k => ({ ...LABELS[EXTRA[k].at], ...EXTRA[k] })));
      labels.forEach((h, i) => { const d = document.createElement('div');
        d.className = 'hotspot'; d.slot = 'hotspot-' + (i + 1); d.dataset.position = h.pos; d.dataset.normal = h.normal;
        d.dataset.side = h.side; d.dataset.visibilityAttribute = 'visible'; d.style.setProperty('--len', h.len + 'px');
        d.innerHTML = `<span class="label">${h[lang][0]}${h[lang][1] ? `<small>${h[lang][1]}</small>` : ''}</span>`;
        mv.appendChild(d); });
      await new Promise(r => setTimeout(r, 1500));
    }, { v, lang, LABELS, EXTRA, OPTIONS });
    const out = path.join(ROOT, 'images', `sheet-${v.name}-${lang}.png`);
    await page.locator('#mv').screenshot({ path: out });
    require('child_process').execFileSync('python3', [path.join(__dirname, 'trim.py'), out]);
    console.log('wrote', path.relative(ROOT, out));
    await page.close();
  }
  await browser.close(); server.close();
})();
