"""F2 negative controls: shuffled ws_class labels and permuted P.

If the granularity/G relationship were a pipeline artifact, the same
signal should appear under shuffled architecture labels. We rerun the
family-clustered bootstrap Spearman rho(P,G) per class under 200 label
permutations, and the granularity-vs-G Kruskal separation under 200
label shuffles. Also permutes P globally to break any real P->G link.

Outputs: tables/table_falsif_shuffle.csv, logs/falsification_f2.txt
"""
import os
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, kruskal

ROOT = os.path.join(os.path.dirname(__file__), "..")
PROC = os.path.join(ROOT, "data_processed")
TAB, LOG = (os.path.join(ROOT, d) for d in ("tables", "logs"))
rng = np.random.default_rng(20261003)
B = 200


def class_stat(P, G, cls):
    rhos = []
    for c in np.unique(cls):
        m = cls == c
        if m.sum() >= 15:
            rhos.append(spearmanr(P[m], G[m]).statistic)
    return rhos


def main():
    d = pd.read_csv(os.path.join(PROC, "poc_dataset.csv"))
    d = d.dropna(subset=["P_total", "G", "ws_class"]).copy()
    d = d[(d.P_total > 0) & (d.G > 0)]
    P, G, cls = d.P_total.to_numpy(), d.G.to_numpy(), d.ws_class.to_numpy()
    gran = d.granularity.to_numpy()

    obs_rhos = class_stat(P, G, cls)
    H_obs, _ = kruskal(*[G[gran == g] for g in np.unique(gran)])

    null_max, null_H = [], []
    for _ in range(B):
        perm = rng.permutation(len(d))
        nr = class_stat(P, G, cls[perm])
        null_max.append(max(np.abs(nr)) if nr else 0)
        null_H.append(kruskal(*[G[perm][gran == g]
                                for g in np.unique(gran)]).statistic)
    p_max = (np.sum(np.array(null_max) >= max(np.abs(obs_rhos))) + 1) / (B + 1)
    p_H = (np.sum(np.array(null_H) >= H_obs) + 1) / (B + 1)

    # P-permutation: destroy true P->G relation, keep labels
    null_rho = [abs(spearmanr(G, P[rng.permutation(len(d))]).statistic)
                for _ in range(B)]
    rho_obs = abs(spearmanr(P, G).statistic)
    p_permP = (np.sum(np.array(null_rho) >= rho_obs) + 1) / (B + 1)

    L = [f"n={len(d)}, B={B}",
         f"observed max |within-class rho(P,G)| = {max(np.abs(obs_rhos)):.3f}",
         f"shuffled-label null max: "
         f"{np.percentile(null_max,[50,95]).round(3)} -> p={p_max:.3f}",
         f"observed Kruskal H(G|granularity) = {H_obs:.1f}",
         f"shuffled-label null H 95% = {np.percentile(null_H,95):.1f} -> p={p_H:.4f}",
         f"observed |rho(P,G)| = {rho_obs:.3f}, P-permutation p={p_permP:.4f}"]
    print("\n".join(L))
    pd.DataFrame({
        "control": ["shuffle_ws_class_max_rho", "shuffle_ws_class_kruskalH",
                    "permute_P_rho"],
        "observed": [max(np.abs(obs_rhos)), H_obs, rho_obs],
        "null_95": [np.percentile(null_max, 95),
                    np.percentile(null_H, 95),
                    np.percentile(null_rho, 95)],
        "p": [p_max, p_H, p_permP]}).to_csv(
        os.path.join(TAB, "table_falsif_shuffle.csv"), index=False)
    with open(os.path.join(LOG, "falsification_f2.txt"), "w") as f:
        f.write("\n".join(L))


if __name__ == "__main__":
    main()
