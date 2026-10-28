"""Download raw datasets for the channel-constraints writing-system study.

Saves originals under data_raw/ and appends machine-readable acquisition
records to data_raw/ACQUISITION_LEDGER.csv (never overwrites: skipped if the
file already exists with identical sha256).
"""
import csv
import hashlib
import io
import os
import urllib.request
from datetime import datetime, timezone

RAW = os.path.join(os.path.dirname(__file__), "..", "data_raw")
LEDGER = os.path.join(RAW, "ACQUISITION_LEDGER.csv")

SOURCES = [
    {
        "dataset": "PHOIBLE",
        "url": "https://raw.githubusercontent.com/phoible/dev/master/data/phoible.csv",
        "dest": "phoible/phoible.csv",
        "license": "CC BY-SA 4.0 (data); see phoible.org",
        "citation": "Moran, S. & McCloy, D. (eds.) 2019. PHOIBLE 2.0. Jena: MPI-SHH.",
        "variables": "phoneme segments per inventory; glottocode; iso6393; segment class; features",
        "unit": "phoneme record per language inventory",
    },
    {
        "dataset": "Glottolog languoid (via zenodo 5.0)",
        "url": "https://raw.githubusercontent.com/glottolog/glottolog-cldf/master/cldf/languages.csv",
        "dest": "glottolog/languoid.csv",
        "license": "CC BY 4.0",
        "citation": "Hammarstrom et al. Glottolog 5.0 (2024)",
        "variables": "glottocode; name; family; macroarea; iso6393",
        "unit": "languoid",
    },
    {
        "dataset": "CLDR likelySubtags",
        "url": "https://raw.githubusercontent.com/unicode-org/cldr/release-46-1/common/supplemental/likelySubtags.xml",
        "dest": "cldr/likelySubtags.xml",
        "license": "Unicode-DFS-2016",
        "citation": "Unicode CLDR 46.1",
        "variables": "default script/region per language tag",
        "unit": "language tag",
    },
    {
        "dataset": "Kim et al. OSF script data (Miton & Morin lab)",
        "url": "https://files.de-1.osf.io/v1/resources/ewp68/providers/osfstorage/6677fe16993d150361049ad0",
        "dest": "miton_morin_osf/all-script-data.csv",
        "license": "CC0/CC-BY (see OSF License.txt)",
        "citation": "Kim, Allassonniere-Tang, Miton & Morin. The phonology of letter shapes (2025)",
        "variables": "script name; unicode codepoints; script family; type",
        "unit": "script",
    },
]

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    os.makedirs(RAW, exist_ok=True)
    rows = []
    for s in SOURCES:
        dest = os.path.join(RAW, s["dest"])
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        status = "downloaded"
        if os.path.exists(dest):
            status = "exists_kept"
        else:
            try:
                with urllib.request.urlopen(s["url"], timeout=120) as r:
                    data = r.read()
                with open(dest, "wb") as f:
                    f.write(data)
            except Exception as e:
                status = f"FAILED: {e}"
        row = {
            "dataset": s["dataset"],
            "url": s["url"],
            "dest": s["dest"],
            "accessed_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "license": s["license"],
            "citation": s["citation"],
            "variables": s["variables"],
            "unit": s["unit"],
            "size_bytes": os.path.getsize(dest) if os.path.exists(dest) else "",
            "sha256": sha256(dest) if os.path.exists(dest) else "",
            "status": status,
        }
        rows.append(row)
        print(status, s["dest"], row["size_bytes"])
    new = not os.path.exists(LEDGER)
    with open(LEDGER, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        if new:
            w.writeheader()
        w.writerows(rows)

if __name__ == "__main__":
    main()
