<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */
import { onMounted, ref, watch } from 'vue'
import FormGroupList from './Form/FormGroupList.vue'
import { sendMockData } from '../test/mock/mockExperimentOptions.js'
import { store, pollForResult } from '../store.js'
import { API_URL } from '../api'
import {
  emptyFormGroup,
  validateEmail,
  reformat,
} from '../helpers/optionsFormatter'
import { progress } from '../helpers/queueFormatter'
import Tags from './Tags.vue'

import filterForm from '../test/mock/filterMock.json'
const options = ref()

// Store the settings of the form in a reference
const form = ref(initForm())
const metadata = ref({})
const experimentMethods = [
  { text: 'Recommendation (default)', value: 'recommendation' },
  { text: 'Prediction', value: 'prediction' },
]

onMounted(async () => {
  await setOptions()
  initSettings()
})

/**
 * Watch for change of global form settings, copy them
 */
watch(
  () => store.settings,
  (newSettings) => {
    console.log('newExperiment watch new settings:', newSettings)
    form.value = newSettings.form
    metadata.value = newSettings.metadata
    store.currentTab = 0
  }
)

/**
 * Update the options based on the chosen datasets
 */
watch(
  () => reformat(form.value.lists.datasets),
  (newDatasets) => {
    // console.log(newDatasets)
    setOptions(newDatasets)
  },
  {
    immediate: false,
  }
)

// POST request: Get available options for selection from server
async function setOptions(chosenDatasets = []) {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ datasets: chosenDatasets }),
  }
  const response = await fetch(API_URL + '/experiment/options', requestOptions)
  const data = await response.json()
  options.value = data.options
  // console.log('new options', options.value)
}

// POST request: Send form to server.
async function sendToServer() {
  const sendForm = JSON.parse(JSON.stringify(form.value)) // clone

  sendForm.rawSettings = JSON.parse(JSON.stringify(form.value)) // send raw settings for copying later TODO refactor
  // console.log('raw settings', sendForm.rawSettings)
  sendForm.lists.approaches = reformat(sendForm.lists.approaches)
  sendForm.lists.metrics = reformat(sendForm.lists.metrics)
  sendForm.lists.datasets = reformat(sendForm.lists.datasets)
  console.log('sendForm', sendForm)

  store.currentExperiment = {
    metadata: metadata.value,
    settings: sendForm,
    progress: progress.notAvailable,
  }
  // Post settings to server
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(store.currentExperiment),
  }
  const response = await fetch(API_URL + '/experiment/', requestOptions)
  // Update queue
  const data = await response.json()
  store.queue = data.queue
  console.log('sendToServer() queue', store.queue)
  // Switch to queue
  store.currentTab = 1
  pollForResult()
}

// Declare default values of the form
function initSettings() {
  form.value = initForm()
  metadata.value = {}
}

// Initialise form group list settings
function initForm() {
  return {
    lists: {
      datasets: emptyFormGroup(true),
      metrics: emptyFormGroup(),
      approaches: emptyFormGroup(true),
    },
    recommendations: options.value && options.value.defaults.recCount.default, // The default amount of recommendations per user
    experimentMethod: 'recommendation', // The default experiment type
    includeRatedItems: true,
  }
}
</script>

<template>
  <div class="py-2 mx-5">
    <b-card>
      <b-row class="text-center">
        <h3>New Experiment</h3>
      </b-row>
      <!--This form contains all the necessary parameters for a user to submit a request for a experiment-->
      <b-form
        v-if="options"
        @submit="$event.preventDefault(), sendToServer()"
        @keydown.enter.prevent
        @reset="$event.preventDefault(), initSettings()"
      >
        <b-row class="text-center">
          <b-row>
            <b-col>
              <b-row>
                <b-col md="auto" class="text-center">
                  <p>
                    Experiment type
                    <i
                      class="bi bi-info-circle"
                      v-b-tooltip.hover
                      title="Predictions are predicted ratings for known user-item pairs in the data , while recommendations are a list of recommended items for a user based on these predicted ratings."
                    >
                    </i>
                  </p>
                </b-col>
                <b-col md="auto">
                  <b-form-radio-group
                    v-model="form.experimentMethod"
                    :options="experimentMethods"
                  >
                  </b-form-radio-group>
                </b-col>
              </b-row>
            </b-col>
            <!-- Input for metadata such as:
            experiment Name
            Tags (optional)
            Email for notification (optional) -->
            <b-col md="auto" class="p-2 m-1 rounded-3 bg-secondary">
              <b-row>
                <b-col>
                  <b-form-group label-cols-md="4" label="Experiment name">
                    <b-form-input
                      placeholder="New experiment"
                      v-model="metadata.name"
                    ></b-form-input>
                  </b-form-group>
                </b-col>
                <b-col>
                  <b-form-group label-cols-md="4" label="E-mail (optional)">
                    <b-form-input
                      type="email"
                      placeholder="example@mail.com"
                      :state="
                        metadata.email
                          ? validateEmail(metadata.email) != null
                          : null
                      "
                      v-model="metadata.email"
                    ></b-form-input>
                  </b-form-group>
                </b-col>
                <b-col cols="12">
                  <b-form-group label-cols-md="2" label="Tags (optional)">
                    <Tags v-model="metadata.tags" />
                  </b-form-group>
                </b-col>
              </b-row>
            </b-col>
          </b-row>

          <b-col class="g-0" cols="6">
            <!--User can select a dataset.-->
            <div class="p-2 my-2 mx-1 rounded-3 bg-secondary">
              <FormGroupList
                v-model="form.lists.datasets"
                name="dataset"
                title="datasets"
                :options="options.datasets"
                required
              />
            </div>
          </b-col>

          <b-col class="g-0" cols="6">
            <!-- User can select any number of recommender approaches -->
            <div class="p-2 my-2 mx-1 rounded-3 bg-secondary">
              <FormGroupList
                v-model="form.lists.approaches"
                name="approach"
                :title="
                  (form.experimentMethod == 'recommendation'
                    ? 'recommender'
                    : 'predictor') + ' approaches'
                "
                :options="
                  form.experimentMethod == 'recommendation'
                    ? options.recommenders
                    : options.predictors
                "
                :required="true"
              />

              <b-row>
                <b-row v-if="form.experimentMethod == 'recommendation'">
                  <b-col md="auto">
                    <!--User can select the amount of recommendations per user -->
                    <b-form-group
                      label="Select number of recommendations per user: *"
                    >
                      <b-form-input
                        type="range"
                        :min="options.defaults.recCount.min"
                        :max="options.defaults.recCount.max"
                        v-model="form.recommendations"
                      />
                    </b-form-group>
                  </b-col>
                  <b-col md="auto">
                    <b-form-input md="auto" v-model="form.recommendations"
                      >{{ form.recommendations }}
                    </b-form-input>
                  </b-col>
                  <b-col md="auto">
                    <b-form-checkbox
                      v-model="form.includeRatedItems"
                      buttons
                      button-variant="outline-primary"
                      required
                    >
                      Include already rated items in
                      recommendations</b-form-checkbox
                    >
                  </b-col>
                </b-row>
              </b-row>
            </div>
          </b-col>
          <b-row>
            <b-col>
              <!--User can select any number of metrics -->
              <div class="p-2 my-2 mx-1 rounded-3 bg-secondary">
                <FormGroupList
                  v-model="form.lists.metrics"
                  name="metric"
                  title="metrics"
                  :maxK="form.recommendations"
                  :datasets="reformat(form.lists.datasets)"
                  :options="
                    form.experimentMethod == 'recommendation'
                      ? options.recMetrics
                      : options.predMetrics
                  "
                />
              </div>
            </b-col>
            <!-- Buttons to submit or reset an experiment-->
            <div class="d-flex justify-content-center">
              <b-button class="mx-1" type="reset" variant="danger"
                >Reset</b-button
              >
              <b-button class="mx-1" type="submit" variant="primary"
                >Send</b-button
              >
            </div>
          </b-row>
        </b-row>
      </b-form>
      <!--Send a plethora of mock data to the queue-->
      <b-button type="test" variant="warning" @click="sendMockData(options)"
        >Mock</b-button
      >
      <!--Simple version of the mock-->
      <b-button
        type="test"
        variant="primary"
        @click="sendMockData(options, true, false)"
        >Simple Mock</b-button
      >
      <!--Simple version of the mock with metrics-->
      <b-button
        type="test"
        variant="primary"
        @click="sendMockData(options, true, true)"
        >Metric Mock</b-button
      >
      <!--Fill the form with mock filter options-->
      <b-button type="test" variant="primary" @click="form = filterForm"
        >Filter Mock</b-button
      >
    </b-card>
  </div>
</template>
