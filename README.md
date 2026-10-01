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

## Known issues in the published paper

These are recorded here only; there is no journal correction. The code reproduces the paper **as
published**, and `results/tables/` holds the published numbers.

### What this means for the paper's conclusions

**No headline conclusion changes.** Two figures in the Conclusions section are typos, one table
total uses the wrong kind of average, and several assumptions were not stated. With those fixed:

| Conclusion | Correct figure | Note |
|---|---|---|
| Technical EGS potential, eight states | **2,372.8 GW** (Table 4) | The Conclusions print 2328 GW (item 5) |
| Potential in HUBZones | **765.8 GW** | Measured with Justice40 tracts as a proxy: right order of magnitude, not exact HUBZone areas. Overlaps the tribal-lands figure, so do not add the two (item 2) |
| Potential on tribal lands | **347.2 GW** | |
| Capacity from repurposed oil and gas wells | **4.3 GW**, from the 14,220 wells in Classes 1–3 | The Conclusions print 3 GW (item 6). 18,520 wells were counted across all classes (item 7) |
| Average plant capacity across Classes 1–3 | **About 26.5 MW** | Table 5 prints 94.94 MW (item 8) |
| Gross power, Table 2 "This Study" | **250 kW** | Printed as 249 kW (item 9) |

### Assumptions the paper does not state

1. **Land per site.** Each site is counted as its 10 km² reservoir plus a 500 m-radius zone around
   the borehole (0.79 km²), for 10.8 km² per site. Sites are packed edge to edge until the land in
   each class is used up. Other land uses (urban areas, parks, private land) are not excluded, as
   §3.5.3 says. The borehole zone would normally lie inside the reservoir footprint, so adding it
   on top is about 8% conservative: 10 km² per site would allow about 96,400 sites rather than
   89,404. If neighbouring reservoirs instead had to be 500 m apart, capacity would be about 20%
   lower.
2. **Justice40 tracts as a proxy for HUBZones.** The study began with Justice40 tracts and moved to
   HUBZones. In the data used, Justice40 tracts overlap substantially with HUBZone and tribal-land
   tracts, so the Justice40 layer serves as a proxy. Every "HUBZone" figure in Tables 3–5, the
   abstract and the Conclusions is a Justice40-tract figure: right order of magnitude and general
   conclusions, not an exact HUBZone area. The layer also includes tribal lands, so the HUBZone and
   tribal-land figures overlap and should not be added together.
3. **Class 3 meets the 120 °C threshold.** The paper counts only reservoirs at 120 °C or above,
   "which excludes Classes 4, 5, and 999". Class 3 spans 110–130 °C and is included in full at its
   120 °C midpoint, because the data cannot separate the 110–120 °C part. The "372,309 sq mi …
   120 °C and above" in the Conclusions rests on this assumption.
4. **Class 1's representative temperature.** 170 °C is a representative value for Class 1
   (>150 °C), chosen toward the low end of the 150–200 °C band where most deep-EGS potential lies
   [19, 50]. It is not a lower bound, as §3.5.2 calls it: the class's lower bound is 150 °C. At
   150 °C, Class 1 plants would be 33.3 MW rather than 44.1 MW, and total potential about 2,290 GW
   rather than 2,372.8 GW.

### Figures that contradict the paper's own tables

5. **Conclusions, total potential:** prints **2328 GW**; Table 4 and the Results give
   **2372.8 GW**.
6. **Conclusions, repurposed wells:** prints **3 GW**; Table 4 gives **4.3 GW** ("over 4 GW" in
   the Results).
7. **Wells counted vs wells calculated:** 18,520 orphaned wells were *counted* in the study area
   (Classes 1–5). Capacity was *calculated* only for the 14,220 in Classes 1–3: 6,166 in HUBZone
   (Justice40) tracts and 5,774 on tribal lands. The abstract's "over 18,000 … that could be
   converted" should be read with that distinction.
8. **Table 5, "Total" average plant capacity:** prints 94.94 MW, the sum of the three class
   averages. The capacity-weighted average is **about 26.5 MW**. The other totals in the table are
   correct.
9. **Table 2** prints 249 kW; the calculation gives 249.93 kW, which rounds to **250 kW**.
10. **Well counts per class are rounded.** Table 3's per-class totals (20; 2,200; 12,000; 2,000;
    2,300) are rounded, while the HUBZone and tribal subsets are exact counts; the calculations
    use the rounded totals. The exact totals cannot be regenerated from public data: the ArcGIS
    Online copy of the USGS orphaned-well dataset used in the analysis now requires a sign-in.
    Re-counting against the public USGS release (doi:10.5066/P91PJETI) with the paper's own
    polygon layers reproduces five of the ten exact subset counts (Justice40 Classes 1, 2 and 4:
    1, 201, 334; tribal Classes 1 and 2: 0, 22). That confirms the method, but Classes 3 and 5
    differ, so the dataset versions differ. Exact totals need the original ArcGIS project.

### Where the text does not match the method

11. **Class 999.** The two source datasets define it differently: "no temperature data" (Table 1)
    and "below 150 °C at a 10 km depth" (§3.4). Both label it Class 999, and it is excluded from
    the capacity estimates either way.
12. **Enthalpy.** §3.5.1 describes "the specific enthalpy of the saturated liquid". The code uses
    R134a vapour at 16 bar and the bottom-hole temperature (445 kJ/kg at 73 °C, where saturated
    liquid would be 309.5 kJ/kg), minus liquid R134a at 4.39 bar and 10 °C. The code is the
    intended cycle; the description is wrong.
13. **Table 2 is a consistency check, not a validation.** The 9% cycle efficiency is an input.
    With the Chena unit's measured 8.2%, the same calculation gives 228 kW rather than 250 kW. It
    also assumes the refrigerant reaches the full brine temperature.

### Facts and wording

14. **§1:** "The National Emergency Energy Act signed in 2025" is the Executive Order *Declaring a
    National Energy Emergency*, as the abstract says.
15. **§1:** "authorized by the Energy Act of 2005" is the **Energy Policy** Act of 2005, as in
    §5.1.
16. **§3.2:** the Justice40 low-income criterion is a tract at or above the **65th percentile** for
    people in households at or below twice the federal poverty level, not "more than 65 percent of
    households".
17. **§4.6** says orphaned wells and tribal lands "mainly overlap in Oklahoma and Louisiana";
    **§4.3** says Louisiana has "few or no tribal lands".
18. "Energy Information Agency" should be Administration; "United States Geology Survey" should be
    Geological Survey. Typos: "adminstration" (abstract), "identfies", "remidiate", "Abandonded"
    (§2.5 heading), "Adminsistration", "incorprated", "communties".
19. The notebook's explanatory text says Class 5 uses 75 °C and saturated liquid water. The code
    and the paper use 73 °C and R134a, and the code is right.

`CLAUDE.md` records the project's other conventions.

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

| What | Licence |
|---|---|
| Code: `notebooks/`, `scripts/`, `tests/`, and the rest of the repository | MIT, see [LICENSE](LICENSE) |
| Data and results: `data/raw/` and `results/tables/` | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

The paper is open access under CC BY 4.0; read it via the DOI.
