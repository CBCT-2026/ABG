"""ABG survey text, English and Japanese. One source for every Microsoft Forms file (build_ms_forms.py).
Follows the live wisdom tooth form (22 October 2026): one question per page, 8 UEQ-S word pairs with the 4 materials,
3 understanding statements per material, ranking, comments. Changes for ABG are marked in the notes.
Each page: (heading, [rows]). Row: (id, English, Japanese, note). English/Japanese can be a list of lines."""

TITLE = ('Bone Graft for a Cleft in the Gum: Three Stages', '歯ぐきの骨のすき間をうめる手術：3つの段階')
FORMAL = ('Seeing the stages: comparing 2D, augmented reality, video and 3D printed education materials to explain '
          'alveolar bone grafting in cleft lip and palate',
          '段階を見る ― 口唇口蓋裂の顎裂部骨移植の説明における、2D、拡張現実（AR）、動画、3Dプリント教材の比較')
# Materials in study order A-D (2D sheet, AR web page, 3D print, video). Rated in this fixed order.
M = (['2D Information Sheet', 'Augmented Reality Web Page', '3D Printed Model', 'Narrated Video'],
     ['2D説明シート', '拡張現実ウェブページ', '3Dプリントモデル', 'ナレーション付き動画'])
UEQ = [('Obstructive', 'Supportive', '妨げになる', '助けられる'), ('Complicated', 'Easy', '複雑', '簡単'),
       ('Inefficient', 'Efficient', '効率が悪い', '効率が良い'), ('Confusing', 'Clear', 'ごちゃごちゃしている', 'すっきりしている'),
       ('Boring', 'Exciting', '退屈だ', 'エキサイティングだ'), ('Not interesting', 'Interesting', 'おもしろくない', 'おもしろい'),
       ('Conventional', 'Inventive', '従来どおり', '独特だ'), ('Usual', 'Leading edge', '普通', '斬新的')]
CEFR = (['None', 'A1 - Beginner', 'A2 - Elementary', 'B1 - Intermediate', 'B2 - Upper intermediate', 'C1 - Advanced', 'C2 - Proficient'],
        ['知識なし', 'A1 入門', 'A2 初級', 'B1 中級', 'B2 中上級', 'C1 上級', 'C2 熟達'])
UND = (['This helped me understand where the gap in the bone is and which tooth is missing.',
        'This helped me understand how the jaw and teeth change across the three stages.',
        'This would help a patient and their family understand the treatment.'],
       ['この資料で、骨のすき間がどこにあり、どの歯がないのかが理解できた。',
        'この資料で、3つの段階で上あごと歯がどう変わるのかが理解できた。',
        'この資料は、かん者と家族が治りょうを理解する助けになると思う。'])
AGREE = (['Strongly disagree', 'Disagree', 'Slightly disagree', 'Neutral', 'Slightly agree', 'Agree', 'Strongly agree'],
         ['全くそう思わない', 'そう思わない', 'あまりそう思わない', 'どちらともいえない', 'ややそう思う', 'そう思う', 'とてもそう思う'])
GROUPS = (['Dentist', 'Dental student', 'Medical doctor', 'Medical student', 'Member of the public (no health training)',
           'Oral and maxillofacial surgeon',
           'Other healthcare worker (for example nurse, speech pathologist, dental hygienist, pharmacist, technician or other)'],
          ['歯科医師', '歯学部生', '医師', '医学部生', '医りょう系の資格・教育のない方', '口くう外科医',
           'その他の医りょうの仕事（看護師、言語ちょうかく士、歯科衛生士、薬ざい師、技師など）'])


def o(a):
    return ['○ ' + s for s in a]


def pages():
    P = []
    P.append(('Form title and description / フォームのタイトルと説明', [
        ('Title', TITLE[0], TITLE[1], 'Same title as the AR web page.'),
        ('Intro', 'An Aichi Gakuin University and Nagoya University study. It takes about [X] minutes to take part in the survey.',
         '愛知学院大学と名古屋大学の研究です。アンケートへの参加には約［X］分かかります。',
         'Time to be set in the pilot (wisdom tooth form: about 10 minutes).'),
        ('Why', 'Why this study: Some children are born with a cleft lip and palate. Many have a gap in the bone that holds the '
                'teeth. An operation called a bone graft fills this gap, and treatment goes on for years. This study compares '
                'four ways to explain three stages of this treatment: before surgery, about 3 months after, and years later.',
         'この研究について：生まれつき口の割れ目（こうしんこうがいれつ）がある子どもがいます。多くの子どもは、歯をささえる骨に'
         'すき間があります。骨移植という手術でこのすき間をうめ、治りょうは何年も続きます。この研究では、この治りょうの3つの段階'
         '（手術の前、約3か月後、数年後）を説明する4つの方法をくらべます。', 'New text for ABG.'),
        ('What', 'What happens: Look at the four patient education materials, one after the other, for a short, fixed time each, '
                 'in a randomised order: a 2D information sheet (printed on paper), an augmented reality (AR) model on a web page '
                 '(shown on the study iPad), a 3D printed model with a short spoken explanation (audio only) and a narrated video of the 3D model. Each one shows all three '
                 'stages. After all four patient education materials have been seen, answer the questions on this form.',
         '参加の内容：4つのかん者向け説明資料を、ランダムな順番で1つずつ、決められた短い時間で見ます：2D説明シート（紙に印刷）、'
         'ウェブページ上の拡張現実（AR）モデル（研究用のiPadで見ます）、短い音声の説明が付いた3Dプリントモデル、3Dモデルのナレーション付き動画。'
         'どの資料も3つの段階すべてを説明しています。4つすべてを見たあとで、このフォームの質問に答えます。',
         'Viewing time per material is set in the pilot, so no seconds are given. Materials listed in study order A-D. The print plays the narration as audio only from the study device (Luke, 22 Oct 2026).'),
        ('Choice', 'Free choice: Taking part is your choice. Saying no does not change study, work or care at Aichi Gakuin '
                   'University or Nagoya University. To stop and not participate, close this form. Nothing is saved until the '
                   '"Submit" button is pressed.',
         '参加は自由です：参加しなくても、愛知学院大学と名古屋大学での学業、仕事、しんりょうに、えいきょうはありません。参加を'
         'やめるときは、このフォームを閉じてください。「送信」ボタンをおすまで、回答は保存されません。',
         'Aichi Gakuin University added, as its patients and students may take part.'),
        ('Study title', f'Study title: {FORMAL[0]}.', f'研究名：{FORMAL[1]}',
         'Japanese study title is a new translation, built like the wisdom tooth one. Please check the medical terms (顎裂部骨移植, 口唇口蓋裂).'),
        ('Required', '* Required', '* 必須', "Shown by Microsoft Forms automatically in the form's language."),
    ]))
    P.append(('Page 1: Consent Form / 同意書', [
        ('Section title', 'Consent Form', '同意書', ''),
        ('Heading', 'Privacy', '回答のあつかい', ''),
        ('', ['No name, email, or student or staff number is asked.',
              'Answers have no name on them. So, after "Submit," an answer cannot be found or taken out.',
              'Answers are collected with Microsoft Forms in the Nagoya University Microsoft 365 account, then moved to safe '
              'Nagoya University storage. They are kept for at least 10 years after the results are published, then permanently deleted.',
              'Results are shared only as group results. A data file with no names may be shared for research.'],
         ['名前、メールアドレス、学生番号、職員番号は聞きません。',
          '回答には名前が付いていません。そのため「送信」のあとは、回答を見つけたり取り消したりできません。',
          '回答は名古屋大学のMicrosoft 365アカウントのMicrosoft Formsで集め、名古屋大学の安全な保存場所に移します。'
          '結果の発表から少なくとも10年間保存し、そのあと完全に消去します。',
          '結果は全体の結果としてのみ発表します。名前のない回答データを、研究のために共有することがあります。'], 'Same as the wisdom tooth form.'),
        ('Heading', 'Risks and benefits', '危険と利益', ''),
        ('', ['The risks are very small. The patient education materials show surgery on a child\'s jaw. This may worry some people.',
              'This study gives no personal advice. Anyone with questions about cleft care should talk with their cleft team or dentist.',
              'When using augmented reality, stay seated or watch the space around.',
              'There is no direct benefit. The results may help teach students and explain this treatment more clearly.'],
         ['危険はほとんどありません。資料では、子どもの上あごの手術を説明しています。不安に感じる人もいるかもしれません。',
          'この研究では、一人一人への助言はしません。口の割れ目の治りょうについて質問がある人は、口の割れ目のチームや歯科医師に相談してください。',
          '拡張現実を使うときは、座ったまま、または周りに気を付けてください。',
          '参加した人への直接の利益はありません。結果は、学生の教育や、この治りょうをより分かりやすく説明するのに役立つかもしれません。'],
         'Rewritten for ABG: the topic, who to ask, and the benefit (teaching students first).'),
        ('Heading', 'Cost', '費用', ''),
        ('', 'Participation is free.', '参加は無料です。', ''),
        ('Heading', 'Study team and contact', '研究をする人・問い合わせ先', ''),
        ('', 'Dr Markus Seifert, PhD student, International Medicine Education, School of Medicine, Nagoya University.',
         'Markus Seifert（医師、名古屋大学 医学部 International Medicine Education 博士課程学生）', 'As in the wisdom tooth form.'),
        ('', 'Professor Toko Hayakawa and Professor Nagato Natsume, Aichi Gakuin University.',
         '早川教授、夏目長門教授（愛知学院大学）', 'New. Please add Professor Hayakawa\'s full name in kanji.'),
        ('', 'For any questions or concerns please email seifert.markus.luke.f5@s.mail.nagoya-u.ac.jp.',
         '質問や意見は、メールでお問い合わせください：seifert.markus.luke.f5@s.mail.nagoya-u.ac.jp', ''),
        ('', 'GitHub repository: https://github.com/CBCT-2026/ABG', 'GitHubリポジトリ：https://github.com/CBCT-2026/ABG', ''),
        ('Heading', 'Consent', '同意', ''),
        ('', 'Taking part means:', '参加するということは、次のことを意味します：', ''),
        ('', ['being 18 years old or older;', 'having read and understood the information above;',
              'knowing that taking part is my choice and I can stop at any time before "Submit";',
              'knowing that answers have no name on them and cannot be taken back after "Submit";',
              'agreeing that answers with no name on them can be published and shared for research.'],
         ['18さい以上であること。', '上の説明を読み、理解したこと。', '参加は自由で、「送信」の前ならいつでもやめられると知っていること。',
          '回答には名前が付かず、「送信」のあとは取り消せないと知っていること。', '名前のない回答が、研究のために発表・共有されることに同意すること。'], ''),
        ('Q1', ['Consent to take part in this study *', *o(['I agree to the above', 'I do not agree to the above'])],
         ['この研究への参加の同意 *', *o(['上の内容に同意する', '上の内容に同意しない'])], '"I do not agree" > End of the form.'),
    ]))
    P.append(('Page 2: Study Participant ID / 参加者ID', [
        ('Section title', 'Study Participant ID', '参加者ID', ''),
        ('Q2', 'Participant number (given by staff, for example EN-DS-007) *', '参加者番号（担当者が伝えます。例：JA-DS-007） *',
         'Text answer, not a number: the stratified code (form language × background).'),
    ]))
    P.append(('Page 3: Participant Information / 参加者について', [
        ('Section title', 'Participant Information', '参加者について', ''),
        ('Description', 'A few questions about the participant. No name or identifying information is requested.',
         '参加者についての質問です。名前や、個人が分かる情報は聞きません。', ''),
        ('Q3', ['Which group fits you the best? *', *o(GROUPS[0])], ['一番当てはまるグループはどれですか？ *', *o(GROUPS[1])], ''),
        ('Q4', ['Age (in years) *', 'Check: Please enter a number greater than or equal to 18'],
         ['年れい（さい） *', 'チェック：18以上の数字を入力してください'], ''),
        ('Q5', ['Gender *', *o(['Man', 'Woman', 'Non-binary', 'Prefer not to say', 'Other'])],
         ['性別 *', *o(['男性', '女性', 'ノンバイナリー', '答えない', 'その他'])], ''),
        ('Q6', ['How well can you read, speak and understand English? *', 'Row: English fluency', 'Columns: ' + ' / '.join(CEFR[0])],
         ['英語を読む・話す・理解する力は、どのくらいですか？ *', '行：英語の力', '列：' + ' / '.join(CEFR[1])],
         'As the live wisdom tooth form, with the CEFR levels picture (cefr-levels-EN/JA.png).'),
        ('Q7', ['How well can you read, speak and understand Japanese? *', 'Row: Japanese fluency', 'Columns: ' + ' / '.join(CEFR[0])],
         ['日本語を読む・話す・理解する力は、どのくらいですか？ *', '行：日本語の力', '列：' + ' / '.join(CEFR[1])], ''),
    ]))
    P.append(('Page 4: cleft and AR experience / 口の割れ目と拡張現実の経験', [
        ('Q8', ['Before today, had you seen or learned about treatment for cleft lip and palate? *',
                *o(['Yes, in my studies or work', 'Yes, in my own life or family', 'No', 'Not sure'])],
         ['今日より前に、口の割れ目（こうしんこうがいれつ）の治りょうを見たり学んだりしたことはありますか？ *',
          *o(['はい、学業や仕事で', 'はい、自分や家族のことで', 'いいえ', '分からない'])],
         'Replaces "Have you ever had a wisdom tooth taken out?". Prior knowledge may affect ratings.'),
        ('Q9', ['Have you ever used augmented reality (AR) on a phone or tablet before? *',
                'For example, Pokémon GO uses AR to show game characters in the real world through the phone camera.',
                *o(['Yes', 'No', 'Not sure'])],
         ['スマートフォンやタブレットで拡張現実（AR）を使ったことはありますか？ *',
          '例：ポケモンGOは、ARを使って、スマートフォンのカメラを通して見た本当の景色の中に、ゲームのキャラクターを表示します。',
          *o(['はい', 'いいえ', '分からない'])],
         'No Pokémon GO screenshot: it is not CC0, CC BY or CC BY-SA. The game name stays as a word example.'),
    ]))
    P.append(('Page 5: Rating the Patient Education Materials / かん者向け説明資料の評価', [
        ('Section title', 'Rating the Patient Education Materials', 'かん者向け説明資料の評価', ''),
        ('Description', 'Each page is one pair of words. Rate each of the four materials on it, from 1 (the left word) to 7 '
                        '(the right word). There are no right or wrong answers. Go with your first impression.',
         '各ページには、1組のことばがあります。4つの資料をそれぞれ、1（左のことば）から7（右のことば）で評価してください。'
         '正解・不正解はありません。直感で答えてください。', ''),
    ]))
    q = 9
    for i, (l, r, jl, jr) in enumerate(UEQ):
        rows = [('Section title', f'{l} or {r}', f'「{jl}」か「{jr}」か',
                 'UEQ-S: official Japanese wording. Standardised items, so please comment rather than reword.' if i == 0 else '')]
        for k in range(4):
            q += 1
            rows.append((f'Q{q}', [f'{M[0][k]} *', f'1 2 3 4 5 6 7  (1 = {l}, 7 = {r})'],
                         [f'{M[1][k]} *', f'1 2 3 4 5 6 7  （1＝{jl}、7＝{jr}）'], ''))
        P.append((f'Page {6 + i}: {l} or {r} / 「{jl}」か「{jr}」か', rows))
    P.append(('Page 13 (continued): AR check / ARの確認', [
        ('Q42', ['Did the model open in augmented reality (shown in the room)? *',
                 *o(['Yes, it worked', 'I tried, but it did not work', 'I did not try to open it'])],
         ['モデルは拡張現実（部屋の中に表示）で表示できましたか？ *', *o(['はい、表示できた', '試したが、うまくいかなかった', '開こうとしなかった'])], ''),
    ]))
    rows = [('Section title', 'Rating Understanding', '理解の評価', ''),
            ('Description', 'Each question below applies to one patient education material. Choose how much each statement fits it.',
             '下の質問は、それぞれ1つのかん者向け説明資料についてです。それぞれの文が、その資料にどのくらい当てはまるかを選んでください。', '')]
    for k in range(4):
        rows.append((f'Q{43 + k}', [f'{M[0][k]} *', *['Row: ' + s for s in UND[0]], 'Columns: ' + ' / '.join(AGREE[0]) if k == 0 else 'Columns: as Q43'],
                     [f'{M[1][k]} *', *['行：' + s for s in UND[1]], '列：' + ' / '.join(AGREE[1]) if k == 0 else '列：Q43と同じ'],
                     'Three ABG statements: where (anatomy), change over the stages, and use for a patient and family.' if k == 0 else ''))
    P.append(('Page 14: Rating Understanding / 理解の評価', rows))
    P.append(('Page 15: Final Comparison / 最後の比較', [
        ('Section title', 'Final Comparison', '最後の比較', ''),
        ('Description', 'Please use the questions below to rank the four patient education materials and if you want to, provide any additional information.',
         '下の質問で、4つのかん者向け説明資料に順位を付けてください。ほかに伝えたいことがあれば、書いてください。', ''),
        ('Q47', ['Please put the four materials in order, from most helpful (top) to least helpful (bottom), for understanding the bone graft and its three stages. *',
                 *['≡ ' + m for m in M[0]]],
         ['骨移植とその3つの段階を理解するのに、一番役に立つもの（上）から一番役に立たないもの（下）の順に、4つを並べてください。 *',
          *['≡ ' + m for m in M[1]]], ''),
        ('Q48', ['Any comments? (optional)', '[Enter your answer]'], ['ご意見があれば書いてください（任意）', '［回答を入力してください］'], ''),
        ('Thank you', 'Many thanks for taking part. For questions about cleft care, please talk to a cleft team or dentist.',
         'ご参加ありがとうございました。口の割れ目の治りょうについて質問がある場合は、口の割れ目のチームや歯科医師に相談してください。',
         'Settings > Customize thank you message.'),
    ]))
    return P
