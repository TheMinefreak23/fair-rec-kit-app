<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { makeHeader, STANDARD_HEADERS } from '../../helpers/resultFormatter'
import { emptyFormGroup, reformat } from '../../helpers/optionsFormatter'
import { onMounted, ref } from 'vue'
import { API_URL } from '../../api'
import Table from '../Table.vue'

const RESULT_URL = API_URL + '/result/'

const props = defineProps({
  id: String,
  entry: String,
  pairData: Object,
  pairIndex: Number,
  runIndex: Number,
})

// Default headers for recommendation experiments.
const selectedHeaders = ref([
  [[{ name: 'Rank' }, { name: 'User' }, { name: 'Item' }, { name: 'Score' }]],
])
const ratings = ref([])

// Sorting / pagination
const startIndex = ref(0)
const sortIndex = ref(0)
const ascending = ref(true)
const entryAmount = ref(10)

// Headers (column filters) and filters (row filters)
const optionalHeaders = ref(STANDARD_HEADERS)
const optionalHeaderOptions = ref({})
const filters = ref(reformat(emptyFormGroup(false)))
const availableFilters = ref([])

onMounted(() => {
  // Load in all the user recommendation/prediction tables
  // Also initialize the components for table storage
  setRecs(parseInt(props.pairIndex), parseInt(props.runIndex))
})

/**
 * GET request: Get available header options for selection from server
 */
async function getHeaderOptions() {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      dataset: props.pairData.dataset,
      matrix: props.pairData.matrix,
    }),
  }
  const response = await fetch(RESULT_URL + 'headers', requestOptions)
  const data = await response.json()
  // console.log(data)
  optionalHeaderOptions.value = data
}

/**
 * GET request: Ask server for available filters
 */
async function getFilters() {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      dataset: props.pairData.dataset,
      matrix: props.pairData.matrix,
    }),
  }
  const response = await fetch(RESULT_URL + 'filters', requestOptions)
  const data = await response.json()
  // console.log(data)
  availableFilters.value = data.filters
}

/**
 * Handles sorting for tables that have pagination.
 * @param {int}   indexVar   - Index of the column on which is sorted.
 */
function paginationSort(indexVar) {
  // When sorting on the same column twice in a row, switch to descending.
  if (sortIndex.value === indexVar) {
    ascending.value = !ascending.value
  }

  // When sorting, start at startIndex 0 again to see either highest or lowest, passing on which column is sorted.
  sortIndex.value = indexVar
  startIndex.value = 0
  getUserRecs()
}

/**
 * Update headers shown in user recommendations
 * @param {Array}   headers  - A list of the headers that have been selected to be shown
 */
function updateHeaders(headers) {
  optionalHeaders.value = headers
  getUserRecs()
}

/**
 * Update headers shown in user recommendations
 * @param {Array}  changedFilters - A list of filters that are selected
 */
function changeFilters(changedFilters) {
  // TODO why filters ref? refactor?
  filters.value = reformat(changedFilters)
  console.log('changeFilters filters', filters.value)
  getUserRecs()
}

/**
 * Loads more data in the table after user asks for more data.
 * @param {Bool}   increase  - Determines whether the next or previous data is required.
 * @param {Int}    amount    - Number of items that the user has requested.
 */
function loadMore(increase, amount) {
  amount = parseInt(amount)

  // Determine the index for where the next page starts, based on how many entries were shown before.
  if (increase != null) {
    if (!increase) startIndex.value -= amount
    if (startIndex.value < 0) startIndex.value = 0
    else if (increase) startIndex.value += entryAmount.value
  }

  // Update amount to new number of entries that are shown.
  entryAmount.value = amount
  getUserRecs()
}

// POST request: Send result ID to the server to set recommendations for the current experiment.
async function setRecs() {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: props.id,
      runid: props.runIndex,
      pairid: props.pairIndex,
    }),
  }
  console.log('sending to server:', requestOptions.body)
  const response = await fetch(RESULT_URL + 'set-recs', requestOptions)
  if (response.status === 200) {
    // console.log('set recs current table', currentTable)
    getHeaderOptions()
    getFilters()
    getUserRecs()
  }
}

/**
 * POST request: Ask server for next part of user recommendation table.
 */
async function getUserRecs() {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: props.id,
      pairid: props.pairIndex,
      runid: props.runIndex,
      start: startIndex.value,
      sortindex: sortIndex.value,
      ascending: ascending.value,
      amount: entryAmount.value,
      filters: filters.value,
      optionalHeaders: optionalHeaders.value,
      dataset: props.pairData.dataset,
      matrix: props.pairData.matrix,
    }),
  }
  const response = await fetch(RESULT_URL, requestOptions)
  ratings.value = await response.json()
  selectedHeaders.value = Object.keys(ratings.value[0])
}
</script>

<template>
  <div>
    <h4>Run {{ runIndex }}</h4>
    <Table
      :key="
        availableFilters +
        optionalHeaderOptions +
        pairData +
        runIndex +
        pairIndex
      "
      v-if="selectedHeaders"
      :caption="entry"
      :results="ratings"
      :headers="selectedHeaders.map(makeHeader)"
      :filterOptions="availableFilters"
      :headerOptions="optionalHeaderOptions"
      :defaultSort="0"
      :startIndex="startIndex"
      pagination
      recs
      @paginationSort="(i) => paginationSort(i)"
      @loadMore="(increase, amount) => loadMore(increase, amount)"
      @changeFilters="(changedFilters) => changeFilters(changedFilters)"
      @updateHeaders="(headers) => updateHeaders(headers)"
    />
  </div>
</template>
