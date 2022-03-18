<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import Table from './Table.vue'
import { ref } from 'vue'

const results = ref([{
    dataset: 'LFM-1b',
    algorithm: 'ALS',
    fst_female: '6.7717',
    fst_male: '0.6142',
    hellinger_distance: '0.0988',
    precision_p1: '0.4505',
}, {
    dataset: 'LFM-1b',
    algorithm: 'POP',
    fst_female: '0.1325',
    fst_male: '1.7299',
    hellinger_distance: '0.1577',
    precision_p1: '0.1033',
}]);

const headers = ref([{ name: 'dataset' }, { name: 'algorithm' }, {
    name: 'avg_position',
    subheaders: ['fst_female', 'fst_male'],
}, { name: 'hellinger_distance' }, { name: 'precision_p1' }]);


const recommendations = ref([
  { user: '1', dataset: 'LFM-1b' , algorithm: 'ALS', item_1: 'Rolling in the deep', item_2: 'Umbrella', item_3: 'Firework' },
  { user: '2', dataset: 'LFM-1b' , algorithm: 'ALS', item_1: 'Umbrella', item_2: 'Rolling in the deep', item_3: 'Heat waves' },
  { user: '1', dataset: 'LFM-1b' , algorithm: 'POP', item_1: 'Umbrella', item_2: 'Heat waves', item_3: 'Umbrella' },
   { user: '2', dataset: 'LFM-1b' , algorithm: 'POP', item_1: 'Umbrella', item_2: 'Rolling in de deep', item_3: 'Firework' }
])

const headers_rec = ref([
  {name: 'user'},
  {name: 'dataset'},
  {name: 'algorithm'},
  {name: 'item_1' },
  {name: 'item_2'},
  {name:'item_3'}])

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
    <Table :results="results" :headers="headers"/>
  </div>

  <h6> Recommended items per user for dataset x and algorithm y </h6>
  <div class="container">
    <Table :results="recommendations" :headers="headers_rec" />
  </div>


</template>

