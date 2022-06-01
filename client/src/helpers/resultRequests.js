/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import { API_URL } from '../api'
import { addResult, store } from '../store'
import { formatResult } from './resultFormatter'

const resultsRoute = '/result/result-by-id'
const url = API_URL + resultsRoute

// Request full result from result ID (timestamp)
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

// Get result back from result ID request
export async function getResult() {
  const response = await fetch(url)
  const data = await response.json()
  return data
}

export async function viewResult(resultId) {
  const data = await loadResult(resultId)
  console.log('Result fetched', data.result)
  addResult(formatResult(data.result))
  viewResultTab()
}

export function viewResultTab() {
  // Make result tab the active tab
  store.currentTab = 3
}
