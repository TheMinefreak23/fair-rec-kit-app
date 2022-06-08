<script setup>
/* A range (minimal and maximal value) for train-test split */
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */
import { computed } from 'vue'

const emit = defineEmits(['update:modelValue'])
const props = defineProps({
  modelValue: { required: true }, // The local range form value
  min: Number, // The minimal range value
  max: Number, // The maximal range value
  step: Number, // The slider step
})

/**
 * Form value of the range
 */
const value = computed({
  get() {
    return props.modelValue
  },
  set(localValue) {
    emit('update:modelValue', localValue)
  },
})

/**
 * The right bound of the range
 */
const rightVal = computed({
  get() {
    return 100 - props.modelValue
  },
  set(localValue) {
    emit('update:modelValue', 100 - localValue)
  },
})

/**
 * Check whether the value is valid
 * (between min and max and divisible by step)
 */
function correctValue() {
  return (
    value.value > props.min &&
    value.value < props.max &&
    value.value % props.step === 0
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
