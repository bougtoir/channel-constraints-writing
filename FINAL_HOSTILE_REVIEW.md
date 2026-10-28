# FINAL HOSTILE REVIEW — JQL submission "Encoded-unit granularity, not phonological channel size, sets the scale of writing-system symbol inventories"

Adversarial review of the final submission package. Each attack lists severity, the evidence checked, the remediation applied (if any), and a per-attack verdict.

## Attack 1 — Granularity coding is tautological: G counts signs, granularity is coded by what the signs encode
**Severity:** CRITICAL (if true, the paper measures itself).
**Evidence checked:** `code/script_type_codebook.csv` codes granularity by *encoded unit size* (phoneme/feature=1, CV-akshara=2, syllable/mora=3, morpheme-syllable=4), not by inventory size G. G is counted independently from CLDR exemplarCharacters. The claimed relationship — larger encoded unit ⇒ larger sign inventory — is an empirical regularity, not a definitional identity: a syllabary *could* have 50 signs and an alphabet *could* have 2000; the coding scheme does not force the outcome. Counterexamples inside the data: Korean is coded gran 1 (featural Hangul) on the coded units (jamo), which is the conservative choice and yields the largest intra-class G-P gap; Han-derived scripts are gran 4 but differ among themselves.
**Residual risk:** granularity class membership is a judgment coding; mitigated by the published codebook (114 scripts) enabling replication/disagreement, and by the within-class analyses that do not rely on the ordinal ordering.
**Verdict:** PASS. Not tautological; the coding is falsifiable and released.

## Attack 2 — CLDR exemplarCharacters is not a grapheme inventory
**Severity:** MAJOR.
**Evidence checked:** CLDR exemplar core sets are intended as "typographically distinctive letters of the alphabet," not full orthographic inventories; they can undercount digraphs and non-core marks. The manuscript states this limitation explicitly (§2, Data) and defines G as "the count of core exemplarCharacters" — an operationalized, reproducible proxy, not a claim of exhaustive grapheme coverage. G_aux is retained for sensitivity. Headline results (medians 27/63/213/2210) are consistent in direction with known inventory scales; the granular ordering is far larger than plausible exemplar-coding error.
**Verdict:** PASS. Proxy limitation disclosed; effect size dwarfs plausible proxy noise.

## Attack 3 — The result is driven by Han and Latin
**Severity:** MAJOR.
**Evidence checked:** `logs/full_analysis.txt` F3 robustness blocks: excluding Latn-script rows, excluding Han-derived rows, and excluding single-language-class rows leaves the level shift significant (Kruskal H=190 vs null-95 6.8, p=0.005). Within-class rhos recomputed for each exclusion; abugida rho stays ≈0.47 without Han (which is morphosyllabic and not in that class anyway).
**Verdict:** PASS. The core separation survives all three exclusions.

## Attack 4 — Unbalanced cells make the medians meaningless (gran-3 n=7 scripts? reported n)
**Severity:** MINOR.
**Evidence checked:** cell sizes are reported in Table 1 and the text; gran-3 (syllabic) has the smallest cells. The median-based statistic is robust to cell imbalance; within-class tests are per-class and never pool small cells into a single estimate. The permutation control (200 label shuffles) accounts for cell structure explicitly.
**Verdict:** PASS. Sparse cells are reported, not hidden; the analysis design does not hinge on them.

## Attack 5 — One observation per script inflates pseudoreplication
**Severity:** MAJOR.
**Evidence checked:** unit of analysis is language×script (544 pairs); family-cluster bootstrap and grouped CV correct for dependence; the F3 control "no_singleton_scripts" (drop scripts seen once) reproduces the pattern. Glottolog family/macroarea grouping is used throughout (family-cluster CIs, script-grouped F1).
**Verdict:** PASS. Dependence is the explicit topic of the design (Jaeger et al. method; SAP prespecifies grouped resampling).

## Attack 6 — H1/H3 are oversold: headline rho is a big 0.47 but the honest answer is null
**Severity:** CRITICAL if the text claims the coupling is real.
**Evidence checked:** the manuscript's own framing: the abugida coefficient 0.47 (CI [0.10, 0.61]) is reported *and then discounted* — under 200 label shuffles the null 95th percentile max|rho| is 0.56, cross-class permutation p=0.154, so H1/H3 are stated as "unsupported in their confirmatory form — reported as exploratory." §4.2 says this verbatim. The abstract reports both the 0.47 and the null.
**Verdict:** PASS. Not oversold; the paper explicitly withdraws confirmatory status.

## Attack 7 — H2 (combinatorial escape) null result is rescued by the written-wordlen finding
**Severity:** MAJOR.
**Evidence checked:** escape analysis is reported as largely null: ASJP-side rho=0.01 (n=526), wordfreq-side rho for spoken-length vs P is −0.05 (spoken) — only the *written* word length correlation (rho(P,orth len)=−0.40, CI [−0.94,−0.11], n=287) is positive, and the text characterizes it as "written-surface residue routed through phonology," not as confirmation of H2. No rescue language ("trend", "marginally") is used elsewhere.
**Verdict:** PASS. Null result retained and framed as such.

## Attack 8 — Inverse inference leaks granularity features into the granularity task
**Severity:** CRITICAL if P or G/P are in the granularity feature set.
**Evidence checked:** `code/inverse_inference.py`: Task 1 (granularity) uses ONLY symbol-side statistics (G and G_aux-derived features) — no P, no G/P, no consonant/vowel counts. Task 2 (ws_class) is the one that adds G/P and phoneme counts — and is labeled secondary/presupposing P. CV is family- and script-grouped; macro-F1 reported (0.76 family / 0.64 script vs majority 0.23). Label-shuffled controls collapse to baseline.
**Verdict:** PASS. No leakage; tasks are correctly separated.

## Attack 9 — Causal language exceeds the design
**Severity:** MAJOR.
**Evidence checked:** scan for cause/drive/determine/produce/govern/explain: every occurrence is (a) inside hypothesis statements, (b) describing the *naive* expectation that is then rejected, or (c) the title/abstract thesis "sets the scale," which is the measured descriptive fact (granularity orders the inventory scale 27→2210 while P is flat 43–49). No causal-verb is attached to an estimated coefficient.
**Verdict:** PASS. Language is descriptive/constrained; the one strong verb is the paper's own empirical claim and is supported by the medians.

## Attack 10 — Simulation bounds are arithmetic, not evidence
**Severity:** MINOR.
**Evidence checked:** the K^L simulation is presented as a *mechanism illustration* (§4.3), explicitly bracketing observed G between stored-unit demand U and compositional bound ⌈U^(1/L)⌉. It is not entered into any hypothesis test; reported numbers (stored ~49, ~517; compositional ~50? — registry SIM_STORED_1=49, SIM_COMP_1=50, SIM_STORED_2=517, SIM_COMP_2=23) come from the same frozen run (seed fixed).
**Verdict:** PASS. Simulation is descriptive scaffolding; correct in-text hedging.

## Attack 11 — Selective reporting: table/figure set could hide contradicting analyses
**Severity:** MINOR.
**Evidence checked:** falsification tables table_falsif_* (shuffle, exclusion controls) are all present and referenced; negative/weak results (abjad imprecise, morphosyllabic null, naive rho trivial, stump ≥ logreg) are all in-text and in tables. No table/figure exists in outputs that is not cited, and none cited is absent.
**Verdict:** PASS.

## Attack 12 — Precision claims exceed data (P medians to 0.1, F1 to 2 decimals)
**Severity:** MINOR.
**Evidence checked:** medians reported as integers/ranges (43–49; 27→2210), rhos to 2dp, F1 to 2dp. Granularity-3 median P=43 with small n is still a median — acceptable as descriptive.
**Verdict:** PASS.

## Attack 13 — The "0.70 vs 0.71" ws_class F1 discrepancy
**Severity:** MINOR (caught during hardcode audit).
**Evidence checked:** frozen text said "0.70" for the symbol-statistics feature set; the frozen table (table_inverse_symbol_only.csv, logreg_family) is 0.7084 → 0.71. The token refactor now renders {F1_WS_SYM}=0.71, matching the table exactly; the fuller-set number 0.7042 → "0.70" is retained via {F1_WS_FULL}.
**Verdict:** PASS after remediation (rounding corrected to match the frozen table).

## Attack 14 — Codebook/class counts in Methods are stale
**Severity:** MINOR (caught during audit).
**Evidence checked:** text said "95 scripts" and "7 writing-system classes"; the frozen codebook has 114 scripts and 6 classes. Corrected via canonical tokens {N_CODEBOOK}=114, {N_CLASSES}=6.
**Verdict:** PASS after remediation.

---
HOSTILE REVIEW VERDICT: **PASS** — two MINOR stale-number findings were remediated by routing the values through the canonical registry; no CRITICAL attack succeeded; all null results and limitations remain in the text.
