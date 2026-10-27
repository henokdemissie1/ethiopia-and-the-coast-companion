# Figure and map guide — First Edition, v1.0

The current book contains **14 numbered figures and two maps**, making 16 current visuals. There are no numbered Figures 15 or 16. This guide follows the book labels rather than treating the map count as additional figure numbers.

`figures/original/` preserves the exact current book-baseline PNGs from the authorized companion archive. **Figure 1 is `image3.png`; Figure 11 is `image15.png`.** Map 1 is `image1.png`. Superseded `image2.png` and `image14.png` are excluded. The public repository contains no manuscript text or DOCX.

`figures/regenerated/` contains new equivalent illustrations produced by the public scripts. Their data, stated assumptions and conceptual content are traceable, but their appearance is **not claimed to be pixel-identical** to the original images. These supplemental outputs do not modify the book or replace its preserved originals. Original-image SHA-256 hashes and the full mapping are recorded in [figure_manifest.json](figure_manifest.json).

Figure 1 retains the current **modern 1950–2024 scope**. It does not visualize the earlier ancient and colonial milestones in Table 1. The public release preserves that baseline selection.

## Reproduce offline

Use Python 3.10 or later. The numerical validation scripts and table exporter use the standard library. Figure rendering additionally requires **Pillow 10.1 or later**:

```sh
python -m pip install "Pillow>=10.1"
python export_tables.py
python reproduce_figures.py
```

The figure script reads the frozen data already in this release; it makes no network request. It creates all 14 numbered equivalents, both maps, CSV/JSON plot inputs under `plot_data/`, and `results/figure_validation.json`. The report distinguishes numeric agreement from empirical validation. The table exporter writes all 15 tables, including qualitative tables, to `tables/table_01.csv` through `tables/table_15.csv` and round-trip checks every displayed cell.

For only the eight formerly missing numerical chart builders:

```sh
python reproduce_figures.py --figures 3 4 5 8 9 10 13 14 --skip-maps
```

The existing entry points `build_history_figure.py`, `build_revised_timeline.py` and `build_maps.py` remain available. They now use portable font discovery with Pillow's scalable fallback, rather than requiring Windows Arial. Text metrics can vary across fonts and Pillow versions. Originals are never overwritten.

## All current visuals

Book-page numbers refer to the frozen 199-page revised reading edition used for this release.

| Book label and page | Original PNG | Equivalent output | Inputs and units | Evidence/assumption status |
| --- | --- | --- | --- | --- |
| Map 1, p. 16 | [image1.png](figures/original/image1.png) | [Map 1](figures/regenerated/map1_orientation_equivalent.png) | Natural Earth coastline and six selected locations; longitude/latitude degrees | General orientation. Boundaries omitted; no port operating status asserted. |
| Figure 1, p. 28 | [image3.png](figures/original/image3.png) | [Figure 1](figures/regenerated/figure_01_equivalent.png) | Eight dated milestones, 1950–2024; references 3, 4, 5, 9, 32, 73, 76 | A selective chronology. Events are equally spaced, not proportional to elapsed time. |
| Figure 2, p. 38 | [image4.png](figures/original/image4.png) | [Figure 2](figures/regenerated/figure_02_equivalent.png) | Farm/factory → dry port/customs → road/rail → terminal → ocean → buyer | Author conceptual service chain, without geographic scale or a surveyed route. |
| Figure 3, p. 44 | [image5.png](figures/original/image5.png) | [Figure 3](figures/regenerated/figure_03_equivalent.png) | `data/archived/population.json`, `SP.POP.TOTL`, 1993–2025; chart in million people | Archived WDI midyear population estimates; revisions are possible. Not a port-demand forecast. |
| Figure 4, p. 46 | [image6.png](figures/original/image6.png) | [Figure 4](figures/regenerated/figure_04_equivalent.png) | Archived imports/exports, `TM.VAL.MRCH.CD.WT` and `TX.VAL.MRCH.CD.WT`, 1993–2025; US$ billion | Current-dollar merchandise values from WDI/WTO. Neither cargo tonnes nor inflation-adjusted growth. |
| Figure 5, p. 48 | [image7.png](figures/original/image7.png) | [Figure 5](figures/regenerated/figure_05_equivalent.png) | Assumed shares 95/5, 70/20/10 and 60/25/15; squared-fraction sum = 0.905, 0.540, 0.445 | Author scenarios; no measured named-port shares. Index is unitless and is not disruption probability. |
| Map 2, p. 71 | [image8.png](figures/original/image8.png) | [Map 2](figures/regenerated/map2_comparison_equivalent.png) | Same location/coastline sources as Map 1; Addis-to-port comparison axes | Dotted connectors are study axes, not roads, railways, surveyed alignments or agreed corridors. |
| Figure 6, p. 75 | [image9.png](figures/original/image9.png) | [Figure 6](figures/regenerated/figure_06_equivalent.png) | Conceptual vessel, waterline, seabed, under-keel clearance, quay and land | Not to scale. Separate 14 + 0.7 + 0.5 + 1 = 16.2 m teaching arithmetic is not an Assab design depth. |
| Figure 7, p. 91 | [image10.png](figures/original/image10.png) | [Figure 7](figures/regenerated/figure_07_equivalent.png) | IPCC AR6 WGI B.5.3, reference 21: SSP1-1.9 0.28–0.55 m; SSP2-4.5 0.44–0.76 m; SSP5-8.5 0.63–1.01 m | Global likely ranges by 2100 relative to 1995–2014, not observed local change or local design levels. A likely upper bound is not a physical maximum. |
| Figure 8, p. 99 | [image11.png](figures/original/image11.png) | [Figure 8](figures/regenerated/figure_08_equivalent.png) | Table 5 components; US$/container. Cargo US$20,000, carrying rate 18%, 20 versus 14 days | Author cost assumptions plus calculated inventory. Routes are fictional; no measured Assab/Djibouti tariff comparison. Totals A 3,577.26; B 3,458.08. |
| Figure 9, p. 100 | [image12.png](figures/original/image12.png) | [Figure 9](figures/regenerated/figure_09_equivalent.png) | Cargo values US$5,000, 20,000, 100,000; days 0–30; `value × 0.18 × days / 365` | Author carrying-rate assumption. Excludes spoilage, penalties and production interruption; no observed lending quotation. |
| Figure 10, p. 104 | [image13.png](figures/original/image13.png) | [Figure 10](figures/regenerated/figure_10_equivalent.png) | US$1.5bn capital, 8% economic rate, 25 years, US$30m annual O&M; savings US$10/20/40 per tonne | Author teaching model. Annual equivalent cost US$170.518m; zero is gross savings equal to annual equivalent cost. No site NPV claim. |
| Figure 11, p. 143 | [image15.png](figures/original/image15.png) | [Figure 11](figures/regenerated/figure_11_equivalent.png) | Preparation windows 0.5–1.5, 2–5, 3–6, 5–10, 10–20 years | Author conditional planning windows. Enabling agreement and safe access start preparation; dependable commercial service starts a separate operating clock. |
| Figure 12, p. 149 | [image16.png](figures/original/image16.png) | [Figure 12](figures/regenerated/figure_12_equivalent.png) | Conceptual waterfront, existing neighborhoods, services, industry, housing, utilities and transport | No location, scale or fixed buffers. Existing residents, jobs, water and environmental evidence govern expansion. |
| Figure 13, p. 154 | [image17.png](figures/original/image17.png) | [Figure 13](figures/regenerated/figure_13_equivalent.png) | Archived `NY.GDP.MKTP.KD`; annual percentage growth, 2014–2024. Five partners = DJI, KEN, UGA, TZA, RWA | Historical transformation. Aggregate is growth of the sum of those five constant-2015-dollar GDP levels, excluding Ethiopia. Correlation approximately 0.26, −0.15 without 2020; no causal access effect. |
| Figure 14, p. 158 | [image18.png](figures/original/image18.png) | [Figure 14](figures/regenerated/figure_14_equivalent.png) | Table 14's limited/central/strong inputs; constant 2026 US$ million/year at Operating Year 10 | Author conditional accounting. Combined totals 145.0425, 643.865, 1,823.13 before display rounding; additional private investment required. Not net welfare, a cumulative total or an empirical forecast. |

## Numeric inputs and validation

The eight formerly unbuilt numerical figures now have explicit production code and CSV/JSON exports. Figure 3 and 4 values come directly from the archived raw series. Figure 13 recomputes annual growth from raw levels, then recomputes the two correlations. Figures 5, 8, 9, 10 and 14 are calculated from stated author assumptions. Full unrounded values are exported; displayed values are compared with the relevant frozen table strings using the table's rounding precision.

Figure 9 and 10 also check the older supplied `companion_rows.json` snapshots against independently recomputed formulas. Those snapshots are comparison targets, not primary observations. Table 5 and 6 compare the route components and investment thresholds; Table 13 checks correlations; Table 14 checks all eight components in each scenario. Validation establishes arithmetic and input agreement, not realism or causation.

Plot-data JSON files distinguish data status, units, sources and assumptions. Their CSV siblings are convenient rectangular chart inputs; schematic exports contain nodes/events rather than pretending they are measurements. `results/figure_validation.json` records the run and generated-file hashes. Font/layout changes do not invalidate numerical agreement.

## Map provenance

[map_data/selected_locations.json](map_data/selected_locations.json) records original degree/minute strings, decimal coordinates and source locators:

- Mombasa: World Port Index 47100, PDF p. 157 / printed p. 130.
- Berbera 47820, Djibouti 47850, Assab 47880 and Massawa/Mitsiwa 47900: PDF p. 159 / printed p. 132.
- Port source: NGA, *World Port Index*, Publication 150, 27th edition, 2019, reference 89. These coordinates do not establish present depth, capacity or operations.
- Addis Ababa and generalized coastline: Natural Earth 1:50 million datasets, reference 88; source addresses and versions are retained in the location register and dataset files.

The bundled Natural Earth coastline shapefile is sufficient to rerun the maps. The full NGA report is linked for traceability rather than redistributed here. No current survey or engineering alignment is implied by these orientation maps.

## Release scope

This public companion release adds a traceable reproduction path and clean figure mapping. It does not revise the manuscript, publish private editorial comments, update the frozen data vintage or convert teaching assumptions into evidence. Refer to the repository's data/asset notices for licenses and third-party attribution.
