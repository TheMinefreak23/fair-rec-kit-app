<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { computed } from 'vue'
import { capitalise, underscoreToSpace } from '../../helpers/resultFormatter'

const emit = defineEmits(['update:modelValue'])
const props = defineProps({
  value: Object,
  modelValue: Object,
  maxK: Number,
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
</script>
<template>
  <b-col :cols="!value.name.includes('split') ? 6 : 12">
    <b-form-group
      :label="capitalise(underscoreToSpace(value.name)) + ' *'"
      :description="
        'Between ' +
        value.min +
        ' and ' +
        (value.name.toLowerCase() == 'k' ? props.maxK : value.max)
      "
      required
      ><!--Regular input-->
      <!--The max k value is based on the amount of recommendations.
                Because of this we use a separate setting to cover for it.-->

      <!--v-model="form.value"-->
      <b-form-input
        v-if="!value.name.includes('split')"
        v-model="form.value"
        :state="
          form.value >= value.min &&
          form.value <=
            (value.name.toLowerCase() == 'k' ? props.maxK : value.max)
        "
        :type="Number.isInteger(form.value) ? 'number' : 'text'"
        number
        :placeholder="'Enter ' + underscoreToSpace(value.name)"
        validated="true"
      />
      <!--Use a range slider if it's a train/test split option-->
      <SplitRange
        @input="form.value = $event"
        v-model="form.value"
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
        @input="form.value = [$event.minValue, $event.maxValue]"
      />
      <!--Display the seed label for the seed option.-->
      <div
        v-if="value.name.includes('seed') && form.value == null"
        class="text-center"
      >
        <b>Seed will be randomly generated.</b>
      </div>
    </b-form-group>
  </b-col>
</template>
