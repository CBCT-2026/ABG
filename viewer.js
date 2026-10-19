// Light/dark toggle. The label names the mode a tap switches to.
const themeBtn = document.getElementById('theme');
const isDark = () => (document.documentElement.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')) === 'dark';
const showTheme = () => { const d = isDark(); themeBtn.textContent = d ? themeBtn.dataset.light : themeBtn.dataset.dark; themeBtn.setAttribute('aria-pressed', d); };
themeBtn.addEventListener('click', () => {
  const t = isDark() ? 'light' : 'dark';
  document.documentElement.dataset.theme = t;
  try { localStorage.setItem('theme', t); } catch (e) {}
  showTheme();
});
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', showTheme);
showTheme();

// The rest is for the stage pages, which have a 3D model.
const mv = document.getElementById('mv');
if (mv) {

mv.addEventListener('progress', e => {
  const bar = mv.querySelector('.progress');
  bar.querySelector('.progress-fill').style.width = (e.detail.totalProgress * 100) + '%';
  if (e.detail.totalProgress === 1) bar.classList.add('done');
});

// Dots whose place on the model is not known yet (no hotspot node in the model) are left out.
mv.querySelectorAll('.hotspot:not([data-position])').forEach(h => h.remove());

// Tap a numbered dot to show its name on the model and its notes under the model.
const info = document.getElementById('info');
mv.querySelectorAll('.hotspot').forEach(h => h.addEventListener('click', () => {
  const open = !h.classList.contains('open');
  mv.querySelectorAll('.hotspot').forEach(o => o.classList.remove('open'));
  h.classList.toggle('open', open);
  info.hidden = !open;
  if (!open) return;
  const num = h.getAttribute('slot').split('-')[1];
  const items = [...h.querySelectorAll('.note > span')].map(s => '<li>' + s.innerHTML + '</li>').join('');
  info.innerHTML = '<h3><span class="num">' + num + '</span>' + h.querySelector('.label').innerHTML + '</h3><ul>' + items + '</ul>';
  info.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
}));

// Tap the notes box to close it.
info.addEventListener('click', () => {
  info.hidden = true;
  mv.querySelectorAll('.hotspot').forEach(o => o.classList.remove('open'));
});

// Hide or show all the numbered dots.
const labels = document.getElementById('labels');
labels.addEventListener('click', () => {
  const off = mv.classList.toggle('labels-off');
  labels.setAttribute('aria-pressed', off);
  labels.textContent = off ? labels.dataset.off : labels.dataset.on;
  if (off) {
    mv.querySelectorAll('.hotspot').forEach(o => o.classList.remove('open'));
    info.hidden = true;
  }
});

// Preset camera views.
const viewButtons = document.querySelectorAll('[data-orbit]');
viewButtons.forEach(b => b.addEventListener('click', () => {
  mv.cameraOrbit = b.dataset.orbit;
  mv.cameraTarget = b.dataset.target || 'auto auto auto';
  viewButtons.forEach(o => o.setAttribute('aria-pressed', o === b));
}));

// Removable parts. Each part is a material in the model, named as in docs/model-spec.md.
// hide: take the part off (and put it back). xray: make it see-through to show what is inside.
// swap: show this part in place of another one (for example a new tooth instead of the crown).
const partButtons = [...document.querySelectorAll('.controls .part')];
const original = new Map();
const materials = name => mv.model ? mv.model.materials.filter(m => m.name === name || m.name.startsWith(name + '.')) : [];
function setAlpha(name, alpha) {
  for (const m of materials(name)) {
    if (!original.has(m)) original.set(m, { color: [...m.pbrMetallicRoughness.baseColorFactor], mode: m.getAlphaMode() });
    const o = original.get(m);
    if (alpha === null) {
      m.setAlphaMode(o.mode);
      m.pbrMetallicRoughness.setBaseColorFactor(o.color);
    } else {
      m.setAlphaMode('BLEND');
      m.pbrMetallicRoughness.setBaseColorFactor([o.color[0], o.color[1], o.color[2], alpha]);
    }
  }
}
function showPartLabel(b, on) { b.setAttribute('aria-pressed', on); b.textContent = on ? b.dataset.off : b.dataset.on; }
function showPart(b, on) {
  showPartLabel(b, on);
  const part = b.dataset.part;
  if (b.dataset.mode === 'hide') setAlpha(part, on ? 0 : null);
  if (b.dataset.mode === 'xray') setAlpha(part, on ? 0.3 : null);
  if (b.dataset.mode === 'swap') {
    setAlpha(part, on ? null : 0);
    setAlpha(b.dataset.with, on ? 0 : null);
    // The hide button for the part being swapped out is not useful while it is swapped out.
    partButtons.filter(o => o.dataset.part === b.dataset.with).forEach(o => { o.disabled = on; showPartLabel(o, false); });
  }
}
partButtons.forEach(b => b.addEventListener('click', () => showPart(b, b.getAttribute('aria-pressed') !== 'true')));
mv.addEventListener('load', () => {
  original.clear();
  // Only show a button if the model has that part.
  partButtons.forEach(b => { b.hidden = materials(b.dataset.part).length === 0; });
  // A replacement part starts hidden: the model shows the first choice.
  partButtons.filter(b => b.dataset.mode === 'swap' && !b.hidden).forEach(b => setAlpha(b.dataset.part, 0));
});

// Show a plain message in the viewer box if 3D cannot be shown, instead of an empty box.
function showProblem(text) {
  let box = mv.querySelector('.problem');
  if (!box) {
    box = document.createElement('div');
    box.className = 'problem';
    mv.appendChild(box);
  }
  box.textContent = text;
}
const msg = document.documentElement.lang === 'ja'
  ? { gl: 'このブラウザでは3D表示（WebGL）が使えません。ブラウザの設定で「ハードウェアアクセラレーション」をオンにするか、別のブラウザで開いてください。',
      load: '3Dモデルを読み込めませんでした。ページを再読み込みしてください。' }
  : { gl: 'This browser cannot show 3D (WebGL is off). Turn on hardware acceleration in the browser settings, or open the page in another browser.',
      load: 'The 3D model could not load. Please reload the page.' };
const canvas = document.createElement('canvas');
if (!(canvas.getContext('webgl2') || canvas.getContext('webgl'))) showProblem(msg.gl);
mv.addEventListener('error', e => {
  // A stage whose model file is not in models/ yet says so, instead of asking for a reload.
  fetch(mv.src, { method: 'HEAD' }).then(r => showProblem(r.ok ? msg.load : mv.dataset.missing))
    .catch(() => showProblem(msg.load));
});
}
