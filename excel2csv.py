import os
import json
import shutil
from pathlib import Path
import pandas as pd
from tempfile import NamedTemporaryFile

EXCEL_EXTENSIONS = {".xlsx", ".xls", ".xlsm"}


def load_metadata(meta_path):
    if not meta_path.exists():
        return {}
    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # Corrupted → safer to ignore
        return {}


def atomic_write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", delete=False, dir=path.parent, encoding="utf-8") as tmp:
        json.dump(data, tmp, indent=2)
        temp_name = tmp.name
    os.replace(temp_name, path)


def is_excel(file_path):
    return file_path.suffix.lower() in EXCEL_EXTENSIONS


def convert_excel_to_csvs(src_file, dst_folder):
    try:
        xls = pd.ExcelFile(src_file)
        for sheet_name in xls.sheet_names:
            df = xls.parse(sheet_name)
            safe_sheet = sheet_name.replace("/", "_").replace("\\", "_")
            out_file = dst_folder / f"{safe_sheet}.csv"
            df.to_csv(out_file, index=False)
    except Exception as e:
        print(f"[ERROR] Failed to convert {src_file}: {e}")


def process_directory(src_dir, dst_dir):
    src_dir = Path(src_dir)
    dst_dir = Path(dst_dir)

    meta_path = src_dir / ".excel2csv"
    old_meta = load_metadata(meta_path)
    new_meta = {}

    any_change = False

    for root, dirs, files in os.walk(src_dir):
        root = Path(root)

        # Skip metadata file
        files = [f for f in files if f != ".excel2csv"]

        rel_root = root.relative_to(src_dir)
        dst_root = dst_dir / rel_root

        folder_changed = False

        for file in files:
            src_file = root / file

            if not is_excel(src_file):
                continue

            rel_path = str(src_file.relative_to(src_dir))
            mtime = os.path.getmtime(src_file)

            new_meta[rel_path] = mtime

            if rel_path not in old_meta or old_meta[rel_path] != mtime:
                # Needs processing
                print(f"[PROCESS] {rel_path}")

                out_folder = dst_root / src_file.stem

                if out_folder.exists():
                    shutil.rmtree(out_folder)

                out_folder.mkdir(parents=True, exist_ok=True)
                convert_excel_to_csvs(src_file, out_folder)

                any_change = True
                folder_changed = True
            else:
                print(f"[SKIP] {rel_path}")

        # Optional pruning: if folder unchanged and no new files
        # (simple heuristic: if no file changed, we don't touch destination)

    # Save metadata (only if something changed OR file missing)
    if any_change or not meta_path.exists():
        atomic_write_json(meta_path, new_meta)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Excel to CSV incremental converter")
    parser.add_argument("src", help="Source directory")
    parser.add_argument("dst", help="Destination directory")

    args = parser.parse_args()

    process_directory(args.src, args.dst)