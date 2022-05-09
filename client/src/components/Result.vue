<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import Table from './Table.vue'
import { onMounted, ref, watch } from 'vue'

import mockdata from '../../../server/mock/1647818279_HelloWorld/results-table.json'
import { API_URL } from '../api'

const props = defineProps({ headers: Array, result: Object })

//Default headers for recommendation experiments.
const headers_rec = ref([{ name: 'Rank'}, { name: 'User' }, { name: 'Item' }, { name: 'Score' }])
//Default headers for prediction experiments
const headers_pre = ref([{ name: 'User' }, { name: 'Item' }, { name: 'Predicted Score' }])

const experiment_tags = ref(['tag1 ', 'tag2 ', 'tag3 ', 'tag4 '])

const data = ref([])
const startIndex = ref(0)
const index = ref(0)
const ascending = ref(true)
const entryAmount = ref(20)
const userHeaders = ref([])
const itemHeaders = ref([])
const generalHeaders = ref([])
const userHeaderOptions = ref([])
const itemHeaderOptions = ref([])
const generalHeaderOptions = ref([])

watch(
  () => props.result,
  async (newResult) => {
    //console.log(newResult.id)
    setRecs()
  }
)

onMounted(() => {
  setRecs()
})

// GET request: Get available options for selection from server
async function getHeaders() {
  const response = await fetch(API_URL + '/all-results/headers')
  const data = await response.json()
  
  generalHeaderOptions.value = makeHeaders(data.headers)
  itemHeaderOptions.value = makeHeaders(data.itemHeaders)
  userHeaderOptions.value = makeHeaders(data.userHeaders)
}

//POST request: Send result ID to the server to set current shown recommendations.
async function setRecs() {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: props.result.id,
    }),
  }
  fetch(API_URL + '/all-results/set-recs', requestOptions).then(() => {
    getUserRecs()
    getHeaders()
  })
}

//POST request: Ask server for next part of user recommendation table.
async function getUserRecs() {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: props.result.id,
      start: startIndex.value,
      sortindex: index.value,
      ascending: ascending.value,
      amount: entryAmount.value,
      generalHeaders: generalHeaders.value,
      itemheaders: itemHeaders.value,
      userheaders: userHeaders.value,
    }),
  }

  const response = await fetch(API_URL + '/all-results/result', requestOptions)
  data.value.results = await response.json()
}

/**
 * Loads more data in the table after user asks for more data.
 * @param {Bool}   increase  - Determines whether the next or previous data is required.
 * @param {Int}    amount    - Number of items that the user has requested.
 */
function loadMore(increase, amount) {
  amount = parseInt(amount)

  //Determine the index for where the next page starts, based on how many entries were shown before.
  if (!increase && startIndex.value > 0) startIndex.value -= entryAmount.value
  if (startIndex.value < 0) startIndex.value = 0
  else if (increase) startIndex.value += entryAmount.value
  else startIndex.value = 0

  //Update amount to new number of entries that are shown.
  entryAmount.value = amount
  getUserRecs()
}

/**
 * Handles sorting for tables that have pagination.
 * @param {int}   indexVar  - Index of the column on which is sorted.
 */
function paginationSort(indexVar) {
  //When sorting on the same column twice in a row, switch to descending.
  if (index.value === indexVar) {
    ascending.value = !ascending.value
  }

  //When sorting, start at startIndex 0 again to see either highest or lowest, passing on which column is sorted.
  index.value = indexVar
  startIndex.value = 0
  getUserRecs()
}


/**
 * Update headers shown in user recommendations
 * @param {Array}   generalHeader  - list of headers that apply to the user-item pair.
 * @param {Array}   userHeader    - list of headers that apply to the user entries.
 * @param {Array}   itemHeader    - list of headers that apply to the item entries.
 */
function updateHeaders(generalHeader, userHeader, itemHeader) {
  generalHeaders.value = makeHeaders(generalHeader)
  userHeaders.value = makeHeaders(userHeader)
  itemHeaders.value = makeHeaders(itemHeader)
  getUserRecs()
}


/**
 * convert list of header names into supported header format, capitalize and remove underscores
 * @param {Array}   headers  - list of headers.
 */
function makeHeaders(headers) {
  for(var i=0; i<headers.length; i++){
    headers[i] = capitalizeFirstLetter(headers[i].replace("_", " "))
  }
  return headers.map((header) => ({
        name: header,
      }))
}

/**
 * Capitalize the first letter of a string
 * @param {int}   string  - the string that needs to be capitalized.
 */
function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

</script>

<template>
  <div class="container">
    <h1 class="display-2">Results</h1>
    <p class="lead">
      These are the results for experiment {{ result.metadata.name }} done at
      {{ result.metadata.datetime }}.
    </p>

    <div class="col">
      Tags:
      <template v-if="!result.metadata.tags">None</template>
      <template v-for="tag in result.metadata.tags">
        <b-button disabled> {{ tag }} </b-button
        ><!--<slot> </slot>-->
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
        <div class="col-6">
          <Table
            :caption="datasetResult.caption"
            :results="datasetResult.results"
            :headers="datasetResult.headers"
            :removable="false"
          />
        </div>
      </template>
    </div>
  </div>

  <div class="container">
    <div class="row">
      <h4>Recommended items per user</h4>
    </div>
    <div class="row">
      <!--Show recommendations for all datasets for now TODO-->
      <!--<template v-for="data in [data]" :key="data">-->
      <div class="col-6">
        <Table
          caption="Testcaption"
          :results="data.results"
          :headers="
            headers_rec
              .concat(generalHeaders)
              .concat(userHeaders)
              .concat(itemHeaders)
          "
          :headerOptions="generalHeaderOptions"
          :userOptions="userHeaderOptions"
          :itemOptions="itemHeaderOptions"
          pagination
          expandable
          @paginationSort="(i) => paginationSort(i)"
          @loadMore="(increase, amount) => loadMore(increase, amount)"
          @updateHeaders="(general, user, item) => updateHeaders(general, user, item)"
        />
      </div>
      <!--</template>-->
    </div>
  </div>
</template>
