<script setup>
/*This program has been developed by students from the bachelor Computer Science at
    Utrecht University within the Software Project course.
    © Copyright Utrecht University (Department of Information and Computing Sciences)*/
import { API_URL } from '../api.js'
import Table from './Table.vue'
import { onMounted, ref, watch } from 'vue'
import { formatResults, status, progress } from '../helpers/resultFormatter.js'
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

const progressMax = 100
const previousNumber = ref(0)

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
    //console.log('queue watch experiment:', store.currentExperiment)
    if (newStatus == null) {
      getQueue()
    }
  }
)

// Return a progress number based on the progress status
function progressNumber(progressStatus) {
  // progress statuses in order
  // TODO refactor
  const progresses = [
    progress.started,
    progress.processingData,
    progress.splittingData,
    progress.model,
    progress.modelLoad,
    progress.training,
    progress.finished,
  ]
  const progressNumbers = {}
  for (let progressIndex in progresses) {
    //console.log(progresses[progressIndex])
    progressNumbers[progresses[progressIndex]] = Math.floor(
      (progressIndex / progresses.length) * progressMax
    )
  }
  //console.log('current exp', store.currentExperiment)
  //console.log('progressStatus', progressStatus)
  //console.log(progressNumbers[progressStatus])
  progressNumber = progressNumbers[progressStatus]
  if (progressNumber) {
    previousNumber.value = progressNumber
  }
  return previousNumber.value
}
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
        <!--{{ store.currentExperiment }}-->
      </h4>
      <b-progress :max="progressMax" height="2rem" show-progress animated>
        <b-progress-bar
          v-if="store.currentExperiment"
          :value="progressNumber(store.currentExperiment.progress)"
        >
          <span>
            Progress:
            {{ store.currentExperiment.progress }}
            <strong>
              {{ progressNumber(store.currentExperiment.progress) }}
            </strong>
          </span>
        </b-progress-bar>
      </b-progress>
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
