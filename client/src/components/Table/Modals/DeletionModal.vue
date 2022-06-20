<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { ref } from 'vue'
import { API_URL } from '../../../api'
import { status, statusPrefix } from '../../../helpers/queueFormatter'
import { getQueue, store } from '../../../store'

const props = defineProps({ item: Object, removalUrl: String })

const deleteModalShow = ref(false)
const entry = ref()

// Remove an entry from the list
async function removeEntry() {
  // TODO could also reload on deletion instead of deleting in store
  if (entry.value.removeFromStore) {
    // Remove first matching item from store
    const list = entry.value.fromQueue ? store.queue : store.allResults
    for (const i in list) {
      console.log(list[i])
      if (list[i].id === entry.value.id) {
        list.splice(i, 1)
        console.log(entry.value.id, 'removed from store')
        break
      }
    }
  }

  // Inform the server to remove the same entry
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: entry.value.id, name: props.item.name }),
  }
  fetch(API_URL + props.removalUrl, requestOptions).then(() => {
    console.log('Item', entry.value.id, 'removed succesfully')
    getQueue()
  })
}

// TODO refactor
function setEntryRemoval(item) {
  let title = ''
  let description = ''
  let removeFromStore = true
  let fromQueue = true
  if (!item.status) {
    fromQueue = false
    title = 'Remove entry?'
    description = `Are you sure you want to remove result ${item.name}?`
  } else if (item.status === status.toDo) {
    title = 'Cancel experiment?'
    description = `Are you sure you want to cancel scheduled experiment ${item.name}?`
  } else {
    removeFromStore = false
    title = 'Abort experiment?'
    description = `Are you sure you want to abort active experiment ${item.name}?`
  }
  entry.value = {
    id: item.id,
    title,
    description,
    removeFromStore,
    fromQueue,
  }
  deleteModalShow.value = !deleteModalShow.value
}

function getCancelIcon(item) {
  if (!item.status) return 'bi-trash'
  const status = item.status.slice(statusPrefix.length)
  if (status === status.toDo) return 'bi-x-lg'
  else return 'bi-x-octagon-fill'
}

function getTooltipText(item) {
  if (!item.status) return 'Delete'
  const status = item.status.slice(statusPrefix.length)
  if (status === status.toDo) return 'Cancel'
  else return 'Cancel'
}
</script>

<template>
  <b-button
    variant="outline-danger"
    class="mx-1 float-end"
    v-b-tooltip.hover
    :title="getTooltipText(item)"
    @click="setEntryRemoval(item)"
    data-testid="delete"
    ><!--Shows when the user wants to delete an entry-->
    <b-modal
      v-if="entry"
      id="deletion-modal"
      v-model="deleteModalShow"
      :title="entry.title"
      ok-title="Yes"
      ok-variant="danger"
      cancel-title="No"
      @ok="removeEntry()"
    >
      <p>{{ entry.description }}</p>
    </b-modal>

    <i :class="'bi ' + getCancelIcon(item)"></i>
  </b-button>
</template>
