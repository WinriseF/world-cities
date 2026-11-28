export function normalizeSearchName(value) {
  return String(value ?? '').normalize('NFKD').replace(/\p{M}/gu, '').toLowerCase().replace(/[^\p{L}\p{N}]/gu, '')
}

export function searchBucket(term) {
  const chars = [...term]
  const prefix = chars.slice(0, /\p{Script=Han}/u.test(chars[0]) ? 1 : 2)
  return (prefix.reduce((hash, char) => hash * 31 + char.codePointAt(0), 0) % 128).toString(16).padStart(2, '0')
}

// English and alternative multi-word names are also searchable from a later word.
export function searchNames(place) {
  const names = [place.zh, place.en, place.pinyin, place.code, ...(place.aliases ?? [])].map(normalizeSearchName)
  for (const name of [place.en, ...(place.aliases ?? [])]) {
    const words = String(name ?? '').normalize('NFKD').replace(/\p{M}/gu, '').toLowerCase().split(/[^\p{L}\p{N}]+/gu).filter(Boolean)
    for (let i = 1; i < words.length; i++) {
      const term = words.slice(i).join('')
      if (/^\p{Script=Latin}/u.test(term) && term.length >= 3) names.push(term)
    }
  }
  return [...new Set(names.filter(Boolean))]
}

// Store only normalized names and country codes; the source records stay in their country shards.
export function createSearchIndex(countries, groups) {
  const buckets = Array.from({ length: 128 }, () => new Map())
  function add(place, country) {
    for (const term of searchNames(place)) {
      const bucket = buckets[parseInt(searchBucket(term), 16)]
      if (!bucket.has(term)) bucket.set(term, new Set())
      bucket.get(term).add(country)
    }
  }
  for (const country of countries) {
    add(country, country.id)
    const { regions, cities } = groups.get(country.id)
    for (const region of regions) {
      add(region, country.id)
      for (const child of region.children ?? []) add(child, country.id)
    }
    for (const city of cities) add(city, country.id)
  }
  return buckets.map((bucket, index) => [index.toString(16).padStart(2, '0'), [...bucket].sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0).map(([term, codes]) => [term, [...codes].sort().join('')])])
}
