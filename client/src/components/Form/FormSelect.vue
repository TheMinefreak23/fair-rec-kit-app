<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { computed } from 'vue'
import {
  article,
  capitalise,
  underscoreToSpace,
} from '../../helpers/resultFormatter'

const emit = defineEmits(['update:modelValue'])
const props = defineProps({
  option: Object,
  modelValue: Object,
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

function chooseLabel() {
  return (
    'Choose ' +
    article(props.option.name) +
    ' ' +
    underscoreToSpace(props.option.name)
  )
}

function checkboxLabel() {
  return capitalise(underscoreToSpace(props.option.name + '?'))
}

function formatOptions(options) {
  console.log(options)
  return options.map((option) => ({
    name: capitalise(String(option)),
    value: option,
  }))
}
</script>

<template>
  <div>
    <!--Use a radio group if there are a few options and they aren't true/false.-->
    <b-form-group
      :label="chooseLabel() + ' *'"
      v-if="option.options.length < 3 && typeof option.options[0] != 'boolean'"
    >
      <b-form-radio-group
        v-model="form.value"
        text-field="name"
        :options="formatOptions(option.options)"
        required
      ></b-form-radio-group>
    </b-form-group>
    <!--Use a checkbox if the options are of a binary (True or False) nature.-->
    <b-form-group
      :label="checkboxLabel() + ' *'"
      v-if="option.options[0] == true || option.options[0] == false"
    >
      <b-form-checkbox v-model="form.value" size="lg" required>{{
        form.value ? 'Yes' : 'No'
      }}</b-form-checkbox>
    </b-form-group>
    <!--Use a dropdown select form otherwise-->
    <b-form-group
      v-if="option.options.length > 2"
      :label="chooseLabel(option.name) + ' *'"
    >
      <!--TODO: ADD MULTIPLE SELECT FOR FILTERS (MODAL?)-->
      <b-form-select
        :id="option.name"
        v-model="form.value"
        :options="formatOptions(option.options)"
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
  </div>
</template>
