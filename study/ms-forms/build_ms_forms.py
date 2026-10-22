"""Build the Microsoft Forms files for the ABG Education Models Study from content.py.
Run: python3 build_ms_forms.py   (needs python-docx)
- quick-import_{EN,JA}.docx: title + the choice and text questions, for Forms > Quick import.
- form-text_{EN,JA}.docx: everything to paste, page by page, each piece saying where it goes.
- form-review_JA.docx: English and Japanese side by side for a native-speaker check (Track Changes on).
Claude cannot build Microsoft Forms; Luke builds the forms from these files (setup-guide.md)."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from docx_util import new_doc, para, table, add_row, NOTE  # noqa: E402
from content import pages, TITLE  # noqa: E402

LETTERS = 'ABCDEFGHIJ'
IMPORT = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q8', 'Q9', 'Q42', 'Q48']  # Likert and ranking questions are added by hand
P = pages()


def lines(x):
    return x if isinstance(x, list) else [x]


def build_import(li, tag):
    doc = new_doc(tag)
    para(doc, TITLE[li], style='Title', justify=False)
    n = 0
    for _, rows in P:
        for rid, *txt, _ in rows:
            if rid not in IMPORT:
                continue
            n += 1
            ls = lines(txt[li])
            q = re.sub(r'\s*\*$', '', ls[0])
            opts = [s[2:] for s in ls[1:] if s.startswith('○ ')]
            para(doc, f'{n}. {q}', justify=False)
            for i, s in enumerate(opts):
                para(doc, f'{LETTERS[i]}. {s}', justify=False)
            para(doc)
    doc.save(os.path.join(HERE, f'quick-import_{tag}.docx'))


def build_text(li, tag):
    doc = new_doc(tag)
    para(doc, f'Text to paste into Microsoft Forms ({tag})', style='Title', justify=False)
    para(doc, 'Grey lines say where each piece goes; copy only the black text. Copying from Word keeps bold and bullets. '
         'Every question has its own section (page): add each section with "Add new" > "Section" just above the question it holds. '
         'Question numbers (Q1-Q48) match the review file and the setup guide. Do not colour the material names: '
         'no colour coding without Luke\'s decision.', color=NOTE, size=9)
    for heading, rows in P:
        para(doc, heading.split(' / ')[0] if li == 0 else heading, style='Heading 1', justify=False)
        for rid, *txt, note in rows:
            where = rid or 'Text'
            para(doc, where + (f' ({note})' if note and rid.startswith('Q') else ''), color=NOTE, size=9, justify=False)
            ls = lines(txt[li])
            bullets = rid == '' and isinstance(txt[li], list)
            for k, s in enumerate(ls):
                para(doc, s, style='List Bullet' if bullets else None, bold=(rid in ('Section title', 'Heading', 'Title') or (rid.startswith('Q') and k == 0)))
    doc.save(os.path.join(HERE, f'form-text_{tag}.docx'))


def build_review():
    doc = new_doc('JA', track=True)
    para(doc, 'Japanese survey: review copy', bold=True, size=14, justify=False)
    para(doc, '日本語版アンケート：確認用', bold=True, size=14, justify=False)
    para(doc, 'ABG Education Models Study (Aichi Gakuin University and Nagoya University). Microsoft Forms survey, Japanese '
         'version for checking, next to the English text. Version 0.1, 22 October 2026.')
    para(doc, 'How to review: please check the Japanese column. If a row is fine, tick OK. To change the Japanese, edit it '
         'directly (Track Changes is already on) or add a Word comment. You can also write in the Comments column. Grey text '
         'in the Comments column is a note from the study team. The word pairs on pages 6 to 13 are the official Japanese '
         'UEQ-S (a standardised questionnaire), so please comment rather than reword them. Some words are written in hiragana '
         'on purpose (for example かん者, 治りょう) so that all participants can read them easily.')
    para(doc, '確認のお願い：「日本語（案）」の列をご確認ください。問題がなければ「OK」欄に✓を付けてください。修正がある場合は、'
         '日本語を直接書き換えるか（変更履歴の記録はオンになっています）、Wordのコメントを付けてください。「コメント」欄に直接'
         '書いていただいても結構です。コメント欄の灰色の文字は研究チームのメモです。フォームのPage 6〜13の語の組は、標準化された'
         '質問票UEQ-Sの公式日本語版のため、言い換えではなくコメントでお知らせください。だれでも読みやすいように、一部の漢字を'
         'わざとひらがなにしています（例：かん者、治りょう）。')
    para(doc, 'Reviewer / 確認者：______________________ Date / 日付：____________ All approved / 全体を承認：☐', justify=False)
    W = [2.2, 5.8, 5.8, 0.9, 3.0]
    for heading, rows in P:
        para(doc, heading, bold=True, size=11.5, justify=False)
        t = table(doc, ['No.', 'English', '日本語（案）', 'OK', 'Comments / コメント'], W)
        for rid, en, ja, note in rows:
            add_row(t, [rid, lines(en), lines(ja), '☐', note], W, colors={4: NOTE})
    doc.save(os.path.join(HERE, 'form-review_JA.docx'))


if __name__ == '__main__':
    for li, tag in enumerate(['EN', 'JA']):
        build_import(li, tag)
        build_text(li, tag)
    build_review()
    print('wrote quick-import, form-text (EN, JA) and form-review_JA.docx')
