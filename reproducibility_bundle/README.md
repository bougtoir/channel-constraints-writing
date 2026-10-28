# Biological Channel Constraints on Writing-System Inventories

Research project: does the size/organization of a writing system's symbol
inventory reflect (a) constraints of the biological signal channel it encodes,
(b) the granularity of the encoded unit, and (c) combinatorial depth — and can
observable symbol statistics support inverse inference about the coding
architecture?

## Layout

- `code/` — all pipeline scripts (run in order below)
- `data_raw/` — downloaded originals + `ACQUISITION_LEDGER.csv` (sha256, UTC)
- `data_processed/` — linked datasets
- `figures/`, `tables/`, `logs/` — generated outputs
- `docs/` — NOVELTY_AUDIT lives at project root per protocol

## Reproduce

```
pip install -r requirements.txt
python3 code/download_data.py
python3 code/build_poc_dataset.py
python3 code/poc_analysis.py
```

## Key variables

- `P` phoneme inventory size: PHOIBLE, largest inventory per ISO6393
- `G` grapheme inventory size: CLDR exemplarCharacters core set
- `ws_class`, `granularity` (1 phoneme-level … 4 morpheme-level): `code/script_type_codebook.csv`
- `family`, `macroarea`: Glottolog 5.0

## Status

POC complete → **WEAK GO** (see `POC_DECISION.md`).
