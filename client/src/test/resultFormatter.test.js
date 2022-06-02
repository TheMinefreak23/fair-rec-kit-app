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
  makeHeader,
  capitalise
} from '../helpers/resultFormatter'

/**
 * Test the formatting of all results
 */
describe('format results', () => {
  // Test a formatted version of an empty array to be empty
  test('empty', () => {
    expect(formatResults([]).length).toBe(0)
  })
  // TODO
})

/**
 * Test the string formatting of an array of items
 */
describe('format multiple items', () => {
  // Test that an empty array gives an empty string
  test('empty', () => {
    expect(formatMultipleItems([])).toBe('')
  })

  // Test that a null array gives None
  test('undefined', () => {
    expect(formatMultipleItems(null)).toBe('None')
  })

  const items = [{ name: 'a' }, { name: 'b' }]
  test('single item', () => {
    expect(formatMultipleItems([items[0]])).toBe(items[0].name)
  })

  test('multiple items', () => {
    expect(formatMultipleItems(items)).toBe('a, b')
  })
})

/*
describe('format result', () => {
  // TODO
  //test('', () => {})
})*/

/**
 * Test the short string description of a dataset
 */
describe('show dataset info', () => {
  // A dataset without parmeters should just show the dataset name
  test('no parameter', () => {
    const dataset = { name: 'foo' }
    expect(showDatasetInfo(dataset)).toBe('Dataset: ' + dataset.name)
  })

  // A dataset with parameters should show both name and parameters
  test('parameter', () => {
    const dataset = { name: 'foo', parameter: 'bar' }
    expect(showDatasetInfo(dataset)).toBe(
      'Dataset: ' + dataset.name + 'with parameters ' + dataset.parameter
    )
  })
})

/**
 * Test evaluation data formatting
 */
describe('format evaluation', () => {
  //TODO
  //test('', () => {})
})

/**
 * Test string formatting (new name) of a metric
 */
describe('format metric', () => {
  // A metric with parameters (k) should show both name and parameters
  test('k metric', () => {
    const metric = {
      name: 'P@K',
      params: [
        {
          name: 'K',
          value: '10',
        },
      ],
    }
    expect(formatMetric(metric)).toBe('P@10')
  })
  // A metric without parameters should just show its name
  test('no parameter metric', () => {
    expect(formatMetric({ name: 'foo' })).toBe('foo')
  })
  // If an empty name is assigned, an empty name is returned
  test('no name', () => {
    expect(formatMetric({ name: '' }).length.toBe(0))
  })
})

/**
 * Test correct header configuration
 */
describe('configure header', () => {
  test('multiple words', () => {
    const header = 'a_b_c_d'
    expect(makeHeader(header).name).toBe('A b c d')
    expect(makeHeader('these_are_multiple_words').name).toBe(
      'These are multiple words'
    )
  })
  test('starts with number', () => {
    const header = '2_isanumber'
    expect(makeHeader(header).name).toBe('2 isanumber')
  })
})

/**
 * Test the capitalise function
 */
 describe('capitalise', () => {
  test('several words', () => {
    const string = 'a random set of words'
    expect(capitalise(string).toBe("A Random Set Of Words"))
  
  })
  test('abbreviations', () => {
    const string = "da"
    expect(capitalise(string).toBe("DA"))
  })
  test('contains numbers', () => {
    const string = "123"
    expect(capitalise(string).toBe("123"))
  })
  test('only spaces', () => {
    const string = "       "
    expect((capitalise(string).length == string.length).toBe(true))
  })
})
