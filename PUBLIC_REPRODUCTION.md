# PUBLIC REPRODUCTION — JQL submission package

## Public repository

- **URL:** https://github.com/bougtoir/channel-constraints-writing
- **Recorded commit SHA:** `98165758939d6538640ca5d74aae997f8db24a0f` (branch `master`)
- **Contents:** complete `channel_constraints_writing/` project subtree — pipeline code, `data_raw/` originals + `ACQUISITION_LEDGER.csv` (URL, UTC access time, sha256, license per dataset), `data_processed/`, `tables/`, `figures/`, `logs/`, `manuscript/` sources, `results/canonical_results.json`, `tests/`, `requirements.txt`.
- Repo name contains no journal name (per standing rule).

## Procedure performed (this audit, on a clean VM-side clone)

```
git clone https://github.com/bougtoir/channel-constraints-writing.git
cd channel-constraints-writing        # @9816575
pip install -r requirements.txt
python3 code/build_poc_dataset.py
python3 code/full_analysis.py
python3 code/simulation.py
python3 code/inverse_inference.py
python3 code/falsification_f2.py
python3 code/combinatorial_escape.py
python3 code/canonical_results.py
```

Raw external inputs (PHOIBLE, Glottolog, CLDR 46.1, ASJP, wordfreq counts, Miton–Morin OSF) are committed in `data_raw/` with sha256 in `data_raw/ACQUISITION_LEDGER.csv`, so `download_data.py` is only needed for freshness checks, not reproduction.

## Results

- **`results/canonical_results.json` regenerated: byte-identical to the committed file** (all 55 headline keys, including N_TOTAL=544, P medians 45/48/43/49, G medians 27/63/213/2210, rho alphabet −0.09 / abjad 0.31 / abugida 0.47 / morphosyllabic −0.01, logP β=0.02, Kruskal H=190 vs null95=6.8 p=0.005, cross-class p=0.154, naive rho=0.09, written-escape rho(P)=−0.40, F1 granularity 0.76/0.64 vs majority 0.23, ws_class 0.71/0.71/0.70).
- **Dataset row count:** poc_dataset.csv = 544 language×script pairs, identical.
- **Numeric tables:** identical at printed precision. Residual diffs are floating-point last-ulp jitter in unrounded CSV fields (`table_primary_model.csv`, `table_inverse_combined.csv` 15th-decimal differences) — values round to the same printed numbers used in the manuscript and registry.
- **Non-numeric diffs:** one CLDR likelySubtags-derived locale label flips in poc_dataset.csv (Friulian `ph`→`ea` closest-language column) — a non-analytic column not used by any reported statistic; fig_simulation.png differs by PNG encoding bytes only.
- Figures 1–3 and Tables 1–7 regenerated from canonical data match the committed artifacts at display precision.

## Conclusion

The public repository at the recorded SHA reproduces the manuscript's canonical result set exactly; pipeline is deterministic (seed 20261003, B=2000, 200 shuffles) modulo float-ulp noise.

PUBLIC REPRODUCTION VERDICT: **PASS**
