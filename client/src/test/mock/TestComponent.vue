<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { ref } from 'vue'

defineProps(['test'])
const counter = ref(0)
</script>

<template>
  <div>
    <h1>{{ test }}</h1>
    <button @click="counter++">increment</button>
    <p>counter: {{ counter }}</p>
  </div>
</template>
