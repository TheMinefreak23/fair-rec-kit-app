<script setup>
import { computed, ref } from 'vue'
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

const emit = defineEmits(['loadResult'])
const props = defineProps({
  overview: Boolean,
  results: Array,
  headers: Array,
  buttonText: String,
})

const modalShow = ref(false)
const selectedEntry = ref(0)
const subheaders = computed(() => {
  const result = []

  for (const header of props.headers) {
    if (header.subheaders) {
      result.push(...header.subheaders)
    } else {
      result.push('')
    }
  }

  return result
})

</script>

<template>
  <b-modal 
    id="deletion-modal" 
    v-model="modalShow"
    title="You are trying to delete this result"
    @ok="$emit('deleteResult', selectedEntry)"
  >
    <div class="d-block text-center">
      <h3>Warning: if you delete this result it will be gone forever</h3>
    </div>
  </b-modal>
  <b-table-simple hover striped responsive>
    <b-thead head-variant="dark">
      <b-tr>
        <b-th v-if="overview"></b-th>
        <b-th
          v-for="(header, index) in headers"
          :key="`header-${index}`"
          :colspan="header.subheaders ? header.subheaders.length : 1"
        >
          {{ header.name }}
        </b-th>
      </b-tr>
      <b-tr>
        <b-th v-if="overview"></b-th>
        <b-th
          v-for="(subheader, index) in subheaders"
          :key="`subheader-${index}`"
        >
          {{ subheader }}
        </b-th>
      </b-tr>
    </b-thead>
    <b-tbody>
      <b-tr v-for="(item, index) of results" :key="item.id">
        <b-td v-if="overview">
          <b-button @click="$emit('loadResult', item.id)">View result</b-button>
        </b-td>
        <b-td
          v-for="[key, value] in Object.entries(item)"
          :key="`${index}-${key}`"
          ><b-td>{{ value }}</b-td>
        </b-td>
        <b-td v-if="overview">
          <b-button pill @click="$emit('edit', item.id)">Edit</b-button>
          &nbsp;
          <b-button variant="danger" @click="modalShow = !modalShow, selectedEntry = item.id">Delete</b-button>
        </b-td>
      </b-tr>
    </b-tbody>
  </b-table-simple>
</template>
