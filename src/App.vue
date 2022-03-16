<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
import HelloWorld from './components/HelloWorld.vue'
import Playground from './components/Playground.vue'
import Documentation from './components/Documentation.vue'
import Results from './components/Results.vue'
</script>

<template>
  <h1 class="text-center">FairRecKit</h1>

  <b-tabs pills card>
    <b-tab title="Computation"> <Playground /></b-tab>
    <b-tab title="Documentation"> <Documentation /></b-tab>
    <b-tab title="Results"> <Results /></b-tab>
  </b-tabs>
</template>
