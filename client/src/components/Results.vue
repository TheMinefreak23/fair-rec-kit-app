<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
import { onMounted, ref, watch } from 'vue'
import Result from './Result.vue'
import VDismissButton from './VDismissButton.vue'
import PreviousResults from './PreviousResults.vue'
import { store, removeResult } from '../store'
import { status } from '../helpers/queueFormatter'
import { shortResultDescription } from '../helpers/resultFormatter'

const emit = defineEmits(['toast'])
const showResultModal = ref(false)
const currentTab = ref(0)

watch(
  () => store.currentExperiment.status,
  // New result added
  (newStatus, oldStatus) => {
    if (newStatus == status.done || newStatus == status.aborted) {
      emit('toast')
      store.currentExperiment.status = status.notAvailable
    }
  }
)

watch(
  () => store.currentResultTab,
  // New result added
  (newTab) => {
    currentTab.value = newTab
  }
)

//onMounted(() => (store.currentResults = [mockResult()]))

// Mockdata result
function mockResult() {
  const testcaption = 'Dataset: LFM-1b, Algorithm: ALS'

  // Add mockdata result to current results
  const mock = {
    caption: testcaption,
    results: mockdata.body,
    headers: mockdata.headers,
  }
  return {
    id: 0,
    metadata: {
      name: 'computation1',
      tags: ['tag1 ', 'tag2 ', 'tag3 ', 'tag4 '],
    },
    result: [mock, mock],
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
          <!--<div class="text-center">
            <h3 class="d-inline">Results</h3>
          </div>-->
          <h3 class="d-inline">Current results</h3>
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
          <template v-if="store.currentResults.length > 0">
            <b-tabs v-model="currentTab" card content-class="mt-3">
              <!-- Show opened results in tabs.-->
              <b-tab v-for="(result, index) in store.currentResults">
                <template #title
                  ><b-button
                    variant="light"
                    v-b-tooltip.hover
                    :title="shortResultDescription(result)"
                  >
                    <b-spinner
                      v-if="index == store.currentResults.length - 1"
                      type="grow"
                      variant="info"
                      small
                    ></b-spinner>
                    Result {{ result.metadata.name }}
                    <VDismissButton @click.stop="closeResult(index)" />
                  </b-button>
                </template>
                <Result :result="result" :key="result.id"
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
          :style="{ width: '60em', overflowY: 'scroll' }"
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
