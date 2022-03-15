<script setup>
const props = defineProps({
  results: Array,
  headers: Array,
})

console.log(props.results)
</script>

<template>
  <b-table-simple striped hover>
    <b-thead head-variant="dark">
      <b-tr>
        <b-th v-for="header in headers" :key="header.id">
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
