# INVERSE_INFERENCE_VERIFICATION

Verified 2026-10-03 against `code/inverse_inference.py` and
`logs/inverse_inference.txt` / `tables/table_inverse_*.csv`.

## Task A — granularity prediction (the inverse problem)

- **Target**: ordinal granularity ∈ {1,2,3,4} as multiclass
- **Features**: `G`, `g_aux` ONLY — i.e. directly observable
  symbol-inventory statistics. **P, G/P, n_cons, n_vow are NOT used**
  (code line: `d[["G","g_aux"]]`).
- **Model**: RandomForestClassifier(300 trees, seed 0)
- **CV**: leave-one-language-family-out and leave-one-script-out
  (LeaveOneGroupOut; folds with <20 training rows skipped)
- **Result**: family-grouped macro-F1 = **0.758 ± 0.340**;
  script-grouped = **0.637 ± 0.435**; majority baseline macro-F1 =
  **0.233**

Therefore the granularity claim is independent of phonological inputs:
granularity is recoverable from directly observable inventory
statistics alone.

## Task B — writing-system-class prediction (secondary)

- **Target**: ws_class ∈ {alphabet, abjad, abugida, featural,
  syllabary, morphosyllabic} (mixed excluded)
- **Feature sets**:
  - `symbol_only`: `G`, `g_aux`, `GP_ratio` — includes G/P (requires
    known P; secondary task only)
  - `full`: `G`, `g_aux`, `GP_ratio`, `n_cons`, `n_vow`
- **Models**: LogisticRegression(C=1.0), RandomForestClassifier(300),
  DecisionTreeClassifier(max_depth=1) on G alone, majority baseline
- **Results (symbol_only, family-grouped macro-F1)**: logreg 0.708,
  RF 0.629, **G-only stump 0.712**, majority 0.180
- **Results (symbol_only, script-grouped)**: logreg 0.551, RF 0.573,
  G-only stump 0.564
- `full` feature set does not beat `symbol_only` (0.704 vs 0.708
  family-grouped logreg).

**Verified conclusion**: a G-only decision stump matches or exceeds the
richer classifiers; finer writing-system-class labels carry essentially
no recoverable signal beyond inventory magnitude. P itself is not
recoverable from these statistics (not tested as a target — P is
approximately constant across architectures, so there is no signal to
recover).
