<script setup>
import Result from './Result.vue'
import VDismissButton from './VDismissButton.vue'
import PreviousResults from './PreviousResults.vue'
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
</script>

<template>
  <div class="mx-5 mt-2">
    <div class="border-top-0 p-0">
      <div class=" p-3 m-0 container-fluid">
        <h3 class="d-inline">Results</h3>
        <button class="d-inline btn btn-primary float-end" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight" aria-controls="offcanvasRight">Previous Results</button>
      </div>
      <div class="border">
        <b-tabs card content-class="mt-3">
          <b-tab>
            <template #title>
              Result 1
              <VDismissButton />
            </template>

            <Result />
          </b-tab>

          <b-tab title="Result1"><p>I'm Result 1</p></b-tab>
          <b-tab title="Result2"><p>I'm Result 2</p></b-tab>
          <b-tab title="Result3"><p>I'm Result 3</p></b-tab>
        </b-tabs>
      </div>

      <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
        <PreviousResults />
      </div>
    </div>

    

    <!--<div class="col-md-4 border-top-0 p-0">
      <h3 class="text-center py-2 m-0 border-bottom">Previous Results</h3>
      <PreviousResults />
    </div>-->
  </div>
</template>
