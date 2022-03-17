<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
import { ref } from 'vue'

const props = defineProps({
  options: Array,
})

const result = ref({})
const form = ref({split:80,
                  recommendations:10,
                  metric:[],
                  metricK:[],
                  splitMethod:"random"
                 })
const groupCount = ref(1)

// POST request: Send form to server.
function sendToServer() {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(form.value),
  }
  fetch('http://localhost:5000/computation/calculation', requestOptions).then(
    () => {
      getCalculation()
    }
  )
}

// GET request: Ask server for latest calculation
async function getCalculation() {
  const response = await fetch('http://localhost:5000/computation/calculation')
  const data = await response.json()
  result.value = data.calculation
  console.log(result.value)
}

function initForm() {
  form.value = {}
  result.value = {}
}
</script>

<template>
  <b-card>

    <!--This form contains all the necessary parameters for a user to submit a request for a computation-->
    <b-form @submit="sendToServer" @reset="initForm">
      <!--User can select a dataset. TODO: Multiple Datasets-->
      <h2>Dataset</h2>
      <b-form-group label="Select a dataset">
        <b-form-select
          v-model="form.dataset"
          :options="[{ text: 'Choose...', value: null }, ...options.datasets]"
          required
        >
        </b-form-select>
      </b-form-group>

      <!--User can select an optional filter-->
      <b-form-group label="Select a filter">
        <b-form-select
          v-model="form.filter"
          :options="[{ text: 'None (default)', value: null }]"
        >
        </b-form-select>
      </b-form-group>

      <!--User provides an optional rating conversion-->
      <b-form-group label="Select a rating conversion">
        <b-form-select
          v-model="form.conversion"
          :options="[{ text: 'None (default)', value: null }]"
        ></b-form-select>
      </b-form-group>

      <!--User can select which recommender approaches they want-->
      <h2>Recommenders</h2>
      <b-form-group>
        <p>Select recommender approaches:</p>
        <b-form-checkbox-group
          v-model="form.recommenders"
          :options= options.approaches
          buttons
          button-variant="outline-primary"
          size="lg"
          name="buttons-2"
          stacked
          required
        ></b-form-checkbox-group>

        <!--User gets additional options for the selected recommender approaches-->
        <b-form-group 
          label="ALS Features value:" 
          v-if="form.recommenders != null && form.recommenders.includes('ALS')">
          <b-form-input
            :state = "form.alsFeatures >= 1"
            placeholder=">= 1"
            v-model="form.alsFeatures"
          ></b-form-input>
        </b-form-group>
        <b-form-group 
          label="POP Method:" 
          v-if="form.recommenders != null && form.recommenders.includes('POP')">
          <b-form-select
            v-model="form.popSettings"
            :options="[{ text:'quantile (default)', value:'quantile'}, 'rank', 'count']"
          ></b-form-select>
        </b-form-group>
      </b-form-group>

      <!--User can select the amount of recommendations per user -->
      <b-form-group label="Select number of recommendations per user:">
        <b-form-input
          type="range"
          min="1"
          max="10"
          v-model="form.recommendations"
        ></b-form-input>
        <p>{{form.recommendations}}</p>
        <b-form-checkbox
          v-model="form.includeRatedItems"
          buttons
          button-variant="outline-primary"
          value="true"
          unchecked-value="false"
          required
        >Include already rated items in recommendations</b-form-checkbox>
      </b-form-group>
      
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
        <p>Train: {{form.split}}</p>
        <p>Test: {{100-form.split}}</p>

        <!--User can choose between a random and time-based train/testsplit-->
        <b-form-radio v-model="form.splitMethod" value="random">Random (default)</b-form-radio>
        <b-form-radio v-model="form.splitMethod" value="timesplit">Timesplit</b-form-radio>
      </b-form-group>

      <!--Input for metrics, user can add infinite metrics -->
      <h2>Metrics</h2>
      <b-form-group 
      v-for="i in groupCount"
      label="Select a metric"
      v-bind:key="i">
        <b-form-select
          v-model="form.metric[i]"
          :options="[{ text: 'Choose...', value: null }, ...options.metrics]"
          required
        >
        </b-form-select>
        <b-form-group v-if="form.metric[i] != null && form.metric[i].includes('@')" >
          <p>Metric @ K?:</p>
          <b-form-input
            v-model="form.metricK[i]"
            :state = "form.metricK[i] <= form.recommendations"
            required
          ></b-form-input>
        </b-form-group>
      </b-form-group>
      
      <b-button @click="groupCount++">Add Metric...</b-button>
      <b-button @click="groupCount--" variant="danger">Remove Metric</b-button>

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
        v-model="form.name"
        required
        ></b-form-input>
      </b-form-group>
      <b-form-group label="Enter tags (optional)">
        <b-form-input
        v-model="form.tags"
        ></b-form-input>
      </b-form-group>
      <b-form-group label="Enter e-mail (optional)">
        <b-form-input
        placeholder="example@mail.com"
        v-model="form.email"
        ></b-form-input>
      </b-form-group>

      <b-button type="submit" variant="primary">Send</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
  </b-card>
</template>