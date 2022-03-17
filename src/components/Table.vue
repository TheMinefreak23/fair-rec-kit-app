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
 //pretty_headers: Object,
  results: Array,
  headers: Array,
  //subheaders: Array
})

console.log(props.results)
</script>

<template>
  <b-table-simple hover striped responsive>
    <colgroup v-for="header in headers" :key="header.id">
      <col v-for="subheader in header.subheaders" :key="subheader.id">
    </colgroup>
    <b-thead head-variant="dark">
      <b-tr>
        <b-th v-for="header in headers" :key="header.id" colspan="header.subheaders.length" >
            {{ header.name}}
        </b-th>
      </b-tr>
      <b-tr>
        <b-th v-for="header in headers" :key="header.id">
          <b-th v-if="header.subheaders == null">test</b-th>
          <b-th v-else v-for="subheader in header.subheaders" :key="subheader.id">
              {{ subheader }}
          </b-th>          
        </b-th>
      </b-tr>
    </b-thead>
    <b-tbody>
      <b-tr v-for="item of results" :key="item.id">
        <b-td v-for="header in headers" :key="header.id">
          <b-td v-if="header.subheaders == null" >
            {{ item[header.name] }}
          </b-td>
          <b-td v-else v-for="subheader in header.subheaders" :key="subheader.id">
              {{ item[subheader] }}
            </b-td>
                
        </b-td>
      </b-tr>
    </b-tbody>
  </b-table-simple>
</template>
