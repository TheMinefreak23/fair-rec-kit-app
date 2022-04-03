<script setup>
import Result from './Result.vue'
import VDismissButton from './VDismissButton.vue'
import PreviousResults from './PreviousResults.vue'
import { ref } from 'vue'
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
</script>

<template>
  <div class="row">
    <div class="col-md-8 border-top-0 p-0">
      <h3 class="py-2 border-bottom text-center m-0">Results</h3>
      <div>
        <b-tabs card content-class="mt-3">
          <b-tab>
            <template #title>
              Result 1
              <VDismissButton />
            </template>

            <!-- Mock headers for now -->
            <Result />
          </b-tab>

          <b-tab title="Result1"><p>I'm Result 1</p></b-tab>
          <b-tab title="Result2"><p>I'm Result 2</p></b-tab>
          <b-tab title="Result3"><p>I'm Result 3</p></b-tab>
        </b-tabs>
      </div>
    </div>
    <div class="col-md-4 border-top-0 p-0">
      <h3 class="text-center py-2 m-0 border-bottom">Previous Results</h3>
      <!--<ul class="list-group overflow-auto" style="max-height: 500px">
        <a
          href="#"
          class="list-group-item list-group-item-action flex-column align-items-start border-0 border-bottom"
        >
          <p class="m-0"><strong>Example Title</strong></p>
          <p class="m-0">description text</p>
          <p class="m-0"><em>01-01-22</em></p>
        </a>
        <a
          href="#"
          class="list-group-item list-group-item-action flex-column align-items-start border-0 border-bottom"
        >
          <p class="m-0"><strong>Example Title</strong></p>
          <p class="m-0">description text</p>
          <p class="m-0"><em>01-01-22</em></p>
        </a>
        <a
          href="#"
          class="list-group-item list-group-item-action flex-column align-items-start border-0 border-bottom"
        >
          <p class="m-0"><strong>Example Title</strong></p>
          <p class="m-0">description text</p>
          <p class="m-0"><em>01-01-22</em></p>
        </a>
        <a
          href="#"
          class="list-group-item list-group-item-action flex-column align-items-start border-0 border-bottom"
        >
          <p class="m-0"><strong>Example Title</strong></p>
          <p class="m-0">description text</p>
          <p class="m-0"><em>01-01-22</em></p>
        </a>
        <a
          href="#"
          class="list-group-item list-group-item-action flex-column align-items-start border-0 border-bottom"
        >
          <p class="m-0"><strong>Example Title</strong></p>
          <p class="m-0">description text</p>
          <p class="m-0"><em>01-01-22</em></p>
        </a>
        <a
          href="#"
          class="list-group-item list-group-item-action flex-column align-items-start border-0 border-bottom"
        >
          <p class="m-0"><strong>Example Title</strong></p>
          <p class="m-0">description text</p>
          <p class="m-0"><em>01-01-22</em></p>
        </a>
        <a
          href="#"
          class="list-group-item list-group-item-action flex-column align-items-start border-0 border-bottom"
        >
          <p class="m-0"><strong>Example Title</strong></p>
          <p class="m-0">description text</p>
          <p class="m-0"><em>01-01-22</em></p>
        </a>
        <a
          href="#"
          class="list-group-item list-group-item-action flex-column align-items-start border-0 border-bottom"
        >
          <p class="m-0"><strong>Example Title</strong></p>
          <p class="m-0">description text</p>
          <p class="m-0"><em>01-01-22</em></p>
        </a>
        <a
          href="#"
          class="list-group-item list-group-item-action flex-column align-items-start border-0 border-bottom"
        >
          <p class="m-0"><strong>Example Title</strong></p>
          <p class="m-0">description text</p>
          <p class="m-0"><em>01-01-22</em></p>
        </a>
        <a
          href="#"
          class="list-group-item list-group-item-action flex-column align-items-start border-0 border-bottom"
        >
          <p class="m-0"><strong>Example Title</strong></p>
          <p class="m-0">description text</p>
          <p class="m-0"><em>01-01-22</em></p>
        </a>
      </ul>-->
      <PreviousResults />
    </div>
  </div>
</template>
