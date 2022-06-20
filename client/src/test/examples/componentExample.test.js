/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import { fireEvent, render } from '@testing-library/vue'
import { test } from 'vitest'
import TestComponent from '../mock/TestComponent.vue'

/**
 * Test queue tab content
 */
test('Queue', async () => {
  // get utilities to query component
  const { getByText } = render(TestComponent, {
    props: { test: 'foo' },
  })

  getByText('foo')

  const button = getByText('increment')

  await fireEvent.click(button)

  getByText('counter: 1')
})
