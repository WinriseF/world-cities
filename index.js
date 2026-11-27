export { default as countries } from './data/countries.json' with { type: 'json' }

/** Resolve the two JSON files relative to this installation or CDN URL. */
export function countryFiles(iso2) {
  if (typeof iso2 !== 'string' || !/^[a-z]{2}$/i.test(iso2)) throw new TypeError('Expected a two-letter country code')
  const code = iso2.toUpperCase()
  return {
    regions: new URL('./data/regions/' + code + '.json', import.meta.url),
    cities: new URL('./data/cities/' + code + '.json', import.meta.url)
  }
}
