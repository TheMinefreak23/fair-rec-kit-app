<script setup>
import { computed, ref } from 'vue'
import sortBy from 'just-sort-by'
import { API_URL } from '../api'
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

const emit = defineEmits(['loadResult', 'loadMore', 'paginationSort'])
const props = defineProps({
  overview: Boolean,
  results: Array,
  headers: Array,
  buttonText: String,
  removable: Boolean,
  serverFile: String,
  serverFile2: String,
  pagination: Boolean,
  caption: String,
})

const caption = ref('')
const entryAmount = ref(20)
const deleteModalShow = ref(false)
const editModalShow = ref(false)
const newName = ref('')
const newTags = ref('')
const newEmail = ref('')
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

async function editEntry() {
  //Inform the server of the new values at the selected index
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      index: selectedEntry.value,
      new_name: newName.value,
      new_tags: newTags.value,
      new_email: newEmail.value,
    }),
  }
  fetch(API_URL + props.serverFile2, requestOptions).then(() => {
    console.log('Item edited succesfully')
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

const sorted = computed(() => {
  console.log(props.results)

  if (!props.pagination) return sort(sortindex.value)
  else return props.results
})

/**
 * Sorts data based on index.
 * @param {Int}	i	- i is the coumn index on which is being sorted.
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
 * @param {Int}	i	- i is the coumn index on which is being sorted.
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
    <b-form-input v-model="newName" placeholder="New name"></b-form-input>
    <br />
    Tags:
    <b-form-input v-model="newTags" placeholder="New tags"></b-form-input>
    <br />
    E-mail:
    <b-form-input
      v-model="newEmail"
      placeholder="New e-mail"
      type="email"
    ></b-form-input>
    <br />
    Color (this doesn't do anything):
    <!-- I may have gotten a little carried away -->
    <b-form-input type="color"></b-form-input>
    <br />
    Date (this doesn't do anything):
    <b-form-input type="date"></b-form-input>
    <br />
    Credit card number (this doesn't do anything):
    <b-form-input type="password"></b-form-input>
  </b-modal>

  <b-table-simple hover striped responsive caption-top>
    <caption>
      {{ props.caption }}
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
        <b-th v-for="(subheader, index) in subheaders" :key="subheader">
          {{ subheader }}
        </b-th>
      </b-tr>
    </b-thead>
    <b-tbody>
      <b-tr v-for="(item, index) of sorted" :key="item"
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

        <b-button
          v-if="overview"
          pill
          @click=";(editModalShow = !editModalShow), (selectedEntry = index)"
          >Edit</b-button
        >
        <template v-if="removable">
          &nbsp; 
        </template>
        <b-button
          v-if="removable"
          variant="danger"
          @click="
            ;(deleteModalShow = !deleteModalShow), (selectedEntry = index)
          "
          >Delete</b-button
        >
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
