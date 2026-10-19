# Microsoft Forms setup guide (ABG study)

Build two forms in the Nagoya University Microsoft 365 account, one English and one Japanese, the same way as the Wisdom Tooth forms. Start with English, then copy its settings for Japanese.

- `quick-import_EN.docx` / `_JA.docx`: the title and 21 numbered questions, for **Quick import**. Quick import merges headings and descriptions into the text, so those are left out.
- `form-text_EN.docx` / `_JA.docx`: the formatted text to paste in: the form description, 7 sections, the two Likert questions, the ranking question and the thank-you message. Each piece says where it goes. Copying from Word keeps the bold and the bullets.
- `build_ms_forms.py`: rebuilds all four files. All text lives in it. Run `python3 build_ms_forms.py` (needs `python-docx`).

## Form layout (question numbers as shown in Forms once built)

| Section | Questions |
| --- | --- |
| Form description: Why this study, What happens, Free choice, study title | none |
| Consent Form: Privacy, Risks and benefits, Cost, Study team and contact, Consent | 1-6 consent ("I do not agree" ends the form) |
| Study Participant ID | 7 Participant number (number, at least 1) |
| Participant Information | 8 group, 9 age, 10 gender, 11 first language, 12 language(s) spoken most, 13 link to cleft, 14 AR used before, 15 which item first (branches) |
| 2D Pamphlet | 16 UEQ-S, 17 understanding, 18 which item next (branches) |
| 3D Models on the Web Page (AR) | 19 UEQ-S, 20 understanding, 21 did AR open, 22 next (branches) |
| 3D Printed Models | 23 UEQ-S, 24 understanding, 25 next (branches) |
| Final Comparison | 26 ranking, 27 preferred item, 28 comments (optional) |

The order a participant saw the items in comes from questions 15, 18, 22 and 25, checked against the participant number on the order list.

## Steps (do these for each language)

1. **Import:** Forms > New > **Quick import** > `quick-import_EN.docx` (or `_JA`). Check that it shows 21 questions.
2. **Description and sections:** paste parts 1-8 of `form-text_*.docx`. For each section, click the question it names > **Insert new question** > **Section**, then paste the title and description. The Consent Form section goes above question 1.
3. **Likerts:** in each of the three item sections, add Likert A (UEQ-S) and Likert B (understanding) from part 9. Put them above "Which item is next?"; in the web page section, put them above the AR question as well. Use the question title text from the file, not "Likert A". Leave the UEQ-S columns as 1 to 7 (scored -3 to +3 in analysis). Do not reword or reorder the UEQ-S rows.
4. **Ranking:** add the ranking question (part 10) at the top of the Final Comparison section, above the preferred item question.
5. **Question settings:**
   - Required on for everything except the comments question.
   - Participant number: Restrictions > Number, greater than or equal to 1.
   - Both language questions: **Add "Other" option** (remove the imported "Other" choice). Turn on **Multiple answers** for "Language(s) spoken the most".
   - "Any personal link to cleft lip and/or palate?": turn on **Multiple answers**.
   - Group, age and language questions: switch to **Drop-down** if the list looks long on a phone (optional).
6. **Branching** (... > Add branching):
   - Each consent question: "I do not agree" > **End of the form**.
   - "Which item is first?" and each "Which item is next?": each item > its section; "All three are done" > **Final Comparison**.
   - Each section's end: leave as **Next section**; the branching on its last question does the routing.
7. **Settings:**
   - Who can fill out this form: **Anyone can respond** (the form must work on participants' own phones without a Nagoya login).
   - Do not record names; one response per person off (several people use the study iPad).
   - Accept responses on, with start and end dates set after the pilot.
   - Shuffle questions off, progress bar on.
   - Thank-you message: part 11.
   - Email notification of each response: off.
8. **Test:** use Preview on a phone and on the iPad. Do one run with "I do not agree" and one full run in each order branch (start with each of the three items once). Then delete the test responses.
9. **Pilot (5 people):** use participant numbers 901-905 with orders A to E (see the order list) so pilot rows are easy to remove. After the pilot, change the viewing time if needed (edit `CAP_EN` / `CAP_JA` in `build_ms_forms.py`, or edit the three section descriptions by hand), then freeze the forms.
10. **Go live:** Collect responses > copy each link. Send both links here for the QR codes.

## Before each session

- Open the web page on the study iPad, check that "View in AR" works for all 3 stages, and connect the iPad to Wi-Fi.
- Have the order list, a phone timer, the pamphlet, the 3 printed models with all parts, and the card ready.
- If a participant uses the study iPad for the form, open the form in a second tab, not over the web page.

## After data collection

Export the results to Excel each week, save the file to Nagoya University secure storage, and check each participant's answers to questions 15, 18, 22 and 25 match their row on the order list. After the last export, delete the responses from Forms.

## Not in the form (on purpose)

- Completion time: Forms records start and completion times for each response, so no question is needed.
- The optional 3-item true/false knowledge check (handover open question 9) is left out, in line with the project's fixed outcome list. Add it before the pilot if wanted.

## Notes

- English text: FK grade 3.3 overall (consent section 4.9), no "you/your".
- Japanese text: no あなた or 私; only kanji taught by grade 6, except the formal study title, the official UEQ-S items and 韓国語 (same exceptions as the Wisdom Tooth form). Terms match the website: 歯そう骨移植, 口しん口がいれつ, きょう正.
- The form may mention the study iPad; the web page, pamphlet and card must not.
- The Japanese understanding items (Likert B) and the new profile items need forward and back translation review before the freeze, as for the Wisdom Tooth items.
- Ethics placeholders: [committee name] and [number] in the consent section of both forms.
