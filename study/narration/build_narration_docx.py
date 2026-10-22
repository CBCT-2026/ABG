"""Build narration-script-EN-JA.docx (review copy, Track Changes on) from video/script-en.json and script-ja.json.
Run from the repo root after python3 tools/narration.py: python3 study/narration/build_narration_docx.py"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
from docx_util import new_doc, para, table, add_row, NOTE  # noqa: E402

en = json.load(open(os.path.join(ROOT, 'video/script-en.json'), encoding='utf-8'))
ja = json.load(open(os.path.join(ROOT, 'video/script-ja.json'), encoding='utf-8'))
W = [1.0, 6.6, 6.6, 3.2]


def secs(lang, text):
    return len(text.split()) / 150 * 60 if lang == 'en' else len(re.sub(r'\s', '', text)) / 5.5


doc = new_doc('EN', track=True, landscape=False)
para(doc, 'ABG Education Models Study: narration script (3D printed model and narrated video)', style='Title', justify=False)
para(doc, 'Version 0.1, 22 October 2026. One part per stage, each spoken in 60 seconds or less by a computer voice '
     '(English bf_emma, Japanese jf_alpha, Kokoro-82M, as in the wisdom tooth study). With the 3D printed model it plays as audio only from the study device. The narrated video shows the same '
     'words as subtitles and the line labels in the right column, with the same names as the AR web page and the 2D '
     'information sheet. Track Changes is on: please type edits and add comments directly.')
para(doc, 'Every sentence comes from, or shortens, the web page text for that stage (cbct-2026.github.io/ABG), with the same '
     'sources. To fit 60 seconds, it leaves out: the medical names (alveolar cleft, agenesis, lateral incisor), the '
     'list of reasons for the graft, the best root stage for timing, wound opening, the return to school, and the '
     'details of each choice for the missing tooth. Source text: content/narration.md in the ABG repo.', color=NOTE, size=9)
for ce, cj in zip(en['chapters'], ja['chapters']):
    te = ' '.join(s for p in ce['paragraphs'] for s in p['sentences'])
    tj = ''.join(s for p in cj['paragraphs'] for s in p['sentences'])
    para(doc, f"{ce['title']} / {cj['title']}", style='Heading 1', justify=False)
    para(doc, f"English: {len(te.split())} words, about {secs('en', te):.0f} s.   日本語：{len(re.sub(r'[\\s]', '', tj))}字、約{secs('ja', tj):.0f}秒。",
         color=NOTE, size=9)
    t = table(doc, ['Part', 'English', '日本語', 'Line labels / ラベル'], W)
    for i, (pe, pj) in enumerate(zip(ce['paragraphs'], cj['paragraphs']), 1):
        lab = [f"{en['labels'][k][0]} / {ja['labels'][k][0]}" for k in pe['labels']] or ['–']
        add_row(t, [str(i), ' '.join(pe['sentences']), ''.join(pj['sentences']), lab], W, colors={3: NOTE})
para(doc, 'Notes: Japanese kanji are grade 6 or below. Timing is estimated (150 English words a minute, 5.5 Japanese '
     'characters a second); measure the real recording. Subtitles (.vtt) are made from the recording, so they come '
     'with the video.', color=NOTE, size=9)
out = os.path.join(HERE, 'narration-script-EN-JA.docx')
doc.save(out)
print('wrote', os.path.relpath(out, ROOT))
