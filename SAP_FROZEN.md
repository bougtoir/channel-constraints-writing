# SAP_FROZEN — Statistical Analysis Plan (frozen)

Frozen: 2026-10-03 · Commit: 6ef2860a9a8da5654c939fba4760d0138511ba01 (dataset+code state at freeze)
Protocol amendment rule: any change after this freeze is recorded in
`docs/PROTOCOL_AMENDMENTS.md` with reason and date.

## Research questions (locked)

RQ1 (channel coupling): does the association between phoneme inventory size
(P) and grapheme inventory size (G) differ across encoded-unit granularity
classes, in direction consistent with progressive decoupling?

RQ2 (combinatorial escape): do language×script pairs with smaller effective
inventories rely on longer coded forms (written word length), and does the
spoken-side trade-off (phoneme count vs word length) extend to the written
channel?

RQ3 (inverse inference): how much information about coding architecture
(ws_class, granularity) and channel inventory (P) is recoverable from
observable symbol statistics, benchmarked against trivial baselines?

## Variables (locked)

| Variable | Definition | Source |
|---|---|---|
| G (G_surface) | count of CLDR core exemplarCharacters | CLDR 46.1 |
| G_aux | auxiliary exemplar count | CLDR 46.1 |
| G_functional | component-level count where compositional (e.g. Korean jamo ~24–40); sensitivity only | curated |
| P | largest PHOIBLE segment inventory per ISO6393 (consonants+vowels+tone) | PHOIBLE 2.0 |
| granularity | ordinal 1 phoneme/feature → 2 CV-akshara → 3 syllable/mora → 4 morpheme-syllable | `code/script_type_codebook.csv` |
| ws_class | alphabet/abjad/featural/abugida/syllabary/morphosyllabic/mixed | codebook |
| family, macroarea | Glottolog 5.0 | languoid.csv |
| script | ISO 15924 code from CLDR likelySubtags / explicit locale tag | CLDR |
| mean written word length | mean characters per Swadesh gloss (ASJP orthographic forms) | lexibank/asjp CLDF |
| mean spoken word length | mean segments per Swadesh gloss | ASJP (phonetic forms if available) |

Unit of analysis: language×script pair (one row per locale/script pairing).
Curated supplement rows documented in `code/curated_pairs.csv`.

## PRIMARY analysis (confirmatory)

P1. Class-median contrasts: median G and median GP ratio across granularity
classes, with bootstrap 95% CIs clustered on script (resample scripts, not
rows, B=2000).

P2. Within-class P–G coupling: per-class Spearman ρ(P, G) with
family-cluster bootstrap CI. The confirmatory statistic is the *set* of
per-class couplings, reported for all classes — no single "effect".

P3. Dependence-aware model: `logG ~ logP * C(granularity)` as crossed
mixed-effects (variance components for script and language family).
Report fixed-effect estimates + 95% CIs + marginal/conditional R².
If MixedLM fails to converge: OLS with family-cluster-robust SEs as the
pre-registered fallback.

## SECONDARY analysis

S1. Combinatorial escape (written): among granularity ≤ 2 pairs, regression
of mean written word length (ASJP) on G and P with family clustering.
Prediction: negative slope on G, controlling P.

S2. Simulation layer: toy channel model — K primitives, mean code length L,
perceptual-confusion noise; show optimal (K*, L*) balance vs noise level.
Presented as mechanism illustration only.

S3. Inverse inference: multinomial classifier of ws_class from
[G, G_aux, G/P, n_cons, n_vow] (and a reduced symbol-statistics-only variant
[G, G_aux, GP]), evaluated under leave-one-language-family-out and
leave-one-script-out grouped CV. Baselines: majority class, G-only decision
stump. Report macro-F1 with CI.

## EXPLORATORY (labeled exploratory in any manuscript)

E1. Sensitivity: alternative P (consonants-only, vowels-only, WALS ordinal),
alternative G (core+aux, G_functional for Korean), excluding constructed and
extinct languages, excluding single-language scripts, excluding Latin.
E2. Leave-one-script-family-out and leave-one-macroarea-out re-estimation.
E3. G_functional vs G_surface divergence (Hangul-type compositional scripts).
E4. Where data permit, phonographicity continuous metric (compressibility/
entropy) replacing ordinal granularity — only if computable for ≥30 pairs.

## Inference rules

- Effect sizes + 95% CIs reported for every primary/secondary statistic.
- P-values retained where tests are run; no p-only claims.
- Naive correlations may be shown only as descriptives, never as primary
  evidence.
- Null/negative results are reportable; the manuscript may not relabel
  exploratory findings as confirmatory.

## Falsification / negative controls (locked)

F1. Permute P within granularity strata (B=200): within-class coupling
distribution under exchangeability.
F2. Shuffle ws_class labels (B=200): classifier must collapse to baseline.
F3. Exclude Latn-script rows; exclude single-language scripts; exclude
Hani-derived rows — primary conclusions must survive.
F4. Alternative grapheme-count definitions (core vs core+aux; Miton & Morin
script-level counts where overlapping).
