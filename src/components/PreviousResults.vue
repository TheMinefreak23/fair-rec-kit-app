<script setup>
import Table from './Table.vue'
import { onMounted, ref, watch } from 'vue'
import { formatResults, formatResult } from '../helpers/resultFormatter.js'

import { store } from '../store.js'

const exResults = ref([
  { id: 1, age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
  { id: 2, age: 21, first_name: 'Larsen', last_name: 'Shaw' },
  { id: 3, age: 89, first_name: 'Geneva', last_name: 'Wilson' },
  { id: 4, age: 38, first_name: 'Jami', last_name: 'Carney' },
])
const exHeaders = ref(['id', 'age', 'first_name', 'last_name'])
const headers = ref([
  { name: 'ID' },
  { name: 'Date Time' },
  { name: 'Name' },
  { name: 'Datasets' },
  { name: 'Approaches' },
  { name: 'Metrics' },
  { name: '' },
])

const ex1CurrentPage = ref(1)
const ex1PerPage = ref(10)
const ex1Rows = ref(100)

const testMessage = ref('')
const results = ref([])

onMounted(() => {
  getResults()
})

watch(
  () => store.currentResult,
  (result) => {
    getResults()
  }
)

async function getResults() {
  const response = await fetch('/api/all-results')
  const data = await response.json()
  console.log(data)
  let allResults = data.all_results
  results.value = formatResults(allResults)
  //console.log(results.value)
}

const url = '/api/all-results/result-by-id'

// Request full result from result ID (timestamp)
async function loadResult(resultId) {
  console.log('Result ID:' + resultId)

  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: resultId }),
  }
  fetch(url, requestOptions).then(() => {
    getResult()
  })
}

// Get result back from result ID request
async function getResult() {
  const response = await fetch(url)
  const data = await response.json()
  store.currentResult = formatResult(data.result)
  console.log(store.currentResult)
}
</script>

<template>
  <div>
    <Table
      @loadResult="loadResult"
      :results="results"
      :headers="headers"
      :buttonText="'Remove'"
      :removable="true"
      :overview="true"
      :serverFile="'/all-results/delete'"
      :serverFile2="'/all-results/edit'"
    />
    <p>{{ testMessage }}</p>
  </div>
</template>
