<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import Table from './Table.vue'
import { onMounted, ref } from 'vue'
import { store, pollForResult, getQueue } from '../store.js'
import { API_URL } from '../api'
import SettingsModal from './Table/Modals/SettingsModal.vue'
// import VueDragResize from 'vue-drag-resize/src/component/vue-drag-resize.vue';
import RatingsTable from './Table/RatingsTable.vue';

const props = defineProps({ headers: Array, result: Object });

const runNumbers = [...Array(props.result.metadata.runs).keys()]
const RESULT_URL = API_URL + '/result/'


// Metrics and ratings table selection
const userTables = combineResults(props.result.result)
const visibleDatasets = ref([])
const visibleMetrics = ref([])
const availableMetrics = ref([])
const uniqueDatasets = findUniqueDatasets()
const visibleMatrices = ref([])

const validationAmount = ref(1)
const showComparison = ref(false)

onMounted(() => {
  console.log('result', props.result);
  fillVisibleDatasets()
  fillShownMetrics()
});


/**
 * Export a results objec to tsv and store in the user's download folder
 * @param {int}   currentTable  - Index of which result file to load (from overview.json)
 * @param {int}   runID         - Index of the run this result belongs to
 */
function exportTable(currentTable, runID) {
  // Convert the result object into tsv format
  const result = props.result.result[currentTable].results[runID]
  const headers = props.result.result[currentTable].headers.map((header) => header.name)
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
    body: JSON.stringify({ 
                           filepath: file, 
                           amount: validationAmount.value, 
                           ID: props.result.id 
                         }),
  }
  await fetch(
    RESULT_URL + 'validate',
    requestOptions
  ).then(() => {
    console.log('Validation added to the queue')
    getQueue()
    store.currentTab = 1
    pollForResult()
  })
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
          <SettingsModal :resultId="result.id" />
          <p class="lead"> Results for </p>
          <h1 class="display-3"> {{ result.metadata.name }} </h1>
          <h3 class="text-muted"> {{ result.metadata.datetime }} </h3>
        </b-col>
        <b-col>
          <div class="float-end">
            <div class="input-group pt-1">
              <b-form-input 
                style="width: 80px;"
                class="float-start pt-1"
                type="number" 
                v-model="validationAmount" 
                v-b-tooltip.hover 
                title="Number of validation runs">
              </b-form-input>
              <b-button 
                @click="validate()" 
                class="float-start"
                variant="outline-primary fw-bold"
                v-b-tooltip.hover
                title="Validate this experiment">
                Validate run
              </b-button>
            </div>
          </div>
        </b-col>
      </b-row>
      <p class="lead">
        Tags:
        <template v-if="!result.metadata.tags">None</template>
        <template v-for="tag in result.metadata.tags" :key="tag">
          <b-button disabled> {{ tag }} </b-button>
        </template>
      </p>
      <!-- TODO briefly show settings overview -->
      <!--<h2>Settings:</h2>-->
      <!--<p>{{result.settings}}</p>-->
      <h2>Filters:</h2>
      <b-list-group horizontal>
        <b-list-group-item v-for="datasetResult in result.result" :key="datasetResult">
          <!-- Filter for each dataset-->
          {{ datasetResult.dataset.name }}
          <b-list-group>
            <b-list-group-item v-for="filter in datasetResult.dataset.filters" :key="filter">
              {{ filter.name }}: {{ Object.values(filter.params)[0] }}
            </b-list-group-item>
            <ul>
              <li v-for="evale in datasetResult.evals" :key="evale">
                <!-- Filter for each metric-->
                {{ evale.evaluation.filtered }}
              </li>
            </ul>
          </b-list-group>
        </b-list-group-item>
      </b-list-group>
      <p>
        Datasets showing items per user:
      </p>
      <div class="form-check" v-for="dataset in uniqueDatasets" :key="dataset">
        <input v-model="visibleDatasets" class="form-check-input" type="checkbox" :value="dataset" :id="dataset" />
        <label class="form-check-label" :id="dataset">
          {{ dataset }}
        </label>
      </div>

    </div>
    <b-container>
      <h4>Metrics</h4>
      <template v-if="availableMetrics.length > 0">
        <p>
        Metrics shown:
        </p>
        <div class="form-check" v-for="metric in availableMetrics" :key="metric">
          <input v-model="visibleMetrics" class="form-check-input" type="checkbox" :value="metric" :id="metric" />
          <label class="form-check-label" :id="metric">
            {{ metric }}
          </label>
        </div>

        <b-row>
        <template v-for="runID in runNumbers">
          <template v-for="(datasetResult, index) in result.result" :key="runID+datasetResult">
            <b-col :cols="result.result.length > 1 ? '6' : '12'" >
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
        <h4 v-if="result.settings.experimentMethod === 'recommendation'">
          Recommended items per user
        </h4>
        <h4 v-else>Predicted rating per user</h4>
      </div>
      <!--<div class="form-check">
      <input v-model="snippet" class="form-check-input" type="checkbox" :id="snippet" />
      <label class="form-check-label" :id="snippet">Show snippets</label>
      </div>-->
      <p>
        Select items to be shown:
      <div class="form-check" v-for="entry in userTables" :key="entry">
        <input v-model="visibleMatrices" class="form-check-input" type="checkbox" :value="entry" :id="entry" />
        <label class="form-check-label" :id="entry">
          {{ entry }}
        </label>
      </div>
      </p>

      <!--<VueDragResize :isActive="true" :w="200" :h="200" >
      <b-card><h3>HEYA</h3></b-card>
        </VueDragResize>-->

      <div class="row">
        <!--Show recommendations for all datasets for now TODO-->
        <template v-for="run in runNumbers">
          <template v-for="(entry, index) in userTables">
            <template v-if="visibleDatasets.includes(getDatasetName(entry)) &&
            visibleMatrices.includes(entry)">
  <div :class="visibleMatrices.length > 1 ? 'col-6' : 'col'" :key="run+entry">
              <RatingsTable :id="result.id" :entry="entry" :pairData="result.result[index].dataset" :pairIndex="index" :runIndex="run" />
  </div>
            </template>
          </template>
        </template>
      </div>
    </div>
  </div>

  <!-- Modal to compare ratings-->
  <b-modal 
    v-model="showComparison"
    title="test">
  </b-modal>
</template>
