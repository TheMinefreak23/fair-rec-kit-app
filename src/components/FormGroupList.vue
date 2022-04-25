<script setup>
import { computed, onMounted, ref } from 'vue'
import { capitalise } from '../helpers/resultFormatter'
import { underscoreToSpace } from '../helpers/resultFormatter'
import { emptyOption, selectionOptions } from '../helpers/optionsFormatter'

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

const groupCount = ref(0)

const form = computed({
  // getter
  get() {
    //console.log(props.data)
    return props.data
  },
  // setter
  set(localValue) {
    console.log('local form change to', localValue)
    emit('input', localValue)
  },
})
//const flatOptions = props.nested ? flattenOptions() : props.options

onMounted(() => {
  groupCount.value = props.required ? 1 : 0 // For required lists the minimum amount of group items is 1.
  form.value.name = props.plural
  console.log(props.name, 'options', props.options)
  /*console.log('type of options', typeof props.options)
  console.log('nested', props.nested)
  console.log(form.value)*/
})

// Set default values for the group parameters.
function setParameter(i, option) {
  //console.log(flatOptions)
  console.log(props.name, props.options, form.value.main)
  //let option = form.value.main[i]
  let choices
  console.log(option)
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
    if (option.params.dynamic && option.params.dynamic.length > 0) {
      choices = option.params.dynamic
      // TODO refactor empty form group function
      form.value.lists[i] = choices.map(() => ({
        main: [],
        inputs: [],
        selects: [],
        lists: [],
      }))
      console.log(form.value.lists)
    }
  }
}

// Splice groups array to remove a group
function removeGroup(i) {
  if (props.required && groupCount.value == 1) return
  groupCount.value--
  form.value.main.splice(i, 1)
  form.value.inputs.splice(i, 1)
  form.value.selects.splice(i, 1)
  form.value.lists.splice(i, 1)
}

/*// Flatten options API structure
function flattenOptions() {
  return props.options
    .map((category) => category.options)
    .concat()
    .flat()
}*/

// Check whether the choice has options
function hasParams(index) {
  console.log(form.value.main)
  const option = form.value.main[index]
  console.log('hasParams option at', index, ':', option)
  return (
    option &&
    option.params &&
    option.params.length != 0 &&
    ((option.params.values && option.params.values.length != 0) ||
      (option.params.options && option.params.options.length != 0) ||
      (option.params.dynamic && option.params.dynamic.length != 0))
  )
}
</script>

<template>
  <div>
    <h3 class="text-center">
      <!--Capitalise the title.-->
      {{ capitalise(plural) }}
      <!--{{ plural }}-->
    </h3>
    <div v-for="i in groupCount" :key="i - 1">
      <b-row class="align-items-end">
        <b-col>
          <b-row>
            <b-col cols="4">
              <b-form-group :label="'Select ' + selectName">
                <!--TODO use form bind instead of emit?-->
                <b-form-select
                  :form="name"
                  v-model="form.main[i - 1]"
                  :options="options"
                  value-field="value"
                  text-field="text"
                  @change="setParameter(i - 1, $event)"
                  :required="required"
                >
                  <template #first>
                    <b-form-select-option value="" disabled
                      >Choose..</b-form-select-option
                    >
                  </template>
                </b-form-select>
                <!--TODO use placeholder-->
              </b-form-group>
              <h3>i: {{ i }}</h3>
              <h3>main: {{ form.main[i - 1] && form.main[i - 1].text }}</h3>
              <h3>input: {{ form.inputs[i - 1] && form.inputs[i - 1] }}</h3>
              <h3>select: {{ form.selects[i - 1] && form.selects[i - 1] }}</h3>
              <!--<h4>main params values: {{ form.main[i - 1].params.values }}</h4>-->
            </b-col>

            <!--Show settings for selected option.-->
            <b-col cols="4" v-if="hasParams(i - 1)">
              <!--Use an input form for values.-->
              <template
                v-for="(value, index) in form.main[i - 1].params.values"
                :key="value"
              >
                <h2>value</h2>
                <b-form-group
                  :label="
                    underscoreToSpace(value.text) +
                    ' between ' +
                    value.min +
                    ' and ' +
                    value.max
                  "
                >
                  <b-form-input
                    v-if="!value.text.includes('split')"
                    v-model="form.inputs[i - 1][index].value"
                    :state="
                      form.inputs[i - 1][index].value >= value.min &&
                      form.inputs[i - 1][index].value <= value.max
                    "
                    validated="true"
                  />
                  <b-form-input
                    v-if="value.text.includes('Train')"
                    type="range"
                    min="value.min"
                    max="value.max"
                    step="5"
                    id="customRange"
                    v-model="form.inputs[i - 1][index].value"
                  ></b-form-input>
                  <div v-if="value.text.includes('Train')" class="text-center">
                    <strong>Train:</strong>
                    <i>{{ ' ' + form.inputs[i - 1][index].value + ' ' }}</i>
                    <strong>Test:</strong
                    ><i>{{ ' ' }}{{ 100 - form.inputs[i - 1][index].value }}</i>
                  </div>
                  <div
                    v-if="
                      value.text.includes('seed') &&
                      form.inputs[i - 1][index].value == null
                    "
                    class="text-center"
                  >
                    Seed will be randomly generated.
                  </div>
                </b-form-group>
              </template>

              <!--Use a select form for options.-->
              <template
                v-for="(option, index) in form.main[i - 1].params.options"
                :key="option"
              >
                <b-form-group
                  :label="'Choose a ' + underscoreToSpace(option.text)"
                  v-if="
                    option.options.length < 3 &&
                    typeof option.options[0] != 'boolean'
                  "
                >
                  <b-form-radio-group
                    v-model="form.selects[i - 1][index].value"
                    :value="option.default"
                    :options="option.options"
                    required
                  ></b-form-radio-group>
                </b-form-group>
                <b-form-group
                  :label="capitalise(underscoreToSpace(option.text + '?'))"
                  v-if="option.options[0] == true || option.options[0] == false"
                >
                  <b-form-checkbox
                    v-model="form.selects[i - 1][index].value"
                    checked="option.default"
                    size="lg"
                    required
                    >{{
                      form.selects[i - 1][index].value ? 'Yes' : 'No'
                    }}</b-form-checkbox
                  >
                </b-form-group>
                <b-form-group
                  v-if="option.options.length > 2"
                  :label="'Choose a ' + underscoreToSpace(option.text)"
                >
                  <b-form-select
                    v-model="form.selects[i - 1][index].value"
                    :options="selectionOptions(option.options)"
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
                  v-if="!(i == 1 && required)"
                  @click="removeGroup(i - 1)"
                  variant="danger"
                  class="mb-2 mr-sm-2 mb-sm-0"
                  >X</b-button
                >
              </b-form-group>
            </b-col>
          </b-row>
          <b-row v-if="hasParams(i - 1)">
            <!--Nested form group list.-->
            <template
              v-for="(option, index) in form.main[i - 1].params.dynamic"
              :key="option"
            >
              <b-card>
                <FormGroupList
                  v-model:data="form.lists[i - 1][index]"
                  :name="option.name"
                  :plural="option.plural"
                  :selectName="option.article + ' ' + option.name"
                  :options="option.options"
                  :nested="option.nested"
                  :required="false"
                />
              </b-card>
            </template>
          </b-row>
        </b-col>
      </b-row>
    </div>

    <b-button @click="groupCount++" align-v="end" variant="primary"
      >Add {{ name }}...</b-button
    >
  </div>
</template>
