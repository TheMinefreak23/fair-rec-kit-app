<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
/*
HelloWorld component: make requests to the server and handle the response
*/

import { ref, onMounted } from 'vue'
import Form from './Form.vue'

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
  <b-container class="p-3 mb-2">
    <b-row>
      <b-col>
        <h3>{{ msg }}</h3>
        <p>{{ flaskGreeting }}</p>
        <b-button variant="outline-primary" @click="greetServer"
          >Greet backend</b-button
        >
      </b-col>
      <b-col cols="8">
        <Form />
      </b-col>
    </b-row>
  </b-container>
</template>
