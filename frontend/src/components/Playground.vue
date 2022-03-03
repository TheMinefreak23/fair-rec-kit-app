<script setup>
/*
Playground component: Shows off a couple Vue 3 + Bootstrap 5 features.
Check out https://vuejs.org/examples 
and https://getbootstrap.com/docs/5.0/getting-started/introduction/ for more
*/
    import { ref } from 'vue'
    const rangeValue = ref(0)
    const checkedNames = ref(['Jack'])
</script>

<template>
  <div class="container p-3 mb-2 bg-secondary">
    <button
      class="btn btn-primary"
      data-bs-target="#collapseTarget"
      data-bs-toggle="collapse"
    >
      Toggle playground
    </button>

    <div class="collapse py-2" id="collapseTarget">
      <!--<img src="@/assets/RecCoonLogo.png" />-->
      <h2>Range</h2>
      <label for="customRange" class="form-label">Example range</label>
      <input
        type="range"
        class="form-range"
        min="0"
        max="100"
        step="20"
        id="customRange"
        v-model="rangeValue"
      />
      <p>Test: {{rangeValue}}</p>
      <p>Train: {{100-rangeValue}}</p>

      <!--
    multiple checkboxes can bind to the same
    array v-model value
    https://vuejs.org/examples/#form-bindings
  -->
  <h2>Multi Checkbox</h2>
  <input type="checkbox" id="jack" value="Jack" v-model="checkedNames" />
  <label for="jack">Jack</label>
  <input type="checkbox" id="john" value="John" v-model="checkedNames" />
  <label for="john">John</label>
  <input type="checkbox" id="mike" value="Mike" v-model="checkedNames" />
  <label for="mike">Mike</label>
  <p>Checked names: <pre>{{ checkedNames }}</pre></p>
    </div>
  </div>
</template>
