// Render the poster picture shown while a model loads.  Usage: node tools/poster.js models/<name>.glb models/<name>-poster.webp
const { chromium } = require('playwright'); const http = require('http'); const fs = require('fs'); const path = require('path');
const [glb, out] = process.argv.slice(2); const root = path.resolve(__dirname, '..');
const types = { '.js': 'text/javascript', '.glb': 'model/gltf-binary', '.html': 'text/html', '.wasm': 'application/wasm' };
const srv = http.createServer((q, r) => { const f = path.join(root, decodeURIComponent(q.url.split('?')[0]));
  if (q.url === '/__poster.html') { r.setHeader('content-type', 'text/html'); return r.end(`<!doctype html><body style="margin:0;background:#fff">
<script>self.ModelViewerElement = { dracoDecoderLocation: location.origin + '/vendor/draco/' };</script>
<script type="module" src="/vendor/model-viewer/model-viewer.min.js"></script>
<model-viewer id="mv" src="/${glb}" camera-controls interaction-prompt="none" camera-orbit="0deg 80deg auto" shadow-intensity="1" exposure="1.05" style="width:800px;height:520px;background:#fff"></model-viewer>`); }
  fs.readFile(f, (e, d) => { if (e) { r.statusCode = 404; return r.end(); } r.setHeader('content-type', types[path.extname(f)] || 'application/octet-stream'); r.end(d); }); });
srv.listen(0, async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 800, height: 520 }, deviceScaleFactor: 1 });
  await p.goto(`http://localhost:${srv.address().port}/__poster.html`);
  await p.waitForFunction(() => document.getElementById('mv').loaded, null, { timeout: 60000 }); await p.waitForTimeout(1500);
  const png = out.replace(/\.webp$/, '.png'); await p.screenshot({ path: png });
  await b.close(); srv.close();
  require('child_process').execSync(`python3 -c "from PIL import Image; Image.open('${png}').convert('RGB').save('${out}', 'WEBP', quality=80)"`); fs.unlinkSync(png);
  console.log(out, fs.statSync(out).size);
});
