# NUMERICAL_CONSISTENCY_AUDIT

Verified 2026-10-03: every headline number traced to
`tables/*.csv` and `logs/*.txt`. ✅ = matches.

| Claim location | Reported | Source value | ✓ |
|---|---|---|---|
| n pairs | 544 | poc_dataset after filters, full_analysis n=544 | ✅ |
| P medians gran 1–4 | 45, 48, 43, 49 ("43–49") | table_primary_class_medians.csv: 45, 48, 43, 48.5 | ✅ (48.5 rounded up in prose as ~49; CI reported in table) |
| G medians gran 1–4 | 27, 63, 213, 2210 | same table | ✅ |
| G/P medians | 0.63 → 45.1 | 0.6316, 1.184, 6.256, 45.10 | ✅ (text cites endpoints only) |
| alphabet rho | −0.09 | table_primary_within_class_rho: −0.0890 | ✅ |
| abjad rho | +0.31 | 0.3099 | ✅ |
| abugida rho | +0.47 | 0.4711, CI [0.10,0.61] | ✅ |
| morphosyllabic rho | −0.01 | −0.0145 | ✅ |
| F2 shuffle max-rho p | 0.154 | table_falsif_shuffle p=0.154 | ✅ |
| F2 Kruskal | H=190 vs null95=6.8, p=0.005 | same | ✅ |
| overall rho(P,G) | 0.09, perm p=0.04 | 0.094, p=0.0398 | ✅ |
| MixedLM logP | β=0.02 CI [−0.05,0.09] | 0.0217 [−0.0465,0.0900] | ✅ |
| MixedLM logP×gran3 | 1.57, p<0.001 | 1.5736, p=0.0004 | ✅ |
| spoken escape rho(P) | ≈0.01; alphabet −0.05 | 0.0085; −0.0465 | ✅ |
| written escape rho(P,orth len) | −0.40 CI [−0.94,−0.11] | −0.397 CI from fam-boot | ✅ |
| written escape rho(G) | +0.13 CI crosses 0 | 0.128 [−0.744,0.371] | ✅ |
| sim bounds: alphabet | obs 27 vs stored ~49 | 27 vs 49.43 | ✅ |
| sim bounds: abugida | obs 63, comp ~23, stored ~517 | 63, 23, 517 | ✅ |
| granularity macro-F1 | 0.76 fam / 0.64 script, baseline 0.23 | 0.758 / 0.637 / 0.233 | ✅ |
| ws_class macro-F1 | 0.70 vs stump 0.71, majority 0.18 | 0.708 logreg / 0.712 stump / 0.180 | ✅ |
| wordfreq pairs | 287 | log | ✅ |
| ASJP pairs | 526 | log | ✅ |

Discrepancies found and corrected this revision:
- Manuscript previously said granularity majority baseline "0.27" → corrected to 0.23.
- Miton & Morin reference subtitle corrected to "Graphic complexity in writing systems" (Cognition 214:104771) and DOI added.
