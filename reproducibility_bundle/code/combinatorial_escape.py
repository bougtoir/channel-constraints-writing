"""S1 combinatorial escape: spoken word length (ASJP) vs P and G.

ASJP doculect-level mean segment count per Swadesh gloss, joined to
language x script pairs via ISO6393. Predictions (SAP S1): smaller
inventories (P or G) associate with longer coded forms.

Outputs: tables/table_escape_*.csv, figures/fig_escape.png, logs/escape.txt
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
RAW = os.path.join(ROOT, "data_raw")
PROC = os.path.join(ROOT, "data_processed")
FIG, TAB, LOG = (os.path.join(ROOT, d) for d in ("figures", "tables", "logs"))
rng = np.random.default_rng(20261003)
B = 2000


def fam_boot(s, xcol, ycol, B=B):
    fam = s.family.to_numpy()
    keys = np.unique(fam)
    ib = {k: np.where(fam == k)[0] for k in keys}
    boots = []
    for i in range(B):
        dr = rng.choice(keys, len(keys), True)
        ii = np.concatenate([ib[k] for k in dr])
        x = s[xcol].to_numpy()[ii]; y = s[ycol].to_numpy()[ii]
        boots.append(spearmanr(x, y).statistic)
    return np.nanpercentile(boots, [2.5, 97.5])


def main():
    forms = pd.read_csv(os.path.join(RAW, "asjp", "forms.csv"),
                        usecols=["Language_ID", "Segments"])
    wl = (forms.assign(nseg=forms.Segments.fillna("").str.split().str.len())
                .groupby("Language_ID").nseg.mean()
                .rename("mean_word_segments").reset_index())
    langs = pd.read_csv(os.path.join(RAW, "asjp", "languages.csv"),
                        usecols=["ID", "ISO639P3code", "Glottocode", "Family"])
    # aggregate ASJP doculects to one observation per ISO6393
    wl = wl.merge(langs, left_on="Language_ID", right_on="ID")
    wl = (wl.groupby("ISO639P3code")
            .agg(mean_word_segments=("mean_word_segments", "mean"),
                 n_doculects=("mean_word_segments", "size"))
            .reset_index())

    d = pd.read_csv(os.path.join(PROC, "poc_dataset.csv"))
    d = d.dropna(subset=["P_total", "G", "ws_class"]).copy()
    d = d[(d.P_total > 0) & (d.G > 0)]
    d["family"] = d.family.fillna("unknown")
    m = d.merge(wl[["ISO639P3code", "mean_word_segments", "n_doculects"]],
                left_on="iso3", right_on="ISO639P3code")
    L = [f"pairs with ASJP word length: {len(m)}"]
    m.to_csv(os.path.join(PROC, "escape_dataset.csv"), index=False)

    rows = []
    for label, sub in [("all", m)] + [(c, m[m.ws_class == c])
                                      for c in sorted(m.ws_class.unique())]:
        if len(sub) < 15:
            continue
        r = {}
        r["subset"] = label; r["n"] = len(sub)
        for (x, name) in [("P_total", "rho_P_vs_wlen"), ("G", "rho_G_vs_wlen")]:
            sr = spearmanr(sub[x], sub.mean_word_segments)
            r[name] = sr.statistic
            r[name + "_p"] = sr.pvalue
            lo, hi = fam_boot(sub, x, "mean_word_segments")
            r[name + "_ci"] = f"[{lo:.3f},{hi:.3f}]"
        rows.append(r)
    t = pd.DataFrame(rows)
    t.to_csv(os.path.join(TAB, "table_escape_spearman.csv"), index=False)
    L.append("\n" + t.to_string())

    # multivariate: mean word length ~ logP + logG + granularity
    sub = m.copy()
    sub["logP"] = np.log(sub.P_total); sub["logG"] = np.log(sub.G)
    sub["wl"] = np.log(sub.mean_word_segments)
    try:
        r = smf.ols("wl ~ logP + logG + C(granularity)", sub).fit(
            cov_type="cluster", cov_kwds={"groups": sub.family})
        L.append("\nOLS wl ~ logP + logG + C(gran), family-clustered SE:\n"
                 + r.summary2().tables[1].loc[["logP", "logG"]].to_string())
    except Exception as e:
        L.append(f"OLS failed: {e}")

    # written-side: wordfreq top-1000 mean orthographic length where available
    try:
        from wordfreq import top_n_list, available_languages
        avail = set(available_languages().keys())
        wl_rows = []
        for loc, sub in d.groupby("iso3"):
            lang_code = sub.iloc[0].locale.split("-")[0]
            if lang_code not in avail:  # no silent nearest-match fallback
                continue
            words = top_n_list(lang_code, 1000)
            if len(words) >= 500:
                wl_rows.append({"iso3": loc,
                                "mean_orth_wordlen": np.mean([len(w) for w in words])})
        wfreq = pd.DataFrame(wl_rows).drop_duplicates("iso3")
        mw = d.merge(wfreq, on="iso3") if len(wfreq) else d.iloc[0:0]
        L.append(f"\nwordfreq-matched pairs: {len(mw)}")
        if len(mw) > 15:
            for x, nm in [("G", "rho_G"), ("P_total", "rho_P")]:
                sr = spearmanr(mw[x], mw.mean_orth_wordlen)
                lo, hi = fam_boot(mw.assign(family=mw.family.fillna("unknown")),
                                  x, "mean_orth_wordlen")
                L.append(f"{nm}(., mean_orth_wordlen) = {sr.statistic:.3f} "
                         f"(p={sr.pvalue:.4f}, fam-boot CI [{lo:.3f},{hi:.3f}])")
            mw.to_csv(os.path.join(PROC, "escape_written.csv"), index=False)
    except Exception as e:
        L.append(f"wordfreq skipped: {e}")

    # figure
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    for cls, sub in m.groupby("ws_class"):
        axes[0].scatter(sub.P_total, sub.mean_word_segments, s=12, alpha=.4, label=cls)
    axes[0].set(xlabel="P (phoneme inventory)", ylabel="Mean word length (segments)",
                title="spoken side (ASJP)")
    axes[0].legend(fontsize=7)
    axes[1].scatter(m.G, m.mean_word_segments, s=12, alpha=.4)
    axes[1].set(xscale="log", xlabel="G (grapheme inventory)",
                title="written-side inventory vs spoken word length")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_escape.png"), dpi=200)

    with open(os.path.join(LOG, "escape.txt"), "w") as f:
        f.write("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
