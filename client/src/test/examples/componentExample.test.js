/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import { render } from '@testing-library/vue'
import { test } from 'vitest'
import ExperimentQueue from '../components/ExperimentQueue.vue'

/**
 * Test queue tab content
 */
test('Queue', async () => {
  // get utilities to query component
  const { getByText } = render(ExperimentQueue)

  getByText('Queue')
  getByText('Current experiment: None')
})
