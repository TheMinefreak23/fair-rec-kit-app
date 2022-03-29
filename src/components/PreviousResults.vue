<script setup>
import Table from './Table.vue'
import { onMounted, ref } from 'vue'
const exResults = ref([
  { id: 1, age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
  { id: 2, age: 21, first_name: 'Larsen', last_name: 'Shaw' },
  { id: 3, age: 89, first_name: 'Geneva', last_name: 'Wilson' },
  { id: 4, age: 38, first_name: 'Jami', last_name: 'Carney' },
])
const exHeaders = ref(['id', 'age', 'first_name', 'last_name'])
const headers = ref([
  { name: 'Date Time' },
  { name: 'Name' },
  { name: 'Datasets' },
  { name: 'Approaches' },
  { name: 'Metrics' },
])

const ex1CurrentPage = ref(1)
const ex1PerPage = ref(10)
const ex1Rows = ref(100)

//const returnMessage = ref('')
const results = ref([])

onMounted(() => {
  getResults()
})

async function getResults() {
  const response = await fetch('http://localhost:5000/all-results')
  const data = await response.json()
  //returnMessage.value = 'the results have been gotten'
  console.log(data)
  let allResults = data.all_results
  for (let i in allResults) {
    let approach = allResults[i].settings.approaches[0]
    let apprName = approach ? approach.name : 'NULL'
    let metric = allResults[i].settings.metrics[0]
    let metricName = metric ? metric.name : 'NULL'

    results.value[i] = {
      datetime: allResults[i].timestamp.datetime,
      name: allResults[i].metadata.name,
      dataset: allResults[i].settings.datasets[0],
      approach: apprName,
      metric: metricName,
    }
  }
}
</script>

<template>
  <div class="text-center py-2 mx-5">
    <h3>Previous results</h3>
    <Table :results="results" :headers="headers" />
    <!--<form @submit.prevent="getResults">
      <input v-model="toRequest" />
      <button>request data</button>
    </form>-->
    <b-button @click="getResults">Request results</b-button>
    <p>{{ returnMessage }}</p>
    <!--<b-card>
      <div class="overflow-auto py-2">
        <h1>Previous results</h1>
        <b-pagination
          v-model="ex1CurrentPage"
          :total-rows="ex1Rows"
          :per-page="ex1PerPage"
          first-text="First"
          prev-text="Prev"
          next-text="Next"
          last-text="Last"
        ></b-pagination>
      </div>
    </b-card>-->
  </div>
</template>
