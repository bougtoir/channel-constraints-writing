"""POC-3/POC-4: descriptive analysis + dependence-aware model + falsification.

Outputs: figures/, tables/, logs/poc_model.txt, data_processed/poc_stats.csv
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import statsmodels.api as sm

ROOT = os.path.join(os.path.dirname(__file__), "..")
PROC = os.path.join(ROOT, "data_processed")
FIG = os.path.join(ROOT, "figures")
TAB = os.path.join(ROOT, "tables")
LOG = os.path.join(ROOT, "logs")

rng = np.random.default_rng(20261003)


def main():
    os.makedirs(FIG, exist_ok=True)
    os.makedirs(TAB, exist_ok=True)
    os.makedirs(LOG, exist_ok=True)
    df = pd.read_csv(os.path.join(PROC, "poc_dataset.csv"))
    df = df.dropna(subset=["ws_class", "granularity"])
    ana = df.dropna(subset=["P_total", "G"]).copy()
    ana = ana[(ana["P_total"] > 0) & (ana["G"] > 0)]
    ana["logG"] = np.log(ana["G"])
    ana["logP"] = np.log(ana["P_total"])
    ana["gran"] = ana["granularity"].astype(int)

    # ---- Table: class-level summary ----
    tab = df.groupby(["ws_class"], dropna=False).agg(
        n_pairs=("locale", "count"),
        n_with_P=("P_total", "count"),
        G_median=("G", "median"), G_iqr=("G", lambda s: s.quantile(.75)-s.quantile(.25)),
        P_median=("P_total", "median"),
        GP_median=("GP_ratio", "median"),
    ).reset_index()
    tab.to_csv(os.path.join(TAB, "table_class_summary.csv"), index=False)

    # ---- Figure 1: log-log scatter by class ----
    cls_order = ["alphabet", "abjad", "featural", "abugida", "syllabary",
                 "morphosyllabic", "mixed"]
    colors = dict(zip(cls_order, plt.cm.tab10.colors))
    fig, ax = plt.subplots(figsize=(7, 5.2))
    for c in cls_order:
        sub = ana[ana.ws_class == c]
        if len(sub):
            ax.scatter(sub.P_total, sub.G, s=16, alpha=.55,
                       color=colors[c], label=f"{c} (n={len(sub)})")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("Phoneme inventory size P (PHOIBLE)")
    ax.set_ylabel("Grapheme inventory size G (CLDR exemplar)")
    ax.legend(fontsize=8, loc="lower right")
    ax.set_title("Phoneme vs grapheme inventory by writing-system class")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "poc_fig_P_vs_G.png"), dpi=200)
    plt.close(fig)

    # ---- Figure 2: G/P ratio by class ----
    fig, ax = plt.subplots(figsize=(7, 4.6))
    data = [df.loc[df.ws_class == c, "GP_ratio"].dropna() for c in cls_order]
    ax.boxplot([np.log10(x) for x in data], labels=cls_order, showfliers=False)
    for i, x in enumerate(data):
        jitter = rng.normal(0, .04, len(x))
        ax.scatter(np.full(len(x), i + 1) + jitter, np.log10(x), s=8, alpha=.4)
    ax.set_ylabel("log10(G/P)")
    ax.set_title("G/P coupling by writing-system class")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "poc_fig_GP_by_class.png"), dpi=200)
    plt.close(fig)

    # ---- POC-4: dependence-aware model ----
    # logG ~ logP * granularity, crossed random effects: script + language family
    lines = []
    m_formula = "logG ~ logP * gran"
    ana["script_f"] = ana["script"]
    ana["family_f"] = ana["family"].fillna("unknown")
    try:
        ana["grp"] = 1
        m = smf.mixedlm(m_formula, ana,
                        groups=ana["grp"],
                        vc_formula={"script": "0 + C(script_f)",
                                    "family": "0 + C(family_f)"})
        r = m.fit(method="lbfgs", reml=False)
        lines.append(str(r.summary()))
        beta_logP = r.fe_params.get("logP", np.nan)
        beta_int = r.fe_params.get("logP:gran", np.nan)
        lines.append(f"\nlogP coef={beta_logP:.4f}  logP:gran coef={beta_int:.4f}")
        ci = r.conf_int()
        lines.append("\nconf_int:\n" + ci.loc[["logP", "gran", "logP:gran"]].to_string())
    except Exception as e:
        lines.append(f"MixedLM failed: {e}")
        r = smf.ols(m_formula + " + C(script)", ana).fit(
            cov_type="cluster", cov_kwds={"groups": ana["family_f"]})
        lines.append(str(r.summary()))

    # ---- falsification: permute P across unrelated families ----
    obs = {}
    try:
        obs["beta_int"] = r.fe_params["logP:gran"]
    except Exception:
        obs["beta_int"] = np.nan
    perm_stats = []
    ana_p = ana.copy()
    for b in range(200):
        # permute P within granularity strata (keeps marginal distribution)
        ana_p["logP"] = np.nan
        for g, idx in ana.groupby("gran").groups.items():
            vals = ana.loc[idx, "logP"].to_numpy()
            ana_p.loc[idx, "logP"] = rng.permutation(vals)
        try:
            rp = smf.ols("logG ~ logP * gran", ana_p).fit()
            perm_stats.append(rp.params.get("logP:gran", np.nan))
        except Exception:
            pass
    perm_stats = np.array(perm_stats)
    lines.append(f"\nPermutation (within-gran) logP:gran: "
                 f"obs={obs['beta_int']:.4f}, "
                 f"perm mean={np.nanmean(perm_stats):.4f}, "
                 f"perm sd={np.nanstd(perm_stats):.4f}, "
                 f"emp p={np.mean(np.abs(perm_stats) >= abs(obs['beta_int'])):.4f}")

    # ---- leave-one-script-out slope ----
    loo = []
    for s in sorted(ana.script_f.unique()):
        sub = ana[ana.script_f != s]
        try:
            rl = smf.ols("logG ~ logP * gran", sub).fit()
            loo.append({"excluded_script": s,
                        "beta_logP": rl.params["logP"],
                        "beta_int": rl.params["logP:gran"]})
        except Exception:
            pass
    loo = pd.DataFrame(loo)
    loo.to_csv(os.path.join(TAB, "table_loo_script.csv"), index=False)
    lines.append("\nleave-one-script-out logP:gran range: "
                 f"[{loo.beta_int.min():.4f}, {loo.beta_int.max():.4f}]")

    with open(os.path.join(LOG, "poc_model.txt"), "w") as f:
        f.write("\n".join(lines))
    print("\n".join(lines[-12:]))


if __name__ == "__main__":
    main()
