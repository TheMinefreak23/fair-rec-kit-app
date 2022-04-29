<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
import { onMounted, ref, watch } from 'vue'
import FormGroupList from './FormGroupList.vue'
import { sendMockData } from '../test/mockComputationOptions.js'
import { store } from '../store.js'
import { API_URL } from '../api'

const result = ref({})
const options = ref()
const form = ref({
  datasets: emptyFormGroup(),
  metrics: emptyFormGroup(),
  approaches: emptyFormGroup(),
  //filters: emptyFormGroup(),
  splitMethod: 'random', //The default split method.
  computationMethod: 'recommendation',
})
const metadata = ref({})
const splitOptions = [
  { text: 'Random', value: 'random' },
  { text: 'Time', value: 'time' },
]

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

  sendForm.approaches = reformat(sendForm.approaches)
  sendForm.metrics = reformat(sendForm.metrics)
  console.log(form.value.metrics, sendForm.metrics)
  sendForm.datasets = reformat(sendForm.datasets)

  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ metadata: metadata.value, settings: sendForm }),
  }
  console.log('sendForm', sendForm)
  const response = await fetch(
    API_URL + '/computation/calculation',
    requestOptions
  )

  // Update queue
  const data = response.json()
  //console.log('calculation route response:', data)
  store.queue = data
  //console.log('queue:', store.queue)
}

async function initForm() {
  //console.log(options.value)
  //console.log(options.value.defaults)
  form.value = {}
  metadata.value = {}
  form.value.datasets = emptyFormGroup()
  form.value.metrics = emptyFormGroup()
  form.value.approaches = emptyFormGroup()
  //form.value.filters = emptyFormGroup()
  form.value.recommendations = options.value.defaults.recCount.default
  form.value.split = options.value.defaults.split
  form.value.splitMethod = 'random'
  form.value.computationMethod = 'recommendation'
  //form.value.result.value = {}
}

function emptyFormGroup() {
  return { main: [], inputs: [], selects: [], lists: [] }
}

// Change the form format (SoA) into a managable data format (AoS)
// TODO just don't use SoA in the first place
function reformat(property) {
  let choices = []
  for (let i in property.main) {
    let params = null
    console.log(
      'reformat',
      property.main[i],
      property.inputs[i],
      property.selects[i]
    )

    if (property.inputs[i] != null) params = property.inputs[i]
    else if (property.selects[i] != null) params = property.selects[i]
    choices[i] = { name: property.main[i].name, params: params }

    if (property.lists[i] != null) {
      choices[i].settings = property.lists[i].map((setting) => ({
        [setting.name]: reformat(setting),
      }))
    }
    //console.log('choices:' + choices)
    //console.log(choices[i])
  }

  return choices
}
</script>

<template>
  <div class="py-2 mx-5 bg-primary">
    <b-card class="block">
      <!--This form contains all the necessary parameters for a user to submit a request for a computation-->
      <b-form v-if="options" @submit="sendToServer" @reset="initForm">
        <b-row>
          <b-col class="g-0">
            <div class="p-2 my-2 mx-1 rounded-3 bg-secondary">
              <h3>Computation type</h3>
              <b-form-radio-group v-model="form.computationMethod">
                <b-form-radio value="recommendation"
                  >Recommendation (default)</b-form-radio
                >
                <b-form-radio value="prediction">Prediction</b-form-radio>
              </b-form-radio-group>
              <!--User can select a dataset.-->
              <FormGroupList
                v-model:data="form.datasets"
                name="dataset"
                plural="Datasets"
                selectName="a dataset"
                :options="options.datasets"
                required
              />

              <!--User can select optional filters-->
              <!--<FormGroupList
                v-model:data="form.filters"
                name="filter"
                plural="Filters"
                selectName="a filter"
                :options="options.filters"
              />-->

              <!--User provides an optional rating conversion-->
              <b-form-group label="Select a rating conversion">
                <!-- Select a rating conversion from the options received from the server -->
                <b-form-select
                  v-model:data="form.conversion"
                  :options="[{ text: 'None (default)', value: null }]"
                ></b-form-select>
              </b-form-group>
            </div>

            <div class="p-2 my-2 mx-1 rounded-3 bg-secondary">
              <FormGroupList
                v-model:data="form.approaches"
                name="approach"
                plural="Recommender approaches"
                selectName="an approach"
                :options="
                  form.computationMethod == 'recommendation'
                    ? options.recommenders
                    : options.predictors
                "
                :required="true"
              />

              <!--User can select the amount of recommendations per user -->
              <b-form-group
                v-if="form.computationMethod == 'recommendation'"
                label="Select number of recommendations per user:"
              >
                <b-form-input
                  type="range"
                  :min="options.defaults.recCount.min"
                  :max="options.defaults.recCount.max"
                  v-model="form.recommendations"
                />
                <p>{{ form.recommendations }}</p>
                <b-form-checkbox
                  v-model="form.includeRatedItems"
                  buttons
                  button-variant="outline-primary"
                  required
                  >Include already rated items in
                  recommendations</b-form-checkbox
                >
              </b-form-group>
            </div>
          </b-col>

          <b-col class="p-0">
            <!--Input for metrics, user can add infinite metrics -->
            <div class="p-2 my-2 mx-1 rounded-3 bg-secondary">
              <FormGroupList
                v-model:data="form.metrics"
                name="metric"
                plural="metrics"
                selectName="a metric"
                :options="
                  form.computationMethod == 'recommendation'
                    ? options.metrics
                    : options.metrics.slice(1)
                "
              />
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
            <b-button class="mx-1" type="reset" variant="danger"
              >Reset</b-button
            >
            <b-button class="mx-1" type="submit" variant="primary"
              >Send</b-button
            >
          </div>
        </b-row>
      </b-form>
      <b-button type="test" variant="warning" @click="sendMockData"
        >Mock</b-button
      >
    </b-card>
  </div>
</template>
