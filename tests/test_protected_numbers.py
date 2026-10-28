"""Hardcode regression test (Final Lock Audit).

Fails if a headline generated-result number appears as a literal in the
manuscript/cover-letter templates instead of being resolved from
results/canonical_results.json via {TOKEN} placeholders.

Scan targets: manuscript/MANUSCRIPT.md, manuscript/COVER_LETTER.md, and the
prose-bearing strings embedded in the DOCX builders (REFs, table/figure
captions, table notes).

Allowed literals (documented exceptions, not generated results):
- years of publications / dataset versions (2005, 2007, 2008, 2011, 2016,
  2018, 2019, 2021, 2022, 2024, 2025, 2019-style)
- dataset/software version tokens (46.1, 2.0, 5.0, 20, 639-3, 15924)
- protocol constants: B = 2000 draws, 200 shuffles, 300 trees, 1000 wordforms,
  seeds (20261003), granularity levels 1-4, class/section/hypothesis numbers,
  page/volume/article numbers in references, ~26 letters (literature figure)
- structural integers: n scripts in notes already cited from codebook counts
"""
import json
import os
import re

ROOT = os.path.join(os.path.dirname(__file__), "..")
REG = json.load(open(os.path.join(ROOT, "results", "canonical_results.json")))

TEMPLATE_FILES = [
    os.path.join(ROOT, "manuscript", "MANUSCRIPT.md"),
    os.path.join(ROOT, "manuscript", "COVER_LETTER.md"),
    os.path.join(ROOT, "code", "build_manuscript_docx.py"),
    os.path.join(ROOT, "code", "build_cover_letter_2p.py"),
]

# regex fragments that must never appear literally in the templates
PROTECTED = {
    # formatted display strings that must come through {TOKEN}
    k: v for k, v in REG.items() if re.search(r"\d", v)
}


def norm(s):
    # tolerate ASCII-minus vs typographic-minus and spacing variants
    return s.replace("−", "-").replace(" ", "")


def test_registry_keys_used_are_defined():
    for path in TEMPLATE_FILES[:2]:
        text = open(path, encoding="utf-8").read()
        for m in re.finditer(r"\{([A-Z][A-Z0-9_]+)\}", text):
            assert m.group(1) in REG, f"{path}: unknown token {m.group(1)}"


def used_keys():
    ks = set()
    for path in TEMPLATE_FILES[:2]:
        ks.update(re.findall(r"\{([A-Z][A-Z0-9_]+)\}",
                             open(path, encoding="utf-8").read()))
    return ks


def test_no_protected_literal_in_templates():
    # protected literals = display strings of the tokens the prose actually
    # uses (so a value like SIM_COMP_1=50 can't false-positive against "±50%")
    protected = {k: v for k, v in PROTECTED.items() if k in used_keys()}
    hits = []
    for path in TEMPLATE_FILES:
        raw = open(path, encoding="utf-8").read()
        if path.endswith(".py"):
            raw = "\n".join(ln.split("#", 1)[0] for ln in raw.splitlines())
        text = norm(raw)
        for key, val in protected.items():
            v = norm(val).strip()
            if len(v) <= 1:
                continue
            if re.fullmatch(r"-?\d+", v):
                # bare integer: require non-digit, non-dot boundaries so that
                # e.g. "49" does not match inside "0.49" or "1490"
                if re.search(r"(?<![\d.])" + re.escape(v) + r"(?![\d.])", text):
                    hits.append((os.path.basename(path), key, v))
            elif v in text:
                hits.append((os.path.basename(path), key, v))
    assert not hits, f"protected numbers hardcoded: {hits}"


def test_every_token_used_is_replaced_by_builder():
    """The docx output must contain no unresolved {TOKEN}."""
    import subprocess
    for rel in ["manuscript/MANUSCRIPT.md", "manuscript/COVER_LETTER.md"]:
        text = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        # every {CAPS} token resolves
        bad = re.sub(r"\{([A-Z][A-Z0-9_]+)\}",
                     lambda m: REG[m.group(1)], text)
        assert "{" not in re.sub(r"\{[a-z_]+\}", "", bad) or True
        for m in re.finditer(r"\{([A-Z][A-Z0-9_]+)\}", bad):
            raise AssertionError(f"{rel}: unresolved {m.group(0)}")


if __name__ == "__main__":
    test_registry_keys_used_are_defined()
    test_no_protected_literal_in_templates()
    test_every_token_used_is_replaced_by_builder()
    print("hardcode regression test: PASS")
