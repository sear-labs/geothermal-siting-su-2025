# geothermal-siting-su-2025 conventions

The portable standard governs this repo. Read it before working here:
  https://github.com/sear-labs/code-standard    canonical - the same from any machine
  a local clone, if you have one                faster

# Part 11 - This project specifically

**Archetype A**, as a published artifact behind Jones, Munjurpet Sridharan, Aghapour &
Rodriguez (2025), Sustainability 17(6), 2558, doi:10.3390/su17062558 (CC BY). Name: route 1,
MDPI's alphabetic DOI stem `su`. Jones is first and corresponding author.

## Four axes (Part 2c)

- Sensitivity: may reach a public host. data/raw/ is the authors' own per-class GIS
  summary (published as Table 3); no shapefiles or licensed layers are held here.
  Public is the owner's decision (Jones).
- Activity: finished work, so git for the record.
- Syncing folder: no. Drive sources: Projects/GeoThermal/ (and an identical copy in
  PhD_Research_Organized/07_GeoThermal/). Reviewer documents and reference PDFs stay there.
- Writers: one (Aghapour).

## The pipeline

    1 GIS suitability analysis          NOT HERE - ArcGIS Pro / Online (point-and-click);
                                        layers published at https://arcg.is/0OWujj
    2 per-class areas and well counts   data/raw/gis_class_summary.csv  (= paper Table 3)
    3 per-well ORC power (CoolProp)     notebooks/geothermal_calcs.ipynb -> per_well_power.csv
    4 EGS capacity and facility counts  same notebook -> table4_capacity_gw.csv, table5_facilities.csv

scripts/run_all.py runs 3-4. It appends one export cell to the in-memory copy only.

## Deliberate exemptions

- **Rule 2:** parameters (12 kg/s, 9% efficiency, class temperatures, 10 km2 + 500 m
  footprint, power-density formula) and the GIS numbers are hardcoded in the notebook, as
  published. data/raw/ records the GIS numbers and a test keeps the two identical.
- **No src/, no figures:** one notebook; the paper's maps come from ArcGIS, not from code.

## Known defects and facts

- **README "Known issues in the published paper" is the record of the paper's errata** (19
  items, 2026-10-01, reviewed by Jones). Not sent to the journal, by Jones's decision. Read it
  before changing any number here; `results/tables/` stays as published.
- **The ArcGIS Online orphaned-well layer the analysis used now needs a sign-in.** A recount from
  the public USGS release (doi:10.5066/P91PJETI) with this paper's polygon layers matched 5 of the
  10 exact subset counts (Classes 1, 2, 4), not Classes 3 and 5: a different data version. Exact
  per-class totals need the original ArcGIS project.
- **Tables 4 and 5 reproduce the paper exactly**; Table 3 equals the notebook's inputs.
- **Table 5 "Total" average plant capacity (94.94 MW) is a sum of the three class averages**,
  not an average; the capacity-weighted value is ~26.5 MW. Published as printed; pinned in
  test_table5_total_row_sums_the_class_averages.
- **Table 2 "This Study" 249 kW** is the notebook's Class 5 case, 249.93 kW, truncated.
- The notebook's own markdown says Class 5 uses 75 C and "saturated liquid water"; the code
  and the paper both use 73 C and R134a at 16 bar. The code is right; the notes are stale.
- Cell 16 (a depth/flow sweep with fixed enthalpies) is exploratory and not in the paper.
- Well depth (3000 m) is set in calculate_geothermal_output but never used.
- CoolProp is pinned to 6.7 (what ran); property tables can change between versions.
