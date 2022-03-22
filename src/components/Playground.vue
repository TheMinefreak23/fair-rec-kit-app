<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
/*
Playground component: Shows off a couple Vue 3 + Bootstrap 5 features.
Check out https://vuejs.org/examples 
and https://getbootstrap.com/docs/5.0/getting-started/introduction/ for more
*/
    import { ref } from 'vue'
    import Table from './Table.vue'
    const rangeValue = ref(0)
    const checkedNames = ref(['Jack'])
    const headers = ref(['header1','header2'])
    const results = ref([{header1:'foo1',header2:'bar1'},{header1:'foo2',header2:'bar2'}])
</script>

<template>

  <div class="container p-3 mb-2 bg-secondary">
    <Table :headers=headers :results=results />
    <b-button
      variant="primary"
      data-bs-target="#collapseTarget"
      data-bs-toggle="collapse"
    >
      Toggle collapse
    </b-button>
    
    <div class="collapse py-2" id="collapseTarget">
      <img src="/RecCoonLogo.png"/>
      <p>RecCoons</p>
      </div>
      <h2>Modal</h2>
      <!-- Button trigger modal -->
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
  Launch demo modal
</button>

<!-- Modal -->
<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        ...
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>
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
</template>
