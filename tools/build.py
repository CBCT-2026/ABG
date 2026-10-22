"""Write every page of the site from content/.
Run from the repo root: python3 tools/build.py
Edit content/*.html, content/ui.json and content/references.json, not the pages under en/, ja/ and video/."""
import json, re, html, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
UI = json.load(open('content/ui.json'))
REFS = json.load(open('content/references.json'))
STAGES = ['pre-op', 'short-term', 'long-term']
MODEL = 'abg-placeholder'  # one placeholder model on every stage until the stage models are built
LANGS = ['en', 'ja']

# Labels on the model: position (metres, model axes), surface normal, side of the leader line.
# "when" ties a label to the gum part being on (on-gum) or taken off (off-gum).
H = {
 'gum':     dict(pos='0.034m 0.008m 0.0226m', normal='0 0 1', side='up', len=60, when='on-gum', en=['Gum', 'you can take it off'], ja=['歯ぐき', '外せます']),
 'gap':     dict(pos='0.019m 0.004m 0.021m', normal='0 0 1', side='left', len=24, when='off-gum', en=['Gap in the bone', 'alveolar cleft'], ja=['骨のすき間', 'がくれつ']),
 'window':  dict(pos='0.036m 0.012m -0.004m', normal='0.6 0 0.8', side='up', len=50, when='off-gum', en=['Eye tooth window', 'canine'], ja=['犬歯の窓', '']),
 'central': dict(pos='-0.002m -0.012m 0.0316m', normal='0 0 1', side='down', len=40, en=['Front tooth', 'central incisor'], ja=['前歯', '中切歯']),
 'missing': dict(pos='0.021m -0.010m 0.024m', normal='0 0 1', side='down', len=18, en=['Missing tooth', 'lateral incisor'], ja=['ない歯', '側切歯']),
 'palate':  dict(pos='0.008m 0.0073m -0.01m', normal='0 -1 0', side='left', len=30, when='on-gum', en=['Roof of the mouth', 'palate'], ja=['上あご', 'こうがい']),
}
LABELS = {'pre-op': ['gum', 'gap', 'window', 'central', 'missing', 'palate'], 'short-term': ['central'], 'long-term': ['central']}

def cite(text):
    order = []
    def sub(m):
        k = m.group(1)
        if k not in order: order.append(k)
        n = order.index(k) + 1
        return f'<sup class="cite"><a href="#ref-{n}">{n}</a></sup>'
    text = re.sub(r'\[\[([a-z0-9]+)\]\]', sub, text)
    refs = '\n'.join(f'    <li id="ref-{i + 1}">{REFS[k]}</li>' for i, k in enumerate(order))
    return text, refs

def head(lang, title, up, desc=''):
    return f'''<!doctype html>
<html lang="{lang}" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
{f'<meta name="description" content="{html.escape(desc)}">' if desc else ''}
<meta name="robots" content="noindex">
<script>
try {{ if (sessionStorage.getItem('theme') === 'dark') document.documentElement.dataset.theme = 'dark'; }} catch (e) {{}}
</script>
<link rel="stylesheet" href="{up}style.css">
'''

def bar(lang, up, other_href):
    t = UI[lang]; o = 'ja' if lang == 'en' else 'en'
    return f'''<header class="bar">
  <div class="bar-left">
    <a class="lang" href="{other_href}" lang="{o}" hreflang="{o}">{'日本語' if lang == 'en' else 'English'}</a>
    <button class="theme" id="theme" type="button" data-dark="{t['dark']}" data-light="{t['light']}">{t['dark']}</button>
  </div>
  <a class="logos" href="{up}" aria-label="{t['home']}">
    <img class="logo" src="{up}images/aichi-gakuin-logo.png" width="44" height="56" alt="Aichi Gakuin University">
    <img class="logo" src="{up}images/nagoya-logo.png" width="74" height="56" alt="Nagoya University">
  </a>
</header>
'''

def steps(lang, current, prefix):
    t = UI[lang]
    items = ''.join(f'<li><a href="{prefix}{s}/"{" aria-current=\"page\"" if s == current else ""}><span>{t[f"stage{i + 1}n"]}</span><b>{t[f"st{i + 1}"]}</b></a></li>' for i, s in enumerate(STAGES))
    return f'<ol class="steps" aria-label="{t["stages"]}">{items}</ol>'

def stage_page(lang, i, stage):
    t = UI[lang]; n = i + 1; up = '../../'
    text, refs = cite(open(f'content/{stage}-{lang}.html').read())
    spots = ''
    for k, key in enumerate(LABELS[stage]):
        h = H[key]
        cls = 'hotspot' + (' ' + h['when'] if h.get('when') else '')
        small = f'<small>{h[lang][1]}</small>' if h[lang][1] else ''
        spots += f'\n    <div class="{cls}" slot="hotspot-{k + 1}" data-position="{h["pos"]}" data-normal="{h["normal"]}" data-visibility-attribute="visible" data-side="{h["side"]}" style="--len: {h["len"]}px"><span class="label">{h[lang][0]}{small}</span></div>'
    placeholder = '' if n == 1 else f'\n    <div class="placeholder"><span>{t["placeholder"]}</span></div>'
    prev = f'<a href="../{STAGES[i - 1]}/">← {t[f"st{n - 1}"]}</a>' if i > 0 else '<span></span>'
    nxt = f'<a href="../{STAGES[i + 1]}/">{t[f"st{n + 1}"]} →</a>' if i < 2 else '<span></span>'
    o = 'ja' if lang == 'en' else 'en'
    return head(lang, f'{t["title"]} · {t[f"st{n}"]}', up, t[f'alt{n}']) + f'''<script type="module" src="https://cdn.jsdelivr.net/npm/@google/model-viewer@3.5.0/dist/model-viewer.min.js"></script>
</head>
<body>
{bar(lang, up, f"{up}{o}/{stage}/")}
<main>
  <h1>{t['title']}</h1>
  {steps(lang, stage, '../')}
  <!-- MODEL: placeholder on every stage until the stage models are built. See README. -->
  <model-viewer id="mv" src="{up}models/{MODEL}.glb" ios-src="{up}models/{MODEL}.usdz"
    alt="{html.escape(t[f'alt{n}'])}"
    ar ar-modes="webxr scene-viewer quick-look" ar-scale="auto"
    camera-controls camera-orbit="0deg 80deg auto" touch-action="pan-y" interaction-prompt="auto"
    shadow-intensity="1" exposure="1.05" loading="eager">
    <button slot="ar-button" class="ar-btn">{t['ar']}</button>{placeholder}{spots}
    <div class="progress" slot="progress-bar"><div class="progress-fill"></div></div>
  </model-viewer>
  <div class="controls" role="group" aria-label="{t['controls']}">
    <button type="button" data-orbit="0deg 80deg auto" aria-pressed="true">{t['vFront']}</button>
    <button type="button" data-orbit="0deg 165deg auto" aria-pressed="false">{t['vBelow']}</button>
    <button type="button" data-orbit="40deg 75deg 0.11m" data-target="0.028m 0.006m 0.01m" aria-pressed="false">{t['vLeft']}</button>
    <button type="button" id="labels" aria-pressed="false" data-on="{t['hideLabels']}" data-off="{t['showLabels']}">{t['hideLabels']}</button>
    <button type="button" id="gum" class="gum" aria-pressed="false" data-off="{t['gumOff']}" data-on="{t['gumOn']}">{t['gumOff']}</button>
  </div>

  <!-- TEXT: generated from content/{stage}-{lang}.html by tools/build.py. -->
{text}
  <section class="refs">
<details>
  <summary><h2>{t['sources']}</h2></summary>
  <ol>
{refs}
  </ol>
</details>
  </section>
  <nav class="next" aria-label="{t['stages']}">{prev}{nxt}</nav>
  <p class="disclaimer">{t['disclaimer']}</p>
</main>
<script src="{up}site.js"></script>
</body>
</html>
'''

def video_page(lang):
    t = UI[lang]; up = '../../'; o = 'ja' if lang == 'en' else 'en'
    ch = ''.join(f'<span class="chapter"><b>{t[f"stage{i}n"]}</b> {t[f"st{i}"]}</span>' for i in (1, 2, 3))
    return head(lang, t['title'], up) + f'''</head>
<body>
{bar(lang, up, f"{up}video/{o}/")}
<main>
  <h1>{t['title']}</h1>
  <!-- VIDEO: one portrait video per language (TTS voice, subtitles, line labels), one chapter per stage. -->
  <div class="player"><p class="notready">{t['videoNotReady']}</p></div>
  <div class="chapters" aria-label="{t['chapters']}">{ch}</div>
  <p class="disclaimer">{t['disclaimer']}</p>
</main>
<script src="{up}site.js"></script>
</body>
</html>
'''

def home():
    t, j = UI['en'], UI['ja']
    lst = ''.join(f'<li><b>{i}</b><span>{t[f"st{i}long"]}<br><span lang="ja">{j[f"st{i}long"]}</span></span></li>' for i in (1, 2, 3))
    return head('en', f'{t["title"]} / {j["title"]}', '') + f'''</head>
<body>
<main>
  <div class="top"><button class="theme" id="theme" type="button" data-dark="Dark mode / ダークモード" data-light="Light mode / ライトモード">Dark mode / ダークモード</button></div>
  <div class="home-logos">
    <img class="logo" src="images/aichi-gakuin-logo.png" width="60" height="76" alt="Aichi Gakuin University">
    <img class="logo" src="images/nagoya-logo.png" width="101" height="76" alt="Nagoya University">
  </div>
  <h1>{t['title']}<br><span lang="ja">{j['title']}</span></h1>
  <p class="lead">{t['choose']}<br><span lang="ja">{t['choose2']}</span></p>
  <section class="choice" aria-labelledby="ar">
    <h2 id="ar">AR web page<span lang="ja">ARウェブページ</span></h2>
    <div class="pick"><a href="en/pre-op/">English</a><a href="ja/pre-op/" lang="ja">日本語</a></div>
  </section>
  <section class="choice" aria-labelledby="video">
    <h2 id="video">Narrated video<span lang="ja">ナレーション動画</span></h2>
    <div class="pick"><a href="video/en/">English</a><a href="video/ja/" lang="ja">日本語</a></div>
  </section>
  <ol class="stage-list">{lst}</ol>
  <p class="disclaimer">{t['disclaimer']}<br><span lang="ja">{j['disclaimer']}</span></p>
</main>
<script src="site.js"></script>
</body>
</html>
'''

def redirect(to):
    return f'<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={to}"><link rel="canonical" href="{to}"><a href="{to}">{to}</a>\n'

def write(path, text):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    open(path, 'w').write(text)

write('index.html', home())
for lang in LANGS:
    write(f'{lang}/index.html', redirect('pre-op/'))
    write(f'video/{lang}/index.html', video_page(lang))
    for i, s in enumerate(STAGES):
        write(f'{lang}/{s}/index.html', stage_page(lang, i, s))
print('built')
