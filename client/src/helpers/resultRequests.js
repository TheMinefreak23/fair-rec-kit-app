/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { API_URL } from '../api'
import { addResult, store } from '../store'
import { formatResult } from './resultFormatter'

const resultsRoute = '/result/result-by-id'
const url = API_URL + resultsRoute

/**
 * Request full result from result ID (timestamp)
 * @param {Int} resultId - The result ID (timestamp)
 * @return {Object} The full result data
 */
export async function loadResult(resultId) {
  console.log('Loading result with ID:' + resultId)

  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: resultId }),
  }
  await fetch(url, requestOptions)
  return getResult()
}

/**
 * Get result back from result ID request
 * @return {Object} The full result data
 */
export async function getResult() {
  const response = await fetch(url)
  const data = await response.json()
  return data.result
}

/**
 * Open a result in a new (or existing) tab by its ID
 * @param {Int} resultId - The result ID
 * @param {Boolean} view - Whether to view the result in the result tab
 */
export async function addResultById(resultId, view = true) {
  // Check if the selected result is already loaded
  const index = store.currentResults
    .map((result) => result.id)
    .indexOf(resultId)
  if (index === -1) {
    const data = await loadResult(resultId)
    console.log('Result fetched', data.result)
    addResult(formatResult(data.result))
  } else store.currentResultTab = index
  if (view) viewResultTab()
}

/**
 * Make result tab the active tab
 */
export function viewResultTab() {
  store.currentTab = 3
}
