<script setup>
import { ref } from 'vue'
const emit = defineEmits(['formChange'])
const props = defineProps({
  name: String,
  plural: String,
  selectName: String,
  options: Array,
})

const groupCount = ref(1) //The minimum amount of group items is 1.
const form = ref({ main: [], inputs: [], selects: [] })

// Set default values for the group parameters.
function setParameter(i, val) {
  let option = props.options.find((option) => option.name === val)
  if (option.params) {
    if (option.params.values && option.params.values.length > 0)
      form.value.inputs[i] = option.params.values[0].default

    if (option.params.options && option.params.options.length > 0)
      form.value.selects[i] = option.params.options[0].default
  }
}

function getFromIndex(i) {
  console.log(props.options)
  console.log(form.value.main)
  //console.log(form.value.main[i])
  return props.options.find((option) => option.name === form.value.main[i])
}
</script>

<template>
  <div>
    <!--Capitalise the title.-->
    <h2>{{ plural.charAt(0).toUpperCase() + plural.slice(1) }}</h2>
    <b-form-group
      v-for="i in groupCount"
      :label="'Select ' + selectName"
      :key="i"
    >
      <b-form-select
        v-model="form.main[i]"
        :options="[
          { text: 'Choose...', value: null },
          ...options.map((x) => x.name),
        ]"
        @change="setParameter(i, $event), $emit('formChange', form, plural)"
        required
        ><!--TODO use placeholder-->
      </b-form-select>

      <!--Show settings for selected option.-->
      <div v-if="form.main[i] != null">
        <!--Use an input form for values.-->
        <template v-for="(value, index) in getFromIndex(i).params.values">
          <b-form-group
            :label="
              'Give a ' +
              value.name +
              ' between ' +
              value.min +
              ' and ' +
              value.max
            "
          >
            <b-form-input
              v-model="form.inputs[i]"
              required
              :state="
                form.inputs[i] >= value.min && form.inputs[i] <= value.max
              "
              @input="$emit('formChange', form, plural)"
              validated="true"
            ></b-form-input>
          </b-form-group>
        </template>

        <!--Use a select form for options.-->
        <template v-for="(option, index) in getFromIndex(i).params.options">
          <b-form-select
            :label="'Choose a ' + option.name"
            v-model="form.selects[i]"
            :options="[{ text: 'Choose...', value: null }, ...option.options]"
            @input="$emit('formChange', form, plural)"
            required
            ><!--TODO use placeholder-->
          </b-form-select>
        </template>
      </div>
    </b-form-group>

    <b-button @click="groupCount++">Add {{ name }}...</b-button>
    <b-button @click="groupCount--" variant="danger"
      >Remove {{ name }}</b-button
    >
  </div>
</template>
