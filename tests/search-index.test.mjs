import test from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { normalizeSearchName, searchBucket, searchNames } from '../scripts/search-index.mjs'

const read = async path => JSON.parse(await readFile(new URL('../data/' + path, import.meta.url), 'utf8'))

test('search index routes multilingual city and region names to their country shards', async () => {
  const index = new Map(await Promise.all(Array.from({ length: 128 }, async (_, i) => {
    const bucket = i.toString(16).padStart(2, '0')
    return [bucket, new Map(await read('search/' + bucket + '.json'))]
  })))
  function verify(place, country) {
    for (const term of searchNames(place)) {
      assert.ok(index.get(searchBucket(term)).get(term)?.match(/../g).includes(country), `${country}: ${term}`)
    }
  }
  for (const country of await read('countries.json')) {
    verify(country, country.id)
    for (const region of await read('regions/' + country.id + '.json')) {
      verify(region, country.id)
      for (const child of region.children ?? []) verify(child, country.id)
    }
    for (const city of await read('cities/' + country.id + '.json')) verify(city, country.id)
  }
  assert.ok(index.get(searchBucket('mumbai')).get('mumbai').match(/../g).includes('IN'))
  for (const query of ['拉萨', 'Lhasa', 'la sa', '西藏']) {
    const term = normalizeSearchName(query)
    assert.ok([...index.get(searchBucket(term))].some(([name, countries]) => name.startsWith(term) && countries.match(/../g).includes('CN')))
  }
})
