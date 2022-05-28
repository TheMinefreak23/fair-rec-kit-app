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
        name: capitalise(param.name),
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

function chooseLabel(name) {
  return 'Choose ' + article(name) + ' ' + underscoreToSpace(name)
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
                <b-row>
                  <template
                    v-for="(value, index) in form.main.params.values"
                    :key="value"
                  >
                    <!--Regular input-->
                    <!--The max k value is based on the amount of recommendations.
                Because of this we use a seperate setting to cover for it.-->
                    <b-col
                      :cols="
                        !value.name.includes('split')
                          ? horizontalLayout
                            ? 3
                            : 6
                          : 12
                      "
                    >
                      <b-form-group
                        :label="
                          capitalise(underscoreToSpace(value.name)) + ' *'
                        "
                        :description="
                          'Between ' +
                          value.min +
                          ' and ' +
                          (value.name.toLowerCase() == 'k'
                            ? props.maxK
                            : value.max)
                        "
                        required
                      >
                        <!--v-model="form.inputs[index].value"-->
                        <b-form-input
                          v-if="!value.name.includes('split')"
                          v-model="form.inputs[index].value"
                          :state="
                            form.inputs[index].value >= value.min &&
                            form.inputs[index].value <=
                              (value.name.toLowerCase() == 'k'
                                ? props.maxK
                                : value.max)
                          "
                          :placeholder="
                            'Enter ' + underscoreToSpace(value.name)
                          "
                          validated="true"
                        />
                        <!--Use a range slider if it's a train/test split option-->
                        <SplitRange
                          @input="form.inputs[index].value = $event"
                          v-model:value="form.inputs[index].value"
                          :min="value.min"
                          :max="value.max"
                          :name="value.name"
                          :step="5"
                        />
                        <!-- Use a slider with 2 sliders if a range is needed-->
                        <MultiRangeSlider
                          v-if="value.name.includes('range')"
                          baseClassName="multi-range-slider-black"
                          :min="value.min"
                          :max="value.max"
                          :step="1"
                          :ruler="false"
                          :label="true"
                          :minValue="value.minValue"
                          :maxValue="value.maxValue"
                          @input="
                            form.inputs[index].value = [
                              $event.minValue,
                              $event.maxValue,
                            ]
                          "
                        />
                        <!--Display the seed label for the seed option.-->
                        <div
                          v-if="
                            value.name.includes('seed') &&
                            form.inputs[index].value == null
                          "
                          class="text-center"
                        >
                          <b>Seed will be randomly generated.</b>
                        </div>
                      </b-form-group></b-col
                    >
                  </template>
                </b-row>

                <!--Selection options-->
                <b-row>
                  <b-col
                    md="auto"
                    v-for="(option, index) in form.main.params.options"
                    :key="option"
                  >
                    <!--Use a radio group if there are a few options and they aren't true/false.-->
                    <b-form-group
                      :label="chooseLabel(option.name) + ' *'"
                      v-if="
                        option.options.length < 3 &&
                        typeof option.options[0] != 'boolean'
                      "
                    >
                      <b-form-radio-group
                        v-model="form.selects[index].value"
                        text-field="name"
                        :options="option.options"
                        required
                      ></b-form-radio-group>
                    </b-form-group>
                    <!--Use a checkbox if the options are of a binary (True or False) nature.-->
                    <b-form-group
                      :label="
                        capitalise(underscoreToSpace(option.name + '?')) + ' *'
                      "
                      v-if="
                        option.options[0] == true || option.options[0] == false
                      "
                    >
                      <b-form-checkbox
                        v-model="form.selects[index].value"
                        size="lg"
                        required
                        >{{
                          form.selects[index].value ? 'Yes' : 'No'
                        }}</b-form-checkbox
                      >
                    </b-form-group>
                    <!--Use a dropdown select form otherwise-->
                    <b-form-group
                      v-if="option.options.length > 2"
                      :label="chooseLabel(option.name) + ' *'"
                    >
                      <!--TODO: ADD MULTIPLE SELECT FOR FILTERS (MODAL?)-->
                      <b-form-select
                        v-model="form.selects[index].value"
                        :options="option.options"
                        text-field="name"
                        required
                      >
                        <template #first>
                          <b-form-select-option :value="null" disabled
                            >Choose..</b-form-select-option
                          >
                        </template>
                      </b-form-select>
                    </b-form-group>
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
