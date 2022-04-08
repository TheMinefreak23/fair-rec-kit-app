// store.js
import { reactive } from 'vue'

const store = reactive({ currentResults: [], queue: [] })

function addResult(result) {
  store.currentResults = [result, ...store.currentResults]
  console.log(store.currentResults)
}

export { store, addResult }
