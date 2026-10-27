# Data dictionary

Version 1.0; prepublication companion baseline dated 27 October 2026.

## Observations and provenance

The five files in `data/archived/` retain the original World Bank API format: a two-element JSON array containing response metadata and an array of observations. They are the baseline calculation inputs. A `null` value means missing; it is never replaced with zero.

| File | Indicator | Period | Unit and meaning |
| --- | --- | --- | --- |
| `population.json` | `SP.POP.TOTL` | Ethiopia, 1993–2025 | People; midyear population estimates, subject to revision |
| `imports.json` | `TM.VAL.MRCH.CD.WT` | Ethiopia, 1993–2025 | Merchandise imports, current US dollars; underlying provider WTO |
| `exports.json` | `TX.VAL.MRCH.CD.WT` | Ethiopia, 1993–2025 | Merchandise exports, current US dollars; underlying provider WTO |
| `NY.GDP.MKTP.KD.json` | `NY.GDP.MKTP.KD` | Ten countries, 2010–2024 | GDP in constant 2015 US dollars |
| `NY.GDP.MKTP.CD.json` | `NY.GDP.MKTP.CD` | Ten countries, 2010–2024 | GDP in current US dollars |

The GDP country codes are ETH, DJI, KEN, UGA, TZA, RWA, ERI, SOM, SDN and SSD. The historical correlation exercise uses Ethiopia and five partners: Djibouti, Kenya, Uganda, Tanzania and Rwanda. Ethiopia is excluded from the partner aggregate. Available preceding-year values produce eleven common growth observations for 2014–2024. Missing Eritrean and South Sudanese values are not imputed. This subset is not an official East African or East African Community aggregate.

Each observation has these principal fields:

| Field | Meaning |
| --- | --- |
| `indicator.id`, `indicator.value` | Series identifier and provider label |
| `country.id`, `country.value`, `countryiso3code` | Provider country identifiers/name and three-letter code |
| `date` | Calendar year, stored as a string |
| `value` | Numeric observation or `null` |
| `unit`, `obs_status`, `decimal` | Provider-supplied descriptors, retained without inventing missing detail |

Response metadata include `page`, `pages`, `per_page`, `total`, `sourceid` and `lastupdated`. The baseline responses report a database update of 8 October 2026. Population/trade retrieval is dated 10 October; GDP retrieval is dated 11 October. Exact query evidence and its scope are listed in `SOURCE_QUERIES.json`. The original GDP query manifest was recovered separately and its responses match the included data byte for byte.

`data/verification_2026_10_27/` contains five separately retained API responses. The GDP queries extend through 2025. Their historical filename prefix `economics_live_` is preserved, but these files are frozen snapshots, not live feeds. The reproduction script compares common observations and calculates a separate updated correlation; it does not substitute those values for the archived baseline.

`data/metadata/` contains official indicator definitions fetched on 27 October 2026. `data/provenance/` contains query records. Metadata describe the observations; they do not turn a hypothetical project coefficient into an observed quantity.

## Machine-readable tables

`tables.json` contains an ordered `tables` array. Item zero corresponds to Table 1. Each table is an array of rows, with the header row first and cell contents stored as strings. Displayed commas, signs, percentages and rounding are preserved. `export_tables.py` exports the same cells to CSV without re-estimating any value.

| Table | Content | Status and units |
| --- | --- | --- |
| 1 | Historical milestones | Dated source-based chronology; not numerical project inputs |
| 2 | Selected Ethiopia observations | Population in millions; merchandise imports/exports in billions of current US dollars |
| 3 | Studies and decisions | Qualitative study framework |
| 4 | Hazards and responses | Qualitative engineering framework |
| 5 | Fictional Route A/Route B costs | US dollars per container |
| 6 | Hypothetical project outcomes | Traffic in million tonnes/year; annual net equivalent in US$ millions |
| 7 | Discount-rate sensitivity | Rate; annual equivalent US$ millions; million tonnes/year |
| 8 | Gateway comparison questions | Qualitative framework; no cost ranking |
| 9 | Proposed indicators | Qualitative measurement definitions |
| 10 | Coastal hub capital allowances | US$ millions in constant 2026 dollars; selected allowances and 25% contingency |
| 11 | Development package alternatives | Conditional capital/time ranges; alternatives include overlapping scopes |
| 12 | Employment-based population cases | Assumed jobs and additional residents; excludes existing population |
| 13 | Historical growth correlations | Pearson r; eleven observations, or ten when 2020 is excluded |
| 14 | Additional production identities | Annual GDP increments in US$ millions, constant 2026 dollars, Operating Year 10 |
| 15 | Voluntary gifts | Total five-year US$ millions and percentage of the US$2.075 billion hub capital |

## Selected teaching assumptions and identities

These are author-selected inputs, not measurements or estimated causal coefficients.

| Example | Inputs and definition |
| --- | --- |
| Container inventory | US$20,000 cargo; 18% annual carrying rate; days divided by 365. Route A uses twenty days and Route B fourteen. Other cost entries appear in Table 5. Avoid double counting storage or disruption. |
| Chapter 8 investment | US$1.5 billion initial capital, twenty-five years, 8% discount rate, US$30 million annual O&M. Sensitivities use 4% and 12%. Annual equivalent is capital divided by annuity present-value factor, plus O&M. |
| Central shared hub | US$2.075 billion initial capital, twenty-five years, 8% economic rate, US$45 million annual O&M; US$200 million annual gross savings. Capital at time zero; constant year-end flows; no residual value or ramp-up. |
| Ethiopian production | Annual tonnes × dollars saved per tonne × selected capture fraction, plus additional private productive capital × selected annual value-added-to-capital ratio. |
| Partner supplier production | Ethiopian increment × 0.35 incremental-import share × 0.20 regional sourcing share × 0.55 domestic value-added share. Separate net logistics and industry components are added only if additional and nonoverlapping. |
| Central additional capital | US$1.0 billion Ethiopian and US$0.3 billion other-regional private industry, outside the shared hub capital. Value added is not profit or a return on hub expenditure. |
| Construction employment | US$1.58 billion eligible asset expenditure × 18% direct labor share ÷ US$9,000 loaded annual labor cost. Divide person-years by six years for an average, then multiply by 1.5 for the selected peak. |
| Settlement population | Jobs × 70% associated with new-resident households ÷ 1.5 workers per household × four members. Service-job ratios vary by cluster. These are not migration estimates. |
| Water and energy | 100 litres of domestic water per resident per day; 20% distribution loss; 4 kWh per cubic metre produced. The medium increment requires 5,600 m³/day delivered, 7,000 produced and 28 MWh/day for desalination. Additional uses require separate provision. |
| Maturity | Year 5 is 0.35 times the selected Year 10 effect; Year 15 is 1.30 times it. Operating years move with the actual opening date. |
| Scale comparator | Ethiopia’s 2024 current-dollar GDP × 1.02² × 1.06¹². This is an illustrative dollar convention and scale comparison, not a World Bank forecast or a baseline tied to an actual coastal opening. |

The limited, central and strong production cases are chosen combinations, not a probability distribution or a complete range of outcomes. Zero response and adverse regional diversion remain possible. A project appraisal would require a realistic without-project alternative, resource costs, environmental/social effects, displacement and additionality evidence.

## Unrounded teaching rows

`companion_rows.json` has three named arrays. Numeric values are stored as strings in the preserved source rows.

- `hypothetical_inventory_costs.csv`: `cargo_value_usd`, `annual_carrying_rate`, `extra_days`, `cost_usd`; fifteen combinations.
- `hypothetical_financing.csv`: `rate`, `capital_usd`, `years`, `annualized_capital_usd`, `annual_total_usd`, `break_even_tonnes_at_20_usd_saving`; three rate cases. Annual O&M is US$30 million.
- `hypothetical_project_grid.csv`: `capital_usd`, `rate`, `years`, `annual_operations_usd`, `traffic_tonnes`, `gross_saving_usd_per_tonne`, `annualized_cost_usd`, `net_annual_benefit_usd`; nine traffic/saving combinations.

## Outputs, references and geographic data

`results/core_models.json` records calculated/printed values, tolerances, differences, pass flags, units and assumption/source basis. Comparisons validate arithmetic against displayed precision. They do not validate a real project. `results/supplemental.json` records additional identities and downside cases; its monetary fields are US$ millions unless the field explicitly names dollars.

`references.json` has `number`, `entry` and `url`. The CSV has matching `Number`, `Entry` and `URL` columns. The directory contains 89 entries. It is a source index, not permission to redistribute all linked works.

Geographic inputs and map coordinates are described in `FIGURES.md` and the geographic source records. Natural Earth geometry is generalized; World Port Index coordinates are approximate and dated 2019. Dotted connectors are study axes rather than surveyed roads, operating routes or legal boundaries. Component-specific rights are described in `THIRD_PARTY_NOTICES.md` and `LICENSE.md`.
