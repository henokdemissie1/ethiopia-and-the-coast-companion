# Ethiopia and the Coast: public numerical companion

**First Edition — v1.0**  
Henok Kefelegn, PhD  
Companion baseline: 27 October 2026

Download the [First Edition — v1.0 release](https://github.com/henokdemissie1/ethiopia-and-the-coast-companion/releases/tag/v1.0), visit the [companion website](https://henokdemissie1.github.io/ethiopia-and-the-coast-companion/), or use the [version-specific archival DOI](https://doi.org/10.5281/zenodo.23698701). The [repository](https://github.com/henokdemissie1/ethiopia-and-the-coast-companion) contains the public source files. Cite version 1.0 when referring to these frozen inputs and results.

This dataset, code, table and figure collection accompanies the prepublication baseline of *Ethiopia and the Coast*. “First Edition” identifies this companion release. It does not declare the book finalized or certify an investment proposal.

The package contains dated public observations and explicitly chosen teaching scenarios. The observations describe population, merchandise trade and historical GDP. The scenarios illustrate shipment costs, project thresholds, capital, production, employment, population and utilities. They are not measurements of present Assab conditions or forecasts of investment returns. GDP is value added, not net welfare or an investor’s profit.

## Reproduce the calculations

Download the complete release archive and extract it. Open a terminal in the extracted folder. Python 3.10 or later is required; the numerical scripts use only its standard library and need no network access, API key or manuscript file.

Before regenerating outputs, optionally run `python verify_integrity.py` to check the distributed files against `MANIFEST.json`. The manifest excludes itself. Regenerating figures or calculation outputs can legitimately change their file hashes; verify the freshly extracted archive first. The release also supplies a SHA-256 checksum for the complete ZIP.

```sh
python reproduce_core_models.py --tables-only
python reproduce_supplemental.py
python export_tables.py
```

These commands write:

- `results/core_models.json`: calculated comparisons, historical correlations and scenario diagnostics.
- `results/supplemental.json`: the negative hub NPV/BCR, full capital boundary, no-private-industry case, zero-response identity and diversion stress.
- `tables/table_01.csv` through `tables/table_15.csv`, with a table index.

The core baseline has 178 numerical comparisons, all passing within the stated rounding tolerances. This is an inventory of calculations, not an assessment of the realism of the assumed inputs. To send the core output elsewhere, use `--output PATH`.

## Reproduce the figures

The figure script uses Pillow in addition to the Python standard library:

```sh
python -m pip install Pillow
python reproduce_figures.py
```

The script runs offline. It produces equivalent numerical plots, their CSV/JSON data and a validation record. See [FIGURES.md](FIGURES.md) for the exact mapping, output paths, dependencies and distinctions between supplied originals and regenerated equivalents. The originals comprise fourteen numbered figures and two orientation maps; superseded redline images are excluded. Pixel-identical rendering across operating systems is not promised.

The preparation environment used Python 3.12.14 and Pillow 12.3.0. These versions identify the tested environment; the numerical scripts remain standard-library-only.

## What is included

| Path | Content |
| --- | --- |
| `data/archived/` | Five frozen World Bank API responses used to reproduce the baseline |
| `data/verification_2026_10_27/` | Separately preserved comparison queries, including 2025 GDP; these do not replace the baseline |
| `data/metadata/` | Official indicator definitions and provider information |
| `data/provenance/` and `SOURCE_QUERIES.json` | Documented retrieval/query provenance, including the recovered original GDP query manifest |
| `tables.json` | Fifteen machine-readable baseline tables, retaining displayed rounding |
| `companion_rows.json` | Unrounded rows for three hypothetical numerical examples |
| `references.json`, `references.csv` | Ninety numbered reference entries and source URLs, including the companion self-citation [90] |
| `map_data/` | Generalized geographic inputs; see source credits and the figure registry |
| `figures/`, `plot_data/`, `tables/`, `results/` | Supplied visuals and reproducible outputs described above |

[DATA_DICTIONARY.md](DATA_DICTIONARY.md) defines units, fields and assumptions. [SOURCE_QUERIES.json](SOURCE_QUERIES.json) distinguishes documented original queries from later verification queries. Re-running an API URL may return revised observations; use the included frozen files to reproduce v1.0.

## Reading the examples

The central hypothetical hub uses US$2.075 billion of shared capital, an 8% economic discount rate, twenty-five years and US$45 million annual operation and maintenance. US$200 million annual gross transport savings yield an NPV of approximately **minus US$420.41 million** and a BCR of **0.8355**. The example fails its transport-savings-only test.

The separate central production illustration also assumes US$1.3 billion of additional private productive capital, bringing the combined capital requirement to at least US$3.375 billion before stated exclusions. Its positive GDP identities cannot be added to transport savings to close the project deficit. Removing both private-industry assumptions while retaining the other central inputs gives US$175.39 million of combined annual production in the illustration. A zero production response is admissible.

All scenario money uses constant 2026 US dollars as a price convention. Operating Year 0 means the start of dependable commercial service, whenever it occurs. It is not a promised 2026 opening. Current-dollar trade/GDP observations retain their original units and are not silently converted to constant dollars or cargo tonnes.

## Sources, rights and versioning

World Development Indicators are credited to the World Bank and the underlying providers, including WTO for the two merchandise series and the providers identified in population and national-accounts metadata. Natural Earth and the World Port Index support generalized map geometry and approximate locations. Refer to [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [LICENSE.md](LICENSE.md) for component-specific terms. The companion does not relicense the book or the referenced publications.

The archive excludes the full manuscript, unpublished review notes and superseded figures. Reference entries link to the original publications; their full texts are not bundled. See [CHANGELOG.md](CHANGELOG.md) for release scope. Future revisions should preserve v1.0 and document changed inputs or methods rather than overwrite its data vintage.


## Dated illustration correction (27 October 2026)

The v1.0 label is retained for the disclosed expansion of Figure 1 to the historical scope of Table 1 and Chapter 1 and addition of the companion self-citation [90]. Numerical data and scenario inputs are unchanged. See [CHANGELOG.md](CHANGELOG.md), [FIGURES.md](FIGURES.md), and [CORRECTIONS_2026_10_27.json](CORRECTIONS_2026_10_27.json) for the precise change and prior-artifact checksum.


## Cite the corrected companion

Kefelegn, Henok. Ethiopia and the Coast: Data and Analysis Companion. First Edition, v1.0. Zenodo, 2026. Correction issued 27 October 2026. https://doi.org/10.5281/zenodo.23698701
