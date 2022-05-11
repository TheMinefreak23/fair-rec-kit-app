import { reactive } from 'vue'
import mockdata from '../../server/mock/1647818279_HelloWorld/results-table.json'

// Mockdata result
function mockResult() {
  const testcaption = 'Dataset: LFM-1b, Algorithm: ALS'

  // Add mockdata result to current results
  const mock = {
    caption: testcaption,
    results: mockdata.body,
    headers: mockdata.headers,
  }
  return {
    id: 0,
    metadata: {
      name: 'computation1',
      tags: ['tag1 ', 'tag2 ', 'tag3 ', 'tag4 '],
    },
    result: [mock, mock],
  }
}

const store = reactive({
  currentResults: [mockResult()],
  queue: [],
  allResults: [],
  experimentRunning: false, // TODO refactor out of store?
  currentExperiment: null, // REFACTOR
  currentTab: 0,
})

// Add a new result to the global current shown results state
function addResult(result) {
  store.currentResults = [result, ...store.currentResults]
  //console.log(store.currentResults)
}

//Remove result from global current shown results state
function removeResult(index) {
  store.currentResults.splice(index, 1)
}

export { store, addResult, removeResult }
