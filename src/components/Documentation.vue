<script setup>
  /*This program has been developed by students from the bachelor Computer Science at
  Utrecht University within the Software Poject course.
  © Copyright Utrecht University (Department of Information and Computing Sciences)*/
  /*
  Documentation tab which shows all algorithms, metrics, datasets, etc. and their meaning.
  */
  function previewFile() {
    const content = document.querySelector('.content');
    const [file] = document.querySelector('input[type=file]').files;
    const reader = new FileReader();

    reader.addEventListener("load", () => {
      // this will then display a text file
      content.innerText = reader.result;
    }, false);

    if (file) {
      reader.readAsText(file);
    }
  }
 
</script>

<template>
  <div class="text-center py-2 mx-5">
    <h3>Documentation</h3>
    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae rerum qui facilis. Perspiciatis officiis debitis accusamus illum harum sit dolore adipisci voluptatum. Rerum, velit quia magnam quis placeat necessitatibus ea.</p>
  </div>
  
  <input type="file" v-on:change=previewFile()><br>
  <p class="content"></p>
  
  
</template>


