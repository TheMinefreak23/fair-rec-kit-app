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
  serverFile: String,
})

const deleteModalShow = ref(false)
const editModalShow = ref(false)
const newName = ref('')
const newTags = ref('')
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

function handleEditOk(){
  emit('edit', selectedEntry.value, newName.value, newTags.value)
  newName.value = ''
  newTags.value = ''
}

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
</script>

<template>
    <b-modal 
        id="deletion-modal"
        v-model="deleteModalShow"
        title="Remove entry?" 
        ok-title ="Yes"
        ok-variant ="danger"
        cancel-title="No"
        @ok ="removeEntry()">
      <p>Are you sure you want to remove this entry from the list?</p>
    </b-modal>
  <b-modal
    id="edit-modal"
    v-model="editModalShow"
    title="Editing results"
    size="lg"
    @ok="handleEditOk"
  >
    <h6>Please type in the new values. Blank fields will be left unchanged.</h6>
    Name:
    <b-form-input v-model="newName" placeholder="New name"></b-form-input>
    <br>
    Tags:
    <b-form-input v-model="newTags" placeholder="New tags"></b-form-input>
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
        
          <b-button v-if="overview" pill @click="editModalShow = !editModalShow, selectedEntry = index">Edit</b-button>
          &nbsp;
          <b-button v-if="removable" variant="danger" @click="deleteModalShow = !deleteModalShow, selectedEntry = index">Delete</b-button>
        
      </b-tr>
    </b-tbody>
  </b-table-simple>
</template>
