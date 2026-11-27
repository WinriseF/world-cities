import assert from 'node:assert/strict'
import wikiNames from '../sources/wikidata-names.json' with { type: 'json' }
import gbCities from '../corrections/gb-cities.json' with { type: 'json' }

const urbanTerritories = new Set(['HK', 'MO', 'SG', 'MC', 'VA'])
const twCity = row => ['city', 'special municipality'].includes(row.type)
export function isRegion(row) {
  return !urbanTerritories.has(row.country_code) && String(row.level) === '1'
}

// Full administrative names in the code list, abbreviated names in CSC.
const shortNames = {
  152200: 159733, 152900: 159753, 433100: 158344, 522700: 157632,
  532800: 159419, 623000: 157328, 632500: 158735, 632800: 158755,
  652700: 159881, 653000: 159904
}
const provinceName = name => name.replace(/(维吾尔自治区|回族自治区|壮族自治区|自治区|省|市)$/, '')
const shortName = name => name?.replace(/(市|地区)$/, '')
function* mainland(divisions, regions, cities) {
  const mainlandRegions = regions.filter(r => r.country_code === 'CN' && isRegion(r))
  const types = new Set(['capital', 'city', 'prefecture', 'adm1', 'adm2', 'municipality', 'cities', 'region'])
  const candidates = cities.filter(row => row.country_code === 'CN' && types.has(row.type))
  for (const [code, official] of Object.entries(divisions)) {
    if (!/^[1-6]\d{3}00$/.test(code) || +code.slice(0, 2) > 65 || code.slice(2, 4) === '90') continue
    const municipality = code.endsWith('0000')
    if (municipality && !['110000', '120000', '310000', '500000'].includes(code)) continue
    const province = provinceName(divisions[code.slice(0, 2) + '0000'])
    const state = mainlandRegions.find(r => provinceName(r.native) === province)
    assert.ok(state, 'Missing province for ' + code)
    const matched = candidates.filter(row => row.state_id === state.id && (
      row.id === shortNames[code] || [row.native, row.translations?.['zh-CN']].some(name => shortName(name) === shortName(official))
    ))
    // Prefer the prefecture record over urban seats and similarly named districts.
    matched.sort((a, b) => Number(b.type === 'prefecture') - Number(a.type === 'prefecture') ||
      Number(b.native === official) - Number(a.native === official) || a.id - b.id)
    const row = matched[0] ?? (municipality ? state : null)
    assert.ok(row, 'Missing source coordinates for ' + code + ' ' + official)
    yield { id: 'cn:' + code, row, stateId: state.id, zh: official.replace(/市$/, ''),
      kind: municipality ? 'municipality' : official.endsWith('市') ? 'city' : 'prefecture' }
  }
}

const nonCityTypes = new Set(['town', 'borough', 'township', 'census designated place', 'woonplaats', 'suburb',
  'unincorporated community', 'village', 'localidad rural', 'town panchayat', 'census town', 'district', 'gu', '구', '군'])
const urbanLocalTypes = new Set(['city', 'municipal corporation', 'metropolitan corporation', 'città', 'ciudad', 'cidade'])
const normalized = value => value?.normalize('NFKD').replace(/\p{M}/gu, '').toLowerCase().replace(/[^\p{L}\p{N}]/gu, '')
const possibleCity = new Set(['city', 'capital', 'municipality', 'locality'])
function qualify(row, place, verifiedCity) {
  if (row.country_code === 'GB') return Object.hasOwn(gbCities, row.id)
  if (/^(?:province of|okres|county of|district of) | (?:rayon|raion|county|district|township)$/i.test(row.name)) return false
  const local = row.type_local?.trim().toLowerCase()
  if (nonCityTypes.has(local)) return false
  if (!possibleCity.has(row.type)) {
    return ['adm1', 'adm2', 'gov_seat'].includes(row.type) && place && verifiedCity &&
      [place.NAME_EN, place.NAMEASCII, place.NAME].some(n => n && normalized(n) === normalized(row.name)) &&
      Math.abs(place.LATITUDE - row.latitude) < 0.25 && Math.abs(place.LONGITUDE - row.longitude) < 0.25
  }
  if (verifiedCity || row.type === 'capital' || (row.type === 'city' && local) || urbanLocalTypes.has(local)) return true
  // The generic CSC "city" also includes villages and districts. Require a
  // second source for rows lacking an explicit local city classification.
  return place && (place.ADM0CAP === 1 || place.WORLDCITY === 1 || place.POP_MAX >= 50000)
}

export function* selectCities(divisions, regions, cities, features, verifiedCities) {
  yield* mainland(divisions, regions, cities)
  for (const row of regions.filter(r => r.country_code === 'TW' && twCity(r))) {
    yield { id: 'tw:' + row.iso2, row, stateId: row.id, kind: 'city' }
  }
  const places = new Map()
  for (const { properties: p } of features) {
    if (!/^[A-Z]{2}$/.test(p.ISO_A2) || !p.WIKIDATAID || !/^(Admin-|Populated place$)/i.test(p.FEATURECLA)) continue
    places.set(p.ISO_A2 + '/' + p.WIKIDATAID, p)
    if (urbanTerritories.has(p.ISO_A2) && /Admin-0/.test(p.FEATURECLA)) {
      yield { id: 'wd:' + p.WIKIDATAID, kind: p.ADM0CAP ? 'capital' : 'city', stateId: null,
        row: { country_code: p.ISO_A2, name: p.NAME_EN, latitude: p.LATITUDE, longitude: p.LONGITUDE }, zh: p.NAME_ZH }
    }
  }
  const seen = new Set()
  const citiesByCountry = new Map()
  for (const row of cities) {
    if (row.country_code === 'CN' || row.country_code === 'TW' || urbanTerritories.has(row.country_code)) continue
    const key = row.country_code + '/' + row.wikiDataId
    const place = row.wikiDataId && places.get(key)
    if (!qualify(row, place, Object.hasOwn(verifiedCities, row.wikiDataId))) continue
    if (row.wikiDataId && seen.has(key)) continue
    if (row.wikiDataId) seen.add(key)
    if (!citiesByCountry.has(row.country_code)) citiesByCountry.set(row.country_code, [])
    citiesByCountry.get(row.country_code).push(row)
    yield { id: 'csc:' + row.id, row, stateId: row.state_id, zh: [row.translations?.['zh-CN'], wikiNames[row.wikiDataId], place?.NAME_ZH, verifiedCities[row.wikiDataId]].find(v => /\p{Script=Han}/u.test(v)),
      kind: row.type === 'capital' ? 'capital' : 'city' }
  }
  // Some national capitals have no corresponding CSC city. Use the urban point
  // only when Wikidata also identifies it and another record does not cover it.
  for (const [key, p] of places) {
    if (p.ADM0CAP !== 1 || seen.has(key) || !Object.hasOwn(verifiedCities, p.WIKIDATAID)) continue
    if (['CN', 'TW', 'GB'].includes(p.ISO_A2) || urbanTerritories.has(p.ISO_A2)) continue
    const local = citiesByCountry.get(p.ISO_A2) ?? []
    const name = normalized(p.NAME_EN)
    if (local.some(r => normalized(r.name) === name || (Math.abs(r.latitude - p.LATITUDE) < 0.1 &&
      Math.abs(r.longitude - p.LONGITUDE) < 0.1 && r.type === 'capital'))) continue
    const region = regions.find(r => r.country_code === p.ISO_A2 && isRegion(r) && normalized(r.name) === normalized(p.ADM1NAME))
    yield { id: 'wd:' + p.WIKIDATAID, kind: 'city', stateId: region?.id ?? null, zh: p.NAME_ZH,
      row: { country_code: p.ISO_A2, name: p.NAME_EN, latitude: p.LATITUDE, longitude: p.LONGITUDE } }
  }

}
