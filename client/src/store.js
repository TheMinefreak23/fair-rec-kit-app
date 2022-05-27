import { reactive } from 'vue'
import { API_URL } from './api'
import { formatResult } from './helpers/resultFormatter'
import { status } from './helpers/queueFormatter'

const store = reactive({
  currentResults: [],
  queue: [],
  allResults: [],
  currentExperiment: { status: status.notAvailable }, // REFACTOR
  currentTab: 0,
  currentResultTab: 0,
  resultPoll: null, // polls when there is an active experiment (result, queue, progress)
})

function pollForResult() {
  const interval = 300
  store.resultPoll = setInterval(getCalculation, interval)
}

/**
 * GET request: Ask server for latest calculation
 */
function getCalculation() {
  if (store.currentExperiment) {
    //console.log('fetching result')
    try {
      fetch(API_URL + '/experiment/calculation')
        .then((response) => response.json())
        .then((data) => {
          store.currentExperiment.status = data.status
          if (data.status == status.done || data.status == status.aborted) {
            clearInterval(store.resultPoll)
            if (data.status == status.done)
              addResult(formatResult(data.calculation))
          } else if (data.status == status.active) {
            // Update queue and progress while waiting for a result
            getQueue()
          }
          console.log(
            'polling experiment, status:',
            data.status,
            'progress:',
            store.currentExperiment && store.currentExperiment.progress
          )
        })
    } catch (e) {
      console.log(e) // TODO better error handling, composable
      store.currentExperiment = null
    }
  }
}

async function getQueue() {
  const response = await fetch(API_URL + '/experiment/queue')
  const data = await response.json()
  //store.queue = formatResults(data).map(x=>x.omit(x,'ID'))
  //store.queue = formatResults(data)
  //console.log('queue', data.queue)
  store.queue = data.queue
  if (data.current && data.current.status == status.active) {
    store.currentExperiment = data.current
  }
}

// Add a new result to the global current shown results state
function addResult(result) {
  //store.currentResults = [result, ...store.currentResults]
  /*console.log(
    'currentResults before addResult',
    JSON.parse(JSON.stringify(store.currentResults))
  )*/
  store.currentResults.push(result)
  /*console.log(
    'currentResults after addResult',
    JSON.parse(JSON.stringify(store.currentResults))
  )*/
  store.currentResultTab = store.currentResults.length - 1
  //console.log('currentResultTab', store.currentResultTab)
  //console.log(store.currentResults)
}

//Remove result from global current shown results state
function removeResult(index) {
  store.currentResults.splice(index, 1)
}

export {
  store,
  addResult,
  removeResult,
  getCalculation,
  getQueue,
  pollForResult,
}
