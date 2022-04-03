<script setup>
import { ref } from 'vue'
import FormGroupList from '../components/FormGroupList.vue'

const form = ref({
  datasets: {
    main: [],
    inputs: [],
    selects: [],
  },
})
const options = ref({ datasets: [{ name: 'test', params: [] }] })

function onSubmit() {
  console.log(form.value)
}
</script>

<template>
  <b-card>
    test
    <b-form v-if="options" @submit="onSubmit">
      <FormGroupList
        v-model:data="form.datasets"
        name="Dataset"
        plural="Datasets"
        selectName="a dataset"
        :options="options.datasets"
      />

      <b-button type="submit" variant="primary">Send</b-button>
    </b-form>
  </b-card>
</template>
