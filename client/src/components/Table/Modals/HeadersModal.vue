<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { ref } from 'vue'
import {
  makeHeader,
  capitalise,
  STANDARD_HEADERS,
} from '../../../helpers/resultFormatter'

defineProps({ headerOptions: Object })
defineEmits(['updateHeaders'])
const updateHeadersModalShow = ref(false)

// Columns
const checkedColumns = ref(STANDARD_HEADERS)
</script>

<template>
  <div>
    <!-- Modal used for changing the headers of the user recommendations table -->
    <b-modal
      v-if="headerOptions"
      id="change-columns-modal"
      v-model="updateHeadersModalShow"
      title="Select headers"
      @ok="$emit('updateHeaders', checkedColumns)"
    >
      <p>Select the extra headers you want to be shown</p>
      <div v-for="category in Object.keys(headerOptions)" :key="category">
        <p>{{ capitalise(category) }} specific:</p>
        <div
          class="form-check form-switch"
          v-for="header in headerOptions[category]"
          :key="header"
        >
          <input
            v-model="checkedColumns"
            class="form-check-input"
            type="checkbox"
            :value="header"
            :id="header"
          />
          <label class="form-check-label" :id="header">
            {{ makeHeader(header).name }}
          </label>
        </div>
      </div>
    </b-modal>

    <b-button
      @click="updateHeadersModalShow = !updateHeadersModalShow"
      class="m-1"
    >
      Select Headers
    </b-button>
  </div>
</template>
