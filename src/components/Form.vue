<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
import { onMounted, ref } from 'vue'
import FormGroupList from './FormGroupList.vue'

const result = ref({})
const options = ref()
const form = ref({
  datasets: [],
  splitMethod: 'random', //The default split method.
})
const metadata = ref({})

onMounted(async () => {
  await getOptions()
  initForm()
})

// GET request: Get available options for selection from server
async function getOptions() {
  const response = await fetch('http://localhost:5000/computation/options')
  const data = await response.json()
  options.value = data.options
  console.log(options.value)
}

// POST request: Send form to server.
function sendToServer() {
  form.value.approaches = reformat(form.value.approaches)
  form.value.metrics = reformat(form.value.metrics)
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ metadata: metadata.value, settings: form.value }),
  }
  console.log(form.value)
  fetch('http://localhost:5000/computation/calculation', requestOptions).then(
    () => {
      getCalculation()
    }
  )
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
    console.log('choices:' + choices.value)
  }
  return choices
}

// GET request: Ask server for latest calculation
async function getCalculation() {
  const response = await fetch('http://localhost:5000/computation/calculation')
  const data = await response.json()
  result.value = data.calculation
  console.log(result.value)
}

async function initForm() {
  //console.log(options.value)
  //console.log(options.value.defaults)
  form.value = {}
  metadata.value = {}
  form.value.datasets = []
  form.value.recommendations = options.value.defaults.recCount.default
  form.value.split = options.value.defaults.split
  form.value.splitMethod = 'random'
  //form.value.result.value = {}
}
</script>

<template>
  <b-card>
    <!--This form contains all the necessary parameters for a user to submit a request for a computation-->
    <b-form v-if="options" @submit="sendToServer" @reset="initForm">
      <b-row>
        <b-col>
          <!--User can select a dataset. TODO: Multiple Datasets-->
          <h2>Dataset</h2>
          <b-form-group label="Select a dataset">
            <!-- Select a dataset from the options received from the server -->
            <b-form-select
              v-model="form.datasets[0]"
              :options="[
                { text: 'Choose...', value: null },
                ...options.datasets,
              ]"
              required
            ></b-form-select>
          </b-form-group>

          <!--User can select an optional filter-->
          <b-form-group label="Select a filter">
            <!-- Select a dataset filter from the options received from the server -->
            <b-form-select
              v-model="form.filter"
              :options="[{ text: 'None (default)', value: null }]"
            ></b-form-select>
          </b-form-group>

          <!--User provides an optional rating conversion-->
          <b-form-group label="Select a rating conversion">
            <!-- Select a rating conversion from the options received from the server -->
            <b-form-select
              v-model="form.conversion"
              :options="[{ text: 'None (default)', value: null }]"
            ></b-form-select>
          </b-form-group>

          <!--
      <!-User can select which recommender approaches they want->
      <h2>Recommenders</h2>
      <b-form-group>
        <p>Select recommender approaches:</p>
        <b-form-checkbox-group
          v-model="form.recommenders"
          :options="options.approaches"
          buttons
          button-variant="outline-primary"
          size="lg"
          name="buttons-2"
          stacked
          required
        ></b-form-checkbox-group>
      </b-form-group>-->

          <b-form-group label="Select recommender approaches:"> </b-form-group>
          <FormGroupList
            @formChange="(x) => (form.approaches = x)"
            name="approach"
            plural="Recommender approaches"
            selectName="an approach"
            :options="options.approaches"
          />
          <!--
        User gets additional options for the selected recommender approaches
        <b-form-group
          label="ALS Features value:"
          v-if="form.recommenders != null && form.recommenders.includes('ALS')">
          ALS Feature value needs to be a number higher than 1
          <b-form-input
            :state = "form.alsFeatures >= 1"
            placeholder=">= 1"
            v-model="form.alsFeatures"
          ></b-form-input>
        </b-form-group>
        <b-form-group
          label="POP Method:"
          v-if="form.recommenders != null && form.recommenders.includes('POP')">
          POP has three modes to choose from-
          <b-form-select
            v-model="form.popSettings"
            :options="[{ text:'quantile (default)', value:'quantile'}, 'rank', 'count']"
          ></b-form-select>
        </b-form-group>
      </b-form-group>
      -->

          <!--User can select the amount of recommendations per user -->
          <b-form-group label="Select number of recommendations per user:">
            <b-form-input
              type="range"
              :min="options.defaults.recCount.min"
              :max="options.defaults.recCount.max"
              v-model="form.recommendations"
            ></b-form-input>
            <p>{{ form.recommendations }}</p>
            <b-form-checkbox
              v-model="form.includeRatedItems"
              buttons
              button-variant="outline-primary"
              required
              >Include already rated items in recommendations</b-form-checkbox
            >
          </b-form-group>
        </b-col>
        <b-col>
          <!--Input for train/test split-->
          <h2>Train/test-split</h2>
          <b-form-group label="Select test/train split:">
            <b-form-input
              type="range"
              min="0"
              max="100"
              step="5"
              id="customRange"
              v-model="form.split"
            ></b-form-input>
            <p>Train: {{ form.split }}</p>
            <p>Test: {{ 100 - form.split }}</p>
          </b-form-group>

          <!--User can choose between a random and time-based train/testsplit-->
          <b-form-group>
            <b-form-radio-group v-model="form.splitMethod">
              <b-form-radio value="random">Random (default)</b-form-radio>
              <b-form-radio value="timesplit">Timesplit</b-form-radio>
            </b-form-radio-group>
          </b-form-group>

          <!--Input for metrics, user can add infinite metrics -->
          <FormGroupList
            @formChange="(x) => (form.metrics = x)"
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

          <!-- Input for metadata such as:
     Computation Name
     Optional Tags
     Optional Email for notification -->
          <h2>Meta</h2>
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
              placeholder="example@mail.com"
              v-model="metadata.email"
            ></b-form-input>
          </b-form-group>

          <b-button type="submit" variant="primary">Send</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-col>
      </b-row>
    </b-form>
  </b-card>
  <div>
   <ActiveComputation :name = "form.name" />
  </div>
</template>
