import { pinyin } from 'pinyin-pro'

const han = /\p{Script=Han}/u
const nativeChinese = new Set(['CN', 'HK', 'MO', 'TW'])

export function placeNames(row, country, correction = {}) {
  const chinese = [
    correction.zh, row.translations?.['zh-CN'], row.translations?.zh,
    nativeChinese.has(country) ? row.native : null
  ].find(value => typeof value === 'string' && han.test(value))
  const zh = chinese?.trim() || null
  const en = (correction.en || row.translations?.en || row.name).trim()
  if (!en) throw new Error('Missing primary name: ' + row.id)

  let reading = null
  if (zh) {
    const words = pinyin(zh, { toneType: 'none', type: 'array', nonZh: 'consecutive' }).join(' ').toLowerCase()
    // Unrecognized Han characters would otherwise silently disappear from the reading.
    if (!han.test(words)) reading = words.match(/[a-züê0-9]+/g)?.join(' ') || null
  }
  if (correction.pinyin) {
    if (!zh || !/^[a-züê0-9]+(?: [a-züê0-9]+)*$/.test(correction.pinyin)) throw new Error('Invalid pinyin override: ' + row.id)
    reading = correction.pinyin
  }
  return { zh, en, pinyin: reading }
}

export function coordinate(value, limit) {
  if (value == null || String(value).trim() === '') throw new Error('Missing coordinate')
  const n = Number(value)
  if (!Number.isFinite(n) || Math.abs(n) > limit) throw new Error('Invalid coordinate: ' + value)
  return n
}
