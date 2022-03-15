<script setup>
import Table from './Table.vue'
import { ref } from 'vue'
const results = ref([
  { id: 1, age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
  { id: 2, age: 21, first_name: 'Larsen', last_name: 'Shaw' },
  { id: 3, age: 89, first_name: 'Geneva', last_name: 'Wilson' },
  { id: 4, age: 38, first_name: 'Jami', last_name: 'Carney' },
])
const headers = ref(['id', 'age', 'first_name', 'last_name'])

const ex1CurrentPage = ref(1)
const ex1PerPage = ref(10)
const ex1Rows = ref(100)
</script>

<template>
  <div class="container p-3 mb-2 bg-secondary">
    <Table :results="results" :headers="headers" />
    <b-card>
      <div class="overflow-auto py-2">
        <h1>Previous results</h1>
        <b-pagination
          v-model="ex1CurrentPage"
          :total-rows="ex1Rows"
          :per-page="ex1PerPage"
          first-text="First"
          prev-text="Prev"
          next-text="Next"
          last-text="Last"
        ></b-pagination>
      </div>
    </b-card>
  </div>
</template>
