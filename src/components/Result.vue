<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import Table from './Table.vue'
import mockdata from '../../api/mock/1647818279_HelloWorld/results-table.json'
import { ref } from 'vue'

const props = defineProps({ results: Array, headers: Array })

const recommendations = ref([
  {
    user: '1',
    dataset: 'LFM-1b',
    algorithm: 'ALS',
    item_1: 'Rolling in the deep',
    item_2: 'Umbrella',
    item_3: 'Firework',
  },
  {
    user: '2',
    dataset: 'LFM-1b',
    algorithm: 'ALS',
    item_1: 'Umbrella',
    item_2: 'Rolling in the deep',
    item_3: 'Heat waves',
  },
  {
    user: '1',
    dataset: 'LFM-1b',
    algorithm: 'POP',
    item_1: 'Umbrella',
    item_2: 'Heat waves',
    item_3: 'Umbrella',
  },
  {
    user: '2',
    dataset: 'LFM-1b',
    algorithm: 'POP',
    item_1: 'Umbrella',
    item_2: 'Rolling in de deep',
    item_3: 'Firework',
  },
])

const headers_rec = ref([
  { name: 'User' },
  { name: 'Dataset' },
  { name: 'Algorithm' },
  { name: 'Item 1' },
  { name: 'Item 2' },
  { name: 'Item 3' },
])
</script>

<template>
  <h1 class="display-2">Results</h1>
  <p class="lead">
    These are the results for your computation with the following name:
    {{ mockdata.computation_name }}.
  </p>

  <p>
    Tags:
    <tags v-for="tag in mockdata.tags"> {{ tag }} </tags>
  </p>

  <div class="container">
    <Table
      :results="props.results.length == 0 ? mockdata.body : props.results"
      :headers="props.results.length == 0 ? mockdata.headers : props.headers"
      :removable="false"
    />
  </div>

  <h6>Recommended items per user for dataset x and algorithm y</h6>
  <div class="container">
    <Table
      :results="recommendations"
      :headers="headers_rec"
      :removable="false"
    />
  </div>
</template>
