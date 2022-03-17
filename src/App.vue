<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import Form from './components/Form.vue';
import HelloWorld from './components/HelloWorld.vue'
import Playground from './components/Playground.vue'
import Documentation from './components/Documentation.vue'
import Results from './components/Results.vue'

</script>

<template>
  <div class="nav-center">
    <h1 class="text-center bg-dark text-white my-0 py-2">FairRecKit</h1>
    <b-tabs class="m-0" align="center">
      <b-tab title="Computation">   <Form /></b-tab>
      <b-tab title="Documentation"> <Documentation /></b-tab>
      <b-tab title="Results">       <Results /></b-tab>
    </b-tabs>
  </div>
</template>
