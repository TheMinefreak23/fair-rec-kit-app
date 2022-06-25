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

// App tabs (TODO use these for dynamic app order)
const APP_TABS = [
  'New Experiment',
  'Experiment Queue',
  'Results',
  'All Results',
  'Documentation',
  'Music Detail',
]

/**
 * Poll for the current experiment result
 */
function pollForResult() {
  // Switch to queue
  store.currentTab = APP_TABS.indexOf('Experiment Queue')
  const interval = 300
  store.resultPoll = setInterval(getCalculation, interval)
}

/**
 * GET request: Ask server for latest calculation
 */
function getCalculation() {
  if (store.currentExperiment.status !== status.notAvailable) {
    try {
      fetch(API_URL + '/experiment/')
        .then((response) => response.json())
        .then((data) => {
          console.log('polling experiment, status:', data.status)
          store.currentExperiment.status = data.status

          // Update queue and progress while waiting for a result
          getQueue()
          if ([status.done, status.aborted].includes(data.status)) {
            clearInterval(store.resultPoll)
            if (data.status === status.done)
              addResultById(data.experimentID, false)
            console.log('DONE or ABORTED!!')
          }
        })
    } catch (e) {
      console.log(e)
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

  // Update latest experiment (queue item)
  if (data.current && data.current.status !== status.notAvailable) {
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
  store.currentResults.push(result)
  store.currentResultTab = store.currentResults.length - 1
}

/**
 * Remove result from global current shown results state
 * @param {Int} index - The index of the result to remove
 */
function removeResult(index) {
  store.currentResults.splice(index, 1)
}

export {
  store,
  APP_TABS,
  addResult,
  removeResult,
  getCalculation,
  getQueue,
  pollForResult,
}
