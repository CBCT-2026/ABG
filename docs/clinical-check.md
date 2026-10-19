# ABG 3-stage models: clinical fidelity check

Checked 19 Oct 2026 against the sources at the end (found via PubMed). Unilateral complete cleft lip and palate (UCLP) assumed, as in the pre-op model.

## Verdict

The three-stage sequence is faithful to real care. Five wording or design points need a change before the text and models are frozen.

| # | What the plan says | What is accurate | Change |
|---|---|---|---|
| 1 | ABG repairs the hard tissue defect "in the roof of the mouth" | The palate (including the hard palate) is closed in infancy. ABG fills the **gap in the gum bone at the front of the upper jaw (the alveolar cleft)**, and often closes a small hole left between mouth and nose (fistula) [1,2] | Say "gap in the gum bone" (alveolus), not "roof of the mouth". The bony gap on the model should sit in the tooth-bearing ridge, from the front of the gum back to just behind the incisors |
| 2 | "Lateral canine" does not develop | The tooth often missing is the **lateral incisor** next to the cleft | Use "lateral incisor" everywhere |
| 3 | Canine erupts into the space "with help of orthodontics" | Most cleft-side canines come through the graft **on their own**: about 81% in a meta-analysis [3], 70 to 84% in a 2025 cohort [4], 26 of 28 at the Royal Children's Hospital Melbourne [5]. Some need a small operation to uncover the tooth plus braces to pull it in [6] | "The canine usually comes through the new bone by itself. Sometimes it needs help from an operation and braces." Braces afterwards: correct, most patients have fixed braces once the adult teeth are in [7,8] |
| 4 | Pre-op overlay = "palate soft tissue repaired in infancy" | Correct. Lip at 3 to 6 months, palate at 6 to 12 months [1,9]. The overlay should cover the gum and palate, with the scar line of the repair, and leave the bony gap underneath | Keep. Make the overlay show the gum over the gap, so removing it reveals the bone gap |
| 5 | Long-term: crown on the canine to look like a lateral incisor | Realistic. Usual first step is reshaping the canine (grinding the tip) plus tooth-coloured filling (composite) build-up; a veneer or crown is used when more change is needed [7,10]. The first premolar then sits in the canine spot. Alternative: keep the space and replace the lateral incisor with an implant or a bonded bridge, usually only once growth has finished [7] | Keep the removable crown/build-up piece. Consider a second removable piece showing a replacement lateral incisor (implant or bridge) so both options can be shown |

## How often the lateral incisor is missing

- Cleft-side lateral incisor absent from birth (agenesis) in about **half** of children with unilateral cleft: 50 to 54% [11]; 46% of all cleft patients in a 2024 cohort, the most often missing tooth [12].
- By the end of treatment it is gone in most cases (93% at SickKids, Toronto: agenesis or taken out because it was small or badly placed) [13].
- Missing permanent teeth overall: pooled 32% in people with cleft lip and palate (meta-analysis, 7 studies) [14]; odds about 19 times higher than without a cleft (meta-analysis, 37 studies) [15].
- When present, it is often small or peg-shaped [11].

Suggested patient text: "In about half of children with a cleft, the side tooth next to the gap (the lateral incisor) never forms."

## Ages in Australia

There is no national Australian protocol. The best Australian data are a 36-year audit of 746 children at the Women's and Children's Hospital, Adelaide [1] and the Royal Children's Hospital Melbourne outcome study [5].

| Step | Usual age | Australian data | Model |
|---|---|---|---|
| Lip repair | 3 to 6 months | Adelaide mean 4.8 months [1] | – |
| Palate repair | 6 to 12 months (TOPS trial: 6 vs 12 months) [9] | Adelaide mean 18.4 months, later than the 9 to 12 month standard [1] | – |
| Braces to widen the upper jaw before the graft (some patients) | about 8 to 9 years [8] | not reported | – |
| **Alveolar bone graft** | 9 to 12 years, when the canine root is half to two-thirds formed, before it comes through [1,2,16] | Adelaide mean 10.8 years (SD 1.8) [1] | **Pre-op: age 8 to 10** |
| Graft check (X-ray) | about 6 months after [16] | – | **Short-term: age 9 to 11, 3 to 6 months after surgery** |
| Canine comes through the graft | a few years after the graft (inferred; no cited interval) | Melbourne: 26/28 [5] | – |
| Full fixed braces | once adult teeth are in, about 12 to 16 years [8] | not reported | – |
| Shaping the canine, crown, implant or bridge | after braces; implants once growth stops (late teens or later) [7] | not reported | **Long-term: age 15 to 18, braces off** |
| Jaw surgery (some patients) | 16 years or older | Adelaide mean 16.3 years [1] | – |

## Teeth each model should show (unilateral cleft)

- **Pre-op (8 to 10 years), mixed dentition:** adult first molars and central incisors in; non-cleft lateral incisor in; baby canines and baby molars still in; adult canines and premolars forming in the bone. Cleft-side canine high in the bone next to the gap, root about half formed. Cleft-side lateral incisor missing (or small, if shown). Central incisor next to the cleft often slightly rotated or tipped [13].
- **Short-term (9 to 11 years):** same teeth; baby canine on the cleft side usually removed before or at the graft; graft fills the gap in a slightly different bone shade; canine still unerupted, now closer to the graft.
- **Long-term (15 to 18 years), permanent dentition:** all adult teeth except wisdom teeth, including second molars; canine moved forward into the lateral incisor space; premolar in the canine spot; graft blended into normal bone; braces removed (retainer wire behind the front teeth is typical and could be shown). Removable piece: canine crown or build-up shaped like a lateral incisor.

## Removable parts (friction fit or dovetail)

Default clearances for a fit that holds but can be taken off by hand:

| Joint | Resin (SLA/DLP) | FDM (PLA/PETG) |
|---|---|---|
| Friction peg in hole (round or D-shaped, stops rotation) | 0.10 to 0.15 mm per side | 0.20 to 0.25 mm per side |
| Dovetail slide (10 to 15° flank angle, slide direction along the arch) | 0.10 mm per side | 0.20 mm per side |
| Minimum wall around a socket | 1.2 mm | 1.6 mm |

- Soft tissue overlay (pre-op): print in flexible resin or TPU at 1.5 to 2 mm thick; locate with 2 or 3 pegs into the palate, not glue.
- Graft piece (short-term): dovetail sliding up into the cleft from below, in a lighter or different bone colour.
- Canine crown (long-term): friction cap over a reduced canine stump with a D-shaped key so it only fits one way.
- Print one test coupon per material first; clearances vary between printers.

These print values are engineering defaults, not from the clinical literature.

## Sources

1. Jensen ED, Soares G, Cook S, et al. The burden of cleft surgery: a 36-year reflection of surgical management of children with orofacial clefts in South Australia. Cleft Palate Craniofac J. 2025;63(8):2610-2617. https://doi.org/10.1177/10556656251387961
2. Elhaddaoui R, Bahije L, Zaoui F, Rerhrhaye W. Timing of alveolar bone graft and sequences of canine eruption in cases of cleft lip and palate: a systematic review. Orthod Fr. 2017;88(2):193-198. https://doi.org/10.1051/orthodfr/2017011
3. Jahanbin A, Kamyabnezhad E, Raisolsadat MA, et al. Long-term stability of alveolar bone graft in cleft lip and palate patients: systematic review and meta-analysis. J Craniofac Surg. 2022;33(2):e194-e200. https://doi.org/10.1097/SCS.0000000000008254
4. Doucet JC, Patel MH, Russell KA, et al. Evaluation of cleft adjacent canine eruption in patients with alveolar cleft treated with early secondary alveolar bone grafting. Cleft Palate Craniofac J. 2025;63(7):1929-1934. https://doi.org/10.1177/10556656251356211
5. Kumar R, Heggie A, Shand J, et al. Secondary bone grafting of alveolar clefts: a review of outcome at two centres in Australia and the UK. Br J Oral Maxillofac Surg. 2017;55(5):496-499. https://doi.org/10.1016/j.bjoms.2017.02.002
6. Alhasyimi AA, Ramadhan IPA, Farmasyanti CA, et al. Clinical orthodontic outcomes following secondary alveolar bone grafting in patients with cleft lip and palate: a systematic review. Cleft Palate Craniofac J. 2026. https://doi.org/10.1177/10556656261454065
7. Clerc MM, Detzen L, Vi-Fane B, et al. Replacement of missing lateral incisors for patients with cleft lip and palate: a decision-making tree based on a systematic review of the literature. J Prosthet Dent. 2025;134(1):50-60. https://doi.org/10.1016/j.prosdent.2023.07.023
8. Freitas JA, Garib DG, Oliveira M, et al. Rehabilitative treatment of cleft lip and palate: experience of the HRAC-USP, part 2: pediatric dentistry and orthodontics. J Appl Oral Sci. 2012;20(2):268-281. https://doi.org/10.1590/s1678-77572012000200024
9. Gamble C, Persson C, Willadsen E, et al. Timing of primary surgery for cleft palate. N Engl J Med. 2023;389(9):795-807. https://doi.org/10.1056/NEJMoa2215162
10. Manfio ASC, Garib D, Flores-Mir C, et al. Closure of maxillary lateral incisor agenesis space in unilateral cleft lip and palate: a digital model assessment. Dental Press J Orthod. 2023;28(1):e2321331. https://doi.org/10.1590/2177-6709.28.1.e2321331.oar
11. Gibson TL, Grayson BH, Cutting CB, Shetye PR. Prevalence of dental anomalies in patients with unilateral cleft lip and alveolus treated with gingivoperiosteoplasty. Cleft Palate Craniofac J. 2022;59(8):1017-1023. https://doi.org/10.1177/10556656211031124
12. Aung WP, Pungchanchaikul P, Pisek A, et al. Prevalence of tooth agenesis and supernumerary teeth related to different Thai cleft lip and cleft palate populations. BMC Oral Health. 2024;24(1):960. https://doi.org/10.1186/s12903-024-04719-3
13. Cassolato SF, Ross B, Daskalogiannakis J, et al. Treatment of dental anomalies in children with complete unilateral cleft lip and palate at SickKids hospital, Toronto. Cleft Palate Craniofac J. 2009;46(2):166-172. https://doi.org/10.1597/07-239.1
14. Srivastav S, Hermann NV, Tewari N, et al. Prevalence of dental anomalies in primary vs. permanent dentition in individuals with non-syndromic cleft lip and palate: a systematic review and meta-analysis. Cleft Palate Craniofac J. 2025;63(9):3069-3081. https://doi.org/10.1177/10556656251398076
15. Fonseca-Souza G, de Oliveira LB, Wambier LM, et al. Tooth abnormalities associated with non-syndromic cleft lip and palate: systematic review and meta-analysis. Clin Oral Investig. 2022;26(8):5089-5103. https://doi.org/10.1007/s00784-022-04540-8
16. Bartzela T, Hoffmann I, Kluge J, et al. Timing matters: dental development and outcomes on secondary alveolar bone grafting in cleft lip and palate patients. Clin Oral Investig. 2025;29(11):545. https://doi.org/10.1007/s00784-025-06594-w
