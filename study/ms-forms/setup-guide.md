# Microsoft Forms setup guide (ABG, version 0.1, 22 October 2026)

Claude cannot build Microsoft Forms. These files hold all the text; Luke builds one anonymous form per language.
The layout copies the live wisdom tooth form (22 October 2026): one question per page, consent inside the form.

| File | Use |
| --- | --- |
| `quick-import_EN.docx`, `quick-import_JA.docx` | Forms > Quick import: title and the 9 choice and text questions (Q1-Q5, Q8, Q9, Q42, Q48) |
| `form-text_EN.docx`, `form-text_JA.docx` | Everything else to paste, page by page: description, consent text, section titles, the Likert and ranking questions, thank-you message |
| `form-review_JA.docx` | English and Japanese side by side for a native-speaker check (Track Changes on) |
| `content.py` | The one source for all of the above. Edit it, then run `python3 build_ms_forms.py` |

## Form layout (15 pages, 48 questions)

| Page | Contents |
| --- | --- |
| 1 | Consent Form; Q1 agree / do not agree ("do not agree" > End of the form) |
| 2 | Q2 participant number: plain text, the stratified code (e.g. EN-DS-007) |
| 3 | Q3 group, Q4 age (number, 18 or more), Q5 gender, Q6-Q7 English and Japanese level (Likert row, CEFR columns, same CEFR picture as the wisdom tooth form) |
| 4 | Q8 cleft care seen or learned before, Q9 AR used before |
| 5 | Section description for the ratings |
| 6-13 | One UEQ-S word pair per page; the 4 materials as 4 questions, 1-7 (Q10-Q41); Q42 AR check after the last pair |
| 14 | Q43-Q46 understanding: one Likert per material, 3 statements as rows, 7 agreement columns |
| 15 | Q47 ranking, Q48 comments (optional), thank-you message |

## What changed from the wisdom tooth form

- Topic text: description, risks, benefit (teaching students first), thank-you message, Q8, the 3 understanding statements and the ranking question.
- Aichi Gakuin University named with Nagoya University; Professor Toko Hayakawa and Professor Nagato Natsume listed in the study team. Please add Professor Hayakawa's full name in kanji in the Japanese form.
- Materials in study order A-D: 2D Information Sheet, Augmented Reality Web Page, 3D Printed Model, Narrated Video. Rated in this fixed order (Forms cannot shuffle within a section).
- No viewing time in seconds and no survey length: both are set in the pilot. Fill in "[X] minutes".
- No material colours: no colour coding without Luke's decision.
- No Pokémon GO screenshot: it is not under CC0, CC BY or CC BY-SA. The game stays as a word example.
- No approval line.

## Readability

Checked with the patient-education-toolkit. The ABG text is plain, but some fixed parts score above grade 6 / outside grade 6 kanji: the formal study title (alveolar, 口唇口蓋裂, 顎裂部), the group names, "Participant number", 比較 and 必須. These match the wisdom tooth form or are names, so they are left as they are.

## Building each form

1. Quick import `quick-import_<LANG>.docx`; check it shows 9 questions.
2. Paste each page from `form-text_<LANG>.docx`. Add each section with "Add new" > "Section" above the question it holds.
3. Add the Likert questions (pages 6-14) and the ranking question (page 15) by hand, as in the file.
4. Required on everything except Q48. Restrictions > Number on age (18-120).
5. Branching on Q1: "do not agree" > End of the form.
6. Settings: anyone can respond, shuffle off, progress bar on, thank-you message.
7. Test with Preview on a phone, then delete the test responses.
8. Put the two form links in both places that use them: the flyer QR codes (`../recruitment-flyer/build_flyer.py --form-en ... --form-ja ...`) and the Microsoft Forms button at the bottom of the site's landing page. The flyer QR codes go to the forms. The site's own expandable QR code goes to the landing page (https://cbct-2026.github.io/ABG/).
