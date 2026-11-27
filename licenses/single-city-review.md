# 单条城市分片核验

以 0.1.7 的国家索引和发布包为基线。逐项数据、地点标识与坐标来源见[历史核验记录](https://github.com/WinriseF/world-cities/tree/9ee4670ec4ae32016611c0283efc6033fe15522c/audit/2026-11-21/single-city-review)。不同国家按各自的城市法、市镇法、地方议会名录或统计局登记核对。partial 表示仅能证实表中列出的范围。

已有地点尽量沿用原 ID。荷兰加勒比区过去只列 Bonaire 的村庄 Rincon，本版用三个法定公共实体的驻地取代该记录。密克罗尼西亚的联邦首都和马绍尔群岛的首都人口中心分别保留；相应自治单位各按一个建制计。

地理坐标使用名录中心点、经核对的既有点或 GeoNames 地名点；找不到界内同名居民点时使用行政区面内的代表点。此类点无需位于首府建筑物。法罗群岛市镇代码与财政表匹配。法语公社代码采用 INSEE，马耳他地方议会匹配 Eurostat/GISCO LAU。中文名采用已匹配实体的名称，未确认译名留空。GeoNames 使用 CC BY 4.0，Wikidata 结构化数据使用 CC0；各行政名录的来源见下表。

| 国家或地区 | 包内地点数 | 核对范围 | 资料 |
| --- | ---: | --- | --- |
| AD · 安道尔 | 1 → 7 | 宪法列名、有独立公社的七个堂区 | [来源1](https://portaljuridicandorra.ad/CONSTITUCIO) |
| AG · 安提瓜和巴布达 | 1 → 2 | 首都圣约翰及《巴布达地方政府法》规定的巴布达议会驻地。其余历史城镇的现行法律身份待核 | [来源1](https://laws.gov.ag/wp-content/uploads/2018/08/cap-44.pdf) |
| AW · 阿鲁巴 | 1 → 2 | 空间规划认定的奥拉涅斯塔德和圣尼古拉斯两个城市中心，全国法定市名录待核 | [来源1](https://www.gobierno.aw/nl/planbeschrijving) |
| AX · 奥兰群岛 | 1 → 16 | 芬兰统计局 2026 年市镇与地区对照表中地区 21 的全部自治市镇，含玛丽港 | [来源1](https://stat.fi/en/luokitukset/corrmaps/kunta_1_20260101%23maakunta_1_20260101) |
| BB · 巴巴多斯 | 1 → 4 | 国土空间规划中的四个传统城市中心。规划区与独立市级建制尚需区别 | [来源1](https://www.barbadosparliament.com/uploads/sittings/attachments/76f2d5d8bea25a42c0ba99a91dc5fe04.pdf) |
| BM · 百慕大 | 1 → 2 | 百慕大政府登记的两座建制市镇 Hamilton 和 St. George’s | [来源1](https://www.gov.bm/department/municipalities) |
| BN · 文莱 | 1 → 4 | 内政部市政机构管辖的城市；包括由同一市政机构管理的 Kuala Belait 和 Seria。Muara 和 Bangar 有城镇地名，未列入市政机构辖区名录 | [来源1](https://www.gov.bn/directory_moha/) |
| BQ · 博内尔岛、圣尤斯特歇斯和萨巴岛 | 1 → 3 | 三个加勒比公共实体，各用驻地为代表点，实体名称可用于检索 | [来源1](https://www.government.nl/themes/government-and-democracy/caribbean-parts-of-the-kingdom/governance-of-bonaire-st-eustatius-and-saba) |
| BS · 巴哈马 | 1 → 34 | 《2024 年地方政府法》第二、三附表列出的 33 个区议会，包括 Freeport。首都 Nassau 另计一条 | [来源1](https://laws.bahamas.gov.bs/cms/images/LEGISLATION/PRINCIPAL/2024/2024-0059/2024-0059_1.pdf)、[来源2](https://opm.gov.bs/prime-minister-davis-national-address-tribunal-gbpa-arbitration/) |
| DM · 多米尼加 | 1 → 3 | 社区发展部现列的城市、镇及都市区议会，排除村议会和原住民领地 | [来源1](https://communitydevelopment.gov.dm/dominica-s-local-government-system) |
| EH · 西撒哈拉 | 1 → 6 | 高等计划委员会区域资料中位于该地理分片的六个城市公社，包括拉古伊拉历史居民点。所属分片按地理范围核对 | [来源1](https://www.hcp.ma/region-eddakhla/attachment/2806162/)、[来源2](https://www.hcp.ma/region-laayoune/attachment/2800161/) |
| FK · 福克兰群岛 | 1 → 1 | 英国内阁办公室授予城市地位的 Stanley | [来源1](https://www.gov.uk/government/publications/list-of-cities/list-of-cities-html) |
| FM · 密克罗尼西亚 | 1 → 77 | 四州自治市镇。普查界线含七十五个，联邦政府另列无常住人口的 Sorol。另保留联邦首都 Palikir | [来源1](https://stats.gov.fm/wp-content/uploads/2023/12/2010-Summary-Analysis-Key-Indicators.pdf)、[来源2](https://personnel.gov.fm/yap-government/)、[来源3](https://personnel.gov.fm/chuuk-government/)、[来源4](https://personnel.gov.fm/pohnpei-government/)、[来源5](https://personnel.gov.fm/kosrae-government/)、[来源6](https://data.humdata.org/dataset/dc71c13f-e848-4ddc-9074-17e608464b63/resource/cb470018-7524-4487-9596-3807a83ac9cb/download/fsm_adm_gazeteer.xls)、[来源7](https://data.humdata.org/dataset/dc71c13f-e848-4ddc-9074-17e608464b63/resource/7348d022-6726-438c-9b1c-0b5524b7dbfd/download/fsm_admbnda_shp.zip) |
| FO · 法罗群岛 | 1 → 29 | 统计局全国市镇维度，按市镇名称、议会目录和市镇代码核对 | [来源1](https://statbank.hagstova.fo/api/v1/en/H2/IB/IB01/fo_midalal.px)、[来源2](https://www.kommunan.fo/) |
| GD · 格林纳达 | 1 → 7 | 《城镇边界法》列名的七个城镇 | [来源1](https://grenadaparliament.gd/wp-content/uploads/2021/08/Cap323-TOWNS-BOUNDARIES-ACT.pdf) |
| GF · 法属圭亚那 | 0 → 22 | 法国政府地理 API 返回的法属圭亚那全部二十二个公社；采用 INSEE 代码及公社代表点 | [来源1](https://geo.api.gouv.fr/departements/973/communes?fields=nom,code,centre) |
| GI · 直布罗陀 | 1 → 1 | 英国内阁办公室授予城市地位的 Gibraltar | [来源1](https://www.gov.uk/government/publications/list-of-cities/list-of-cities-html) |
| GM · 冈比亚 | 1 → 2 | 地方选举委员会和国家发展计划列出的 City Council 和 Municipal Council。普通 Area Council 属区域政府 | [来源1](https://iec.gm/election/local-government-elections/)、[来源2](https://gambia.gov.gm/government-directory/) |
| GU · 关岛 | 1 → 19 | 市长委员会十九个市级建制，联名村镇按一个市镇计 | [来源1](https://mcog.guam.gov/villages-list)、[来源2](https://www2.census.gov/geo/tiger/TIGER2025/COUSUB/tl_2025_66_cousub.zip) |
| IM · 马恩岛 | 1 → 21 | 选举机关登记的全部 21 个同级地方政府，其中包含合并后的 Garff、Arbory and Rushen | [来源1](https://elections.gov.im/local-authority-elections/)、[来源2](https://www.douglas.gov.im/~documents/route%3A/download/331/) |
| KN · 圣基茨和尼维斯 | 1 → 5 | 政府、选举法及道路法可辨认的城市、城镇；所据文件未给出全国同级城镇的闭合名录 | [来源1](https://www.gov.kn/about-st-kitts-and-nevis/)、[来源2](https://lawcommission.gov.kn/wp-content/documents/Revised-Acts-of-St-Kitts-and-Nevis/Revised-Acts-of-St-Kitts-and-Nevis-2020/Ch-02_01-National-Assembly-Elections-Act.pdf)、[来源3](https://lawcommission.gov.kn/wp-content/documents/Act02and09TOC/Ch-15_05-Roads-Act.pdf) |
| KW · 科威特 | 1 → 1 | 市政法设全国统一的科威特市政机构，保留科威特城。其他住宅新城的法定地位待核 | [来源1](https://pp.moj.gov.kw/ar/LawsPP/KuwaitMunicipalityLaw.pdf)、[来源2](https://unhabitat.org/sites/default/files/documents/2019-08/national-report-asia-pacific-kuwait-final-in-english.pdf) |
| KY · 开曼群岛 | 1 → 1 | 保留首府乔治敦。开曼宪法委员会列出的区咨询委员会未作为城市计入 | [来源1](https://www.constitutionalcommission.ky/upimages/publicationdoc/Enclosure1-ConstitutionalCommissionConclusionsandRecommendationsonAdvisoryDistrictCouncils_151021_1643925864_1643925864.pdf)、[来源2](https://otp.gov.ky/web/govky/ourislands) |
| LI · 列支敦士登 | 1 → 11 | 宪法列举的十一个 Gemeinde | [来源1](https://www.regierung.li/files/attachments/101-05-02-2021-en.pdf) |
| LV · 拉脱维亚 | 1 → 82 | 国家地址登记簿城市文件中 STATUSS 为 EKS 的现行 pilsēta，使用 KODS 识别 | [来源1](https://data.gov.lv/dati/dataset/6b06a7e8-dedf-4705-a47b-2a7c51177473/resource/ee02baa4-2bc3-4f77-a6cb-5427a3e9befe/download/aw_pilseta.csv)、[来源2](https://data.gov.lv/dati/api/3/action/resource_show?id=ee02baa4-2bc3-4f77-a6cb-5427a3e9befe) |
| MC · 摩纳哥 | 1 → 1 | 宪法第七十八条规定全境构成单一公社 | [来源1](https://journaldemonaco.gouv.mc/Journaux/2002/Journal-7542/Constitution-du-17-decembre-1962-revisee-par-la-loi-n-1.249-du-2-avril-2002) |
| MH · 马绍尔群岛 | 1 → 25 | 地方政府宪章及审计名录。Kili/Bikini/Ejit 合计一个地方政府；首都人口中心与 Majuro 自治范围分列 | [来源1](https://rmicourts.org/constitutions-of-the-local-governments-of-the-republic-of-the-marshall-islands/)、[来源2](https://www.rmioag.com/local-governments/)、[来源3](https://data.humdata.org/dataset/c215706c-9c22-43ca-8d36-9de4726eb9e0/resource/f7db4038-975c-4a18-a3aa-0ae5aa6fa6e7/download/mhl_admgz.xls)、[来源4](https://data.humdata.org/dataset/c215706c-9c22-43ca-8d36-9de4726eb9e0/resource/383a9368-998f-4657-a380-6323bb827296/download/mhl_admbnda_wgs84_ab_shp.zip) |
| MT · 马耳他 | 1 → 68 | 地址登记机关列明的所有地方议会，按区域及欧盟 LAU 单元代码区分重名市镇 | [来源1](https://address.gov.mt/local-council/)、[来源2](https://gisco-services.ec.europa.eu/distribution/v2/lau/geojson/LAU_RG_01M_2024_4326.geojson) |
| MV · 马尔代夫 | 1 → 5 | 地方政府管理局登记的五个 City Council，排除岛议会 | [来源1](https://www.lga.gov.mv/en/councils?type%5Bcount%5D=5&type%5Bid%5D=city-council&type%5Bname%5D=City+Council) |
| NC · 新喀里多尼亚 | 1 → 33 | 新喀里多尼亚政府的全国公社目录，Poya 跨省，区域字段按驻地选北部省 | [来源1](https://nouvelle-caledonie.opendatasoft.com/api/explore/v2.1/catalog/datasets/communes-nc/records?limit=100) |
| NI · 尼加拉瓜 | 1 → 153 | INETER 市镇界线逐项对照唯一市镇代码与一级行政区 | [来源1](https://mapserveride.ineter.gob.ni/geoserver/wsINETER-DGGC/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=wsINETER-DGGC%3ALim_Municipal&outputFormat=application%2Fjson&srsName=EPSG%3A4326)、[来源2](https://mapserveride.ineter.gob.ni/geoserver/wsINETER-DGGC/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName=wsINETER-DGGC%3ALim_Departamental&outputFormat=application%2Fjson&srsName=EPSG%3A4326) |
| NR · 瑙鲁 | 1 → 1 | 保留政府机构所在地亚伦。十四个区尚无可对应本库口径的全国市级名录 | [来源1](https://naoero.gov.nr/parliament-of-naoero/about-parliament/how-was-parliament-established/) |
| PM · 圣皮埃尔和密克隆 | 0 → 2 | 法国政府地理 API 返回的圣皮埃尔和密克隆两个公社；采用 INSEE 代码及公社代表点 | [来源1](https://geo.api.gouv.fr/communes?codeDepartement=975&fields=nom,code,centre) |
| PW · 帕劳 | 1 → 2 | 前首都科罗尔及国家政府所在地恩吉鲁穆德；帕劳各州的建制另计 | [来源1](https://www.palaugov.pw/who-we-are/) |
| QA · 卡塔尔 | 1 → 8 | 国家总体规划登记的八个自治市 | [来源1](https://www.mme.gov.qa/QatarMasterPlan/English/MSDP-Municipalities.aspx?panel=about) |
| SB · 所罗门群岛 | 1 → 1 | 地方政府部门所列九省以外独立设立的霍尼亚拉市政委员会 | [来源1](https://mpgis.gov.sb/provincial-governments.html) |
| SC · 塞舌尔 | 1 → 1 | 核对有市长建制的维多利亚。其他法定同级单位仍待核 | [来源1](https://statehouse.gov.sc/news/6819/appointment-of-mrs-josy-ita-michaud-payet-as-mayor-of-victoria) |
| SG · 新加坡 | 1 → 1 | 城市国家新加坡；市镇理事会负责组屋区管理 | [来源1](https://www.mnd.gov.sg/our-work/regulating-town-councils) |
| SH · 圣赫勒拿 | 1 → 1 | 英国内阁办公室授予城市地位的 Jamestown；海外领地包括圣赫勒拿、阿森松和特里斯坦-达库尼亚 | [来源1](https://www.gov.uk/government/publications/list-of-cities/list-of-cities-html) |
| SM · 圣马力诺 | 1 → 9 | 内政部门列名的九个 castelli | [来源1](https://www.interni.sm/pub2/InterniSM/Giunte-di-Castello/Le-Giunte-di-Castello.html) |
| SR · 苏里南 | 1 → 2 | 官方空间规划及政府资料确认的帕拉马里博和新尼克里。其余城镇的法定层级待核 | [来源1](https://gov.sr/wp-content/uploads/2024/09/Structuurvisie-voor-de-Ruimtelijke-Ontwikkeling-van-Suriname.pdf)、[来源2](https://gov.sr/wp-content/uploads/2022/11/Telesur-Jaarrekening-2016.pdf) |
| ST · 圣多美和普林西比 | 1 → 7 | 国家统计局居民点普查中称作 cidade 的六个区首府与普林西比区域首府 | [来源1](https://www.ine.st/phocadownload/userupload/Documentos/DADOS_LOCALIDADE_PROJECOES/Publica%C3%A7%C3%A3o%20dos%20Resultados%20sobre%20Localidades%20-%20IV%20RGPH%202012.pdf) |
| TO · 汤加 | 1 → 3 | 《城镇规例法》明确提及的努库阿洛法、内亚富、庞艾。该条覆盖范围不足以确定全国应收总数 | [来源1](https://faolex.fao.org/docs/pdf/ton74776.pdf) |
| TV · 图瓦卢 | 1 → 8 | 《Falekaupule 法》及地方政府名录中的八个岛级自治议会 | [来源1](https://tuvalu-legislation.tv/cms/images/LEGISLATION/PRINCIPAL/1997/1997-0008/FalekaupuleAct_1.pdf)、[来源2](https://www.clgf.org.uk/default/assets/File/Country_profiles/Tuvalu.pdf) |
| VA · 梵蒂冈 | 1 → 1 | 梵蒂冈城国全境对应一个城市代表点 | [来源1](https://www.vaticanstate.va/en/state-and-government/general-informations/geography.html) |
| VC · 圣文森特和格林纳丁斯 | 1 → 6 | 土地税法附表列名的圣文森特主岛六个镇。格林纳丁斯群岛另核 | [来源1](https://ird.gov.vc/images/pdf/Cap438.pdf) |
| VI · 维尔京群岛（美国） | 1 → 3 | 美国人口普查局确认的三个建制镇；排除普查指定人口点 | [来源1](https://www.census.gov/programs-surveys/geography/about/glossary.html)、[来源2](https://www2.census.gov/geo/tiger/TIGER2025/PLACE/tl_2025_78_place.zip) |
| VU · 瓦努阿图 | 1 → 3 | 城市事务和规划部门现行名录中的三个市议会 | [来源1](https://duap.gov.vu/index.php/what-we-do/municipalities) |
| WF · 瓦利斯群岛和富图纳群岛 | 1 → 3 | 瓦利斯和富图纳组织法设立的三个有法人资格的行政区，各取一个代表点 | [来源1](https://www.legifrance.gouv.fr/codes/section_lc/JORFTEXT000000684031/LEGISCTA000006087719/) |
| WS · 萨摩亚 | 1 → 1 | 萨摩亚政府环境现状报告认定的城市中心 Apia。村庄属于下一级 | [来源1](https://www.mnre.gov.ws/wp-content/uploads/2024/09/Final-Samoa-SOE-2023-v39-digital-1.pdf) |
| XK · 科索沃 | 1 → 38 | 地方政府部登记的三十八个市镇，以行政区识别同名地点 | [来源1](https://mapl.rks-gov.net/en/municipal-portal/)、[来源2](https://askapi.rks-gov.net/Custom/c42a79d8-f7b8-4a28-ab0a-31a9f96665c7.pdf) |
| YT · 马约特 | 1 → 17 | 法国政府地理 API 中马约特的全部公社，使用 INSEE 代码及公社中心点 | [来源1](https://geo.api.gouv.fr/departements/976/communes?fields=nom,code,centre) |
