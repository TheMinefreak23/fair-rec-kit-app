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
