<script setup>
import { onMounted, ref } from 'vue'
import FormGroupList from '../components/Form/FormGroupList.vue'
import { API_URL } from '../api'

const props = defineProps({
  useTestOptions: Boolean,
  initialForm: Object,
  testOptions: Array,
})

const options = ref([{ name: 'hi', value: { name: 'hivalue' } }])

const form = ref({
  groupCount: 1,
  main: [],
  inputs: [],
  selects: [],
  lists: [],
})

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

function onSubmit() {
  console.log(form.value)
}
</script>

<template>
  <b-card>
    <h3>test fgl</h3>
    <b-form v-if="useTestOptions || options" @submit="onSubmit">
      <!--<FormGroupList
        v-model:data="form.datasets"
        name="Dataset"
        plural="Datasets"
        selectName="a dataset"
        :options="options.datasets"
        :required="true"
      />-->
      <!--<p>{{ options.datasets }}</p>-->
      <FormGroupList
        v-model:data="form"
        name="foo"
        plural="foos"
        :options="useTestOptions ? options : options.datasets"
        :required="true"
      />
      <p v-if="form.main[0]">First Selected: {{ form.main[0].name }}</p>
      <b-button type="submit" variant="primary">Send</b-button>
    </b-form>
  </b-card>
</template>
