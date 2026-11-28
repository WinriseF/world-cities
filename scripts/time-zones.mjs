import assert from 'node:assert/strict'
import { find } from 'geo-tz/all'

export function assignTimeZones(groups, zoneTab) {
  const zonesByCountry = new Map()
  for (const line of zoneTab.split('\n')) {
    if (!line || line.startsWith('#')) continue
    const [country, , zone] = line.split('\t')
    const zones = zonesByCountry.get(country) ?? []
    zones.push(zone)
    zonesByCountry.set(country, zones)
  }
  for (const [country, { regions, cities }] of groups) {
    const regionCodes = new Map(regions.map(region => [region.id, region.code]))
    const regionZones = new Map()
    const unresolved = []
    for (const city of cities) {
      const area = country === 'CN' && ['CN-TW', 'CN-HK', 'CN-MO'].includes(regionCodes.get(city.region))
        ? regionCodes.get(city.region).slice(3) : country
      const expected = zonesByCountry.get(area) ?? []
      // Prefer the official timekeeping zone where an area has only one.
      const matches = area === 'CN' ? ['Asia/Shanghai'] : expected.length === 1 ? expected : find(city.lat, city.lon)
      const timeZone = expected.length ? matches.find(zone => expected.includes(zone)) : matches[0]
      if (!timeZone) {
        unresolved.push(city)
        continue
      }
      city.timeZone = timeZone
      const peers = regionZones.get(city.region) ?? new Set()
      peers.add(timeZone)
      regionZones.set(city.region, peers)
    }
    // For a border point outside its recorded country, use its region only if unambiguous.
    for (const city of unresolved) {
      const peers = regionZones.get(city.region)
      assert.ok(city.region && peers?.size === 1, `Unresolved time zone: ${city.id}`)
      city.timeZone = [...peers][0]
    }
  }
}
