<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { computed } from 'vue'

const emit = defineEmits(['update:modelValue'])
const props = defineProps({
  modelValue: { required: true },
})

const tags = computed({
  // getter
  get() {
    return props.modelValue
  },
  // setter
  set(localValue) {
    emit('update:modelValue', localValue)
  },
})
</script>

<template>
  <b-form-tags
    v-model="tags"
    tag-pills
    tag-variant="dark"
    remove-on-delete
    separator=" ,;"
  />
</template>
