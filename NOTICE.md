# Data attribution

This database is based predominantly on official administrative-division references, supplemented by other publicly available geographic sources for cross-checking and missing information. See LICENSE and the source-specific notices in licenses/, including their reuse terms and outstanding rights questions.

Source attribution: includes data derived from [Countries States Cities Database](https://github.com/dr5hn/countries-states-cities-database/releases/tag/v5.2.0-export.1) by Darshan Gada and contributors, snapshot v5.2.0-export.1, under the Open Database License 1.0.

This edition selects and normalizes names, keeps administrative links and WGS84 coordinates, adds generated Mandarin readings and reviewed corrections, and groups records by country. The upstream data files and SHA-256 digests are identified in sources.lock.json. The npm package includes the complete derived database in machine-readable JSON. Pinyin is generated using pinyin-pro at build time.

Mainland China administrative codes and official names are selected from [mumuy/data_location](https://github.com/mumuy/data_location), used under MIT (see licenses/data_location-MIT.txt).

The China Institute of Toponymy supplied Xiamen's city point to the [UN Group of Experts on Geographical Names](https://ungegn.un.org/dashboard/cities/details?id=2441). Mainland city points are checked against the [Tianditu city boundary layer](https://cloudcenter.tianditu.gov.cn/administrativeDivision).

The public-domain [Natural Earth populated places, 1:10m v5.1.2](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-populated-places/) supplies cross-checks, names and five city-territory coordinates.

Additional city status, labels and selected seat coordinates are from [Wikidata structured data (CC0)](https://www.wikidata.org/wiki/Wikidata:Licensing). The repository keeps a frozen Wikidata extract, its SPARQL query and supplemental names. Where the administrative-area point is distant from the urban seat, the reviewed Tibetan seat entries cite the coordinate entity in corrections/names.json.

The UK city selection is based on the [Cabinet Office List of cities](https://www.gov.uk/government/publications/list-of-cities/list-of-cities-html). Contains public sector information licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

National city registers and additional urban coordinates are credited in [official-data.md](licenses/official-data.md), including the U.S. Census Bureau, IBGE, Destatis, Japan MIC, Philippine Statistics Authority and GeoNames.

Local-government rosters and territorial place names added in 0.1.8 are documented in [the source register](licenses/single-city-review.md).

The 0.1.9 municipal review uses HCP census identifiers, GISCO 2024 geography and location points credited in [the source register](licenses/municipal-followup.md).

Localities and municipal equivalents added from 0.1.10 through 0.1.12 are credited in [the locality source register](licenses/search-localities.md).

Municipal registers, point sources and licenses for Albania, Armenia, Austria, Azerbaijan, Bahrain, Belarus, Belgium, Benin, Bhutan, Bosnia and Herzegovina, Botswana, Burundi, Cabo Verde, Cameroon, Chile, Christmas Island, Cocos (Keeling) Islands, Colombia, Comoros, Congo (Brazzaville), Costa Rica, Cyprus, Denmark, Djibouti, Dominican Republic, Ecuador, El Salvador, Equatorial Guinea, Eswatini, Gabon, Georgia, Greenland, Guernsey, Guyana, Iceland, Ireland, Jamaica, Jersey, Jordan, Kazakhstan, Kenya, Kiribati, Kyrgyzstan, Lesotho, Lithuania, Malawi, Malaysia, Mauritius, Moldova, Montenegro, Montserrat, Mozambique, Namibia, the Netherlands, New Zealand, Norfolk Island, North Macedonia, Norway, Oman, Paraguay, Portugal, Puerto Rico, Rwanda, Saint Lucia, Serbia, Sierra Leone, South Korea, Sri Lanka, Sweden, Tajikistan, Thailand, Timor-Leste, Togo, Trinidad and Tobago, Uganda, Uzbekistan, Vietnam, and Zimbabwe are listed in [the municipal source register](licenses/municipal-rosters.md).

Additional Chinese names and project transliterations added in 0.1.14 are described in [the Chinese name sources](licenses/chinese-place-names.md).

The 0.1.42 reviews of Cuba, Greece, Israel, Portugal, Tanzania, and Uruguay cite the national registers, coordinate providers, and municipal verification tables in [the municipal source register](licenses/municipal-rosters.md).

The 0.1.43 reviews of Haiti, Peru, and Turkmenistan cite national registers and coordinate sources in [the municipal source register](licenses/municipal-rosters.md).

The 0.1.44 reviews of Australia, South Africa, and Switzerland cite official municipal registers, boundary-derived points, and GeoNames in [the municipal source register](licenses/municipal-rosters.md).

The 0.1.45 reviews of Spain, Italy, and Mexico use the official INE and IGN, Istat, and INEGI registers, with source and point methods documented in [the municipal source register](licenses/municipal-rosters.md).

The 0.1.46 review of metropolitan France uses Insee's Code officiel géographique and Etalab's 2026 mairie point layer under Licence Ouverte 2.0. [Source details](licenses/municipal-rosters.md)

The 0.1.47 review credits Angola’s National Institute of Statistics for the Census Atlas, Bolivia’s INE, SDSN Bolivia and Laboratorio de Tecnologías Sociales for the municipal geodata (CC BY 4.0), and the Mongolian NSO and OCHA for the COD-AB reference (CC BY 3.0 IGO). Same-name settlement coordinates use GeoNames (CC BY 4.0). [Source details](licenses/municipal-rosters.md)

The 0.1.48 review uses U.S. Census Bureau TIGER/Line data for American Samoa, Ukraine’s 2026 KATOTTG and OpenStreetMap contributor coordinates cross-referenced by ua-geo (ODbL), and Venezuela INE boundaries from OCHA (CC BY 3.0 IGO). [Source details](licenses/municipal-rosters.md)

The 0.1.51 review credits the Tonga Statistics Department and Department of Lands, the Palau National Government, Suriname’s electoral secretariat, and Equatorial Guinea’s national statistical institute and government press office. Reference points use GeoNames, geoBoundaries, and OpenStreetMap contributors where indicated. [Source details](licenses/municipal-rosters.md)

The 0.1.50 review credits Nigeria’s Office of the Surveyor-General and Independent National Electoral Commission, Burkina Faso’s INSD and Institut Géographique du Burkina, and the Lao Statistics Bureau and National Geographic Department. Geographic points and boundaries provided through OCHA COD-AB are credited under [CC BY 3.0 IGO](https://creativecommons.org/licenses/by/3.0/igo/). [Source details](licenses/municipal-rosters.md)

The 0.1.49 review credits Argentina’s INDEC and Georef, Algeria’s national gazette and syscli’s MIT transcription ([license](licenses/syscli-algeria-MIT.txt)), and Julia Clark’s reference map of Tunisian municipalities. Boundaries from OpenStreetMap-derived layers are credited to OpenStreetMap contributors. [Source details](licenses/municipal-rosters.md)

The 0.1.52 review credits Senegal's ANSD and ONDDL, Vie-Publique and OrvLabs, Niger's INS and Ministry of the Interior, and the Turks and Caicos Islands Attorney General's Chambers. Point sources credit GeoNames, OpenStreetMap contributors, and OCHA's COD partners where indicated. See [source details](licenses/municipal-rosters.md).

The 0.1.53 review credits Statistics Canada, the relevant Canadian provincial governments, Côte d’Ivoire’s General Directorate of Taxes and Treasury, and Bhutan’s Ministry of Infrastructure and Transport and Election Commission. Representative points also use GeoNames and OpenStreetMap contributors. See [source details](licenses/municipal-rosters.md).

The 0.1.54 review credits the Sudanese Ministry of Justice and COD-AB contributors, the Parliament and Central Statistical Organization of Yemen, and Kuwait’s Ministry of Justice. Point attribution is recorded per place, including GeoNames, Overture Maps, and OCHA COD partners where indicated. See [source details](licenses/municipal-rosters.md).

The 0.1.55 review credits Mauritania’s ANSADE, Ministry of the Interior, GeoNames, Open Admin Data and CheikhEbeoumar/mauritania-geo, together with the Saint Kitts and Nevis Law Commission and the Nevis Island Administration. See [source details](licenses/municipal-rosters.md).

The 0.1.56 Myanmar roster credits the General Administration Department and the Myanmar Information Management Unit. The MIMU-sourced elements are available for noncommercial reuse with attribution under [MIMU terms](https://themimu.info/license/). Representative points also credit GeoNames and OpenStreetMap contributors as indicated in [the source register](licenses/municipal-rosters.md).

The 0.1.57 Madagascar review credits the Independent National Electoral Commission, the National Legislation Centre, BNGRC and OCHA for election and administrative reference data. Coordinates also credit GeoNames and OpenStreetMap contributors. See [source details](licenses/municipal-rosters.md).

The 0.1.58 Palestine review credits the Central Elections Commission, the Municipal Development and Lending Fund, and GeoNames. See [source details](licenses/municipal-rosters.md).

The 0.1.59 Guinea and Guinea-Bissau review credits the respective ministries, the national statistical agencies, OCHA COD partners, GeoNames, OpenStreetMap contributors, and the additional point references documented per row. See [source details](licenses/municipal-rosters.md).

The 0.1.60 Eritrea review credits the Eritrean ministries, the Central Region Administration, African Development Bank project materials, OCHA COD partners, and GeoNames. See [source details](licenses/municipal-rosters.md).

The 0.1.61 Korea (North) review credits the Korean national statistics office and Ministry of Unification, the administrative law collection published by the National Intelligence Service, GeoNames, and the Endonym Atlas. See [source details](licenses/municipal-rosters.md).

The 0.1.62 reviews credit the UAE federal and emirate governments, the Moroccan Haut-Commissariat au Plan and Interior Ministry, the Morocco Census crosswalk, GISCO, GeoNames and Wikidata. See [source details](licenses/municipal-rosters.md).

The 0.1.63 Central African Republic review credits ICASEES, the national elections authority, the U.S. Census Bureau, OCHA COD partners, MINUSCA, GeoNames and OpenStreetMap contributors. See [source details](licenses/municipal-rosters.md).

The 0.1.64 Türkiye review credits the Turkish Official Gazette and the Ministry of Environment, Urbanisation and Climate Change, the Ministry of Interior, OCHA COD partners, GeoNames and OpenStreetMap contributors. See [source details](licenses/municipal-rosters.md).

The 0.1.68 Libya review credits the Ministry of Local Government, Libya's High National Elections Commission, the Libyan Legal Archive, and OCHA's Libya COD partners. Representative coordinates credit GeoNames and OpenStreetMap contributors where indicated. See [source details](licenses/municipal-rosters.md).

The 0.1.69 Russia review credits the Bank of Russia publications of OKATO and OKTMO, the Federal Agency on Technical Regulating and Metrology, the Leningrad Oblast legislature, Kurskstat and GeoNames. See [source details](licenses/municipal-rosters.md).

The 0.1.70 Iran review credits the Statistical Centre of Iran, the public cabinet decisions where indicated, GeoNames, OpenStreetMap contributors and Wikidata. See [source details](licenses/municipal-rosters.md).

The 0.1.72 Lebanon review credits the Ministry of Interior and Municipalities, UNDP Lebanon, the Municipality of Tabarja and Kfaryassine, Lebanon's Central Administration of Statistics, OCHA, GeoNames and OpenStreetMap contributors. See [source details](licenses/municipal-rosters.md).

The 0.1.73 Somalia review credits the Somali Disaster Management Agency, OCHA, FAO SWALIM, GeoNames and OpenStreetMap contributors. See [source details](licenses/municipal-rosters.md).

The 0.1.74 Curaçao and Sint Maarten review credits their spatial planning ministries and Curaçao's Central Bureau of Statistics. See [source details](licenses/municipal-rosters.md).

The 0.1.75 Ethiopia review credits the Ethiopian Statistical Service, regional Bureaux of Finance and Economic Development, OCHA, GeoNames and the UNHCR map referenced by DIIS. See [source details](licenses/municipal-rosters.md).

The 0.1.76 Egypt review credits the Cabinet’s Information and Decision Support Center, CAPMAS, the New Urban Communities Authority, the Egyptian General Survey Authority, OCHA, GeoNames, and keltokhy/Egypt_NUCA’s transcription of the official city planning layer. See [source details](licenses/municipal-rosters.md).

The 0.1.77 Pakistan review credits the Pakistan Bureau of Statistics, Survey of Pakistan, Punjab and Balochistan local government departments, Khyber Pakhtunkhwa local government offices, the Azad Jammu and Kashmir Planning and Development Department, the Gilgit-Baltistan Election Commission, OCHA, GeoNames, and OpenStreetMap contributors. See [source details](licenses/municipal-rosters.md).

The 0.1.78 South Sudan review credits the National Audit Chamber, the National Bureau of Statistics, the Ministry of Finance and Planning, the National Elections Commission, Abyei and Warrap local administrations, OCHA, IOM, GeoNames, and OpenStreetMap contributors. See [source details](licenses/municipal-rosters.md).

The 0.1.80 India review credits the Ministry of Panchayati Raj, the National Informatics Centre (Bharatmaps), the Central Pollution Control Board, Ministry of Housing and Urban Affairs, Survey of India, India Post, the respective governments of Delhi, Telangana, Karnataka and Maharashtra, GeoNames, OpenStreetMap and Wikimedia contributors. See [source details](licenses/municipal-rosters.md).

The 0.1.81 partial review credits Mali's National Directorate of Territorial Planning, National Institute of Statistics, Ministry of Economy and Finance and Geographic Institute, Chad's General Secretariat of Government and INSEED, Liberia's Executive Mansion, Ministry of Local Government, LISGIS and the Liberia News Agency, and the OCHA, UNMEER, GeoNames and OpenStreetMap contributors named in the [source register](licenses/municipal-rosters.md).

The 0.1.82 partial review credits the Afghanistan National Portal and the government and UN-Habitat State of Afghan Cities project, Iraq's Basra Municipalities Directorate, Syria's published city-council decrees and local administration ministry, and OCHA and GeoNames for representative points. See [source details](licenses/municipal-rosters.md).

The 0.1.84 review credits Syria's Ministry of Local Administration and Environment for its published council appointment orders, the Syrian Official Gazette and SANA for later records, and OCHA and GeoNames for populated-place coordinates. Mali's added points were checked against its 2023 commune act and OCHA/IGM district boundaries. See [source details](licenses/municipal-rosters.md).
