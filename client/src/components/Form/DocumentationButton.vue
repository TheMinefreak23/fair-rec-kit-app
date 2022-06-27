<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */
import { scrollToDocText } from '../../documentation/documentation_tree2'

defineProps({ name: String })
</script>

<template>
  <b-button
    variant="light"
    v-b-tooltip.hover
    title="Go to documentation"
    @click="scrollToDocText(name)"
  >
    <i class="bi bi-info-circle" />
    <i class="bi bi-arrow-right-short" />
  </b-button>
</template>
