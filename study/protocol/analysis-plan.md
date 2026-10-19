# Study protocol and analysis plan: ABG Education Models Study

Hypotheses, design, sample size and analysis plan, fixed before the first participant. Items in [square brackets] need Luke's input.

---

## Study information

### Title
Comparing a 2D pamphlet, an augmented reality 3D model and 3D printed models for explaining alveolar bone grafting in cleft lip and palate: a within-participant study

### Authors
Markus Seifert, Department of International Medicine Education, School of Medicine, Nagoya University. [Co-authors and affiliations]

### Description
Alveolar bone grafting (ABG) fills the bony gap in the upper gum (alveolar cleft) in children with cleft lip and palate, usually before the permanent canine erupts. Explaining the operation is hard because the cleft is a 3D structure and the treatment runs over several years. This study compares three formats that carry the same written text and cover the same three stages in clinical order (pre-operative, short-term post-operative, and long-term after canine eruption and orthodontic treatment):

1. a 2D printed pamphlet with images rendered from the 3D models;
2. a web page with interactive 3D models and augmented reality (AR), shown on a study tablet;
3. 3D printed models with removable parts and a printed card with the same text.

Each adult participant sees all three formats in one session, in one of six counterbalanced orders, and rates each format on the UEQ-S and three study-specific understanding items. The design follows the Wisdom Tooth Education Models Study by the same team.

### Hypotheses
Primary outcome: UEQ-S pragmatic quality.

- **H1:** The AR web page is rated higher than the pamphlet.
- **H2:** The 3D printed models are rated higher than the pamphlet.
- **H3 (two-sided, no directional prediction):** The AR web page and the 3D printed models differ.

H1 and H2 are directional predictions, tested two-sided. Secondary (same structure): understanding score, UEQ-S hedonic quality and overall score.

Exploratory: the pamphlet vs 3D difference is larger in caregivers, people with a cleft and laypeople than in clinicians and students.

## Design plan

### Study type
Experiment: a within-participant (crossover) study with three conditions, single session, no follow-up.

### Blinding
No blinding. Participants and facilitators know which format is in use. Facilitators are independent of the study lead and follow a fixed script; the study lead does not recruit participants or run sessions.

### Study design
Within-participant, 3 formats x 3 periods. All six possible format orders are used (Williams design for three conditions: two 3x3 Latin squares), so each format appears equally often in each period and follows each other format equally often.

Each format is shown for a fixed time of [120 s; final value set after the pilot], timed by the facilitator. Within each format the three stages are always shown in clinical order. After each format, participants rate it on the anonymous online form. After all three, they rank the formats and choose a preferred format.

The written text is identical in all three formats (the printed card leaves out only the model pictures and uses numbered stickers on the models). English text is at or below Flesch-Kincaid grade 6; Japanese text uses only kanji taught by grade 6. Before data collection, the materials pass an expert PEMAT check (PEMAT-P for the pamphlet and card, PEMAT-A/V for the web page; two raters per language who did not make the materials; anything under 70% understandability is revised), then a pilot with five people, after which all materials and forms are frozen. Frozen versions: [repository commit / Zenodo DOI].

### Randomization
Format order comes from a pre-set list for participant numbers 1 to 100, generated before data collection: the six orders shuffled in blocks of six (Python `random`, seed 20261019; script and list attached). Each new participant receives the next unused number regardless of group or language, so orders stay balanced at every multiple of six. Numbers are never skipped or reused. Pilot participants use separate numbers (901-905) and are not analysed.

## Sampling plan

### Data collection procedures
- **Setting:** Nagoya University [and Aichi Gakuin University, if covered by the ethics approval]. Convenience sampling by direct approach.
- **Inclusion:** aged 18 or over; reads English or Japanese; gives consent in the form.
- **Exclusion:** people who made or rated the materials (study team, PEMAT raters, pilot participants).
- **Groups (self-reported, first that fits):** (1) parents or caregivers of a child with a cleft; (2) people with a cleft lip and/or palate; (3) members of the public with no health training; (4) dental or medical students; (5) dentists or orthodontists; (6) oral and maxillofacial, cleft or plastic surgeons, or other medical doctors; (7) other healthcare workers.
- **Form:** one anonymous Microsoft Form per language (English, Japanese) in the Nagoya University Microsoft 365 account, with consent inside the form. Answered on the participant's own phone (QR code) or the study tablet. No names or contact details are collected; answers are saved only on submission.
- **Payment:** none.
- **Ethics:** [committee name], Nagoya University, approval number [number] [amendment for this design, if needed].

### Sample size
48 participants with complete data.

### Sample size rationale
Paired comparison with a medium within-person effect (dz = 0.5), 80% power, two-sided alpha 0.05/3 = 0.0167 (the most stringent step of the Holm correction over three pairwise contrasts): n = 45 (statsmodels `TTestPower`). Rounded up to 48, the next multiple of six, so each of the six orders is used eight times. Group comparisons are exploratory and not powered.

### Stopping rule
Data collection stops when 48 participants have submitted complete forms, or on [end date], whichever comes first. If a participant stops early, the next number is used, so the final sample may slightly unbalance the orders; the achieved order counts will be reported.

## Variables

### Manipulated variables
- **Format** (within participant): 2D pamphlet; AR web page; 3D printed models.
- **Period** (position in the sequence): 1, 2, 3, set by the order list.

### Measured variables
After each format:
- **UEQ-S** (Schrepp et al. 2017): 8 official item pairs, official English and Japanese versions, not reworded, 7-point scale scored -3 to +3. Items 1-4 pragmatic quality; items 5-8 hedonic quality.
- **Understanding:** three study-specific items, 7-point agreement (1 strongly disagree to 7 strongly agree):
  - U1. This helped me understand where the gap in the bone is and what the bone graft fills.
  - U2. This helped me understand why the bone graft is done before the adult canine tooth comes through.
  - U3. This helped me understand what happens after the operation, soon after and later with braces.
- **AR check** (after the web page only): AR worked / tried but did not work / did not try.

After all three formats:
- **Ranking** of the three formats, most to least helpful for understanding ABG.
- **Preferred format** to explain the operation if it were planned for the participant or their child.

Profile: group, age group, gender, first language, language(s) used most, personal link to cleft lip and/or palate, prior AR use, form language. Completion time is taken from the form's start and submit times.

### Indices
- **Pragmatic quality (primary):** mean of UEQ-S items 1-4 (-3 to +3).
- **Hedonic quality:** mean of items 5-8. **UEQ-S overall:** mean of all 8.
- **Understanding score:** mean of U1-U3 (1 to 7).

## Analysis plan

### Statistical models
**Primary:** linear mixed model for pragmatic quality, with fixed effects format, period, group and language, and a random intercept per participant:

`PQ ~ format + period + group + language + (1 | participant)`

Fitted by REML in R (`lme4`, `lmerTest`, Satterthwaite degrees of freedom). The three pairwise format contrasts (estimated marginal means, `emmeans`) are reported with Holm-adjusted p values, 95% confidence intervals and within-person standardised differences.

If any group has fewer than 6 participants, groups are merged before fitting into: cleft community (1, 2), public (3), students (4), clinicians (5-7).

**Secondary:** the same model and contrasts for the understanding score, hedonic quality and UEQ-S overall, with Holm correction within each outcome. Understanding items are also reported one by one (descriptive).

**Ranking and preference:** Friedman test on the ranks with pairwise Wilcoxon signed-rank tests (Holm); proportion ranking each format first, and proportion choosing each preferred format, with 95% confidence intervals and a chi-square goodness-of-fit test against equal proportions.

**Checks:**
- Carryover: add a format x period interaction to the primary model and test it with a likelihood ratio test.
- First-format analysis: pragmatic quality of the first format only (between participants), Kruskal-Wallis across the three formats.
- Non-parametric check: Friedman test on pragmatic quality across formats.
- Reliability: Cronbach's alpha for pragmatic quality, hedonic quality and understanding, per language and per format (the Japanese UEQ-S has no published validation).
- AR failure: primary analysis repeated without participants who tried AR and it did not work.

### Transformations
UEQ-S responses (1-7 in the form) are recoded to -3 to +3 by subtracting 4. Format is coded with the pamphlet as reference. Group and language are categorical.

### Inference criteria
Two-sided tests, alpha 0.05 after Holm correction within each outcome family. Effects are interpreted from estimates and confidence intervals, not p values alone.

### Data exclusion
- Pilot responses (numbers 901-905).
- Responses with consent not given (the form ends; no data).
- Duplicate participant numbers: the first submission is kept and the case is reported.
- If the formats ticked in the form do not match the order list, the order actually seen (from the form) is used, and the primary analysis is repeated without these participants.
- No exclusion on response patterns.

### Missing data
All questions except comments are required and nothing is saved before submission, so item-level missing data are not expected. Any incomplete case is kept in the mixed model with the data available.

### Exploratory analysis
- Format x group and format x language interactions.
- Clinicians and students (groups 4-7) vs others (groups 1-3) for the pamphlet vs 3D contrasts.
- Completion time by format order.
- Free-text comments: summarised descriptively.

## Other

- **Data handling:** anonymous data exported weekly to Excel and stored on Nagoya University secure storage managed by permanent academic staff; kept at least 10 years after publication, then destroyed. Responses are deleted from Microsoft Forms after the final export.
- **Reporting:** CROSS and CHERRIES checklists.
- **Open release (Zenodo, DOI):** anonymised data, analysis code, questionnaires, order list, and the 3D models (STL, GLB, USDZ). The Nagoya University logo is excluded.
- **Related files:** order list (`participant_order_list.xlsx` and `.csv`, `make_order_list.py`), form text (`quick-import_EN/JA.docx`, `form-text_EN/JA.docx`), [frozen materials link], [analysis script].
