<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import {
  article,
  capitalise,
  underscoreToSpace,
  formatMultipleItems,
} from '../helpers/resultFormatter'
//import { selectionOptions } from '../helpers/optionsFormatter'

//const emit = defineEmits(['formChange'])
const props = defineProps({
  name: String,
  plural: String,
  description: String,
  options: Array,
  required: Boolean,
  maxK: Number,
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
  form.value.name = props.plural
  //console.log(props.name, 'options', props.options)
})

watch(
  () => {
    // Watch for the changing of options
    return props.options
  },
  () => {
    // Update form if this changes
    update()
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
        groupCount: 0, // For sublists there is no minimum amount of group items.
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
  if (props.required && form.value.groupCount == 1) return
  form.value.groupCount--
  form.value.main.splice(i, 1)
  form.value.inputs.splice(i, 1)
  form.value.selects.splice(i, 1)
  form.value.lists.splice(i, 1)
  visibleGroup.value = i // Set visible group to last before deleted one
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
  form.value.groupCount++ //Add a new item
  form.value.main[form.value.groupCount - 1] = form.value.main[i] //Copy the selected value to the new item
  visibleGroup.value = form.value.groupCount // Show newly copied item

  if (form.value.inputs[i]) {
    //Copy textfield options (if applicable)
    form.value.inputs[form.value.groupCount - 1] = form.value.inputs[i].map(
      (param) => ({
        name: param.name,
        value: param.value,
      })
    )
  }
  if (form.value.selects[i]) {
    //Copy select options (if applicable)
    form.value.selects[form.value.groupCount - 1] = form.value.selects[i].map(
      (param) => ({
        name: param.name,
        value: param.value,
      })
    )
  }
  if (form.value.lists[i]) {
    //Copy nested option list (if applicable)
    form.value.lists[form.value.groupCount - 1] = form.value.lists[i].map(
      (param) => ({
        name: param.name,
        value: param.value,
      })
    )
  }
}
//Update the options that cannot be be submitted due to changing experiment type (
function update() {
  let entries = props.options
    .map((category) => category.options)
    .concat()
    .flat()
    .map((entry) => entry.name)
  const deleteEntry = 'NULL'
  for (let i = 0; i < form.value.main.length; i++) {
    if (!entries.includes(form.value.main[i].name)) {
      //every entry that does not exist in the list of option should be removed
      //Non-existing entries are replaced with a null entry
      form.value.main[i] = deleteEntry
      form.value.selects[i] = deleteEntry
      form.value.inputs[i] = deleteEntry
      form.value.lists[i] = deleteEntry
      if (props.required && form.value.groupCount > 1) form.value.groupCount--
    }
  }
  //console.log(form.value.main)
  // Filter null values
  form.value.main = form.value.main.filter((x) => x != deleteEntry)
  form.value.selects = form.value.selects.filter((x) => x != deleteEntry)
  form.value.inputs = form.value.inputs.filter((x) => x != deleteEntry)
  form.value.lists = form.value.lists.filter((x) => x != deleteEntry)
  //console.log(form.value.main)
}

// A brief description of the group option
// TODO REALLY NEEDS REFACTOR
function shortGroupDescription(i) {
  const option = form.value.main[i]
  let desc = capitalise(props.name) + ' ' + (i + 1)
  /*switch (props.name) {
    case value:
      ''
      break;

    default:
      break;
  }*/
  if (!option) return desc // No choice made yet, no description

  desc = desc + ': ' + option.name
  if (visibleGroup.value == i + 1) return desc // This group is selected, only show the option name

  // Show first inner options as featured option
  console.log(form.value.lists[i] && form.value.lists[i][0])
  const featuredOptions =
    (form.value.selects[i] &&
      form.value.selects[i][0] &&
      form.value.selects[i][0].value) +
    ', ' +
    (form.value.inputs[i] &&
      form.value.inputs[i][0] &&
      form.value.inputs[i][0].value) +
    ', ' +
    (form.value.lists[i] &&
      form.value.lists[i][0] &&
      // Display inner form list length
      form.value.lists[i][0].name + ': ' + form.value.lists[i][0].main.length)

  desc += ' | ' + featuredOptions
  return desc
}
</script>

<template>
  <h3 class="text-center">
    <b-card no-body class="mb-1">
      <!--Collapsable group list toggle button-->
      <b-button
        align-v="end"
        @click="form.visible = !form.visible"
        :variant="form.visible ? 'primary' : 'danger'"
      >
        <template v-if="form.visible">&#x25BC; | </template>
        <template v-else>&#x25BA; | </template>
        <!--Capitalise the title.-->
        {{ capitalise(plural) }}</b-button
      >
    </b-card>
  </h3>
  <p>{{ description && capitalise(description) }}</p>
  <!--TODO b-collapse doesn't work-->
  <!--Collapsable group list-->
  <template id="collapse" v-if="form.visible">
    <b-card class="g-0">
      <h5>
        {{ capitalise(plural) }} selected:
        {{ formatMultipleItems(form.main) }}
      </h5>
      <div
        class="accordion"
        role="tablist"
        v-for="i in form.groupCount"
        :key="i - 1"
      >
        <b-card class="g-0">
          <b-card-header header-tag="header" class="p-1" role="tab">
            <b-card no-body class="mb-1">
              <!--Collapsable group toggle button-->
              <b-button
                block
                v-b-toggle="name + 'accordion-' + i"
                @click="visibleGroup = i"
                variant="info"
                >{{ shortGroupDescription(i - 1) }}
              </b-button>
            </b-card>
          </b-card-header>
          <!--Collapsable group-->
          <b-collapse
            :id="name + 'accordion-' + i"
            :accordion="name + '-accordion'"
            :visible="visibleGroup == i"
            role="tabpanel"
          >
            <b-row class="align-items-end">
              <b-col>
                <b-row>
                  <b-col cols="4">
                    <b-form-group
                      :label="'Select ' + article(name) + ' ' + name"
                    >
                      <b-form-select
                        v-model="form.main[i - 1]"
                        data-testid="main-select"
                        :options="options"
                        text-field="name"
                        @change="setParameter(i - 1, $event)"
                        :required="
                          // If the option is needed, at least one selection must've been made
                          required &&
                          (form.main.length == 0 ||
                            form.main.every((x) => x == ''))
                        "
                      >
                        <template #first>
                          <b-form-select-option :value="''"
                            >Choose..</b-form-select-option
                          >
                        </template>
                      </b-form-select>
                      <b-button
                        v-if="form.main[i - 1]"
                        @click="copyItem(i - 1)"
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
                  <b-col cols="4" v-if="hasParams(i - 1)">
                    <!--Use an input form for values.-->
                    <template
                      v-for="(value, index) in form.main[i - 1].params.values"
                      :key="value"
                    >
                      <!--The max k value is based on the amount of recommendations.
                Because of this we use a seperate setting to cover for it.-->
                      <b-form-group
                        :label="capitalise(underscoreToSpace(value.name))"
                        :description="
                          'Between ' +
                          value.min +
                          ' and ' +
                          (value.name == 'k' ? props.maxK : value.max)
                        "
                      >
                        <b-form-input
                          v-if="!value.name.includes('split')"
                          v-model="form.inputs[i - 1][index].value"
                          :state="
                            form.inputs[i - 1][index].value >= value.min &&
                            form.inputs[i - 1][index].value <=
                              (value.name == 'k' ? props.maxK : value.max)
                          "
                          validated="true"
                        />
                        <b-form-input
                          v-if="value.name.includes('Train')"
                          type="range"
                          min="value.min"
                          max="value.max"
                          step="5"
                          data-testid="split-input"
                          id="customRange"
                          v-model="form.inputs[i - 1][index].value"
                        ></b-form-input>
                        <div
                          v-if="value.name.includes('Train')"
                          class="text-center"
                        >
                          <strong>Train:</strong>
                          <i>{{
                            ' ' + form.inputs[i - 1][index].value + ' '
                          }}</i>
                          <strong>Test:</strong
                          ><i
                            >{{ ' '
                            }}{{ 100 - form.inputs[i - 1][index].value }}</i
                          >
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
                        :label="
                          capitalise(underscoreToSpace(option.name + '?'))
                        "
                        v-if="
                          option.options[0] == true ||
                          option.options[0] == false
                        "
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
                            <b-form-select-option :value="null" disabled
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
                        data-testid="remove-button"
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
                    <b-card class="bg-secondary">
                      <FormGroupList
                        v-model:data="form.lists[i - 1][index]"
                        :name="option.name"
                        :plural="option.plural"
                        :description="
                          option.plural +
                          ' for ' +
                          name +
                          ' ' +
                          form.main[i - 1].name
                        "
                        :options="option.options"
                        :required="false"
                      />
                    </b-card>
                  </template>
                </b-row>
              </b-col>
            </b-row>
          </b-collapse>
        </b-card>
      </div>

      <b-button
        @click="form.groupCount++, (visibleGroup = form.groupCount)"
        align-v="end"
        variant="primary"
        >Add {{ name }}...</b-button
      >
    </b-card></template
  >
</template>
