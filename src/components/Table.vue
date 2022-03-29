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
  removable: Boolean,
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

function removeEntry() {
  let entry = props.results[selectedEntry.value].datetime
  console.log(entry)
  //updateserver(selectedEntry.value)
  props.results.splice(selectedEntry.value, 1)
}
</script>

<template>
  <b-modal
    id="popup"
    v-model="modalShow"
    title="Remove entry?"
    ok-title="Yes"
    ok-variant="danger"
    cancel-title="No"
    @ok="removeEntry()"
  >
    <p>Are you sure you want to remove this entry from the list?</p>
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
      <b-tr v-for="(item, index) of props.results" :key="item"
        ><b-td v-if="overview">
          <b-button @click="$emit('loadResult', item.id)">View result</b-button>
        </b-td>
        <b-td
          v-for="[key, value] in Object.entries(item)"
          :key="`${index}-${key}`"
        >
          <b-td>
            {{ value }}
          </b-td>
        </b-td>
        <b-button
          v-if="removable"
          variant="danger"
          @click=";(modalShow = !modalShow), (selectedEntry = index)"
          >{{ buttonText }}</b-button
        >
      </b-tr>
    </b-tbody>
  </b-table-simple>
</template>
