# NOVELTY AUDIT — Biological channel constraints and writing-system inventories

Date: 2026-10-03. Status: Phase-1 deliverable (will be revisited after full analysis).

## 1. Neighboring literatures and what they already establish

| Literature / representative work | What is already known | What remains unresolved | Relation to this project |
|---|---|---|---|
| Phoneme-inventory ↔ word-length trade-offs (Nettle 1999; Fenk & Fenk-Oczlon; Wichmann et al. 2011; PLOS One 2023 Swadesh-list study; Frontiers 2021 61-language parallel-corpus study) | Larger segment inventories correlate with shorter words/syllables; robust across big samples | Applies to spoken sequences, not writing | Establishes the *spoken-side* inventory–combinatoriality trade-off our H2 generalizes to the written channel |
| Phonotactic complexity in bits/phoneme (Easterday 2019; TACL 2020) | Information-theoretic phonotactic measures are computable cross-linguistically | Not linked to script inventories | Supplies metrics for spoken-side combinatorial burden |
| Writing-system typology / grapholinguistics (Meletis 2020; Neef; Rogers 2005; Daniels) | Qualitative classes (alphabet/abjad/abugida/syllabary/logography) and their inadequacy as discrete categories | Lack of comparative quantitative corpus of inventories tied to phonology | Motivates continuous "encoding granularity" instead of trichotomy |
| Feature economy / combinatoriality of phonemes vs letter shapes (Kim, Allassonnière-Tang, Miton & Morin 2025, J. Memory & Language — 43 scripts vs P-base) | Letter shapes use more, less-informative features than phonemes; scripts vs phoneme inventories compared on feature economy | Compares shape primitives, not inventory-size coupling to P | Directly adjacent: it treats the *graphic* primitive level; we treat the *functional-unit* level (G vs P by encoded unit) |
| Graphic complexity of scripts (Changizi & Shimojo 2005, 115 scripts; Miton & Morin 2021, Cognition — 133 scripts, 47k characters) | Per-character complexity depends mainly on encoded unit type; script inventory sizes recorded per script (e.g., Latin 52 with case) | Inventory size recorded but not modeled against phonological inventory | Supplies an independent surface-grapheme count source for validation/sensitivity |
| Orthographic depth / transparency metrics (Borgwaldt et al. entropy; Seymour et al.; arXiv 2505.13657 compressibility measure, 22 languages) | Spelling–sound regularity quantifiable per language | Language-level, not inventory-size level | Orthographic depth enters as covariate; arXiv measure covers 22 languages only |
| Logography measurement (Sproat & Gutkin 2020; Penn & Choma 2006 burstiness) | Continuous degree-of-logography metrics exist from corpora | Requires corpora per language; distinct homophones operationalization | "Phonographicity" can borrow the continuous-trait logic |
| Decipherment / unknown scripts (Corazza et al. Cypro-Minoan; automatic decipherment reviews; script clustering 2023) | Sign-list size heuristics used informally to guess script type | No validated statistical model of inventory→architecture inference | Our inverse problem (H4) is the least-covered component: grouped-CV classification of ws_class from symbol statistics |
| Channel capacity / evolution of combinatorial coding (Nowak et al. 1999; Kirby; Little et al.; Zuidema & de Boer) | Finite discriminable signal space → combinatorial coding pressure (theory + experiments) | Not applied to writing-system inventory distributions | Supplies the theoretical frame, not empirical data on scripts |
| Exosemiotics / unknown-channel inference | Speculative, non-quantitative | — | Discussion-only generalization |

## 2. Direct predecessors to the specific analysis

No located work regresses **grapheme inventory size on phoneme inventory size across languages with dependence-aware modeling and encoded-unit granularity as moderator**. Closest partial overlaps:

- Miton & Morin (2021): inventory size is a *control variable* in character-complexity models, at the script level, unlinked to P.
- Kim et al. (2025): compares phoneme vs letter-shape inventories via feature economy — different estimand (feature structure, not size coupling).
- Word-length literature: trade-off established on the spoken side only.
- Decipherment folklore: sign-count → likely script type is asserted, never validated.

## 3. Novelty boundary

Genuinely open (defensible contribution if it survives analysis):

1. Quantitative model of **P–G coupling varying with encoded-unit granularity** across languages, with crossed dependence (language family × script).
2. **Inverse inference**: grouped-cross-validated classification of coding architecture from observable symbol statistics, benchmarked against trivial baselines — this is the least-covered piece.
3. Joint framework linking channel constraint → granularity → combinatorial escape across the spoken/written boundary.

Incremental, not novel (must not be oversold):

- "Alphabets have smaller inventories than morphosyllabaries" — trivially known; only acceptable as a calibrated quantification, never as the headline.
- Sign-count heuristics for undeciphered scripts — usage exists; contribution is validation, not the heuristic.
- Continuous phonographicity — Sproat & Gutkin already argue for continuous measures.

## 4. Gate-1 verdict

**Defensible gap exists, conditional on analyses 1–2 surviving dependence correction.** Proceed to POC. Risk: if the P–G interaction is driven entirely by script genealogy (scripts cluster within families), contribution collapses to redundancy with Miton & Morin — monitored via leave-one-script-family-out checks.
