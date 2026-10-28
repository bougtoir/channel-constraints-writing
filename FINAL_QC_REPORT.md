# FINAL_QC_REPORT — JQL final revision (2026-10-03)

## Scientific

- Inverse-inference wording now matches code: §4.5 split into Task 1
  (granularity; features G + G_aux ONLY — verified in
  INVERSE_INFERENCE_VERIFICATION.md) and Task 2 (ws_class; feature sets
  include G/P, which presupposes known P — flagged as secondary).
- Granularity classifier is verified independent of P and of G/P.
- G/P is confined to the secondary classifier and is never described as
  directly observable from an unfamiliar symbolic system.
- Biophysical-limit claims recalibrated: Discussion now states the
  analysis "does not estimate a universal upper bound"; biological
  constraints are presented as plausible interpretation backed by prior
  literature, distinct from the observed comparative result.
- All null results intact and prominent: H1/H3 unsupported confirmatorily,
  alphabet coupling absent, abugida result does not establish a
  cross-class ordering, H2 spoken side null, class prediction ≈ G-stump.
- Results-section phonological-constraint sentence uses "consistent with"
  phrasing with citation (Maddieson) — interpretation, not result.
- Causal language proportionate: title kept ("sets the scale" =
  architectural; see TITLE_DECISION.md); no causality claims beyond the
  comparative design.
- "Unknown channel" phrasing replaced by "unfamiliar symbolic system"
  wherever the empirical classifier is meant; "channel" retained only for
  the theoretical construct.
- Abstract, Results, Discussion, Conclusion, and cover letter tell the
  same story (decoupling → architecture → inverse boundary).

## Numerical

- Every headline number traced to code output — see
  NUMERICAL_CONSISTENCY_AUDIT.md. Two discrepancies found and fixed
  (granularity baseline 0.27→0.23; Miton & Morin reference title/DOI).
- No new analyses added; no numbers altered except the baseline typo.

## Writing

- §4.5 rewritten to separate the two prediction tasks exactly.
- Discussion reordered: empirical decoupling → failed naive hypothesis →
  architectural interpretation → stored vs composed → escape limits →
  inverse boundary → calibrated biophysical interpretation → limitations.
- Conclusion revised per §21 structure.
- Cover letter rewritten (5-paragraph structure, first-person "I",
  energetic but non-promotional; no "proves/first/universal" claims).

## Submission

- Formatting: TNR 12pt body, 10pt captions/table text, black text,
  OMML math for the one formula (⌈U^{1/L}⌉), zero markdown artifacts /
  backticks / braces verified by programmatic scan of the docx.
- Tables 1–7 reformatted: human-readable headers, 2-decimal effects,
  3-decimal p-values (<0.001 floor), compact CIs, integer counts as
  integers — no machine-precision decimals.
- Figure/table citation order verified programmatically by the build
  script (assertion fails on any out-of-order or orphaned object):
  Figures 1→3 and Tables 1→7 cited strictly in numerical order; every
  object cited before insertion; no supplementary references.
- References verified against authoritative sources (Cognition,
  Proc R Soc B, Linguistic Typology, Sci Adv DOIs); one JQL-adjacent
  citation added (Coupé et al. 2019) because it substantively supports
  the channel-framing, not as journal flattery.
- Figures 1–3: 200+ dpi raster at final size, legible axis/legend labels,
  log scales labeled.

## Deliverables (this revision)

- manuscript/MAIN_MANUSCRIPT_JQL_FINAL.docx
- manuscript/COVER_LETTER_JQL_FINAL.docx (+ .md source)
- REPRODUCIBILITY_BUNDLE_JQL_FINAL.zip
- ANALYSIS_CODE_JQL_FINAL.zip
- INVERSE_INFERENCE_VERIFICATION.md
- NUMERICAL_CONSISTENCY_AUDIT.md
- TITLE_DECISION.md
- FINAL_QC_REPORT.md (this file)
