# geothermal-siting-su-2025

Code for:

> Jones, E. C. Jr., Munjurpet Sridharan, C., Aghapour, R., & Rodriguez, A. (2025). **Re-Energizing Legacy Fossil Infrastructure: Evaluating Geothermal Power in Tribal Lands and HUBZones.** *Sustainability*, 17(6), 2558. https://doi.org/10.3390/su17062558

**Status:** published artifact — reproduces the paper's Tables 4 and 5 exactly, and the "This Study" column of Table 2, from `python scripts/run_all.py` (2026-09-29). The GIS analysis that produced Table 3 was done in ArcGIS and is not re-run here. Not yet run from a clean clone on a second machine.

## What it does

The paper maps U.S. geothermal potential (by temperature class) against tribal lands, HUBZones and existing oil and gas wells, then estimates how much power could be developed there.

| Stage | Where | Paper |
|---|---|---|
| GIS suitability analysis | ArcGIS Pro / Online — [published layers](https://arcg.is/0OWujj) | Figures, Table 3 |
| Per-class areas and well counts | `data/raw/gis_class_summary.csv` | Table 3 |
| Power per repurposed oil/gas well: R134a organic Rankine cycle, CoolProp | `notebooks/geothermal_calcs.ipynb` | §3.5.1, Table 2 |
| Enhanced-geothermal capacity and number of facilities per class and land type | same notebook | Tables 4, 5 |

## Inputs

`data/raw/gis_class_summary.csv` — committed on purpose: the per-class results of the authors' ArcGIS analysis (land area in sq mi and oil-well counts, total / in HUBZones / in tribal communities), exactly as published in Table 3. The notebook types the same numbers in; a test keeps them identical.

## Running it

```bash
git clone https://github.com/sear-labs/geothermal-siting-su-2025.git
cd geothermal-siting-su-2025
python3.11 -m venv .venv && source .venv/bin/activate
pip install -e ".[notebooks]"               # exactly what ran: pip install -r requirements-lock.txt -e .
python scripts/run_all.py
```

`run_all.py` executes the notebook in `results/runs/` (the committed notebook is not modified) and writes:

- `results/tables/per_well_power.csv` — power per repurposed well, by class
- `results/tables/table4_capacity_gw.csv` — Table 4
- `results/tables/table5_facilities.csv` — Table 5

Runs in seconds; no solver or licence. On Google Colab the notebook still installs CoolProp itself.

## What is deliberately committed

`data/raw/` (the GIS summary) and `results/tables/` (the three tables), so a reader sees the numbers without running anything. `results/runs/` is gitignored.

## Tests

```bash
pip install -e ".[dev]"
pytest -q
```

No CoolProp needed. The tests check that the inputs equal the paper's Table 3 (and the notebook's own numbers); that the regenerated Tables 4 and 5 equal the printed ones; that Table 2's 249 kW comes out; that inlet enthalpy exceeds outlet, per-well power falls with temperature and equals ṁ·Δh·η; that HUBZone and tribal areas never exceed the total; and that the facilities counted fit in the land available.

## Known issues

- **Table 5's "Total" average plant capacity (94.94 MW) adds up the three class averages** (44.08 + 28.97 + 21.89). A sum of averages is not an average: the capacity-weighted average is total potential ÷ total facilities ≈ **26.5 MW**. The other totals in the table are correct.
- **Table 2 prints 249 kW**; the calculation gives 249.93 kW (truncated rather than rounded).
- The notebook's explanatory text says Class 5 uses 75 °C and saturated liquid water; the code and the paper use **73 °C and R134a**. The code is right.

`CLAUDE.md` records these and the project's other conventions.

## How to cite

```bibtex
@article{jones2025geothermal,
  author  = {Jones, Jr., Erick C. and Munjurpet Sridharan, Chandramouli and Aghapour, Raziye and Rodriguez, Angel},
  title   = {Re-Energizing Legacy Fossil Infrastructure: Evaluating Geothermal Power in Tribal Lands and HUBZones},
  journal = {Sustainability},
  volume  = {17},
  number  = {6},
  pages   = {2558},
  year    = {2025},
  doi     = {10.3390/su17062558}
}
```

GitHub's **Cite this repository** button reads the same from `CITATION.cff`.

## License

Code: MIT — see [LICENSE](LICENSE). The paper is open access under CC BY 4.0; read it via the DOI.
