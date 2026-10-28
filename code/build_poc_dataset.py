"""Build the POC linked dataset: language x writing-system pairs.

Unit of analysis: (language, default script) pair.
  P  = phoneme inventory size (PHOIBLE, largest inventory per language)
  G  = grapheme inventory size (CLDR exemplarCharacters, core set)
  ws_class / granularity from code/script_type_codebook.csv
  family / macroarea from Glottolog

Outputs:
  data_processed/poc_dataset.csv
  data_processed/poc_dataset_summary.md
"""
import csv
import os
import re
import xml.etree.ElementTree as ET

import pandas as pd
import pycountry

ROOT = os.path.join(os.path.dirname(__file__), "..")
RAW = os.path.join(ROOT, "data_raw")
PROC = os.path.join(ROOT, "data_processed")
CODEBOOK = os.path.join(os.path.dirname(__file__), "script_type_codebook.csv")

BRACE = re.compile(r"\{[^}]*\}|[^\s{}\[\]]+")


def parse_exemplar(s):
    """Count graphemes in a CLDR exemplarCharacters bracket list.
    Multigraphs appear as {ch}; ranges like [a-z] appear literally."""
    if not isinstance(s, str):
        return None, None
    inner = s.strip().strip("[]")
    tokens = BRACE.findall(inner)
    toks = []
    for t in tokens:
        t = t.strip("{}")
        if "-" in t and len(t) == 3 and t[1] == "-":  # range like a-z
            toks.extend(chr(c) for c in range(ord(t[0]), ord(t[2]) + 1))
        elif t:
            toks.append(t)
    return len(toks), toks


# BCP47 language subtag -> ISO 639-3 macrolanguage fallbacks where
# PHOIBLE inventories the individual language code, not the macro.
MACRO_TO_PHOIBLE = {
    "zh": "cmn",   # Chinese macro -> Mandarin
    "no": "nob",   # Norwegian macro -> Bokmal
    "ms": "zsm",   # Malay macro -> Standard Malay
    "fa": "pes",   # Persian macro -> Iranian Persian
    "sq": "als",   # Albanian macro -> Tosk
    "ku": "ckb",   # Kurdish macro -> Central Kurdish (approx; flagged)
    "lv": "lvs",   # Latvian macro -> Standard Latvian
    "sw": "swh",   # Swahili macro -> Swahili (individual)
    "uz": "uzn",   # Uzbek macro -> Northern Uzbek
    "az": "azj",   # Azerbaijani macro -> North Azerbaijani
    "kk": "kaz",
    "ky": "kir",
    "tg": "tgk",
    "bs": "bos",
    "hr": "hrv",
    "sr": "srp",
    "mn": "khk",   # Mongolian macro -> Khalkha
}


def lang_alpha3(subtag, phoible_isos=frozenset()):
    """Map BCP47 language subtag -> ISO 639-3, preferring codes PHOIBLE uses."""
    subtag = subtag.lower()
    if len(subtag) == 3 and subtag in phoible_isos:
        return subtag
    alpha3 = None
    if len(subtag) == 2:
        # strict alpha-2 attribute match only; languages.lookup() also fuzzy-
        # matches names ('ko' -> 'Ko' (fuj)) which corrupts joins
        for l in pycountry.languages:
            if getattr(l, "alpha_2", None) == subtag:
                alpha3 = getattr(l, "alpha_3", None)
                break
    else:
        alpha3 = subtag
    if alpha3 not in phoible_isos and subtag in MACRO_TO_PHOIBLE:
        alt = MACRO_TO_PHOIBLE[subtag]
        if alt in phoible_isos:
            return alt
    return alpha3


def main():
    # ---- CLDR exemplar inventories ----
    main_dir = os.path.join(RAW, "cldr", "package", "main")
    if not os.path.isdir(main_dir):
        import tarfile
        tgz = os.path.join(RAW, "cldr-misc-full.tgz")
        with tarfile.open(tgz) as t:
            t.extractall(os.path.join(RAW, "cldr"))
    rows = []
    for loc in sorted(os.listdir(main_dir)):
        p = os.path.join(main_dir, loc, "characters.json")
        if not os.path.exists(p):
            continue
        import json
        d = json.load(open(p))
        chars = d["main"][loc]["characters"]
        n_core, toks = parse_exemplar(chars.get("exemplarCharacters", ""))
        n_aux, _ = parse_exemplar(chars.get("auxiliary", ""))
        rows.append({"locale": loc, "g_core": n_core, "g_aux": n_aux or 0})
    cldr = pd.DataFrame(rows)

    # ---- likelySubtags: language -> default script ----
    tree = ET.parse(os.path.join(RAW, "cldr", "likelySubtags.xml"))
    lang2script = {}
    for el in tree.getroot().find("likelySubtags"):
        frm, to = el.get("from"), el.get("to")
        if frm is None:
            continue
        parts = frm.split("_")
        if len(parts) == 1:
            m = re.search(r"_([A-Z][a-z]{3})_", to + "_")
            script = m.group(1) if m else None
            lang2script.setdefault(parts[0].lower(), script)
    # also explicit script in locale tag wins
    cldr["lang_tag"] = cldr["locale"].str.split("-").str[0].str.lower()
    cldr["script_tag"] = cldr["locale"].str.split("-").apply(
        lambda p: next((x for x in p if re.fullmatch(r"[A-Z][a-z]{3}", x)), None))
    cldr["script"] = cldr.apply(
        lambda r: r["script_tag"] or lang2script.get(r["lang_tag"]), axis=1)
    # ---- PHOIBLE: largest inventory per language ----
    ph = pd.read_csv(os.path.join(RAW, "phoible", "phoible.csv"), low_memory=False)
    phoible_isos = set(ph["ISO6393"].dropna().unique())
    cldr["iso3"] = cldr["lang_tag"].apply(lambda t: lang_alpha3(t, phoible_isos))
    seg = ph[ph["SegmentClass"].isin(["consonant", "vowel", "tone"])]
    inv = (seg.groupby(["InventoryID", "ISO6393", "Glottocode", "Source"])
              .agg(P=("Phoneme", "nunique"),
                   n_cons=("SegmentClass", lambda s: (s == "consonant").sum()),
                   n_vow=("SegmentClass", lambda s: (s == "vowel").sum()),
                   n_tone=("SegmentClass", lambda s: (s == "tone").sum()))
              .reset_index())
    # keep the inventory with maximum P per ISO6393 (documented choice)
    inv = inv.sort_values("P").groupby("ISO6393", as_index=False).last()

    # ---- Glottolog family/macroarea ----
    gl = pd.read_csv(os.path.join(RAW, "glottolog", "languoid.csv"))
    lang_rows = gl[gl["Level"] == "language"].copy()
    fam = gl[gl["Level"] == "family"][["Glottocode", "Name"]].rename(
        columns={"Glottocode": "Family_ID", "Name": "family"})
    lang_rows = lang_rows.merge(fam, on="Family_ID", how="left")
    lang_rows = lang_rows[["ISO639P3code", "Glottocode", "Name", "Macroarea", "family", "Is_Isolate"]]
    lang_rows.columns = ["iso3", "glottocode", "language", "macroarea", "family", "is_isolate"]

    # ---- merge ----
    df = (cldr.merge(inv[["ISO6393", "P", "n_cons", "n_vow", "n_tone", "Source"]],
                     left_on="iso3", right_on="ISO6393", how="left")
              .merge(lang_rows, on="iso3", how="left"))
    df = df[df["g_core"].notna() & df["script"].notna()]

    cb = pd.read_csv(CODEBOOK)
    df = df.merge(cb[["script_code", "ws_class", "encoded_unit", "granularity"]],
                  left_on="script", right_on="script_code", how="left")

    # ---- curated supplement: under-represented architecture classes ----
    cur = pd.read_csv(os.path.join(os.path.dirname(__file__), "curated_pairs.csv"))
    cur = cur.merge(inv[["ISO6393", "P", "n_cons", "n_vow", "n_tone", "Source"]],
                    left_on="iso3", right_on="ISO6393", how="left")
    cur = cur.merge(lang_rows, on="iso3", how="left")
    cur["g_core"] = cur["G"]
    cur["g_aux"] = 0
    cur["script_tag"] = cur["script"]
    cur["script_code"] = cur["script"]
    cur["lang_tag"] = cur["locale"].str.split("-").str[0]
    df = pd.concat([df, cur], ignore_index=True, sort=False)
    df["P_total"] = df["P"]
    df["G"] = df["g_core"]
    df["GP_ratio"] = df["G"] / df["P_total"]

    out = df[["locale", "iso3", "glottocode", "language", "family", "macroarea",
              "script", "ws_class", "encoded_unit", "granularity",
              "G", "g_aux", "P_total", "n_cons", "n_vow", "n_tone",
              "Source", "GP_ratio", "is_isolate"]]
    out.to_csv(os.path.join(PROC, "poc_dataset.csv"), index=False)

    summ = []
    summ.append(f"locales with exemplar data: {len(cldr)}")
    summ.append(f"rows with script resolved: {len(df)}")
    summ.append(f"rows with PHOIBLE P matched: {df['P_total'].notna().sum()}")
    summ.append(f"rows with glottolog match: {df['glottocode'].notna().sum()}")
    summ.append(f"rows with ws_class: {df['ws_class'].notna().sum()}")
    summ.append("\nby ws_class:")
    summ.append(df.groupby("ws_class").agg(
        n=("locale", "count"), G_med=("G", "median"),
        P_med=("P_total", "median"), GP_med=("GP_ratio", "median")).to_string())
    summ.append("\nunclassified scripts:")
    summ.append(", ".join(sorted(df[df["ws_class"].isna()]["script"].unique())))
    with open(os.path.join(PROC, "poc_dataset_summary.md"), "w") as f:
        f.write("\n".join(str(x) for x in summ))
    print("\n".join(str(x) for x in summ))


if __name__ == "__main__":
    main()
