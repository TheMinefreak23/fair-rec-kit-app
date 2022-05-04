<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import Table from './Table.vue'
import { onMounted, ref, watch } from 'vue'

import mockdata from '../../../server/mock/1647818279_HelloWorld/results-table.json'
import { API_URL } from '../api'

const props = defineProps({ headers: Array, result: Object })

const headers_rec = ref([{ name: 'User' }, { name: 'Item' }, { name: 'Score' }])

const computation_tags = ref(['tag1 ', 'tag2 ', 'tag3 ', 'tag4 '])

const data = ref([])
const startIndex = ref(0)
const index = ref(0)
const ascending = ref(true)
const entryAmount = ref(20)
const userHeaders = ref([])
const itemHeaders = ref([])
const headers = ref([])

watch(
  () => props.result,
  async (newResult) => {
    console.log(newResult.id, newResult)
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
  
  headers.value = data.headers
  itemHeaders.value = data.itemHeaders
  userHeaders.value = data.userHeaders

  console.log(headers.value)

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
      headers: headers.value,
      itemheaders: itemHeaders.value,
      userheaders: userHeaders.value
    }),
  }

  const response = await fetch(API_URL + '/result/result', requestOptions)
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

//Update headers shown in user recommendations
function changeColumns(generalHeader, userHeader, itemHeader) {
  ;(headers.value = generalHeader),
    (userHeaders.value = userHeader),
    (itemHeaders.value = itemHeader)

  console.log(headers.value)
  getUserRecs()
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
          :headers="headers_rec"
          :headerOptions = "headers"
          :userOptions = "userHeaders"
          :itemOptions = "itemHeaders"
          pagination
          expandable
          @paginationSort="(i) => paginationSort(i)"
          @loadMore="(increase, amount) => loadMore(increase, amount)"
          @changeColumns="
            (general, user, item) => changeColumns(general, user, item)
          "
        />
      </div>
      <!--</template>-->
    </div>
  </div>
</template>
