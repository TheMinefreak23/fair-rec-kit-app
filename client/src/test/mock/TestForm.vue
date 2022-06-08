<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { onMounted, ref } from 'vue'
import FormGroupList from '../components/Form/FormGroupList.vue'
import { API_URL } from '../api'
import { emptyFormGroup } from '../helpers/optionsFormatter'

const props = defineProps({
  useTestOptions: Boolean,
  initialForm: Object,
  testOptions: Array,
})

const options = ref()
const testOptions = [{ name: 'hi', value: { name: 'hivalue' } }]

const form = ref(initForm())

onMounted(() => {
  if (!props.useTestOptions) getOptions()
})

// GET request: Get available options for selection from server
async function getOptions() {
  const response = await fetch(API_URL + '/experiment/options')
  const data = await response.json()
  options.value = data.options
  console.log(options.value)
}

// Declare default values of the form
function initForm() {
  return {
    lists: { foos: emptyFormGroup(true), optionalFoos: emptyFormGroup(false) },
  }
}

function onSubmit() {
  console.log('form', form.value)
}
</script>

<template>
  <b-card>
    <h3>test fgl</h3>
    <b-form v-if="useTestOptions || options" @submit="onSubmit">
      <FormGroupList
        v-model="form.lists.foos"
        name="foo"
        title="foos"
        :options="useTestOptions ? testOptions : options.datasets"
        required
      />
      <FormGroupList
        v-model="form.lists.optionalFoos"
        name="optional foo"
        title="optional foos"
        :options="useTestOptions ? testOptions : options.recMetrics"
      />
      <p>{{ form }}</p>
      <b-button type="submit" variant="primary">Send</b-button>
    </b-form>
  </b-card>
</template>
