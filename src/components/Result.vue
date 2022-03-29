<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import Table from './Table.vue'
import { onMounted, ref } from 'vue'


import mockdata from '../../api/mock/1647818279_HelloWorld/results-table.json'

const props = defineProps({ results: Array, headers: Array })


const headers_rec = ref([
  { name: 'User' },
  { name: 'Item' },
  { name: 'Score' },
])

const computation_name = ref('computation1')
const computation_tags = ref(['tag1 ', 'tag2 ', 'tag3 ', 'tag4 '])

const data = ref([])
const page = ref(0)

async function getUserRecs() {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ start: page.value }),
  }

  const response = await fetch('http://localhost:5000/all-results/result', requestOptions)
  data.value = (await response.json())
}

function log(){
  console.log("hi2");
}
function loadMore(){
  console.log("button pressed");
  page.value++
  getUserRecs()
}

function paginationSort(index){
  
}

onMounted(() => {
  getUserRecs()
})

</script>

<template>
  <h1 class="display-2">Results</h1>
  <p class="lead">
    These are the results for your computation with the following name:
    {{ mockdata.computation_name }}.
  </p>

  <p>
    Tags:
    <div v-for="tag in mockdata.tags"> {{ tag }} </div>
  </p>

  <div class="container">
    <div class="row">
      <div class="col-6">
         <Table
          :results="props.results.length == 0 ? mockdata.body : props.results"
          :headers="props.results.length == 0 ? mockdata.headers : headers"
          :removable="false"
          />
      </div>
      <div class="col-6">
         <Table
          :results="props.results.length == 0 ? mockdata.body : props.results"
          :headers="props.results.length == 0 ? mockdata.headers : headers"
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
            :removable="false"
            pagination
            @loadMore="() => loadMore()" 
            />
      </div>
      <div class="col-6">
          <Table 
          :results="data" 
          :headers="headers_rec" 
          :removable="false" 
          pagination
          @loadMore="() => loadMore()" 
          />
      </div>
    </div>  
  </div>
</template>
