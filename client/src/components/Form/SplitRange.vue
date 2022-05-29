<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */
import { computed } from 'vue'

const emit = defineEmits(['update:modelValue'])
const props = defineProps({
  modelValue: { required: true },
  name: String,
  min: Number,
  max: Number,
  step: Number,
})

const value = computed({
  // getter
  get() {
    return props.modelValue
  },
  // setter
  set(localValue) {
    emit('update:modelValue', localValue)
  },
})

const rightVal = computed({
  // getter
  get() {
    return 100 - props.modelValue
  },
  // setter
  set(localValue) {
    emit('update:modelValue', 100 - localValue)
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
} */

function correctValue() {
  // Between min and max and divisible by step
  return (
    props.value > props.min &&
    props.value < props.max &&
    props.value % props.step === 0
  )
}
</script>

<template>
  <div>
    <b-form-input
      type="range"
      :min="min"
      :max="max"
      :step="step"
      data-testid="split-input"
      id="customRange"
      v-model="value"
      number
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
  </div>
</template>
