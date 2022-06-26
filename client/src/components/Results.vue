<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
import { ref, watch } from 'vue'
import Result from './Result.vue'
import VDismissButton from './VDismissButton.vue'
import PreviousResults from './PreviousResults.vue'
import { store, removeResult, APP_TABS } from '../store'
import { status } from '../helpers/queueFormatter'
import { shortResultDescription } from '../helpers/resultFormatter'

const emit = defineEmits(['toast'])
// const showResultModal = ref(false)
const currentTab = ref(0)
const blink = ref(-1)

/**
 * Show a toast and set the status when the experiment is finished
 */
watch(
  () => store.currentExperiment.status,
  // New result added
  (newStatus, oldStatus) => {
    if (newStatus === status.done || newStatus === status.aborted) {
      emit('toast')
      store.currentExperiment.status = status.notAvailable
      blink.value = store.currentResults.length
    }
  }
)

/**
 * Switch to the new result tab when it's updated (added)
 */
watch(
  () => store.currentResultTab,
  // New result added
  (newTab) => {
    currentTab.value = newTab
  }
)

/**
 * Apply a blink to a newly added result
 */
watch(
  () => store.currentTab,
  // This activates upon opening the results tab
  (index) => {
    if (index === APP_TABS.indexOf('Results')) {
      if (blink.value >= 0) {
        // Blink fades after 5 seconds
        const timeoutMs = 5000
        setTimeout(() => {
          blink.value = -1
        }, timeoutMs)
      }
    }
  }
)

/**
 * Close an inner result tab by index
 * @param {Int} index - the index of the tab within the result tabs
 */
function closeResult(index) {
  removeResult(index)
}
</script>

<template>
  <!--Show modal overlay when there is a new result-->
  <!--<b-modal
    id="result-modal"
    v-model="showResultModal"
    title="New result"
    ok-title="View new result"
    ok-variant="danger"
    cancel-title="Cancel"
    @ok="store.currentTab = 3"
  >
    <p>An experiment has finished.</p>
  </b-modal>-->
  <!--Result content-->
  <b-card>
    <div class="mx-5 mt-2">
      <div class="border-top-0 p-0">
        <!--Open previous results sidebar on button press-->
        <div class="p-3 m-0 container-fluid">
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
              <b-tab
                v-for="(result, index) in store.currentResults"
                :title-item-class="blink == index ? 'blink' : ''"
              >
                <template #title
                  ><b-button
                    variant="light"
                    v-b-tooltip.hover
                    :title="shortResultDescription(result)"
                  >
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
          :style="{ width: '60vw', overflowY: 'scroll' }"
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
