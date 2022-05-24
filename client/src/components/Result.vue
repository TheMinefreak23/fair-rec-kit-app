<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import Table from './Table.vue'
import { onActivated, onMounted, onUpdated, ref, watch } from 'vue'
import { emptyFormGroup } from '../helpers/optionsFormatter'
import { makeHeader } from '../helpers/resultFormatter'

import mockdata from '../../../server/mock/1647818279_HelloWorld/results-table.json'
import { API_URL } from '../api'

const props = defineProps({ headers: Array, result: Object })

//Default headers for recommendation experiments.
const selectedHeaders = ref([
  [{ name: 'Rank' }, { name: 'User' }, { name: 'Item' }, { name: 'Score' }],
])

const experiment_tags = ref(['tag1 ', 'tag2 ', 'tag3 ', 'tag4 '])

const data = ref({ results: [[]] })
const runID = ref(0)
const startIndex = ref(0)
const sortIndex = ref(0)
const ascending = ref(true)
const entryAmount = ref(20)
const optionalHeaders = ref([[]])
const availableFilters = ref([])
const filters = ref(emptyFormGroup(false))
const userHeaderOptions = ref([[]])
const itemHeaderOptions = ref([[]])
const userTables = combineResults(props.result.result)
const visibleDatasets = ref([])

onMounted(() => {
  console.log('result', props.result)
  console.log('result id', props.result.id)
  //loadEvaluations()
  fillVisibleDatasets()
  //Load in all the user recommendation/prediction tables
  for (let index in userTables) {
    setRecs(parseInt(index))
  }
  console.log('availableFilters', availableFilters.value)
  //loadEvaluations()
})

// GET request: Get available header options for selection from server
async function getHeaderOptions(index) {
  const response = await fetch(API_URL + '/all-results/headers')
  const data = await response.json()
  let headerOptions = data[getDatasetName(userTables[index])]
  itemHeaderOptions.value[index] = headerOptions.itemHeaders
  userHeaderOptions.value[index] = headerOptions.userHeaders
}

//POST request: Send result ID to the server to set current shown recommendations.
async function setRecs(currentTable) {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: props.result.id,
      runid: runID.value,
      pairid: currentTable,
    }),
  }
  console.log('sending to server:', requestOptions.body)
  const response = await fetch(
    API_URL + '/all-results/set-recs',
    requestOptions
  )
  //console.log('resultfetch', response)
  if (response.status == '200') {
    const data = await response.json()
    availableFilters.value = data.availableFilters
    getUserRecs(currentTable)
    getHeaderOptions(currentTable)
  }
}

//POST request: Ask server to load the evaluations of the current result
//Currently not used, as evaluation tables are not finished
// async function loadEvaluations() {
//   const requestOptions = {
//     method: 'POST',
//     headers: { 'Content-type': 'application/json' },
//     body: JSON.stringify({ id: props.result.id }),
//   }
//   const response = await fetch(
//     API_URL + '/all-results/result-by-id',
//     requestOptions
//   ).then(() => {
//     console.log('succesful POST request to API to retrieve evaluation data')
//     const resultsData = await response.json()
//     console.log('results data', resultsData)
//     getEvaluations()
//   })
// }

// //GET request: Ask server for currently loaded evaluations
// async function getEvaluations() {
//   const response = await fetch(API_URL + '/all-results/result-by-id')
//   console.log('succesfully retrieved evaluation data.')
//   const resultsData = await response.json()
//   console.log('results data', resultsData)
// }

//POST request: Ask server for next part of user recommendation table.
async function getUserRecs(currentTable) {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: props.result.id,
      pairid: currentTable,
      start: startIndex.value,
      sortindex: sortIndex.value,
      ascending: ascending.value,
      amount: entryAmount.value,
      filters: filters.value,
      optionalHeaders: optionalHeaders.value[currentTable],
      dataset: getDatasetName(userTables[currentTable])
    }),
  }

  const response = await fetch(API_URL + '/all-results/result', requestOptions)
  data.value.results[currentTable] = await response.json()
  selectedHeaders.value[currentTable] = Object.keys(
    data.value.results[currentTable][0]
  )
}

async function exportTable() {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-type': 'application/json' },
    body: JSON.stringify({ results: props.result.result[0].results}),
  }
  const response = await fetch(
    API_URL + '/all-results/export',
    requestOptions
  ).then(() => {
    console.log('exported succesfully')
  })
}

/**
 * Loads more data in the table after user asks for more data.
 * @param {Bool}   increase  - Determines whether the next or previous data is required.
 * @param {Int}    amount    - Number of items that the user has requested.
 * @param {Int}    pairid    - Index of which result file to load (from overview.json)
 */
function loadMore(increase, amount, pairid) {
  amount = parseInt(amount)

  //Determine the index for where the next page starts, based on how many entries were shown before.
  if (!increase && startIndex.value > 0) startIndex.value -= entryAmount.value
  if (startIndex.value < 0) startIndex.value = 0
  else if (increase) startIndex.value += entryAmount.value
  else startIndex.value = 0
  //Update amount to new number of entries that are shown.
  entryAmount.value = amount
  getUserRecs(pairid)
}

/**
 * Handles sorting for tables that have pagination.
 * @param {int}   indexVar  - Index of the column on which is sorted.
 * @param {Int}    pairid    - Index of which result file to load (from overview.json)
 */
function paginationSort(indexVar, pairid) {
  //When sorting on the same column twice in a row, switch to descending.
  if (sortIndex.value === indexVar) {
    ascending.value = !ascending.value
  }

  //When sorting, start at startIndex 0 again to see either highest or lowest, passing on which column is sorted.
  sortIndex.value = indexVar
  startIndex.value = 0
  getUserRecs(pairid)
}

/**
 * Update headers shown in user recommendations
 * @param {Array}   headers  - A list of the headers that have been selected to be shown
 * @param {Int}    pairid    - Index of which result file to load (from overview.json)
 */
function updateHeaders(headers, pairid) {
  optionalHeaders.value[pairid] = headers
  getUserRecs(pairid)
}

/**
 * Update headers shown in user recommendations
 * @param {Array}   changedFilters  - A list of filters that are selected
 * @param {Int}    pairid    - Index of which result file to load (from overview.json)
 */
function changeFilters(changedFilters, pairid) {
  filters.value = changedFilters
  getUserRecs(pairid)
}

/**
 * Combines every approach with every dataset that it is being applied onto
 * @param {Array}     - A list of the results (the same as props.results.result)
 * @returns {Array}   - An array of all the user recommendation tables for this run
 */
function combineResults(results) {
  console.log(results)
  let tables = []
  for (let dataset in results) {
    for (let approach in results[dataset].results) {
      tables.push(results[dataset].caption + '_' + results[dataset].results[approach].approach + '_' + runID.value)
    }
  }
  return tables
}

/**
 * Returns the name of the dataset of the requested user recommendation table
 * @param {string}   string   - the dataset-approach couple to extract the dataset from
 * @returns {string}          - the name of the requested dataset
 */
function getDatasetName(string) {
return string.split(' ')[1].split('_')[0]
}

/**
 * Fill array of datasets that are shown so that all are shown upon loading the page
 */
function fillVisibleDatasets() {

  for(let i=0; i<userTables.length;i++){
      visibleDatasets.value[i] = getDatasetName(userTables[i])
  }
  

   
}
</script>

<template>
  <div>
    <div class="container">
      <h1 class="display-2">Results</h1>
      <p class="lead">
        These are the results for experiment {{ result.metadata.name }} done at
        {{ result.metadata.datetime }}.
      </p>

      <p>
        Datasets shown:
        <div class="form-check" v-for="dataset in userTables">
          <input
            v-model = "visibleDatasets"
            class = "form-check-input"
            type="checkbox"
            :value="getDatasetName(dataset)"
            :id="dataset"
          />
          <label class="form-check-label" :id="dataset">
            {{getDatasetName(dataset)}}
          </label>
        </div>
      </p>

      <div class="col">
        Tags:
        <template v-if="!result.metadata.tags">None</template>
        <template v-for="tag in result.metadata.tags">
          <b-button disabled> {{ tag }} </b-button
          >
        </template>
      </div>
    </div>

    <div class="container">
      <div class="row">
        <h4>Metrics</h4>

        <!--Show first two dataset results for now TODO-->
        <template
          v-for="datasetResult in result.result[1]
            ? [result.result[0], result.result[1]]
            : [result.result[0]]"
          :key="datasetResult"
        >
          <p> {{datasetResult.results[0].dataset}}</p>
          <div class="col-6">

          
          <template v-if="visibleDatasets.includes(getDatasetName(datasetResult.caption))" :key="visibleDatasets">
            <Table
              :caption="datasetResult.dataset"
              :results="datasetResult.results"
              :headers="datasetResult.headers"
              :removable="false"
            />
            <b-button @click="exportTable()">Export table</b-button>
          </template>
          </div>
        </template>
      </div>
    </div>

    <div class="container">
      <div class="row">
        <!--Type of experiment decides which label to give the section-->
        <h4 v-if="selectedHeaders[0][0] == 'rank'">
          Recommended items per user
        </h4>
        <h4 v-else>Predicted rating per user</h4>
      </div>
      <div class="row">
        <!--Show recommendations for all datasets for now TODO-->
        <!--Currently only shows the results of the first dataset-->
        <template v-for="(entry, index) in userTables" :key="data">
          <template v-if="visibleDatasets.includes(getDatasetName(entry))" :key="visibleDatasets">
          <!--<template v-for="(entry, index) in props.result.result" :key="data">-->
            <div class="col-6">
              <Table
                v-if="selectedHeaders[index]"
                :key="props.result.id"
                :caption="entry"
                :results="data.results[index]"
                :headers="selectedHeaders[index].map(makeHeader)"
                :filters="filters"
                :filterOptions="availableFilters"
                :userOptions="userHeaderOptions[index]"
                :itemOptions="itemHeaderOptions[index]"
                pagination
                expandable
                @paginationSort="(i) => paginationSort(i, index)"
                @loadMore="
                  (increase, amount) => loadMore(increase, amount, index)
                "
                @changeFilters="
                  (changedFilters) => changeFilters(changedFilters, index)
                "
                @updateHeaders="(headers) => updateHeaders(headers, index)"
              />
            </div>
          </template>
        </template>
      </div>
    </div>
  </div>
</template>
