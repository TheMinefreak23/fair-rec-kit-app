<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
import Result from './Result.vue'
import VDismissButton from './VDismissButton.vue'
import PreviousResults from './PreviousResults.vue'
import { onMounted, ref, watch } from 'vue'
import { store, addResult, removeResult } from '../store'
import { formatResult } from '../helpers/resultFormatter'
import { API_URL } from '../api'

const emit = defineEmits(['goToResult'])
const showResultModal = ref(false)

watch(
  () => store.queue,
  (newQueue, oldQueue) => {
    if (newQueue.length < oldQueue.length) getCalculation()
  }
)

// GET request: Ask server for latest calculation
async function getCalculation() {
  const response = await fetch(API_URL + '/computation/calculation')
  const data = await response.json()
  console.log(data)
  //if (Object.keys(data).length === 0) // not null check
  //store.currentResult = data.calculation
  addResult(formatResult(data.calculation))
  showResultModal.value = true
}

function closeResult(id) {
  console.log(id)
  removeResult(id)
}
</script>

<template>
  <!--Shows when there is a new result-->
  <b-modal
    id="result-modal"
    v-model="showResultModal"
    title="New result"
    ok-title="View new result"
    ok-variant="danger"
    cancel-title="Cancel"
    @ok="$emit('goToResult')"
  >
    <p>An experiment has finished.</p>
  </b-modal>
  <b-card>
    <div class="mx-5 mt-2">
      <div class="border-top-0 p-0">
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
            <b-tabs card content-class="mt-3">
              <!-- Result tabs.-->
              <!--Always show JSON Mockdata result tab.-->
              <b-tab
                v-for="(result, index) in [...store.currentResults]"
                :key="result.id"
              >
                <template #title>
                  Result {{ result.name }}
                  <VDismissButton @click.stop="closeResult(index)" />
                </template>
                <Result :result="result"
              /></b-tab>
            </b-tabs>
          </template>
          <p v-else>
            No results to show, start a new experiment or choose a previous
            experiment
          </p>
        </div>

        <div
          class="offcanvas offcanvas-end"
          tabindex="-1"
          id="offcanvasRight"
          aria-labelledby="offcanvasRightLabel"
        >
          <PreviousResults @goToResult="" />
        </div>
      </div>

      <!--<div class="col-md-4 border-top-0 p-0">
      <h3 class="text-center py-2 m-0 border-bottom">Previous Results</h3>
      <PreviousResults />
    </div>-->
    </div>
  </b-card>
</template>
