<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { ref } from 'vue'
import { API_URL } from '../../../api'
import { validateEmail } from '../../../helpers/optionsFormatter'
import { loadResult } from '../../../helpers/resultRequests'
import { store } from '../../../store'
import Tags from '../../Tags.vue'

const props = defineProps({ editUrl: String, id: String })
const emit = defineEmits(['loadResults'])

const editModalShow = ref(false)

// Item info
const newName = ref('')
const newTags = ref([])
const newEmail = ref('')

async function editEntry() {
  const newEntry = {
    name: newName.value,
    tags: newTags.value,
    email: newEmail.value,
  }
  // console.log('new entry ', props.id, ':', newEntry)

  /*
    // TODO change from store because
    // updating results doesn't work (store changes but table doesn't update)
    // Edit first matching item from store
    const result = store.allResults[props.index]
    console.log('result', result)
    result.name = newEntry.name
    result.tags = newEntry.tags
    store.allResults.splice(props.index, 1, result)
    console.log(store.allResults) */

  // Update current open results
  for (const [index, result] of store.currentResults.entries()) {
    console.log(result)
    if (result.id === props.id) {
      // console.log('BINGU')
      result.name = newEntry.name
      result.metadata.name = newEntry.name
      result.metadata.tags = newEntry.tags
      result.metadata.email = newEntry.email
    }
    store.currentResults.splice(index, 1, result)
  }
  // console.log('current results', store.currentResults)

  // TODO make editing by index possible? (Store index?)

  // Inform the server of the new values of the item with the ID
  newEmail.value = checkEmail(newEmail.value)
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: props.id,
      new_name: newEntry.name,
      new_tags: newEntry.tags,
      new_email: newEntry.email,
    }),
  }
  fetch(API_URL + props.editUrl, requestOptions).then((response) => {
    if (response.text === 'Edited index')
      console.log('Item ', props.id, ' edited succesfully')
    emit('loadResults')
  })
  emptyVmodels()
}

async function getNameTagsMail() {
  const data = await loadResult(props.id)
  console.log('Metadata succesfully requested')
  newName.value = data.result.metadata.name
  if (data.result.metadata.tags) newTags.value = data.result.metadata.tags
  if (data.result.metadata.email) newEmail.value = data.result.metadata.email
}

// Resets the editable values
function emptyVmodels() {
  newName.value = ''
  newTags.value = []
  newEmail.value = ''
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
</script>

<template>
  <div>
    <!--Shows when the user wants to edit an entry-->
    <b-modal
      id="edit-modal"
      v-model="editModalShow"
      title="Editing results"
      size="lg"
      @ok="editEntry()"
      @cancel="emptyVmodels()"
    >
      <h6>
        Please type in the new values. Blank fields will be left unchanged.
      </h6>
      Name:
      <b-form-input v-model="newName" placeholder="Enter new name" />
      <br />
      Tags: (separate tags using a single comma)
      <Tags v-model="newTags" />
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
      />
      <br />
      <!--
    Color (this doesn't do anything):
    <b-form-input type="color"></b-form-input>
    <br />-->
    </b-modal>

    <b-button
      variant="primary"
      class="mx-1"
      @click=";(editModalShow = !editModalShow), getNameTagsMail()"
      data-testid="edit"
    >
      <i class="bi bi-pencil-square" />
    </b-button>
  </div>
</template>
