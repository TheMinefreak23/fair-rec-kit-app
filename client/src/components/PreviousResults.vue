<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
import Table from './Table.vue'
import { onMounted, ref, watch } from 'vue'
import { formatResults, formatResult } from '../helpers/resultFormatter.js'

import { addResult, store } from '../store.js'
import { API_URL } from '../api'

const oldResultsFormat = ref(true) // TODO DEV
const emit = defineEmits(['goToResult'])

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
  { name: 'Tags' },
  { name: 'Datasets' },
  { name: 'Approaches' },
  { name: 'Metrics' },
  { name: '' },
])

const ex1CurrentPage = ref(1)
const ex1PerPage = ref(10)
const ex1Rows = ref(100)

onMounted(() => {
  getResults()
})

watch(
  () => store.currentResults.length,
  () => {
    //console.log('previousResults watch currentResults')
    getResults()
  }
)

async function getResults() {
  const response = await fetch(API_URL + '/all-results')
  const data = await response.json()
  store.allResults = formatResults(data.all_results)
  //console.log('all results', store.allResults)
}

const resultsRoute =
  '/all-results/' + (oldResultsFormat ? 'old' : '') + '-result-by-id'
const url = API_URL + resultsRoute

// Request full result from result ID (timestamp)
async function loadResult(resultId) {
  console.log('Loading result with ID:' + resultId)

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
  addResult(formatResult(data.result))
  emit('goToResult')
}
</script>

<template>
  <b-card>
    <div class="text-center py-2 mx-5">
      <h3>Previous results</h3>
      <b-row>
        <b-col md="auto">
          <b-form-checkbox v-model="oldResultsFormat"
            >use old results route
          </b-form-checkbox>
        </b-col>
      </b-row>
      <Table
        @loadResult="loadResult"
        @loadResults="getResults"
        :results="store.allResults"
        :headers="headers"
        buttonText="Remove"
        :removable="true"
        :overview="true"
        serverFile="/all-results/delete"
        serverFile2="/all-results/edit"
        :serverFile3="resultsRoute"
        :defaultSort="1"
      />
    </div>
  </b-card>
</template>
