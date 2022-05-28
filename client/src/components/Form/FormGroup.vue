<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
import FormGroupList from './FormGroupList.vue'
import { computed, onMounted, ref, watch } from 'vue'
import {
  article,
  capitalise,
  underscoreToSpace,
  formatMultipleItems,
} from '../../helpers/resultFormatter'
//import { selectionOptions } from '../helpers/optionsFormatter'
import SplitRange from './SplitRange.vue'
import { emptyFormGroup } from '../../helpers/optionsFormatter'
import MultiRangeSlider from 'multi-range-slider-vue'
import '../../../node_modules/multi-range-slider-vue/MultiRangeSliderBlack.css'
import FormInput from './FormInput.vue'
import FormSelect from './FormSelect.vue'

const emit = defineEmits(['copy'])
const props = defineProps({
  name: String,
  title: String,
  options: Array,
  required: Boolean,
  defaultOption: String,
  maxK: Number,
  horizontalLayout: Boolean,
  data: { type: Object, required: true },
  single: { type: Boolean, default: false }, // single form group or multi (form group list)
})

onMounted(() => {
  form.value.single = props.single
  form.value.name = props.title
  if (props.defaultOption) {
    form.value.main = props.defaultOption.value
  }
  //console.log('form', form.value)
})

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

watch(
  () => form.value.main,
  (newMain) => {
    setParameter(newMain)
    //console.log('form', form.value)
  }
)

watch(
  () =>
    // Watch for the changing of max K (recommendations) value
    props.maxK,
  (newK, oldK) => {
    if (!form.value.inputs) return
    for (const input of form.value.inputs) {
      if (
        (!input.value || input.value == oldK) &&
        input.name.toLowerCase() == 'k'
      ) {
        input.value = newK
      }
    }
  }
)

// Set default values for the group parameters.
function setParameter(option) {
  //console.log('setting parameter', props.name, props.options, form.value.main)
  let choices
  //console.log(option)
  if (option.params) {
    //console.log('option', props.name, option.name, 'params', option.params)
    if (option.params.values && option.params.values.length > 0) {
      choices = option.params.values
      form.value.inputs = choices.map((param) => ({
        name: param.name,
        value: param.name.toLowerCase() == 'k' ? props.maxK : param.default,
      }))
    }
    if (option.params.options && option.params.options.length > 0) {
      choices = option.params.options
      form.value.selects = choices.map((param) => ({
        name: param.name,
        value: param.default,
      }))
    }
    if (option.params.dynamic && option.params.dynamic.length > 0) {
      choices = option.params.dynamic
      // Sublists are not required TODO maybe some are?
      form.value.lists = choices.map(() => emptyFormGroup(false))
    }
  }
}

// Check whether the option has values/options params (not dynamic params)
function hasParams() {
  const option = form.value.main
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
function hasDynamic() {
  //console.log('form main', form.value.main)
  // TODO refactor with hasParams
  const option = form.value.main
  return (
    option &&
    option.params &&
    option.params.length != 0 &&
    option.params.dynamic &&
    option.params.dynamic.length != 0
  )
}
</script>

<template>
  <b-row class="align-items-end">
    <b-col>
      <b-col>
        <b-row>
          <b-col>
            <b-row>
              <!--Main option selection-->
              <b-col cols="12">
                <b-form-group
                  :label="'Select ' + article(name) + ' ' + name + ' *'"
                >
                  <b-form-select
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
                  <template #first>
                    <b-form-select-option value="" disabled
                      >Choose..</b-form-select-option
                    >
                  </template>
                </b-form-group>
              </b-col>
              <!--Show settings for selected option.-->
              <b-col v-if="hasParams()">
                <!--Value input options.-->
                <b-row v-if="form.main.params.values">
                  <template
                    v-for="(value, index) in form.main.params.values"
                    :key="value"
                  >
                    <FormInput
                      :value="value"
                      v-model:formValue="form.inputs[index]"
                      :maxK="maxK"
                    />
                  </template>
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
                      v-model:formValue="form.selects[index]"
                    />
                  </b-col>
                </b-row>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
        <!--Dynamic lists-->
        <b-col v-if="hasDynamic()">
          <!--Nested form group list.-->
          <template
            v-for="(option, index) in form.main.params.dynamic"
            :key="option"
          >
            <b-card class="mb-1 bg-secondary">
              <!-- Make a form group or list depending on the type -->
              <FormGroup
                v-if="option.single"
                single
                v-model:data="form.lists[index].choices[0]"
                :name="option.name"
                :title="option.title"
                :options="option.options"
                :defaultOption="option.default"
                :required="option.required"
              />
              <FormGroupList
                v-else
                v-model:data="form.lists[index]"
                :name="option.name"
                :title="option.title"
                :description="
                  option.title + ' for ' + name + ' ' + form.main.name
                "
                :options="option.options"
                :defaultOption="option.default"
                :required="false"
              />
            </b-card>
          </template>
        </b-col>
      </b-col>
    </b-col>
  </b-row>
</template>
