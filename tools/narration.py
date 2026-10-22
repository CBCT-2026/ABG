"""Write the narrated video scripts video/script-en.json and video/script-ja.json from content/narration.md.
Run from the repo root: python3 tools/narration.py
One chapter per stage. Each paragraph of narration.md is one scene; SCENES names it and lists the line labels it shows.
Label names are the ones on the AR web page (H in tools/build.py); stage 2 and 3 labels get positions once those models exist."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
from build import H  # noqa: E402  (build.py also rebuilds the site; harmless)

EXTRA = {
 'canine':  dict(en=['Eye tooth', 'canine'], ja=['犬歯', '']),
 'graft':   dict(en=['New bone', 'bone graft'], ja=['新しい骨', '骨移植']),
 'braces':  dict(en=['Braces', 'fixed braces'], ja=['装置', '歯につける装置']),
 'implant': dict(en=['Implant', 'with a crown'], ja=['インプラント', 'クラウン']),
 'bridge':  dict(en=['Bridge', 'one wing'], ja=['ブリッジ', '一まいの羽']),
 'plate':   dict(en=['Plate', 'false tooth you can take out'], ja=['入れ歯', '取り外しできる']),
}
SCENES = {
 1: [('intro', []), ('gum', ['gum']), ('missing', ['missing', 'central']), ('canine', ['window']), ('graft', ['gap'])],
 2: [('intro', []), ('graft', ['graft']), ('canine', ['canine']), ('xray', ['graft']), ('hip', [])],
 3: [('intro', []), ('canine', ['canine', 'graft']), ('braces', ['braces']), ('options', ['implant', 'bridge', 'plate'])],
}
UI = json.load(open('content/ui.json'))
VOICE = {'en': 'bf_emma', 'ja': 'jf_alpha'}  # Kokoro-82M voices used in the wisdom tooth study
SPEED = {'en': 1.0, 'ja': 1.1}  # Kokoro's Japanese voice is slow; 1.1 keeps each stage within 45 s
text = open('content/narration.md', encoding='utf-8').read()
parts = {h.strip(): b.strip() for h, b in re.findall(r'^## ([^\n]+)\n(.*?)(?=^## |\Z)', text, re.S | re.M)}
for lang, name in (('en', 'English'), ('ja', 'Japanese')):
    labels = {k: v[lang] for k, v in {**H, **EXTRA}.items()}
    chapters = []
    for n in (1, 2, 3):
        paras = [p.strip() for p in parts[f'Stage {n} {name}'].split('\n\n')]
        assert len(paras) == len(SCENES[n]), (lang, n, len(paras))
        split = (lambda p: re.findall(r'[^。]+。', p)) if lang == 'ja' else (lambda p: re.split(r'(?<=[.?!])\s+', p))
        chapters.append(dict(stage=n, title=f"{UI[lang][f'stage{n}n']}: {UI[lang][f'st{n}']}",
                             paragraphs=[dict(scene=s, labels=l, sentences=split(p)) for (s, l), p in zip(SCENES[n], paras)]))
    out = dict(lang=lang, voice=VOICE[lang], speed=SPEED[lang], title=UI[lang]['title'], labels=labels, chapters=chapters,
               sentence_gap=0.4, paragraph_gap=1.2, chapter_gap=2.5)
    json.dump(out, open(f'video/script-{lang}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', f'video/script-{lang}.json')
