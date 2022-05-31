<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import {
  article,
  capitalise,
  underscoreToSpace,
  formatMultipleItems,
} from '../helpers/resultFormatter'
//import { selectionOptions } from '../helpers/optionsFormatter'

import FormGroup from './Form/FormGroup.vue'
import { showToast } from '../store'

//const emit = defineEmits(['formChange'])
const props = defineProps({
  name: String,
  title: String,
  description: String,
  options: Array,
  required: Boolean,
  maxK: Number,
  horizontalLayout: Boolean,
  data: { type: Object, required: true },
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
//const flatOptions = props.nested ? flattenOptions() : props.options

const visibleGroup = ref(1)

onMounted(() => {
  /*console.log(props.name)
  if (props.name == 'filter' || props.name == 'dataset')
    console.log(props.name, props.options)*/
  // TODO separate 1-sized formgrouplists
  form.value.name = props.title
  /*if (props.name == 'filter')
    console.log(props.name,form)*/
  //console.log(props.name, 'options', props.options)
})

watch(
  () => {
    // Watch for the changing of options
    return props.options
  },
  () => {
    // Update form if this changes
    // TODO refactor
    if (props.name == 'approach' || props.name == 'metric') update()
  },
  {
    // Make sure this does not trigger on initialization
    immediate: false,
    deep: true,
  }
)

/* TODO doesn't work
// Set visible group on group count change (added/copy/remove)
watch(
  (form.groupCount,
  (newCount) => {
    visibleGroup.value = newCount - 1
  })
)*/

// Splice groups array to remove a group
function removeGroup(i) {
  // Don't remove first required option
  if (props.required && form.value.groupCount == 1) return
  //const mainOption = form.value.main[i]
  const mainOption = { ...form.value.choices[i].main }

  form.value.groupCount--
  /*form.value.main.splice(i, 1)
  form.value.inputs.splice(i, 1)
  form.value.selects.splice(i, 1)
  form.value.lists.splice(i, 1)*/
  form.value.choices.splice(i, 1)

  // Set visible group to last before deleted one
  visibleGroup.value = i

  showFormToast(mainOption, 'removed')
}

// Copies the selected item and puts it at the end of the list
function copyItem(i) {
  form.value.groupCount++ //Add a new item
  // Deep-copy the selected value to the new item
  // form.value.choices[form.value.groupCount - 1] = JSON.parse(
  //   JSON.stringify(form.value.choices[i])
  // )
  let item = JSON.parse(JSON.stringify(form.value.choices[i]))
  form.value.choices.splice(i, 0, item)
  visibleGroup.value = i + 2 // Show newly copied item
  console.log(form.value.choices[i].main)
  showFormToast(form.value.choices[i].main, 'copied')
}

/**
 * TODO document
 */
function showFormToast(object, actionMessage) {
  // Show toast
  // TODO delay and variant don't work?
  const mainOptions = {
    title:
        capitalise(props.name) + ' ' + 
        //If the metric doesn't have a value, don't mention it
        (object.name == undefined ?  '' : object.name + ' ') +
         actionMessage + '!',
  }
  const otherOptions = { pos: 'top-right', delay: 800, variant: 'warning' }
  showToast(mainOptions, otherOptions)
}

//Update the options that cannot be be submitted due to changing experiment type (
function update() {
  let entries = props.options
    .map((category) => category.options)
    .concat()
    .flat()
    .map((entry) => entry.name)
  const deleteEntry = 'NULL'
  for (let i = 0; i < form.value.choices.length; i++) {
    const mainChoice = form.value.choices[i].main
    if (mainChoice && !entries.includes(mainChoice.name)) {
      //every entry that does not exist in the list of option should be removed
      //Non-existing entries are replaced with a null entry
      /*form.value.main[i] = deleteEntry
      form.value.selects[i] = deleteEntry
      form.value.inputs[i] = deleteEntry
      form.value.lists[i] = deleteEntry*/
      form.value.choices[i] = deleteEntry
      if (props.required && form.value.groupCount > 1) form.value.groupCount--
    }
  }
  //console.log(form.value.main)
  // Filter null values
  /*form.value.main = form.value.main.filter((x) => x != deleteEntry)
  form.value.selects = form.value.selects.filter((x) => x != deleteEntry)
  form.value.inputs = form.value.inputs.filter((x) => x != deleteEntry)
  form.value.lists = form.value.lists.filter((x) => x != deleteEntry)*/
  form.value.choices = form.value.choices.filter((x) => x != deleteEntry)
  //console.log(form.value.main)
}

// A brief description of the group option
// TODO REALLY NEEDS REFACTOR
function shortGroupDescription(i) {
  const option = form.value.choices[i]
  let desc = capitalise(props.name) + ' ' + (i + 1)
  /*switch (props.name) {
    case value:
      ''
      break;

    default:
      break;
  }*/
  if (!option || !option.main) return desc // No choice made yet, no description

  desc = desc + ': ' + option.main.name
  if (visibleGroup.value == i + 1) return desc // This group is selected, only show the option name

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
    .filter((x) => x != '') // remove empty slots
    .join(', ')

  if (featuredOptions != '') desc += ' | ' + featuredOptions
  return desc

  function valueOrEmptyString(list) {
    return listNonEmpty(list) ? list[0].value : ''
  }

  function listNonEmpty(list) {
    return list && list.length > 0
  }
}
</script>

<template>
  <b-container>
    <b-container
      :toast="{ root: true }"
      fluid="sm"
      position="position-fixed"
    ></b-container>
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
            <b-col
              cols="12"
              class="accordion"
              role="tablist"
              v-for="i in form.groupCount"
              :key="i - 1"
            >
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
                            visibleGroup == i
                              ? (visibleGroup = -1)
                              : (visibleGroup = i)
                          "
                          :variant="visibleGroup == i ? 'secondary' : 'dark'"
                        >
                          <!-- TODO refactor-->
                          <template v-if="visibleGroup == i"
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
                <b-collapse
                  :id="name + 'accordion-' + i"
                  :accordion="name + '-accordion'"
                  :visible="visibleGroup == i"
                  role="tabpanel"
                >
                  <FormGroup
                    v-model:data="form.choices[i - 1]"
                    :name="name"
                    :options="options"
                    :required="
                      // If the option is needed, at least one selection must've been made
                      required &&
                      (!form.choices.main ||
                        form.choices.every((x) => x.main == ''))
                    "
                    :maxK="maxK"
                    :horizontalLayout="horizontalLayout"
                    @copy="copyItem(i - 1)"
                  />
                </b-collapse>
              </b-container>
            </b-col>
          </b-row>
        </b-card>
      </b-collapse>
    </b-row>
    <b-row>
      <h3 class="m-0">
        <b-card no-body class="mt-1">
          <b-button
            @click="
              form.groupCount++,
                form.choices.push({}),
                (form.visible = true),
                (visibleGroup = form.groupCount)
            "
            variant="primary"
            data-testid="add-button"
            >Add {{ name }}...
          </b-button>
        </b-card>
      </h3>
    </b-row>
  </b-container>
</template>
