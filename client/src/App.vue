<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import Documentation from './components/Documentation.vue'
import Results from './components/Results.vue'
import PreviousResults from './components/PreviousResults.vue'
import ActiveComputation from './components/ActiveComputation.vue'
import NewExperiment from './components/NewExperiment.vue'
import TestForm from './test/TestForm.vue'
import { onMounted, ref } from 'vue'
import { API_URL } from './api'
import MusicDetail from './components/MusicDetail.vue'

const activeComputations = ref(false)
const done = ref(false)

// Ping
onMounted(async () => {
  //console.log(API_URL)
  const response = await fetch(API_URL)
  const data = await response.json()
  console.log(data)
})
const tabIndex = ref(0)

// Make result tab the active tab
function goToResult() {
  tabIndex.value = 3
}
</script>

<template>
  <!--<TestForm :useTestOptions="true" />-->
  <div class="bg-dark nav justify-content-center py-2">
    <img src="/RecCoonLogo.png" style="height: 50px" class="ms-auto" />
    <h1 class="text-white my-0 p-0">FairRecKit</h1>

    <div class="dropdown my-auto ms-auto me-3">
      <button
        class="btn btn-secondary dropdown-toggle"
        type="button"
        id="dropdownMenuButton1"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          fill="currentColor"
          class="bi bi-gear-fill"
          viewBox="0 0 16 16"
        >
          <path
            d="M9.405 1.05c-.413-1.4-2.397-1.4-2.81 0l-.1.34a1.464 1.464 0 0 1-2.105.872l-.31-.17c-1.283-.698-2.686.705-1.987 1.987l.169.311c.446.82.023 1.841-.872 2.105l-.34.1c-1.4.413-1.4 2.397 0 2.81l.34.1a1.464 1.464 0 0 1 .872 2.105l-.17.31c-.698 1.283.705 2.686 1.987 1.987l.311-.169a1.464 1.464 0 0 1 2.105.872l.1.34c.413 1.4 2.397 1.4 2.81 0l.1-.34a1.464 1.464 0 0 1 2.105-.872l.31.17c1.283.698 2.686-.705 1.987-1.987l-.169-.311a1.464 1.464 0 0 1 .872-2.105l.34-.1c1.4-.413 1.4-2.397 0-2.81l-.34-.1a1.464 1.464 0 0 1-.872-2.105l.17-.31c.698-1.283-.705-2.686-1.987-1.987l-.311.169a1.464 1.464 0 0 1-2.105-.872l-.1-.34zM8 10.93a2.929 2.929 0 1 1 0-5.86 2.929 2.929 0 0 1 0 5.858z"
          />
        </svg>
      </button>
      <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
        <li>
          <div class="form-check form-switch px-2">
            <p class="d-inline ps-2">Dark Mode</p>
            <input
              class="form-check-input mx-auto"
              type="checkbox"
              id="changeTheme"
            />
          </div>
        </li>
      </ul>
    </div>
  </div>
  <div class="nav-center">
    <b-tabs v-model="tabIndex" class="m-0 pt-2" align="center">
      <b-tab title="New Experiment"><NewExperiment /></b-tab>
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
      <b-tab title="Documentation" data-testid="DocTab">
        <Documentation
      /></b-tab>
      <b-tab title="Results"> <Results @goToResult="goToResult" /></b-tab>
      <b-tab title="All results">
        <PreviousResults @goToResult="goToResult" />
      </b-tab>
      <b-tab title="Music Detail"> <MusicDetail /></b-tab>
    </b-tabs>
  </div>
</template>

<style scoped>
b-tab.success {
  color: yellow;
}
</style>
