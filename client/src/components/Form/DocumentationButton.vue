<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */
import { scrollToDocText } from '../../documentation/documentation_tree2'
import { capitalise } from '../../helpers/resultFormatter'
import descriptions from '../../documentation/descriptions.json'
import { ref } from 'vue'

defineProps({ name: String, dark: Boolean })
const show = ref(false)
</script>

<template>
  <div v-if="capitalise(name) in descriptions">
    <b-popover :show="show" :target="name + 'info'" triggers="click blur">
      <template #title>{{ capitalise(name) }}</template>
      {{ descriptions[capitalise(name)] }}
      <b-button
        variant="outline-info"
        @click="
          () => {
            scrollToDocText(name)
            show = false
          }
        "
      >
        Go to documentation</b-button
      >
    </b-popover>

    <b-button
      @click="show = true"
      :id="name + 'info'"
      :variant="dark ? 'light' : 'outline-light'"
    >
      <i class="bi bi-info-circle-fill" />
    </b-button>
    <!--<slot :id="name + 'info'"></slot>-->
  </div>
</template>
