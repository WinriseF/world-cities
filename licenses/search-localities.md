# 搜索地点来源

## 0.1.10 科威特

名称、所属省与代表点来自 [Overture Maps Divisions](https://docs.overturemaps.org/guides/divisions/) 2026-11-18.0（© OpenStreetMap contributors 等，ODbL 1.0）。位置和拼写交叉核对使用 [Who’s On First 科威特分片](https://data.geocode.earth/wof/dist/parquet/whosonfirst-data-admin-kw-latest.parquet)；[WOF 来源和署名](https://whosonfirst.org/docs/licenses/)。艾哈迈迪中文名参照 Wikidata Q980396（CC0），杰赫拉保留繁简异写。Sabah Al-Ahmad 由[科威特住房部门](https://www.pahw.gov.kw/Sabah-Alhmad_en)列为住宅新城。

| 地点 | Overture GERS ID | WOF locality ID | Wikidata |
| --- | --- | --- | --- |
| Ahmadi | 85b2dbc5-0ffe-434e-8313-ef8c0d6212f5 | 421190381 | Q980396 |
| Al Jahra | a29c3749-4829-414d-96bf-c6bc8c71e848 | 890439989 | Q1077024 |
| Sabah Al-Ahmad | 83ac7638-a19b-4e4e-bd52-078e3648c821 | 1729724885 | — |

## 0.1.11 地区代表点与自治单位

各地建制和政府驻地的官方依据见 data/coverage.json 中的 cityReference。美属萨摩亚一级地区采用[美国人口普查局名录](https://tigerweb.geo.census.gov/tigerwebmain/Files/tab20/tigerweb_tab20_county_2020_as.html)。蒙特塞拉特的三个堂区采用[英国地名委员会资料](https://assets.publishing.service.gov.uk/media/69b1718558d4ef5adaf0e46a/UK_Overseas_Territories_Information_paper.pdf)。

Overture Divisions 使用 2026-11-18.0 的 Point 几何，包含 © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright)（ODbL 1.0）与 [Esri Community Maps](https://doc.arcgis.com/en/community-maps/)（CC BY 4.0）资料。WOF locality ID 对应的位置供交叉核对。Wikidata 结构化资料使用 CC0。

| 分片 | 代表点 | Overture GERS ID | WOF locality ID | Wikidata |
| --- | --- | --- | --- | --- |
| AI | The Valley | 24213396-42ec-4949-b9e2-d608501ea105 | 890441875 | Q30994 |
| AS | Pago Pago | 19b61a55-fe71-497c-853b-9e8393a0b0f4 | — | Q51678 |
| BL | Gustavia | 2d2139e7-f65b-4fa8-95b0-657a89b4019f | 421201293 | Q34112 |
| CK | Avarua | c893c7ec-791b-4d86-9091-a86aac274ee8 | 1125943171 | Q170482 |
| CW | Willemstad | d82ca597-2490-4287-902a-2b4a70f1d826 | 421187435 | Q132679 |
| CX | Flying Fish Cove | 6e2a4373-7fe4-42db-9694-deb395c53523 | 890440049 | Q30980 |
| GG | St Peter Port | 047e8436-2d61-4de9-81b2-fda758cfd7b2 | 1125821075 | Q174262 |
| MF | Marigot | 80ea4f40-5e19-4f09-a3dc-f66b623fe575 | 890434943 | Q200605 |
| MP | Capitol Hill | e69c1724-3304-4a88-b349-666f2a8d8ac4 | 1141908371 | Q3273113 |
| MS | Brades | 495de63c-b07c-4561-abca-83f829bfed62 | 1125778197 | Q31006 |
| NF | Kingston | f063a844-dac7-42cc-8b52-ab20f10623c1 | 890440179 | Q30963 |
| NU | Alofi | c91c8f54-0d12-4f2a-aefb-db8c75404015 | 1125943189 | Q30966 |
| PN | Adamstown | f8ea4133-f2cf-460c-802c-42ad310e829d | 890440159 | Q48273 |
| SJ | Longyearbyen | 69ddc39b-0cda-49e4-8f69-59824efdf840 | 890442521 | Q25923 |
| SX | Philipsburg | 27225ef5-7e4b-4291-8e3a-50d30108d998 | 890434823 | Q30958 |
| TC | Cockburn Town | 0b06fcab-0671-424b-a5e5-215950d5b2e0 | 890440113 | Q34205 |
| TK | Atafu | 3c52a4e8-a483-4eb7-a687-5c4de9da85d2 | — | Q642787 |
| TK | Fakaofo | 529d62e4-af98-4cc1-bac1-b70ec8f8d166 | — | Q650847 |
| TK | Nukunonu | 4b56babe-cc25-45aa-a496-c75c037b9447 | 1209325079 | Q656709 |
| VG | Road Town | b7f22385-02a3-426e-8c38-466faab1884e | 890434937 | Q179431 |

西岛代表点采用 [Wikidata Q48675](https://www.wikidata.org/wiki/Q48675)，行政中心由澳大利亚国会报告确认。
北马里亚纳四个自治单位采用人口普查 GEOID 69085、69100、69110、69120。塞班代表点位于 Capitol Hill，其他三个采用[美国人口普查局公布的内部点](https://tigerweb.geo.census.gov/tigerwebmain/Files/bas26/tigerweb_bas26_county_2020_tab20_mp.html)。

## 0.1.12 公社及同级自治名录

- 瓜德罗普、马提尼克、留尼汪与法属波利尼西亚的 138 个公社逐条匹配 INSEE 2026 年地理编码。前三个地区取法国 API Geo 的公所代表点。来源包含 INSEE、IGN 和 Etalab 开放地理数据，查询日期为 2026-11-21。 [INSEE 2026 COG](https://www.insee.fr/fr/information/8740222) · [API Geo 数据说明](https://www.data.gouv.fr/dataservices/api-decoupage-administratif-api-geo)
- 法属波利尼西亚 48 个公社采用当地土地事务部门 DAF 地籍测绘处发布的驻地坐标，并与公社轮廓和五个行政分区配对。原始测绘地名图层采用 Etalab Licence Ouverte 2.0。公社的驻地名称也可用于搜索。 [Tefenua BD Carto](https://www.arcgis.com/home/item.html?id=2d483b3bc0f7490a828f3c751dd1c876) · [行政分区法令](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000811386/2026-05-06)
- 斐济依据议会列出的 13 个市镇议会，伯利兹依据主管部门与镇议会法列出的 9 个市镇议会。斐济使用 Overture 点几何，其中 Tavua 采用 GeoNames 2197895。伯利兹 Orange Walk Town 采用 GeoNames 3581514。GeoNames 数据采用 CC BY 4.0。 [斐济议会记录](https://www.parliament.gov.fj/wp-content/uploads/2026/10/Daily-Hansard-Tuesday-29th-September-2026-1.pdf) · [伯利兹官方名录](https://www.ruraltransformation.gov.bz/the-ministry/local-government/town-and-city-councils-of-belize/) · [GeoNames 署名与许可](https://forum.geonames.org/about.html)
- 库克群岛按总理办公室列出的 10 个外岛自治政府收录。代表点来自 Overture 2026-11-18.0，Palmerston 和 Rakahanga 分别采用 GeoNames 4036432 和 11876846。Pukapuka 与 Nassau 共用一个自治政府。 [总理办公室名录](https://www.pmoffice.gov.ck/our-work/pa-enua/)
- 纽埃按《2016 年村议会法》和政府名录收录 14 个地方议会。代表点来自 Overture 2026-11-18.0 或 Pacific Data Hub 发布的村界内部点。geoBoundaries 镜像的村界使用 CC BY 4.0。库克群岛与纽埃均保留原有首都代表点。 [纽埃政府](https://www.gov.nu/government) · [Pacific Data Hub 村界](https://pacificdata.org/data/dataset/2011_niu_phc_admin_boundaries)
- 卢森堡按国家统计局公布的 12 个法定城市核对，补入 Esch-sur-Alzette、Remich 和 Vianden。代表点与州归属采用 CSC 已锁定版本。 [国家统计局名录](https://statistiques.public.lu/dam-assets/fr/publications/thematique/population-emploi/recueil-communes/recueil-communes.pdf) · [议会答复](https://www.chd.lu/en/question/30314)
- 中文搜索名保留已有译名，并补充 Wikidata 的中文名、Who’s On First 中可核对的常用异写和少量按官方地名的音译。 [Wikidata CC0](https://www.wikidata.org/wiki/Wikidata:Licensing) · [WOF 许可](https://whosonfirst.org/docs/licenses/)
