<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import { ref } from 'vue'
import { API_URL } from '../../api'
import { store } from '../../store'

const emit = defineEmits(['click'])
const props = defineProps({
  title: String,
  entry: String, // Table item ID
  showButton: Boolean,
  deleteURL: String,
})

const deleteModalShow = ref(false)

async function removeEntry() {
  //Remove entry from the list
  //props.results.splice(entry, 1)
  store.allResults = store.allResults.filter((e) => e.id != props.entry)
  //Inform the server to remove the same entry
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: props.entry }),
  }
  fetch(API_URL + props.deleteURL, requestOptions)
    .then((response) => response.text())
    .then((data) => {
      if (data == 'Removed index')
        console.log('Item', props.entry, 'removed succesfully')
    })
}
</script>
<template>
  <!--Shows when the user wants to delete an entry-->
  <b-modal
    id="deletion-modal"
    v-model="deleteModalShow"
    :title="title"
    ok-title="Yes"
    ok-variant="danger"
    cancel-title="No"
    @ok="removeEntry()"
  >
    <p>Are you sure you want to remove this entry from the list?</p>
  </b-modal>
  <b-button
    v-if="showButton"
    variant="danger"
    class="mx-1 float-end"
    @click="deleteModalShow = !deleteModalShow"
  >
    <slot></slot>
  </b-button>
</template>
