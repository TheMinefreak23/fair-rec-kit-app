<script setup>
import { computed, ref } from 'vue'
//const emit = defineEmits(['formChange'])
const props = defineProps({
  name: String,
  plural: String,
  selectName: String,
  options: Array,
  required: Boolean,
  nested: false,
  data: { type: Object, required: true },
})

const groupCount = ref(1) //The minimum amount of group items is 1.
const form = computed({
  // getter
  get() {
    //console.log(props.data)
    return props.data
  },
  // setter
  set(localValue) {
    emit('input', localValue)
    //console.log('local form change')
  },
})
const flatOptions = props.nested ? flattenOptions() : props.options

// Set default values for the group parameters.
function setParameter(i, val) {
  console.log(flatOptions)
  //console.log(options)
  let option = flatOptions.find((option) => option.text === val)
  let choices
  console.log(option.params)
  if (option.params) {
    if (option.params.values && option.params.values.length > 0) {
      choices = option.params.values
      form.value.inputs[i] = choices.map((param) => ({
        name: param.text,
        value: param.default,
      }))
    }

    if (option.params.options && option.params.options.length > 0) {
      choices = option.params.options
      form.value.selects[i] = choices.map((param) => ({
        name: param.text,
        value: param.default,
      }))
    }
  }
}

// Get options from group index
function getFromIndex(i) {
  console.log(props.options)
  console.log(form.value.main[i])

  const option = flatOptions.find(
    (option) => option.text === form.value.main[i]
  )
  console.log(option)
  return option
}

// Splice groups array to remove a group
function removeGroup(i) {
  if (groupCount.value != 1) {
    groupCount.value--
  }
  form.value.main.splice(i, 1)
  form.value.inputs.splice(i, 1)
  form.value.selects.splice(i, 1)
}

// Flatten options API structure
function flattenOptions() {
  /*const options = []
  console.log(props.options)
  for (let api of props.options) options = [...options, ...api.options.keys()]
  return options*/

  return props.options
    .map((api) => api.options)
    .concat()
    .flat()
}
</script>

<template>
  <div>
    <!--Capitalise the title.-->
    <h3 class="text-center">{{ plural.charAt(0).toUpperCase() + plural.slice(1) }}</h3>
    <div v-for="i in groupCount" :key="i - 1">
      <b-row class="align-items-end">
        <b-col cols="4">
          <b-form-group :label="'Select ' + selectName">
            <b-form-select
              v-model="form.main[i - 1]"
              :options="[
                { text: 'Choose...', value: null },
                //...options.map((x) => x.name),
                ...options,
              ]"
              @change="setParameter(i - 1, $event)"
              :required="props.required"
            >
              <!--TODO use placeholder-->
            </b-form-select>
          </b-form-group>
        </b-col>

        <!--Show settings for selected option.-->
        <b-col
          cols="4"
          v-if="
            form.main[i - 1] != null && getFromIndex(i - 1).params.length != 0
          "
        >
          <!--Use an input form for values.-->
          <template
            v-for="(value, index) in getFromIndex(i - 1).params.values"
            :key="value"
          >
            <b-form-group
              :label="
                'Give a ' +
                value.text +
                ' between ' +
                value.min +
                ' and ' +
                value.max
              "
            >
              <b-form-input
                v-model="form.inputs[i - 1][index].value"
                required
                :state="
                  form.inputs[i - 1][index].value >= value.min &&
                  form.inputs[i - 1][index].value <= value.max
                "
                validated="true"
              ></b-form-input>
            </b-form-group>
          </template>

          <!--Use a select form for options.-->
          <template
            v-for="(option, index) in getFromIndex(i - 1).params.options"
            :key="option"
          >
            <b-form-group :label="'Choose a ' + option.text">
              <b-form-select
                v-model="form.selects[i - 1][index].value"
                :options="[
                  { text: 'Choose...', value: null },
                  ...option.options,
                ]"
                required
              >
                <!--TODO use placeholder-->
              </b-form-select>
            </b-form-group>
          </template>
        </b-col>
        <b-col cols="4">
          <b-form-group>
            <b-button
              v-if="i != 1"
              @click="removeGroup(i - 1)"
              variant="danger"
              class="mb-2 mr-sm-2 mb-sm-0"
              >X</b-button
            >
          </b-form-group>
        </b-col>
      </b-row>
    </div>

    <b-button @click="groupCount++" align-v="end">Add {{ name }}...</b-button>
  </div>
</template>
