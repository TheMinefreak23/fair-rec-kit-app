<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import DictionaryDisplay from '../DictionaryDisplay.vue'
import { store } from '../../../store'
import { loadResult } from '../../../helpers/resultRequests'
import { ref } from 'vue'

const props = defineProps({ resultId: String })
const settings = ref() // The result settings to display
const show = ref(false) // Whether to show the modal

/**
 * Set the new experiment form settings using the modal settings
 */
function setSettings() {
  store.settings = {
    form: settings.value.rawSettings,
    metadata: settings.value.metadata,
  }
  // console.log('raw settings', settings.value.rawSettings)
  // console.log('settings updated', store.settings)
}

/**
 * Load the result settings modal.
 * @param {Int} resultId - The ID of the result
 */
async function loadSettings(resultId) {
  await getSettings(resultId)
  show.value = !show.value
}

/**
 * Get the settings for the result.
 * @param {Int} selectedID - The ID of the result
 */
async function getSettings(selectedID) {
  const result = await loadResult(selectedID)
  console.log('Settings from ID', selectedID, 'succesfully requested')
  settings.value = result.settings
  settings.value.metadata = result.metadata
}

/**
 * Don't show the raw settings in the modal.
 */
function cleanSettings() {
  // Omit raw settings
  const { rawSettings, metadata, ...rest } = settings.value
  return rest
}
</script>

<template>
  <!--Show when the user wants to make settings from a result.-->
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
    <!--Display the result settings in a readable way.-->
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
    v-b-tooltip.hover
    title="Copy result settings to new experiment"
    data-testid="copy-settings"
    @click="loadSettings(resultId)"
  >
    Copy settings
  </b-button>
</template>
