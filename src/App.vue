<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import Form from './components/Form.vue'
import Playground from './components/Playground.vue'
import Documentation from './components/Documentation.vue'
import Results from './components/Results.vue'
import PreviousResults from './components/PreviousResults.vue';
import ActiveComputation from './components/ActiveComputation.vue';
</script>

<template>
  <div class="bg-dark nav justify-content-center py-2">
    <img src="/RecCoonLogo.png" class="" style="height: 50px" />
    <h1 class="text-white my-0 p-0">FairRecKit</h1>
  </div>
  <div class="nav-center">
    <b-tabs class="m-0 pt-2" align="center">
      <b-tab title="New Computation"> <Form /></b-tab>
      <b-tab title="Active Computations"> <ActiveComputation /></b-tab>
      <b-tab title="Documentation"> <Documentation /></b-tab>
      <b-tab title="Results"> <Results /></b-tab>
      <b-tab title="All results"> <PreviousResults /></b-tab>
    </b-tabs>
  </div>
</template>
