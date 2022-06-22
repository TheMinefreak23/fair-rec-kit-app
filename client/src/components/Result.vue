<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import Table from './Table.vue'
import { onMounted, ref } from 'vue'
import { emptyFormGroup } from '../helpers/optionsFormatter'
import { makeHeader } from '../helpers/resultFormatter'
import { API_URL } from '../api'
import SettingsModal from './Table/Modals/SettingsModal.vue'

const props = defineProps({ headers: Array, result: Object });

// Default headers for recommendation experiments.
const selectedHeaders = ref([[
  [{ name: 'Rank' }, { name: 'User' }, { name: 'Item' }, { name: 'Score' }],
]]);


const data = ref({ results: [] })
const runNumbers = [...Array(props.result.metadata.runs).keys()]
const startIndex = ref(0)
const sortIndex = ref(0)
const ascending = ref(true)
const entryAmount = ref(10)
const optionalHeaders = ref([[]])
const availableFilters = ref([])
const filters = ref(emptyFormGroup(false))
const optionalHeaderOptions = ref([])
const userTables = combineResults(props.result.result)
const visibleDatasets = ref([])
const visibleMetrics = ref([])
const availableMetrics = ref([])
const uniqueDatasets = findUniqueDatasets()
const visibleMatrices = ref([])
const validationAmount = ref(1)
const snippet = ref(false)

onMounted(() => {
  console.log('result', props.result);
  fillVisibleDatasets()
  fillShownMetrics()
  // Load in all the user recommendation/prediction tables
  // Also initialize the components for table storage
  for (const run in runNumbers) {
    data.value.results[run] = []
    selectedHeaders.value[run] = []
    for (const index in userTables) {
      selectedHeaders.value[run][index] = []
      data.value.results[run][index] = []
      optionalHeaders.value[index] = ['track_spotify-uri']
      setRecs(parseInt(index), parseInt(run))
    }
  }

  console.log('availableFilters', availableFilters.value);
});

/** 
 * GET request: Get available header options for selection from server
 * @param {Int}  index  - index of the current result table
 */
async function getHeaderOptions(index) {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: props.result.result[index].dataset.dataset,
    }),
  }
  const response = await fetch(API_URL + '/result/headers', requestOptions)
  const data = await response.json()
  const headerOptions = data
  optionalHeaderOptions.value[index] = headerOptions
}

// POST request: Send result ID to the server to set recommendations for the current experiment.
async function setRecs(currentTable, runID) {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: props.result.id,
      runid: runID,
      pairid: currentTable,
    }),
  };
  console.log('sending to server:', requestOptions.body);
  const response = await fetch(
    API_URL + '/result/set-recs',
    requestOptions
  )
  if (response.status === 200) {
    const data = await response.json()
    availableFilters.value = data.availableFilters
    getUserRecs(currentTable, runID)
    getHeaderOptions(currentTable)
  }
}

/**
 * POST request: Ask server for next part of user recommendation table.
 * @param {Int}   currentTable  - Index of which result file to load (from overview.json)
 * @param {int}   runID         - Index of the run this result belongs to
 */
async function getUserRecs(currentTable, runID) {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: props.result.id,
      pairid: currentTable,
      runid: runID,
      start: startIndex.value,
      sortindex: sortIndex.value,
      ascending: ascending.value,
      amount: entryAmount.value,
      filters: filters.value,
      optionalHeaders: optionalHeaders.value[currentTable],
      dataset: props.result.result[currentTable].dataset.dataset,
      matrix: props.result.result[currentTable].dataset.matrix
    }),
  };
  const response = await fetch(API_URL + '/result/', requestOptions);
  data.value.results[runID][currentTable] = await response.json();
  selectedHeaders.value[runID][currentTable] = Object.keys(
    data.value.results[0][currentTable][0]
  )
}

/**
 * Export a results objec to tsv and store in the user's download folder
 * @param {int}   currentTable  - Index of which result file to load (from overview.json)
 * @param {int}   runID         - Index of the run this result belongs to
 */
function exportTable(currentTable, runID) {
  // Convert the result object into tsv format
  let result = props.result.result[currentTable].results[runID]
  let headers = props.result.result[currentTable].headers.map((header) => header.name)
  let tsv = headers.join('  ') + '\n';
    result.forEach((row) => {
            tsv += Object.values(row).join('  ');
            tsv += "\n";
    });

  // Create an element to download the file
  const anchor = document.createElement('a')
  anchor.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(tsv)
  anchor.target = '_blank'
  anchor.download = props.result.metadata.name + '.csv'
  anchor.click();
}


async function validate() {
  const file = props.result.id + '_' + props.result.metadata.name
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-type': 'application/json' },
    body: JSON.stringify({ filepath: file, amount: validationAmount.value }),
  }
  await fetch(
    API_URL + '/result/validate',
    requestOptions
  ).then(() => {
    console.log('Validation added to the queue')
  })
}

/**
 * Loads more data in the table after user asks for more data.
 * @param {Bool}   increase  - Determines whether the next or previous data is required.
 * @param {Int}    amount    - Number of items that the user has requested.
 * @param {Int}    pairid    - Index of which result file to load (from overview.json)
 * @param {int}    runID     - Index of the run this result belongs to
 */
function loadMore(increase, amount, pairid, runID) {
  amount = parseInt(amount);

  // Determine the index for where the next page starts, based on how many entries were shown before.
  if (increase != null)
  {
    if (!increase) startIndex.value -= amount;
    if (startIndex.value < 0) startIndex.value = 0;
    else if (increase) startIndex.value += entryAmount.value;
  }
  
  // Update amount to new number of entries that are shown.
  entryAmount.value = amount;
  getUserRecs(pairid, runID);
}

/**
 * Handles sorting for tables that have pagination.
 * @param {int}   indexVar   - Index of the column on which is sorted.
 * @param {Int}    pairid    - Index of which result file to load (from overview.json)
 * @param {int}    runID     - Index of the run this result belongs to
 */
function paginationSort(indexVar, pairid, runID) {
  // When sorting on the same column twice in a row, switch to descending.
  if (sortIndex.value === indexVar) {
    ascending.value = !ascending.value;
  }

  // When sorting, start at startIndex 0 again to see either highest or lowest, passing on which column is sorted.
  sortIndex.value = indexVar;
  startIndex.value = 0;
  getUserRecs(pairid, runID);
}

/**
 * Update headers shown in user recommendations
 * @param {Array}   headers  - A list of the headers that have been selected to be shown
 * @param {Int}    pairid    - Index of which result file to load (from overview.json)
 * @param {int}    runID     - Index of the run this result belongs to
 */
function updateHeaders(headers, pairid, runID) {
  optionalHeaders.value[pairid] = headers;
  getUserRecs(pairid, runID);
}

/**
 * Update headers shown in user recommendations
 * @param {Array}  changedFilters - A list of filters that are selected
 * @param {Int}    pairid         - Index of which result file to load (from overview.json)
 * @param {int}    runID          - Index of the run this result belongs to
 */
function changeFilters(changedFilters, pairid, runID) {
  filters.value = changedFilters;
  getUserRecs(pairid, runID);
}

/**
 * Combines every approach with every dataset that it is being applied onto
 * @param {Array}     - A list of the results (the same as props.results.result)
 * @returns {Array}   - An array of all the user recommendation tables for this run
 */
function combineResults(results) {
  const tables = []
  for (const dataset in results) {
    for (const approach in results[dataset].results[0]) {
      tables.push(results[dataset].dataset.dataset + '_' + results[dataset].results[0][approach].approach)
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
  return string.split('_')[0]
}

/**
 * Fill array of datasets that are shown so that all are shown upon loading the page
 */
function fillVisibleDatasets() {
  visibleDatasets.value = findUniqueDatasets()

}

/**
 * Create an array that has all unique datasets in the result
 * @returns {string}         - a list of all datasets in the experiments without duplicates
 */
function findUniqueDatasets() {
  const datasetnames = userTables.map(getDatasetName)
  return Array.from(new Set(datasetnames))
}

/**
 * Fill array of metrics that are shown so that all are shown upon loading the page
 */
function fillShownMetrics() {
  const result = props.result.result
  let i = 0
  for (const dataset in result) {
    for (const metric in result[dataset].headers)

      if (!(result[dataset].headers[metric].name.includes("Approach")) && !(visibleMetrics.value.includes(result[dataset].headers[metric].name))) {
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
function hideHeaders(headers) {
  const result = []
  for (let i = 0; i < headers.length; i++) {
    if (visibleMetrics.value.includes(headers[i].name) || headers[i].name === "Approach") {
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
function hideResults(results) {
  const result = []
  for (let i = 0; i < results.length; i++) {
    const objectAsArray = Object.entries(results[i]).filter(([property, value]) => {
      return property.startsWith('approach') || contains(property, visibleMetrics.value)
    })
    result.push(Object.fromEntries(objectAsArray))
  }

  return result
}

/**
 * Check if input string starts with any of the array elements, 
 * return a boolean
 * @param {String} string - string that might start with element of array
 * @param {Array} array - array of strings that might be part of the string
 */
function contains(string, array) {
  return array.some(element => string.startsWith(element))
}

</script>

<template>
  <div>
    <div class="container">
      <b-row>
        <b-col>
          <p class="lead"> Results for </p>
          <h1 class="display-3"> {{ result.metadata.name }} </h1>
          <h3 class="text-muted"> {{ result.metadata.datetime }} </h3>
        </b-col>
        <b-col>
          <div class="float-end">
            <SettingsModal :resultId="result.id" />
            <b-form-input type="number" v-model="validationAmount" v-b-tooltip.hover title="Number of validation runs">
            </b-form-input>
            <b-button @click="validate()" variant="outline-primary fw-bold" v-b-tooltip.hover
              title="Validate this experiment">Validate run
            </b-button>
          </div>
        </b-col>
      </b-row>
      <p class="lead">
        Tags:
        <template v-if="!result.metadata.tags">None</template>
        <template v-for="tag in result.metadata.tags">
          <b-button disabled> {{ tag }} </b-button>
        </template>
      </p>
      <h2>Filters:</h2>
      <b-list-group horizontal>
        <b-list-group-item v-for="datasetResult in result.result">
          <!-- Filter for each dataset-->
          {{ datasetResult.dataset.name }}
          <b-list-group>
            <b-list-group-item v-for="filter in datasetResult.dataset.filters">
              {{ filter.name }}: {{ Object.values(filter.params)[0] }}
            </b-list-group-item>
            <ul>
              <li v-for="evale in datasetResult.evals">
                <!-- Filter for each metric-->
                {{ evale.evaluation.filtered }}
              </li>
            </ul>
          </b-list-group>
        </b-list-group-item>
      </b-list-group>
      <p>
        Datasets showing items per user:
      <div class="form-check" v-for="dataset in uniqueDatasets">
        <input v-model="visibleDatasets" class="form-check-input" type="checkbox" :value="dataset" :id="dataset" />
        <label class="form-check-label" :id="dataset">
          {{ dataset }}
        </label>
      </div>
      </p>

    </div>
    <b-container>
      <h4>Metrics</h4>
      <template v-if="availableMetrics.length > 0">
        <p>
        Metrics shown:
        <div class="form-check" v-for="metric in availableMetrics">
          <input v-model="visibleMetrics" class="form-check-input" type="checkbox" :value="metric" :id="metric" />
          <label class="form-check-label" :id="metric">
            {{ metric }}
          </label>
        </div>
        </p>

        <b-row>
        <template v-for="runID in runNumbers">
          <template v-for="(datasetResult, index) in result.result" :key="datasetResult">
            <b-col :cols="result.result.length > 1 ? '6' : '12'">
              <template v-if="visibleDatasets.includes(datasetResult.dataset.dataset)" :key="visibleDatasets">
                <h4>Run {{ runID }}</h4>
                <Table :caption="datasetResult.dataset.dataset" :results="hideResults(datasetResult.results[runID])"
                  :headers="hideHeaders(datasetResult.headers)" :removable="false" />
                <b-button @click="exportTable(index, runID)">Export table</b-button>
              </template>
            </b-col>
          </template>
        </template>
        </b-row>
      </template>
      <template v-else>(None)</template>
    </b-container>

    <div class="container">
      <div class="row">
        <!--Type of experiment decides which label to give the section-->
        <h4 v-if="selectedHeaders[0][0][0] == 'rank'">
          Recommended items per user
        </h4>
        <h4 v-else>Predicted rating per user</h4>
      </div>
      <div class="form-check">
      <input v-model="snippet" class="form-check-input" type="checkbox" :id="snippet" />
      <label class="form-check-label" :id="snippet">Show snippets</label>
      </div>
      <p>
        Select items to be shown:
      <div class="form-check" v-for="entry in userTables">
        <input v-model="visibleMatrices" class="form-check-input" type="checkbox" :value="entry" :id="entry" />
        <label class="form-check-label" :id="entry">
          {{ entry }}
        </label>
      </div>
      </p>


      <div class="row">
        <!--Show recommendations for all datasets for now TODO-->
        <template v-for="run in runNumbers">
          <template v-for="(entry, index) in userTables" :key="data">
            <template v-if="visibleDatasets.includes(getDatasetName(entry)) &&
            visibleMatrices.includes(entry)" :key="visibleUserTables">
              <h4>Run {{ run }}</h4>
              <div :class="visibleMatrices.length > 1 ? 'col-6' : 'col'">
                <Table v-if="selectedHeaders[run][index]" :key="props.result.id" :caption="entry"
                  :results="data.results[run][index]" :headers="selectedHeaders[run][index].map(makeHeader)"
                  :filters="filters" :filterOptions="availableFilters" :headerOptions="optionalHeaderOptions[index]" defaultSort="0"
                  :startIndex = "startIndex" pagination expandable :recs="snippet" @paginationSort="(i) => paginationSort(i, index, run)" @loadMore="
                    (increase, amount) => loadMore(increase, amount, index, run)
                  " @changeFilters="
  (changedFilters) => changeFilters(changedFilters, index, run)
" @updateHeaders="(headers) => updateHeaders(headers, index, run)" />
              </div>
            </template>
          </template>
        </template>
      </div>
    </div>
  </div>
</template>
