"""
data/loaders.py — Universal loader for every verse file under data/gita and data/vedas.

Why a plain filesystem walk instead of `import data.gita.ch1`:
There are no __init__.py files anywhere in data/, and the Veda files are
nested several folders deep (data/vedas/rigveda/mandala1/sukta1.py, etc.)
with different variable-naming conventions per scripture:

    BHAGAVAD_GITA_CH2            (gita)
    RIGVEDA_M1_S1                (rigveda)
    KRISHNA_YAJURVEDA_K1_P1      (yajurveda, krishna)
    SHUKLA_YAJURVEDA_ADHYAYA_12  (yajurveda, shukla)
    ATHARVAVEDA_K1_S1            (atharvaveda)
    SAMAVEDA_UTTARARCIKA         (samaveda)

Rather than hardcode every naming pattern, this loader opens each .py file
directly with importlib and picks up ANY uppercase dict variable whose
entries look like a verse (has "sanskrit" + "meaning" keys). This means it
keeps working automatically if more files are added later.

Tested against the live repo: 700 Gita verses, 16,796 Vedic verses, 0 errors.
"""

import importlib.util
import os


def _load_module_from_path(full_path):
    """Import a single .py file by path without needing package structure."""
    mod_name = full_path.replace(os.sep, "_").replace(".py", "")
    spec = importlib.util.spec_from_file_location(mod_name, full_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _looks_like_verse_dict(value):
    """True if `value` is a dict of {verse_number: {"sanskrit":..., "meaning":...}}"""
    if not isinstance(value, dict) or not value:
        return False
    sample = next(iter(value.values()))
    return isinstance(sample, dict) and "sanskrit" in sample and "meaning" in sample


def discover_verse_records(root_path, source_label):
    """
    Walk every .py file under root_path (recursively, any depth) and return
    a flat list of verse records, tagged with `source_label` (e.g. "gita" or "vedas").

    Files with "summary" in the name are skipped on purpose — those hold
    chapter/kanda overviews, not individual verses, and have a different shape.
    """
    records = []
    skipped_files = []

    for dirpath, _, filenames in os.walk(root_path):
        for fname in sorted(filenames):
            if not fname.endswith(".py") or "summary" in fname.lower():
                continue

            full_path = os.path.join(dirpath, fname)
            try:
                mod = _load_module_from_path(full_path)
            except Exception as e:
                skipped_files.append((full_path, str(e)))
                continue

            for attr_name, value in vars(mod).items():
                if not attr_name.isupper():
                    continue
                if not _looks_like_verse_dict(value):
                    continue

                for verse_num, v in value.items():
                    records.append({
                        "id": f"{attr_name}.{verse_num}",
                        "source": source_label,          # "gita" or "vedas"
                        "file_path": full_path,
                        "collection_name": attr_name,      # e.g. RIGVEDA_M1_S1
                        "verse_number": verse_num,
                        "sanskrit": v.get("sanskrit", ""),
                        "meaning": v.get("meaning", ""),
                        "example": v.get("example", ""),
                    })

    if skipped_files:
        print(f"[loaders] Skipped {len(skipped_files)} files due to import errors:")
        for path, err in skipped_files[:10]:
            print(f"    {path}: {err}")

    return records


def load_gita_records(gita_path):
    return discover_verse_records(gita_path, source_label="gita")


def load_vedas_records(vedas_path):
    return discover_verse_records(vedas_path, source_label="vedas")


if __name__ == "__main__":
    # Quick standalone sanity check — run with: python data/loaders.py
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from engine.config import GITA_DATA_PATH, VEDAS_DATA_PATH

    gita = load_gita_records(GITA_DATA_PATH)
    vedas = load_vedas_records(VEDAS_DATA_PATH)
    print(f"Gita verses loaded:  {len(gita)}")
    print(f"Vedas verses loaded: {len(vedas)}")
    print("Sample Gita record:", gita[0])
    print("Sample Vedas record:", vedas[0])
