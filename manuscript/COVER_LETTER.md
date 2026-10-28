Dear Editor,

I submit my manuscript, "Encoded-unit granularity, not phonological channel size, sets the scale of writing-system symbol inventories," for consideration in the Journal of Quantitative Linguistics. Writing systems vary from a few dozen recurrent symbols to inventories in the thousands. The intuitive account — that this variation tracks the size of the phonological inventory being encoded — has never been tested under dependence-aware comparative inference. I test it, and it fails.

I assembled a dependence-aware dataset of {N_TOTAL} language×script pairs linking PHOIBLE phoneme inventories, CLDR grapheme exemplars, and Glottolog genealogies, with a frozen analysis plan, cluster-resampled confidence intervals, grouped cross-validation, and three families of negative controls. The result is a sharp decoupling: median phoneme inventory size is essentially constant across architectures ({P_MED_RANGE}), while median symbol inventory size shifts over two orders of magnitude with encoded-unit granularity ({G_MED_LIST}).

The null results are what make this credible. The theoretically obvious prediction — that phonographic scripts should show the strongest P–G coupling — is unsupported: alphabets show none (rho = {RHO_ALPH}), the cross-class coupling pattern does not exceed a label-permutation null, and the classic inventory–length trade-off fails on the spoken side. These negatives redirect the explanation from channel size to architecture: what linguistic unit the script encodes, and whether its signs are stored or composed. A K^L simulation locates each class between a stored-unit bound and a compositional bound, reproducing the observed orders of magnitude.

The paper's second contribution is an identifiability boundary for inverse inference. Using only directly observable inventory statistics, encoded-unit granularity remains recoverable under grouped cross-validation (macro-F1 = {F1_GRAN_FAM}), whereas finer architecture labels gain little beyond raw inventory size, and the underlying phonological inventory is not recoverable at all.

I believe the paper belongs in this journal specifically because it pairs a falsifiable quantitative hypothesis with dependence-aware comparative statistics and explicit negative controls — the methodological combination the journal has long cultivated for quantitative typology and writing-system research — and because its main finding is a calibrated null that reframes a textbook intuition rather than a new positive law.

The manuscript is original, not under consideration elsewhere. I declare no competing interests. All analysis code, the script-type codebook, and derived data are openly available for verification.

Sincerely,

Onishi Tatsuki
Graduate School of Data Science, Shiga University
Hikone, Japan
