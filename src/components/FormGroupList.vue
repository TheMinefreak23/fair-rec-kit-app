<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import {
  article,
  capitalise,
  underscoreToSpace,
} from '../helpers/resultFormatter'

//const emit = defineEmits(['formChange'])
const props = defineProps({
  name: String,
  plural: String,
  selectName: String,
  options: Array,
  required: Boolean,
  data: { type: Object, required: true },
})

const groupCount = ref(0)

const form = computed({
  // getter
  get() {
    //console.log(props.name, props.data)
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
  console.log(props.name, props.nested, props.options)
  form.value.name = props.plural
  //console.log(props.name, 'options', props.options)
})

watch(
  () => { // Watch for the changing of options
    return props.options
  },
  () => { // Update form if this changes
    update()
  },
  { // Make sure this does not trigger on initialization
    immediate: false,
    deep: true
  }
)

// Set default values for the group parameters.
function setParameter(i, option) {
  //console.log(props.name, props.options, form.value.main)
  //let option = form.value.main[i]
  let choices
  //console.log(option)
  //console.log(option.params)
  if (option.params) {
    if (option.params.values && option.params.values.length > 0) {
      choices = option.params.values
      form.value.inputs[i] = choices.map((param) => ({
        name: param.name,
        value: param.default,
      }))
    }
    if (option.params.options && option.params.options.length > 0) {
      choices = option.params.options
      form.value.selects[i] = choices.map((param) => ({
        name: capitalise(param.name),
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
      //console.log(form.value.lists)
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

// Check whether the option has values/options params (not dynamic params)
function hasParams(index) {
  //console.log(form.value.main)
  const option = form.value.main[index]
  //console.log('hasParams option at', index, ':', option)
  return (
    option &&
    option.params &&
    option.params.length != 0 &&
    ((option.params.values && option.params.values.length != 0) ||
      (option.params.options && option.params.options.length != 0))
  )
}

// Check whether the option has dynamic params
function hasDynamic(index) {
  // TODO refactor with hasParams
  const option = form.value.main[index]
  return (
    option &&
    option.params &&
    option.params.length != 0 &&
    option.params.dynamic &&
    option.params.dynamic.length != 0
  )
}

function chooseLabel(name) {
  return 'Choose ' + article(name) + ' ' + underscoreToSpace(name)
}

// Copies the selected item and puts it at the end of the list
function copyItem(i) {
  groupCount.value++ //Add a new item
  form.value.main[groupCount.value - 1] = form.value.main[i] //Copy the selected value to the new item
  
  if (form.value.inputs[i]) { //Copy textfield options (if applicable)
    form.value.inputs[groupCount.value - 1] = form.value.inputs[i].map(
      (param) => ({
        name: param.name,
        value: param.value,
      })
    )
  }
  if (form.value.selects[i]) { //Copy select options (if applicable)
    form.value.selects[groupCount.value - 1] = form.value.selects[i].map(
      (param) => ({
        name: param.name,
        value: param.value,
      })
    )
  }
  if (form.value.lists[i]) { //Copy nested option list (if applicable)
    form.value.lists[groupCount.value - 1] = form.value.lists[i].map(
      (param) => ({
        name: param.name,
        value: param.value,
      })
    )
  }
}
//Update the options that cannot be be submitted due to changing experiment type (
function update() {
  let entries = flattenOptions().map((entry) => entry.text)
  for (let i = 0; i < form.value.main.length; i++) {
    if (!entries.includes(form.value.main[i])) {
      //every entry that does not exist in the list of option should be removed
      //Non-existing entries are replaced with a null entry
      form.value.main.splice(i, 1, null)
      form.value.selects.splice(i, 1, null)
      form.value.inputs.splice(i, 1, null)
      form.value.lists.splice(i, 1, null)
    }
  }
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
                  text-field="name"
                  @change="setParameter(i - 1, $event)"
                  :required="required"
                >
                  <template #first>
                    <b-form-select-option value="" disabled
                      >Choose..</b-form-select-option
                    >
                  </template>
                </b-form-select>
              </b-form-group>
            </b-col>

            <!--Show settings for selected option.-->
            <b-col cols="4" v-if="hasParams(i - 1)">
              <!--Use an input form for values.-->
              <template
                v-for="(value, index) in form.main[i - 1].params.values"
                :key="value"
              >
                <b-form-group
                  :label="capitalise(underscoreToSpace(value.name))"
                  :description="'Between ' + value.min + ' and ' + value.max"
                >
                  <b-form-input
                    v-if="!value.name.includes('split')"
                    v-model="form.inputs[i - 1][index].value"
                    :state="
                      form.inputs[i - 1][index].value >= value.min &&
                      form.inputs[i - 1][index].value <= value.max
                    "
                    validated="true"
                  />
                  <b-form-input
                    v-if="value.name.includes('Train')"
                    type="range"
                    min="value.min"
                    max="value.max"
                    step="5"
                    id="customRange"
                    v-model="form.inputs[i - 1][index].value"
                  ></b-form-input>
                  <div v-if="value.name.includes('Train')" class="text-center">
                    <strong>Train:</strong>
                    <i>{{ ' ' + form.inputs[i - 1][index].value + ' ' }}</i>
                    <strong>Test:</strong
                    ><i>{{ ' ' }}{{ 100 - form.inputs[i - 1][index].value }}</i>
                  </div>
                  <div
                    v-if="
                      value.name.includes('seed') &&
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
                  :label="chooseLabel(option.name)"
                  v-if="
                    option.options.length < 3 &&
                    typeof option.options[0] != 'boolean'
                  "
                >
                  <b-form-radio-group
                    v-model="form.selects[i - 1][index].value"
                    text-field="name"
                    :value="option.default"
                    :options="option.options"
                    required
                  ></b-form-radio-group>
                </b-form-group>
                <b-form-group
                  :label="capitalise(underscoreToSpace(option.name + '?'))"
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
                  :label="chooseLabel(option.name)"
                >
                  <b-form-select
                    v-model="form.selects[i - 1][index].value"
                    :options="option.options"
                    text-field="name"
                    required
                  >
                    <template #first>
                      <b-form-select-option value="" disabled
                        >Choose..</b-form-select-option
                      >
                    </template>
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
          <b-row v-if="hasDynamic(i - 1)">
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
