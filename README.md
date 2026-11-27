# @winrisef/world-cities

全球国家、行政区及城市地名数据库，支持中文、英文、拼音检索，提供 WGS84 经纬度。数据按地区拆分为 JSON，可按需加载，无运行时依赖。

本数据库的行政区划名录几乎全部以各国官方相关资料为依据，结合其他公开地理资料进行交叉核验与缺失信息补充，并统一整理数据格式、名称及经纬度。

## 数据概况

| 内容 | 数量 |
| --- | ---: |
| 国家和地区 | 247 |
| 一级行政区 | 3,814 |
| 城市及同级单位、代表地点 | 122,061 |
| 城市中英文及拼音覆盖率 | 100% |

229 个国家和地区按法定名录核验，5 个按主要城市优先收录，13 个不适用市级建制口径。各国具体范围见 [数据覆盖](COVERAGE.md)。无通行中文译名的地点采用项目音译或意译。

## 安装

```sh
npm install @winrisef/world-cities
```

## 使用

Node.js 中读取指定国家和地区的数据：

```js
import { readFile } from 'node:fs/promises'
import { countries, countryFiles } from '@winrisef/world-cities'

const { regions, cities } = countryFiles('CN')
const read = async url => JSON.parse(await readFile(url, 'utf8'))
const [provinceList, cityList] = await Promise.all([read(regions), read(cities)])
const search = 'lasa'
const results = cityList.filter(city =>
  [city.zh, city.en, city.pinyin, ...(city.aliases ?? [])]
    .some(name => name?.toLowerCase().replaceAll(' ', '').includes(search))
)
```

浏览器可直接请求部署后的 JSON，无需引入库：

```js
const base = '/data'
const countries = await fetch(`${base}/countries.json`).then(r => r.json())
const cities = await fetch(`${base}/cities/CN.json`).then(r => r.json())
```

发布后也可以使用固定版本的 npm CDN 地址作为 `base`。

## 数据结构

| 路径 | 内容 |
| --- | --- |
| `data/countries.json` | `id`, `zh`, `en`, `pinyin` |
| `data/regions/{ISO2}.json` | `id`, `country`, `code`, `zh`, `en`, `pinyin`，可选 `aliases`, `children` |
| `data/cities/{ISO2}.json` | `id`, `country`, `region`, `kind`, `zh`, `en`, `pinyin`, `lat`, `lon`，可选 `subregion`, `officialId`, `aliases` |
| `data/coverage.json` | 数据总量、名称覆盖率、逐国核验状态 |

- `region` 指向一级行政区 ID；不适用或无法可靠确定一级行政区时为 `null`。
- `subregion` 可以是所属 `children` 记录的 ID，也可能是来源名录中的下级行政区名称或代码。`id` 应视为不透明字符串。
- `kind` 区分城市、首都、同级自治单位、同级地区以及供检索的代表地点。
- `lat`、`lon` 为地点代表坐标（WGS84）；时区由调用方按经纬度映射。
- 中国大陆、台湾、香港和澳门统一归入 `CN`；`TW`、`HK`、`MO` 提供相应区域筛选入口，全球汇总以 `countries.json` 为准。中国大陆收录地级市、直辖市及同级自治州、地区、盟，不扩展到县级和以下。

## 维护

```sh
npm ci
npm run build
npm test
npm run pack:local
```

## 许可与来源

数据以官方行政区划资料为主要依据。使用和再分发请保留 [许可](LICENSE) 与 [来源及署名说明](NOTICE.md)，具体数据使用条件见 `licenses/`。
