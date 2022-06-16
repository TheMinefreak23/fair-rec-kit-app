<script setup>
/* Display a dictionary in a human-readable way */
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

const props = defineProps({
  dict: Object, // The dictionary to display
  alternateBg: Boolean, // TODO use Whether to alternate the background
})

/**
 * Format the dictionary
 */
function format() {
  const formatted = props.dict
  if ('name' in props.dict) {
    formatted[props.dict.name] = props.dict.params
  }
  delete formatted.name
  delete formatted.params
  return formatted
}
</script>

<template>
  <b-col
    md="auto"
    cols="2"
    v-for="[key, value] in Object.entries(format(dict))"
  >
    <!-- Don't show empty option lists -->
    <b-card
      v-if="!Array.isArray(value) || value.length > 0"
      :header-bg-variant="alternateBg ? 'secondary' : 'dark'"
      :header-text-variant="alternateBg ? 'black' : 'white'"
      :header="key"
      class="text-center pt-1 mt-1"
    >
      <b-col>
        <!-- Loop if the value is an array -->
        <template v-if="value && Array.isArray(value)">
          <b-card v-for="(val, index) in value" 
            :header-bg-variant="!alternateBg ? 'secondary' : 'dark'"
            :header-text-variant="!alternateBg ? 'black' : 'white'"
            :header="'#' + (parseInt(index) + 1)"
            class="text-center pt-1 mt-1"
          >
            <DictionaryDisplay
              :dict="val"
              :alternateBg="alternateBg"
          /></b-card>
        </template>
        <!-- Display the value using a display if it's an object -->
        <template v-else>
          <DictionaryDisplay
            v-if="value && typeof value == 'object'"
            :dict="value"
            :alternateBg="!alternateBg"
          />
          <!-- TODO Decide between these two implementations-->
          <template v-else-if="key == 'test_ratio'">
            {{ (1 - value) * 100 }}/{{ value * 100 }}
          </template>
          <template v-else-if="key == 'Train/testsplit'">
            {{ value }}/{{ 100 - value }}
          </template>
          <template v-else>
            <!-- <b-button disabled>{{ value ? value : 'None' }}</b-button> -->
            {{ value ? value : 'None' }}
          </template>
        </template>
      </b-col>
    </b-card>
  </b-col>
</template>
