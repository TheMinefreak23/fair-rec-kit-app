<script setup>
// DEV

import { ref } from 'vue'
import { emptyFormGroup } from '../helpers/optionsFormatter'
import TestComponent from './TestComponent.vue'
import TestForm from './TestForm.vue'

const test = ref('hi')
</script>

<template>
  <div id="App">
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css"
      rel="stylesheet"
    />
    <TestComponent v-model="test" />
    <TestForm :useTestOptions="false" />
  </div>
</template>
