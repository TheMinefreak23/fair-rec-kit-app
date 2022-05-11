<script setup>
/*This program has been developed by students from the bachelor Computer Science at
    Utrecht University within the Software Project course.
    © Copyright Utrecht University (Department of Information and Computing Sciences)*/
import { API_URL } from '../api.js'
import Table from './Table.vue'
import { onMounted, ref, watch } from 'vue'
import { formatResults } from '../helpers/resultFormatter.js'
import { store } from '../store.js'

const emit = defineEmits(['computing', 'done', 'stop'])
const props = defineProps({
  names: [String],
  experiments: [],
})

//Declare the info about the experiments that will be shown to the user
const headers = ref([
  { name: 'ID' },
  { name: 'Date Time' },
  { name: 'Name' },
  { name: 'Datasets' },
  { name: 'Approaches' },
  { name: 'Metrics' },
  { name: '' },
])

//Retrieve the queue when the page is loaded
onMounted(() => {
  getQueue()
})

//Reload the queue when a new experiment is added
watch(
  () => store.queue,
  (data) => {
    console.log('queue watch new queue:', data)
    //console.log('queue watch old queue:', oldQueue)
    if (data.length != 0) {
      getQueue()
      emit('computing')
    } else {
      emit('done')
    }
  }
)

async function getQueue() {
  const response = await fetch(API_URL + '/experiment/queue')
  const data = await response.json()
  //store.queue = formatResults(data).map(x=>x.omit(x,'ID'))
  //store.queue = formatResults(data)
  store.queue = data.queue
}
</script>

<template>
  <b-card>
    <div class="text-center py-2 mx-5">
      <h3>Queue</h3>
      <Table
        :results="formatResults(store.queue)"
        :headers="headers"
        buttonText="Cancel"
        :removable="true"
        serverFile="/experiment/queue/delete"
      />
    </div>
  </b-card>
</template>
