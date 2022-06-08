/* This program has been developed by students from the bachelor Computer
Science at Utrecht University within the Software Project course. © Copyright
Utrecht University (Department of Information and Computing Sciences) */

import { render } from '@testing-library/vue'
import { test } from 'vitest'
import Results from '../../components/Results.vue'
import { store } from '../../store'

/**
 * Test results tab
 */
test('results tab', async () => {
  // Render results view
  const { getByText } = render(Results)

  // No results display
  getByText(/No results to show/)

  // Add a result
  // TODO
  // store.addResult({})
})
