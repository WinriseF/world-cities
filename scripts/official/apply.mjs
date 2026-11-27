import assert from 'node:assert/strict'
import worldCities from '../../sources/reviewed-world-cities.json' with { type: 'json' }
import reviewed from '../../corrections/administration.json' with { type: 'json' }
import { placeNames } from '../transform.mjs'

const names = (country, en, zh) => placeNames({ name: en }, country, { zh })

export function applyOfficialData(groups, rosters) {
  for (const [country, rows] of Object.entries(reviewed.regions)) {
    for (const [id, en, zh] of rows) {
      groups.get(country).regions.push({ id, country, code: null, ...names(country, en, zh) })
    }
  }

  for (const [country, roster] of Object.entries(rosters)) {
    const group = groups.get(country)
    const states = new Map(group.regions.map(r => [r.code || r.en, r.id]))
    // Tokyo and Yakutat have different administrative forms from the national city lists.
    group.cities = group.cities.filter(c => c.id === 'csc:64500' || c.id === 'csc:129652')
    for (const record of roster) {
      const { code, state, en, zh, lat, lon, aliases } = record
      assert.ok(states.has(state), 'Unknown official region ' + country + '/' + state)
      group.cities.push({
        id: record.csc ? 'csc:' + record.csc : country.toLowerCase() + ':' + code,
        officialId: code, country, region: states.get(state), kind: record.capital ? 'capital' : 'city',
        ...names(country, en, zh), ...(aliases?.length ? { aliases } : {}), lat, lon
      })
    }
  }

  const bangsamoro = groups.get('PH').regions.find(r => r.code === 'PH-14')
  Object.assign(bangsamoro, names('PH', 'Bangsamoro Autonomous Region in Muslim Mindanao', '邦萨摩洛自治区'))
  for (const city of groups.get('BI').cities) {
    assert.ok(reviewed.burundiCities[city.en], 'Unmapped Burundi city ' + city.en)
    city.region = reviewed.burundiCities[city.en]
  }
  // The former Icolo e Bengo municipality is now represented by the province and its seat.
  const angola = groups.get('AO')
  angola.cities = angola.cities.filter(c => c.id !== 'csc:611')

  // The Bermuda government lists Paget as a parish. Hamilton holds city status.
  const bermuda = groups.get('BM')
  bermuda.cities = bermuda.cities.filter(city => city.id !== 'csc:153516')

  const france = groups.get('FR')
  const noumea = france.cities.find(c => c.id === 'csc:160039')
  assert.ok(noumea, 'Expected Nouméa before moving it to NC')
  groups.get('NC').cities.push({ ...noumea, country: 'NC', region: 'csc:r:5225' })
  france.cities = france.cities.filter(c => c !== noumea)
  france.regions = france.regions.filter(r => !reviewed.franceOutsideRegions.includes(r.code))
  for (const { unName, geonames, wikidata, ...r } of worldCities) {
    const spellings = [unName, ...Array.from(unName.matchAll(/\(([^)]+)\)/g), m => m[1])]
    const aliases = [...new Set(spellings)].filter(v => v !== r.en)
    groups.get(r.country).cities.push({ ...r, ...names(r.country, r.en, r.zh), ...(aliases.length ? { aliases } : {}) })
  }
  for (const r of reviewed.cities) {
    groups.get(r.country).cities.push({ ...r, ...names(r.country, r.en, r.zh) })
  }
  for (const [country, changes] of Object.entries(reviewed.cityUpdates)) {
    const cities = new Map(groups.get(country).cities.map(city => [city.id, city]))
    for (const [id, update] of Object.entries(changes)) {
      assert.ok(cities.has(id), 'Unknown reviewed city ' + id)
      Object.assign(cities.get(id), update)
    }
  }
}

export function mergeReviewedCities(groups, review) {
  for (const [country, { cities, retired, regions, regionNames }] of Object.entries(review)) {
    const group = groups.get(country)
    if (regions) {
      group.regions = regions.map(({ en, zh, ...region }) => ({ ...region, country, ...names(country, en, zh) }))
    }
    if (regionNames) {
      const pending = new Map(Object.entries(regionNames))
      const applyNames = list => {
        for (const region of list) {
          if (pending.has(region.id)) {
            Object.assign(region, names(country, region.en, pending.get(region.id)))
            pending.delete(region.id)
          }
          if (region.children) applyNames(region.children)
        }
      }
      applyNames(group.regions)
      assert.equal(pending.size, 0, `Unknown region name updates: ${country} ${[...pending.keys()].join(', ')}`)
    }
    const byId = new Map(group.cities.map(city => [city.id, city]))
    for (const id of retired) assert.ok(byId.delete(id), 'Unknown retired record ' + id)
    for (const record of cities) {
      const prior = byId.get(record.id)
      const labels = prior?.en === record.en && prior?.zh === record.zh
        ? { en: prior.en, zh: prior.zh, pinyin: prior.pinyin }
        : names(country, record.en, record.zh)
      byId.set(record.id, { ...prior, ...record, country, ...labels })
    }
    group.cities = [...byId.values()]
  }
}
