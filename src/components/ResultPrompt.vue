<script setup>
const emit = defineEmits(['goToResult'])
const props = defineProps({
  show: Boolean,
})
</script>

<template>
  <!--Shows when there is a new result-->
  <b-modal
    id="result-modal"
    v-model="show"
    title="New result"
    ok-title="View new result"
    ok-variant="danger"
    cancel-title="Cancel"
    @ok="$emit('goToResult')"
  >
    <p>An experiment has finished.</p>
  </b-modal>
</template>
