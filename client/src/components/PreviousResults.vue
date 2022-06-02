<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */
import Table from './Table.vue'
import { onMounted, ref, watch } from 'vue'
import { formatResults, formatResult } from '../helpers/resultFormatter.js'

import { addResult, store } from '../store.js'
import { API_URL } from '../api'
import { viewResult } from '../helpers/resultRequests.js'

const headers = ref([
  { name: 'ID' },
  { name: 'Date Time' },
  { name: 'Name' },
  { name: 'Tags' },
  { name: 'Datasets' },
  { name: 'Approaches' },
  { name: 'Metrics' },
  { name: '' },
])

onMounted(() => {
  getResults()
})

watch(
  () => store.currentResults.length,
  () => {
    getResults()
  }
)

async function getResults() {
  const response = await fetch(API_URL + '/all-results/')
  const data = await response.json()
  store.allResults = formatResults(data.all_results)
}
</script>

<template>
  <b-card>
    <div class="text-center py-2 mx-5">
      <h3>Previous results</h3>
      <Table
        @viewResult="viewResult"
        @loadResults="getResults"
        :results="store.allResults"
        :headers="headers"
        removeText="Remove"
        removable
        editable
        overview
        serverFile="/all-results/delete"
        serverFile2="/all-results/edit"
        :defaultSort="1"
      />
    </div>
  </b-card>
</template>
