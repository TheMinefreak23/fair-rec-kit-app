/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { API_URL } from '../api'
import { addResult, tabs, store, switchToTab } from '../store'
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
 * @param {Boolean} newResult - Whether we just ran the experiment
 */
export async function addResultById(resultId, view = true, newResult = false) {
  if (newResult) store.polling = false
  console.log('addResultById', resultId)
  // Check if the selected result is already loaded
  const index = store.currentResults
    .map((result) => result.id)
    .indexOf(resultId)
  if (index === -1 || newResult) {
    const dataResult = await loadResult(resultId)
    console.log('Result fetched', dataResult)
    const formatted = formatResult(dataResult)
    if (index !== -1) store.currentResults[index] = formatted // Update result
    else addResult(formatted)
  } else {
    store.currentResultTab = index
  }
  if (view) viewResultTab()
}

/**
 * Make result tab the active tab
 */
export function viewResultTab() {
  switchToTab(tabs.results)
}
