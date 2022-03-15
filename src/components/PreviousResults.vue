<script setup>
import { ref } from 'vue'
const results = ref([
  { age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
  { age: 21, first_name: 'Larsen', last_name: 'Shaw' },
  { age: 89, first_name: 'Geneva', last_name: 'Wilson' },
  { age: 38, first_name: 'Jami', last_name: 'Carney' },
])

const ex1CurrentPage = ref(1)
const ex1PerPage = ref(10)
const ex1Rows = ref(100)
</script>

<template>
  <div class="container p-3 mb-2 bg-secondary">
    <b-table-simple striped hover>
      <b-tr v-for="item of results">
        <b-th>{{ item.age }}</b-th>
        <b-th>{{ item.first_name }}</b-th>
        <b-th>{{ item.last_name }}</b-th>
      </b-tr>
    </b-table-simple>
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
