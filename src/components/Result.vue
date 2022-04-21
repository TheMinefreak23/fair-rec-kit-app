<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import Table from './Table.vue'
import { onMounted, ref, watch } from 'vue'

import mockdata from '../../api/mock/1647818279_HelloWorld/results-table.json'
import { API_URL } from '../api'

const props = defineProps({ headers: Array, result: Object })

const headers_rec = ref([{ name: 'User' }, { name: 'Item' }, { name: 'Score' }])
const headers_options = ref([{ name: 'Option1' }, { name: 'Option2' }, { name: 'Option3' }])

const computation_tags = ref(['tag1 ', 'tag2 ', 'tag3 ', 'tag4 '])

const data = ref([])
const startIndex = ref(0)
const index = ref(0)
const ascending = ref(true)
const entryAmount = ref(20)

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
    }),
  }

  const response = await fetch(API_URL + '/all-results/result', requestOptions)
  data.value.results = await response.json()
}

//Loads more data in the table after user asks for more data.
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

function handleScroll() {
  console.log('test')
}
</script>

<template>
  <div class="container">
    <h1 class="display-2">Results</h1>
    <p class="lead">
      These are the results for your computation with the following name:
      {{ result.name }}.
    </p>

    <div class="col">
      Tags:
      <template v-for="tag in mockdata.computation_tags"
        >{{ tag }} <slot> </slot
      ></template>
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
          caption=""
          :results="data.results"
          :headers="headers_rec"
          :headerOptions = "headers_options"
          pagination
          expandable
          @paginationSort="(i) => paginationSort(i)"
          @loadMore="(increase, amount) => loadMore(increase, amount)"
        />
      </div>
      <!--</template>-->
    </div>
  </div>
</template>
