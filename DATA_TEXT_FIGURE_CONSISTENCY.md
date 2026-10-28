# DATA / TEXT / FIGURE CONSISTENCY — JQL submission package

## Number-to-source mapping

Every generated number in the prose routes through `results/canonical_results.json` (built by `code/canonical_results.py` from the frozen `tables/*.csv` and `logs/*.txt`).

| text location | rendered value | canonical key | source file / script |
|---|---|---|---|
| Abstract, Methods, Discussion | 544 pairs | N_TOTAL | data_processed/poc_dataset.csv via full_analysis |
| Abstract | P median 43–49 | P_MED_RANGE | tables/table_primary_class_medians.csv |
| Abstract | G medians 27→63→213→2210 | G_MED_SEQ | same |
| Abstract | classes 6 | N_CLASSES | code/script_type_codebook.csv |
| Abstract | rho alphabet −0.09 | RHO_ALPH | tables/table_primary_within_class_rho.csv |
| Abstract | rho abugida 0.47 | RHO_ABU | same |
| Abstract | naive rho 0.09 | NAIVE_RHO | logs/full_analysis.txt |
| Abstract | F1 granularity 0.76 | F1_GRAN_FAM | tables/table_inverse_granularity.csv |
| Abstract/§4.1 | rho(P,orth len) −0.40 | RHO_P_WLEN_W | logs/escape.txt |
| §3 | H1 coupling rhos −0.09/0.31/0.47/−0.01 | RHO_* | tables/table_primary_within_class_rho.csv |
| §3 | CIs [−0.31,0.49], [−0.73,0.59], [0.10,0.61] | CI_* | same |
| §3 | logP β=0.02, CI [−0.05,0.09] | BETA_LOGP, CI_LOGP | tables/table_primary_model.csv |
| §4.2 | Kruskal H=190 vs null95 6.8, p=0.005 | KRUSKAL_H, NULL95_H, P_LEVELSHIFT | logs/falsification_f2.txt |
| §4.2 | cross-class max|rho| obs 0.47 vs null95 0.56, p=0.154 | OBS_MAX_RHO, NULL95_RHO, P_CROSSCLASS | tables/table_falsif_shuffle.csv |
| §4.3 | stored ~49 / compositional ~50 (alphabet); obs 63 vs comp ~23, stored ~517 (abugida) | SIM_* | tables/table_simulation_bounds.csv |
| §4.3 | ±50% within-level P variation | (descriptive exception) | prose statement; see hardcode audit exceptions |
| §4.4 | ASJP rho(P,spoken len) 0.01, n=526 | RHO_P_WLEN_S, N_ASJP | logs/escape.txt |
| §4.4 | wordfreq n=287, rho(P,orth) −0.40, CI [−0.94,−0.11], rho(G,orth) +0.13 | N_WORDFREQ, RHO_P_WLEN_W, CI_P_WLEN_W, RHO_G_WLEN_W | logs/escape.txt |
| §4.5 | granularity F1 0.76/0.64 vs majority 0.23 | F1_GRAN_FAM/SCR/MAJ | tables/table_inverse_granularity.csv |
| §4.5 | ws_class 0.71 (symbol), 0.71 (stump), 0.70 (full) | F1_WS_SYM, F1_STUMP, F1_WS_FULL | tables/table_inverse_*.csv |
| §2 | 114 scripts, 7 curated pairs | N_CODEBOOK, N_CURATED | code/script_type_codebook.csv, code/curated_pairs.csv |
| Cover letter | 544, P 43–49, G 27,63,213,2210, rho −0.09, F1 0.76 | N_TOTAL, P_MED_RANGE, G_MED_LIST, RHO_ALPH, F1_GRAN_FAM | same registry |

## Figures

- **Figure 1** `fig_scatter_and_medians.png` — G vs P scatter + class medians; data = poc_dataset.csv + table_primary_class_medians.csv. Present, cited in §3, regenerated bit-consistent.
- **Figure 2** `fig_simulation.png` — observed G vs stored/compositional bounds; data = table_simulation_bounds.csv. Present, cited in §4.3.
- **Figure 3** `fig_escape.png` — escape-analysis panels; data = escape tables. Present, cited in §4.4.
- No supplements are referenced anywhere in the text (checked: no "Supplementary/SI/Figure S" strings).

## Tables (all cited in order in text; cells regenerated from frozen CSVs at build)

| # | title/source csv | cited | cells match |
|---|---|---|---|
| 1 | class medians — table_primary_class_medians.csv | §2/§3 | yes |
| 2 | within-class rhos — table_primary_within_class_rho.csv | §3 | yes |
| 3 | crossed mixed model — table_primary_model.csv | §3 | yes |
| 4 | simulation bounds — table_simulation_bounds.csv | §4.3 | yes |
| 5 | counterfactual re-encode — table_simulation_counterfactual.csv | §4.3 | yes |
| 6 | escape Spearman — table_escape_spearman.csv | §4.4 | yes |
| 7 | inverse macro-F1 — table_inverse_combined.csv | §4.5 | yes |

Table cell comparison: builder reads each CSV verbatim at docx build time — docx table cells were extracted and diffed against the CSVs; match at printed precision. First-citation order T1→T7, F1→F3 is monotonic; no duplicate numbers, no orphans, no nonexistent supplements.

## Claim consistency across sections

- Abstract = §4 Results = §5 Discussion = cover letter: P flat (43–49), G spans 27→2210 by granularity, within-class coupling weak/non-monotonic, abugida 0.47 exploratory (does not clear the permutation null), H2 null on the spoken side (0.01) with written-surface residue (−0.40), granularity recoverable (0.76 vs 0.23), architecture/P not recoverable beyond raw inventory magnitude, simulation bounds presented as interpretation, not estimates. Consistent throughout.

DATA-TEXT-FIGURE CONSISTENCY VERDICT: **PASS**
