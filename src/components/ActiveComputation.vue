<script setup>
    /*This program has been developed by students from the bachelor Computer Science at
    Utrecht University within the Software Project course.
    © Copyright Utrecht University (Department of Information and Computing Sciences)*/

import { onMounted, ref } from 'vue'

const emit = defineEmits(['computing', 'done', 'stop'])
const props = defineProps({
  name: String,
})


const computations = ref([])

onMounted(() => {
  getResults()
})


async function cancelComputation() {

  emit('stop')
}

async function getComputations(){
  const response = await fetch('http://localhost:5000/activecomputations')
  const data = await response.json()
  //if active computations:
  emit('computing')
}

var done;

</script>

<template>
    <div>
      <h1>Waiting for "{{name}}" to be finished...</h1>
      <b-spinner></b-spinner> 
      <b-button v-b-modal.popup variant="danger">Cancel</b-button>
      <b-modal id="popup" 
               title="Cancel computation?" 
               ok-title ="Yes"
               ok-variant ="danger"
               cancel-title="No"
               @ok ="cancelComputation()">
        <p>Are you sure you want to cancel the active computation?</p>
      </b-modal>
      <b-button @click="$emit('computing')">Computing</b-button>
      <b-button @click="$emit('done')">Done</b-button>
    </div>
</template>