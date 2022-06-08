/* This program has been developed by students from the bachelor Computer
Science at Utrecht University within the Software Project course. © Copyright
Utrecht University (Department of Information and Computing Sciences) */

import { render, fireEvent } from '@testing-library/vue'
import { test } from 'vitest'
import Results from '../../components/Results.vue'
import { store } from '../../store'

/**
 * Test results tab
 */
test('results tab', async () => {
  // Render results view
  const { getByLabelText, getByText } = render(Results)

  // No results display
  getByText(/No results to show/)

  // Add a result
  // TODO
  // store.addResult({})

  // Test previous results sidebar button
  const button = getByText('Previous Results')
  await fireEvent.click(button)
  // getByText('Previous Results')
  // Check sidebar view/open result text
  // getByText('Open result')
  // getByLabelText('offcanvasRightLabel')
  // getByText('Copy settings')
  for (const header of [
    'ID',
    'Date Time ▲',
    'Name',
    'Tags',
    'Datasets',
    'Approaches',
    'Metrics',
  ]) {
    getByText(header)
  }
})
