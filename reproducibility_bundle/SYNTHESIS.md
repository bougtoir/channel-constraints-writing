# SYNTHESIS — Phase 5

## Verdict: **GO** (as revised at POC). Contribution type: (C)
dependence-aware comparative analysis of progressive decoupling +
(B) primitive-inventory/combinatorial-depth bounds + (D) a partially
validated inverse-inference framework. NOT (A): no new general model
survives — the honest finding is a reframing.

## The result in one sentence

Phoneme inventory P is essentially constant across writing-system
architectures (median 43–49), while symbol inventory G shifts by orders
of magnitude with encoded-unit granularity (median 27 → 63 → 213 →
2210): what constrains writing systems is *how big the encoded unit is*
and *whether signs are stored or composed*, not the size of the
phonological channel they encode.

## Confirmatory findings (PRIMARY, survived controls)

| Finding | Evidence |
|---|---|
| P is decoupled from architecture | medians 43–49 across all granularity levels (T1); script-cluster bootstrap CIs |
| Granularity sets the scale of G | Kruskal H=190.1 vs shuffled-label null 95% = 6.8, permutation p=0.005 (F2) |
| Survives exclusions | F3: no Latin, no Han-derived, no single-language scripts — class medians and coupling pattern stable |
| Mixed model | logP main effect null (β=0.02, CI [-0.05,0.09]); granularity×logP interaction positive only at syllabic level |

## Findings that did NOT survive controls (reported as exploratory)

- Within-class ρ(P,G) pattern (alphabet −0.09, abjad +0.31, abugida
  +0.47): the abugida coefficient itself is significant (CI
  [0.10,0.61], F1 perm p<0.005), but the *pattern of differences*
  between classes does not exceed what label shuffling produces
  (F2 max-|rho| p=0.154). Reported as suggestive, not confirmatory.
- H1 as originally stated (uniform channel coupling) is falsified:
  coupling is absent precisely where it was predicted strongest
  (alphabets).

## Null results (kept, per protocol)

- Overall ρ(P,G) = 0.09 (weak; P-permutation p=0.04 but trivial effect).
- Spoken-side combinatorial escape null: ρ(P, ASJP word length) ≈ 0.01
  overall; −0.05 within alphabets.
- Inverse inference adds nothing beyond G: ws_class macro-F1 0.70 with
  all features vs 0.71 with a G-only stump — symbol statistics beyond
  inventory size carry no additional class signal under grouped CV.

## Secondary findings

- Written-side: ρ(P, mean orthographic word length) = −0.40 (fam-boot CI
  [−0.94,−0.11]) — the classic phoneme-vs-length trade-off replicates on
  the written surface, but ρ(G, word length) = +0.13 (CI crosses 0):
  the trade-off lives in phonology, not in the letter inventory.
- Simulation bounds: observed G sits between stored-unit demand U and
  the compositional bound U^{1/L}; abugidas cluster near the
  compositional bound (real composition), alphabets undershoot U
  (not every phoneme gets a letter), syllabaries sit mid-range.
- Inverse inference IS meaningful at the granularity level:
  granularity predicted at macro-F1 0.76 (family-grouped) from
  (G, G_aux) alone — the recoverable signal of an unknown channel is
  encoded-unit size, not its phonology.

## What the paper claims

1. Dependence-aware comparative evidence that P and G are decoupled
   across architectures (C).
2. A two-bound framework (stored-unit vs compositional) that locates
   each architecture class in inventory space (B).
3. A validated inverse-inference result: granularity (encoded-unit
   size) is recoverable from inventory statistics alone; class labels
   beyond that are not (D).
4. Explicitly reported nulls: naive P–G coupling and spoken-side
   inventory–length trade-off do not generalize.
