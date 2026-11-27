export interface PlaceNames {
  zh: string | null
  en: string
  pinyin: string | null
}

export interface Country extends PlaceNames {
  id: string
}

export interface Region extends PlaceNames {
  id: string
  country: string
  code: string | null
  aliases?: string[]
  children?: Region[]
}

export interface City extends PlaceNames {
  id: string
  country: string
  region: string | null
  subregion?: string
  officialId?: string
  aliases?: string[]
  kind: 'city' | 'capital' | 'municipality' | 'prefecture' | 'locality'
  lat: number
  lon: number
}

export const countries: readonly Country[]
export function countryFiles(iso2: string): { regions: URL; cities: URL }
