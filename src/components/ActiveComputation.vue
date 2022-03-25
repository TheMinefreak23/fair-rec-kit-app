<script setup>
    /*This program has been developed by students from the bachelor Computer Science at
    Utrecht University within the Software Project course.
    © Copyright Utrecht University (Department of Information and Computing Sciences)*/
import Table from './Table.vue'
import { onMounted, ref } from 'vue'

const emit = defineEmits(['computing', 'done', 'stop'])
const props = defineProps({
  names: [String],
})

const computations = ref([])
const headers = ref([
  { name: 'Date Time' },
  { name: 'Name' },
  { name: 'Datasets' },
  { name: 'Approaches' },
  { name: 'Metrics' },
])


onMounted(() => {
  getComputations()
})


async function cancelComputation() {

  emit('stop')
}

async function getComputations(){
  const response = await fetch('http://localhost:5000/computation/queue')
  const data = await response.json()

  console.log(data)
  let allResults = data
  for (let i in allResults) {
    let approach = allResults[i].settings.approaches[0]
    let apprName = approach ? approach.name : 'NULL'
    let metric = allResults[i].settings.metrics[0]
    let metricName = metric ? metric.name : 'NULL'

    computations.value[i] = {
      datetime: allResults[i].timestamp.datetime,
      name: allResults[i].metadata.name,
      dataset: allResults[i].settings.datasets[0],
      approach: apprName,
      metric: metricName,
    }}
  if(data != [])
  {
      emit('computing')
      console.log(computations.value)
  }
  else
  {
      emit('done')
      alert('computations done!!!!')
  }
}

var done;

</script>

<template>
    <div>
      <Table :results="computations" :headers="headers" :buttonText="'Cancel'" :removable="true" />

      <b-button @click="$emit('computing')">Computing</b-button>
      <b-button @click="$emit('done')">Done</b-button>
    </div>
</template>