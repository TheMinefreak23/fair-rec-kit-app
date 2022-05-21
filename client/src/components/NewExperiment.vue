<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
import { onMounted, ref } from 'vue'
import FormGroupList from './FormGroupList.vue'
import { sendMockData } from '../test/mockExperimentOptions.js'
import { store, pollForResult } from '../store.js'
import { API_URL } from '../api'
import { emptyOption } from '../helpers/optionsFormatter'
import { emptyFormGroup, validateEmail } from '../helpers/optionsFormatter'
import { progress } from '../helpers/resultFormatter'

const horizontalLayout = ref(false)
const oldMetadata = ref(false)
const options = ref()

//Store the settings of the form in a reference
const form = ref({
  lists: initLists(),
})
const metadata = ref({})
const splitOptions = [
  { text: 'Random', value: 'random' },
  { text: 'Time', value: 'time' },
]
const experimentMethods = [
  { text: 'Recommendation (default)', value: 'recommendation' },
  { text: 'Prediction', value: 'prediction' },
]

onMounted(async () => {
  await getOptions()
  initForm()
})

// GET request: Get available options for selection from server
async function getOptions() {
  const response = await fetch(API_URL + '/experiment/options')
  const data = await response.json()
  options.value = data.options
  console.log('options', options.value)
}

// POST request: Send form to server.
async function sendToServer() {
  var sendForm = JSON.parse(JSON.stringify(form.value)) // clone

  sendForm.lists.approaches = reformat(sendForm.lists.approaches)
  sendForm.lists.metrics = reformat(sendForm.lists.metrics)
  sendForm.lists.datasets = reformat(sendForm.lists.datasets)
  console.log('sendForm', sendForm)

  // TODO get from server?
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
  const response = await fetch(
    API_URL + '/experiment/calculation',
    requestOptions
  )
  // Update queue
  const data = await response.json()
  store.queue = data.queue
  console.log('sendToServer() queue', store.queue)
  // Switch to queue
  store.currentTab = 1
  pollForResult()
}

//Declare default values of the form
function initForm() {
  form.value = { lists: initLists() }
  metadata.value = {}
  form.value.recommendations = options.value.defaults.recCount.default //The default amount of recommendations per user
  //form.value.split = options.value.defaults.split //The default train-test ratio
  //form.value.splitMethod = 'random' //The default method of splitting datasets
  form.value.experimentMethod = 'recommendation' //The default experiment type
}

// Initialise form group list settings
function initLists() {
  return {
    datasets: emptyFormGroup(true),
    metrics: emptyFormGroup(),
    approaches: emptyFormGroup(true),
  }
}

// Change the form format into a data format
function reformat(property) {
  let formattedChoices = []
  for (let i in property.choices) {
    const choices = property.choices[i]
    //console.log('reformat', choices)
    if (choices.main) {
      // Direct settings (inputs/selects)
      let params = []
      if (choices.inputs) params = params.concat(choices.inputs)
      if (choices.selects) params = params.concat(choices.selects)
      formattedChoices[i] = {
        name: choices.main.name,
        params: params,
      }
      // Nested formgrouplists
      if (choices.lists != null) {
        for (let list of choices.lists) {
          //console.log('list', list)
          if (list.choices[0].single) {
            // formgroup not list
            // TODO refactor
            formattedChoices[i][list.choices[0].name] = reformat(list)
          } else formattedChoices[i][list.name] = reformat(list)
          //console.log('list', formattedChoices[i][list.name])
        }
      }
    }
  }
  return formattedChoices
}
</script>

<template>
  <div class="py-2 mx-5">
    <b-row>
      <b-col md="auto">
        <b-form-checkbox v-model="horizontalLayout"
          >use broad layout</b-form-checkbox
        >
      </b-col>
      <b-col>
        <b-form-checkbox v-model="oldMetadata"
          >use old metadata layout</b-form-checkbox
        >
      </b-col>
    </b-row>
    <b-card>
      <b-row class="text-center"> <h3>New Experiment</h3></b-row>
      <!--This form contains all the necessary parameters for a user to submit a request for a experiment-->
      <b-form
        v-if="options"
        @submit="$event.preventDefault(), sendToServer()"
        @reset="$event.preventDefault(), initForm()"
      >
        <b-row class="text-center">
          <b-row>
            <b-col>
              <b-row>
                <b-col md="auto" class="text-center">
                  <p>Experiment type</p>
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
            <b-col
              md="auto"
              v-if="!oldMetadata"
              class="p-2 m-1 rounded-3 bg-secondary"
            >
              <!--<h3 class="text-center">Meta</h3>-->
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
                    <b-form-tags
                      v-model="metadata.tags"
                      tag-pills
                      tag-variant="dark"
                      remove-on-delete
                      separator=" ,;"
                      no-add-on-enter
                      size="lg"
                    ></b-form-tags> </b-form-group
                ></b-col>
              </b-row>
            </b-col>
          </b-row>

          <b-col class="g-0" :cols="horizontalLayout ? 12 : 6">
            <!--User can select a dataset.-->
            <div class="p-2 my-2 mx-1 rounded-3 bg-secondary">
              <FormGroupList
                v-model:data="form.lists.datasets"
                name="dataset"
                title="Datasets"
                :options="options.datasets"
                required
                :horizontalLayout="horizontalLayout"
                id="datasets"
              />
              <!--User provides an optional rating conversion-->
              <!-- Select a rating conversion from the options received from the server -->
              <!--
              <b-form-group label="Select a rating conversion">
                <b-form-select
                  v-model:data="form.conversion"
                  :options="[{ text: 'None (default)', value: null }]"
                >
                </b-form-select>
              </b-form-group>-->
            </div>
          </b-col>

          <b-col class="g-0" :cols="horizontalLayout ? 12 : 6">
            <!-- User can select any number of recommender approaches -->
            <div class="p-2 my-2 mx-1 rounded-3 bg-secondary">
              <FormGroupList
                v-model:data="form.lists.approaches"
                name="approach"
                :title="
                  (form.experimentMethod == 'recommendation'
                    ? 'Recommender'
                    : 'Predictor') + ' approaches'
                "
                :options="
                  form.experimentMethod == 'recommendation'
                    ? options.recommenders
                    : options.predictors
                "
                :required="true"
                :horizontalLayout="horizontalLayout"
              />

              <b-row>
                <b-row>
                  <b-col md="auto">
                    <!--User can select the amount of recommendations per user -->
                    <b-form-group
                      v-if="form.experimentMethod == 'recommendation'"
                      label="Select number of recommendations per user:"
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
                      >Include already rated items in
                      recommendations</b-form-checkbox
                    ></b-col
                  >
                </b-row>
              </b-row>
            </div>
          </b-col>
          <b-row>
            <b-col>
              <!--User can select any number of metrics -->
              <div class="p-2 my-2 mx-1 rounded-3 bg-secondary">
                <FormGroupList
                  v-model:data="form.lists.metrics"
                  name="metric"
                  title="metrics"
                  :maxK="form.recommendations"
                  :options="
                    form.experimentMethod == 'recommendation'
                      ? options.recMetrics
                      : options.predMetrics
                  "
                  :horizontalLayout="!oldMetadata"
                /></div
            ></b-col>
            <b-col v-if="oldMetadata">
              <!-- Input for metadata such as:
            experiment Name
            Tags (optional)
            Email for notification (optional) -->
              <div class="p-2 m-1 rounded-3 bg-secondary">
                <!--<h3 class="text-center">Meta</h3>-->
                <b-row>
                  <b-col>
                    <b-form-group label="Experiment name">
                      <b-form-input
                        placeholder="New experiment"
                        v-model="metadata.name"
                      ></b-form-input>
                    </b-form-group>
                  </b-col>
                  <b-col>
                    <b-form-group label="E-mail (optional)">
                      <b-form-input
                        type="email"
                        placeholder="example@mail.com"
                        v-model="metadata.email"
                      ></b-form-input>
                    </b-form-group>
                  </b-col>
                  <b-form-group label="Tags (optional)">
                    <b-form-input v-model="metadata.tags"></b-form-input>
                  </b-form-group>
                </b-row>
              </div>
            </b-col>
            <!-- Buttons to submit or reset an experiment-->
            <div class="d-flex justify-content-center">
              <b-button class="mx-1" size="lg" type="reset" variant="danger"
                >Reset</b-button
              >
              <b-button class="mx-1" size="lg" type="submit" variant="primary"
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
        @click="sendMockData(options, true)"
        >Simple Mock</b-button
      >
      <!--Simple version of the mock with metrics-->
      <b-button
        type="test"
        variant="primary"
        @click="sendMockData(options, true, true)"
        >Metric Mock</b-button
      >
    </b-card>
  </div>
</template>
