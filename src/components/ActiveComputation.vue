<script setup>
/*This program has been developed by students from the bachelor Computer Science at
    Utrecht University within the Software Project course.
    © Copyright Utrecht University (Department of Information and Computing Sciences)*/
import Table from './Table.vue'
import { onMounted, ref, watch } from 'vue'
import { formatResults } from '../helpers/resultFormatter.js'
import { store } from '../store.js'

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

watch(
  () => store.currentResult,
  (result) => {
    getComputations()
    console.log(result)
  }
)

async function cancelComputation() {
  emit('stop')
}

async function getComputations() {
  const response = await fetch('http://localhost:5000/computation/queue')
  const data = await response.json()

  console.log(data)
  computations.value = formatResults(data)
  if (data != []) {
    emit('computing')
    console.log(computations.value)
  } else {
    emit('done')
    alert('computations done!!!!')
  }
}

var done
</script>

<template>
  <div>
    <Table
      :results="computations"
      :headers="headers"
      :buttonText="'Cancel'"
      :removable="true"
      :serverFile="'/computation/queue/delete'"
    />
    <b-button @click="$emit('computing')">Computing</b-button>
    <b-button @click="$emit('done')">Done</b-button>
  </div>
</template>
