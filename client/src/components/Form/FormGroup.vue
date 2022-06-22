<script setup>
/* A form option */
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */
import FormGroupList from './FormGroupList.vue'
import { computed, onMounted, watch } from 'vue'
import { article } from '../../helpers/resultFormatter'
import { emptyFormGroup, formatDefault } from '../../helpers/optionsFormatter'
import '../../../node_modules/multi-range-slider-vue/MultiRangeSliderBlack.css'
import FormInput from './FormInput.vue'
import FormSelect from './FormSelect.vue'

const emit = defineEmits(['copy', 'scroll', 'update:modelValue'])
const props = defineProps({
  groupId: String, // The group ID for scrolling
  index: Number, // The group index for scrolling
  name: String, // The name of the group for usage in the buttons
  title: String, // The title of the group for usage in the header
  options: Array, // The available options to choose from
  required: Boolean, // WHether the group option is required
  defaultOption: String, // The default main option
  maxK: Number, // The amount of  recommendations (caps K)
  datasets: Object, // The chosen datasets (for filters)
  modelValue: { type: Object, required: true }, // The local form linked to the form component
  single: { type: Boolean, default: false }, // single form group or multi (form group list)
})

/**
 * Form per group
 */
const form = computed({
  // getter
  get() {
    // console.log(props.name, props.data)
    return props.modelValue
  },
  // setter
  set(localValue) {
    console.log('local form change to', localValue)
    emit('update:modelValue', localValue)
  },
})

/**
 * Initialise form values: single, name and default option.
 */
onMounted(() => {
  // Reset main option (TODO temporary measure for changing options prop)
  if (form.value.main) {
    console.log(props.title, form.value.main)
    form.value.main = ''
  }
  form.value.single = props.single
  form.value.name = props.title
  if (props.defaultOption) {
    form.value.main = props.defaultOption.value
  }
  // If there is only one option (no main selection), use it as the default
  if (props.options.length === 1) form.value.main = props.options[0].value
  // console.log('form', form.value)
})

/**
 * Set the parameter defaults when the main option changes.
 */
watch(
  () => form.value.main,
  () => {
    // Whether the form options have already been set.
    if (!(form.value.values || form.value.options || form.value.lists)) {
      if (form.value.main) setParameterDefaults()
    }
  }
)

/**
 * Set the parameter defaults when the main option changes.
 */
watch(
  () => props.options,
  () => {
    // Reset main option (TODO temporary measure for changing options prop)
    if (props.name === 'metric' && form.value.main) {
      // console.log(props.name, form.value.main)
      form.value.main = ''
    }
  }
)

/**
 * Cap metrics K values to the recommendation amount.
 */
watch(
  () =>
    // Watch for the changing of max K (recommendations) value.
    props.maxK,
  (newK, oldK) => {
    if (!form.value.inputs) return
    for (const input of form.value.inputs) {
      if (
        (!input.value || input.value === oldK) &&
        input.name.toLowerCase() === 'k'
      ) {
        input.value = newK
      }
    }
  }
)

/**
 * Set default values for the group parameters.
 */
function setParameterDefaults() {
  const option = form.value.main
  let choices
  // Only set defaults if the form hasn't been set (when copying)
  if (option.params) {
    // console.log('option', props.name, option.name, 'params', option.params)
    if (option.params.values && option.params.values.length > 0) {
      choices = option.params.values
      // console.log('choices', choices)
      form.value.inputs = choices.map((param) => ({
        name: param.name,
        value: param.name.toLowerCase() === 'k' ? props.maxK : param.default,
      }))
    }
    if (option.params.options && option.params.options.length > 0) {
      choices = option.params.options
      form.value.selects = choices.map((param) => ({
        name: param.name,
        value: formatDefault(param.default),
      }))
    }
    // console.log('selects', form.value.selects)
    if (option.params.dynamic && option.params.dynamic.length > 0) {
      choices = option.params.dynamic
      // Sublists are not required TODO maybe some are?
      form.value.lists = choices.map(() => emptyFormGroup(false))
    }
  }
}

/**
 * Check whether the option has parameters
 */
function hasParams() {
  const option = form.value.main
  // console.log('hasParams option at', index, ':', option)
  return option && option.params
}
</script>

<template>
  <template v-if="options && options.length === 0">
    <h4>No options available!</h4>
    <h4 v-if="title === 'matrix'">Please select a dataset and matrix.</h4>
  </template>
  <b-row v-else class="align-items-end">
    <b-col>
      <b-col>
        <b-row>
          <b-col>
            <b-row>
              <!--Main option selection-->
              <b-col cols="12">
                <h4 v-if="props.name === 'metric'">
                  NOTE: resets when changing dataset
                </h4>
                <b-form-group
                  :label="
                    props.options.length > 1
                      ? 'Select ' + article(name) + ' ' + name + ' *'
                      : form.main && name + ': ' + form.main.name
                  "
                >
                  <!-- If there is only one main option available, don't use a main selection-->
                  <b-form-select
                    v-if="options.length > 1"
                    :class="blink ? 'subtle-blink' : ''"
                    v-model="form.main"
                    data-testid="main-select"
                    :options="options"
                    text-field="name"
                    :required="required"
                  >
                    <template #first>
                      <b-form-select-option
                        :value="''"
                        data-testid="main-option"
                        >Choose..</b-form-select-option
                      >
                    </template>
                  </b-form-select>
                  <b-button
                    v-if="!single && form.main"
                    @click="$emit('copy')"
                    variant="primary"
                    >Copy {{ name }}...</b-button
                  >
                  <!--<template #first>
                    <b-form-select-option value="" disabled
                      >Choose..</b-form-select-option
                    >
                  </template>-->
                </b-form-group>
              </b-col>
              <!--Show settings for selected option.-->
              <b-col v-if="hasParams()">
                <!--Value input options.-->
                <b-row v-if="form.main.params.values">
                  <FormInput
                    v-for="(value, index) in form.main.params.values"
                    :key="value"
                    :value="value"
                    v-model="form.inputs[index]"
                    :maxK="maxK"
                  />
                </b-row>

                <!--Selection options-->
                <b-row v-if="form.main.params.options">
                  <b-col
                    md="auto"
                    v-for="(option, index) in form.main.params.options"
                    :key="option"
                  >
                    <FormSelect
                      :option="option"
                      v-model="form.selects[index]"
                    />
                  </b-col>
                </b-row>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
        <!--Dynamic lists-->
        <b-col v-if="hasParams()">
          <!--Nested form group list.-->
          <b-card
            class="mb-1 bg-secondary"
            v-for="(option, index) in form.main.params.dynamic"
            :key="option"
          >
            <!-- Make a form group or list depending on the type -->
            <FormGroup
              v-if="option.single"
              single
              v-model="form.lists[index].choices[0]"
              :groupId="
                (groupId ? groupId : name) +
                ' ' +
                props.index +
                ' ' +
                option.name
              "
              :name="form.main.name + ' ' + option.name"
              :index="index"
              :title="option.title"
              :options="option.options"
              :defaultOption="option.default"
              :required="option.required"
            />
            <FormGroupList
              v-else
              v-model="form.lists[index]"
              :groupId="
                (groupId ? groupId : name) +
                ' ' +
                props.index +
                ' ' +
                option.name
              "
              :name="form.main.name + ' ' + option.name"
              :index="index"
              :title="option.title"
              :description="name + ' ' + option.title"
              :options="option.options"
              :defaultOption="option.default"
              :required="false"
            />
          </b-card>
        </b-col>
      </b-col>
    </b-col>
  </b-row>
</template>
