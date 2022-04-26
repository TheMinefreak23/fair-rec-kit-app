<script setup>
import { onMounted, ref } from 'vue'
import FormGroupList from '../components/FormGroupList.vue'
import { API_URL } from '../api'

const form = ref({
  datasets: {
    main: [],
    inputs: [],
    selects: [],
    lists: [],
  },
})
const selected = ref({})
const testOptions = ref([
  { text: 'foo', value: { blub: 'bar' } },
  { text: 'hi', value: { blub: 'hivalue' } },
  { text: 'foo3', value: { blub: 'bar3' } },
])

const options = ref({})

onMounted(() => getOptions())

// GET request: Get available options for selection from server
async function getOptions() {
  const response = await fetch(API_URL + '/computation/options')
  const data = await response.json()
  options.value = data.options
  console.log(options.value)
}

function onSubmit() {
  console.log(form.value)
}
</script>

<template>
  <b-card>
    <h3>test form</h3>
    <b-form-select v-model="selected" :options="testOptions"></b-form-select>
    <h4>selected: {{ selected }}</h4>
    <h4>-----------------------------</h4>
    <h3>test fgl</h3>
    <b-form v-if="options" @submit="onSubmit">
      <FormGroupList
        v-model:data="form.datasets"
        name="Dataset"
        plural="Datasets"
        selectName="a dataset"
        :options="options.datasets"
        :required="true"
      />

      <b-button type="submit" variant="primary">Send</b-button>
    </b-form>
  </b-card>
</template>
