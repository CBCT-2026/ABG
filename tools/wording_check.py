"""Wording rules for the patient text, checked on every built page.

- English pages: no "you" or "your".
- Japanese pages: no あなた or 私, and only kanji taught in primary school (grades 1 to 6, MEXT 2020 list,
  1,026 kanji, in tools/kyoiku-kanji-2020.txt, taken from KANJIDIC2 via the npm package kanji 0.19.3).
The source list is left out (titles of papers are in English).
Run: python3 tools/wording_check.py  (exit code 1 if anything is found)
"""
import re, sys
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
GRADE6 = set((ROOT / 'tools/kyoiku-kanji-2020.txt').read_text().strip())


def visible(path):
    soup = BeautifulSoup(path.read_text(), 'html.parser')
    for x in soup.select('.refs, script, style'):
        x.decompose()
    attrs = ' '.join(v for el in soup.find_all(True) for k, v in el.attrs.items()
                     if k in ('alt', 'aria-label', 'data-on', 'data-off', 'data-dark', 'data-light', 'data-missing', 'content', 'title'))
    return soup.get_text(' ') + ' ' + attrs


problems = []
for path in sorted(ROOT.glob('en/**/index.html')):
    for m in re.finditer(r'\b(you|your|yours|yourself)\b', visible(path), re.I):
        problems.append(f'{path.relative_to(ROOT)}: "{m.group(0)}"')
for path in sorted(ROOT.glob('ja/**/index.html')):
    text = visible(path)
    for w in ('あなた', '私'):
        if w in text:
            problems.append(f'{path.relative_to(ROOT)}: {w}')
    bad = sorted({c for c in text if '一' <= c <= '鿿' and c not in GRADE6})
    for c in bad:
        i = text.index(c)
        problems.append(f'{path.relative_to(ROOT)}: kanji {c} not taught by grade 6 ("{text[max(0, i - 8):i + 8].strip()}")')

print('\n'.join(problems) or 'No problems found.')
sys.exit(1 if problems else 0)
