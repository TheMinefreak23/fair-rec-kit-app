<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import Table from './Table.vue'
import { ref } from 'vue'

const results = ref([
  { dataset: 'LFM-1b', algorithm: 'ALS', hellinger_distance: '0.0988' , precision_p1 : '0.4505' }
])

const recommendations = ref([
  { user_id: '1', rec_item1: 'song1', rec_item2:'song2' }
])

const headers = ref(['dataset', 'algorithm', 'hellinger_distance', 'precision_p1'])
const headers_rec = ref(['user_id', 'rec_item1', 'rec_item2'])
const pretty_headers = ref(['Dataset', 'Algorithm', 'Hellinger distance', 'Precision p1@k'])
const pretty_headers_rec= ref([ 'User id', 'First recommended item', 'Second recommended item'])
</script>

<template>
  <h1 class="display-2"> Results</h1>
  <p class="lead">
    These are the results for your computation.
  </p>

  <div class = "container">
    <Table :results="results" :headers="headers" :pretty_headers="pretty_headers"/>
  </div>

  <div class="container">
    <Table :results="recommendations" :headers="headers_rec" :pretty_headers="pretty_headers_rec"/>
  </div>
</template>

