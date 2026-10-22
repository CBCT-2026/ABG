// Light/dark toggle. Pages open in light mode; the choice lasts for this browser tab only,
// so the next participant on the same device starts in light mode once the tab is closed.
const themeBtn = document.getElementById('theme');
const isDark = () => document.documentElement.dataset.theme === 'dark';
const showTheme = () => { const d = isDark(); themeBtn.textContent = d ? themeBtn.dataset.light : themeBtn.dataset.dark; themeBtn.setAttribute('aria-pressed', d); };
themeBtn.addEventListener('click', () => {
  const t = isDark() ? 'light' : 'dark';
  document.documentElement.dataset.theme = t;
  try { sessionStorage.setItem('theme', t); } catch (e) {}
  showTheme();
});
showTheme();

const mv = document.getElementById('mv');
if (mv) {
  mv.addEventListener('progress', e => {
    const bar = mv.querySelector('.progress');
    bar.querySelector('.progress-fill').style.width = (e.detail.totalProgress * 100) + '%';
    if (e.detail.totalProgress === 1) bar.classList.add('done');
  });

  // Hide or show the labels on the model.
  const labels = document.getElementById('labels');
  labels.addEventListener('click', () => {
    const off = mv.classList.toggle('labels-off');
    labels.setAttribute('aria-pressed', off);
    labels.textContent = off ? labels.dataset.off : labels.dataset.on;
  });

  // Preset camera views.
  const views = document.querySelectorAll('[data-orbit]');
  views.forEach(b => b.addEventListener('click', () => {
    mv.cameraOrbit = b.dataset.orbit;
    mv.cameraTarget = b.dataset.target || 'auto auto auto';
    views.forEach(o => o.setAttribute('aria-pressed', o === b));
  }));

  // Take the gum part off: it slides down off the jaw (animation "remove" in the model), then fades out.
  // Put it back: it fades in below the jaw, then slides back up ("replace").
  const gum = document.getElementById('gum');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let gumOff = false, busy = false;
  const gumMaterial = () => mv.model && mv.model.materials.find(m => m.name.replace(/\.\d+$/, '') === 'gum');
  function fade(from, to, ms) {
    const m = gumMaterial(); if (!m) return Promise.resolve();
    m.setAlphaMode('BLEND');
    const c = m.pbrMetallicRoughness.baseColorFactor.slice(0, 3);
    return new Promise(res => { const t0 = performance.now();
      (function step(now) { const k = Math.min(1, (now - t0) / ms);
        m.pbrMetallicRoughness.setBaseColorFactor([...c, from + (to - from) * k]);
        if (k < 1) requestAnimationFrame(step); else { if (to === 1) m.setAlphaMode('OPAQUE'); res(); } })(t0); });
  }
  function playClip(name) {
    return new Promise(res => {
      mv.animationName = name; mv.currentTime = 0;
      let done = false;
      const end = () => { if (!done) { done = true; mv.pause(); mv.currentTime = mv.duration; res(); } };
      mv.addEventListener('finished', end, { once: true });
      setTimeout(end, 1700);
      mv.play({ repetitions: 1 });
    });
  }
  if (gum) {
    mv.addEventListener('load', () => { if (!gumMaterial() || !mv.availableAnimations.includes('remove')) gum.hidden = true; });
    gum.addEventListener('click', async () => {
      if (busy) return; busy = true; gum.disabled = true;
      if (!gumOff) {
        if (!reduce) await playClip('remove');
        await fade(1, 0, reduce ? 1 : 450);
        gumOff = true; mv.classList.add('gum-off');
      } else {
        gumOff = false; mv.classList.remove('gum-off');
        await fade(0, 1, reduce ? 1 : 300);
        if (!reduce) await playClip('replace');
      }
      gum.setAttribute('aria-pressed', gumOff);
      gum.textContent = gumOff ? gum.dataset.on : gum.dataset.off;
      gum.disabled = false; busy = false;
    });
  }

  // Show a plain message in the viewer box if 3D cannot be shown, instead of an empty box.
  const msg = document.documentElement.lang === 'ja'
    ? { gl: 'このブラウザでは3D表示（WebGL）が使えません。別のブラウザで開いてください。', load: '3Dモデルを読み込めませんでした。ページを再読み込みしてください。' }
    : { gl: 'This browser cannot show 3D (WebGL is off). Open the page in another browser.', load: 'The 3D model could not load. Please reload the page.' };
  const problem = text => { const box = document.createElement('div'); box.className = 'problem'; box.textContent = text; mv.appendChild(box); };
  const canvas = document.createElement('canvas');
  if (!(canvas.getContext('webgl2') || canvas.getContext('webgl'))) problem(msg.gl);
  mv.addEventListener('error', () => problem(msg.load));
}

// A tap on a source number opens the closed list of sources first.
document.querySelectorAll('.cite a').forEach(a => a.addEventListener('click', () => {
  const d = document.querySelector('.refs details');
  if (d) d.open = true;
}));
