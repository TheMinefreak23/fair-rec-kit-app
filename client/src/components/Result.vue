<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import Table from './Table.vue'
import { onActivated, onMounted, onUpdated, ref, watch } from 'vue'
import { emptyFormGroup } from '../helpers/optionsFormatter'
import { makeHeader } from '../helpers/resultFormatter'
import { API_URL } from '../api'
import { store, addResult, removeResult } from '../store'

const props = defineProps({ headers: Array, result: Object })

//Default headers for recommendation experiments.
const selectedHeaders = ref([
  [{ name: 'Rank' }, { name: 'User' }, { name: 'Item' }, { name: 'Score' }],
])


const data = ref({ results: [[]] })
const startIndex = ref(0)
const sortIndex = ref(0)
const ascending = ref(true)
const entryAmount = ref(20)
const optionalHeaders = ref([[]])
const availableFilters = ref([])
const filters = ref(emptyFormGroup(false))
const userHeaderOptions = ref([[]])
const itemHeaderOptions = ref([[]])
const userTables = combineResults()
const visibleDatasets = ref([])
const visibleMetrics = ref([])
const availableMetrics =ref([])
const uniqueDatasets = findUniqueDatasets()

onMounted(() => {
  console.log('result', props.result)
  console.log('result id', props.result.id)
  loadEvaluations()
  fillVisibleDatasets()
  fillShownMetrics()
  //Load in all the user recommendation/prediction tables
  for (let index in userTables) {
    setRecs(parseInt(index))
  }
  console.log('availableFilters', availableFilters.value)
  console.log(store.allResults)
  //loadEvaluations()
})

/** 
 * GET request: Get available header options for selection from server
 * @param {Int}  index  - index of the current result table
 */
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
      runid: 0,
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
async function loadEvaluations() {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-type': 'application/json' },
    body: JSON.stringify({ id: props.result.id }),
  }
  const response = await fetch(
    API_URL + '/all-results/result-by-id',
    requestOptions
  ).then(() => {
    console.log('succesful POST request to API to retrieve evaluation data')
    getEvaluations()
  })
}

//GET request: Ask server for currently loaded evaluations
async function getEvaluations() {
  const response = await fetch(API_URL + '/all-results/result-by-id')
  console.log('succesfully retrieved evaluation data.')
  const resultsData = await response.json()
  console.log('results data', resultsData)
}

/**
 * POST request: Ask server for next part of user recommendation table.
 * @param {Int}   currentTable  - Index of which result file to load (from overview.json)
 */
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
 * @returns {Array}   - An array of all the user recommendation tables for this run
 */
function combineResults() {
  let tables = []
  for (let dataset in props.result.result) {
    for (let approach in props.result.result[dataset].results) {
      tables.push(props.result.result[dataset].caption + '_' + props.result.result[dataset].results[approach].approach)
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
function fillVisibleDatasets(){
  console.log(findUniqueDatasets[0])
  visibleDatasets.value = findUniqueDatasets()
   
}

/**
 * Create an array that has all unique datasets in the result
 */
function findUniqueDatasets(){
  let datasetnames = []

  for(let i=0; i<userTables.length;i++){
      datasetnames[i] = getDatasetName(userTables[i])
  }

  return Array.from(new Set(datasetnames))

}

/**
 * Fill array of metrics that are shown so that all are shown upon loading the page
 */
function fillShownMetrics(){
  let result = props.result.result
  let i=0
  for(let dataset in result) {
     for(let metric in result[dataset].headers)
      
       if (!(result[dataset].headers[metric].name.includes("Approach"))) {
             visibleMetrics.value[i] = result[dataset].headers[metric].name
              availableMetrics.value[i] = result[dataset].headers[metric].name
              i++
     }        
  } 

}

/**
 * Return an array of filtered headers, so that only those selected are shown
 * @param {Array} headers  - array of headers that have to be checked
 */
function hideHeaders(headers){
  let result = []
     for(let i=0; i<headers.length; i++){
        if (visibleMetrics.value.includes(headers[i].name) || headers[i].name == "Approach")
        {
          result.push(headers[i])
        }
      }

  return result
}

/**
 * Return an array of filtered results, so that only results for the selected
 * headers are shown
 * @param {Array} results  - array of results that have to be filtered
 */
function hideResults(results){
  let result = []
    for(let i=0; i<results.length; i++) {
      const object_as_array = Object.entries(results[i]).filter(([property, value]) => {
        return !property.startsWith('P@') || contains(property, visibleMetrics.value)
      })
      result.push(Object.fromEntries(object_as_array))
    }

  return result
}

/**
 * Check if input string starts with any of the array elements, 
 * return a boolean
 * @param {String} string - string that might start with element of array
 * @param {Array} array - array of strings that might be part of the string
 */
function contains(string, array){
  return array.some(element => string.startsWith(element))
}


</script>

<template>
  <div>
    <div class="container">
      <p class="lead" > Results for </p>
      <h1 class="display-3"> {{ result.metadata.name }}    </h1>
      <h3 class="text-muted"> {{ result.metadata.datetime}} </h3>
      <!-- TODO more human readable date time-->
      <p class="lead">
        Tags:
        <template v-if="!result.metadata.tags">None</template>
        <template v-for="tag in result.metadata.tags">
          <b-button disabled> {{ tag }} </b-button
          >
        </template>
      </p>

      <p>&nbsp;</p> 
      <p>
        Datasets showing items per user:
        <div class="form-check" v-for="dataset in uniqueDatasets">
          <input
            v-model = "visibleDatasets"
            class = "form-check-input"
            type="checkbox"
            :value="dataset"
            :id="dataset"
          />
          <label class="form-check-label" :id="dataset">
            {{dataset}}
          </label>
        </div>
      </p>

      <p>
        Metrics shown:
        <div class="form-check" v-for="metric in availableMetrics">
          <input
            v-model = "visibleMetrics"
            class = "form-check-input"
            type = "checkbox"
            :value="metric"
            :id="metric"
            />
          <label class="form-check-label" :id="metric">
            {{metric}}
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

            <Table
              :caption="datasetResult.caption"
              :results="hideResults(datasetResult.results)"
              :headers="hideHeaders(datasetResult.headers)"
              :removable="false"
            />
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
