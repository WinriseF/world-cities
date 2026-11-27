# 用 GADM 4.1 核对世界城市包 0.1.1

本次核查发现 **5 座漏收城市、6 条上级缺失、2 条上级错挂，以及 7 个需要调整的代表点**。共 20 条，均已用 GADM 以外的资料复核。候选记录仍有未定项。这里统计的是本次确认的问题，无法推算全球城市总缺口。核查对象是本地安装包，结果保存在本地审查文件中。

[完整的 20 条核实清单（含原记录 ID、独立来源、修订建议）](gadm-verified-findings.csv)

## 已核实的问题

- 印尼分片漏收 Subulussalam、Tidore Kepulauan、Baubau、Bitung 和 Sawahlunto。先从 GADM 标识为 Kota 的 97 个区域反查哪些没有包内点，再逐个检查名称、别名和印尼分片的全体记录，并查到印尼统计局分别发布的 2026 城市年鉴。第六个空间空白是坤甸 Pontianak，但包中已有该市，未计入漏项。[印尼统计局 Subulussalam 年鉴](https://subulussalamkota.bps.go.id/en/publication/2026/02/27/54cd636ef8dcfba93f166f46/kota-subulussalam-dalam-angka-2026.html) · [Bitung 年鉴](https://bitungkota.bps.go.id/id/publication/2026/02/27/1ddb0eb978376c6a0d7127c8/kota-bitung-dalam-angka-2026.html)
- 六条空归属有当地官方依据，且包内已有可关联的一级记录。布宜诺斯艾利斯关联同名自治市 AR-C，雅加达关联 ID-JK，基尔肯尼关联 IE-KK，加德满都关联巴格马蒂省 NP-P3，乌干达的托罗罗和卡塞塞分别关联 UG-212 和 UG-406。[布宜诺斯艾利斯市政府](https://buenosaires.gob.ar/gcaba_historico/justicia/elecciones-2025-en-la-ciudad/organizacion-politico-territorial) · [尼泊尔人口普查地图集](https://giwmscdnone.gov.np/media/pdf_upload/Population%20Atlas%20of%20Nepal_szjjvc5.pdf) · [卡塞塞区行政单位表](https://www.kasese.go.ug/admin-units/)
- 乌兰巴托被挂到蒙古国中央省 Töv，包内已有独立首都记录 MN-1。博茨瓦纳哈博罗内挂到 South-East，按统计局的分区和包内已有的城市区应归 BW-GA。两例的字段修正有独立依据。[蒙古国家统计局年鉴](https://downloads.1212.mn/Statistical_Yearkbook_2021_eng.pdf) · [博茨瓦纳人口普查分区表](https://statsbots.org.bw/sites/default/files/publications/2022%20Population%20and%20Housing%20Census%20Preliminary%20Results%20Aug.pdf)
- 孟加拉国贾马尔普尔的包内坐标是 25.0010825°N、89.2605013°E，已越过当地统计部门所列县域的西界。到 GeoNames 的同名行政驻地点约 70 公里，应该优先复核坐标。包中填写的迈门辛分区与官方人口普查一致。[当地统计部门](https://bbs.jamalpur.gov.bd/pages/static-pages/6970740ea31054345f1510c8) · [人口普查](https://nsds.bbs.gov.bd/storage/files/1/Publications/PHC_2021%20Community%20Report/MYMENSING%20DIVISION/Community%20Report%20Jamalpur.pdf) · [GeoNames 驻地点](https://www.geonames.org/1185106/jamalpur.html)
- 巴西 5,570 个代表点以 IBGE 官方代码连接到 **2025 年相应市界**后，5,564 个落在所属市内，6 个在外。六个是 Guaratinguetá、Nossa Senhora de Lourdes、Brasiléia、Balneário Piçarras、Ilhabela、Colônia Leopoldina。距离所属边界约 0.015–4.553 公里，清单中列出了各自经验证位于市内的 IBGE 驻地点。此前官方名录代码和州归属均已匹配，这次检出了代码检查覆盖不到的点位问题。[IBGE 2025 市界](https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2025/Brasil/) · [IBGE 居民地参考点](https://geoftp.ibge.gov.br/organizacao_do_territorio/estrutura_territorial/localidades/Localidades_do_Brasil/2022/)

## 全量空间核查

从 npm 压缩包读取全部 28,417 个城市代表点，用空间索引筛选候选多边形，解码 GeoPackage 原始几何，按点是否位于多边形内部或边界上进行精确判断。共 28,362 个点命中一个多边形，55 个没有命中。对后者另查约 5 公里邻域，53 个找到了同一国家分片对应的临近多边形。这批近邻只供诊断，未据此重分行政区。

| 一级归属比对的互斥结果 | 城市数 |
| --- | ---: |
| 已填归属与同国 ADM1 匹配 | 27,193 |
| 名称与同位置的其他层级或大区标签匹配 | 424 |
| 命中同国 ADM1，尚不能建立明确名称或代码对应 | 513 |
| 命中另一个已能对应的同国 ADM1 | 89 |
| 参考图层代码和城市区、州的命名口径冲突，隔离复核 | 67 |
| 国家或地区的图层编码与包的分片不同 | 27 |
| 同国命中但当前位置无 ADM1 | 1 |
| 已填归属但没有命中多边形 | 51 |
| 包中上级为 null | 52 |
| 合计 | 28,417 |

一级匹配采用地区代码、名称、当地文字和别名的唯一对应，结合 ISO 地区名称及捷克、匈牙利等地的行政后缀。67 条涉及俄罗斯同名城市和环绕它的州，参考数据中的 Moscow City、Moskva、区域类型及代码存在冲突，未拿该代码覆盖包内数据。89 条不同 ADM1 中有 36 条在约 5 公里内能找到期望地区的多边形。一级匹配只检验这个点的省州归属；一个落在本省其他城市的点也可能通过。

52 条空归属逐条分流。42 个点落在有一级名称的多边形内，6 个落在没有一级名称的多边形内，4 个没有命中多边形。根据包的建模和独立资料，其中 6 条已有可补的父级，5 条属于项目已约定的城市型地区，8 条是乌干达在 2020 年调整建制的城市，6 条须区分马拉维的城市议会与区议会，其余 27 条继续核实当地层级或坐标。行政边界覆盖和行政隶属分开判断。[乌干达议会](https://cmis.parliament.go.ug/cmis/views/f8cb1842-1871-4fe4-8b18-421871bfe440%253B1.0) · [马拉维地方政府](https://nlgfc.localgov.gov.mw/index.php/entertainment/city-councils)

## 版本差异和城市覆盖

- 中国大陆 337 条中，335 个坐标在文件中匹配预期省级行政区。厦门点没有命中陆地多边形，距文件中福建边界约 1.33 公里；三沙所在海域使用另一分区编码。地级层面有 328 条直接匹配名称，其余包含区划变化、旧名称和点位待查项。例如 GADM 仍使用襄樊的拼写，现名襄阳成立。中国现行行政名录继续以民政部为准。[湖北省政府资料](https://mzw.hubei.gov.cn/ztzl/dzh/jcdzh/202311/t20231115_4946451.shtml) · [民政部地名信息库](https://dmfw.mca.gov.cn/XzqhVersionPublish.html)
- 巴西有 12 个点未通过 GADM 市级代码比对。用现行 IBGE 边界复核后，其中 7 个在所属市内，包括 2025 年正式设立的 Boa Esperança do Norte。另有 1 个点通过了 GADM 比对，却落在现行 IBGE 所属市界之外。[IBGE 新设城市资料](https://www.ibge.gov.br/cidades-e-estados/mt/boa-esperanca-do-norte.html)
- 做了全球一级目录的双向对照。GADM 文件有 3,661 个非空一级几何单元，2,987 个与包内一级记录建立了唯一对应。两套目录中仅一方出现或无法唯一对应的名称，既可能是覆盖缺口，也可能是层级、译名或年代差异。布隆迪在该文件中仍有 17 个一级单元，而现行官方建制为 5 省；安哥拉文件中的 18 个也早于现行 21 省。[布隆迪总统府](https://presidence.gov.bi/le-pays/) · [安哥拉政府](https://brasil.mirex.gov.ao/web/noticias/nova-divisao-politica-administrativa)
- 日本、菲律宾也做了按城市型多边形的反向筛查，分别有 12 和 7 个此类旧多边形没有命中同国包内城市点。空多边形不等同于漏收，例如浦安市已在日本分片。全球未逐国建立每种市制与 GADM 层级的一一关系。

## 输入与明细

核查读取下载目录中的 GADM 4.1 全球 ZIP，大小为 1,466,771,821 字节，包含单个 GeoPackage，几何层有 356,508 条 EPSG:4326 多面要素。压缩包 SHA-256 为 `4eb416375d9352654bb55f205cc710db3f0568503011724971be7eb6b4cc861c`。世界城市 0.1.1 安装包 SHA-256 为 `ae0cfec92d10eab70c360b2b72adfb9f898c8a9d838bda029e75c7a51e980b5d`。

本地的全部坐标结果、52 条空归属分流、逐国汇总和巴西官方边界复核保存在项目的 `.cache/gadm-check/`。归属候选与几何属性仅作本地审查，未随 npm 包分发。[GADM 元数据](https://gadm.org/metadata.html) · [GADM 许可](https://gadm.org/license.html)
