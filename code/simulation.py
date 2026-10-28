"""S2 toy channel simulation (K^L encoding).

Model. A writing system must assign written codes to U encoded units
set by granularity:
  gran 1 (phonemic/abjad): U ~ P (consonants, or C+V for full alphabets)
  gran 2 (akshara/CV):     U ~ C x V + V
  gran 3 (syllabary):      U ~ C x V x closure factor + V
  gran 4 (morphosyllabic): U = morpheme-root inventory (proxy)

Two bounds bracket observed inventories:
  * stored-unit bound: G = U (every encoded unit gets a distinct sign)
  * compositional bound: G = ceil(U^(1/L)) if signs are built
    compositionally from K primitives at depth L (e.g. Hangul jamo,
    Brahmic akshara decomposition). Channel noise eta inflates U:
    U_eff = U/(1-eta).

We test whether granularity alone reproduces the observed orders of
magnitude of G and where each class sits between the two bounds.

Outputs: tables/table_simulation_bounds.csv,
figures/fig_simulation.png, logs/simulation.txt. Seed 20261003.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.join(os.path.dirname(__file__), "..")
PROC = os.path.join(ROOT, "data_processed")
FIG, TAB, LOG = (os.path.join(ROOT, d) for d in ("figures", "tables", "logs"))
rng = np.random.default_rng(20261003)
NREP = 200
ETA_MU, ETA_SD = 0.10, 0.08


def needed_units(gran, C, V):
    if gran == 1:
        return C + V
    if gran == 2:
        return C * V + V
    if gran == 3:
        return C * V * 1.4 + V
    return 2000  # morpheme-root inventory proxy (historical, opaque)


def main():
    d = pd.read_csv(os.path.join(PROC, "poc_dataset.csv"))
    d = d.dropna(subset=["P_total", "G", "granularity"]).copy()
    d = d[(d.P_total > 0) & (d.G > 0)]
    d["C"] = d.n_cons.where(d.n_cons > 0, np.maximum(d.P_total * 0.8, 4))
    d["V"] = d.n_vow.where(d.n_vow > 0, 5)

    L = [f"n={len(d)}"]

    # per-pair simulated bounds at its own granularity
    etas = np.clip(rng.normal(ETA_MU, ETA_SD, (len(d), NREP)), 0, 0.5)
    U = np.array([needed_units(int(g), c, v)
                  for g, c, v in zip(d.granularity, d.C, d.V)])[:, None]
    U_eff = U / (1 - etas)                       # noise-inflated demand
    d["U_med"] = np.median(U_eff, axis=1)
    d["G_compositional"] = np.median(
        np.ceil(U_eff ** (1.0 / d.granularity.to_numpy()[:, None])), axis=1)
    d["G_stored"] = d.U_med

    rows = []
    for g, s in d.groupby("granularity"):
        rows.append({
            "granularity": int(g), "n": len(s),
            "obs_G_median": s.G.median(),
            "sim_stored_median": s.G_stored.median(),
            "sim_compositional_median": s.G_compositional.median(),
            "obs_within_bounds_frac":
                ((s.G >= s.G_compositional * 0.5)
                 & (s.G <= s.G_stored * 2)).mean()})
    t = pd.DataFrame(rows)
    t.to_csv(os.path.join(TAB, "table_simulation_bounds.csv"), index=False)
    L.append("simulated bounds vs observed G:\n" + t.to_string())

    # counterfactual: re-encode every system at every granularity
    cf = []
    for gnew in (1, 2, 3, 4):
        Usim = np.array([needed_units(gnew, c, v)
                         for c, v in zip(d.C, d.V)])
        cf.append({"reencoded_granularity": gnew,
                   "U_median": np.median(Usim),
                   "U_iqr": f"[{np.percentile(Usim,25):.0f},{np.percentile(Usim,75):.0f}]",
                   "range": f"{Usim.min():.0f}-{Usim.max():.0f}"})
    tc = pd.DataFrame(cf)
    tc.to_csv(os.path.join(TAB, "table_simulation_counterfactual.csv"), index=False)
    L.append("\ncounterfactual stored-unit demand by granularity "
             "(same phonologies, different depth):\n" + tc.to_string())

    # figure: observed G vs simulated stored-unit demand, colored by gran
    fig, ax = plt.subplots(figsize=(6, 5.5))
    for g, s in d.groupby("granularity"):
        ax.scatter(s.G_stored, s.G, s=10, alpha=.45, label=f"gran {int(g)}")
    lim = [8, 6000]
    ax.plot(lim, lim, "k--", lw=1)
    ax.set(xscale="log", yscale="log", xlim=lim, ylim=lim,
           xlabel="simulated stored-unit demand U (noise-inflated)",
           ylabel="observed G")
    ax.legend(title="granularity", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_simulation.png"), dpi=200)

    # slope check: log G ~ log U within gran (stored-unit model fit)
    from scipy.stats import pearsonr
    for g, s in d.groupby("granularity"):
        if len(s) > 10 and s.G_stored.nunique() > 2:
            r = pearsonr(np.log10(s.G_stored), np.log10(s.G))
            L.append(f"gran {int(g)}: r(log10 U, log10 G) = {r.statistic:.3f} "
                     f"(n={len(s)})")

    with open(os.path.join(LOG, "simulation.txt"), "w") as f:
        f.write("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
