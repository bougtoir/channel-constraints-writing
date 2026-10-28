"""S3 inverse inference: classify ws_class / granularity from symbol stats.

Grouped CV: leave-one-language-family-out and leave-one-script-out.
Baselines: majority class; G-only decision stump.
Outputs: tables/table_inverse_*.csv, logs/inverse_inference.txt
"""
import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import f1_score

ROOT = os.path.join(os.path.dirname(__file__), "..")
PROC = os.path.join(ROOT, "data_processed")
TAB, LOG = (os.path.join(ROOT, d) for d in ("tables", "logs"))
rng = np.random.default_rng(20261003)


def grouped_cv(X, y, groups, clf_factory):
    """macro-F1 per fold; folds with single-class test set are skipped."""
    logo = LeaveOneGroupOut()
    scores = []
    for tr, te in logo.split(X, y, groups):
        if len(np.unique(y[te])) < 1 or len(tr) < 20:
            continue
        clf = clf_factory()
        clf.fit(X[tr], y[tr])
        scores.append(f1_score(y[te], clf.predict(X[te]), average="macro"))
    return np.array(scores)


def main():
    d = pd.read_csv(os.path.join(PROC, "poc_dataset.csv"))
    d = d.dropna(subset=["P_total", "G", "ws_class", "granularity"])
    d = d[(d.P_total > 0) & (d.G > 0) & (d.ws_class != "mixed")].copy()
    d["family"] = d.family.fillna("unknown")
    L = [f"n={len(d)}"]

    feats_full = ["G", "g_aux", "GP_ratio", "n_cons", "n_vow"]
    feats_sym = ["G", "g_aux", "GP_ratio"]  # symbol statistics only
    for name, feats in [("full", feats_full), ("symbol_only", feats_sym)]:
        X = d[feats].fillna(0).to_numpy(float)
        X = np.log1p(np.clip(X, 0, None))
        y = d.ws_class.to_numpy()
        res = {}
        for model_name, factory in [
            ("logreg", lambda: LogisticRegression(max_iter=2000, C=1.0)),
            ("rf", lambda: RandomForestClassifier(300, random_state=0, n_jobs=-1)),
            ("stump_G", lambda: DecisionTreeClassifier(max_depth=1, random_state=0)),
            ("majority", None),
        ]:
            if factory is None:
                scores = np.array([f1_score(y, np.full(len(y), pd.Series(y).mode()[0]),
                                            average="macro")])
            else:
                scores = grouped_cv(X, y, d.family.to_numpy(), factory)
            res[f"{model_name}_family"] = (scores.mean(), scores.std())
            if factory is not None:
                s2 = grouped_cv(X, y, d.script.to_numpy(), factory)
                res[f"{model_name}_script"] = (s2.mean(), s2.std())
        df_res = pd.DataFrame(res, index=["mean_macroF1", "sd"]).T.round(4)
        L.append(f"\n=== features {name} ===\n" + df_res.to_string())
        df_res.to_csv(os.path.join(TAB, f"table_inverse_{name}.csv"))

    # same but predict granularity ordinal as multiclass
    X = np.log1p(np.clip(d[["G", "g_aux"]].fillna(0).to_numpy(float), 0, None))
    y = d.granularity.astype(int).to_numpy()
    sc = grouped_cv(X, y, d.family.to_numpy(),
                    lambda: RandomForestClassifier(300, random_state=0, n_jobs=-1))
    L.append(f"\ngranularity (G+g_aux only), family-grouped RF macroF1: "
             f"{sc.mean():.3f} ± {sc.std():.3f}")
    sc2 = grouped_cv(X, y, d.script.to_numpy(),
                     lambda: RandomForestClassifier(300, random_state=0, n_jobs=-1))
    maj = f1_score(y, np.full(len(y), pd.Series(y).mode()[0]), average="macro")
    L.append(f"script-grouped: {sc2.mean():.3f} ± {sc2.std():.3f}")
    L.append(f"granularity majority-baseline macroF1: {maj:.3f}")
    gran_rows = pd.DataFrame(
        {"mean_macroF1": [sc.mean(), sc2.mean(), maj],
         "sd": [sc.std(), sc2.std(), 0.0]},
        index=["rf_family", "rf_script", "majority"])
    gran_rows.to_csv(os.path.join(TAB, "table_inverse_granularity.csv"))

    a = pd.read_csv(os.path.join(TAB, "table_inverse_symbol_only.csv"), index_col=0)
    a.index.name = "model"; a.insert(0, "target", "ws_class")
    b = gran_rows.copy(); b.index.name = "model"; b.insert(0, "target", "granularity")
    pd.concat([a, b]).reset_index().to_csv(
        os.path.join(TAB, "table_inverse_combined.csv"), index=False)

    with open(os.path.join(LOG, "inverse_inference.txt"), "w") as f:
        f.write("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
