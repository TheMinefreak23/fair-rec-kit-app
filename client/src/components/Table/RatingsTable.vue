<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { makeHeader, STANDARD_HEADERS } from '../../helpers/resultFormatter'
import { emptyFormGroup, reformat } from '../../helpers/optionsFormatter'
import { computed, onMounted, ref, watch } from 'vue'
import FormGroupList from '../Form/FormGroupList.vue'
// import VueDragResize from 'vue-drag-resize/src/component/vue-drag-resize.vue'
import { API_URL } from '../../api'
import Table from '../Table.vue'
import HeadersModal from '../Table/Modals/HeadersModal.vue'
import FilterOverview from '../Form/FilterOverview.vue'

const RESULT_URL = API_URL + '/result/'

const emit = defineEmits(['add'])
const props = defineProps({
  id: String,
  entry: String,
  pairData: Object,
  pairIndex: Number,
  runIndex: Number,
  //poppable: { type: Boolean, default: true },
  initValues: Object,
  comparing: { type: Boolean, default: false },
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
const filters = ref(emptyFormGroup(false))
const availableFilters = ref([])

// Modals
const filtersModalShow = ref(false)

// Pop out
// const showPopout = ref(false)

onMounted(() => {
  if (props.comparing) entryAmount.value = 5
  // Set initial values if given
  if (props.initValues) {
    console.log('initial values', props.initValues)
    startIndex.value = props.initValues.startIndex
    sortIndex.value = props.initValues.sortIndex
    ascending.value = props.initValues.ascending
    optionalHeaders.value = props.initValues.optionalHeaders
    filters.value = props.initValues.filters
  }
  // Load the full user recommendation/prediction table
  setRecs()
})

watch(optionalHeaders, () => {
  if (ratings.value) getUserRecs()
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
      filters: reformat(filters.value),
      optionalHeaders: optionalHeaders.value,
      dataset: props.pairData.dataset,
      matrix: props.pairData.matrix,
    }),
  }
  console.log('getting ratings for', props.id)
  const response = await fetch(RESULT_URL, requestOptions)
  ratings.value = await response.json()
  selectedHeaders.value = Object.keys(ratings.value[0])
}
</script>

<template>
  <b-overlay :show="ratings == []">
    <!-- Filters Modal -->
    <b-modal
      id="change-columns-modal"
      v-model="filtersModalShow"
      title="Change filters"
      @ok="getUserRecs"
    >
      <FormGroupList
        v-model="filters"
        name="filter pass"
        title="subset"
        :options="availableFilters"
        :useFilterModal="false"
      />
    </b-modal>
    <!--Clone this table to the popout.-->
    <!--<VueDragResize :isActive="false" v-if="poppable && showPopout">
      <b-card>
        <b-button @click="showPopout = !showPopout">Close</b-button>
        <RatingsTable
          :id="id"
          :entry="entry"
          :pairData="pairData"
          :pairIndex="pairIndex"
          :runIndex="runIndex"
          :poppable="false"
        />
      </b-card>
    </VueDragResize>
    <b-button @click="showPopout = !showPopout">Pop out</b-button>
    -->
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
      :defaultSort="0"
      :startIndex="startIndex"
      pagination
      recs
      :comparing="comparing"
      @paginationSort="(i) => paginationSort(i)"
      @loadMore="(increase, amount) => loadMore(increase, amount)"
    >
      <b-container>
        <b-row>
          <!--Main headers selection-->
          <b-col>
            <b-button
              variant="info"
              @click="
                $emit('add', {
                  run: runIndex,
                  pair: pairIndex,
                  settings: {
                    startIndex: startIndex,
                    sortIndex: sortIndex,
                    ascending: ascending,
                    optionalHeaders: optionalHeaders,
                    filters: filters,
                  },
                })
              "
              >Add table to comparison
            </b-button>
            <b-row>
              <!--HELLO?
      <b-col v-for="category in Object.keys(optionalHeaderOptions)">
        {{ category }}
        <b-form-checkbox-group v-model="optionalHeaders">
          <template v-for="header in optionalHeaderOptions[category]">
            {{ header }}
            <template v-if="STANDARD_HEADERS.includes(header)">
              <b-form-checkbox :value="header" switch>{{
                header
              }}</b-form-checkbox>
            </template>
          </template>
        </b-form-checkbox-group>
      </b-col>-->
              <b-col>
                <b-row> <p>Main headers:</p></b-row>
                <b-row md="auto">
                  <template
                    v-for="category in Object.keys(optionalHeaderOptions)"
                    :key="category"
                  >
                    <b-col
                      md="auto"
                      class="form-check form-switch"
                      v-for="header in optionalHeaderOptions[category]"
                      :key="header"
                    >
                      <template v-if="STANDARD_HEADERS.includes(header)">
                        <input
                          v-model="optionalHeaders"
                          class="form-check-input"
                          type="checkbox"
                          :value="header"
                          :id="header"
                        />
                        <label class="form-check-label" :id="header">
                          {{ makeHeader(header).name }}
                        </label>
                      </template>
                    </b-col>
                  </template>
                </b-row>
              </b-col>
            </b-row>
          </b-col>
          <b-col>
            <!-- Headers and filters modal buttons -->
            <div class="float-end">
              <!--TODO use Table slot for the headers/filters, handle them in RatingsTable-->
              <!--
            <h2>{{ headerOptions }}</h2>
            <h2>{{ filterOptions }}</h2>
            -->
              <HeadersModal
                :headerOptions="optionalHeaderOptions"
                @updateHeaders="updateHeaders"
              />
              <b-button
                @click="filtersModalShow = !filterModalShow"
                class="m-1"
                data-testid="filterButton"
                variant="warning"
              >
                Select Filters
              </b-button>
              <!--TODO: show selected filters-->
              <!--<b-row>
                <FilterOverview :filters="filters" />
              </b-row>-->
            </div>
          </b-col>
        </b-row>
      </b-container>
    </Table>
  </b-overlay>
</template>
