<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { capitalise } from '../../helpers/resultFormatter'

import FormGroup from './FormGroup.vue'
import { showToast } from '../../store'

const emit = defineEmits(['update:modelValue'])
const props = defineProps({
  name: String,
  groupId: String,
  title: String,
  description: String,
  options: Array,
  required: Boolean,
  default: String,
  maxK: Number,
  modelValue: { type: Object, required: true },
})

const form = computed({
  get() {
    // console.log(props.name, props.title, props.modelValue)
    return props.modelValue
  },
  set(localValue) {
    console.log('local form change to', localValue)
    emit('update:modelValue', localValue)
  },
})

const scrollId = computed(() => {
  // console.log(props.groupId)
  return props.groupId ? props.groupId : props.name
})

// const visibleGroup = ref(1)
const groupVisible = ref([true]) // TODO refactor

// const removedGroup = ref(false) // for animation on group removal

onMounted(() => {
  // TODO separate 1-sized formgrouplists
  form.value.name = props.title
})

watch(
  () => {
    // Watch for the changing of options
    return props.options
  },
  () => {
    // Update form if this changes
    // TODO refactor
    if (props.name === 'approach' || props.name === 'metric') update()
  },
  {
    // Make sure this does not trigger on initialization
    immediate: false,
    deep: true,
  }
)

/**
 * Splice groups array to remove a group
 * @param {Int} i - The index of the group.
 */
function removeGroup(i) {
  // Don't remove first required option
  if (props.required && form.value.groupCount === 1) return
  // const mainOption = form.value.main[i]
  const mainOption = { ...form.value.choices[i].main }

  form.value.groupCount--
  form.value.choices.splice(i, 1)

  // Set visible group to last before deleted one
  // visibleGroup.value = i
  groupVisible.value[i] = true

  showFormToast(mainOption, 'removed')

  /*
  // TODO multiple usage, refactor to function/composable?
  removedGroup.value = 'removed'
  const timeoutMs = 500
  setTimeout(() => {
    removedGroup.value = ''
  }, timeoutMs) */
}

// Copies the selected item and puts it at the end of the list
function copyItem(i) {
  form.value.groupCount++ // Add a new item
  // Deep-copy the selected value to the new item
  const item = JSON.parse(JSON.stringify(form.value.choices[i]))
  console.log(item)
  // Insert item
  form.value.choices.splice(i, 0, item)
  // visibleGroup.value = i + 2 // Show newly copied item
  groupVisible.value[i + 1] = true
  // console.log('copy', form.value.choices[i].main)
  showFormToast(form.value.choices[i].main, 'copied')

  scrollToGroup(i + 1)
}

/**
 * TODO document
 */
function showFormToast(object, actionMessage) {
  // Show toast
  // TODO delay and variant don't work?
  const mainOptions = {
    title:
      capitalise(props.name) +
      ' ' +
      //If the metric doesn't have a value, don't mention it
      (object.name == undefined ? '' : object.name + ' ') +
      actionMessage +
      '!',
  }
  const otherOptions = { pos: 'top-right', delay: 800, variant: 'warning' }
  showToast(mainOptions, otherOptions)
}

// Update the options that cannot be be submitted due to changing experiment type (
function update() {
  const entries = props.options
    .map((category) => category.options)
    .concat()
    .flat()
    .map((entry) => entry.name)

  const deleteEntry = 'NULL'
  for (let i = 0; i < form.value.choices.length; i++) {
    const mainChoice = form.value.choices[i].main
    if (mainChoice && !entries.includes(mainChoice.name)) {
      // Every entry that does not exist in the list of option should be removed
      if (!props.required || form.value.groupCount > 1) {
        // Mark entry for deletion
        form.value.choices[i] = deleteEntry
        form.value.groupCount--
        // Don't remove the required first option, but reset it
      } else {
        form.value.choices[i].main = ''
      }
    }
  }
  // Filter null values
  form.value.choices = form.value.choices.filter((x) => x !== deleteEntry)
  // console.log('after update', form.value.choices)
}

// A brief description of the group option
// TODO REALLY NEEDS REFACTOR
function shortGroupDescription(i) {
  const option = form.value.choices[i]
  let desc = capitalise(props.name) + ' ' + (i + 1)
  if (!option || !option.main) return desc // No choice made yet, no description

  desc = desc + ': ' + option.main.name
  // if (visibleGroup.value === i + 1) return desc // This group is selected, only show the option name
  if (groupVisible.value[i]) return desc

  // Show first inner options as featured option
  const featuredOptions = [
    valueOrEmptyString(option.selects),
    valueOrEmptyString(option.inputs),
    listNonEmpty(form.value.lists) // Display inner form list length
      ? option.lists[0].name +
        ': ' +
        (option.lists[0].main && option.lists[0].main.length)
      : '',
  ]
    .filter((x) => x !== '') // remove empty slots
    .join(', ')

  if (featuredOptions !== '') desc += ' | ' + featuredOptions
  return desc

  function valueOrEmptyString(list) {
    return listNonEmpty(list) ? list[0].value : ''
  }

  function listNonEmpty(list) {
    return list && list.length > 0
  }
}

function addGroup() {
  form.value.groupCount++
  form.value.choices.push({})
  form.value.visible = true
  // (visibleGroup.value = form.value.groupCount
  groupVisible.value[form.value.groupCount - 1] = true

  // Scroll to newly added group
  scrollToGroup(form.value.groupCount - 1)
}

// Scroll to group index
function scrollToGroup(index) {
  nextTick(() => {
    // console.log(`#group-${scrollId.value.split(' ').join('-')}-${index}`)
    // TODO refactor to ID function?
    const element = document.querySelector(
      `#group-${scrollId.value.split(' ').join('-')}-${index}`
    )
    // console.log(element)
    element.scrollIntoView({ behavior: 'smooth' })
  })
}
</script>

<template>
  <b-container>
    <b-row>
      <h3 class="text-center text-white mb-0">
        <b-card no-body class="mb-0 bg-dark">
          <!--Capitalise the title.-->
          {{ title && capitalise(title) }}
          <!--Collapsable group list toggle button-->
          <b-button
            class="text-start"
            @click="form.visible = !form.visible"
            variant="dark"
          >
            <template v-if="form.visible"
              ><i class="bi bi-caret-down" /> |
            </template>
            <template v-else><i class="bi bi-caret-up" /> | </template>
          </b-button>
        </b-card>
      </h3>
      <!-- <p>{{ description && capitalise(description) }}</p> -->
    </b-row>
    <!--Collapsable group list-->
    <b-row>
      <b-collapse id="collapse" :visible="form.visible">
        <b-card class="g-0">
          <!--<p>
        {{ capitalise(title) }} selected:
        {{ formatMultipleItems(form.main) }}
      </p>-->
          <b-row>
            <TransitionGroup name="list">
              <b-col
                :id="`group-${scrollId.split(' ').join('-')}-${i - 1}`"
                cols="12"
                role="tablist"
                v-for="i in form.groupCount"
                :key="i - 1"
              >
                <!--{{ `group-${scrollId.split(' ').join('-')}-${i - 1}` }}-->
                <b-container class="g-0">
                  <!--Collapsable group toggle button with remove button-->
                  <b-row md="auto">
                    <b-row class="pe-0">
                      <b-col class="pe-0">
                        <b-card no-body class="mb-1">
                          <b-button
                            class="text-start"
                            block
                            @click="
                              // TODO this is pretty hacky
                              /*visibleGroup == i
                              ? (visibleGroup = -1)
                              : (visibleGroup = i)*/
                              groupVisible[i - 1] = !groupVisible[i - 1]
                            "
                            :variant="
                              //visibleGroup == i ? 'secondary' : 'dark'
                              groupVisible[i - 1] ? 'secondary' : 'dark'
                            "
                          >
                            <!-- TODO refactor-->
                            <template
                              v-if="
                                //visibleGroup == i
                                groupVisible[i - 1]
                              "
                              ><i class="bi bi-caret-down" /> |
                            </template>
                            <template v-else
                              ><i class="bi bi-caret-up" /> |
                            </template>
                            {{ shortGroupDescription(i - 1) }}
                          </b-button>
                        </b-card>
                      </b-col>
                      <!--Remove button-->
                      <b-col cols="1" v-if="!(i == 1 && required)" class="p-0">
                        <b-button
                          data-testid="remove-button"
                          @click="removeGroup(i - 1)"
                          variant="danger"
                          class="mb-2 mr-sm-2 mb-sm-0 float-end"
                          style="width: 90%"
                          >X</b-button
                        >
                      </b-col>
                    </b-row>
                  </b-row>
                  <!--Collapsable group-->
                  <!--<b-collapse :visible="visibleGroup == i" role="tabpanel">-->
                  <b-collapse :visible="groupVisible[i - 1]" role="tabpanel">
                    <FormGroup
                      v-model="form.choices[i - 1]"
                      :index="i - 1"
                      :name="name"
                      :groupId="name"
                      :options="options"
                      :required="
                        // If the option is needed, at least one selection must've been made
                        required &&
                        (!form.choices.main ||
                          form.choices.every((x) => x.main == ''))
                      "
                      :default="defaultOption"
                      :maxK="maxK"
                      @copy="copyItem(i - 1)"
                    />
                  </b-collapse>
                </b-container>
              </b-col>
            </TransitionGroup>
          </b-row>
        </b-card>
      </b-collapse>
    </b-row>
    <b-row>
      <h3 class="m-0">
        <b-card no-body class="mt-1">
          <b-button
            @click="addGroup()"
            variant="primary"
            data-testid="add-button"
            >Add {{ name }}...
          </b-button>
        </b-card>
      </h3>
    </b-row>
  </b-container>
</template>

<style>
.list-enter-active {
  transition: all 0.5s ease;
  animation: subtle-glowing 1300ms infinite;
}

.list-leave-active {
  transition: all 0.5s ease;
  animation: subtle-glowing-red 800ms infinite;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.subtle-blink {
  animation: subtle-glowing 1300ms infinite;
}

@keyframes subtle-glowing {
  0% {
    background-color: #ffffffd6;
  }
  50% {
    background-color: #77bfe6d7;
  }
  100% {
    background-color: #ffffffd6;
  }
}

@keyframes subtle-glowing-red {
  0% {
    background-color: #ffffffd6;
  }
  50% {
    background-color: #e67777d7;
  }
  100% {
    background-color: #ffffffd6;
  }
}
</style>
