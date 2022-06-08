/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { render } from '@testing-library/vue'
import DictionaryDisplay from '../../components/Table/DictionaryDisplay.vue'

// TODO test empty params (gives nothing)

/**
 * Test text param display
 */
test('name and text param', async () => {
  // Render Dictionary Display
  const { getByText } = render(DictionaryDisplay, {
    props: { dict: { name: 'foo', params: 'bar' } },
  })

  getByText('bar')
})

/**
 * Test dict param display
 */
test('name and dict param', async () => {
  // Render Dictionary Display
  const { getByText } = render(DictionaryDisplay, {
    props: { dict: { name: 'foo', params: { name: 'bar', params: 'bogo' } } },
  })

  getByText('bogo')
})

/**
 * Test list param display
 */
test('name and list param', async () => {
  // Render Dictionary Display
  const { getByText } = render(DictionaryDisplay, {
    props: {
      dict: {
        name: 'foo',
        params: [
          { name: 'foo1', params: 'bar1' },
          { name: 'foo2', params: 'bar2' },
        ],
      },
    },
  })

  getByText('bar1')
  getByText('bar2')
})
