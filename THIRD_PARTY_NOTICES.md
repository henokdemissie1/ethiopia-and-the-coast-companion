# Third-party data and source notices

Public companion v1.0, baseline 27 October 2026. Terms checked against the primary sources below on 27 October 2026. These notices distinguish source observations from the author's hypothetical scenarios and original presentation.

## World Bank World Development Indicators

The archived reproduction inputs and the separately retained verification snapshot contain responses obtained from the World Bank Indicators API. The exact indicator landing pages below each identify **CC BY 4.0** as their data license. The general World Bank website terms preserve dataset-specific terms; their general website restrictions should not be substituted for these explicit indicator licenses.

| Indicator | Source credit shown by the World Bank |
| --- | --- |
| [SP.POP.TOTL: Population, total](https://data.worldbank.org/indicator/SP.POP.TOTL) | World Bank, World Development Indicators; underlying providers include UN Population Division / World Population Prospects, national statistical offices, Eurostat, and UN Statistics Division |
| [TM.VAL.MRCH.CD.WT: Merchandise imports, current US dollars](https://data.worldbank.org/indicator/TM.VAL.MRCH.CD.WT) | World Bank, World Development Indicators; World Trade Organization (WTO) |
| [TX.VAL.MRCH.CD.WT: Merchandise exports, current US dollars](https://data.worldbank.org/indicator/TX.VAL.MRCH.CD.WT) | World Bank, World Development Indicators; World Trade Organization (WTO) |
| [NY.GDP.MKTP.KD: GDP, constant 2015 US dollars](https://data.worldbank.org/indicator/NY.GDP.MKTP.KD) | World Bank, World Development Indicators; country official statistics / national statistical organizations and central banks; OECD National Accounts; World Bank staff estimates |
| [NY.GDP.MKTP.CD: GDP, current US dollars](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD) | Same GDP source categories as above |

License and required attribution/change notices: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). World Bank legal information: [Terms and Conditions](https://www.worldbank.org/ext/en/legal/terms-conditions).

`SOURCE_QUERIES.json` records each file, URL, indicator, date, API update stamp, and the limits of the preserved transport provenance. The archived population/trade retrieval is dated 10 October 2026; archived GDP retrieval is dated 11 October 2026. The later verification files are dated 27 October 2026 and are kept separate. Do not silently replace these inputs with current API responses.

Raw observation responses preserve source values and response metadata. Derived tables, growth rates, correlations, rounding, selections, and charts are author computations or presentation changes. Credit the World Bank and the listed underlying providers when reusing those source-derived outputs, as well as the author for original presentation. The author has not converted third-party observations into author-owned data. No World Bank or provider endorsement is implied.

## Natural Earth

The generalized coastline and Addis Ababa location use the 1:50-million Natural Earth coastline and populated-places datasets. Their accompanying source README/version files are retained where distributed. Natural Earth states that all its raster and vector map-data versions are in the public domain and permits modification, electronic redistribution, print, and commercial use without permission or mandatory credit.

Courtesy credit: **Made with Natural Earth.**

Primary terms: <https://www.naturalearthdata.com/about/terms-of-use/>

The companion maps select a regional extent, omit political boundaries, and add the author's labels and study axes. These are original presentation choices, not a new license over the geographic source data. Dotted connections are comparison axes, not surveyed roads or operational corridors.

## National Geospatial-Intelligence Agency World Port Index

Five approximate port locations used in the maps are transcribed from the National Geospatial-Intelligence Agency (NGA), *World Port Index*, Publication 150, twenty-seventh edition, 2019: Mombasa 47100 (PDF page 157, printed page 130), Berbera 47820, Djibouti 47850, Assab 47880, and Massawa/Mitsiwa 47900 (the latter four on PDF page 159, printed page 132). `map_data/selected_locations.json` preserves the used coordinates and individual provenance; `figure_manifest.json` and `FIGURES.md` identify the visual transformations. The full reference PDF is omitted from this public package because the used coordinates and provenance suffice for the supplied maps.

The archived publication's title leaf (PDF page 3) states that it is a United States Government publication with no copyright claimed under Title 17 U.S.C. NGA's official public-information policy permits copying or distribution unless otherwise specified and requests source credits. No author-owned MIT or CC BY claim is made over the underlying NGA material.

Source PDF: <https://msi.nga.mil/api/publications/download?key=16694622%2FSFH00000%2FPub150bk.pdf&lang=en>

NGA public-information policy: <https://www.nga.mil/resources/Privacy_Policy.html>

The source is dated 2019. Its approximate coordinates do not establish present port depths, capacity, condition, ownership arrangements, or operating status. This companion is not a navigation product. Use does not imply NGA or United States Government endorsement.

## Other cited sources and original figures

The reference directory provides bibliographic metadata and source links. It does not redistribute or grant rights over the full cited publications. Original historical timelines, hypothetical engineering diagrams, and scenario charts are the author's illustrations. Source-derived numerical values remain attributed to their underlying sources; factual values are not represented as newly measured author observations.

For example, the sea-level figure uses stated IPCC AR6 Working Group I Summary for Policymakers numerical ranges and scenarios; the companion's figure registry identifies its source and the author's plotting transformation. The license for the original drawing does not grant a license to IPCC report text, logos, or source artwork. Reference excerpts and other separately identified third-party content retain their original rights.

No book manuscript, tracked review document, publisher layout, copied institutional logo, or font file is included in the public-data license grant. Python libraries and fonts installed by a reader retain their own licenses.

