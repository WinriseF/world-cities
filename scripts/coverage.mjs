export function coverageMarkdown({ totals, byCountry }) {
  const format = n => n.toLocaleString('en-US')
  const labels = { 'reference-checked': '已核验', 'major-cities': '主要城市', partial: '部分核实', pending: '待核实', 'not-applicable': '不适用' }
  const refs = Object.values(byCountry).map(c => c.cityReference.status)
  const count = status => refs.filter(s => s === status).length
  const rows = Object.entries(byCountry).sort(([a], [b]) => a.localeCompare(b)).map(([id, c]) =>
    `| ${id} | ${format(c.regions)} | ${format(c.cities)} | ${labels[c.cityReference.status]} |`
  )
  return [
    '# 数据覆盖', '',
    `国家和地区：${format(totals.countries)} · 一级行政区：${format(totals.regions)} · 地点：${format(totals.cities)}`,
    '', `已核验：${count('reference-checked')} · 主要城市：${count('major-cities')} · 不适用：${count('not-applicable')}`,
    '', '地点包括城市、同级行政单位及代表地点。', '',
    '| 国家或地区 | 一级行政区 | 地点数量 | 状态 |',
    '| --- | ---: | ---: | --- |', ...rows, ''
  ].join('\n')
}
