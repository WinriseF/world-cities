import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { test } from 'node:test'
import { countries, countryFiles } from '../index.js'
import coverage from '../data/coverage.json' with { type: 'json' }

const load = async url => JSON.parse(await readFile(url, 'utf8'))

test('every exported city and region is counted and linked in its own country', async () => {
  const ids = new Set()
  const timeZones = new Set()
  let totalCities = 0, totalRegions = 0, translated = 0, romanized = 0, unassigned = 0
  for (const { id } of countries) {
    const files = countryFiles(id)
    const regions = await load(files.regions)
    const cities = await load(files.cities)
    const regionIds = new Set(regions.map(r => r.id))
    const regionById = new Map(regions.map(r => [r.id, r]))
    assert.equal(regionIds.size, regions.length)
    assert.ok(regions.every(r => r.country === id))
    assert.equal(cities.length, coverage.byCountry[id].cities)
    for (const city of cities) {
      assert.ok(!ids.has(city.id))
      ids.add(city.id)
      assert.equal(city.country, id)
      assert.ok(city.region === null || regionIds.has(city.region), city.id)
      if (city.subregion) {
        assert.ok(typeof city.subregion === 'string' && city.subregion.trim(), city.id)
        const children = regionById.get(city.region)?.children
        if (children?.length) assert.ok(children.some(child => child.id === city.subregion), city.id)
      }
      assert.ok(Number.isFinite(city.lat) && Math.abs(city.lat) <= 90)
      assert.ok(Number.isFinite(city.lon) && Math.abs(city.lon) <= 180)
      assert.ok(city.en.trim().length)
      assert.ok(['capital', 'city', 'municipality', 'prefecture', 'locality'].includes(city.kind))
      assert.ok(typeof city.timeZone === 'string' && city.timeZone, city.id)
      timeZones.add(city.timeZone)
      if (city.zh) translated++
      if (city.pinyin) {
        assert.ok(city.zh)
        assert.match(city.pinyin, /^[a-züê0-9]+(?: [a-züê0-9]+)*$/)
        romanized++
      }
      if (city.region === null) unassigned++
    }
    totalRegions += regions.length
    totalCities += cities.length
  }
  for (const timeZone of timeZones) assert.doesNotThrow(() => new Intl.DateTimeFormat('en-US', { timeZone }), timeZone)
  assert.equal(totalCities, coverage.totals.cities)
  assert.equal(totalRegions, coverage.totals.regions)
  assert.equal(translated, coverage.totals.withChinese)
  assert.equal(romanized, coverage.totals.withPinyin)
  assert.equal(unassigned, coverage.totals.withoutRegion)
})

test('mainland hierarchy stops at prefecture level, including Tibet and the four municipalities', async () => {
  const files = countryFiles('cn')
  const regions = (await load(files.regions)).filter(r => !['CN-TW', 'CN-HK', 'CN-MO'].includes(r.code))
  const mainlandIds = new Set(regions.map(r => r.id))
  const cities = (await load(files.cities)).filter(c => mainlandIds.has(c.region))
  const tibet = regions.find(r => r.zh.includes('西藏'))
  assert.equal(regions.length, 31)
  assert.equal(cities.length, 337)
  assert.deepEqual(cities.filter(c => c.region === tibet.id).map(c => c.zh).sort(),
    ['拉萨', '日喀则', '昌都', '林芝', '山南', '那曲', '阿里地区'].sort())
  assert.equal(cities.filter(c => c.kind === 'municipality').length, 4)
  assert.equal(cities.filter(c => c.kind === 'city').length, 293)
  assert.equal(cities.find(c => c.zh === '阿里地区').kind, 'prefecture')
  const xiamen = cities.find(city => city.id === 'cn:350200')
  assert.deepEqual([xiamen.zh, xiamen.pinyin, xiamen.lat, xiamen.lon], ['厦门', 'xia men', 24.48, 118.08])
  assert.equal(cities.filter(c => c.kind === 'prefecture').length, 40)
  assert.ok(cities.every(c => c.zh && c.en && c.pinyin && c.region))
  assert.ok(!cities.some(c => ['昆山', '琼海', '浦东新区', '城关区', '狮泉河镇'].includes(c.zh)))
  for (const [zh, reading] of Object.entries({ 昌都: 'chang du', 六安: 'lu an', 重庆: 'chong qing', 喀什地区: 'ka shi di qu' })) {
    assert.equal(cities.find(c => c.zh === zh)?.pinyin, reading)
  }
})

test('CN contains the three regional views with shared records and no duplicate global entries', async () => {
  const cn = countryFiles('CN')
  const regions = await load(cn.regions)
  const cities = await load(cn.cities)
  assert.equal(regions.length, 34)
  assert.equal(cities.length, 348)
  const reference = coverage.byCountry.CN.cityReference
  assert.equal(reference.status, 'reference-checked')
  assert.equal(reference.expected, cities.length)
  assert.ok(Object.values(reference.parts).every(part => part.status === 'reference-checked'))
  assert.equal(Object.values(reference.parts).reduce((sum, part) => sum + part.expected, 0), cities.length)
  for (const [id, zh, pinyin, places] of [
    ['TW', '中国台湾', 'zhong guo tai wan', ['台北', '新北市', '桃园', '台中', '台南', '高雄', '基隆', '新竹', '嘉义']],
    ['HK', '中国香港', 'zhong guo xiang gang', ['香港']],
    ['MO', '中国澳门', 'zhong guo ao men', ['澳门']]
  ]) {
    assert.ok(!countries.some(c => c.id === id))
    assert.ok(!Object.hasOwn(coverage.byCountry, id))
    const region = regions.find(r => r.code === 'CN-' + id)
    assert.equal(region.zh, zh)
    assert.equal(region.pinyin, pinyin)
    const files = countryFiles(id)
    assert.deepEqual(await load(files.regions), [region])
    const subset = cities.filter(c => c.region === region.id)
    assert.deepEqual(await load(files.cities), subset)
    assert.deepEqual(subset.map(c => c.zh).sort(), places.sort())
    assert.ok(subset.every(c => c.country === 'CN'))
    if (id === 'TW') {
      assert.equal(region.children.length, 22)
      assert.equal(new Set(region.children.map(r => r.id)).size, 22)
      assert.ok(region.children.every(r => r.country === 'CN'))
      for (const city of subset) {
        const child = region.children.find(r => r.id === city.subregion)
        assert.equal(child.en, city.en)
      }
    }
  }
})

test('cities with the same name keep distinct parents and lower subdivisions stay out', async () => {
  const uk = await load(countryFiles('GB').cities)
  assert.equal(uk.length, 76)
  assert.equal(new Set(uk.filter(c => c.en === 'Bangor').map(c => c.region)).size, 2)
  assert.ok(!uk.some(c => c.en === 'Edgware'))
  for (const cc of ['SG', 'VA', 'MC']) {
    const files = countryFiles(cc)
    assert.equal((await load(files.cities)).length, 1)
    assert.deepEqual(await load(files.regions), [])
  }
  for (const [code, city, region] of [['FR', 'Paris', 'Île-de-France'], ['GB', 'London', 'England'], ['AU', 'Sydney', 'New South Wales']]) {
    const files = countryFiles(code)
    const cities = await load(files.cities)
    const regions = await load(files.regions)
    assert.equal(cities.find(c => c.en === city)?.region, regions.find(r => r.en === region)?.id)
    assert.ok(cities.find(c => c.en === city)?.zh)
  }
})

test('five major-city exceptions preserve their scope and provide searchable cities in every listed region', async () => {
  const exceptions = ['IQ', 'LR', 'ML', 'SY', 'TD']
  assert.deepEqual(Object.entries(coverage.byCountry).filter(([, c]) => c.cityReference.status === 'major-cities').map(([id]) => id).sort(), exceptions)
  for (const cc of exceptions) {
    const files = countryFiles(cc)
    const cities = await load(files.cities)
    const regions = await load(files.regions)
    assert.ok(regions.every(r => cities.some(c => c.region === r.id)))
    assert.ok(cities.every(c => c.zh && c.en && c.pinyin))
  }
  const lr = await load(countryFiles('LR').cities)
  assert.ok(['Yekepa', 'Harbel'].every(name => lr.some(c => c.en === name && c.kind === 'locality')))
  const ml = await load(countryFiles('ML').cities)
  for (const [name, legal] of [['Fana', 'Guégnéka'], ['Dioïla', 'Kaladougou'], ['Yanfolila', 'Wassoulou-Ballé'], ['Ké-Macina', 'Macina']]) {
    const city = ml.find(c => c.en === name)
    assert.ok(city?.aliases.includes(legal) && city.officialId)
  }
  assert.equal(Object.values(coverage.byCountry).filter(c => c.cityReference.status === 'reference-checked').length, 229)
})


test('every country, region, subregion and city has English, Chinese and pinyin names', async () => {
  const check = place => {
    assert.ok(place.en?.trim() && /\p{Script=Han}/u.test(place.zh || ''), place.id)
    assert.match(place.pinyin || '', /^[a-züê0-9]+(?: [a-züê0-9]+)*$/, place.id)
    for (const child of place.children || []) check(child)
  }
  for (const country of countries) {
    check(country)
    const files = countryFiles(country.id)
    for (const place of [...await load(files.regions), ...await load(files.cities)]) check(place)
  }
  assert.equal(coverage.totals.withChinese, coverage.totals.cities)
  assert.equal(coverage.totals.withPinyin, coverage.totals.cities)
})


test('city time zones follow administrative context and precise boundaries', async () => {
  const us = await load(countryFiles('US').cities)
  for (const [name, expected] of [['Diomede', 'America/Nome'], ['Kupreanof', 'America/Sitka'], ['Calais', 'America/New_York']]) {
    assert.equal(us.find(city => city.en === name)?.timeZone, expected)
  }
  const cn = await load(countryFiles('CN').cities)
  for (const [name, expected] of [['林芝', 'Asia/Shanghai'], ['乌鲁木齐', 'Asia/Shanghai'], ['台北', 'Asia/Taipei'], ['香港', 'Asia/Hong_Kong'], ['澳门', 'Asia/Macau']]) {
    assert.equal(cn.find(city => city.zh === name)?.timeZone, expected)
  }
  const ps = await load(countryFiles('PS').cities)
  assert.equal(ps.find(city => city.id === 'ps:CEC-003')?.timeZone, 'Asia/Hebron')
})
