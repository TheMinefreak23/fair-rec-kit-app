//import { log } from 'console'
import { reactive } from 'vue'
import mockdata from '../api/mock/1647818279_HelloWorld/results-table.json'

// Mockdata result
function mockResult() {
  const testcaption = 'Dataset: LFM-1b, Algorithm: ALS'

  // Add mockdata result to current results
  const mock = {
    caption: testcaption,
    results: mockdata.body,
    headers: mockdata.headers,
  }
  return { id: 0, name: 'computation1', result: [mock, mock] }
}

const store = reactive({
  currentResults: [mockResult()],
  queue: [],
  allResults: [],
})

// Add a new result to the global current shown results state
function addResult(result) {
  store.currentResults = [result, ...store.currentResults]
  //console.log(store.currentResults)
}

//Remove result from global current shown results state
function removeResult(result) {

  for(var i=0; i<store.currentResults.length; i++){
    
    if(store.currentResults[i].id === result) {
      store.currentResults.splice(i,1);
      i--;

    }
    
  }
}

export { store, addResult, removeResult }
