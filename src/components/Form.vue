<script setup>
import { ref } from 'vue'

const props = defineProps({
  options: Array,
})

const result = ref({})
const form = ref({split:80,
                  recommendations:10,
                  metricK:1
                 })
const split = ref(80)
//const split = ref(80)


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
  split = 80
}

function generateMetric(){ //todo: generate multiple metrics
 
}
</script>

<template>
  <b-card>
    <b-form @submit="sendToServer" @reset="initForm">
      <h2>Dataset</h2>
      <b-form-group label="Select a dataset">
        <b-form-select
          v-model="form.dataset"
          :options="[{ text: 'Choose...', value: null }, ...options.datasets]"
          required
        >
        </b-form-select>
      </b-form-group>
      <b-form-group label="Select a filter">
        <b-form-select
          v-model="form.filter"
          :options="[{ text: 'None (default)', value: null }]"
        >
        </b-form-select>
      </b-form-group>
      <b-form-group label="Select a rating conversion">
        <b-form-select
          v-model="form.conversion"
          :options="[{ text: 'None (default)', value: null }]"
        ></b-form-select>
      </b-form-group>

      <b-form-group>
        <h2>Recommenders</h2>
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
        <b-form-checkbox
          v-model="form.timesplit"
          buttons
          button-variant="outline-primary"
          name="timesplit"
          value="true"
          unchecked-value="false"
        >Time-split</b-form-checkbox>
      </b-form-group>

      <h2>Metrics</h2>
      <b-form-group label="Select a metric">
        <b-form-select
          v-model="form.metric"
          :options="[{ text: 'Choose...', value: null }, ...options.metrics]"
          required
        ></b-form-select>
        <b-form-group label="Metric @ K:" 
          v-if="form.metric != null && form.metric.includes('@')" >
          <b-form-input
            v-model="form.metricK"
            :state = "form.metricK >= 1 && form.metricK <= form.recommendations"
            required
          ></b-form-input>
          <p>{{form.recommendations}} {{form.metricK}}</p>
        </b-form-group>
      </b-form-group>
      <b-form-group label="Select a results filter">
        <b-form-select
          v-model="form.resFilter"
          :options="[{ text: 'Global (default)', value: null }]"
        ></b-form-select>
      </b-form-group>

      <h2>Meta</h2>
      <b-form-group label="Enter name for computation">
        <b-form-input
        placeholder="New Computation"
        v-model="form.name"
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
