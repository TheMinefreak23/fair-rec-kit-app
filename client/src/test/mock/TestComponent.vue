<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { computed } from 'vue'

const props = defineProps(['modelValue'])
const emit = defineEmits(['update:modelValue'])

const form = computed({
  get() {
    // console.log(props.name, props.data)
    return props.modelValue
  },
  set(localValue) {
    console.log('local form change to', localValue)
    emit('update:modelValue', localValue)
  },
})
</script>

<template>
  <div>
    <p>{{ form }}</p>
    <b-form-input v-model="form" />
  </div>
</template>
