<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
import { onMounted, ref, watch } from 'vue'
import FormGroupList from './FormGroupList.vue'
import { sendMockData } from '../test/mockComputation.js'
import { store } from '../store.js'
import { formatResult } from '../helpers/resultFormatter.js'
import { API_URL } from '../api'

const result = ref({})
const options = ref()
const form = ref({
  datasets: { main: [], inputs: [], selects: [] },
  metrics: { main: [], inputs: [], selects: [] },
  approaches: { main: [], inputs: [], selects: [] },
  filters: { main: [], inputs: [], selects: [] },
  splitMethod: 'random', //The default split method.
})
const metadata = ref({})

onMounted(async () => {
  await getOptions()
  initForm()
})

// GET request: Get available options for selection from server
async function getOptions() {
  const response = await fetch(API_URL + '/computation/options')
  const data = await response.json()
  options.value = data.options
  console.log(options.value)
}

// POST request: Send form to server.
async function sendToServer() {
  var sendForm = { ...form.value } // clone
  sendForm.approaches = reformat(form.value.approaches)
  sendForm.metrics = reformat(form.value.metrics)
  sendForm.datasets = reformat(form.value.datasets)
  sendForm.filters = reformat(form.value.filters)

  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ metadata: metadata.value, settings: sendForm }),
  }
  console.log(sendForm)
  const response = await fetch(
    API_URL + '/computation/calculation',
    requestOptions
  )

  // Update queue
  const data = response.json()
  //if (data.status == 'success') getComputations()
  store.queue = data
}

async function initForm() {
  //console.log(options.value)
  //console.log(options.value.defaults)
  form.value = {}
  metadata.value = {}
  form.value.datasets = emptyFormGroup()
  form.value.metrics = emptyFormGroup()
  form.value.approaches = emptyFormGroup()
  form.value.filters = emptyFormGroup()
  form.value.recommendations = options.value.defaults.recCount.default
  form.value.split = options.value.defaults.split
  form.value.splitMethod = 'random'
  //form.value.result.value = {}
}

function emptyFormGroup() {
  return { main: [], inputs: [], selects: [] }
}

// Change the form format (SoA) into a managable data format (AoS)
// TODO just don't use SoA in the first place
function reformat(property) {
  let choices = []
  for (let i in property.main) {
    let parameter = null
    if (property.inputs[i] != null) parameter = property.inputs[i]
    else if (property.selects[i] != null) parameter = property.selects[i]
    choices[i] = { name: property.main[i], parameter: parameter }
    //console.log('choices:' + choices)
  }
  return choices
}
</script>

<template>
  <div class="py-2 mx-5">
  <b-card>
    <!--This form contains all the necessary parameters for a user to submit a request for a computation-->
    <b-form v-if="options" @submit="sendToServer" @reset="initForm">
      <b-row>
        <b-col>
          <!--User can select a dataset.-->
          <FormGroupList
            v-model:data="form.datasets"
            name="Dataset"
            plural="Datasets"
            selectName="a dataset"
            :options="options.datasets"
            required
          />

          <!--User can select optional filters-->
          <FormGroupList
            v-model:data="form.filters"
            name="filter"
            plural="Filters"
            selectName="a filter"
            :options="options.filters"
          />

          <!--User provides an optional rating conversion-->
          <b-form-group label="Select a rating conversion">
            <!-- Select a rating conversion from the options received from the server -->
            <b-form-select
              v-model:data="form.conversion"
              :options="[{ text: 'None (default)', value: null }]"
            ></b-form-select>
          </b-form-group>
          </div>

          <FormGroupList
            v-model:data="form.approaches"
            nested="true"
            name="approach"
            plural="Recommender approaches"
            selectName="an approach"
            :options="options.approaches.libraries"
          />

          <!--User can select the amount of recommendations per user -->
          <b-form-group label="Select number of recommendations per user:">
            <b-form-input
              type="range"
              :min="options.defaults.recCount.min"
              :max="options.defaults.recCount.max"
              v-model="form.recommendations"
            ></b-form-input>
            <p>{{ form.recommendations }}</p>
            <!--  No longer feasible from a back-end perspective -Bug V22H-194
              <b-form-checkbox
              v-model="form.includeRatedItems"
              buttons
              button-variant="outline-primary"
              required
              >Include already rated items in recommendations</b-form-checkbox
            >-->
          </b-form-group>
        </b-col>
        <b-col class="p-0">
          <!--Input for train/test split-->
          <div class="p-2 my-2 mx-1 rounded-3 bg-secondary">
          <h3 class="text-center">Train/test-split</h3>
          <b-form-group label="Select test/train split:">
            <b-form-input
              type="range"
              min="0"
              max="100"
              step="5"
              id="customRange"
              v-model="form.split"
            ></b-form-input>
            <div class="text-center">
              <p class="d-inline px-5"><strong>Train: </strong><i>{{ form.split }}</i></p>
              <p class="d-inline px-5"><strong>Test: </strong><i>{{ 100 - form.split }}</i></p>
            </div>
          </b-form-group>

          <!--User can choose between a random and time-based train/testsplit-->
          <b-form-group>
            <b-form-radio-group v-model="form.splitMethod">
              <b-form-radio value="random">Random (default)</b-form-radio>
              <b-form-radio value="timesplit">Timesplit</b-form-radio>
            </b-form-radio-group>
          </b-form-group>
          </div>

          <!--Input for metrics, user can add infinite metrics -->
          <div class="p-2 my-2 mx-1 rounded-3 bg-secondary">
          <FormGroupList
            v-model:data="form.metrics"
            name="metric"
            plural="metrics"
            selectName="a metric"
            :options="options.metrics"
          />

          <!--Input for results filter -->
          <b-form-group label="Select a results filter">
            <b-form-select
              v-model="form.resFilter"
              :options="[{ text: 'Global (default)', value: null }]"
            ></b-form-select>
          </b-form-group>
          </div>

          <!-- Input for metadata such as:
     Computation Name
     Optional Tags
     Optional Email for notification -->
          <div class="p-2 m-1 rounded-3 bg-secondary">
          <h3 class="text-center">Meta</h3>
          <b-form-group label="Enter name for computation">
            <b-form-input
              placeholder="New Computation"
              v-model="metadata.name"
              required
            ></b-form-input>
          </b-form-group>
          <b-form-group label="Enter tags (optional)">
            <b-form-input v-model="metadata.tags"></b-form-input>
          </b-form-group>
          <b-form-group label="Enter e-mail (optional)">
            <b-form-input
              type="email"
              placeholder="example@mail.com"
              v-model="metadata.email"
            ></b-form-input>
          </b-form-group>
          </div>
        </b-col>
        <div class="d-flex justify-content-center">
            <b-button class="mx-1" type="reset" variant="danger">Reset</b-button>
            <b-button class="mx-1" type="submit" variant="primary">Send</b-button>
          </div>
      </b-row>
    </b-form>
    <b-button type="test" variant="warning" @click="sendMockData"
      >Mock</b-button
    >
  </b-card>
  </div>
</template>
