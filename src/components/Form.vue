<script setup>
import { ref } from 'vue'

const props = defineProps({
  options: Array,
})

const result = ref({})
const form = ref({ split : 80 })
//const split = ref(80)
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
}
</script>

<template>
  <b-card>
    <b-form @submit="sendToServer" @reset="initForm">
      <b-form-group label="Select a dataset">
        <b-form-select
          v-model="form.dataset"
          :options="[{ text: 'Choose...', value: null }, ...options.datasets]"
          required
        ></b-form-select>
      </b-form-group>
<<<<<<< HEAD
      <b-form-group label="Choose recommender approaches:">
        <b-form-checkbox-group
          v-model="form.recommenders"
          :options= options.approaches
          buttons
          button-variant="outline-primary"
          size="lg"
          name="buttons-2"
          stacked
=======
      <b-form-group label="Select a filter">
        <b-form-select
          v-model="form.filter"
          :options="[{ text: 'None (default)', value: null }]"
          required
        ></b-form-select>
      </b-form-group>
      <b-form-group label="Select a rating conversion">
        <b-form-select
          v-model="form.conversion"
          :options="[{ text: 'None (default)', value: null }]"
>>>>>>> 7a61380506c51111bc06b27e1bfb9f33e771d8bb
          required
        ></b-form-checkbox-group>
      </b-form-group>
      <h2>Train/test-split</h2>
      <b-form-group label="Choose range for test/train split">
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
          required
        >Time-split</b-form-checkbox>
      </b-form-group>


      <b-form-group label="Select a metric">
        <b-form-select
          v-model="form.metric"
          :options="[{ text: 'Choose...', value: null }, ...options.metrics]"
          required
        ></b-form-select>
      </b-form-group>

      <b-form-group label="Enter name for computation">
        <b-form-input
        placeholder="New Computation"
        v-model="form.name"
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
