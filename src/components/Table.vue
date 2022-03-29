<script setup>
import { computed, ref } from 'vue'
import sortBy from 'just-sort-by';
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
  serverFile: String,
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

async function removeEntry() {
  let entry = selectedEntry.value
  props.results.splice(entry, 1)
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({index: entry}),
  }
  fetch('http://localhost:5000' + props.serverFile, requestOptions).then(
    () => {
        console.log("Item removed succesfully")
    }
  )
}

const sorted = computed(() => sort(sortindex.value))

const sortindex = ref(0)
const descending = ref(false)

function sort(i){
    const res = sortBy(props.results, function(o){
        return Object.values(o)[i]
    } )
    
    if(descending.value){
        return res.reverse()
    }
    return res
}

function setsorting(i){
    if(i === sortindex.value){
        descending.value = !descending.value
    }
    sortindex.value = i
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
          :key="header"
          :colspan="header.subheaders ? header.subheaders.length : 1"
          style="cursor: pointer;"
            @click="setsorting(index)"
        >
          {{ header.name }}
        </b-th>
      </b-tr>
      <b-tr>
        <b-th v-if="overview"></b-th>
        <b-th v-for="(subheader, index) in subheaders" :key="subheader">
          {{ subheader }}
        </b-th>
      </b-tr>
    </b-thead>
    <b-tbody>
      <b-tr v-for="(item, index) of sorted" :key="item"
        ><b-td v-if="overview">
          <b-button @click="$emit('loadResult', item.id)">View result</b-button>
        </b-td>
        <b-td
          v-for="[key, value] in Object.entries(item)"
          :key="`${descending}_${sortindex}_${index}-${key}`"
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
