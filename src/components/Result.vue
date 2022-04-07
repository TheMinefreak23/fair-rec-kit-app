<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import Table from './Table.vue'
import { onMounted, ref, watch } from 'vue'

import mockdata from '../../api/mock/1647818279_HelloWorld/results-table.json'
import { store } from '../store.js'
import { formatResult } from '../helpers/resultFormatter'
import { API_URL } from '../api'

const props = defineProps({ headers: Array })

const headers_rec = ref([{ name: 'User' }, { name: 'Item' }, { name: 'Score' }])

const computation_name = ref('computation1')
const computation_tags = ref(['tag1 ', 'tag2 ', 'tag3 ', 'tag4 '])

const data = ref([])
const startIndex = ref(0)
const index = ref(0)
const ascending = ref(true)
const entryAmount = ref(20)

const testcaption = ref('Dataset: LFM-1b, Algorithm: ALS')


watch(
  () => store.queue,
  (newQueue, oldQueue) => {
    if (newQueue.length < oldQueue.length) getCalculation()
  }
)

function makeHeaders(result) {
  //console.log(result)
  const headers = Object.keys(result).map((key) => ({
    name: key,
  }))
  //console.log(headers)
  return headers
}

// GET request: Ask server for latest calculation
async function getCalculation() {
  const response = await fetch(API_URL + '/computation/calculation')
  const data = await response.json()
  console.log(data)
  //if (Object.keys(data).length === 0) // not null check
    //store.currentResult = data.calculation
    store.currentResult = formatResult(data.calculation)
  console.log(store.currentResult)
}

//POST request: Ask server for next part of user recommendation table.
async function getUserRecs() {

  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ start: startIndex.value , sortindex: index.value, ascending: ascending.value, amount: entryAmount.value}),
  }

  const response = await fetch(API_URL + '/all-results/result', requestOptions)
  data.value = (await response.json())
}

//Loads more data in the table after user asks for more data.
function loadMore(increase, amount){
  amount = parseInt(amount)  

  //Determine the index for where the next page starts, based on how many entries were shown before.
  if(!increase && startIndex.value > 0)
    startIndex.value -=entryAmount.value
      if(startIndex.value < 0)
      startIndex.value = 0

  else if(increase)
    startIndex.value += entryAmount.value

  else
    startIndex.value = 0
  
  //Update amount to new number of entries that are shown.
  entryAmount.value = amount 
  getUserRecs()
}

function paginationSort(indexVar){ 
  //When sorting on the same column twice in a row, switch to descending.
  if(index.value === indexVar){
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

onMounted(() => {
  getUserRecs()
})
</script>

<template>
<div class="container">
  <h1 class="display-2">Results</h1>
  <p class="lead">
    These are the results for your computation with the following name:
    {{
      store.currentResult.length == 0
        ? mockdata.computation_name
        : store.currentResult.name
    }}.
  </p>

  <div class="col">
    Tags:
    <template v-for="tag in mockdata.computation_tags">{{ tag }} <slot> </slot></template>
  </div>

</div>

  <div class="container">
    <div class="row">
      <div class="col-6">
        <Table
          :results="
            store.currentResult.length == 0
              ? mockdata.body
              : store.currentResult.result
          "
          :headers="
            store.currentResult.length == 0
              ? mockdata.headers
              : makeHeaders(store.currentResult.result[0])
          "
          :removable="false"
        />
      </div>
      <div class="col-6">
        <Table
          :results="
            store.currentResult.length == 0
              ? mockdata.body
              : store.currentResult.result
          "
          :headers="
            store.currentResult.length == 0
              ? mockdata.headers
              : makeHeaders(store.currentResult.result[0])
          "
          :removable="false"
        />
      </div>
    </div>
  </div>

  <div class="container">
    <div class="row">
      <h4>Recommended items per user</h4>
    </div>
    <div class="row">
      <div class="col-6">
          <Table 
            :caption="testcaption"
            :results="data" 
            :headers="headers_rec" 
            pagination
            @paginationSort="(i) => paginationSort(i)"
            @loadMore="(increase, amount) => loadMore(increase, amount)" 
            />
      </div>
      <div class="col-6">
          <Table 
          :caption="testcaption"
          :results="data" 
          :headers="headers_rec" 
          pagination
          @paginationSort="(i) => paginationSort(i)"
          @loadMore="(increase, amount) => loadMore(increase, amount)" 
          />
      </div>
    </div>
  </div>
</template>
