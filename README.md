# Bookkeeping backup

The bookkeeping backup contains backup version of paneled knowledge data (knowledge reference sheets) structured and built as spreadsheet. 

Spreadsheets are maintained using a script that converts from Excel files to CSV files incrementally, which stays in sync with development tools.

---

# excel2csv incremental

A Python script that recursively converts Excel files into CSV files while avoiding redundant work using incremental updates.

The script mirrors the source directory structure in the destination directory and only reprocesses files that have changed.

---

## Platform Support

* Windows (tested)
* Linux (not tested)
* macOS (not tested)

The script is platform-independent in principle, but only verified on Windows.

---

## 📦 Dependencies

Install required Python packages:

```bash
pip install pandas openpyxl
```

---

## Usage

```bash
python excel2csv.py "<source_directory>" "<destination_directory>"
```

### Example

```bash
python excel2csv.py "C:\Users\mowan\OneDrive - KTH\Data convergence" "C:\Users\mowan\source\repos\Bookkeeping_backup\Bookkeeping"
```

---

## Behavior

### Recursive Processing

* Traverses the source directory recursively
* Finds all Excel files (`.xlsx`, `.xls`, `.xlsm`)
* Converts each Excel file into a folder of CSV files (one per sheet)

### Output Structure

The destination directory mirrors the source structure:

```
source/
  file.xlsx
  sub/
    data.xlsx

destination/
  file/
    Sheet1.csv
  sub/
    data/
      Sheet1.csv
```

---

## Incremental Conversion

The script avoids reprocessing unchanged files by storing metadata in:

```
.excel2csv
```

This file contains modification timestamps of processed Excel files.

### Rules:

* If `.excel2csv` is missing → **process everything**
* If a file is missing in the metadata → **process it**
* If a file's modification time changed → **process it**
* Otherwise → **skip it**

---

## Important Notes

### Do NOT edit `.excel2csv`

* MODIFYING IT MAY CAUSE MISSING OR INCORRECT PROCESSING
* IF ANYTHING GOES WRONG, **DELETE IT INSTEAD**

```bash
del .excel2csv
```

This forces a full rebuild safely.

---

### Folder Optimization

* The script implicitly skips unchanged folders by skipping all files inside them
* No explicit folder timestamp tracking is used (more reliable across platforms)

---

### File Locking (Windows)

* Excel files must be closed before running the script
* Open files may cause conversion errors

---

## Typical Workflow

1. Add or modify Excel files
2. Run the script
3. Only changed files are reprocessed

---

## Limitations

* No automatic deletion of CSVs if source Excel files are removed
* No parallel processing (yet)
* Relies on file modification timestamps (not content hashing)

---

## Future Improvements (optional)

* Parallel processing for faster conversion
* Sync deletion (remove CSVs when Excel files are deleted)
* Hash-based change detection
* CLI flags (`--force`, `--clean`, etc.)

---

## License

Use freely. Modify as needed.
