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
  //console.log(props.options)
  //console.log(form.value.main)
  //console.log(form.value.main[i])
  return props.options.find((option) => option.name === form.value.main[i])
}

function removeGroup(i) {
  if (groupCount.value != 1) {
    groupCount.value--
  }
  form.value.main.splice(i, 1)
  form.value.inputs.splice(i, 1)
  form.value.selects.splice(i, 1)
}
</script>

<template>
  <div>
    <!--Capitalise the title.-->
    <h2>{{ plural.charAt(0).toUpperCase() + plural.slice(1) }}</h2>
    <div v-for="i in groupCount" :key="i - 1">
      <b-row>
        <b-col>
          <b-form-group :label="'Select ' + selectName">
            <b-form-select
              v-model="form.main[i - 1]"
              :options="[
                { text: 'Choose...', value: null },
                ...options.map((x) => x.name),
              ]"
              @change="setParameter(i - 1, $event), $emit('formChange', form)"
              required
              ><!--TODO use placeholder-->
            </b-form-select>
          </b-form-group>
        </b-col>

        <!--Show settings for selected option.-->
        <b-col v-if="form.main[i - 1] != null">
          <!--Use an input form for values.-->
          <template v-for="(value, index) in getFromIndex(i - 1).params.values">
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
                v-model="form.inputs[i - 1]"
                required
                :state="
                  form.inputs[i - 1] >= value.min &&
                  form.inputs[i - 1] <= value.max
                "
                @input="$emit('formChange', form)"
                validated="true"
              ></b-form-input>
            </b-form-group>
          </template>

          <!--Use a select form for options.-->
          <template
            v-for="(option, index) in getFromIndex(i - 1).params.options"
          >
            <b-form-select
              :label="'Choose a ' + option.name"
              v-model="form.selects[i - 1]"
              :options="[{ text: 'Choose...', value: null }, ...option.options]"
              @input="$emit('formChange', form)"
              required
              ><!--TODO use placeholder-->
            </b-form-select>
          </template>
        </b-col>
        <b-col>
          <b-button
            v-if="i != 1"
            @click="removeGroup(i - 1)"
            variant="danger"
            class="mb-2 mr-sm-2 mb-sm-0"
            >X</b-button
          >
        </b-col>
      </b-row>
    </div>

    <b-button @click="groupCount++">Add {{ name }}...</b-button>
  </div>
</template>
