<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import Documentation from './components/Documentation.vue'
import Results from './components/Results.vue'
import PreviousResults from './components/PreviousResults.vue'
import ActiveComputation from './components/ActiveComputation.vue'
import NewComputation from './components/NewComputation.vue'
import TestForm from './test/TestForm.vue'
import { onMounted, ref } from 'vue'
import { API_URL } from './api'

const activeComputations = ref(false)
const done = ref(false)

// Ping
onMounted(async () => {
  console.log(API_URL)
  const response = await fetch(API_URL)
  const data = await response.json()
  console.log(data)
})
const tabIndex = ref(0)
</script>

<style scoped>
b-tab.success {
  color: yellow;
}
</style>

<template>
  <div class="bg-dark nav justify-content-center py-2">
    <img src="/RecCoonLogo.png" style="height: 50px" />
    <h1 class="text-white my-0 p-0">FairRecKit</h1>
    <div class="form-check form-switch justify-content-end">
      <label class="form-check-label" for="lightSwitch" style="color:white;">  
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-moon" viewBox="0 0 16 16">
        <path d="M6 .278a.768.768 0 0 1 .08.858 7.208 7.208 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277.527 0 1.04-.055 1.533-.16a.787.787 0 0 1 .81.316.733.733 0 0 1-.031.893A8.349 8.349 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.752.752 0 0 1 6 .278zM4.858 1.311A7.269 7.269 0 0 0 1.025 7.71c0 4.02 3.279 7.276 7.319 7.276a7.316 7.316 0 0 0 5.205-2.162c-.337.042-.68.063-1.029.063-4.61 0-8.343-3.714-8.343-8.29 0-1.167.242-2.278.681-3.286z"/>
        </svg>
      </label>
      <input class="form-check-input" type="checkbox" id="lightSwitch"/>
    </div>
  </div>
  <div class="nav-center">
    <b-tabs v-model="tabIndex" class="m-0 pt-2" align="center">
      <b-tab title="New Computation"> <NewComputation /></b-tab>
      <b-tab :class="{ success: done }">
        <ActiveComputation
          @computing="
            ;(activeComputations = true), (done = false), (tabIndex = 1)
          "
          @done=";(activeComputations = false), (done = true)"
          @stop=";(activeComputations = false), (done = false)"
        />
        <template v-slot:title :class="{ success: done }">
          <b-spinner v-if="activeComputations" small align="center"></b-spinner>
          <b-icon v-if="done" align="center" icon="check">√</b-icon>
          Active Computations
        </template>
      </b-tab>
      <b-tab title="Documentation"> <Documentation /></b-tab>
      <b-tab title="Results"> <Results /></b-tab>
      <b-tab title="All results"> <PreviousResults /></b-tab>
    </b-tabs>
  </div>
</template>
