<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import Table from './Table.vue'
import { onMounted, ref, watch } from 'vue'

import mockdata from '../../api/mock/1647818279_HelloWorld/results-table.json'
import { store } from '../store.js'
import { formatResult } from '../helpers/resultFormatter'

const props = defineProps({ headers: Array })

const headers_rec = ref([{ name: 'User' }, { name: 'Item' }, { name: 'Score' }])

const computation_name = ref('computation1')
const computation_tags = ref(['tag1 ', 'tag2 ', 'tag3 ', 'tag4 '])

const data = ref([])
const page = ref(0)
const index = ref(0)
const ascending = ref(true)


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
  const response = await fetch('http://localhost:5000/computation/calculation')
  const data = await response.json()
  console.log(data)
  if (Object.keys(data).length === 0)
    store.currentResult = formatResult(data.calculation)
  console.log(store.currentResult)
}

async function getUserRecs() {

  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ start: page.value , sortindex: index.value, ascending: ascending.value}),
  }

  const response = await fetch('http://localhost:5000/all-results/result', requestOptions)
  data.value = (await response.json())
}

//Loads more data, keeps track of which "page" of data user is on.
function loadMore(increase){
  if(!increase && page.value > 0)
    page.value--
  else if(increase)
    page.value++
  else
    page.value = 0
  getUserRecs()
}

function paginationSort(indexVar){ 
  //When sorting on the same column twice in a row, switch to descending.
  if(index.value === indexVar){
    ascending.value = !ascending.value
  }

  //When sorting, start at page 0 again to see either highest or lowest, passing on which column is sorted.
  index.value = indexVar
  page.value = 0
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
  <h1 class="display-2">Results</h1>
  <p class="lead">
    These are the results for your computation with the following name:
    {{
      store.currentResult.length == 0
        ? mockdata.computation_name
        : store.currentResult.name
    }}.
  </p>

  <p>
    Tags:
    <div v-for="tag in mockdata.tags"> {{ tag }} </div>
  </p>

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

  <h6>Recommended items per user for dataset x and algorithm y</h6>
  <div class="container">
    <div class="row">
      <div class="col-6">
          <Table 
            :results="data" 
            :headers="headers_rec" 
            pagination
            @paginationSort="(i) => paginationSort(i)"
            @loadMore="(increase) => loadMore(increase)" 
            />
      </div>
      <div class="col-6">
          <Table 
          :results="data" 
          :headers="headers_rec" 
          pagination
          @paginationSort="(i) => paginationSort(i)"
          @loadMore="(increase) => loadMore(increase)" 
          />
      </div>
    </div>
  </div>
</template>
