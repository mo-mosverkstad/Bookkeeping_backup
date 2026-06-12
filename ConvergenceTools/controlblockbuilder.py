import json
import re
import sys
from pathlib import Path


def to_snake_case(filename: str) -> str:
    name = Path(filename).stem.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    return name.strip("_")


def generate_control_json(data_dir: Path):
    if not data_dir.exists():
        raise FileNotFoundError(f"Directory does not exist: {data_dir}")

    if not data_dir.is_dir():
        raise NotADirectoryError(f"Not a directory: {data_dir}")

    entries = []

    for csv_file in sorted(data_dir.glob("*.csv")):
        entries.append({
            "id": to_snake_case(csv_file.name),
            "view": "table",
            "file": csv_file.name
        })

    output = {
        "version": "1.0",
        "entries": entries
    }

    output_file = data_dir / "control.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Created {output_file}")
    print(f"Found {len(entries)} CSV files")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {Path(sys.argv[0]).name} <csv_directory>")
        sys.exit(1)

    generate_control_json(Path(sys.argv[1]))