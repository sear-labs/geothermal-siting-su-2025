"""Smoke tests for geothermal-siting-su-2025.

Adapted from sear-labs/code-standard templates/tests/test_smoke.py.

No CoolProp and no notebook execution: CI installs pandas only. These check
the committed GIS inputs, the committed results (written by scripts/run_all.py),
and that both still say what the paper printed.

Watch it fail
-------------
    pytest -q                                                  # green
    <in results/tables/table5_facilities.csv, change 7696 to 7697>
    pytest -q -k table5                                        # MUST go red
    git checkout -- results/tables/table5_facilities.csv
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
GIS = ROOT / "data" / "raw" / "gis_class_summary.csv"
TABLES = ROOT / "results" / "tables"
NOTEBOOK = ROOT / "notebooks" / "geothermal_calcs.ipynb"

# ---- the paper, as printed (Sustainability 17(6) 2558) ----------------------
# Table 3: total, HUBZone, tribal area (sq mi); oil wells: all, in HUBZones, in tribal communities
PAPER_TABLE_3 = {
    "Class 1": (32050, 10090, 1838, 20, 1, 0),
    "Class 2": (144141, 38776, 10832, 2200, 201, 22),
    "Class 3": (196118, 74051, 48026, 12000, 5964, 5752),
    "Class 4": (221513, 22641, 18729, 2000, 334, 290),
    "Class 5 and 999": (236160, 31320, 18845, 2300, 663, 370),
}
PAPER_TABLE_3_TOTAL = (829982, 176878, 98270, 18520, 7163, 6434)
# Table 4 (GW, one decimal): total, HUBZones, tribal, oil wells, oil wells in HUBZones, on tribal lands
PAPER_TABLE_4 = {
    "Class 1": (339.3, 106.8, 19.4, 0.0, 0.0, 0.0),
    "Class 2": (1002.6, 269.7, 75.3, 0.7, 0.1, 0.0),
    "Class 3": (1031.0, 389.3, 252.5, 3.5, 1.8, 1.7),
    "Total": (2372.8, 765.8, 347.2, 4.3, 1.8, 1.7),
}
# Table 5: max facilities total, HUBZones, tribal; average plant capacity (MW)
PAPER_TABLE_5 = {
    "Class 1": (7696, 2423, 441, 44.08),
    "Class 2": (34613, 9311, 2601, 28.97),
    "Class 3": (47095, 17782, 11532, 21.89),
    "Total": (89404, 29516, 14574, 94.94),
}
# Table 2 "This Study": R134a at 164 degF (73 C), 12 kg/s, 9% efficiency -> 249 kW gross.
PAPER_TABLE_2_KW = 249


def _gis() -> pd.DataFrame:
    return pd.read_csv(GIS).set_index("class")


def _t(name: str) -> pd.DataFrame:
    return pd.read_csv(TABLES / name).set_index("Class")


# ------------------------------------------------------------------ inputs
def test_gis_inputs_match_paper_table_3():
    g = _gis()
    assert list(g.index) == list(PAPER_TABLE_3)
    for cls, row in PAPER_TABLE_3.items():
        assert tuple(g.loc[cls]) == row, cls
    assert tuple(g.sum()) == PAPER_TABLE_3_TOTAL


def test_gis_inputs_match_the_notebook():
    """The notebook types the GIS results in; data/raw records them. They must agree."""
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    code = "\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code")
    live = code[code.index("GIS_data = {\n    \"Class\": [\"Class 1\"", code.rindex("# Creating the DataFrame")):]
    block = live[: live.index("}") + 1]
    nums = {k: [int(x) for x in re.findall(r"\d+", v)] for k, v in re.findall(r'"([^"]+)": \[([^\]]+)\]', block) if k != "Class"}
    g = _gis()
    assert nums["Total Potential (sq. miles)"] == list(g["total_area_sq_mi"])
    assert nums["Hub Zones (sq. miles)"] == list(g["hubzone_area_sq_mi"])
    assert nums["Tribal Lands (sq. miles)"] == list(g["tribal_area_sq_mi"])
    assert nums["Oil Wells Count"] == list(g["oil_wells"])


def test_subsets_never_exceed_their_whole():
    g = _gis()
    assert (g["hubzone_area_sq_mi"] <= g["total_area_sq_mi"]).all()
    assert (g["tribal_area_sq_mi"] <= g["total_area_sq_mi"]).all()
    assert (g["oil_wells_in_hubzones"] <= g["oil_wells"]).all()
    assert (g["oil_wells_in_tribal_communities"] <= g["oil_wells"]).all()


# ------------------------------------------------------------------ results
def test_table4_matches_the_paper():
    t = _t("table4_capacity_gw.csv")
    cols = ["Total Potential (GW)", "Hub Zones (GW)", "Tribal Lands (GW)",
            "Oil Wells (GW)", "Oil Wells (GW) in Hub Zones", "Oil Wells (GW) on Tribal Lands"]
    for cls, row in PAPER_TABLE_4.items():
        got = tuple(round(float(t.loc[cls, c]), 1) for c in cols)
        assert got == row, f"{cls}: {got} vs paper {row}"


def test_table5_matches_the_paper():
    t = _t("table5_facilities.csv")
    for cls, (tot, hub, tri, mw) in PAPER_TABLE_5.items():
        r = t.loc[cls]
        assert (int(r.iloc[0]), int(r.iloc[1]), int(r.iloc[2])) == (tot, hub, tri), cls
        assert round(float(r.iloc[3]), 2) == mw, cls


def test_table5_total_row_sums_the_class_averages():
    """KNOWN ISSUE, pinned. The 'Total' average plant capacity (94.94 MW) is the SUM of
    the three class averages, not an average. The capacity-weighted average is
    total GW / total facilities, about 26.5 MW. Published as printed; not corrected."""
    t = _t("table5_facilities.csv")
    classes = t.drop(index="Total")
    assert float(t.loc["Total"].iloc[3]) == pytest.approx(classes.iloc[:, 3].astype(float).sum(), abs=0.011)
    weighted = _t("table4_capacity_gw.csv").loc["Total", "Total Potential (GW)"] * 1000 / t.loc["Total"].iloc[0]
    assert weighted == pytest.approx(26.5, abs=0.1)


def test_table2_this_study_power():
    """Class 5 (73 C) is the paper's calibration case. 249.93 kW, printed as 249 (truncated)."""
    w = _t("per_well_power.csv")
    kw = float(w.loc["Class 5", "Power Output per Well (kW)"])
    assert int(kw) == PAPER_TABLE_2_KW
    assert float(w.loc["Class 5", "Bottom Temperature (°C)"]) == 73


def test_per_well_physics():
    w = _t("per_well_power.csv")
    assert (w["Specific Enthalpy Inlet (kJ/kg)"] > w["Specific Enthalpy Outlet (kJ/kg)"]).all()
    kw = w["Power Output per Well (kW)"]
    assert kw.is_monotonic_decreasing, "hotter class must give more power per well"
    assert (kw > 0).all()
    # P = m * dh * eta with the paper's m = 12 kg/s and eta = 0.09
    dh = w["Specific Enthalpy Inlet (kJ/kg)"] - w["Specific Enthalpy Outlet (kJ/kg)"]
    assert (kw - 12 * dh * 0.09).abs().max() < 1e-9


def test_facility_counts_fit_the_land():
    """Facilities x footprint (10 km2 + 500 m buffer) cannot exceed the class's area."""
    import math
    per_facility_sq_mi = 10 / 2.59 + math.pi * (500 / 1609.34) ** 2
    t = _t("table5_facilities.csv").drop(index="Total")
    g = _gis()
    for cls in t.index:
        assert t.loc[cls].iloc[0] * per_facility_sq_mi <= g.loc[cls, "total_area_sq_mi"], cls
        assert t.loc[cls].iloc[1] * per_facility_sq_mi <= g.loc[cls, "hubzone_area_sq_mi"], cls
        assert t.loc[cls].iloc[2] * per_facility_sq_mi <= g.loc[cls, "tribal_area_sq_mi"], cls


# ------------------------------------------------------------------ hygiene
def test_notebook_reads_nothing_from_outside():
    text = NOTEBOOK.read_text(encoding="utf-8")
    assert not re.search(r"drive\.mount|/content/|/Users/|[A-Z]:\\\\", text)
    assert not re.search(r"(?i)(api[_-]?key|token|password)\s*=", text)
