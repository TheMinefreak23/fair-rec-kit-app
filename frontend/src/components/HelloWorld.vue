<script setup>
/*
HelloWorld component: make requests to the server and handle the response
*/

import { ref } from 'vue'

const props = defineProps({
  msg: String,
})

const flaskGreeting = ref('')

// GET request
async function greetServer() {
  const response = await fetch('http://localhost:5000/greeting')
  const data = await response.json()
  flaskGreeting.value = data.greeting
}
</script>

<template>
  <div class="container p-3 mb-2 bg-secondary">
    <p>{{ msg }}</p>
    <p>{{ flaskGreeting }}</p>
    <button class="btn btn-primary" @click="greetServer">Greet backend</button>
  </div>
</template>
