<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import DictionaryDisplay from './DictionaryDisplay.vue'
import { store } from '../../store'
import { loadResult } from '../../helpers/resultRequests'
import { ref } from 'vue'

const props = defineProps({ resultId: String })
const settings = ref()
const show = ref(false)

function setSettings() {
  store.settings = {
    form: settings.value.rawSettings,
    metadata: settings.value.metadata,
  }
  //console.log('raw settings', settings.value.rawSettings)
  //console.log('settings updated', store.settings)
}

async function copySettings(resultId) {
  await getSettings(resultId)
  show.value = !show.value
}

async function getSettings(selectedID) {
  const data = await loadResult(selectedID)
  console.log('Settings succesfully requested')
  settings.value = data.result.settings
  settings.value.metadata = data.result.metadata
}

// omit raw settings in view
function cleanSettings() {
  const { rawSettings, metadata, ...rest } = settings.value
  return rest
}
</script>

<template>
  <!--Shows when the user wants to make settings from a result-->
  <b-modal
    scrollable
    size="lg"
    header-bg-variant="dark"
    header-text-variant="light"
    id="settings-modal"
    v-model="show"
    title="Copy settings from this result?"
    ok-title="Yes"
    ok-variant="danger"
    cancel-title="No"
    @ok="setSettings"
  >
    <b-container v-if="settings">
      <h2>Settings for {{ settings.metadata.name }}:</h2>
      <b-row>
        <DictionaryDisplay :dict="cleanSettings()" />
      </b-row>
    </b-container>
    <p>Do you want to use these settings for a new experiment?</p>
  </b-modal>

  <b-button
    variant="outline-primary fw-bold"
    @click="copySettings(resultId)"
    v-b-tooltip.hover
    title="Copy result settings to new experiment"
  >
    Copy settings
  </b-button>
</template>
