import { reactive } from 'vue'
import { API_URL } from './api'
import { formatResult } from './helpers/resultFormatter'

const store = reactive({
  currentResults: [],
  queue: [],
  allResults: [],
  currentExperiment: null, // REFACTOR
  currentTab: 0,
  currentResultTab: 0,
  resultPoll: null,
})

function setResult(result) {
  addResult(result)
  store.currentExperiment = null
  clearInterval(store.resultPoll)
}

/**
 * GET request: Ask server for latest calculation
 */
function getCalculation() {
  if (store.currentExperiment) {
    console.log('fetching result')
    try {
      fetch(API_URL + '/experiment/calculation')
        .then((response) => response.json())
        .then((data) => {
          if (data.status == 'done') {
            console.log('done', data)
            // TODO refactor?
            //const clone = JSON.parse(JSON.stringify(data.calculation))
            //setResult(formatResult(clone))
            setResult(formatResult(data.calculation))
          } else if (data.status == 'busy') {
            console.log('busy', data)
          }
        })
    } catch (e) {
      console.log(e) // TODO better error handling, composable
      store.currentExperiment = null
    }
  }
}

// Add a new result to the global current shown results state
function addResult(result) {
  //store.currentResults = [result, ...store.currentResults]
  store.currentResults.push(result)
  store.currentResultTab = store.currentResults.length - 1
  console.log('currentResultTab', store.currentResultTab)
  //console.log(store.currentResults)
}

//Remove result from global current shown results state
function removeResult(index) {
  store.currentResults.splice(index, 1)
}

export { store, addResult, removeResult, getCalculation }
