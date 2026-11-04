"""Write every page of the site from content/.
Run from the repo root: python3 tools/build.py
Edit content/*.html, content/ui.json and content/references.json, not the pages under en/, ja/, video/ and sheet/.
Also writes the 2D information sheets (sheet/<lang>/<stage>/) and tools/sheet/labels.json for tools/sheet/render.js."""
import json, re, html, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
UI = json.load(open('content/ui.json'))
REFS = json.load(open('content/references.json'))
STAGES = ['pre-op', 'during-braces', 'long-term']
MODEL = 'abg-placeholder'  # placeholder for stages whose model is not built yet
MODELS = {'pre-op': 'abg-1-pre-op', 'during-braces': 'abg-2-during-braces', 'long-term': 'abg-3-long-term'}  # stage -> models/<name>.glb
LANGS = ['en', 'ja']
SITE_URL = 'https://cbct-2026.github.io/ABG/'  # the QR code on the home page opens this (make it with tools/make_qr.py)
# Microsoft Forms for the study (information sheet + survey). Paste each link here, then run this script again.
FORM_EN = ''
FORM_JA = ''

# Labels on the model: position (metres, model axes), surface normal, side of the leader line.
# "when" ties a label to the gum part being on (on-gum) or taken off (off-gum).
H = {
 'gum':     dict(pos='0.034m 0.008m 0.0226m', normal='0 0 1', side='up', len=60, when='on-gum', en=['Gum', 'you can take it off'], ja=['歯ぐき', '外せます']),
 'gap':     dict(pos='0.019m 0.004m 0.021m', normal='0 0 1', side='left', len=24, when='off-gum', en=['Gap in the bone', 'alveolar cleft'], ja=['骨のすき間', 'がくれつ']),
 'window':  dict(pos='0.036m 0.012m -0.004m', normal='0.6 0 0.8', side='up', len=50, when='off-gum', en=['Eye tooth window', 'canine'], ja=['犬歯の窓', '']),
 'central': dict(pos='-0.002m -0.012m 0.0316m', normal='0 0 1', side='down', len=40, en=['Front tooth', 'central incisor'], ja=['前歯', '中切歯']),
 'missing': dict(pos='0.021m -0.010m 0.024m', normal='0 0 1', side='down', len=18, en=['Missing tooth', 'lateral incisor'], ja=['ない歯', '側切歯']),
 'palate':  dict(pos='0.008m 0.0073m -0.01m', normal='0 -1 0', side='left', len=30, when='on-gum', en=['Roof of the mouth', 'palate'], ja=['上あご', 'こうがい']),
 'graft':   dict(pos='0.021m 0.010m 0.027m', normal='0 0 1', side='left', len=44, when='off-gum', en=['New bone', 'bone graft'], ja=['新しい骨', '骨移植']),
 'healed':  dict(pos='0.021m 0.010m 0.027m', normal='0 0 1', side='left', len=44, when='off-gum', en=['New bone', 'healed graft'], ja=['新しい骨', 'ついた骨']),
 'canine':  dict(pos='0.030m -0.003m 0.027m', normal='0 0 1', side='up', len=76, en=['Eye tooth', 'grew through the new bone'], ja=['犬歯', '新しい骨を通って生えた']),
 'braces':  dict(pos='-0.014m -0.006m 0.033m', normal='0 0 1', side='up', len=50, when='on-braces', en=['Braces', 'you can take them off'], ja=['矯正装置', '外せます']),
 'false':   dict(pos='0.021m -0.007m 0.031m', normal='0 0 1', side='down', len=18, when='on-braces', en=['False tooth on the wire', 'lateral incisor'], ja=['ワイヤーの仮の歯', '側切歯']),
 'space':   dict(pos='0.021m -0.004m 0.030m', normal='0 0 1', side='down', len=18, en=['Missing tooth', 'pick an option below'], ja=['ない歯のスペース', '下のボタンで選べます']),
}
LABELS = {'pre-op': ['gum', 'gap', 'window', 'central', 'missing', 'palate'],
          'during-braces': ['gum', 'graft', 'canine', 'braces', 'central', 'palate'],
          'long-term': ['gum', 'healed', 'canine', 'space', 'central', 'palate']}

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

def model_head(up):
    return f'''<script>
// The models are Draco-compressed; the decoder is served from this site, so no outside download is needed.
self.ModelViewerElement = {{ dracoDecoderLocation: new URL('{up}vendor/draco/', location.href).href }};
</script>
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
    src = open(f'content/{stage}-{lang}.html').read()
    for old, new in WEB_SWAP.get((stage, lang), []):
        assert old in src, (stage, lang, old)
        src = src.replace(old, new)
    text, refs = cite(src)
    refs = refs.replace('<a href=', '<a target="_blank" rel="noopener" href=')  # sources open in a new tab, so the material stays open
    spots = ''
    for k, key in enumerate(LABELS[stage]):
        h = H[key]
        cls = 'hotspot' + (' ' + h['when'] if h.get('when') else '')
        small = f'<small>{h[lang][1]}</small>' if h[lang][1] else ''
        spots += f'\n    <div class="{cls}" slot="hotspot-{k + 1}" data-position="{h["pos"]}" data-normal="{h["normal"]}" data-visibility-attribute="visible" data-side="{h["side"]}" style="--len: {h["len"]}px"><span class="label">{h[lang][0]}{small}</span></div>'
    model = MODELS[stage]
    placeholder = '' if (n == 1 or model != MODEL) else f'\n    <div class="placeholder"><span>{t["placeholder"]}</span></div>'
    ios = f' ios-src="{up}models/{model}.usdz"' if os.path.exists(f'models/{model}.usdz') else ''
    poster = f' poster="{up}models/{model}-poster.webp"' if os.path.exists(f'models/{model}-poster.webp') else ''
    prev = f'<a href="../{STAGES[i - 1]}/">← {t[f"st{n - 1}"]}</a>' if i > 0 else '<span></span>'
    nxt = f'<a href="../{STAGES[i + 1]}/">{t[f"st{n + 1}"]} →</a>' if i < 2 else '<span></span>'
    o = 'ja' if lang == 'en' else 'en'
    # Removable parts in the model, switched by site.js through their material names (hidden until the model confirms them).
    parts = ''
    if stage == 'during-braces':
        parts = f'''
  <div class="controls parts" id="parts" role="group" aria-label="{t['partsLabel']}" hidden>
    <button type="button" data-part="braces" aria-pressed="true" data-on="{t['bracesOn']}" data-off="{t['bracesOff']}">{t['bracesOn']}</button>
  </div>'''
    elif stage == 'long-term':
        parts = f'''
  <div class="controls parts" id="parts" role="group" aria-label="{t['partsLabel']}" hidden>
    <button type="button" data-option="option-none" aria-pressed="true">{t['optNone']}</button>
    <button type="button" data-option="option-implant" aria-pressed="false">{t['optImplant']}</button>
    <button type="button" data-option="option-bridge" aria-pressed="false">{t['optBridge']}</button>
    <button type="button" data-option="option-denture" aria-pressed="false">{t['optDenture']}</button>
  </div>'''
    return head(lang, f'{t["title"]} · {t[f"st{n}"]}', up, t[f'alt{n}']) + model_head(up) + f'''<script type="module" src="{up}vendor/model-viewer/model-viewer.min.js"></script>
</head>
<body data-stage="{stage}">
{bar(lang, up, f"{up}{o}/{stage}/")}
<main>
  <h1>{t['title']}</h1>
  {steps(lang, stage, '../')}
  <!-- MODEL: set per stage in MODELS (tools/build.py). See README. -->
  <model-viewer id="mv" src="{up}models/{model}.glb"{ios}{poster}
    alt="{html.escape(t[f'alt{n}'])}"
    ar ar-modes="webxr scene-viewer quick-look" ar-scale="auto"
    camera-controls camera-orbit="0deg 80deg auto" touch-action="pan-y" interaction-prompt="auto"
    shadow-intensity="1" exposure="1.05" loading="eager">
    <button slot="ar-button" class="ar-btn">{t['ar']}</button>{placeholder}{spots}
    <div class="progress" slot="progress-bar"><div class="progress-fill"></div></div>
  </model-viewer>
  <p class="hint" id="hint" data-touch="{t['hintTouch']}" data-mouse="{t['hintMouse']}">{t['hintMouse']}</p>
  <div class="narration"><span id="listen-label">{t['listen']}</span><audio controls preload="none" aria-labelledby="listen-label" src="{up}video/audio/{lang}/stage-{n}.mp3"></audio></div>
  <div class="controls" role="group" aria-label="{t['controls']}">
    <button type="button" data-orbit="0deg 80deg auto" aria-pressed="true">{t['vFront']}</button>
    <button type="button" data-orbit="0deg 165deg auto" aria-pressed="false">{t['vBelow']}</button>
    <button type="button" data-orbit="40deg 75deg 0.11m" data-target="0.028m 0.006m 0.01m" aria-pressed="false">{t['vLeft']}</button>
    <button type="button" id="labels" aria-pressed="false" data-on="{t['hideLabels']}" data-off="{t['showLabels']}">{t['hideLabels']}</button>
    <button type="button" id="gum" class="gum" aria-pressed="false" data-off="{t['gumOff']}" data-on="{t['gumOn']}">{t['gumOff']}</button>
  </div>{parts}

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
  <p class="restart"><button type="button" id="restart" class="again" data-home="../pre-op/">{t['startAgain']}</button></p>
  <p class="disclaimer">{t['disclaimer']}</p>
  <div class="timer" id="timer" hidden><span>{t['timeLeft']}</span> <b id="timer-left"></b></div>
  <div class="timeup gate" id="gate" role="dialog" aria-modal="true" aria-labelledby="gate-msg" hidden><div class="done-card"><h2 class="done-title">{t[f"stage{n}n"]}: {t[f"st{n}"]}</h2><p id="gate-msg">{t['ready']}</p><button type="button" class="start" id="start">{t['start']}</button></div></div>
  <div class="timeup" id="timeup" role="alertdialog" aria-modal="true" aria-labelledby="timeup-msg" hidden><div class="done-card"><svg class="tick" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="22"/><path d="M14 25l7 7 13-15"/></svg><h2 class="done-title">{t['thanks'] if i == 2 else t['stageDone'].format(n=n)}</h2><p id="timeup-msg">{t['timeUp'] if i == 2 else t['stageUp']}</p>{'<button type="button" class="again" data-home="../pre-op/">' + t['startAgain'] + '</button>' if i == 2 else '<a class="next-stage" href="../' + STAGES[i + 1] + '/">' + t['nextStage'] + ' →</a>'}</div></div>
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

def form_link(url, label, lang):
    if url:
        return f'<a href="{url}" lang="{lang}" target="_blank" rel="noopener">{label}</a>'
    return f'<span lang="{lang}" class="soon">{label}<small>Link coming / リンクは準備中</small></span>'

def home():
    t, j = UI['en'], UI['ja']
    lst = ''.join(f'<li><b>{i}</b><span>{t[f"st{i}long"]}<br><span lang="ja">{j[f"st{i}long"]}</span></span></li>' for i in (1, 2, 3))
    return head('en', f'{t["title"]} / {j["title"]}', '') + f'''</head>
<body class="home">
<header class="bar">
  <div class="bar-left">
    <button class="theme" id="theme" type="button" data-dark="Dark mode / ダークモード" data-light="Light mode / ライトモード">Dark mode / ダークモード</button>
  </div>
  <div class="logos">
    <img class="logo" src="images/aichi-gakuin-logo.png" width="44" height="56" alt="Aichi Gakuin University">
    <img class="logo" src="images/nagoya-logo.png" width="74" height="56" alt="Nagoya University">
  </div>
</header>
<main>
  <div class="hero">
    <h1>{t['title']}<span class="h1-ja" lang="ja">{j['title']}</span></h1>
    <p class="lead">{t['choose']}<span lang="ja">{t['choose2']}</span></p>
  </div>
  <section class="choice" aria-labelledby="ar">
    <h2 id="ar">AR web page<span lang="ja">ARウェブページ</span></h2>
    <div class="pick"><a href="en/pre-op/" aria-label="AR web page, English">English</a><a href="ja/pre-op/" lang="ja" aria-label="ARウェブページ、日本語">日本語</a></div>
  </section>
  <section class="choice" aria-labelledby="video">
    <h2 id="video">Narrated video<span lang="ja">ナレーション動画</span></h2>
    <div class="pick"><a href="video/en/" aria-label="Narrated video, English">English</a><a href="video/ja/" lang="ja" aria-label="ナレーション動画、日本語">日本語</a></div>
  </section>
  <section class="stages-card" aria-labelledby="stages-h">
    <h2 id="stages-h">The three stages<span lang="ja">3つの段階</span></h2>
    <ol class="stage-list">{lst}</ol>
  </section>
  <section class="choice study-card" aria-labelledby="form-h">
    <h2 id="form-h">Take part in the study<span lang="ja">研究に参加する</span></h2>
    <p>The form has the information sheet and the survey.<span lang="ja">フォームには、説明書とアンケートがあります。</span></p>
    <div class="pick">{form_link(FORM_EN, 'Open the form (English)', 'en')}{form_link(FORM_JA, 'フォームを開く（日本語）', 'ja')}</div>
  </section>
  <div class="qr-card">
    <button type="button" class="qr-open" id="qr-open" aria-haspopup="dialog"><img src="images/qr-home.svg" width="72" height="72" alt=""><span>Show QR code for this site<span lang="ja">このサイトのQRコードを表示</span></span></button>
  </div>
  <dialog class="qr" id="qr" aria-label="QR code / QRコード">
    <img src="images/qr-home.svg" alt="QR code: {SITE_URL}">
    <p>Scan to open this site<span lang="ja">読み取ると、このサイトが開きます</span></p>
    <p class="qr-url">{SITE_URL.replace('https://', '')}</p>
    <form method="dialog"><button type="submit">Close / 閉じる</button></form>
  </dialog>
  <p class="disclaimer">{t['disclaimer']}<br><span lang="ja">{j['disclaimer']}</span></p>
</main>
<script src="site.js"></script>
</body>
</html>
'''

def redirect(to):
    # The script keeps ?study=1&t=... when someone opens /en/ or /ja/; the meta refresh is the fallback.
    return f'<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><script>location.replace({to!r} + location.search)</script><meta http-equiv="refresh" content="0; url={to}"><link rel="canonical" href="{to}"><a href="{to}">{to}</a>\n'


# 2D information sheet: the same text as the web page, laid out for one side of A4.
# Only sentences about on-screen buttons or parts you can handle change (SHEET_SWAP).
SHEET_SWAP = {
 ('pre-op', 'en'): [('Tap <b>Take off the gum</b> to see the gap in the bone.', 'The pictures show the jaw with and without the gum.')],
 ('pre-op', 'ja'): [('「歯ぐきを外す」をおすと、骨のすき間が見えます。', '図は、歯ぐきがある時と外した時の上あごです。')],
 ('during-braces', 'en'): [('The braces on the model clip on and off.', 'The pictures show the jaw with and without the braces.')],
 ('during-braces', 'ja'): [('模型の装置は、つけたり外したりできます。', '図は、装置がある時と外した時の上あごです。')],
 ('long-term', 'en'): [('The model has parts you can swap to show each choice.', 'The pictures show each choice.')],
 ('long-term', 'ja'): [('模型は、部品をつけかえて、それぞれの方法を見せられます。', '図は、それぞれの方法を見せています。')],
}
# Sentences about the 3D print's parts, which the web page can't do: left out of the web page.
WEB_SWAP = {
 ('during-braces', 'en'): [('  <p>The braces on the model clip on and off.</p>\n', '')],
 ('during-braces', 'ja'): [('  <p>模型の装置は、つけたり外したりできます。</p>\n', '')],
 ('long-term', 'en'): [('  <p>The model has parts you can swap to show each choice.</p>\n', '')],
 ('long-term', 'ja'): [('  <p>模型は、部品をつけかえて、それぞれの方法を見せられます。</p>\n', '')],
}
# Pictures per stage: (image file or None for a placeholder, English caption, Japanese caption).
# All pictures come from tools/sheet/render.js (VIEWS there), rendered from the stage models.
SHEET_FIGS = {
 'pre-op': [('sheet-front-gum-{lang}.png', 'Whole jaw, with the gum', '上あご全体（歯ぐきあり）'),
            ('sheet-front-bone-{lang}.png', 'Gum taken off: the gap in the bone', '歯ぐきを外した所：骨のすき間'),
            ('sheet-below-{lang}.png', 'From below: the roof of the mouth', '下から見た所：上あご'),
            ('sheet-left-{lang}.png', 'Left side: the eye tooth window', '左側：犬歯の窓')],
 'during-braces': [('sheet-s2-braces-{lang}.png', 'Whole jaw: braces on, with the gap kept open', '上あご全体：装置とあけておくすき間'),
                ('sheet-s2-off-{lang}.png', 'Braces taken off: the gap where the small tooth never grew', '装置を外した所：はえてこなかった歯のすき間'),
                ('sheet-s2-bone-{lang}.png', 'Gum taken off: the new bone and the eye tooth', '歯ぐきを外した所：新しい骨と犬歯'),
                ('sheet-s2-below-{lang}.png', 'From below: the roof of the mouth and the braces', '下から見た所：上あごと装置')],
 'long-term': [('sheet-s3-implant-{lang}.png', 'Implant with a crown', 'インプラントとクラウン'),
               ('sheet-s3-bridge-{lang}.png', 'Bridge with one wing', '一まいの羽のブリッジ'),
               ('sheet-s3-plate-{lang}.png', 'Plate with a false tooth', '取り外しできる入れ歯'),
               ('sheet-s3-bone-{lang}.png', 'Gum taken off: the new bone where the gap was', '歯ぐきを外した所：すき間にできた新しい骨')],
}
SHEET_UI = {
 'en': dict(ph='PLACEHOLDER: picture of the {stage} model', how='Render with tools/sheet/render.js once the model is built.',
            note='Pictures of the study model.', footer='This sheet is for a study at Aichi Gakuin University and Nagoya University. Version 0.2, 4 November 2026.'),
 'ja': dict(ph='仮の図：{stage}の模型の図', how='模型ができたら tools/sheet/render.js で作ります。',
            note='研究用の模型の図です。', footer='このシートは、愛知学院大学と名古屋大学の研究のためのものです。バージョン0.2、2026年11月4日。'),
}

def sheet_page(lang, i, stage):
    t = UI[lang]; n = i + 1; u = SHEET_UI[lang]; up = '../../../'
    src = open(f'content/{stage}-{lang}.html').read()
    for a, b in SHEET_SWAP.get((stage, lang), []):
        assert a in src, (stage, lang, a)
        src = src.replace(a, b)
    text, refs = cite(src)
    imp, rest = text.split('</section>', 1)
    figs = ''
    for k, (img, en, ja) in enumerate(SHEET_FIGS[stage]):
        cap = en if lang == 'en' else ja
        if img:
            body = f'<img src="{up}images/{img.format(lang=lang)}" alt="{html.escape(cap)}">'
        else:
            body = f'<div class="ph"><b>{u["ph"].format(stage=t[f"st{n}"])}</b><span>{html.escape(cap)}</span><small>{u["how"]}</small></div>'
        figs += f'\n    <figure class="f{k + 1}">{body}<figcaption>{cap}</figcaption></figure>'
    o = 'ja' if lang == 'en' else 'en'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(t['title'])} · {t[f'st{n}']}</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="{up}sheet/sheet.css">
</head>
<body class="sheet {stage}">
<main>
  <header class="sheet-head">
    <div class="titles"><p class="stage">{t[f'stage{n}n']}: {t[f'st{n}']}</p><h1>{t['title']}</h1></div>
    <div class="logos">
      <img class="logo" src="{up}images/aichi-gakuin-logo.png" alt="Aichi Gakuin University">
      <img class="logo" src="{up}images/nagoya-logo.png" alt="Nagoya University">
    </div>
  </header>
  <!-- Generated by tools/build.py from content/{stage}-{lang}.html. Edit that file, not this page. -->
{imp.strip()}</section>
  <div class="visual n{len(SHEET_FIGS[stage])}">{figs}
  </div>
  <div class="text">
{rest.strip()}
  </div>
  <section class="refs">
    <h2>{t['sources']}</h2>
    <ol>
{refs}
    </ol>
  </section>
  <p class="disclaimer">{u['footer']}</p>
</main>
</body>
</html>
'''

def write(path, text):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    open(path, 'w').write(text)

write('index.html', home())
for lang in LANGS:
    write(f'{lang}/index.html', redirect('pre-op/'))
    write(f'video/{lang}/index.html', video_page(lang))
    for i, s in enumerate(STAGES):
        write(f'{lang}/{s}/index.html', stage_page(lang, i, s))
for lang in LANGS:
    for i, s in enumerate(STAGES):
        write(f'sheet/{lang}/{s}/index.html', sheet_page(lang, i, s))
# Old stage URLs forward to the renamed pages, so printed links keep working.
REDIRECTS = {'short-term': 'during-braces'}
for lang in ('en', 'ja'):
    for old, new in REDIRECTS.items():
        write(f'{lang}/{old}/index.html', f'<!doctype html>\n<html lang="{lang}"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=../{new}/"><link rel="canonical" href="../{new}/"><title>→ {new}</title></head><body><a href="../{new}/">../{new}/</a></body></html>\n')
        write(f'sheet/{lang}/{old}/index.html', f'<!doctype html>\n<html lang="{lang}"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=../{new}/"><link rel="canonical" href="../{new}/"><title>→ {new}</title></head><body><a href="../{new}/">../{new}/</a></body></html>\n')
write('tools/sheet/labels.json', json.dumps(H, ensure_ascii=False, indent=1) + '\n')
print('built')
