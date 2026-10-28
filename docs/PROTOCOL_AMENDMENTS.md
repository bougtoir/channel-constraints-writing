# Protocol amendments (post-freeze)

All amendments after SAP freeze (2026-10-03, commit 6ef2860):

1. **S1 implementation**: ASJP supplies *spoken* word length (segment count
   per Swadesh gloss), not written. Written-side escape uses `wordfreq`
   top-1000 token mean orthographic length (exact language-code match only,
   no nearest-match fallback; 287 pairs). Both reported.
2. **S2 reframed**: implemented as two bounds — stored-unit demand
   U(granularity) vs compositional bound ceil(U^{1/L}) — rather than a
   K*,L* optimizer, matching observable G to bounds. Mechanism illustration
   only, as frozen.
3. **F2 implementation**: label-shuffle control applied to the within-class
   coupling pattern (max |rho|) and granularity->G Kruskal separation, plus
   P-permutation control — same falsification target as the frozen F2.
4. ASJP doculects aggregated to one observation per ISO6393 before merge
   (unit-of-analysis integrity).
