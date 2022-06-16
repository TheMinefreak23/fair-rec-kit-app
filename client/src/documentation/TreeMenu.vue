<template>
  <div class="tree-menu">
    <b-card class="border-end-0 border-top-0 border-bottom-0 border-5 bg-secondary">
      <b-card-title>{{ label }} 
        <b-button> 
          <template> <i class="bi bi-caret-down" /> </template>
        </b-button>
      </b-card-title>
      <!-- v-if because if there is no description -> undefined, which takes space. -->    
      <tree-menu 
        v-for="node in nodes" 
        :nodes="node.nodes" 
        :label="node.label"
        :depth="depth+1"
      >
      </tree-menu>
    </b-card> 
  </div>
</template>
<script>
  export default { 
    props: [ 'label', 'nodes' ],
    name: 'tree-menu'
  }
</script>