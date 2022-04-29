<script setup>
import { onMounted, ref } from 'vue'
import { API_URL } from '../api'

const test = ref('test')

onMounted(() => {
  auth()
})

async function auth() {
  const response = await fetch(API_URL + '/token')
  const data = await response.json()
  test.value = data
}
</script>

<template>
  <h1>KEK</h1>
  {{ test.token_type + ': ' + test.access_token }}
</template>
