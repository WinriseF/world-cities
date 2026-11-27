# @winrisef/world-cities

A worldwide geographic database of countries, administrative regions, cities and city-level equivalents, with Chinese and English names, Mandarin pinyin, and WGS84 coordinates. Country-specific JSON files can be loaded on demand, with zero runtime dependencies.

[简体中文](#简体中文) · [Coverage](COVERAGE.md) · [Data attribution](NOTICE.md)

The administrative rosters are based almost entirely on official national sources, supplemented by other public geographic references for cross-checking and filling gaps. Names, data formats and representative coordinates are normalized across countries.

## Coverage

| Content | Count |
| --- | ---: |
| Countries and territories | 247 |
| First-level administrative regions | 3,814 |
| Cities, city-level equivalents and representative places | 122,061 |
| City records with English, Chinese and pinyin names | 100% |

Of the 247 countries and territories, 229 have been checked against their statutory reference rosters, 5 prioritize major cities, and 13 have no applicable city-level administrative structure. Administrative definitions differ by country; the total is not a count of legally designated cities alone. See [coverage details](COVERAGE.md). Places without established Chinese translations use project-supplied transliterations or translations.

## Installation

```sh
npm install @winrisef/world-cities
```

## Usage

### Node.js

Load the regions and cities for a country, then search Chinese, English, pinyin and alternative names:

```js
import { readFile } from 'node:fs/promises'
import { countries, countryFiles } from '@winrisef/world-cities'

const { regions, cities } = countryFiles('CN')
const read = async url => JSON.parse(await readFile(url, 'utf8'))
const [provinceList, cityList] = await Promise.all([read(regions), read(cities)])
const query = 'lasa' // also supports 拉萨 and Lhasa
const normalize = text => text.toLowerCase().replace(/\s+/g, '')
const results = cityList.filter(city =>
  [city.zh, city.en, city.pinyin, ...(city.aliases ?? [])]
    .some(name => name && normalize(name).includes(normalize(query)))
)
```

### Browser / CDN

Load JSON directly without installing the package. Pin a version to keep the data consistent:

```js
const base = 'https://cdn.jsdelivr.net/npm/@winrisef/world-cities@0.1.134/data'
const countries = await fetch(`${base}/countries.json`).then(r => r.json())
const cities = await fetch(`${base}/cities/CN.json`).then(r => r.json())
```

You can also serve the packaged `data/` directory yourself and change `base` accordingly.

## Data structure

| Path | Fields |
| --- | --- |
| `data/countries.json` | `id`, `zh`, `en`, `pinyin` |
| `data/regions/{ISO2}.json` | `id`, `country`, `code`, `zh`, `en`, `pinyin`; optional `aliases`, `children` |
| `data/cities/{ISO2}.json` | `id`, `country`, `region`, `kind`, `zh`, `en`, `pinyin`, `lat`, `lon`; optional `subregion`, `officialId`, `aliases` |
| `data/coverage.json` | Record totals, name coverage and per-country verification status |

- `region` refers to a first-level administrative region ID, or is `null` when no applicable region exists or one cannot be reliably determined.
- `subregion` may refer to an entry in `children`, or contain a lower-level name or code from the source roster. Treat `id` values as opaque strings.
- `kind` distinguishes `city`, `capital`, `municipality`, `prefecture` and `locality` records.
- `lat` and `lon` are representative WGS84 coordinates. Time zones can be resolved separately from coordinates.
- Mainland China, Taiwan, Hong Kong and Macao are grouped under `CN`; `TW`, `HK` and `MO` are corresponding regional subsets. Use `countries.json` for global totals. Mainland China includes prefecture-level cities, centrally administered municipalities and equivalent autonomous prefectures, prefectures and leagues, excluding county-level or lower divisions.

## Development

```sh
npm ci
npm run build
npm test
npm run pack:local
```

## License and attribution

The database is licensed under [ODbL 1.0](LICENSE), subject to the source-specific reuse conditions documented in [`licenses/`](licenses/). Retain the license and [data attribution](NOTICE.md) when using or redistributing the data. The administrative rosters are based predominantly on official sources.

---

## 简体中文

全球国家、行政区及城市地名数据库，支持中文、英文、拼音检索，提供 WGS84 经纬度。数据按国家和地区拆分为 JSON，可按需加载，无运行时依赖。

本数据库的行政区划名录几乎全部以各国官方相关资料为依据，结合其他公开地理资料进行交叉核验与缺失信息补充，并统一整理数据格式、名称及经纬度。

### 数据概况

| 内容 | 数量 |
| --- | ---: |
| 国家和地区 | 247 |
| 一级行政区 | 3,814 |
| 城市及同级单位、代表地点 | 122,061 |
| 城市中英文及拼音覆盖率 | 100% |

229 个国家和地区按法定名录核验，5 个按主要城市优先收录，13 个不适用市级建制口径。各国行政建制不同，总量并非仅指法定城市数量。具体范围见 [数据覆盖](COVERAGE.md)。无通行中文译名的地点采用项目音译或意译。

### 安装与使用

```sh
npm install @winrisef/world-cities
```

- Node.js：通过 `countryFiles('CN')` 获取省级行政区和城市 JSON 的 URL，再读取数据，按 `zh`、`en`、`pinyin` 和 `aliases` 字段搜索。
- 浏览器：直接请求固定版本的 CDN JSON，或自行部署 `data/`，无需引入库。

完整代码示例见上方 [Usage](#usage)。

### 数据结构

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
- 中国大陆、台湾、香港和澳门统一归入 `CN`；`TW`、`HK`、`MO` 提供相应区域筛选入口，全球汇总以 `countries.json` 为准。中国大陆收录地级市、直辖市及同级自治州、地区、盟，不扩展到县级及以下。

### 维护

```sh
npm ci
npm run build
npm test
npm run pack:local
```

### 许可与来源

数据库采用 [ODbL 1.0](LICENSE) 许可，具体来源的使用条件见 [`licenses/`](licenses/)。使用和再分发请保留许可与 [来源及署名说明](NOTICE.md)。数据以官方行政区划资料为主要依据。
