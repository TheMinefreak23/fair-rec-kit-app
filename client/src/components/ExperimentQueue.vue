<script setup>
/* This program has been developed by students from the bachelor Computer Science at
    Utrecht University within the Software Project course.
    © Copyright Utrecht University (Department of Information and Computing Sciences) */
import Table from './Table.vue'
import { onMounted, ref } from 'vue'
import { formatResults } from '../helpers/resultFormatter.js'
import { status } from '../helpers/queueFormatter.js'
import { store, getQueue, pollForResult } from '../store.js'
import { addResultById } from '../helpers/resultRequests.js'

/**
 * Declare the info about the experiments that will be shown to the user
 */
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

const progressMax = 100 // the maximal value of the progress bar

/**
 * Retrieve the queue when the page is loaded
 */
onMounted(() => {
  getQueue()
})
</script>

<template>
  <b-card>
    <div class="text-center py-2 mx-5">
      <h3>Queue</h3>
      <h4>
        Current experiment:
        {{
          store.currentExperiment.status != status.notAvailable
            ? store.currentExperiment.metadata.name
            : 'None'
        }}
      </h4>
      <!--Show the experiment progress.-->
      <template v-if="store.currentExperiment.status == status.active">
        <b-progress :max="progressMax" height="2rem" show-progress animated>
          <b-progress-bar :value="store.currentExperiment.progress.number">
            <span>
              Progress:
              {{ store.currentExperiment.progress.status }}
            </span>
          </b-progress-bar>
        </b-progress>
        <!--<p>{{ store.currentExperiment.progress.message }}</p>-->
      </template>
      <!--<p>{{ store.currentExperiment.progress }}</p>-->
      <!--Show the queue with this session's experiments.-->
      <Table
        @viewResult="addResultById"
        :results="formatResults(store.queue, true)"
        :headers="headers"
        buttonText="Cancel"
        overview
        removable
        :defaultSort="1"
        serverFile="/experiment/queue/abort"
        serverFile3="/all-results/result-by-id"
      />
    </div>
  </b-card>
</template>
