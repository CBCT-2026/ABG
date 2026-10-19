"""Build the webpages from the shared text, the page strings and the 3D models.

- content/ui-<lang>.json: page strings, numbered dots, buttons and colour key for each stage.
- content/<stage>-<lang>.html: the patient text for each stage. Citations are written as [[key]]
  (keys in content/references.json); they are numbered per page in order of first use, with a source list.
- models/abg-<stage>.glb: if it has empty nodes named hotspot-1, hotspot-2 ... (and view-canine, view-front),
  their positions are written into the page, so the numbered dots sit on the model. Dots with no node are left out.

Writes index.html (language choice: the QR code points here), <lang>/index.html (choose a stage)
and <lang>/<stage>/index.html (one page per stage).
Run: python3 tools/build.py
"""
import json, re, struct
from html import escape
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
REFS = json.loads((ROOT / 'content/references.json').read_text())
LANGS = ('en', 'ja')
REF_TITLE = {'en': 'Sources', 'ja': '参考にした論文'}
MODEL_VIEWER = 'https://cdn.jsdelivr.net/npm/@google/model-viewer@3.5.0/dist/model-viewer.min.js'


# ---------- references ----------

def link(ref):
    if 'doi' in ref:
        return f'<a href="https://doi.org/{ref["doi"]}">doi.org/{ref["doi"]}</a>'
    return f'<a href="{ref["url"]}">{ref["url"].split("://")[1].rstrip("/")}</a>'


def short(text):
    """List up to three authors, then et al."""
    authors, rest = text.split('. ', 1)
    names = [n for n in authors.split(', ') if n != 'et al']
    m = list(re.finditer(r'\. ([^.]+\. \d{4};)', rest))
    if m:
        rest = f'<span class="rt">{rest[:m[-1].start() + 1]}</span> {rest[m[-1].start() + 2:]}'
    return (', '.join(names[:3]) + ', et al' if len(names) > 3 or 'et al' in authors else authors) + '. ' + rest


def render_text(lang, stage):
    text = (ROOT / f'content/{stage}-{lang}.html').read_text()
    order = []
    def cite(m):
        key = m.group(1)
        if key not in REFS:
            raise SystemExit(f'Unknown citation [[{key}]] in content/{stage}-{lang}.html')
        if key not in order:
            order.append(key)
        n = order.index(key) + 1
        return f'<sup class="cite"><a href="#ref-{n}">{n}</a></sup>'
    text = re.sub(r'\[\[(\w+)\]\]', cite, text)
    items = '\n'.join(f'    <li id="ref-{i}">{short(REFS[k]["text"])} {link(REFS[k])}</li>'
                      for i, k in enumerate(order, 1))
    refs = f'<section class="refs">\n  <h2>{REF_TITLE[lang]}</h2>\n  <ol>\n{items}\n  </ol>\n</section>'
    return text.strip() + '\n\n' + refs


# ---------- model nodes ----------

def node_matrix(n):
    if 'matrix' in n:
        return np.array(n['matrix'], dtype=float).reshape(4, 4).T
    t = np.array(n.get('translation', [0, 0, 0]), dtype=float)
    x, y, z, w = n.get('rotation', [0, 0, 0, 1])
    s = np.array(n.get('scale', [1, 1, 1]), dtype=float)
    r = np.array([[1 - 2*(y*y + z*z), 2*(x*y - z*w), 2*(x*z + y*w)],
                  [2*(x*y + z*w), 1 - 2*(x*x + z*z), 2*(y*z - x*w)],
                  [2*(x*z - y*w), 2*(y*z + x*w), 1 - 2*(x*x + y*y)]])
    m = np.eye(4)
    m[:3, :3] = r * s
    m[:3, 3] = t
    return m


def model_points(stage):
    """World positions of the named empty nodes in models/<stage>.glb, and the model's centre."""
    path = ROOT / f'models/{stage}.glb'
    if not path.exists():
        return {}, None
    data = path.read_bytes()
    size = struct.unpack('<I', data[12:16])[0]
    gltf = json.loads(data[20:20 + size])
    nodes = gltf.get('nodes', [])
    points, centre = {}, []
    def walk(i, parent):
        m = parent @ node_matrix(nodes[i])
        name = nodes[i].get('name', '')
        if re.fullmatch(r'(hotspot-\d+|view-[\w-]+)', name):
            points[name] = m[:3, 3]
        if 'mesh' in nodes[i]:
            centre.append(m[:3, 3])
        for c in nodes[i].get('children', []):
            walk(c, m)
    scene = gltf.get('scenes', [{}])[gltf.get('scene', 0)]
    for i in scene.get('nodes', []):
        walk(i, np.eye(4))
    return points, (np.mean(centre, axis=0) if centre else np.zeros(3))


def metres(v):
    return ' '.join(f'{x:.4f}m' for x in v)


# ---------- page parts ----------

def head(lang, title, description, root, model=False):
    draco = (f"\n// The models are Draco-compressed; the decoder is served from this site.\n"
             f"self.ModelViewerElement = {{ dracoDecoderLocation: new URL('{root}vendor/draco/', location.href).href }};") if model else ''
    mv = f'\n<script type="module" src="{MODEL_VIEWER}"></script>' if model else ''
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{escape(description)}">
<meta name="robots" content="noindex">
<script>
// Pick light or dark before the page draws: the saved choice, else the device setting.
try {{ const t = localStorage.getItem('theme'); if (t) document.documentElement.dataset.theme = t; }} catch (e) {{}}{draco}
</script>
<link rel="stylesheet" href="{root}style.css">{mv}
</head>
<body>
'''


def bar(ui, other_href, home_href=None):
    home = f'\n    <a class="lang" href="{home_href}">{ui["home_link"]}</a>' if home_href else ''
    return f'''<header class="bar">
  <div class="bar-left">
    <a class="lang" href="{other_href}" lang="{ui["other"]}" hreflang="{ui["other"]}">{ui["other_label"]}</a>
    <button class="theme" id="theme" type="button" data-dark="{ui["dark"]}" data-light="{ui["light"]}">{ui["dark"]}</button>
  </div>{home}
</header>
'''


def stepper(ui, current):
    items = []
    for s in ui['stages']:
        cur = ' aria-current="page"' if s['id'] == current else ''
        items.append(f'    <li><a href="../{s["id"]}/"{cur}><span class="step-num">{s["num"]}</span>{s["short"]}</a></li>')
    return f'  <nav class="stepper" aria-label="{ui["stage_nav"]}"><ol>\n' + '\n'.join(items) + '\n  </ol></nav>\n'


def stage_files(stage):
    """Model file names for a stage: one per choice, or one for the stage."""
    return [c['file'] for c in stage.get('choices', [])] or [f'abg-{stage["id"]}']


def hotspots(stage, points, centre):
    out = []
    for h in stage['hotspots']:
        p = points.get(f'hotspot-{h["n"]}')
        pos = ''
        if p is not None:
            d = p - centre
            d = d / (np.linalg.norm(d) or 1)
            pos = f' data-position="{metres(p)}" data-normal="{d[0]:.2f} {d[1]:.2f} {d[2]:.2f}"'
        notes = ''.join(f'<span>{n}</span>' for n in h['notes'])
        if 'choice' in h:
            pos += f' data-choice="{h["choice"]}"'
        out.append(f'    <button class="hotspot" slot="hotspot-{h["n"]}"{pos} data-visibility-attribute="visible" '
                   f'aria-label="{h["n"]}. {escape(h["label"])}">{h["n"]}<span class="label">{h["label"]}</span>'
                   f'<span class="note">{notes}</span></button>')
    return '\n'.join(out)


def controls(ui, stage, points):
    out = []
    if stage.get('choices'):
        out.append(f'    <div class="choices" role="group" aria-label="{escape(stage["choices_label"])}">')
        for i, c in enumerate(stage['choices']):
            out.append(f'      <button type="button" class="choice" data-choice="{c["id"]}" data-src="../../models/{c["file"]}.glb" '
                       f'data-ios-src="../../models/{c["file"]}.usdz" aria-pressed="{"true" if i == 0 else "false"}">{c["label"]}</button>')
        out.append('    </div>')
    for i, v in enumerate(stage['views']):
        target = points.get(v.get('target_node', ''))
        t = f' data-target="{metres(target)}"' if target is not None else ''
        out.append(f'    <button type="button" data-orbit="{v["orbit"]}"{t} aria-pressed="{"true" if i == 0 else "false"}">{v["label"]}</button>')
    for p in stage['parts']:
        extra = f' data-with="{p["with"]}"' if 'with' in p else ''
        out.append(f'    <button type="button" class="part" data-part="{p["part"]}" data-mode="{p["mode"]}"{extra} '
                   f'data-on="{escape(p["on"])}" data-off="{escape(p["off"])}" aria-pressed="false" hidden>{p["on"]}</button>')
    out.append(f'    <button type="button" id="labels" aria-pressed="false" data-on="{ui["labels_on"]}" data-off="{ui["labels_off"]}">{ui["labels_on"]}</button>')
    return '\n'.join(out)


def stage_page(lang, ui, i):
    stage = ui['stages'][i]
    sid = stage['id']
    files = stage_files(stage)
    points, centre = {}, None
    for f in files:
        pts, c = model_points(f)
        points = {**pts, **points}
        centre = c if centre is None else centre
    legend = '\n'.join(f'    <li><span class="dot" style="background:{l["color"]}"></span>{l["text"]}</li>' for l in stage['legend'])
    prev = ui['stages'][i - 1] if i > 0 else None
    nxt = ui['stages'][i + 1] if i + 1 < len(ui['stages']) else None
    pager = ''
    if prev:
        pager += f'    <a class="prev" href="../{prev["id"]}/"><span>{ui["prev"]}</span>{prev["num"]}. {prev["short"]}</a>\n'
    if nxt:
        pager += f'    <a class="next" href="../{nxt["id"]}/"><span>{ui["next"]}</span>{nxt["num"]}. {nxt["short"]}</a>\n'
    return (head(lang, stage['title'], stage['description'], '../../', model=True)
            + bar(ui, f'../../{ui["other"]}/{sid}/', '../')
            + f'''
<main>
{stepper(ui, sid)}  <h1>{stage["h1"]}</h1>
  <p class="intro">{ui["intro"]}</p>

  <p class="hint">{ui["hint"]} {stage["hint_extra"]}</p>
  <p class="hint arnote">{ui["arnote"]}</p>

  <!-- MODEL: models/{files[0]}.glb (Draco, under 5 MB) and models/{files[0]}.usdz. See docs/model-spec.md. -->
  <model-viewer id="mv"
    src="../../models/{files[0]}.glb"
    ios-src="../../models/{files[0]}.usdz"
    alt="{escape(stage["alt"])}"
    ar ar-modes="webxr scene-viewer quick-look" ar-scale="auto"
    camera-controls camera-orbit="{stage["views"][0]["orbit"]}" touch-action="pan-y" interaction-prompt="auto"
    shadow-intensity="1" exposure="1" loading="eager" data-missing="{escape(ui["missing"])}">
    <button slot="ar-button" class="ar-btn">{ui["ar_button"]}</button>
{hotspots(stage, points, centre)}
    <div class="progress" slot="progress-bar"><div class="progress-fill"></div></div>
  </model-viewer>
  <div class="info" id="info" aria-live="polite" hidden></div>
  <div class="controls" role="group" aria-label="{ui["controls_label"]}">
{controls(ui, stage, points)}
  </div>

  <ul class="legend" aria-label="{ui["legend_label"]}">
{legend}
  </ul>

  <!-- SHARED TEXT: generated from content/{sid}-{lang}.html by tools/build.py. Edit that file, not this block. -->
{render_text(lang, sid)}

  <nav class="pager">
{pager}  </nav>

  <p class="disclaimer">{ui["disclaimer"]}</p>
</main>

<script src="../../viewer.js"></script>
</body>
</html>
''')


def home_page(lang, ui):
    intro = '\n'.join(f'  <p class="intro">{p}</p>' for p in ui['home']['intro'])
    important = re.search(r'<section class="important">.*?</section>', (ROOT / f'content/pre-op-{lang}.html').read_text(), re.S).group(0)
    buttons = '\n'.join(f'    <a href="{s["id"]}/"><span class="step-num">{s["num"]}</span><span class="pick-text"><b>{s["button"]}</b>'
                        f'<span>{s["age"]}</span></span></a>' for s in ui['stages'])
    return (head(lang, ui['site_title'], ui['home']['description'], '../')
            + bar(ui, f'../{ui["other"]}/')
            + f'''
<main>
  <h1>{ui["home"]["h1"]}</h1>
{intro}
  <h2 class="pick-title">{ui["home"]["choose"]}</h2>
  <div class="stage-pick">
{buttons}
  </div>
{important}
  <p class="disclaimer">{ui["disclaimer"]}</p>
</main>

<script src="../viewer.js"></script>
</body>
</html>
''')


def language_page():
    return '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Alveolar Bone Grafting</title>
<meta name="robots" content="noindex">
<link rel="stylesheet" href="style.css">
</head>
<body>
<main>
  <h1>Choose a language<br><span lang="ja">言語をえらんでください</span></h1>
  <div class="pick">
    <a href="en/">English</a>
    <a href="ja/" lang="ja">日本語</a>
  </div>
</main>
</body>
</html>
'''


if __name__ == '__main__':
    (ROOT / 'index.html').write_text(language_page())
    for lang in LANGS:
        ui = json.loads((ROOT / f'content/ui-{lang}.json').read_text())
        (ROOT / lang).mkdir(exist_ok=True)
        (ROOT / f'{lang}/index.html').write_text(home_page(lang, ui))
        for i, s in enumerate(ui['stages']):
            d = ROOT / lang / s['id']
            d.mkdir(exist_ok=True)
            (d / 'index.html').write_text(stage_page(lang, ui, i))
            files = stage_files(s)
            found = {k for f in files for k in model_points(f)[0] if k.startswith('hotspot-')}
            have = [f for f in files if (ROOT / f'models/{f}.glb').exists()]
            print(f'{lang}/{s["id"]}: models {len(have)}/{len(files)} found, '
                  f'{len(found)}/{len(s["hotspots"])} dots placed')
