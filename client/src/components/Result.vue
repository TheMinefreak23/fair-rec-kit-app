<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import Table from './Table.vue'
import { onMounted, ref } from 'vue'
import { store, pollForResult, getQueue } from '../store.js'
import { API_URL } from '../api'
import SettingsModal from './Table/Modals/SettingsModal.vue'
import RatingsTable from './Table/RatingsTable.vue'
import { capitalise, underscoreToSpace } from '../helpers/resultFormatter'
import draggable from 'vuedraggable'

const props = defineProps({ headers: Array, result: Object })

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
const comparisonTables = ref([]) // Tables to show in compariosn

onMounted(() => {
  console.log('result', props.result)
  fillVisibleDatasets()
  fillShownMetrics()
})

/**
 * Export a results objec to tsv and store in the user's download folder
 * @param {int}   currentTable  - Index of which result file to load (from overview.json)
 * @param {int}   runID         - Index of the run this result belongs to
 */
function exportTable(currentTable, runID) {
  // Convert the result object into tsv format
  const result = props.result.result[currentTable].results[runID]
  const headers = props.result.result[currentTable].headers.map(
    (header) => header.name
  )
  let tsv = headers.join('  ') + '\n'
  result.forEach((row) => {
    tsv += Object.values(row).join('  ')
    tsv += '\n'
  })

  // Create an element to download the file
  const anchor = document.createElement('a')
  anchor.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(tsv)
  anchor.target = '_blank'
  anchor.download = props.result.metadata.name + '.csv'
  anchor.click()
}

async function validate() {
  const file = props.result.id + '_' + props.result.metadata.name
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-type': 'application/json' },
    body: JSON.stringify({
      filepath: file,
      amount: validationAmount.value,
      ID: props.result.id,
    }),
  }
  await fetch(RESULT_URL + 'validate', requestOptions).then(() => {
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
      tables.push(
        results[dataset].dataset.dataset +
          '_' +
          results[dataset].results[0][approach].approach
      )
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
      if (
        !result[dataset].headers[metric].name.includes('Approach') &&
        !visibleMetrics.value.includes(result[dataset].headers[metric].name)
      ) {
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
    if (
      visibleMetrics.value.includes(headers[i].name) ||
      headers[i].name === 'Approach'
    ) {
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
    const objectAsArray = Object.entries(results[i]).filter(
      ([property, value]) => {
        return (
          property.startsWith('approach') ||
          contains(property, visibleMetrics.value)
        )
      }
    )
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
  return array.some((element) => string.startsWith(element))
}
</script>

<template>
  <div>
    <b-card>
      <div class="container">
        <b-row>
          <b-col>
            <p class="lead">Results for</p>
            <h1 class="display-3">{{ result.metadata.name }}</h1>
            <h3 class="text-muted">{{ result.metadata.datetime }}</h3>
            <!--Show experiments data (original experiment and validations)-->
            <template v-if="result.experiments">
              <b v-if="result.experiments.length > 1">Experiments:</b>
              <ul>
                <li v-for="(experiment, index) in result.experiments">
                  {{
                    index !== 0
                      ? experiment.runs + ' Validation experiments'
                      : 'Experiment'
                  }}
                  started at {{ experiment.started }} and ended at
                  {{ experiment.ended }}.
                  {{ index !== 0 && experiment.runs > 1 ? 'They' : 'It' }} took
                  {{
                    new Date(1000 * experiment.elapsed_time)
                      .toISOString()
                      .substr(11, 8)
                  }}
                  to complete.
                </li>
              </ul>
            </template>
          </b-col>
          <b-col cols="3">
            <div class="float-end">
              <SettingsModal :resultId="result.id" />
              <div class="input-group pt-1">
                <b-form-input
                  style="width: 80px"
                  class="float-start pt-1"
                  type="number"
                  v-model="validationAmount"
                  v-b-tooltip.hover
                  title="Number of validation runs"
                >
                </b-form-input>
                <b-button
                  @click="validate()"
                  class="float-start"
                  variant="outline-primary fw-bold"
                  v-b-tooltip.hover
                  title="Validate this experiment"
                >
                  Validate run
                </b-button>
              </div>
            </div>
          </b-col>
        </b-row>
        <b-row>
          <p class="lead">
            Tags:
            <template v-if="!result.metadata.tags">None</template>
            <template v-for="tag in result.metadata.tags" :key="tag">
              <b-button disabled> {{ tag }} </b-button>
            </template>
          </p>
        </b-row>
        <!-- TODO briefly show settings overview -->
        <!--<h2>Settings:</h2>-->
        <!--<p>{{result.settings}}</p>-->
        <p class="lead">(Pre-)Filters used:</p>
        <b-list-group horizontal>
          <b-list-group-item
            v-for="datasetResult in result.result"
            :key="datasetResult"
          >
            <!-- Filter for each dataset-->
            {{ underscoreToSpace(datasetResult.dataset.name) }}
            <b-list-group>
              <b-list-group-item
                v-for="(filterGroup, index) in datasetResult.dataset.subset"
                :key="filterGroup"
              >
                Filter pass {{ index }}
                <b-list-group v-for="filters in filterGroup" :key="filters">
                  <b-list-group-item v-for="filter in filters">
                    {{ filter.name }} :
                    {{ Object.values(filter.params).flat() }}
                  </b-list-group-item>
                </b-list-group>
              </b-list-group-item>
              <ul>
                <li v-for="evale in datasetResult.evals" :key="evale">
                  <!-- Filter for each metric-->
                  {{ evale.evaluation.filtered }}
                  {{ evale.evaluation }}
                </li>
              </ul>
            </b-list-group>
          </b-list-group-item>
        </b-list-group>
        <b-row>
          <b-container>
            <b-row class="float-end">
              <b-col md="auto">
                <b>Select datasets to be shown:</b>
              </b-col>
              <b-col
                md="auto"
                class="form-check"
                v-for="dataset in uniqueDatasets"
                :key="dataset"
              >
                <input
                  v-model="visibleDatasets"
                  class="form-check-input"
                  type="checkbox"
                  :value="dataset"
                  :id="dataset"
                />
                <label class="form-check-label" :id="dataset">
                  {{ dataset }}
                </label>
              </b-col>
            </b-row>
          </b-container>
        </b-row>
      </div>
    </b-card>

    <b-card>
      <b-container>
        <b-row>
          <h4>Metrics</h4>
        </b-row>
        <b-row v-if="availableMetrics.length > 0">
          <b-container>
            <b-row class="float-end">
              <b-col md="auto">
                <b>Select metrics shown:</b>
              </b-col>
              <b-col
                md="auto"
                class="form-check"
                v-for="metric in availableMetrics"
                :key="metric"
              >
                <input
                  v-model="visibleMetrics"
                  class="form-check-input"
                  type="checkbox"
                  :value="metric"
                  :id="metric"
                />
                <label class="form-check-label" :id="metric">
                  {{ metric }}
                </label>
              </b-col>
            </b-row>
          </b-container>

          <b-row>
            <template v-for="runID in runNumbers">
              <b-button v-b-toggle="'metrics' + runID">
                <h4 class="opened">
                  <i class="bi bi-caret-down" /> Run {{ runID + 1 }}
                </h4>
                <h4 class="closed">
                  <i class="bi bi-caret-up" /> Run {{ runID + 1 }}
                </h4>
              </b-button>
              <b-collapse visible :id="'metrics' + runID">
                <b-container>
                  <b-row>
                    <b-col
                      :cols="result.result.length > 1 ? '6' : '12'"
                      v-for="(datasetResult, index) in result.result"
                      :key="runID + datasetResult"
                    >
                      <template
                        v-if="
                          visibleDatasets.includes(
                            datasetResult.dataset.dataset
                          )
                        "
                        :key="visibleDatasets"
                      >
                        <Table
                          :caption="datasetResult.dataset.dataset"
                          :results="hideResults(datasetResult.results[runID])"
                          :headers="hideHeaders(datasetResult.headers)"
                          :removable="false"
                        />
                        <b-button @click="exportTable(index, runID)"
                          >Export table</b-button
                        >
                      </template>
                    </b-col>
                  </b-row>
                </b-container>
              </b-collapse>
            </template>
          </b-row>
        </b-row>
        <template v-else>(None)</template>
      </b-container>
    </b-card>

    <b-card>
      <b-container>
        <b-row>
          <!-- Modal to compare ratings-->
          <b-modal v-model="showComparison" title="Comparison" size="xl">
            <b-container>
              <p v-if="comparisonTables.length === 0">No tables selected.</p>
              <template v-else>
                <b>Drag the tables to compare them.</b>
                <draggable v-model="comparisonTables" item-key="id" class="row">
                  <template #item="{ element, index }">
                    <b-col cols="6">
                      <b-row>
                        <b-button @click="comparisonTables.splice(index, 1)"
                          >X</b-button
                        ></b-row
                      >
                      <b-row>
                        <b-card>
                          <RatingsTable
                            :id="result.id"
                            :entry="userTables[element.pair]"
                            :pairData="result.result[element.pair].dataset"
                            :pairIndex="element.pair"
                            :runIndex="element.run"
                            @add="
                              (r, p) =>
                                comparisonTables.push({
                                  run: r,
                                  pair: p,
                                  id: r + ',' + p,
                                })
                            "
                            comparing
                          />
                        </b-card>
                      </b-row>
                    </b-col>
                  </template>
                </draggable>
              </template>
            </b-container>
          </b-modal>
        </b-row>
      </b-container>

      <b-container>
        <b-row>
          <b-col>
            <!--Type of experiment decides which label to give the section-->
            <h4 v-if="result.settings.experimentMethod === 'recommendation'">
              Recommended items per user
            </h4>
            <h4 v-else>Predicted rating per user</h4>
          </b-col>
          <b-col cols="3">
            <div class="float-end">
              <b-button variant="info" @click="showComparison = !showComparison"
                >Show comparison ({{
                  comparisonTables.length
                }}
                tables)</b-button
              >
            </div>
          </b-col>
        </b-row>
        <!--<div class="form-check">
      <input v-model="snippet" class="form-check-input" type="checkbox" :id="snippet" />
      <label class="form-check-label" :id="snippet">Show snippets</label>
      </div>-->
        <b-row>
          <b-container>
            <b-row class="float-end">
              <b-col md="auto">
                <b>Select rating tables shown:</b>
              </b-col>
              <b-col
                md="auto"
                class="form-check"
                v-for="entry in userTables"
                :key="entry"
              >
                <input
                  v-model="visibleMatrices"
                  class="form-check-input"
                  type="checkbox"
                  :value="entry"
                  :id="entry"
                />
                <label class="form-check-label" :id="entry">
                  {{ underscoreToSpace(entry) }}
                </label>
              </b-col>
            </b-row>
          </b-container>
        </b-row>

        <b-row>
          <!--Show recommendations for all datasets for now TODO-->
          <template v-for="run in runNumbers">
            <b-button v-b-toggle="'recs' + run">
              <h4 class="opened">
                <i class="bi bi-caret-down" /> Run {{ run + 1 }}
              </h4>
              <h4 class="closed">
                <i class="bi bi-caret-up" /> Run {{ run + 1 }}
              </h4>
            </b-button>
            <b-collapse visible :id="'recs' + run">
              <b-container>
                <b-row>
                  <template v-for="(entry, index) in userTables">
                    <template
                      v-if="
                        visibleDatasets.includes(getDatasetName(entry)) &&
                        visibleMatrices.includes(entry)
                      "
                    >
                      <div
                        :class="visibleMatrices.length > 1 ? 'col-6' : 'col'"
                        :key="run + entry"
                      >
                        <RatingsTable
                          :id="result.id"
                          :entry="underscoreToSpace(entry)"
                          :pairData="result.result[index].dataset"
                          :pairIndex="index"
                          :runIndex="run"
                          @add="
                            (r, p) => comparisonTables.push({ run: r, pair: p })
                          "
                        />
                      </div>
                    </template>
                  </template>
                </b-row>
              </b-container>
            </b-collapse>
          </template>
        </b-row>
      </b-container>
    </b-card>
  </div>
</template>

<style>
.collapsed > .opened {
  display: none;
}
:not(.collapsed) > .closed {
  display: none;
}
</style>
