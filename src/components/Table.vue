<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
/*
Playground component: Shows off a couple Vue 3 + Bootstrap 5 features.
Check out https://vuejs.org/examples 
and https://getbootstrap.com/docs/5.0/getting-started/introduction/ for more
*/
const props = defineProps({
  pretty_headers: Array,
  results: Array,
  headers: Array,
})

console.log(props.results)
</script>

<template>
  <b-table-simple striped hover>
    <b-thead head-variant="dark">
      <b-tr>
        <b-th v-for="header in pretty_headers" :key="header.id">
          {{ header }}
        </b-th>
      </b-tr>
    </b-thead>
    <b-tr v-for="item of results" :key="item.id">
      <b-td v-for="header in headers" :key="header.id">
        {{ item[header] }}
      </b-td>
    </b-tr>
  </b-table-simple>
</template>
