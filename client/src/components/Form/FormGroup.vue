<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */
import FormGroupList from './FormGroupList.vue'
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { article, capitalise } from '../../helpers/resultFormatter'
import { emptyFormGroup } from '../../helpers/optionsFormatter'
import '../../../node_modules/multi-range-slider-vue/MultiRangeSliderBlack.css'
import FormInput from './FormInput.vue'
import FormSelect from './FormSelect.vue'

const emit = defineEmits(['copy', 'scroll', 'update:modelValue'])
const props = defineProps({
  index: Number, // group index for scrolling
  name: String,
  title: String,
  options: Array,
  required: Boolean,
  defaultOption: String,
  maxK: Number,
  modelValue: { type: Object, required: true },
  single: { type: Boolean, default: false }, // single form group or multi (form group list)
})

const blink = ref(false) // whether items should blink

onMounted(() => {
  form.value.single = props.single
  form.value.name = props.title
  if (props.defaultOption) {
    form.value.main = props.defaultOption.value
  }
  // console.log('form', form.value)
  // scroll to new group

  // Make new group blink
  // TODO multiple usage, refactor to function/composable?
  blink.value = true
  const timeoutMs = 1500
  setTimeout(() => {
    blink.value = false
  }, timeoutMs)

  // console.log(`#group-${props.name.split()[0]}-${props.index}`)
  // TODO refactor to ID function?
  const element = document.querySelector(
    `#group-${props.name.split()[0]}-${props.index}`
  )
  // console.log(element)
  if (element) element.scrollIntoView({ behavior: 'smooth' })
})

onUnmounted(() => {
  // console.log(props.index)
  const element = document.querySelector(`#group-${props.index - 1}`)
  // console.log(element)
  if (element) element.scrollIntoView({ behavior: 'smooth' })
})

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

watch(
  () => form.value.main,
  () => {
    // console.log('form', form.value)
    setParameter()
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
        (!input.value || input.value === oldK) &&
        input.name.toLowerCase() === 'k'
      ) {
        input.value = newK
      }
    }
  }
)

// Set default values for the group parameters.
function setParameter() {
  const option = form.value.main
  // console.log('setting parameter', props.name, props.options, form.value.main)
  let choices
  // console.log(option)
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
        value: param.default,
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

// Check whether the option has values/options params (not dynamic params)
function hasParams() {
  const option = form.value.main
  // console.log('hasParams option at', index, ':', option)
  return option && option.params
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
              :name="option.name"
              :title="option.title"
              :options="option.options"
              :defaultOption="option.default"
              :required="option.required"
            />
            <FormGroupList
              v-else
              v-model="form.lists[index]"
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
        </b-col>
      </b-col>
    </b-col>
  </b-row>
</template>

<style>
.subtle-blink {
  animation: subtle-glowing 1300ms infinite;
}

@keyframes subtle-glowing {
  0% {
    background-color: #ffffffd6;
  }
  50% {
    background-color: #58b3e4d7;
  }
  100% {
    background-color: #ffffffd6;
  }
}
</style>
