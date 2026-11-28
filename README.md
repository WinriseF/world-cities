# @winrisef/world-cities

A worldwide geographic database of countries, administrative regions, cities and city-level equivalents, with Chinese and English names, Mandarin pinyin, WGS84 coordinates and IANA time zones. Country-specific JSON files can be loaded on demand, with zero runtime dependencies.

[Live demo / 在线展示](https://winrisef.github.io/world-cities/) · [简体中文](#简体中文) · [Coverage](COVERAGE.md) · [Data attribution](NOTICE.md)

The administrative rosters are based almost entirely on official national sources, supplemented by other public geographic references for cross-checking and filling gaps. Names, data formats and representative coordinates are normalized across countries.

## Coverage

| Content | Count |
| --- | ---: |
| Countries and territories | 247 |
| First-level administrative regions | 3,814 |
| Cities, city-level equivalents and representative places | 122,061 |
| City records with English, Chinese, pinyin and time zone | 100% |

Coverage: 229 reference-checked, 5 major-city selections, 13 not applicable. See [coverage details](COVERAGE.md). Chinese names without established translations are translated or transliterated.

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
const base = 'https://cdn.jsdelivr.net/npm/@winrisef/world-cities@0.1.138/data'
const countries = await fetch(`${base}/countries.json`).then(r => r.json())
const cities = await fetch(`${base}/cities/CN.json`).then(r => r.json())
```

You can also serve the packaged `data/` directory yourself and change `base` accordingly.

### Global search routing

Search a name before downloading country files. The 128 `data/search/` shards map normalized name prefixes to country codes; fetch only the matching countries' city and region files.

```js
const term = 'Lhasa'.normalize('NFKD').replace(/\p{M}/gu, '').toLowerCase().replace(/[^\p{L}\p{N}]/gu, '')
const chars = [...term]
const prefix = chars.slice(0, /\p{Script=Han}/u.test(chars[0]) ? 1 : 2)
const shard = (prefix.reduce((n, c) => n * 31 + c.codePointAt(0), 0) % 128).toString(16).padStart(2, '0')
const entries = await fetch(`${base}/search/${shard}.json`).then(r => r.json())
const codes = new Set(entries.filter(([name]) => name.startsWith(term)).flatMap(([, ids]) => ids.match(/../g)))
```

Use at least two non-Han characters, or one Chinese character. Each row is `[normalizedName, concatenatedCountryCodes]`; the actual place records remain in the country files.

## Data structure

| Path | Fields |
| --- | --- |
| `data/countries.json` | `id`, `zh`, `en`, `pinyin` |
| `data/regions/{ISO2}.json` | `id`, `country`, `code`, `zh`, `en`, `pinyin`; optional `aliases`, `children` |
| `data/cities/{ISO2}.json` | `id`, `country`, `region`, `kind`, `zh`, `en`, `pinyin`, `lat`, `lon`, `timeZone`; optional `subregion`, `officialId`, `aliases` |
| `data/coverage.json` | Record totals, name coverage and per-country verification status |
| `data/search/{00..7f}.json` | Normalized names and country-code routing index |

- `region` refers to a first-level administrative region ID, or is `null` when no applicable region exists or one cannot be reliably determined.
- `subregion` may refer to an entry in `children`, or contain a lower-level name or code from the source roster. Treat `id` values as opaque strings.
- `kind` distinguishes `city`, `capital`, `municipality`, `prefecture` and `locality` records.
- `lat` and `lon` are representative WGS84 coordinates. `timeZone` is an IANA time zone identifier (for example `America/New_York`), suitable for `Intl.DateTimeFormat`.

## Development

```sh
npm ci
npm run build
npm test
npm run pack:local
```

## License and attribution

The database is licensed under [ODbL 1.0](LICENSE), subject to the source-specific reuse conditions documented in [`licenses/`](licenses/). Retain the license and [data attribution](NOTICE.md) when using or redistributing the data.

---

## 简体中文

全球国家、行政区及城市地名数据库，支持中文、英文、拼音检索，提供 WGS84 经纬度及 IANA 时区。数据按国家和地区拆分为 JSON，可按需加载，无运行时依赖。

本数据库的行政区划名录几乎全部以各国官方相关资料为依据，结合其他公开地理资料进行交叉核验与缺失信息补充，并统一整理数据格式、名称及经纬度。

### 数据概况

| 内容 | 数量 |
| --- | ---: |
| 国家和地区 | 247 |
| 一级行政区 | 3,814 |
| 城市及同级单位、代表地点 | 122,061 |
| 城市中英文、拼音及时区覆盖率 | 100% |

覆盖状态：229 个名录已核验，5 个仅收录主要城市，13 个不适用市级建制。详见 [数据覆盖](COVERAGE.md)。无通行中文译名的地点采用音译或意译。

### 安装与使用

```sh
npm install @winrisef/world-cities
```

- Node.js：通过 `countryFiles('CN')` 获取省级行政区和城市 JSON 的 URL，再读取数据，按 `zh`、`en`、`pinyin` 和 `aliases` 字段搜索。
- 浏览器：直接请求固定版本的 CDN JSON，或自行部署 `data/`，无需引入库。

完整代码示例见上方 [Usage](#usage)。全球地名检索可先调用[搜索索引](#global-search-routing)，再按需加载国家数据。

### 数据结构

| 路径 | 内容 |
| --- | --- |
| `data/countries.json` | `id`, `zh`, `en`, `pinyin` |
| `data/regions/{ISO2}.json` | `id`, `country`, `code`, `zh`, `en`, `pinyin`，可选 `aliases`, `children` |
| `data/cities/{ISO2}.json` | `id`, `country`, `region`, `kind`, `zh`, `en`, `pinyin`, `lat`, `lon`, `timeZone`，可选 `subregion`, `officialId`, `aliases` |
| `data/coverage.json` | 数据总量、名称覆盖率、逐国核验状态 |
| `data/search/{00..7f}.json` | 地名搜索索引，仅返回匹配的国家代码 |

- `region` 指向一级行政区 ID；不适用或无法可靠确定一级行政区时为 `null`。
- `subregion` 可以是所属 `children` 记录的 ID，也可能是来源名录中的下级行政区名称或代码。`id` 应视为不透明字符串。
- `kind` 区分城市、首都、同级自治单位、同级地区以及供检索的代表地点。
- `lat`、`lon` 为地点代表坐标（WGS84）；`timeZone` 为 IANA 时区标识，可直接用于 `Intl.DateTimeFormat`。

### 维护

```sh
npm ci
npm run build
npm test
npm run pack:local
```

### 许可与来源

数据库采用 [ODbL 1.0](LICENSE) 许可，具体来源的使用条件见 [`licenses/`](licenses/)。使用和再分发请保留许可与 [来源及署名说明](NOTICE.md)。数据以官方行政区划资料为主要依据。
