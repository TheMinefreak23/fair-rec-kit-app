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

const results = ref([
  { id: 1, age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
  { id: 2, age: 21, first_name: 'Larsen', last_name: 'Shaw' },
  { id: 3, age: 89, first_name: 'Geneva', last_name: 'Wilson' },
  { id: 4, age: 38, first_name: 'Jami', last_name: 'Carney' },
])
const headers = ref([
  { name: 'Date Time' },
  { name: 'Name' },
  { name: 'Datasets' },
  { name: 'Approaches' },
  { name: 'Metrics' },
])

const computations = ref([])

onMounted(() => {
  //getResults()
})


async function cancelComputation() {

  emit('stop')
}

async function getComputations(){
  const response = await fetch('http://localhost:5000/queue')
  const data = await response.json()
  if(/* computing */ true)
  {
      emit('computing')
  }
  if(/* all computations done */ false)
  {
      emit('done')
      alert('computations done!!!!')
  }
}

var done;

</script>

<template>
    <div>
      <h1>Waiting for "{{name}}" to be finished...</h1>
      <b-spinner></b-spinner> 
      <b-button v-b-modal.popup variant="danger">Cancel</b-button>
    </div>
    <div>
      <Table :results="results" :headers="headers" :buttonText="'Cancel'" />

      <b-button @click="$emit('computing')">Computing</b-button>
      <b-button @click="$emit('done')">Done</b-button>
    </div>
</template>