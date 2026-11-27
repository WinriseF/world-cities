export function coverageMarkdown({ totals, byCountry }) {
  const format = n => n.toLocaleString('en-US')
  const statusLabels = { 'reference-checked': '所列名录已核对', 'major-cities': '主要城市收录（非完整名录）', partial: '部分核实', pending: '待核实', 'not-applicable': '市级口径不适用' }
  const refs = Object.values(byCountry).map(c => c.cityReference.status)
  const full = refs.filter(s => s === 'reference-checked').length
  const major = refs.filter(s => s === 'major-cities').length
  const applicable = refs.filter(s => s !== 'not-applicable').length
  const rows = Object.entries(byCountry).sort(([a], [b]) => a.localeCompare(b)).map(([id, c]) => {
    const ref = c.cityReference
    return '| ' + [id, format(c.cities), statusLabels[ref.status], ref.scope || '收录尺度待核实'].join(' | ') + ' |'
  })
  return [
    '# 数据覆盖', '',
    '国家或地区索引有 ' + format(totals.countries) + ' 项，其中 ' + format(totals.countriesWithCities) + ' 项有可检索地点。',
    '共 ' + format(totals.regions) + ' 个一级行政区、' + format(totals.cities) + ' 条可检索地点记录。具有中文名的地点为 ' +
      format(totals.withChinese) + ' 个，具有拼音的地点为 ' + format(totals.withPinyin) + ' 个。',
    '共有 ' + format(totals.withoutRegion) + ' 个地点没有适用或可核实的一级行政区。',
    '', `完整名录核验：${full}/${applicable}；主要城市优先收录（不保证法定名录完整）：${major} 个国家。`,
    '', '全国记录归入 CN。大陆收录 293 个地级市、4 个直辖市及 40 个同级自治州、地区和盟，台湾收录 9 个市，香港和澳门各收录一个代表点。台湾的 22 个县市可在省级记录的 children 中查询。', '',
    '下表的数量按分片内的地点记录计数，包含各地名录收录的市、市镇及另行保留的政府驻地。各行的核验结果仅适用于该行所列范围。', '',
    '| 国家或地区码 | 收录条数 | 核验状态 | 当地收录及核验范围 |',
    '| --- | ---: | --- | --- |', ...rows, '',
    '全球应收城市总数仍待逐国核实。各地按法定市及与市平级的自治建制确定范围。马里、利比里亚、乍得、伊拉克、叙利亚按主要城市优先收录，不宣称法定名录完整；其他缺少名录的地区记为待核实，有充分依据证明该地没有适用建制才记为不适用。', '',
    '国际数据按来源可核实的城市记录统计。各国城市建制和资料完备程度不同，以上数字表示本包的收录量。完整分国统计见 [coverage.json](data/coverage.json)。', ''
  ].join('\n')
}
