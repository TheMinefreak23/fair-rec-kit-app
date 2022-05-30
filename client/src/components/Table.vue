<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
import { computed, onMounted, ref } from 'vue'
import sortBy from 'just-sort-by'
import { API_URL } from '../api'
import { formatMetadata } from '../helpers/metadataFormatter'
import FormGroupList from './FormGroupList.vue'
import { validateEmail, emptyFormGroup } from '../helpers/optionsFormatter'
import { store } from '../store'
import { statusPrefix, statusVariant, status, makeHeader } from '../helpers/resultFormatter'

const emit = defineEmits([
  'loadResult',
  'loadResults',
  'loadMore',
  'paginationSort',
  'changeFilters',
  'updateHeaders',
])
const props = defineProps({
  overview: Boolean,
  results: Array,
  headers: Array,
  buttonText: String,
  removable: Boolean,
  serverFile: String,
  serverFile2: String,
  serverFile3: String,
  pagination: Boolean,
  caption: String,
  expandable: Boolean,
  userOptions: Array,
  itemOptions: Array,
  filters: Object,
  filterOptions: Array,
  defaultSort: Number,
})

const caption = ref('')
const entryAmount = ref(20)
const deleteModalShow = ref(false)
const editModalShow = ref(false)
const viewModalShow = ref(false)
const filtersModalShow = ref(false)
const updateHeadersModalShow = ref(false)
const checkedColumns = ref([])
const itemColumns = ref([])
const userColumns = ref([])
const filters = ref(emptyFormGroup(false))
const newName = ref('')
const newTags = ref('')
const newTagsList = ref([])
const newEmail = ref('')
const metadataStr = ref('')
const selectedEntry = ref(0)
const sortindex = ref(0)
const descending = ref(false)

const subheaders = computed(() => {
  const result = []

  for (const header of props.headers) {
    if (header.subheaders) {
      result.push(...header.subheaders)
    } else {
      result.push('')
    }
  }
  return result
})

const sorted = computed(() => {
  //console.log(props.results)

  if (!props.pagination) return sort(sortindex.value)
  else return props.results
})

onMounted(() => {
  /*if (props.caption == 'Testcaption')
    console.log('filterOptions', props.filterOptions)*/
  // Sort on default column if it is given
  if (props.defaultSort) {
    sortindex.value = props.defaultSort
    descending.value = true // For now sort by descending on default, TODO refactor
  }
})

/**
 * Turns a string into an array separated by comma's
 * @param {string} str the string that turns into an array
 * @return {[string]} array of strings
 */
function stringToList(str) {
  return str.split(',')
}

/**
 * returns an empty string if the Email is not valid
 * @param {string} Email Email to validate
 * @return {string}
 */
function checkEmail(Email) {
  if (validateEmail(Email)) {
    return Email
  } else {
    return ''
  }
}

async function editEntry() {
  //Inform the server of the new values at the selected index
  newTagsList.value = stringToList(newTags.value)
  newEmail.value = checkEmail(newEmail.value)
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      index: selectedEntry.value,
      new_name: newName.value,
      new_tags: newTagsList.value,
      new_email: newEmail.value,
    }),
  }
  fetch(API_URL + props.serverFile2, requestOptions).then(() => {
    console.log('Item edited succesfully')
    emit('loadResults')
  })
  emptyVmodels()
}

// Resets the editable values
function emptyVmodels() {
  newName.value = ''
  newTags.value = ''
  newEmail.value = ''
}

async function removeEntry() {
  //Remove an entry from the list
  const entry = selectedEntry.value
  //props.results.splice(entry, 1)
  store.allResults = store.allResults.filter((e) => e.id != entry)
  //Inform the server to remove the same entry
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: entry }),
  }
  fetch(API_URL + props.serverFile, requestOptions).then(() => {
    console.log('Item', entry, 'removed succesfully')
  })
}

async function getMetadata(selectedID) {
  //request the metadata of the specified entry
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: selectedID }),
  }
  fetch(API_URL + props.serverFile3, requestOptions).then(() => {
    console.log('Metadata succesfully requested')
    getResult()
  })
}

async function getResult() {
  const response = await fetch(API_URL + props.serverFile3)
  const data = await response.json()
  metadataStr.value = formatMetadata(data.result)
}

async function getNameTagsMail(selectedID) {
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: selectedID }),
  }
  fetch(API_URL + props.serverFile3, requestOptions).then(() => {
    console.log('Metadata succesfully requested')
    getOldValues()
  })
}
async function getOldValues() {
  const response = await fetch(API_URL + props.serverFile3)
  const data = await response.json()
  newName.value = data.result.metadata.name
  newTags.value = data.result.metadata.tags.toString()
  newEmail.value = data.result.metadata.email
}

/**
 * Sorts data based on index.
 * @param {Int}	i	- i is the column index on which is being sorted.
 * @return	{[Object]} Sorted array of results.
 */
function sort(i) {
  const res = sortBy(props.results, function (o) {
    return Object.values(o)[i]
  })
  if (descending.value) {
    return res.reverse()
  }

  return res
}

/**
 * Sets index on which is being sorted and determines if the
 * sorting is ascending or descending.
 * @param {Int}	i	- i is the column index on which is being sorted.
 */
function setsorting(i) {
  if (i === sortindex.value) {
    descending.value = !descending.value
  }
  sortindex.value = i
  emit('paginationSort', i)
}
//console.log('propsfilteroptions', props.filterOptions)
</script>

<template>
  <!--Shows when the user wants to delete an entry-->
  <b-modal
    id="deletion-modal"
    v-model="deleteModalShow"
    title="Remove entry?"
    ok-title="Yes"
    ok-variant="danger"
    cancel-title="No"
    @ok="removeEntry()"
  >
    <p>Are you sure you want to remove this entry from the list?</p>
  </b-modal>

  <!--Shows when the user wants to edit an entry-->
  <b-modal
    id="edit-modal"
    v-model="editModalShow"
    title="Editing results"
    size="lg"
    @ok="editEntry()"
    @cancel="emptyVmodels()"
  >
    <h6>Please type in the new values. Blank fields will be left unchanged.</h6>
    Name:
    <b-form-input v-model="newName" placeholder="Enter new name"></b-form-input>
    <br />
    Tags: (separate tags using a single comma)
    <b-form-input v-model="newTags" placeholder="Enter new tags"></b-form-input>
    <br />
    E-mail:
    <p v-if="validateEmail(newEmail)" style="color: green">
      This is E-mail is valid :)
    </p>
    <p v-else-if="newEmail != '' && newEmail != null" style="color: red">
      This is not a valid E-mail :(
    </p>
    <b-form-input
      v-model="newEmail"
      placeholder="Enter new e-mail"
      type="email"
    ></b-form-input>
    <br />
    <!--
    Color (this doesn't do anything):
    <b-form-input type="color"></b-form-input>
    <br />-->
  </b-modal>

  <!-- Shows the metadata and experiment configuration of the designated entry -->
  <b-modal
    id="view-modal"
    v-model="viewModalShow"
    title="Result information"
    ok-only
  >
    <h5>Here is the metadata and experiment configuration:</h5>
    <span style="white-space: pre-wrap">{{ metadataStr }}</span>
  </b-modal>

  <!-- Modal used for changing the headers of the user recommendations table -->
  <b-modal
    id="change-columns-modal"
    v-model="updateHeadersModalShow"
    title="Select headers"
    @ok="
      $emit('updateHeaders', [
        ...checkedColumns,
        ...userColumns,
        ...itemColumns,
      ])
    "
  >
    <p>Select the extra headers you want to be shown</p>
    <p>User specific:</p>
    <div
      class="form-check form-switch"
      v-for="(header, index) in userOptions"
      :key="header"
    >
      <input
        v-model="userColumns"
        class="form-check-input"
        type="checkbox"
        :value="header"
        :id="header"
      />
      <label class="form-check-label" :id="header">
        {{ makeHeader(header).name }}
      </label>
    </div>

    <p>Item specific:</p>
    <div
      class="form-check form-switch"
      v-for="(header, index) in itemOptions"
      :key="header"
    >
      <input
        v-model="itemColumns"
        class="form-check-input"
        type="checkbox"
        :value="header"
        :id="header"
      />
      <label class="form-check-label" :id="header">
        {{ makeHeader(header).name }}
      </label>
    </div>
  </b-modal>
  <b-modal
    id="change-columns-modal"
    v-model="filtersModalShow"
    title="Change filters"
    @ok="$emit('changeFilters', filters)"
  >
    <FormGroupList
      v-model:data="filters"
      name="filter"
      plural="filters"
      :options="filterOptions"
      id="filters"
    />
  </b-modal>

  <b-table-simple hover striped responsive caption-top>
    <caption>
      {{
        props.caption
      }}

      <template v-if="expandable">
      <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css" rel="stylesheet">

        <div class="float-end">
          <b-button
            @click="updateHeadersModalShow = !updateHeadersModalShow"
            class="m-1"
          >
            Select Headers
          </b-button>
          <b-button @click="filtersModalShow = !filterModalShow" class="m-1">
            Filters
          </b-button>
        </div>
      </template>
    </caption>
    <b-thead head-variant="dark">
      <b-tr>
        <b-th v-if="overview"></b-th>
        <b-th
          v-for="(header, index) in headers"
          :key="header"
          :colspan="header.subheaders ? header.subheaders.length : 1"
          style="cursor: pointer"
          @click="setsorting(index)"
        >
          {{ header.name }}
        </b-th>
      </b-tr>
      <b-tr>
        <b-th v-if="overview"></b-th>
        <b-th v-for="subheader in subheaders" :key="subheader">
          {{ subheader }}
        </b-th>
      </b-tr>
    </b-thead>
    <b-tbody>
      <b-tr v-for="(item, index) in sorted" :key="item"
        ><b-td class="align-middle" v-if="overview">
          <b-button variant="outline-primary fw-bold" @click="$emit('loadResult', item.id)">View result</b-button>
        </b-td>
        <b-td
          v-for="[key, value] in Object.entries(item)"
          :key="`${descending}_${sortindex}_${index}-${key}`"
          class="text-center"
        >
            <!--Special pill format for status-->
            <!-- TODO refactor-->
            <template
              v-if="typeof value === 'string' && value.startsWith(statusPrefix)"
            >
              <b-button
                disabled
                :variant="statusVariant(value)"
                :class="
                  value.slice(statusPrefix.length) == status.active
                    ? 'status-blinking'
                    : 'status'
                "
                class="fw-bold"
              >
                {{ value.slice(statusPrefix.length) }}
              </b-button>
            </template>
            <template v-else> {{ value }}</template>
        </b-td>
          <b-td class="align-middle" v-if="overview || removable">
            <div class="m-0 float-end" style="width: 150px;">
            <b-button
              v-if="overview"
              variant="primary"
              class="mx-1"
              @click="
                ;(editModalShow = !editModalShow),
                  (selectedEntry = index),
                  getNameTagsMail(item.id)
              "
              ><i class="bi bi-pencil-square"></i></b-button
            >
            <b-button
              v-if="overview"
              variant="primary"
              class="mx-1"
              @click=";(viewModalShow = !viewModalShow), getMetadata(item.id)"
              ><i class="bi bi-info-circle"></i></b-button
            >
            <!--REFACTOR status condition-->
            <b-button
              v-if="
                removable &&
                (!item.status ||
                  [status.toDo, status.active].includes(
                    item.status.slice(statusPrefix.length)
                  ))
              "
              variant="danger"
              class="mx-1 float-end"
              @click="
                ;(deleteModalShow = !deleteModalShow), (selectedEntry = item.id)
              "
              ><i class="bi bi-trash"></i></b-button
            >
            </div>
          </b-td>
      </b-tr>
    </b-tbody>
  </b-table-simple>

  <b-button
    v-if="pagination"
    @click="$emit('loadMore', false, entryAmount)"
    variant="outline-primary"
    :disabled="entryAmount < 1"
  >
    Show previous {{ entryAmount }} items
  </b-button>
  <b-button
    v-if="pagination"
    @click="$emit('loadMore', true, entryAmount)"
    variant="outline-primary"
    :disabled="entryAmount < 1"
  >
    Show next {{ entryAmount }} items
  </b-button>
  <b-form-input
    v-model="entryAmount"
    v-if="pagination"
    :state="entryAmount >= 1"
    type="number"
    >20</b-form-input
  >
</template>

<style scoped>
/*adapted from SOURCE: https://www.w3docs.com/snippets/css/how-to-create-flashing-glowing-button-using-animation-in-css3.html*/
.status,
.status-blinking {
  background-color: #28a745;
}
@keyframes glowing {
  0% {
    background-color: #28a745;
    box-shadow: 0 0 5px #28a745;
  }
  50% {
    background-color: #28a745;
    box-shadow: 0 0 20px #28a745;
  }
  100% {
    background-color: #28a745;
    box-shadow: 0 0 5px #28a745;
  }
}
.status-blinking {
  animation: glowing 1300ms infinite;
}
</style>
