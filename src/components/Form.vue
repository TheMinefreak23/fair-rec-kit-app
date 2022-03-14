<script setup>
import { ref } from 'vue'

const props = defineProps({
  options: Array,
})

const result = ref({})
const form = ref(0)
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
</script>

<template>
  <b-card>
    <b-form @submit="sendToServer" @reset="initForm">
      <b-form-group label="Pick a dataset">
        <b-form-select
          v-model="form.dataset"
          :options="[{ text: 'Choose...', value: null }, ...options.datasets]"
          required
        ></b-form-select>
      </b-form-group>
      <b-form-group label="Pick a number">
        <b-form-select
          v-model="form.number"
          :options="[{ text: 'Choose...', value: null }, ...options.numbers]"
          required
        ></b-form-select>
      </b-form-group>
      <h2>Train/test-split</h2>
      <b-form-group label="Choose range for test/train split">
        <b-form-input
          type="range"
          min="0"
          max="100"
          step="5"
          id="customRange"
          v-model="split"
        ></b-form-input>
      </b-form-group>
      <p>Train: {{split}}</p>
      <p>Test: {{100-split}}</p>

      <b-button type="submit" variant="primary">Send</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
    <p v-if="form.number">{{ result.number }} {{ result.reverse }}</p>
    <p v-else>Magic comes here..</p>
  </b-card>
</template>
