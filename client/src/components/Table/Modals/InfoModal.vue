<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { ref } from 'vue'
import { formatMetadata } from '../../../helpers/metadataFormatter'
import { loadResult } from '../../../helpers/resultRequests'

defineProps({ id: String })
const metadataStr = ref('')
const viewModalShow = ref(false)

async function getMetadata(selectedID) {
  const data = await loadResult(selectedID)
  metadataStr.value = formatMetadata(data.result)
  console.log('Metadata succesfully requested')
}
</script>

<template>
  <b-button
    variant="outline-primary"
    class="mx-1"
    v-b-tooltip.hover
    title="Show information"
    @click=";(viewModalShow = !viewModalShow), getMetadata(id)"
    data-testid="view-meta"
    ><i class="bi bi-info-circle"></i>
    <!-- Shows the metadata and experiment configuration of the designated entry -->
    <b-modal
      id="view-modal"
      v-model="viewModalShow"
      title="Result information"
      ok-only
    >
      <h5>Here is the metadata and experiment configuration:</h5>
      <span style="white-space: pre-wrap">{{ metadataStr }}</span>
    </b-modal>
  </b-button>
</template>
