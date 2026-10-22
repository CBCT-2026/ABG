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

// Device check: a touch screen (finger) or a mouse.
// The page shows the matching "how to turn the model" hint.
const touch = matchMedia('(pointer: coarse)').matches || (!matchMedia('(pointer: fine)').matches && navigator.maxTouchPoints > 0);
const device = { input: touch ? 'touch' : 'mouse' };
document.documentElement.dataset.input = device.input;
const hint = document.getElementById('hint');
if (hint) hint.textContent = hint.dataset[device.input];

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
  mv.addEventListener('camera-change', e => {
    if (e.detail.source === 'user-interaction') views.forEach(o => o.setAttribute('aria-pressed', 'false'));
  });

  // Take the gum part off: it slides down off the jaw (animation "remove" in the model), then fades out.
  // Put it back: it fades in below the jaw, then slides back up ("replace").
  const gum = document.getElementById('gum');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) mv.interactionPrompt = 'none';
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
    // The button works only once the model has loaded; it is hidden if the model has no gum part or fails to load.
    gum.disabled = true;
    mv.addEventListener('load', () => { if (!gumMaterial() || !mv.availableAnimations.includes('remove')) gum.hidden = true; else gum.disabled = false; });
    mv.addEventListener('error', () => { gum.hidden = true; });
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
  const gl = canvas.getContext('webgl2') || canvas.getContext('webgl');
  if (!gl) problem(msg.gl);
  else { const lose = gl.getExtension('WEBGL_lose_context'); if (lose) lose.loseContext(); }
  mv.addEventListener('error', () => problem(msg.load));
  // If the 3D viewer script itself did not load, say so instead of showing an empty box.
  setTimeout(() => { if (!customElements.get('model-viewer')) { mv.classList.add('no-viewer'); problem(msg.load); } }, 8000);
}

// A tap on a source number opens the closed list of sources first.
document.querySelectorAll('.cite a').forEach(a => a.addEventListener('click', () => {
  const d = document.querySelector('.refs details');
  if (d) d.open = true;
}));

// Study mode: open stage 1 with ?study=1&t=<seconds per stage> (for example /en/pre-op/?study=1&t=60).
// Each stage page gets that viewing time, counted from when it is first opened in this tab. When a stage's time is up,
// the page asks the participant to go to the next stage; after stage 3 it asks them to tell the researcher. The language switch and the
// link to the home page are hidden, so every participant sees only this material, in the language of their form.
// When the time is up, a full-page message asks the participant to tell the researcher.
const clearEnds = () => { try { Object.keys(sessionStorage).filter(k => k.startsWith('studyEnd')).forEach(k => sessionStorage.removeItem(k)); } catch (e) {} };
(function study() {
  let cfg = null;
  const q = new URLSearchParams(location.search);
  try {
    if (q.get('study') === '1') {
      cfg = { t: Math.max(10, parseInt(q.get('t') || '60', 10) || 60) };
      sessionStorage.setItem('study', JSON.stringify(cfg));
      // Opening the study link starts fresh timers; reloading the page or going back keeps the running ones.
      const nav = performance.getEntriesByType('navigation')[0];
      if (!nav || nav.type === 'navigate') clearEnds();
    } else {
      cfg = JSON.parse(sessionStorage.getItem('study') || 'null');
    }
  } catch (e) {}
  if (!cfg) return;
  document.documentElement.classList.add('study');
  // No way out of the material: the language switch and the home link stop working for mouse, touch and keyboard.
  document.querySelectorAll('.bar .lang, .bar .logos').forEach(a => { a.removeAttribute('href'); a.setAttribute('tabindex', '-1'); a.setAttribute('aria-hidden', 'true'); });
  const timer = document.getElementById('timer'), left = document.getElementById('timer-left'), up = document.getElementById('timeup');
  if (!timer) return;
  const key = 'studyEnd:' + document.body.dataset.stage;
  let fallback = 0;
  // Read the end time on every tick, so a page restored by the back button stays in step.
  const endTime = () => { try { return parseInt(sessionStorage.getItem(key), 10) || fallback; } catch (e) { return fallback; } };
  const tick = () => {
    const s = Math.max(0, Math.ceil((endTime() - Date.now()) / 1000));
    left.textContent = Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0');
    timer.classList.toggle('soon', s <= 15);
    if (s === 0) {
      // Time is up: only the message and its button (next stage, or the researcher's Start again after stage 3) can be used.
      up.hidden = false; clearInterval(id);
      [...document.body.children].forEach(el => { if (!el.contains(up)) el.inert = true; });
      [...up.parentNode.children].forEach(el => { if (el !== up) el.inert = true; });
      const btn = up.querySelector('.again, .next-stage'); if (btn) btn.focus();
      document.querySelectorAll('audio').forEach(a => a.pause());
    }
  };
  let id;
  const run = () => { timer.hidden = false; id = setInterval(tick, 500); tick(); };
  // Each stage's time starts when the participant taps Start, so loading time and hand-over don't count.
  const gate = document.getElementById('gate');
  if (endTime() || !gate) { if (!endTime()) fallback = Date.now() + cfg.t * 1000; run(); return; }
  timer.hidden = true;
  gate.hidden = false;
  const others = [...document.body.children].filter(el => !el.contains(gate)).concat([...gate.parentNode.children].filter(el => el !== gate));
  others.forEach(el => { el.inert = true; });
  const start = document.getElementById('start');
  start.focus();
  start.addEventListener('click', () => {
    fallback = Date.now() + cfg.t * 1000;
    try { sessionStorage.setItem(key, String(fallback)); } catch (e) {}
    gate.hidden = true; others.forEach(el => { el.inert = false; });
    run();
  });
})();

// Start again: put everything back as the next participant should find it (light mode, labels on,
// gum part on, stage 1, and in study mode a fresh timer).
// In study mode the button at the bottom of the page is hidden, so a participant cannot reset their own timer;
// the researcher uses the one on the time-up screen.
document.querySelectorAll('.again').forEach(restart => restart.addEventListener('click', () => {
  try { sessionStorage.removeItem('theme'); } catch (e) {}
  clearEnds();
  let study = null;
  try { study = JSON.parse(sessionStorage.getItem('study') || 'null'); } catch (e) {}
  const url = new URL(restart.dataset.home, location.href);
  if (study) { url.searchParams.set('study', '1'); url.searchParams.set('t', study.t); }
  location.href = url.href;
}));

// QR code on the home page: a tap opens it full screen, so someone can scan it from this screen.
const qrOpen = document.getElementById('qr-open'), qr = document.getElementById('qr');
if (qrOpen && qr) {
  qrOpen.addEventListener('click', () => { if (qr.showModal) qr.showModal(); else qr.setAttribute('open', ''); });
  qr.addEventListener('click', e => { if (e.target === qr) qr.close(); });
}
