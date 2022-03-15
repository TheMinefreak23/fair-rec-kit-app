<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
import HelloWorld from './components/HelloWorld.vue'
import Playground from './components/Playground.vue'
import Results from './components/Results.vue'
</script>

<template>
  <b-tabs content-class="mt-3">
    <b-tab title="Playground" active> <Playground /></b-tab>
    <b-tab title="Hello World"> <HelloWorld msg="Hello Vue!" /></b-tab>
    <b-tab title="Disabled" disabled><p>I'm a disabled tab!</p></b-tab>
    <b-tab title="Results"> <Results msg="Hello Vue!" /></b-tab>
  </b-tabs>
</template>
