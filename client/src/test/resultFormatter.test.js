/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import {
  formatResults,
  formatMultipleItems,
  formatResult,
  showDatasetInfo,
  formatMetric,
  formatEvaluation,
} from '../helpers/resultFormatter'

describe('format results', () => {
  test('empty', () => {
    expect(formatResults([]).length).toBe(0)
  })
  // TODO
})

describe('format multiple items', () => {
  test('empty', () => {
    expect(formatMultipleItems([])).toBe('')
  })

  test('undefined', () => {
    expect(formatMultipleItems(null)).toBe('NULL')
  })

  const items = [{ name: 'a' }, { name: 'b' }]
  test('single item', () => {
    expect(formatMultipleItems([items[0]])).toBe(items[0].name)
  })

  test('multiple items', () => {
    expect(formatMultipleItems(items)).toBe('a, b')
  })
})

describe('format result', () => {
  // TODO
  //test('', () => {})
})

describe('show dataset info', () => {
  test('no parameter', () => {
    const dataset = { name: 'foo' }
    expect(showDatasetInfo(dataset)).toBe('Dataset: ' + dataset.name)
  })

  test('parameter', () => {
    const dataset = { name: 'foo', parameter: 'bar' }
    expect(showDatasetInfo(dataset)).toBe(
      'Dataset: ' + dataset.name + 'with parameters ' + dataset.parameter
    )
  })
})

describe('format evaluation', () => {
  //TODO
  //test('', () => {})
})

describe('format metric', () => {
  test('k metric', () => {
    const metric = { name: 'foo k', params: [{ value: 0 }] }
    expect(formatMetric(metric)).toBe('foo 0')
  })
  test('no parameter metric', () => {
    expect(formatMetric({ name: 'foo' })).toBe('foo')
  })
})
