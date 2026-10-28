"""PRIMARY/SECONDARY analysis per SAP_FROZEN.md.

P1 class-median contrasts (script-cluster bootstrap)
P2 within-class Spearman coupling (family-cluster bootstrap CI)
P3 crossed mixed-effects logG ~ logP * C(granularity)
F1/F2/F3 falsification controls

Outputs: tables/table_primary_*.csv, figures/fig_*.png, logs/full_analysis.txt
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from scipy.stats import spearmanr

ROOT = os.path.join(os.path.dirname(__file__), "..")
PROC = os.path.join(ROOT, "data_processed")
FIG, TAB, LOG = (os.path.join(ROOT, d) for d in ("figures", "tables", "logs"))
rng = np.random.default_rng(20261003)
B = 2000


def cluster_boot(x, clusters, stat, b=B, rng=rng):
    """Bootstrap CI resampling clusters."""
    vals = np.asarray(list(stat(x)))
    keys = np.unique(clusters)
    out = np.empty((b, len(vals)))
    idx_by = {k: np.where(clusters == k)[0] for k in keys}
    for i in range(b):
        draw = rng.choice(keys, size=len(keys), replace=True)
        ii = np.concatenate([idx_by[k] for k in draw])
        try:
            out[i] = stat(ii, x)
        except Exception:
            out[i] = np.nan
    return vals, np.nanpercentile(out, [2.5, 97.5], axis=0)


def main():
    os.makedirs(LOG, exist_ok=True)
    df = pd.read_csv(os.path.join(PROC, "poc_dataset.csv"))
    d = df.dropna(subset=["P_total", "G", "ws_class", "granularity"]).copy()
    d = d[(d.P_total > 0) & (d.G > 0)]
    d["logG"] = np.log(d.G)
    d["logP"] = np.log(d.P_total)
    d["gran"] = d.granularity.astype(int)
    d["family"] = d.family.fillna("unknown")
    L = []

    # ---------- P1: class medians with script-cluster bootstrap ----------
    rows = []
    for g in sorted(d.gran.unique()):
        s = d[d.gran == g]
        scr = s.script.to_numpy()
        n_scr = len(set(scr))
        for var in ["G", "P_total", "GP_ratio"]:
            stat = lambda ii, x=None, s=s, v=var: s[v].to_numpy()[ii].mean() if False else np.median(s[v].to_numpy()[ii])
            if n_scr > 1:
                vals = []
                keys = np.unique(scr)
                ib = {k: np.where(scr == k)[0] for k in keys}
                boots = np.empty(B)
                for i in range(B):
                    draw = rng.choice(keys, len(keys), True)
                    ii = np.concatenate([ib[k] for k in draw])
                    boots[i] = np.median(s[var].to_numpy()[ii])
                lo, hi = np.percentile(boots, [2.5, 97.5])
            else:
                lo = hi = np.nan
            rows.append({"gran": g, "var": var, "n": len(s), "n_scripts": n_scr,
                         "median": s[var].median(), "ci_lo": lo, "ci_hi": hi})
    t1 = pd.DataFrame(rows)
    t1.to_csv(os.path.join(TAB, "table_primary_class_medians.csv"), index=False)
    L.append("P1 class medians (script-cluster bootstrap):\n" + t1.to_string())

    # ---------- P2: within-class Spearman with family-cluster bootstrap ----------
    rows = []
    for cls in sorted(d.ws_class.unique()):
        s = d[d.ws_class == cls]
        if len(s) < 10:
            continue
        fam = s.family.to_numpy()
        keys = np.unique(fam)
        ib = {k: np.where(fam == k)[0] for k in keys}
        rho = spearmanr(s.P_total, s.G).statistic
        p = spearmanr(s.P_total, s.G).pvalue
        if len(keys) > 1:
            boots = np.empty(B)
            for i in range(B):
                dr = rng.choice(keys, len(keys), True)
                ii = np.concatenate([ib[k] for k in dr])
                if len(np.unique(ii)) > 5:
                    boots[i] = spearmanr(s.P_total.to_numpy()[ii], s.G.to_numpy()[ii]).statistic
                else:
                    boots[i] = np.nan
            lo, hi = np.nanpercentile(boots, [2.5, 97.5])
        else:
            lo = hi = np.nan
        rows.append({"ws_class": cls, "n": len(s), "n_families": len(keys),
                     "rho": rho, "p": p, "ci_lo": lo, "ci_hi": hi})
    t2 = pd.DataFrame(rows)
    t2.to_csv(os.path.join(TAB, "table_primary_within_class_rho.csv"), index=False)
    L.append("\nP2 within-class Spearman rho(P,G) (family-cluster bootstrap):\n" + t2.to_string())

    # ---------- P3: crossed mixed-effects ----------
    try:
        d["grp"] = 1
        m = smf.mixedlm("logG ~ logP * C(gran)", d, groups=d["grp"],
                        vc_formula={"script": "0 + C(script)", "family": "0 + C(family)"})
        r = m.fit(method="lbfgs", reml=False)
        L.append("\nP3 mixed model:\n" + str(r.summary()))
        coefs = r.fe_params
        ci = r.conf_int().loc[coefs.index]
        t3 = pd.DataFrame({"term": coefs.index, "coef": coefs.values,
                           "ci_lo": ci[0].values, "ci_hi": ci[1].values})
    except Exception as e:
        L.append(f"MixedLM failed ({e}); fallback OLS cluster-robust")
        r = smf.ols("logG ~ logP * C(gran)", d).fit(
            cov_type="cluster", cov_kwds={"groups": d["family"]})
        L.append(str(r.summary()))
        t3 = pd.DataFrame({"term": r.params.index, "coef": r.params.values,
                           "ci_lo": r.conf_int()[0].values, "ci_hi": r.conf_int()[1].values})
    t3.to_csv(os.path.join(TAB, "table_primary_model.csv"), index=False)

    # ---------- Figure: conceptual scatter + per-class medians ----------
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    for cls, sub in d.groupby("ws_class"):
        axes[0].scatter(sub.P_total, sub.G, s=12, alpha=.4, label=cls)
    axes[0].set(xscale="log", yscale="log",
                xlabel="Phoneme inventory P", ylabel="Grapheme inventory G")
    axes[0].legend(fontsize=7)
    t1g = t1[t1["var"] == "G"].sort_values("gran")
    axes[1].errorbar(t1g.gran, t1g["median"],
                     yerr=[t1g["median"] - t1g.ci_lo, t1g.ci_hi - t1g["median"]],
                     fmt="o-", capsize=4)
    axes[1].set(yscale="log", xlabel="Encoded-unit granularity",
                ylabel="Median G (95% CI)")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_scatter_and_medians.png"), dpi=200)
    plt.close(fig)

    # ---------- F1: permute P within granularity (within-class rho under H0) ----------
    obs = t2.set_index("ws_class")["rho"]
    perm_out = {}
    dpp = d.copy()
    for cls in obs.index:
        s_idx = dpp.index[dpp.ws_class == cls]
        rhos = []
        for i in range(300):
            perm = rng.permutation(dpp.loc[s_idx, "P_total"].to_numpy())
            rhos.append(spearmanr(perm, dpp.loc[s_idx, "G"].to_numpy()).statistic)
        perm_out[cls] = {"perm_mean": np.mean(rhos), "perm_sd": np.std(rhos),
                         "emp_p": np.mean(np.abs(rhos) >= abs(obs[cls]))}
    t4 = pd.DataFrame(perm_out).T
    t4.to_csv(os.path.join(TAB, "table_falsif_perm_within_class.csv"))
    L.append("\nF1 permutation within class:\n" + t4.to_string())

    # ---------- F3: exclusions ----------
    for label, sub in [("no_Latn", d[d.script != "Latn"]),
                       ("no_Han", ~d.script.isin(["Hans", "Hant", "Jpan", "Kore"])),
                       ("no_singleton_scripts", d.groupby("script")["script"].transform("count") > 1)]:
        if isinstance(sub, pd.Series):
            sub = d[sub]
        rr = []
        for cls in sorted(sub.ws_class.unique()):
            s = sub[sub.ws_class == cls]
            if len(s) >= 10:
                rr.append(f"{cls}:rho={spearmanr(s.P_total,s.G).statistic:.3f}(n={len(s)})")
        L.append(f"F3 {label} (n={len(sub)}): " + "; ".join(rr))

    with open(os.path.join(LOG, "full_analysis.txt"), "w") as f:
        f.write("\n".join(L))
    print("\n".join(L[-5:]))


if __name__ == "__main__":
    main()
