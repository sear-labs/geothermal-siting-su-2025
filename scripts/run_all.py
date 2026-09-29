"""Re-run the paper's calculations and write its tables.

    python scripts/run_all.py

Executes notebooks/geothermal_calcs.ipynb in results/runs/ (the committed
notebook is not modified). One cell is appended to the in-memory copy only, to
export the DataFrames the notebook already builds:

    results/tables/per_well_power.csv      Section 3.5.1; Table 2 "This Study"
    results/tables/table4_capacity_gw.csv  Table 4
    results/tables/table5_facilities.csv   Table 5

The GIS step (ArcGIS Pro / Online) is not re-run; its per-class results are
typed into the notebook and recorded in data/raw/gis_class_summary.csv.
"""
from __future__ import annotations

import sys
from pathlib import Path

import nbformat
import yaml
from nbclient.exceptions import CellExecutionError, CellTimeoutError
from nbconvert.preprocessors import ExecutePreprocessor

ROOT = Path(__file__).resolve().parents[1]

EXPORT = '''
from pathlib import Path as _P
_out = _P(r"{tables}")
geothermal_well_df.to_csv(_out / "per_well_power.csv", index=False)
final_df_sumadded.to_csv(_out / "table4_capacity_gw.csv", index=False)
final_df_for_table.to_csv(_out / "table5_facilities.csv", index=False)
'''


def main() -> int:
    cfg = yaml.safe_load((ROOT / "config.yaml").read_text())
    nb_path = ROOT / cfg["notebook"]
    work = ROOT / cfg["run_dir"]
    tables = ROOT / cfg["tables_dir"]
    work.mkdir(parents=True, exist_ok=True)
    tables.mkdir(parents=True, exist_ok=True)
    nb = nbformat.read(nb_path, as_version=4)
    nb.cells.append(nbformat.v4.new_code_cell(EXPORT.format(tables=tables)))
    try:
        ExecutePreprocessor(timeout=cfg["cell_timeout_s"]).preprocess(nb, {"metadata": {"path": str(work)}})
    except (CellExecutionError, CellTimeoutError) as exc:
        print(f"FAIL  {nb_path.name}: {str(exc).strip().splitlines()[-1][:200]}")
        return 1
    finally:
        nbformat.write(nb, work / nb_path.name)
    for f in ("per_well_power.csv", "table4_capacity_gw.csv", "table5_facilities.csv"):
        print(f"ok    results/tables/{f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
