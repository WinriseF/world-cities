# Updating the national rosters

Normal builds use the compressed snapshot in sources/official-cities.json.gz. The source registry is [official-data.md](../../licenses/official-data.md). The [audit download manifest](../../audit/2026-11-20/sources.json) also records the input checksums for this edition.

To refresh the snapshot, supply two directories to prepare.py. It uses Python 3.10+ and openpyxl as a maintenance tool.

- The register directory contains us.zip (the national Places Gazetteer), br.json (IBGE municipalities with view=nivelado), de.xlsx, jp.xlsx and ph.json (a mapping of each ten-digit PSA code to its official city label).
- The enrichment directory contains the extracted national IBGE GeoPackage named br-points.gpkg, ph-codes.json (a mapping of the same PSA codes to their older correspondence codes), and the five Wikidata TSV files named US.tsv, BR.tsv, DE.tsv, JP.tsv and PH.tsv. Request text/tab-separated-values for entity-roster.rq using the appropriate identifier property from the source registry. The final JSON stores the matched names and coordinates; ordinary builds never query live Wikidata.
- Run npm run build first to populate .cache/csc. For stable IDs the importer prefers the legacy city row when CSC has duplicate entries for one urban area. It can read that baseline from the previous local preview tarball, or the current built data as a fallback.
- Run python3 scripts/official/prepare.py REGISTERS ENRICHMENT, review changes in names, IDs, state assignments and point locations, then update the checksum under nationalRosters in sources.lock.json. Re-check the independent national reference codes before updating the regression fixtures in tests/official.test.mjs.

Run python3 scripts/official/verify.py PACKAGE.tgz REGISTERS to independently verify every audited national identifier and its parent against the packed JSON.

For mainland China, run `python3 scripts/official/verify-cn-boundaries.py PACKAGE.tgz 中国_市.geojson` with Shapely and pyproj. It compares both lists by six-digit code and tests each city point against its own Tianditu polygon in the layer's coordinate system. The reference file used for 0.1.3 has SHA-256 `d7a6f05b7e58cf758d74bd71ed0ea2ce981ef99436e4881e9a68098c3cd80b3b`.

The additional 59 international records are a reviewed selection from the 0.1.0 UN name-difference list. They required agreement between a UN city-proper row of at least 100,000, a unique GeoNames populated place of at least 50,000, one nearby upstream city candidate with a resolved region, and a Wikidata city classification. The candidate and GeoNames points had to be within 12 km, and a nearby already published city was excluded from automatic additions. Former places and village or urban-district classifications were excluded. Each saved record identifies the UN spelling, GeoNames ID and Wikidata ID so later edits can be checked against the same entity.

For the Polish and Indonesian snapshot, fetch the four files named in [the source manifest](../../audit/2026-11-20/0.1.2-sources.json) to REGISTERS. Run `python3 scripts/official/prepare-id-pl.py REGISTERS` and update the idPlRosters digest. The frozen Chinese label supplement is keyed by Polish SIMC identifier and records the matching Wikidata entity. Code and province validation of the installed files uses `python3 scripts/official/verify-additions.py PACKAGE.tgz REGISTERS OUTPUT.csv` (xlrd and beautifulsoup4, audit only), alongside verify.py for the original five national registers.

For the November 2026 register review, the [input manifest](../../audit/2026-11-21/inputs.json) gives the download locations and SHA-256 checksums. The [authority notes](../../licenses/national-review.md) also identify manually transcribed lists and their editions. Extracts from live GIS services can change order or contents. The frozen roster in sources is sufficient for an ordinary npm build.

To regenerate that review from its inputs, put the downloaded files under their manifest keys in a directory. Keep the 0.1.6 baseline tarball in artifacts to retain public IDs. Maintenance uses Python with Beautiful Soup, openpyxl, xlrd, pypdf, pyshp, pyproj and Shapely. Run these from the repository root.

```sh
python3 scripts/official/national_2026/reconcile.py INPUTS
python3 scripts/official/national_2026/snapshot.py INPUTS
npm run pack:local
python3 scripts/official/national_2026/verify.py artifacts/winrisef-world-cities-0.1.7.tgz INPUTS
python3 scripts/official/screen-un-cities.py artifacts/winrisef-world-cities-0.1.7.tgz UN_INPUTS audit/2026-11-21
```

UN_INPUTS contains un.xls and m49.csv from the 2026-11-20 audit. The screen counts unique, ambiguous and unmatched names within reporting areas. It uses published aliases and keeps the Hong Kong and Macao reporting areas distinct when matching names against the CN shard. The city-status decision is made separately using a legislative or statistical register.
