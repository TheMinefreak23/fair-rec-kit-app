/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import { render, fireEvent } from '@testing-library/vue'
import { test } from 'vitest'
import Result from '../components/Result.vue'

test('subResult', async () => {
  // get utilities to query component
  const { getAllByText, getByText } = render(Result, {
    props: {
      headers: [{ name: 'foo' }, { name: 'bar' }],
      result: {
        metadata: {
          id: 1234,
          name: 'testcomputation',
          tags: ['tag1', 'tag2'],
        },
        result: [
          {
            caption: 'a test',
            results: [{ approach: 'number1' }, { approach: 'number2' }],
            headers: [{ name: 'foo' }, { name: 'bar' }],
          },
        ],
      },
    },
  })

  getByText('Tags:')
  getByText('Result')
})

/**
 * Test combineResults functionality
 */
describe('combine dataset-approach combinations', () => {
  test('starts with number', () => {
    const result = [
        {
          caption: 'test',
          results: [{ approach: 'number1' }, { approach: 'number2' }],
          headers: [{ name: 'foo' }, { name: 'bar' }],
        },
      ]
    //expect(Result.combineResults(result).length).toBe(2)
  })
})

// userrecs
// header change
