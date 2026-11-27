import assert from 'node:assert/strict'
import { createHash, randomUUID } from 'node:crypto'
import { mkdir, mkdtemp, readFile, rename, rm, writeFile } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { gunzipSync, gzipSync } from 'node:zlib'
import searchLocalities from '../sources/search-localities.json' with { type: 'json' }
import municipalFollowup from '../sources/municipal-followup-2026.json' with { type: 'json' }
import majorCitySupplement from '../sources/major-city-supplement-2026.json' with { type: 'json' }
import cityBenchmarks from '../sources/city-benchmarks.json' with { type: 'json' }
import { applyOfficialData, mergeReviewedCities } from './official/apply.mjs'
import { coverageMarkdown } from './coverage.mjs'
import { isRegion, selectCities } from './city-scope.mjs'
import { coordinate, placeNames } from './transform.mjs'

const root = fileURLToPath(new URL('../', import.meta.url))
const cache = path.join(root, '.cache/csc')
const lock = JSON.parse(await readFile(path.join(root, 'sources.lock.json'), 'utf8'))
const corrections = JSON.parse(await readFile(path.join(root, 'corrections/names.json'), 'utf8'))
const usedCorrections = new Set()

async function source(file) {
  const spec = lock.files.find(entry => entry.file === file)
  const local = path.join(cache, file)
  let bytes
  try {
    bytes = await readFile(local)
  } catch (error) {
    if (error.code !== 'ENOENT') throw error
  }
  const digest = data => createHash('sha256').update(data).digest('hex')
  if (!bytes || digest(bytes) !== spec.sha256) {
    const res = await fetch(spec.url, { signal: AbortSignal.timeout(120_000) })
    if (!res.ok) throw new Error(file + ' download failed: HTTP ' + res.status)
    bytes = Buffer.from(await res.arrayBuffer())
    assert.equal(digest(bytes), spec.sha256, file + ' does not match sources.lock.json')
    const tmp = local + '.' + randomUUID()
    await writeFile(tmp, bytes)
    await rename(tmp, local)
  }
  return JSON.parse(file.endsWith('.gz') ? gunzipSync(bytes).toString('utf8') : bytes.toString('utf8'))
}

function names(row, country, id, zh) {
  const fix = corrections[id]
  if (fix) usedCorrections.add(id)
  return placeNames(row, country, { zh, ...fix })
}

await mkdir(cache, { recursive: true })
const chinaAreaNames = new Map([['TW', '台湾省'], ['HK', '香港特别行政区'], ['MO', '澳门特别行政区']])
const countries = []
const groups = new Map()
for (const row of await source('countries.json')) {
  const id = row.iso2
  assert.match(id, /^[A-Z]{2}$/)
  assert.ok(!groups.has(id), 'Duplicate ISO code ' + id)
  if (!chinaAreaNames.has(id)) countries.push({ id, ...names(row, id, id) })
  groups.set(id, { regions: [], cities: [] })
}
countries.sort((a, b) => a.id < b.id ? -1 : 1)

const regions = new Map()
const rawRegions = await source('regions.json')
const parents = new Map(rawRegions.map(r => [r.id, r]))
for (const row of rawRegions.filter(isRegion)) {
  const country = row.country_code
  const id = 'csc:r:' + row.id
  assert.ok(groups.has(country) && !regions.has(row.id), 'Invalid region link or duplicate: ' + id)
  const region = { id, country, code: row.iso3166_2 || null, ...names(row, country, id) }
  regions.set(row.id, region)
  groups.get(country).regions.push(region)
}

const cityIds = new Set()
const divisions = await source('china-divisions.json')
const places = await source('world-places.geojson')
const rawCities = await source('cities.json.gz')
const snapshot = await readFile(path.join(root, lock.wikidata.file))
assert.equal(createHash('sha256').update(snapshot).digest('hex'), lock.wikidata.sha256)
const verifiedCities = JSON.parse(gunzipSync(snapshot))
for (const { id, row, stateId, zh, kind } of selectCities(divisions, rawRegions, rawCities, places.features, verifiedCities)) {
  const country = row.country_code
  let state = parents.get(stateId)
  const visited = new Set()
  while (state && !regions.has(state.id)) {
    assert.ok(!visited.has(state.id), 'Cyclic region ' + state.id)
    visited.add(state.id)
    state = parents.get(Number(state.parent_id))
  }
  const region = state && regions.get(state.id)
  assert.ok(!cityIds.has(id) && groups.has(country), 'Duplicate city or unknown country: ' + id)
  assert.ok(!region || region.country === country, 'Invalid region for ' + id)
  cityIds.add(id)
  groups.get(country).cities.push({
    id, country, region: region?.id ?? null, kind, ...names(row, country, id, zh),
    lat: coordinate(corrections[id]?.lat ?? row.latitude, 90), lon: coordinate(corrections[id]?.lon ?? row.longitude, 180)
  })
}
async function frozenRoster(spec) {
  const bytes = await readFile(path.join(root, spec.file))
  assert.equal(createHash('sha256').update(bytes).digest('hex'), spec.sha256, spec.file)
  return JSON.parse(gunzipSync(bytes))
}
const officialRosters = Object.assign({}, await frozenRoster(lock.nationalRosters), await frozenRoster(lock.idPlRosters))
applyOfficialData(groups, officialRosters)
mergeReviewedCities(groups, await frozenRoster(lock.nationalReview))
mergeReviewedCities(groups, await frozenRoster(lock.singleCityReview))
mergeReviewedCities(groups, municipalFollowup)
mergeReviewedCities(groups, searchLocalities)
mergeReviewedCities(groups, await frozenRoster(lock.municipalRosters))
mergeReviewedCities(groups, await frozenRoster(lock.chinesePlaceNames))
mergeReviewedCities(groups, majorCitySupplement)

// Keep the regional URLs as filtered views of the same nationally indexed records.
const china = groups.get('CN')
const regionViews = new Map()
for (const [code, name] of chinaAreaNames) {
  const province = china.regions.find(r => r.code === 'CN-' + code)
  assert.ok(province, 'Missing Chinese province-level entry for ' + code)
  province.aliases = [name]
  const local = groups.get(code)
  if (local.regions.length) province.children = local.regions.map(r => ({ ...r, country: 'CN' }))
  const cities = local.cities.map(city => ({
    ...city, country: 'CN', region: province.id, ...(city.region ? { subregion: city.region } : {})
  }))
  china.cities.push(...cities)
  regionViews.set(code, { regions: [province], cities })
  groups.delete(code)
}

const finalIds = new Set()
let regionCount = 0
for (const [country, group] of groups) {
  const stateIds = new Set(group.regions.map(r => r.id))
  assert.equal(stateIds.size, group.regions.length)
  regionCount += stateIds.size
  for (const city of group.cities) {
    assert.ok(!finalIds.has(city.id) && city.country === country, 'Invalid final city ' + city.id)
    assert.ok(city.region === null || stateIds.has(city.region), 'Invalid final region for ' + city.id)
    coordinate(city.lat, 90)
    coordinate(city.lon, 180)
    const pinyin = corrections[city.id]?.pinyin
    if (pinyin && pinyin !== city.pinyin) {
      city.pinyin = placeNames({ id: city.id, name: city.en }, country, { zh: city.zh, pinyin }).pinyin
      usedCorrections.add(city.id)
    }
    finalIds.add(city.id)
  }
}
for (const id of Object.keys(corrections)) assert.ok(usedCorrections.has(id), 'Unused name correction: ' + id)

const stage = await mkdtemp(path.join(root, '.cache/build-'))
const json = value => JSON.stringify(value) + '\n'
async function writeJSON(file, value) {
  await writeFile(path.join(stage, file), json(value))
}

try {
  await mkdir(path.join(stage, 'cities'))
  await mkdir(path.join(stage, 'regions'))
  await writeJSON('countries.json', countries)
  const byCountry = {}
  const kinds = {}
  const totals = { countries: countries.length, countriesWithCities: 0, regions: regionCount, cities: finalIds.size, withChinese: 0, withPinyin: 0, withoutRegion: 0 }
  for (const { id } of countries) {
    const { regions, cities } = groups.get(id)
    const withChinese = cities.filter(place => place.zh).length
    const withPinyin = cities.filter(place => place.pinyin).length
    const withoutRegion = cities.filter(place => !place.region).length
    for (const { kind } of cities) kinds[kind] = (kinds[kind] ?? 0) + 1
    if (cities.length) totals.countriesWithCities++
    totals.withChinese += withChinese
    totals.withPinyin += withPinyin
    totals.withoutRegion += withoutRegion
    const cityReference = cityBenchmarks[id] ?? { status: 'pending' }
    byCountry[id] = { cityReference, regions: regions.length, cities: cities.length, withChinese, withPinyin, withoutRegion, gzipBytes: gzipSync(json(cities)).length }
    await writeJSON('cities/' + id + '.json', cities)
    await writeJSON('regions/' + id + '.json', regions)
  }
  for (const [code, view] of regionViews) {
    await writeJSON('cities/' + code + '.json', view.cities)
    await writeJSON('regions/' + code + '.json', view.regions)
  }
  const coverage = { sourceVersion: lock.version, totals, kinds, byCountry }
  await writeJSON('coverage.json', coverage)
  // Only switch to the replacement once every country and reference has been checked.
  const output = path.join(root, 'data')
  const previous = stage + '-previous'
  let moved = false
  try {
    await rename(output, previous)
    moved = true
  } catch (error) {
    if (error.code !== 'ENOENT') throw error
  }
  try {
    await rename(stage, output)
  } catch (error) {
    if (moved) await rename(previous, output)
    throw error
  }
  if (moved) await rm(previous, { recursive: true })
  await writeFile(path.join(root, 'COVERAGE.md'), coverageMarkdown(coverage))
  console.log(totals)
} finally {
  await rm(stage, { recursive: true, force: true })
}
