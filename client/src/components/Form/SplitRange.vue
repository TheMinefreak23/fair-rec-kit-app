<script setup>
import { computed, ref } from 'vue'

const emit = defineEmits(['input'])
const props = defineProps({
  value: { type: [String, Number], required: true },
  name: String,
  min: Number,
  max: Number,
  step: Number,
})

const rightVal = computed({
  // getter
  get() {
    return 100 - props.value
  },
  // setter
  set(newValue) {
    emit('input', 100 - newValue)
  },
})

/*
// source: https://www.geeksforgeeks.org/multiple-of-x-closest-to-n/
// Function to calculate the
// smallest multiple
function closestMultiple(n, x) {
  if (x > n) return x
  n = n + parseInt(x / 2, 10)
  n = n - (n % x)
  console.log('closest mult', n)
  return n
}*/

function correctValue() {
  // Between min and max and divisible by step
  return (
    props.value > props.min &&
    props.value < props.max &&
    props.value % props.step == 0
  )
}
</script>

<template>
  <template v-if="name.includes('Train')">
    <b-form-input
      type="range"
      :min="min"
      :max="max"
      :step="step"
      data-testid="split-input"
      id="customRange"
      v-model="value"
    ></b-form-input>
    <b-row>
      <b-col cols="5">
        <strong>Train:</strong>
        <b-form-input v-model="value" :state="correctValue()"></b-form-input>
      </b-col>
      <b-col></b-col>
      <b-col cols="5">
        <strong>Test:</strong>
        <b-form-input v-model="rightVal" :state="correctValue()"></b-form-input>
      </b-col>
    </b-row>
  </template>
</template>
