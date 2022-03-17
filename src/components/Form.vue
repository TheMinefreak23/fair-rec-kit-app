<script setup>
import { ref } from 'vue'

const props = defineProps({
  options: Object,
})

const result = ref({})
const form = ref({})

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
      <b-button type="submit" variant="primary">Send</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
    <p v-if="form.number">{{ result.number }} {{ result.reverse }}</p>
    <p v-else>Magic comes here..</p>
  </b-card>
</template>
