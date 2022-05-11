<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
import { ref, watch } from 'vue'
import { API_URL } from '../api'
import Result from './Result.vue'
import VDismissButton from './VDismissButton.vue'
import PreviousResults from './PreviousResults.vue'
import { store, addResult, removeResult } from '../store'
import { formatResult } from '../helpers/resultFormatter'

const emit = defineEmits(['goToResult', 'toast'])
const showResultModal = ref(false)
const currentTab = ref(0)
const fetchResult = ref(false)

// Request latest calculation when the queue is updated
watch(
  () => store.queue,
  (newQueue, oldQueue) => {
    // Only request if the queue length has decreased
    // (An experiment has finished)
    if (newQueue.length < oldQueue.length) {
      // Long polling: Try to get the finished result every interval
      const interval = 1000 // Every second
      fetchResult.value = true
      setInterval(() => getCalculation(), interval)
      currentTab.value = 0
    }
  }
)

/**
 * GET request: Ask server for latest calculation
 */
async function getCalculation() {
  if (fetchResult.value) {
    console.log('fetching result')
    try {
      const response = await fetch(API_URL + '/experiment/calculation')
      const data = await response.json()

      if (data.status == 'done') {
        console.log('done', data)
        addResult(formatResult(data.calculation))
        emit('toast')
        fetchResult.value = false
        store.experimentRunning = false
        store.currentExperiment = null
      } else if (data.status == 'busy') {
        console.log('busy', data)
        store.experimentRunning = true
      }
    } catch (e) {
      console.log(e) // TODO better error handling, composable
      fetchResult.value = false
    }
  }
}

/**
 * Close an inner result tab by index
 * @param {Int} index - the index of the tab within the result tabs
 */
function closeResult(index) {
  console.log(index)
  removeResult(index)
}
</script>

<template>
  <!--Show modal overlay when there is a new result-->
  <b-modal
    id="result-modal"
    v-model="showResultModal"
    title="New result"
    ok-title="View new result"
    ok-variant="danger"
    cancel-title="Cancel"
    @ok="
      store.currentTab = 3 //$emit('goToResult')
    "
  >
    <p>An experiment has finished.</p>
  </b-modal>
  <!--Result content-->
  <b-card>
    <div class="mx-5 mt-2">
      <div class="border-top-0 p-0">
        <!--Open previous results sidebar on button press-->
        <div class="p-3 m-0 container-fluid">
          <h3 class="d-inline">Results</h3>
          <button
            class="d-inline btn btn-primary float-end"
            type="button"
            data-bs-toggle="offcanvas"
            data-bs-target="#offcanvasRight"
            aria-controls="offcanvasRight"
          >
            Previous Results
          </button>
        </div>
        <div class="border">
          <template v-if="[...store.currentResults].length > 0">
            <b-tabs v-model="currentTab" card content-class="mt-3">
              <!-- Show opened results in tabs.-->
              <b-tab
                v-for="(result, index) in [...store.currentResults]"
                :key="result.id"
              >
                <template #title>
                  Result {{ result.metadata.name }}
                  <VDismissButton @click.stop="closeResult(index)" />
                </template>
                <Result :result="result"
              /></b-tab>
            </b-tabs>
          </template>
          <!--Show message when there are no results.-->
          <p v-else>
            No results to show, start a new experiment or choose a previous
            experiment
          </p>
        </div>

        <!--Toggled results sidebar (offcanvas)-->
        <div
          class="offcanvas offcanvas-end"
          tabindex="-1"
          id="offcanvasRight"
          aria-labelledby="offcanvasRightLabel"
        >
          <PreviousResults />
        </div>
      </div>
    </div>
  </b-card>
</template>
