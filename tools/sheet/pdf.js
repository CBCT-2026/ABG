// Print the 2D information sheets to A4 PDFs: sheet/abg-sheet-<n>-<stage>-<lang>.pdf
// Usage, from the repo root, after python3 tools/build.py: node tools/sheet/pdf.js   (needs Playwright)
const { chromium } = require('playwright');
const path = require('path');
const ROOT = path.resolve(__dirname, '../..');
const STAGES = ['pre-op', 'short-term', 'long-term'];
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  for (const lang of ['en', 'ja']) for (const [i, s] of STAGES.entries()) {
    await page.goto('file://' + path.join(ROOT, 'sheet', lang, s, 'index.html'), { waitUntil: 'networkidle' });
    const over = await page.evaluate(() => { const m = document.querySelector('main'); return m.scrollHeight - m.clientHeight; });
    const out = path.join(ROOT, 'sheet', `abg-sheet-${i + 1}-${s}-${lang}.pdf`);
    await page.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
    console.log('wrote', path.relative(ROOT, out), over > 0 ? `(text overflows by ${over}px: shorten or shrink)` : '');
  }
  await browser.close();
})();
