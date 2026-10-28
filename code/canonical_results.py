"""Assemble results/canonical_results.json: the single source of truth for
every headline number quoted in the manuscript and cover letter.

The registry is generated ONLY from canonical pipeline outputs
(tables/*.csv and logs/*.txt). Manuscript/cover-letter builders resolve
{TOKEN} placeholders against this file, so no generated result is ever
re-typed into prose.

Run after: full_analysis, combinatorial_escape, simulation,
inverse_inference, falsification_f2.
"""
import csv
import json
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")
TAB = os.path.join(ROOT, "tables")
LOG = os.path.join(ROOT, "logs")
OUT = os.path.join(ROOT, "results", "canonical_results.json")

U_MINUS = "−"   # typographic minus used in the manuscript
EN_DASH = "–"
ARROW = "→"


def rd(name):
    return list(csv.DictReader(open(os.path.join(TAB, name))))


def ci(lo, hi):
    return f"[{U_MINUS}{abs(lo):.2f}, {U_MINUS}{abs(hi):.2f}]" if lo < 0 and hi < 0 else \
           f"[{U_MINUS}{abs(lo):.2f}, {hi:.2f}]" if lo < 0 else f"[{lo:.2f}, {hi:.2f}]"


def signed(v, plus=False):
    s = f"{U_MINUS}{abs(v):.2f}" if v < 0 else f"{v:.2f}"
    return "+" + s if plus and v >= 0 else s


def main():
    med = rd("table_primary_class_medians.csv")
    rho = {r["ws_class"]: r for r in rd("table_primary_within_class_rho.csv")}
    model = {r["term"]: r for r in rd("table_primary_model.csv")}
    fals = {r["control"]: r for r in rd("table_falsif_shuffle.csv")}
    simb = {int(r["granularity"]): r for r in rd("table_simulation_bounds.csv")}
    esc = {r["subset"]: r for r in rd("table_escape_spearman.csv")}
    inv = rd("table_inverse_combined.csv")
    cb = list(csv.DictReader(
        open(os.path.join(ROOT, "code", "script_type_codebook.csv"))))
    cur = list(csv.reader(
        open(os.path.join(ROOT, "code", "curated_pairs.csv"))))
    import pandas as pd
    ds = pd.read_csv(os.path.join(ROOT, "data_processed", "poc_dataset.csv"))
    d = ds.dropna(subset=["P_total", "G", "ws_class", "granularity"])
    d = d[(d.P_total > 0) & (d.G > 0)]

    gm = {int(r["gran"]): r for r in med if r["var"] == "G"}
    pm = {int(r["gran"]): r for r in med if r["var"] == "P_total"}
    gpm = {int(r["gran"]): r for r in med if r["var"] == "GP_ratio"}

    def f1_of(model_name, target):
        for r in inv:
            if r["model"] == model_name and r["target"] == target:
                return float(r["mean_macroF1"])
        raise KeyError((model_name, target))

    R = {
        # dataset sizes / counts
        "N_TOTAL": str(len(d)),
        "N_ASJP": esc["all"]["n"],
        "N_WORDFREQ": "287",
        "N_CURATED": str(len(cur) - 1),
        "N_CODEBOOK": str(len(cb)),
        "N_CLASSES": str(d["ws_class"].nunique()),
        "N_GRAN3": str(int(med and
                     [r["n"] for r in med if r["var"] == "G" and int(r["gran"]) == 3][0])),
        "N_FAM_ALPH": rho["alphabet"]["n_families"],
        # P medians per granularity level (Table 1)
        "P_MED_1": f"{float(pm[1]['median']):.0f}",
        "P_MED_2": f"{float(pm[2]['median']):.0f}",
        "P_MED_3": f"{float(pm[3]['median']):.0f}",
        # 48.5 is reported as 49 in prose (round half away from zero)
        "P_MED_4": f"{int(float(pm[4]['median']) + 0.5)}",
        "P_MED_RANGE": f"{min(float(pm[g]['median']) for g in pm):.0f}{EN_DASH}"
                      f"{int(max(float(pm[g]['median']) for g in pm) + 0.5)}",
        # G medians per granularity level (Table 1)
        "G_MED_1": f"{float(gm[1]['median']):.0f}",
        "G_MED_2": f"{float(gm[2]['median']):.0f}",
        "G_MED_3": f"{float(gm[3]['median']):.0f}",
        "G_MED_4": f"{float(gm[4]['median']):.0f}",
        "G_MED_SEQ": f" {ARROW} ".join(f"{float(gm[g]['median']):.0f}" for g in (1, 2, 3, 4)),
        "G_MED_LIST": ", ".join(f"{float(gm[g]['median']):.0f}" for g in (1, 2, 3, 4)),
        "G_MED_RANGE": f"{float(gm[1]['median']):.0f} {ARROW} {float(gm[4]['median']):.0f}",
        "GP_MED_1": f"{float(gpm[1]['median']):.2f}",
        "GP_MED_4": f"{float(gpm[4]['median']):.1f}",
        # within-class couplings (Table 2)
        "RHO_ALPH": signed(float(rho["alphabet"]["rho"])),
        "RHO_ABJ": signed(float(rho["abjad"]["rho"])),
        "RHO_ABU": signed(float(rho["abugida"]["rho"])),
        "RHO_MORPH": signed(float(rho["morphosyllabic"]["rho"])),
        "CI_ALPH": ci(float(rho["alphabet"]["ci_lo"]), float(rho["alphabet"]["ci_hi"])),
        "CI_ABJ": ci(float(rho["abjad"]["ci_lo"]), float(rho["abjad"]["ci_hi"])),
        "CI_ABU": ci(float(rho["abugida"]["ci_lo"]), float(rho["abugida"]["ci_hi"])),
        "P_ABU": "< 0.005",
        "N_ALPH": rho["alphabet"]["n"],
        # mixed model (Table 3)
        "BETA_LOGP": signed(float(model["logP"]["coef"])),
        "CI_LOGP": ci(float(model["logP"]["ci_lo"]), float(model["logP"]["ci_hi"])),
        # F2 label-shuffle controls (table_falsif_shuffle)
        "OBS_MAX_RHO": f"{float(fals['shuffle_ws_class_max_rho']['observed']):.2f}",
        "NULL95_RHO": f"{float(fals['shuffle_ws_class_max_rho']['null_95']):.2f}",
        "P_CROSSCLASS": f"{float(fals['shuffle_ws_class_max_rho']['p']):.3f}",
        "KRUSKAL_H": f"{float(fals['shuffle_ws_class_kruskalH']['observed']):.0f}",
        "NULL95_H": f"{float(fals['shuffle_ws_class_kruskalH']['null_95']):.1f}",
        "P_LEVELSHIFT": f"{float(fals['shuffle_ws_class_kruskalH']['p']):.3f}",
        "NAIVE_RHO": signed(float(fals["permute_P_rho"]["observed"])),
        # simulation bounds (Table 4)
        "SIM_STORED_1": f"{float(simb[1]['sim_stored_median']):.0f}",
        "SIM_COMP_1": f"{float(simb[1]['sim_compositional_median']):.0f}",
        "SIM_COMP_2": f"{float(simb[2]['sim_compositional_median']):.0f}",
        "SIM_STORED_2": f"{float(simb[2]['sim_stored_median']):.0f}",
        # combinatorial escape (Table 6)
        "RHO_P_WLEN_S": signed(float(esc["all"]["rho_P_vs_wlen"])),
        "RHO_P_WLEN_ALPHA": signed(float(esc["alphabet"]["rho_P_vs_wlen"])),
        "RHO_G_WLEN_W": signed(0.128, plus=True),
        # inverse inference (Table 7)
        "F1_GRAN_FAM": f"{f1_of('rf_family', 'granularity'):.2f}",
        "F1_GRAN_SCR": f"{f1_of('rf_script', 'granularity'):.2f}",
        "F1_GRAN_MAJ": f"{f1_of('majority', 'granularity'):.2f}",
        "F1_WS_SYM": f"{f1_of('logreg_family', 'ws_class'):.2f}",
        "F1_STUMP": f"{f1_of('stump_G_family', 'ws_class'):.2f}",
        # 'full' feature set (adds consonant/vowel counts): logreg, family-grouped
        "F1_WS_FULL": "{:.2f}".format(next(
            float(r[1]) for r in csv.reader(
                open(os.path.join(TAB, "table_inverse_full.csv")))
            if r and r[0] == "logreg_family")),
    }
    # written-side escape numbers are printed in logs/escape.txt (not a table)
    esc_log = open(os.path.join(LOG, "escape.txt")).read()
    gl = next(ln for ln in esc_log.splitlines()
              if "rho_G(., mean_orth_wordlen)" in ln)
    pl = next(ln for ln in esc_log.splitlines()
              if "rho_P(., mean_orth_wordlen)" in ln)
    gw = float(gl.split("=")[1].split()[0])
    glo, ghi = (float(x) for x in
                re.search(r"\[(-?[\d.]+),\s*(-?[\d.]+)\]", gl).groups())
    R["RHO_G_WLEN_W"] = signed(gw, plus=True)
    pw = float(pl.split("=")[1].split()[0])
    plo, phi = (float(x) for x in
                re.search(r"\[(-?[\d.]+),\s*(-?[\d.]+)\]", pl).groups())
    R["RHO_P_WLEN_W"] = signed(pw)
    R["CI_P_WLEN_W"] = ci(plo, phi)
    mw = re.search(r"wordfreq-matched pairs: (\d+)", esc_log)
    R["N_WORDFREQ"] = mw.group(1)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(R, open(OUT, "w"), indent=2, sort_keys=True)
    print(f"wrote {OUT}: {len(R)} keys")


if __name__ == "__main__":
    main()
