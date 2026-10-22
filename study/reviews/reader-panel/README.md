# Simulated reader panel (pre-test)

10 AI personas (`personas.json`) each read the EN sheet text (`material-sheet-en.txt`) or heard the EN narration once
(`material-narration-en.txt`), then answered `questions-for-readers.txt` without outside knowledge. Answers are in
`answers/`; judged against `questions.json`; tallied with `pitk panel results-<material>.json` (`panel-report.txt`).

Result: every key message found and understood by 10/10 readers for both materials.

Limits: AI readers have a ceiling effect (they read everything and remember perfectly), so this only shows that each
message is present and stated clearly. It does not replace testing with real readers (MHRA: 20 people), and the
Japanese versions were not tested. Extra detail readers picked up from the sheet but not the narration: medical names
(alveolar cleft, lateral incisor), timing by tooth growth rather than age, return to school after about 2 weeks.
