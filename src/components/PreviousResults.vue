<script setup>
import Table from './Table.vue'
import { onMounted, ref } from 'vue'

const emit = defineEmits(['loadResult'])

const exResults = ref([
  { id: 1, age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
  { id: 2, age: 21, first_name: 'Larsen', last_name: 'Shaw' },
  { id: 3, age: 89, first_name: 'Geneva', last_name: 'Wilson' },
  { id: 4, age: 38, first_name: 'Jami', last_name: 'Carney' },
])
const exHeaders = ref(['id', 'age', 'first_name', 'last_name'])
const headers = ref([
  { name: 'ID' },
  { name: 'Date Time' },
  { name: 'Name' },
  { name: 'Datasets' },
  { name: 'Approaches' },
  { name: 'Metrics' },
  { name: ''},
])

const ex1CurrentPage = ref(1)
const ex1PerPage = ref(10)
const ex1Rows = ref(100)

const testMessage = ref('')
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
    const result = allResults[i]
    let approach = result.settings.approaches[0]
    let apprName = approach ? approach.name : 'NULL'
    let metric = result.settings.metrics[0]
    let metricName = metric ? metric.name : 'NULL'

    results.value[i] = {
      id: result.timestamp.stamp,
      datetime: result.timestamp.datetime,
      name: result.metadata.name,
      dataset: result.settings.datasets[0],
      approach: apprName,
      metric: metricName,
    }
  }
}

function edit(id, newName, newTags){
  if(newName != ''){
    testMessage.value = 'Result number ' + id + 's new name is ' + newName + '. '
  }else{
    testMessage.value = ''
  }
  if(newTags != ''){
    testMessage.value += 'Result number ' + id + 's new tags are ' + newTags + '.'
  }

}

function deleteResult(id){
  testMessage.value = 'delete result number ' + id + '!'
}
</script>

<template>
  <div>
    <Table
      @loadResult="(id) => $emit('loadResult', id)"
      @edit="(id, newName, newTags) => edit(id, newName, newTags)"
      @deleteResult="(id) => deleteResult(id)"
      :overview="true"
      :results="results"
      :headers="headers"
    />
    <!--<form @submit.prevent="getResults">
      <input v-model="toRequest" />
      <button>request data</button>
    </form>-->
    <b-button @click="getResults">Request results</b-button>
    <p>{{ testMessage }}</p>
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
