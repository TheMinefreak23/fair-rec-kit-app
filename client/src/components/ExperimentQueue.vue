<script setup>
/*This program has been developed by students from the bachelor Computer Science at
    Utrecht University within the Software Project course.
    © Copyright Utrecht University (Department of Information and Computing Sciences)*/
import { API_URL } from '../api.js'
import Table from './Table.vue'
import { onMounted, ref, watch } from 'vue'
import { formatResults, status } from '../helpers/resultFormatter.js'
import { store, getQueue, pollForResult } from '../store.js'

//const emit = defineEmits(['computing', 'done', 'stop'])
const props = defineProps({
  names: [String],
  experiments: [],
})

//Declare the info about the experiments that will be shown to the user
const headers = ref([
  { name: 'ID' },
  { name: 'Date Time' },
  { name: 'Name' },
  { name: 'Tags' },
  { name: 'Datasets' },
  { name: 'Approaches' },
  { name: 'Metrics' },
  { name: 'Status' }, // unique to the queue
  { name: '' },
])

//Retrieve the queue when the page is loaded
onMounted(() => {
  getQueue()
  if (
    store.currentExperiment &&
    store.currentExperiment.status == status.active
  ) {
    pollForResult()
  }
})

//Reload the queue when the experiment is done
watch(
  () => store.currentExperiment,
  (newStatus, oldStatus) => {
    console.log('queue watch experiment:', store.currentExperiment)
    if (newStatus == null) {
      getQueue()
    }
  }
)
</script>

<template>
  <b-card>
    <div class="text-center py-2 mx-5">
      <h3>Queue</h3>
      <h4>
        Current experiment:
        {{
          store.currentExperiment
            ? store.currentExperiment.metadata.name
            : 'None'
        }}
      </h4>
      <Table
        :results="formatResults(store.queue, true)"
        :headers="headers"
        buttonText="Cancel"
        :removable="true"
        serverFile="/experiment/queue/abort"
        :defaultSort="1"
      />
    </div>
  </b-card>
</template>
