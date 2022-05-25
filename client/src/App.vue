<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import Documentation from './components/Documentation.vue'
import Results from './components/Results.vue'
import PreviousResults from './components/PreviousResults.vue'
import ExperimentQueue from './components/ExperimentQueue.vue'
import NewExperiment from './components/NewExperiment.vue'
import TestForm from './test/TestForm.vue'
import { onMounted, ref } from 'vue'
import { API_URL } from './api'
import MusicDetail from './components/MusicDetail.vue'
import { useToast } from 'bootstrap-vue-3'
import { store } from './store'
import VCheckmark from './components/VCheckmark.vue'
let toast = useToast()

/*
const activeExperiments = ref(false)
const done = ref(false)*/

// Ping
onMounted(async () => {
  //console.log(API_URL)
  const response = await fetch(API_URL)
  const data = await response.json()
  console.log(data)
})
//const tabIndex = ref(0)

// Make result tab the active tab
function goToResult() {
  store.currentTab = 3
}

function callToast() {
  toast.show(
    { title: 'An experiment has finished! View here' },
    {
      pos: 'top-right',
      delay: 800,
      href: 'https://cdmoro.github.io/bootstrap-vue-3/components/Toast.html#variants',
    }
  )
}
</script>

<template>
  <b-container
    :toast="{ root: true }"
    fluid="sm"
    position="position-fixed"
    @click="goToResult()"
  >
  </b-container>
  <div class="d-flex flex-column min-vh-100">
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css"
      rel="stylesheet"
    />
    <!--<TestForm :useTestOptions="true" />-->
    
  <div class="bg-dark">
    <div class=" wrap bg-dark nav justify-content-center py-2 " >
      <img src="/RecCoonLogo.png" style="height: 50px;" class="ms-auto" />
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
    
  </div>
    <div class="nav-center">
      <b-tabs
        v-model="store.currentTab"
        class="m-0 pt-2"
        align="center"
        nav-class="tab-active"
      >
        <b-tab title="New Experiment" title-item-class="tab-title-class"
          ><NewExperiment
        /></b-tab>
        <b-tab title-item-class="tab-title-class">
          <!--<ActiveExperiments
          @computing="
            ;(activeExperiments = true), (done = false), (tabIndex = 1)
          "
          @done=";(activeExperiments = false), (done = true)"
          @stop=";(activeExperiments = false), (done = false)"
        />-->
          <ExperimentQueue />
          <template v-slot:title>
            <div
              :style="{
                color: store.currentExperiment ? 'red' : 'black',
                backgroundColor: store.currentExperiment ? 'yellow' : 'white',
              }"
            >
              <b-spinner v-if="store.currentExperiment" small></b-spinner>
              <VCheckmark v-else />
              Experiment Queue
            </div>
          </template>
        </b-tab>
        <b-tab title="Documentation" data-testid="DocTab">
          <Documentation
        /></b-tab>
        <b-tab title="Results">
          <Results @goToResult="goToResult" @toast="callToast"
        /></b-tab>
        <b-tab title="All results">
          <PreviousResults @goToResult="goToResult" />
        </b-tab>
        <b-tab title="Music Detail">
          <MusicDetail />
        </b-tab>
      </b-tabs>
    </div>
    <!-- Footer -->
    <div class="bg-dark py-1 mt-auto">
      <p class="text-white my-0 mt-2 pb-2 text-center">
        &copy; Utrecht University (ICS).
      </p>
      <div class="container text-center text-white py-2">
        <!-- Github -->
        <a
          href="https://github.com/TheMinefreak23/fair-rec-kit-app"
          target="_blank"
          class="btn btn-outline-light btn-floating m-1 mx-3 rounded-pill border-2 p-0"
          role="button"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            fill="currentColor"
            class="bi bi-github m-2"
            viewBox="0 0 16 16"
          >
            <path
              d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"
            />
          </svg>
        </a>
        <!-- Email -->
        <a
          href="mailto:FairRecKit@hotmail.com"
          target="_blank"
          class="btn btn-outline-light btn-floating m-1 mx-3 rounded-pill border-2 p-0"
          role="button"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            fill="currentColor"
            class="bi bi-envelope-fill m-2"
            viewBox="0 0 16 16"
          >
            <path
              d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414.05 3.555ZM0 4.697v7.104l5.803-3.558L0 4.697ZM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586l-1.239-.757Zm3.436-.586L16 11.801V4.697l-5.803 3.546Z"
            />
          </svg>
        </a>
        <!-- Spotify -->
        <a
          href="#"
          target="_blank"
          class="btn btn-outline-light btn-floating m-1 mx-3 rounded-pill border-2 p-0"
          role="button"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            fill="currentColor"
            class="bi bi-spotify m-2"
            viewBox="0 0 16 16"
          >
            <path
              d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0zm3.669 11.538a.498.498 0 0 1-.686.165c-1.879-1.147-4.243-1.407-7.028-.77a.499.499 0 0 1-.222-.973c3.048-.696 5.662-.397 7.77.892a.5.5 0 0 1 .166.686zm.979-2.178a.624.624 0 0 1-.858.205c-2.15-1.321-5.428-1.704-7.972-.932a.625.625 0 0 1-.362-1.194c2.905-.881 6.517-.454 8.986 1.063a.624.624 0 0 1 .206.858zm.084-2.268C10.154 5.56 5.9 5.419 3.438 6.166a.748.748 0 1 1-.434-1.432c2.825-.857 7.523-.692 10.492 1.07a.747.747 0 1 1-.764 1.288z"
            />
          </svg>
        </a>
        <!-- License -->
        <a
          href="#"
          target="_blank"
          class="btn btn-outline-light btn-floating m-1 mx-3 rounded-pill border-2 p-0"
          role="button"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            fill="currentColor"
            class="bi bi-bookmark-check-fill m-2"
            viewBox="0 0 16 16"
          >
            <path
              fill-rule="evenodd"
              d="M2 15.5V2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.74.439L8 13.069l-5.26 2.87A.5.5 0 0 1 2 15.5zm8.854-9.646a.5.5 0 0 0-.708-.708L7.5 7.793 6.354 6.646a.5.5 0 1 0-.708.708l1.5 1.5a.5.5 0 0 0 .708 0l3-3z"
            />
          </svg>
        </a>
        <!-- Youtube/Trailer -->
        <a
          href="#"
          target="_blank"
          class="btn btn-outline-light btn-floating m-1 mx-3 rounded-pill border-2 p-0"
          role="button"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            fill="currentColor"
            class="bi bi-youtube m-2"
            viewBox="0 0 16 16"
          >
            <path
              d="M8.051 1.999h.089c.822.003 4.987.033 6.11.335a2.01 2.01 0 0 1 1.415 1.42c.101.38.172.883.22 1.402l.01.104.022.26.008.104c.065.914.073 1.77.074 1.957v.075c-.001.194-.01 1.108-.082 2.06l-.008.105-.009.104c-.05.572-.124 1.14-.235 1.558a2.007 2.007 0 0 1-1.415 1.42c-1.16.312-5.569.334-6.18.335h-.142c-.309 0-1.587-.006-2.927-.052l-.17-.006-.087-.004-.171-.007-.171-.007c-1.11-.049-2.167-.128-2.654-.26a2.007 2.007 0 0 1-1.415-1.419c-.111-.417-.185-.986-.235-1.558L.09 9.82l-.008-.104A31.4 31.4 0 0 1 0 7.68v-.123c.002-.215.01-.958.064-1.778l.007-.103.003-.052.008-.104.022-.26.01-.104c.048-.519.119-1.023.22-1.402a2.007 2.007 0 0 1 1.415-1.42c.487-.13 1.544-.21 2.654-.26l.17-.007.172-.006.086-.003.171-.007A99.788 99.788 0 0 1 7.858 2h.193zM6.4 5.209v4.818l4.157-2.408L6.4 5.209z"
            />
          </svg>
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* NOT WORKING
b-tab {
  background-color: yellow;
}*/
.tab-title-class {
  font-size: 300;
  background-color: green;
  color: #ff0000 !important;
}
.tab-active {
  background-color: #ff0000;
  color: green;
}

.bg {
  background-color: blue;
}


.wrap {
  opacity: 0.5;
  background-image: url("public/background.png");
  background-repeat: repeat;
  background-size: 30%;
}
</style>
