<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
import { computed, ref } from 'vue'
import sortBy from 'just-sort-by'
import { API_URL } from '../api'
import { validateEmail } from '../helpers/optionsFormatter'

const emit = defineEmits([
  'loadResult',
  'loadResults',
  'loadMore',
  'paginationSort',
  'updateHeaders'
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
  headerOptions: Array,
  userOptions: Array,
  itemOptions: Array,
})

const caption = ref('')
const entryAmount = ref(20)
const deleteModalShow = ref(false)
const editModalShow = ref(false)
const viewModalShow = ref(false)
const updateHeadersModalShow = ref(false)
const checkedColumns = ref([])
const itemColumns = ref([])
const userColumns = ref([])
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
  newName.value = ''
  newTags.value = ''
  newEmail.value = ''
}

async function removeEntry() {
  //Remove an entry from the list
  let entry = selectedEntry.value
  props.results.splice(entry, 1)
  //Inform the server to remove the same entry
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ index: entry }),
  }
  fetch(API_URL + props.serverFile, requestOptions).then(() => {
    console.log('Item removed succesfully')
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
  metadataStr.value = data.result
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
    <p v-else-if="newEmail != ''" style="color: red">
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

  <!-- Shows the metadata of the designated entry -->
  <b-modal id="view-modal" v-model="viewModalShow" title="Metadata" ok-only>
    <h5>Here is the metadata:</h5>
    <p>{{ metadataStr }}</p>
  </b-modal>

  <!-- Modal used for changing the headers of the user recommendations table -->
  <b-modal
    id="change-columns-modal"
    v-model="updateHeadersModalShow"
    title="Change columns"
    @ok="$emit('updateHeaders', checkedColumns, userColumns, itemColumns)"
    >
    <p>Select the extra headers you want to be shown</p>
    <p>{{headerOptions}}</p>
    <p>General:</p>
    <div
      class="form-check form-switch"
      v-for="(header, index) in headerOptions"
      :key="header"
    >
      <input
        v-model="checkedColumns"
        class="form-check-input"
        type="checkbox"
        :value="header.name"
        :id="header.name"
      />
      <label class="form-check-label" :id="header.name">
        {{ header.name }}
      </label>
    </div>

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
        :value="header.name"
        :id="header.name"
      />
      <label class="form-check-label" :id="header.name">
        {{ header.name }}
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
        :value="header.name"
        :id="header.name"
      />
      <label class="form-check-label" :id="header.name">
        {{ header.name }}
      </label>
    </div>
  </b-modal>

  <b-table-simple hover striped responsive caption-top>
    <caption>
      {{
        props.caption
      }}
       <template v-if="expandable">
      <b-button 
        @click="updateHeadersModalShow = !updateHeadersModalShow">  
        change headers 
      </b-button>
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
        ><b-td v-if="overview">
          <b-button @click="$emit('loadResult', item.id)">View result</b-button>
        </b-td>
        <b-td
          v-for="[key, value] in Object.entries(item)"
          :key="`${descending}_${sortindex}_${index}-${key}`"
        >
          <b-td>
            {{ value }}
          </b-td>
        </b-td>

        <b-td v-if="overview || removable">
          <b-button
            v-if="overview"
            pill
            @click="
              ;(editModalShow = !editModalShow),
                (selectedEntry = index),
                getNameTagsMail(item.id)
            "
            >Edit</b-button
          >
          <b-button
            v-if="overview"
            pill
            @click=";(viewModalShow = !viewModalShow), getMetadata(item.id)"
            >View</b-button
          >
          <template v-if="removable"> </template>
          <b-button
            v-if="removable"
            variant="danger"
            @click="
              ;(deleteModalShow = !deleteModalShow), (selectedEntry = index)
            "
            >Delete</b-button
          >
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
