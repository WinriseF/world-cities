import assert from 'node:assert/strict'
import { createHash } from 'node:crypto'
import { readFile } from 'node:fs/promises'
import { test } from 'node:test'
import { countryFiles } from '../index.js'

const load = async url => JSON.parse(await readFile(url, 'utf8'))

test('official city identifiers and their region assignments survive the build', async () => {
  const expected = {
    BR: [5570, '0e97620ef084e8d90673861a4ed7dca16a69a26130a6ae368776b7826f74999c'],
    US: [10247, '7547769fddfb9b18ab958378b75e1c863d9b6a1eafae6c19098746ac96db25c2'],
    DE: [2060, '3324d03fbbfdef218e7c0dbefd1a27cdfe8849e14406c1e12e7a7c63f0260b68'],
    JP: [792, '0f88de5c94b100410d8956cce8a783c4af6d1d37c2e2965921bcf232f41219e9'],
    ID: [98, 'e38d42862c796934e6abaa26fbea872c0490c11e4ed2a319b9440f0c72699351'],
    PL: [1026, 'eb4e171732a3bf318b35bc378aa74f2510e84f8b815bd7ea2f8d144cb056ff44'],
    PH: [149, '54f4a1a2f61808c5493dfbfde458ba6469c177fa0033d5184d892aada4e06454']
  }
  for (const [country, [count, digest]] of Object.entries(expected)) {
    const files = countryFiles(country)
    const states = new Map((await load(files.regions)).map(r => [r.id, r.code || r.en]))
    const records = (await load(files.cities)).filter(c => c.officialId)
    assert.equal(new Set(records.map(c => c.officialId)).size, count)
    const pairs = records.map(c => c.officialId + ' ' + states.get(c.region)).sort()
    assert.equal(createHash('sha256').update(pairs.join('\n')).digest('hex'), digest, country)
  }
})

test('restored cities have representative coordinates and searchable names', async () => {
  for (const [cc, officialId, en, lat, lon] of [
    ['BR','1100049','Cacoal',-11.44,-61.45], ['US','0200065','Adak',51.9,-176.6],
    ['DE','06435014','Hanau',50.13,8.92], ['JP','092134','Nasushiobara',36.96,140.05],
    ['PH','1380600000','Manila',14.60,120.98]
  ]) {
    const c = (await load(countryFiles(cc).cities)).find(r => r.officialId === officialId)
    assert.equal(c.en, en)
    assert.ok(c.zh && c.pinyin)
    assert.ok(Math.abs(c.lat-lat)<0.1 && Math.abs(c.lon-lon)<0.1)
  }
  const us = await load(countryFiles('US').cities)
  const sf = us.find(c => c.officialId === '0667000')
  assert.equal(sf.id,'csc:125809')
  assert.ok(Math.abs(sf.lon + 122.42) < 0.03)
  assert.ok(us.find(c => c.officialId === '3651000').aliases.includes('New York City'))
})

test('overseas communes keep their official codes and Polynesian seats stay in their assigned divisions', async () => {
  for (const [country, prefix, count] of [['GP', '971', 32], ['MQ', '972', 34], ['RE', '974', 24], ['PF', '987', 48]]) {
    const cities = await load(countryFiles(country).cities)
    assert.equal(cities.length, count)
    assert.equal(new Set(cities.map(city => city.officialId)).size, count)
    assert.ok(cities.every(city => city.officialId.startsWith(prefix) && city.zh && city.pinyin))
  }
  const pf = await load(countryFiles('PF').cities)
  const gambier = pf.find(city => city.officialId === '98719')
  assert.equal(gambier.region, 'pf:r:tuamotu-gambier')
  assert.ok(gambier.aliases.includes('Rikitea'))
  assert.ok(Math.abs(gambier.lon + 134.97) < 0.02 && Math.abs(gambier.lat + 23.12) < 0.02)
  const papeete = pf.find(city => city.id === 'csc:154909')
  assert.equal(papeete.kind, 'capital')
  assert.equal(papeete.region, 'pf:r:windward')
})

test('municipal registers preserve distinct codes and the official parent division', async () => {
  const loadRegister = async (country, count, width = 4) => {
    const files = countryFiles(country)
    const cities = await load(files.cities)
    const regions = new Map((await load(files.regions)).map(region => [region.id, region.code]))
    assert.equal(cities.length, count)
    assert.equal(new Set(cities.map(city => city.officialId)).size, count)
    assert.ok(cities.every(city => /^\d+$/.test(city.officialId) && city.officialId.length === width && regions.has(city.region)))
    return new Map(cities.map(city => [city.officialId, { ...city, regionCode: regions.get(city.region) }]))
  }
  const [dk, ec, no, se, al, sv] = await Promise.all([
    loadRegister('DK', 98), loadRegister('EC', 223), loadRegister('NO', 357),
    loadRegister('SE', 290), loadRegister('AL', 61, 2), loadRegister('SV', 44)
  ])
  assert.equal(dk.get('0751').regionCode, 'DK-82')
  assert.equal(ec.get('0809').en, 'Borbón')
  assert.equal(ec.get('0809').regionCode, 'EC-E')
  assert.ok([...no.values()].every(city => city.regionCode === 'NO-' + city.officialId.slice(0, 2)))
  assert.equal(se.get('0305').en, 'Håbo')
  assert.equal(se.get('0305').regionCode, 'SE-C')
  assert.equal(se.get('0643').en, 'Habo')
  assert.equal(se.get('0643').regionCode, 'SE-F')
  assert.ok(se.get('0680').aliases.includes('Huskvarna'))
  assert.equal(ec.get('1001').zh, '伊瓦拉')
  assert.equal(ec.get('1001').pinyin, 'yi wa la')
  assert.equal(se.get('1281').zh, '隆德')
  for (const register of [ec, no, se, al, sv]) {
    assert.ok([...register.values()].every(city => city.zh && city.pinyin))
  }
  assert.equal(al.get('05').en, 'Dimal')
  assert.equal(al.get('05').regionCode, 'AL-01')
  assert.ok(al.get('05').aliases.includes('Ura Vajgurore'))
  assert.equal(sv.get('0601').id, 'csc:104914')
  assert.equal(sv.get('0601').kind, 'capital')
  assert.equal(sv.get('0601').regionCode, 'SV-SS')
  assert.ok(sv.get('0601').aliases.includes('San Salvador'))
})

test('national rosters distinguish local authorities, preserve seats and separate counties with the same name', async () => {
  const [nz, md, kr] = await Promise.all(['NZ', 'MD', 'KR'].map(code => load(countryFiles(code).cities)))
  for (const [rows, count] of [[nz, 67], [md, 67], [kr, 167]]) {
    assert.equal(rows.length, count)
    assert.ok(rows.every(row => row.zh && row.pinyin && row.region))
  }
  assert.equal(new Set(nz.map(row => row.officialId)).size, 67)
  assert.ok(nz.find(row => row.officialId === '076').aliases.includes('Manukau City'))
  assert.equal(nz.find(row => row.officialId === '067').kind, 'municipality')
  assert.equal(new Set(md.map(row => row.officialId)).size, 67)
  assert.equal(md.find(row => row.officialId === '0154000').en, 'Stăuceni')
  const goseong = kr.filter(row => row.en === 'Goseong County')
  assert.equal(goseong.length, 2)
  assert.equal(new Set(goseong.map(row => row.region)).size, 2)
  assert.equal(kr.filter(row => row.id.startsWith('kr:county:')).length, 82)
  assert.equal(kr.find(row => row.id === 'kr:city:suncheon:12').region, 'csc:r:5854')
})

test('Colombia includes every reviewed DIVIPOLA municipality code and the island representative', async () => {
  const cities = await load(countryFiles('CO').cities)
  const byCode = new Map(cities.map(city => [city.officialId, city]))
  assert.equal(cities.length, 1104)
  assert.equal(byCode.size, 1104)
  assert.ok(cities.every(city => city.zh && city.pinyin && city.region))
  assert.equal(new Set(cities.map(city => city.region)).size, 33)
  assert.equal(byCode.get('27493').region, 'csc:r:2876')
  assert.equal(byCode.get('11001').zh, '波哥大')
  assert.equal(byCode.get('88001').zh, '圣安德烈斯')
  assert.equal(byCode.has('91263'), false)
})

test('Iceland groups its current municipalities by the eight statistical regions', async () => {
  const files = countryFiles('IS')
  const [regions, cities] = await Promise.all([load(files.regions), load(files.cities)])
  const byCode = new Map(cities.map(city => [city.officialId, city]))
  assert.equal(regions.length, 8)
  assert.equal(cities.length, 61)
  assert.equal(byCode.size, 61)
  assert.ok(cities.every(city => city.zh && city.pinyin))
  assert.equal(byCode.get('0000').kind, 'capital')
  assert.equal(byCode.get('8401').region, regions.find(region => region.code === 'IS-8').id)
  assert.ok(byCode.get('3609').aliases.includes('Skorradalshreppur'))
  assert.equal(byCode.has('3506'), false)
})

test('recent registers retain current cities and municipalities', async () => {
  const counts = { AT: [205, 9], BE: [565, 3], LT: [103, 10], NL: [342, 12], ME: [25, 25] }
  const registers = await Promise.all(Object.entries(counts).map(async ([country, [count, regionCount]]) => {
    const files = countryFiles(country)
    const [cities, regions] = await Promise.all([load(files.cities), load(files.regions)])
    const regionIds = new Set(regions.map(region => region.id))
    const byCode = new Map(cities.map(city => [city.officialId, city]))
    assert.equal(cities.length, count, country)
    assert.equal(byCode.size, count, country)
    assert.equal(new Set(cities.map(city => city.region)).size, regionCount, country)
    assert.ok(cities.every(city => city.officialId && city.zh && city.pinyin && regionIds.has(city.region)), country)
    return byCode
  }))
  const [austria, belgium, lithuania, netherlands, montenegro] = registers
  assert.equal(austria.get('90001').kind, 'capital')
  assert.ok(belgium.get('82039').aliases.includes('Bertogne'))
  assert.ok(belgium.get('73111').aliases.includes('Borgloon'))
  assert.equal(belgium.has('11007'), false)
  assert.equal([...belgium.values()].filter(city => city.region === 'csc:r:1376').length, 19)
  assert.equal(lithuania.get('15345').en, 'Grigiškės')
  assert.equal(lithuania.get('15345').region, 'csc:r:1601')
  assert.equal(netherlands.get('0363').kind, 'capital')
  assert.equal(netherlands.get('0518').zh, '海牙')
  assert.equal(netherlands.get('0765').zh, '佩克拉')
  assert.ok(netherlands.get('1979').aliases.includes('Delfzijl'))
  assert.ok([...netherlands.values()].every(city => city.id !== 'csc:149852'))
  assert.equal(montenegro.get('20176').id, 'csc:67364')
  assert.ok(montenegro.get('20281').aliases.includes('Golubovci'))
  assert.ok([...montenegro.values()].every(city => city.id !== 'csc:160069'))
})

test('Armenia keeps official urban codes and North Macedonia groups cities by statistical region', async () => {
  const armenia = await load(countryFiles('AM').cities)
  const armenianCodes = new Map(armenia.map(city => [city.officialId, city]))
  assert.equal(armenia.length, 49)
  assert.equal(armenianCodes.size, 49)
  assert.equal(armenianCodes.get('01001000').kind, 'capital')
  const etchmiadzin = armenianCodes.get('04002011')
  assert.equal(etchmiadzin.id, 'csc:549')
  assert.equal(etchmiadzin.en, 'Etchmiadzin')
  assert.equal(etchmiadzin.zh, '埃奇米亚津')
  assert.ok(etchmiadzin.aliases.includes('Vagharshapat'))
  assert.equal(armenianCodes.get('09007011').en, 'Kajaran')
  const files = countryFiles('MK')
  const [regions, cities] = await Promise.all([load(files.regions), load(files.cities)])
  const byId = new Map(regions.map(region => [region.id, region]))
  const skopje = cities.find(city => city.kind === 'capital')
  assert.equal(regions.length, 8)
  assert.equal(new Set(regions.flatMap(region => region.children.map(child => child.id))).size, 80)
  assert.equal(cities.length, 34)
  assert.equal(skopje.id, 'csc:67526')
  assert.equal(byId.get(skopje.region).code, 'MK008')
  assert.ok(cities.some(city => city.officialId === 'MK0040310' && city.en === 'Valandovo'))
  assert.ok(cities.some(city => city.officialId === 'MK0030305' && city.en === 'Debar'))
  for (const city of cities.filter(city => city.kind !== 'capital')) {
    const region = byId.get(city.region)
    assert.ok(city.officialId.startsWith(region.code))
    assert.ok(region.children.some(child => child.id === city.subregion))
  }
  assert.ok([...armenia, ...cities].every(city => city.zh && city.pinyin))
})

test('Serbia contains each city and peer municipality once', async () => {
  const files = countryFiles('RS')
  const [cities, regions] = await Promise.all([load(files.cities), load(files.regions)])
  const regionIds = new Set(regions.map(region => region.id))
  assert.equal(cities.length, 145)
  assert.equal(cities.filter(city => city.kind === 'municipality').length, 117)
  assert.equal(cities.filter(city => city.kind === 'city').length, 27)
  assert.equal(cities.filter(city => city.kind === 'capital').length, 1)
  assert.equal(cities.find(city => city.en === 'Belgrade').id, 'csc:165467')
  assert.equal(cities.find(city => city.en === 'Bor').kind, 'city')
  assert.equal(cities.find(city => city.en === 'Petrovac na Mlavi').region, regions.find(region => region.code === 'RS-11').id)
  assert.ok(cities.every(city => city.zh && city.pinyin && regionIds.has(city.region)))
  assert.ok(cities.every(city => !['Petrovaradin', 'Dobanovci', 'Kosovska Mitrovica'].includes(city.en)))
})

test('corrected provincial and territory partitions refer to the current location', async () => {
  for (const [cc, count] of [['AO',21], ['BI',5], ['FR',18]]) {
    const states = await load(countryFiles(cc).regions)
    assert.equal(states.length, count)
  }
  const bi = await load(countryFiles('BI').cities)
  assert.ok(bi.every(c => c.region))
  assert.equal(bi.find(c => c.en==='Muramvya').region,'bi:gitega')
  for (const [cc, en] of [['FK','Stanley'],['GI','Gibraltar'],['IM','Douglas'],['SH','Jamestown'],['NC','Nouméa']]) {
    assert.equal((await load(countryFiles(cc).cities)).filter(c => c.en===en).length,1)
  }
})

test('new national registers reach the published city shards with their intended level and identities', async () => {
  for (const [code, count] of Object.entries({ CZ: 610, RO: 319, HR: 128, SK: 141,
    HU: 348, BG: 257, EE: 47, SI: 69, FI: 107, NP: 293 })) {
    const cities = await load(countryFiles(code).cities)
    assert.equal(cities.length, count, code)
  }
  const cz = await load(countryFiles('CZ').cities)
  assert.ok(cz.some(c => c.en === 'Přebuz' && c.officialId))
  assert.ok(cz.some(c => c.en === 'Boží Dar' && c.officialId))
  assert.ok(!cz.some(c => c.en === 'Praha 1'))
  const ca = await load(countryFiles('CA').cities)
  for (const en of ['Flin Flon', 'Lloydminster']) assert.equal(ca.filter(c => c.en === en).length, 1)
  const np = await load(countryFiles('NP').cities)
  assert.ok(np.some(c => c.id === 'csc:165412' && [c.en, ...c.aliases].includes('Birgunj')))
  const indian = await load(countryFiles('IN').cities)
  const kerala = indian.filter(c => c.officialId && /^[MC]\d+$/.test(c.officialId))
  assert.equal(new Set(kerala.map(c => c.officialId)).size, 93)
  assert.equal(kerala.filter(c => [c.en, ...(c.aliases ?? [])].includes('Paravur')).length, 2)
})

test('single-entry shards now include peer municipalities and distinguish seats from jurisdictions', async () => {
  for (const [cc, count] of Object.entries({ AX: 16, BS: 34, FM: 77, FO: 29, GU: 19, IM: 21,
    LV: 82, MH: 25, MT: 68, NC: 33, NI: 153, XK: 38, YT: 17, GF: 22, PM: 2 })) {
    const places = await load(countryFiles(cc).cities)
    assert.equal(places.length, count, cc)
  }
  const malta = await load(countryFiles('MT').cities)
  const rabat = malta.filter(r => r.en.startsWith('Ir-Rabat'))
  assert.equal(new Set(rabat.map(r => r.officialId)).size, 2)
  assert.equal(new Set(rabat.map(r => r.region)).size, 2)
  assert.ok(rabat.some(r => r.aliases.includes('Victoria') && r.lat > 36))
  const fm = await load(countryFiles('FM').cities)
  assert.ok(fm.every(p => p.lat > 0 && p.lat < 11 && p.lon > 137 && p.lon < 164))
  assert.equal(fm.filter(p => p.kind === 'municipality').length, 76)
  const bq = await load(countryFiles('BQ').cities)
  assert.deepEqual(bq.map(r => r.officialId).sort(), ['BQ-BO', 'BQ-SA', 'BQ-SE'])
  assert.ok(!bq.some(r => r.en === 'Rincon'))
  const doha = (await load(countryFiles('QA').cities)).find(r => r.en === 'Doha')
  assert.equal(doha.zh, '多哈')
})

test('Kuwait search localities coexist with the capital and keep their governorates', async () => {
  const files = countryFiles('KW')
  const cities = await load(files.cities)
  const regions = new Map((await load(files.regions)).map(r => [r.id, r.code]))
  assert.equal(cities.filter(r => r.kind === 'capital').length, 1)
  assert.deepEqual(cities.filter(r => r.kind === 'locality').map(r => [r.en, regions.get(r.region)]).sort(),
    [['Ahmadi', 'KW-AH'], ['Al Jahra', 'KW-JA'], ['Sabah Al-Ahmad', 'KW-AH']])
  assert.equal(cities.find(r => r.en === 'Ahmadi').pinyin, 'ai ha mai di')
})
