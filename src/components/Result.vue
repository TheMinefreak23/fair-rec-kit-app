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
  const response = await fetch(
    'http://localhost:5000/all-results/result/?start=0'
  )
  data.value = await response.json()
  console.log(data.value)
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
    <tags v-for="tag in mockdata.tags"> {{ tag }} </tags>
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
          v-on:scroll.passive="handleScroll"
          :results="data"
          :headers="headers_rec"
          :removable="false"
        />
      </div>
      <div class="col-6">
        <Table :results="data" :headers="headers_rec" :removable="false" />
      </div>
    </div>
  </div>
</template>
