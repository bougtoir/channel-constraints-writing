# REFERENCE VERIFICATION — JQL submission package

15 references in `code/build_manuscript_docx.py` `REFS`. Verified against Crossref (`api.crossref.org`), publisher records, or official dataset documentation on 2026-10-28.

| # | key | verification | status |
|---|---|---|---|
| 1 | daniels | Daniels PT, *An Exploration of Writing*, Equinox 2018 — book, publisher record confirmed | OK |
| 2 | sproat | Sproat R, *A Computational Theory of Writing Systems*, CUP 2000 — book, correct | OK |
| 3 | changizi | Crossref: Proc R Soc B **272(1560):267–275**, 2005, DOI 10.1098/rspb.2004.2942 — exact match | OK |
| 4 | miton | Crossref: Cognition **214:104771**, 2021, authors Miton & Morin — exact match | OK |
| 5 | coupe | Crossref: Sci Adv **5(9):eaaw2594**, 2019, authors Coupé, Oh, Dediu, Pellegrino — exact match | OK |
| 6 | jaeger | Crossref: Linguistic Typology **15(2)**, 2011, DOI 10.1515/lity.2011.021 — pages 281–319 correct | OK |
| 7 | bickel | Crossref: Linguistic Typology **11(1)**, 2007, DOI 10.1515/lingty.2007.018 — pages 239–251 correct | OK |
| 8 | phoible | PHOIBLE 2.0, Moran & McCloy (eds), MPI-SHH Jena 2019 — official dataset record | OK |
| 9 | moran_phoneme | **FIXED.** Was cited as 2016;50(3):469-503. Crossref: *Investigating diachronic trends in phonological inventories using BDPROTO*, Lang Resour Eval **2021;55(1):79–103**, DOI 10.1007/s10579-019-09483-3, authors Moran, Grossman, Verkerk. Reference corrected in REFS. | FIXED |
| 10 | cldr | **FIXED.** Year was 2025; CLDR 46.1 released 2024-12-18 (release-46-1 tag, the version used in the pipeline). Year corrected to 2024. | FIXED |
| 11 | glottolog | Glottolog 5.0, MPI-EVA Leipzig 2024 — official record | OK |
| 12 | asjp | ASJP Database version 20, 2022, asjp.clld.org — official record | OK |
| 13 | wordfreq | Zenodo DOI 10.5281/zenodo.7199437 = rspeer/wordfreq v3.0 — verified | OK |
| 14 | maddieson | *Patterns of Sounds*, CUP 1984 — correct | OK |
| 15 | fenk | Crossref: "Complexity trade-offs between the subsystems of language", SLCS 94, Benjamins 2008, pp. 43–65, DOI 10.1075/slcs.94.05fen — exact match | OK |

## Claim-support audit (spot-checked)

- **Biophysical constraint / discriminability**: changizi (character complexity vs discriminability), miton (graphic complexity) — both cited where demanded/producibility limits are discussed. Support holds.
- **Channel efficiency / information rate**: coupe — cited for comparable information rates across languages. Support holds.
- **Comparative-typology dependence**: jaeger, bickel — cited where family/areal resampling is justified. Support holds.
- **PHOIBLE as phoneme-inventory source**: phoible (+ moran_phoneme for diachronic context). Support holds.
- **Complexity trade-offs (escape expectation)**: fenk — cited exactly where the P–G/trade-off expectation is invoked. Support holds.
- **Dataset citations**: phoible, cldr, glottolog, asjp, wordfreq — all cited in Data §2 at first use.

## Citation numbering (order of appearance, per JQL numbered-reference convention)

First-citation order in MANUSCRIPT.md = REFS order = [1]–[15] monotonic (scripted check: daniels, sproat, changizi, miton, coupe, jaeger, bickel, phoible, moran_phoneme, cldr, glottolog, asjp, wordfreq, maddieson, fenk). **All 15 cited; no orphans; no unused entries.**

REFERENCE VERIFICATION VERDICT: **PASS** (two bibliographic errors found and corrected: moran_phoneme volume/pages/year/DOI; CLDR citation year).
