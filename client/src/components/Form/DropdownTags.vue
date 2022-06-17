<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */
// adapted from https://bootstrap-vue.org/docs/components/form-tags

import { computed, ref } from 'vue'

const emit = defineEmits(['update:modelValue'])
const props = defineProps({
  name: String,
  options: Array,
  modelValue: Array,
})

const search = ref('')

const value = computed({
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

const criteria = computed(() => {
  // Compute the search criteria
  return search.value.trim().toLowerCase()
})

const availableOptions = computed(() => {
  // Filter out already selected options
  const options = props.options.filter((opt) => value.value.indexOf(opt) === -1)
  if (criteria.value) {
    // Show only options that match criteria
    return options.filter((opt) => opt.toLowerCase().includes(criteria.value))
  }
  // Show all options available
  return options
})

const searchDesc = computed(() => {
  if (criteria.value && availableOptions.value.length === 0) {
    return 'There are no tags matching your search criteria'
  }
  return ''
})

function onOptionClick({ option, addTag }) {
  addTag(option)
  search.value = ''
}
</script>

<template>
  <div>
    <b-form-tags
      id="tags-with-dropdown"
      v-model="value"
      no-outer-focus
      class="mb-2"
    >
      <template v-slot="{ tags, disabled, addTag, removeTag }">
        <ul v-if="tags.length > 0" class="list-inline d-inline-block mb-2">
          <li v-for="tag in tags" :key="tag" class="list-inline-item">
            <b-form-tag
              @remove="removeTag(tag)"
              :title="tag"
              :disabled="disabled"
              :variant="tag === 'null' ? 'warning' : 'info'"
              >{{ tag }}</b-form-tag
            >
          </li>
        </ul>

        <b-dropdown
          size="sm"
          variant="outline-secondary"
          block
          menu-class="w-100"
        >
          <template #button-content>
            <b-icon icon="tag-fill"></b-icon> Choose {{ name }}
          </template>
          <b-dropdown-form @submit.stop.prevent="() => {}">
            <b-form-group
              label="Search tags"
              label-for="tag-search-input"
              label-cols-md="auto"
              class="mb-0"
              label-size="sm"
              :description="searchDesc"
              :disabled="disabled"
            >
              <b-form-input
                v-model="search"
                id="tag-search-input"
                type="search"
                size="sm"
                autocomplete="off"
              ></b-form-input>
            </b-form-group>
          </b-dropdown-form>
          <b-dropdown-divider></b-dropdown-divider>
          <b-dropdown-item-button
            v-for="option in availableOptions"
            :key="option"
            @click="onOptionClick({ option, addTag })"
          >
            {{ option }}
          </b-dropdown-item-button>
          <b-dropdown-text v-if="availableOptions.length === 0">
            There are no {{ name }} available to select
          </b-dropdown-text>
        </b-dropdown>
      </template>
    </b-form-tags>
    <b-button @click="value = []">Clear {{ name }}</b-button>
  </div>
</template>
