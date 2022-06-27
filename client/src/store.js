import { reactive } from 'vue'
import { API_URL } from './api'
import { progress, status } from './helpers/queueFormatter'
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
  polling: false,
  toast: null, // Toast settings to show in the toast over the app
})

// App tabs and order (TODO use these for dynamic app order)
const tabs = {
  newExperiment: 'New Experiment',
  experimentQueue: 'Experiment Queue',
  results: 'Results',
  allResults: 'All Results',
  documentation: 'Documentation',
  musicDetail: 'Music Detail',
}

const APP_TABS = [
  tabs.newExperiment,
  tabs.experimentQueue,
  tabs.results,
  tabs.allResults,
  tabs.documentation,
  tabs.musicDetail,
]

function switchToTab(tab) {
  console.log(tab, APP_TABS.indexOf(tab))
  store.currentTab = APP_TABS.indexOf(tab)
}

/**
 * Poll for the current experiment result
 */
function pollForResult() {
  if (!store.polling) {
    store.polling = true
    // Switch to queue
    switchToTab(tabs.experimentQueue)
    const interval = 600
    store.resultPoll = setInterval(getExperiment, interval)
  }
}

/**
 * GET request: Ask server for latest calculation
 */
function getExperiment() {
  if (
    store.currentExperiment.status !== status.notAvailable &&
    store.currentExperiment.progress !== progress.finished &&
    store.polling
  ) {
    try {
      fetch(API_URL + '/experiment/')
        .then((response) => response.json())
        .then((data) => {
          // console.log('polling experiment, status:', data.status)
          // console.log('progress:', data.progress)

          if ([status.done, status.aborted].includes(data.status)) {
            store.polling = false
            clearInterval(store.resultPoll)
            if (data.status === status.done) {
              addResultById(data.timestamp.stamp, false, true)
            }
            console.log('DONE or ABORTED!!')
          }
          store.currentExperiment = data

          // Update queue while waiting for a result
          getQueue()
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
  /* console.log(
    'queue | data current',
    data.current,
    'current experiment',
    store.currentExperiment
  ) */

  // Update latest experiment (queue item)
  if (data.current && data.current.status !== status.notAvailable) {
    // New experiment
    if (
      data.current.status === status.active &&
      store.currentExperiment.status === status.notAvailable
    ) {
      store.currentExperiment = data.current
      pollForResult()
      store.polling = true
      // console.log('new experiment started running')
    }
  }

  // Update queue
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
  tabs,
  switchToTab,
  addResult,
  removeResult,
  getExperiment as getCalculation,
  getQueue,
  pollForResult,
}
