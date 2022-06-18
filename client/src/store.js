import { reactive } from 'vue'
import { API_URL } from './api'
import { status } from './helpers/queueFormatter'
import { addResultById } from './helpers/resultRequests'

const store = reactive({
  settings: {}, // Experiment settings (NOTE: only used for copying settings for now)
  currentResults: [], // Current opened results
  queue: [], // Experiment queue
  allResults: [], // Previous results (overview)
  currentExperiment: { status: status.notAvailable }, // The current experiment // REFACTOR
  currentTab: 0, // Current open tab view
  currentResultTab: 0, // Current tab open in the result tab
  resultPoll: null, // Polls when there is an active experiment (result, queue, progress)
  toast: null, // Toast settings to show in the toast over the app
})

/**
 * Poll for the current experiment result
 */
function pollForResult() {
  const interval = 300
  store.resultPoll = setInterval(getCalculation, interval)
}

/**
 * GET request: Ask server for latest calculation
 */
function getCalculation() {
  if (store.currentExperiment.status !== status.notAvailable) {
    // console.log('fetching result')
    try {
      fetch(API_URL + '/experiment/')
        .then((response) => response.json())
        .then((data) => {
          console.log('polling experiment, status:', data.status)
          store.currentExperiment.status = data.status
          if ([status.done, status.aborted].includes(data.status)) {
            clearInterval(store.resultPoll)
            if (data.status === status.done)
              // addResult(formatResult(data.calculation))
              // addResultById(data.calculation.timestamp.stamp, false)
              addResultById(data.experimentID, false)
            console.log('DONE or ABORTED!!')
          }

          // Update queue and progress while waiting for a result
          getQueue()
        })
    } catch (e) {
      console.log(e) // TODO better error handling, composable
      store.currentExperiment = null
    }
  }
}

/**
 * GET request: Get the experiment queue from the server
 */
async function getQueue() {
  const response = await fetch(API_URL + '/experiment/queue')
  const data = await response.json()
  // console.log('queue latest', data.current)

  // Update latest experiment (queue item)
  if (data.current && data.current.status !== status.notAvailable) {
    // console.log(data.current)
    store.currentExperiment = data.current
    console.log('progress:', data.current.progress)
  }
  store.queue = data.queue
}

/**
 * Add a new result to the global current shown results state
 * @param {Object} result - The new result
 */
function addResult(result) {
  // store.currentResults = [result, ...store.currentResults]
  /* console.log(
    'currentResults before addResult',
    JSON.parse(JSON.stringify(store.currentResults))
  ) */
  store.currentResults.push(result)
  /* console.log(
    'currentResults after addResult',
    JSON.parse(JSON.stringify(store.currentResults))
  ) */
  store.currentResultTab = store.currentResults.length - 1
  // console.log('currentResultTab', store.currentResultTab)
  // console.log(store.currentResults)
}

/**
 * Remove result from global current shown results state
 * @param {Int} index - The index of the result to remove
 */
function removeResult(index) {
  store.currentResults.splice(index, 1)
  // console.log(store.currentResultTab)
}

export {
  store,
  addResult,
  removeResult,
  getCalculation,
  getQueue,
  pollForResult,
}
