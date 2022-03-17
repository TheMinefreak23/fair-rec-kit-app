<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import Table from './Table.vue'
import { ref } from 'vue'

const results = ref([
  { dataset: 'LFM-1b', algorithm: 'ALS', fst_female: '6.7717', fst_male : '0.6142' , hellinger_distance: '0.0988' , precision_p1 : '0.4505' },
  { dataset: 'LFM-1b', algorithm: 'POP', hellinger_distance: '0.1577' , precision_p1 : '0.1033' }
])

const recommendations = ref([
  { user_id: '1', rec_item1: 'song1', rec_item2:'song2' }
])

const headers = ref([
  {name: 'dataset',},
  {name: 'algorithm'},
  {name: 'avg_position' , subheaders: ['fst_female', 'fst_male']},
  {name: 'hellinger_distance'},
  {name:'precision_p1'}])
const headers_rec = ref(['user_id', 'rec_item1', 'rec_item2'])
const pretty_headers = ref(['Dataset', 'Algorithm', 'Hellinger distance', 'Precision p1@k'])
const pretty_headers_rec= ref([ 'User id', 'First recommended item', 'Second recommended item'])

const computation_name = ref('computation1')
const computation_tags = ref(['tag1 ', 'tag2 ', 'tag3 ', 'tag4 '])

</script>

<template>
  <h1 class="display-2"> Results</h1>
  <p class="lead">
    These are the results for your computation with the following name: {{computation_name}}.
  </p>
  
  <p>
    Tags: 
      <tags v-for="tag in computation_tags"> {{tag}} </tags>
  </p>

  <div class = "container">
    <Table :results="results" :headers="headers" :pretty_headers="pretty_headers"/>
  </div>

  <h6> Recommended items per user for dataset x and algorithm y </h6>
  <div class="container">
    <Table :results="recommendations" :headers="headers_rec" :pretty_headers="pretty_headers_rec"/>
  </div>
</template>

