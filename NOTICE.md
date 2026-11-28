# Data attribution

This database is based predominantly on official administrative-division references, supplemented by other publicly available geographic sources for cross-checking and missing information. See LICENSE and the source-specific notices in licenses/, including their reuse terms and outstanding rights questions.

Source attribution: includes data derived from [Countries States Cities Database](https://github.com/dr5hn/countries-states-cities-database/releases/tag/v5.2.0-export.1) by Darshan Gada and contributors, snapshot v5.2.0-export.1, under the Open Database License 1.0.

Data snapshots and SHA-256 digests: `sources.lock.json`. Pinyin: `pinyin-pro`.

Time zones: [geo-tz](https://github.com/evansiroky/node-geo-tz) 8.1.11 using [timezone-boundary-builder](https://github.com/evansiroky/timezone-boundary-builder) (ODbL, © OpenStreetMap contributors), and the [IANA Time Zone Database](https://www.iana.org/time-zones) 2026f country-zone table (public domain).

Mainland China administrative codes and official names are selected from [mumuy/data_location](https://github.com/mumuy/data_location), used under MIT (see licenses/data_location-MIT.txt).

The China Institute of Toponymy supplied Xiamen's city point to the [UN Group of Experts on Geographical Names](https://ungegn.un.org/dashboard/cities/details?id=2441). Mainland city points are checked against the [Tianditu city boundary layer](https://cloudcenter.tianditu.gov.cn/administrativeDivision).

The public-domain [Natural Earth populated places, 1:10m v5.1.2](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-populated-places/) supplies cross-checks, names and five city-territory coordinates.

City classifications, names and coordinates: [Wikidata (CC0)](https://www.wikidata.org/wiki/Wikidata:Licensing).

The UK city selection is based on the [Cabinet Office List of cities](https://www.gov.uk/government/publications/list-of-cities/list-of-cities-html). Contains public sector information licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

National city registers and additional urban coordinates are credited in [official-data.md](licenses/official-data.md), including the U.S. Census Bureau, IBGE, Destatis, Japan MIC, Philippine Statistics Authority and GeoNames.

Local-government rosters and territorial place names are documented in [the source register](licenses/single-city-review.md).

Municipal data uses HCP census identifiers, GISCO 2024 geography and location points credited in [the source register](licenses/municipal-followup.md).

Localities and municipal equivalents are credited in [the locality source register](licenses/search-localities.md).

Municipal registers, coordinate sources and license details are listed by country in [the municipal source register](licenses/municipal-rosters.md).

Chinese names and transliterations are described in [the Chinese name sources](licenses/chinese-place-names.md).

## Additional source attribution

See the [municipal source register](licenses/municipal-rosters.md) for country-specific sources and terms.

- Australia, South Africa, and Switzerland cite official municipal registers, boundary-derived points, and GeoNames in [the municipal source register](licenses/municipal-rosters.md).
- Spain, Italy, and Mexico use the official INE and IGN, Istat, and INEGI registers, with source and point methods documented in [the municipal source register](licenses/municipal-rosters.md).
- Metropolitan France uses Insee's Code officiel géographique and Etalab's 2026 mairie point layer under Licence Ouverte 2.0.
- Angola’s National Institute of Statistics for the Census Atlas, Bolivia’s INE, SDSN Bolivia and Laboratorio de Tecnologías Sociales for the municipal geodata (CC BY 4.0), and the Mongolian NSO and OCHA for the COD-AB reference (CC BY 3.0 IGO). Same-name settlement coordinates use GeoNames (CC BY 4.0).
- American Samoa, Ukraine and Venezuela: U.S. Census Bureau TIGER/Line data, Ukraine’s 2026 KATOTTG and OpenStreetMap contributor coordinates cross-referenced by ua-geo (ODbL), and Venezuela INE boundaries from OCHA (CC BY 3.0 IGO).
- the Tonga Statistics Department and Department of Lands, the Palau National Government, Suriname’s electoral secretariat, and Equatorial Guinea’s national statistical institute and government press office. Reference points use GeoNames, geoBoundaries, and OpenStreetMap contributors where indicated.
- Nigeria’s Office of the Surveyor-General and Independent National Electoral Commission, Burkina Faso’s INSD and Institut Géographique du Burkina, and the Lao Statistics Bureau and National Geographic Department. Geographic points and boundaries provided through OCHA COD-AB are credited under [CC BY 3.0 IGO](https://creativecommons.org/licenses/by/3.0/igo/).
- Argentina’s INDEC and Georef, Algeria’s national gazette and syscli’s MIT transcription ([license](licenses/syscli-algeria-MIT.txt)), and Julia Clark’s reference map of Tunisian municipalities. Boundaries from OpenStreetMap-derived layers are credited to OpenStreetMap contributors.
- Senegal's ANSD and ONDDL, Vie-Publique and OrvLabs, Niger's INS and Ministry of the Interior, and the Turks and Caicos Islands Attorney General's Chambers. Point sources credit GeoNames, OpenStreetMap contributors, and OCHA's COD partners where indicated.
- Statistics Canada, the relevant Canadian provincial governments, Côte d’Ivoire’s General Directorate of Taxes and Treasury, and Bhutan’s Ministry of Infrastructure and Transport and Election Commission. Representative points also use GeoNames and OpenStreetMap contributors.
- the Sudanese Ministry of Justice and COD-AB contributors, the Parliament and Central Statistical Organization of Yemen, and Kuwait’s Ministry of Justice. Point attribution is recorded per place, including GeoNames, Overture Maps, and OCHA COD partners where indicated.
- Mauritania’s ANSADE, Ministry of the Interior, GeoNames, Open Admin Data and CheikhEbeoumar/mauritania-geo, together with the Saint Kitts and Nevis Law Commission and the Nevis Island Administration.
- Myanmar sources include the General Administration Department and the Myanmar Information Management Unit. The MIMU-sourced elements are available for noncommercial reuse with attribution under [MIMU terms](https://themimu.info/license/). Representative points also credit GeoNames and OpenStreetMap contributors as indicated in [the source register](licenses/municipal-rosters.md).
- Madagascar sources include the Independent National Electoral Commission, the National Legislation Centre, BNGRC and OCHA for election and administrative reference data. Coordinates also credit GeoNames and OpenStreetMap contributors.
- Palestine sources include the Central Elections Commission, the Municipal Development and Lending Fund, and GeoNames.
- Guinea and Guinea-Bissau sources include the respective ministries, the national statistical agencies, OCHA COD partners, GeoNames, OpenStreetMap contributors, and the additional point references documented per row.
- Eritrea sources include the Eritrean ministries, the Central Region Administration, African Development Bank project materials, OCHA COD partners, and GeoNames.
- Korea (North) sources include the Korean national statistics office and Ministry of Unification, the administrative law collection published by the National Intelligence Service, GeoNames, and the Endonym Atlas.
- the UAE federal and emirate governments, the Moroccan Haut-Commissariat au Plan and Interior Ministry, the Morocco Census crosswalk, GISCO, GeoNames and Wikidata.
- Central African Republic sources include ICASEES, the national elections authority, the U.S. Census Bureau, OCHA COD partners, MINUSCA, GeoNames and OpenStreetMap contributors.
- Türkiye sources include the Turkish Official Gazette and the Ministry of Environment, Urbanisation and Climate Change, the Ministry of Interior, OCHA COD partners, GeoNames and OpenStreetMap contributors.
- Libya sources include the Ministry of Local Government, Libya's High National Elections Commission, the Libyan Legal Archive, and OCHA's Libya COD partners. Representative coordinates credit GeoNames and OpenStreetMap contributors where indicated.
- Russia sources include the Bank of Russia publications of OKATO and OKTMO, the Federal Agency on Technical Regulating and Metrology, the Leningrad Oblast legislature, Kurskstat and GeoNames.
- Iran sources include the Statistical Centre of Iran, the public cabinet decisions where indicated, GeoNames, OpenStreetMap contributors and Wikidata.
- Lebanon sources include the Ministry of Interior and Municipalities, UNDP Lebanon, the Municipality of Tabarja and Kfaryassine, Lebanon's Central Administration of Statistics, OCHA, GeoNames and OpenStreetMap contributors.
- Somalia sources include the Somali Disaster Management Agency, OCHA, FAO SWALIM, GeoNames and OpenStreetMap contributors.
- Curaçao and Sint Maarten sources include their spatial planning ministries and Curaçao's Central Bureau of Statistics.
- Ethiopia sources include the Ethiopian Statistical Service, regional Bureaux of Finance and Economic Development, OCHA, GeoNames and the UNHCR map referenced by DIIS.
- Egypt sources include the Cabinet’s Information and Decision Support Center, CAPMAS, the New Urban Communities Authority, the Egyptian General Survey Authority, OCHA, GeoNames, and keltokhy/Egypt_NUCA’s transcription of the official city planning layer.
- Pakistan sources include the Pakistan Bureau of Statistics, Survey of Pakistan, Punjab and Balochistan local government departments, Khyber Pakhtunkhwa local government offices, the Azad Jammu and Kashmir Planning and Development Department, the Gilgit-Baltistan Election Commission, OCHA, GeoNames, and OpenStreetMap contributors.
- South Sudan sources include the National Audit Chamber, the National Bureau of Statistics, the Ministry of Finance and Planning, the National Elections Commission, Abyei and Warrap local administrations, OCHA, IOM, GeoNames, and OpenStreetMap contributors.
- India sources include the Ministry of Panchayati Raj, the National Informatics Centre (Bharatmaps), the Central Pollution Control Board, Ministry of Housing and Urban Affairs, Survey of India, India Post, the respective governments of Delhi, Telangana, Karnataka and Maharashtra, GeoNames, OpenStreetMap and Wikimedia contributors.
- Mali's National Directorate of Territorial Planning, National Institute of Statistics, Ministry of Economy and Finance and Geographic Institute, Chad's General Secretariat of Government and INSEED, Liberia's Executive Mansion, Ministry of Local Government, LISGIS and the Liberia News Agency, and the OCHA, UNMEER, GeoNames and OpenStreetMap contributors named in the [source register](licenses/municipal-rosters.md).
- the Afghanistan National Portal and the government and UN-Habitat State of Afghan Cities project, Iraq's Basra Municipalities Directorate, Syria's published city-council decrees and local administration ministry, and OCHA and GeoNames for representative points.
- Syria's Ministry of Local Administration and Environment for its published council appointment orders, the Syrian Official Gazette and SANA for later records, and OCHA and GeoNames for populated-place coordinates. Mali's added points were checked against its 2023 commune act and OCHA/IGM district boundaries.
