# 补充中文地名

0.1.14 为 60 个国家或地区的 512 个既有地点增加了中文名。以同一地点的公开中文译名为先，通过行政归属、原名、坐标或来源 ID 核对。其余 382 条采用项目音译或意译。逐条来源类型和身份编号见项目的 `audit/2026-11-21/chinese-place-names-0.1.14.csv`。

- 已有译名来自 CSC 同名居民点、Wikidata 结构化标签和 GeoNames 同名居民点，也参考了使领馆公开发布的地名。 [CSC 来源说明](SOURCES.txt) · [Wikidata CC0](https://www.wikidata.org/wiki/Wikidata:Licensing) · [GeoNames 许可](https://forum.geonames.org/about.html) · [中国驻厄瓜多尔大使馆省府译名](https://ec.china-embassy.gov.cn/lqfw/lsbdzjbgxx/201912/t20191211_4969485.htm)
- 阿尔巴尼亚市镇参考中国商务部和驻阿尔巴尼亚大使馆的区划译名，Dimal 使用项目音译。萨尔瓦多市镇中文名采用中国驻萨尔瓦多大使馆国别指南的省名，加上各自治市正式名称对应的方位。 [阿尔巴尼亚国别指南](https://www.mofcom.gov.cn/dl/gbdqzn/upload/aerbaniya.pdf) · [萨尔瓦多国别指南](https://sv.china-embassy.gov.cn/zsgx/jmhzdt/202510/P020251017214776018880.pdf)

- 巴哈马岛名参考公开国别指南。马绍尔群岛的埃内韦塔克、乌杰朗和夸贾林沿用联合国或中国外交部译名。 [巴哈马国别指南](https://jnfao.jining.gov.cn/module/download/downfile.jsp?classid=0&filename=76daada2b8794e2fad59426314e6c78c.pdf) · [联合国国际法委员会文件](https://digitallibrary.un.org/record/717847/files/ilc_2004_v2_p1ch.pdf) · [中国外交部马绍尔群岛国别资料](https://www.fmprc.gov.cn/web/gjhdq_676201/gj_676203/dyz_681240/1206_681492/1206x0_681494/)

- 0.1.39 按越南现行区划移出已撤销的富寿市社。富寿仍作为省名可检索，省政府驻地采用越池。 [越南现行区划名录](https://danhmuchanhchinh.nso.gov.vn/Lich_Su_Moi.aspx)

- **0.1.134**：补齐 678 条城市记录（美国 408、尼泊尔 254、西撒哈拉 16）的中文名及拼音，以及 92 条行政区/下属行政区记录的中文名或拼音。优先沿用数据库中已有的同名译法（不是相同实体官方译名的声明），缺少现成译法采用项目人工音译或意译；拼音由 `pinyin-pro` 在构建时生成。行政身份、ID、英文名及城市坐标不变。逐条方法见项目的 [城市补齐记录](../audit/2026-11-27/complete-city-labels-0.1.134.csv) 与 [行政区补齐记录](../audit/2026-11-27/complete-region-labels-0.1.134.csv)。
