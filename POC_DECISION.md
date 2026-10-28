# POC DECISION — Channel constraints on writing-system inventories

Date: 2026-10-03 · Branch state: devin/1791019923-channel-constraints

## Verdict: WEAK GO

Proceed with narrowed claims: the primary contribution becomes the
**granularity-graded P–G coupling model plus the inverse-inference framework**,
not a strong universal law.

## Evidence against the GO criteria

| Criterion | Status | Evidence |
|---|---|---|
| Variables reproducible | PASS | P = PHOIBLE max inventory per ISO6393; G = CLDR exemplar core set; script via CLDR likelySubtags; ws_class via codebook. Full pipeline `code/build_poc_dataset.py` |
| Coverage across architectures | PARTIAL | 719 classified pairs + 7 curated pairs; P-matched analysis set n=544: granularity 1: 470, 2: 47, 3: 7, 4: 20. High-granularity cells remain thin — main WEAK driver |
| Relationships survive dependence correction | PARTIAL-PASS | Crossed-RE model (script + language family): logP×granularity interaction β=0.19, 95% CI [-0.003, 0.384] — direction consistent, borderline; treat as exploratory |
| Driven by famous scripts | PASS | Leave-one-script-out OLS interaction range [0.62, 0.86], always positive |
| Defensible novelty | PASS (conditional) | NOVELTY_AUDIT.md: P–G coupling regression unlocated in prior work; inverse-inference validation is the least-covered component |

## Revised empirical picture (supersedes the naive H1 expectation)

1. **P is nearly constant across architecture classes** (median 43–49 across
   alphabet/abjad/abugida/syllabary/morphosyllabic) while median G scales
   26 → 38 → 64 → 269 → 2210. Encoded-unit granularity, not channel
   inventory, sets the order of magnitude of G.
2. **Within-class P–G coupling is weak and non-monotonic**: alphabet
   Spearman ρ = -0.09 (p = 0.06, n = 444) — alphabets do NOT add letters
   for bigger phoneme inventories; abjad ρ = 0.31 (p = 0.12, n = 26);
   abugida ρ = 0.47 (p = 0.0008, n = 47) — the strongest coupling sits at
   intermediate granularity, not at the phoneme level.
3. Within granularity-1 OLS: logG on logP slope ≈ 0.11, R² ≈ 0.02.
4. **Inverse-inference potential is real but asymmetric**: ws_class is
   strongly constrained by G (class G-ranges barely overlap), while P is
   poorly recoverable from G — exactly the asymmetry the framework predicts
   (symbol statistics constrain architecture, not physiology).

## POC-2 grapheme-count validation (stratified manual check)

CLDR exemplar core counts vs authoritative descriptions:

| System | CLDR G | Authoritative | Verdict |
|---|---|---|---|
| English/Latn | 26 | 26 | match |
| German/Latn | 27 (+ä ö ü in aux) | 26+4 | match after aux |
| Russian/Cyrl | 32 (ё in aux) | 33 | match after aux |
| Arabic/Arab | 38 | 28 letters + ~10 vowel/hamza signs | consistent |
| Hebrew/Hebr | 22 (+finals in aux) | 22+5 | match |
| Hindi/Deva | 67 | ~45 letters + signs | plausible |
| Amharic/Ethi | 282 | ~275–287 fidäl | match (surface composite glyphs) |
| Thai | 71 | 44 cons + ~21 vowel/tones | plausible |
| Khmer | 72 | ~74 | match |
| Georgian | 33 | 33 (Mkhedruli) | match |
| Cherokee | 85 | 85–86 | match |
| Vai | 269 | ~212–300 (sources differ) | flag: definition-sensitive |
| Japanese/Jpan | 2187 | ~2136 jōyō + 92 kana | plausible |
| Korean/Kore | 11172 | surface syllable blocks vs 24–40 jamo | **DEFINITIONAL FLAG**: G_surface ≠ G_functional for compositional scripts; needs jamo-level treatment |
| Tibetan | 101 | core ~80 + Sanskrit extensions | minor flag |

The definition problem is real but *manageable*: it does not stop the project,
it forces explicit G_surface / G_functional separation (prompt §1.4), with
Hangul-style compositional scripts handled at component (jamo) level in
sensitivity analysis.

## Gate decision

WEAK GO conditions adopted for Phase 3–4:

1. Claims narrowed to: (a) granularity-moderated P–G coupling; (b) validated
   inverse-inference baseline; (c) no universal channel-capacity claim.
2. Full analysis must enlarge the P-matched set at high granularity:
   add curated P for syllabic/morphosyllabic languages absent from CLDR-PHOIBLE
   join (documented hand-curated rows with sources) or WALS ordinal fallback.
3. Compositional scripts get dual G definitions (surface / functional components).
4. The logP×granularity interaction is re-estimated with grouped
   cross-validation and phylogenetic/family checks before any confirmatory claim.
5. If the interaction does not survive the enlarged data or if ws_class
   is unrecoverable from symbol statistics beyond trivial baselines → NO-GO
   for the manuscript, report null results instead.

## Files produced this phase

- `code/download_data.py` — acquisition + ledger (sha256)
- `code/script_type_codebook.csv` — script→class/granularity codebook
- `code/build_poc_dataset.py` — linked dataset builder
- `code/poc_analysis.py` — descriptive + crossed-RE model + falsification
- `data_processed/poc_dataset.csv` (725→380 analysis rows)
- `figures/poc_fig_P_vs_G.png`, `figures/poc_fig_GP_by_class.png`
- `tables/table_class_summary.csv`, `tables/table_loo_script.csv`
- `logs/poc_model.txt`
- `NOVELTY_AUDIT.md`, `DATA_SOURCE_LEDGER.csv`, `data_raw/ACQUISITION_LEDGER.csv`
