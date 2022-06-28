<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

const options = [{ text: 'foo', value: 'bar' }]
</script>

<template>
  <b-card>
    <h3>test select</h3>
    <b-form>
      <b-form-group label="Select">
        <b-form-select :options="options" data-testid="select"></b-form-select>
      </b-form-group>
      <b-form-group label="Input">
        <b-form-input></b-form-input>
      </b-form-group>
    </b-form>
  </b-card>
</template>
