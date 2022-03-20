<script setup>
    /*This program has been developed by students from the bachelor Computer Science at
    Utrecht University within the Software Project course.
    © Copyright Utrecht University (Department of Information and Computing Sciences)*/
const props = defineProps({
  name: String,
})

function cancelComputation() {

}

</script>

<template>
    <div>
      <h1>Waiting for "{{name}}" to be finished...</h1>
      <b-img src="/Loading_icon.gif" fluid alt="Loading"></b-img>
      <b-button v-b-modal.popup variant="danger">Cancel</b-button>
      <b-modal id="popup" 
               title="Cancel computation?" 
               ok-title ="Yes"
               ok-variant ="danger"
               cancel-title="No"
               @ok ="cancelComputation()">
        <p>Are you sure you want to cancel the active computation?</p>
      </b-modal>
    </div>
</template>