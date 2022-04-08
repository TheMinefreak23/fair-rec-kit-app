<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import Table from './Table.vue'
import { onMounted, ref } from 'vue'

const props = defineProps({ results: Array, headers: Array })


const headers_rec = ref([
  { name: 'User' },
  { name: 'Item' },
  { name: 'Score' },
])

const computation_name = ref('computation1')
const computation_tags = ref(['tag1 ', 'tag2 ', 'tag3 ', 'tag4 '])

const data = ref([])
const run_data = ref([])
const name = ""

async function getUserRecs() {
  const response = await fetch('http://localhost:5000/all-results/result-by-id')
  data.value = (await response.json())
  console.log("data has been loaded in!")
  console.log(data)
}

onMounted(() => {
  getUserRecs()
})

</script>

<template>
  <h1 class="display-2">Results</h1>
  <p class="lead">
    These are the results for your computation with the following name:
    {{ name }}.
  </p>

  <p>
    Tags:
    <!--<tags v-for="tag in mockdata.tags"> {{ tag }} </tags>-->
  </p>
<!--
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
          <Table :results="data" :headers="headers_rec" :removable="false" />
      </div>
      <div class="col-6">
          <Table :results="data" :headers="headers_rec" :removable="false" />
      </div>
    </div>  
  </div>-->
</template>
