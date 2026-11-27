# 世界城市名录覆盖核查

审查对象为独立包 `@winrisef/world-cities@0.1.0` 的实际 npm 安装包。核对日期为 2026-11-20。**中国大陆的省级和地级名录、英国本土的城市名录均逐项匹配。全球城市和一级行政区仍有明确漏项。** 原包中 19,323 / 19,521 条有中文名和拼音，这个比例只衡量已收录记录的字段覆盖。

## 按国家官方名录核对城市

“唯一匹配”要求该城市在正确的省州或对应行政区内能定位到一条记录。比对使用包内名称，并在有条件时用同一上游实体的当地文字名称识别异写。官方清单和包中记录数量的差给出了最低缺口。更名、译名和地区归属差异会影响名称匹配，不能把未匹配数直接作为漏收数。

| 地区及版本口径 | 官方记录 | 包内全部城市级记录 | 唯一匹配 | 有歧义 | 名称或归属未匹配 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 中国大陆，民政部公开行政区划树，地级单位加直辖市 | 337 | 337 | 337 | 0 | 0 |
| 英国本土，内阁办公室城市名录 | 76 | 76 | 76 | 0 | 0 |
| 巴西，IBGE 普通 município 的同名驻地 | 5,569 | 378 | 377 | 0 | 5,192 |
| 美国，2025 Gazetteer，50 州和华盛顿特区，LSAD 25 且 FUNCSTAT A/B | 10,223 | 6,810 | 6,688 | 6 | 3,529 |
| 德国，2024 年底具有城市权的 Gemeinden | 2,059 | 1,924 | 1,683 | 0 | 376 |
| 日本，2024-01-01 总务省地方公共团体代码表中的“市” | 792 | 744 | 742 | 0 | 50 |
| 菲律宾，PSA 149 市名录，按 PSGC 所属 region 核对 | 149 | 139 | 135 | 0 | 14 |

- 中国大陆按行政代码、中文名和上级省份逐条核对，293 个地级市、30 个自治州、7 个地区、3 个盟和 4 个直辖市均匹配。另用民政部 2024 年固定版复核，同一范围的代码和名称相符。西藏包含六市及阿里地区。[国家地名信息库](https://dmfw.mca.gov.cn/XzqhVersionPublish.html) · [民政部固定版](https://www.mca.gov.cn/mzsj/xzqh/2025/202401xzqh.html)
- 英国按英格兰、苏格兰、威尔士和北爱尔兰区分，同名 Bangor 的两条都在正确归属下。同一政府名录还列有王室属地和海外领地。百慕大的 Hamilton 已收录；马恩岛 Douglas、直布罗陀 Gibraltar、福克兰群岛 Stanley、圣赫勒拿 Jamestown 各自的地区文件均为空。[英国内阁办公室](https://www.gov.uk/government/publications/list-of-cities/list-of-cities-html)
- 巴西法律赋予 município 驻地城市地位，并规定驻地与 município 同名。IBGE 接口返回 5,571 条，核对普通市镇驻地时剔除 Brasília 和 Fernando de Noronha 两个特殊单位。5,569 个普通驻地中有 377 个能在同州匹配。上游已有朗多尼亚州 Cacoal（IBGE 1100049），其类型为 município，最终包中没有该市；马托格罗索州 2025 年设立的 Boa Esperança do Norte 也未收录。[巴西法令第 3 条](https://www.planalto.gov.br/ccivil_03/decreto-lei/1937-1946/del0311.htm) · [IBGE 行政区划](https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-mlhas.html) · [Cacoal](https://www.ibge.gov.br/cidades-e-estados/ro/cacoal.html) · [Boa Esperança do Norte](https://www.ibge.gov.br/cidades-e-estados/mt/boa-esperanca-do-norte.html)
- 美国仅使用 Census 法定类型为 city 且功能状态为 A/B 的记录。阿拉斯加州 Adak 在官方表有独立代码和坐标，安装包中最近的同国记录是约 709 公里外的 Unalaska。普查指定居民点、镇和村均未计入本表官方分母。[Census Gazetteer 2025](https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.2025.html) · [LSAD 类型](https://www.census.gov/library/reference/code-lists/legal-status-codes.html)
- 德国按州和城市名核对。官方 Marburg 在包中写作 Marburg an der Lahn，是 376 条自动未匹配记录中的一个已知别名。即使把别名全部对齐，包内全部记录仍比官方城市数少 135 条。[德国联邦统计局](https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Administrativ/05-staedte.html)
- 日本按都道府县和日本市名核对，排除了町、村及政令指定都市下辖的区。栃木县的那須塩原市在官方表和原始数据中都有，成品没有该记录。2025 年日本人口普查列出的 793 个统计单位将东京特别区部合计为一市，两份来源口径差一。[日本总务省团体代码](https://www.soumu.go.jp/denshijiti/code.html) · [2025 年国势调查](https://www.stat.go.jp/data/kokusei/2025/kekka/pdf/outline.pdf)
- 菲律宾核对官方清单中的十位 PSGC 代码、城市名和所属 region。PSA 2026 年第三季度的汇总仍为 149 市。该国的 82 个 province 与包中用作一级的 region 是两层，不能直接拿 82 和 18 相减。[PSA 城市名单](https://psa.gov.ph/classification/psgc/cities) · [PSGC 汇总](https://psa.gov.ph/classification/psgc/summary)

## 省州层

| 地区 | 核对结果 |
| --- | --- |
| 中国大陆 | 31 个省级行政区名称全部匹配，337 条城市级记录均归到相应省级单位。 |
| 巴西 | 26 州加联邦区共 27 项，州缩写和名称均匹配。 |
| 日本、德国、英国 | 日本 47 个都道府县代码、德国 16 个州代码、英国 4 个构成国名称均匹配。 |
| 法国 | INSEE 2026 年的 18 个 région 全部在包里。FR 分片还把法属波利尼西亚、新喀里多尼亚等 8 个其他类别的领地列在同一层；若用于“法国大区”筛选，结果会多 8 项。[INSEE 2026](https://www.insee.fr/fr/information/8740222) |
| 安哥拉 | 政府新制为 21 省，包内有 19 省。缺 Icolo e Bengo 和 Moxico Leste。[安哥拉政府](https://brasil.mirex.gov.ao/web/noticias/nova-divisao-politica-administrativa) |
| 布隆迪 | 总统府列五省，包内一级行政区为零，九条城市记录均没有省归属。上游仍是旧制 18 省，且未填写 level；现有构建规则过滤了这些记录。新制五省均需按政府名录建立。[布隆迪总统府](https://presidence.gov.bi/le-pays/) |

## 全球核查范围

- **国家和地区代码**。本次下载的联合国 M49 页面列出 248 个两位代码，在包内均有对应分片。此外包中有 TW 和 XK 两个分片。[联合国 M49](https://unstats.un.org/unsd/methodology/m49/overview/)
- **城市**。联合国《人口统计年鉴》2024 表 8 涵盖 203 个国家和地区，在 2005–2024 年各地可用的最近统计期列出首都及人口达十万的城市。共 4,141 条城市行，用同国公开英文名进行大小写、变音符号、标点和括号别名归一化筛查，2,280 条有唯一名称匹配，196 条有多个候选，1,665 条未命中名称。年鉴同时提供城区和都市圈口径，各地报送年份不同；这些数字只能用作待查线索。另有 47 个包内国家和地区缺少本表筛查依据。[联合国表 8 及说明](https://unstats.un.org/unsd/demographic-social/products/dyb/dyb_2024/)
- **一级行政区**。对照 geoBoundaries 汇集的联合国 SALB 元数据 32 份及人道主义边界元数据 142 份，去重覆盖 148 个国家或地区。SALB 的 32 份中有 22 份与包内数量相等，人道主义资料 142 份中有 88 份相等。部分资料早于行政改革。逐国结果保留来源机构和参考年份；只有国家官方新名录能支持具体的现行漏项判断。[联合国 SALB](https://salb.un.org/en) · [geoBoundaries 元数据与来源](https://www.geoboundaries.org/api.html)

## 数据与复核

[逐国结果](country-results.json) 列出全部 250 个包内分片及其有据可查的检查项。缺少检查字段表示该项未核实。[名称差异清单](name-review.json) 保留国家名录比对中需要复核的名称、归属和可获得的官方代码，同时列出联合国英文名筛查未命中项。[来源清单](sources.json) 记录下载地址及本次文件的 SHA-256。审查对象为 tarball 的公开城市记录；本地审查文件独立于 npm 分发内容。
