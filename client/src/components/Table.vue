<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
import { computed, onMounted, ref } from 'vue'
import sortBy from 'just-sort-by'
import { API_URL } from '../api'
import { formatMetadata } from '../helpers/metadataFormatter'
import FormGroupList from './Form/FormGroupList.vue'
import { validateEmail, emptyFormGroup } from '../helpers/optionsFormatter'
import { store } from '../store'
import { makeHeader, capitalise } from '../helpers/resultFormatter'
import { statusPrefix, statusVariant, status } from '../helpers/queueFormatter'
import { loadResult } from '../helpers/resultRequests'
import SettingsModal from './Table/SettingsModal.vue'
import { getInfoFromSpotifyID, getSpotifyToken } from '../helpers/songInfo'
import MusicModal from './ItemDetail/MusicModal.vue'

const emit = defineEmits([
  'viewResult',
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
  removeText: String,
  removable: Boolean,
  editable: Boolean,
  serverFile: String,
  serverFile2: String,
  pagination: Boolean,
  caption: String,
  expandable: Boolean,
  headerOptions: Object,
  userOptions: Array,
  itemOptions: Array,
  filters: Object,
  filterOptions: Array,
  defaultSort: Number,
})

const colWidth = '6em'
const colItemStyle = {
  minWidth: colWidth,
  width: colWidth,
  maxWidth: colWidth,
  inlineSize: colWidth,
  overflowWrap: 'break-word',
}
// Pagination
const caption = ref('')
const entryAmount = ref(20)

// Modals
const deleteModalShow = ref(false)
const editModalShow = ref(false)
const viewModalShow = ref(false)
const filtersModalShow = ref(false)
const updateHeadersModalShow = ref(false)

// Columns
const checkedColumns = ref([])

// Filters
const filters = ref(emptyFormGroup(false))

// Item info
const newName = ref('')
const newTags = ref('')
const newTagsList = ref([])
const newEmail = ref('')
const metadataStr = ref('')
const selectedEntry = ref(0)

// Sorting
const sortindex = ref(0)
const descending = ref(false)

// Item (music) detail
const track = ref()
const highlevelFeatures = ref()
const songInfo = ref({ lastFM: {} }) // TODO
const musicModalShow = ref(false)

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

// Remove an entry from the list
async function removeEntry() {
  const entry = selectedEntry.value

  if (entry.remove) {
    // Remove first matching item from store
    const list = entry.fromQueue ? store.allResults : store.queue
    for (let i in list) {
      if (list[i].id == entry.id) list.splice(i, 1)
      break
    }
  }

  // Inform the server to remove the same entry
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: entry.id }),
  }
  fetch(API_URL + props.serverFile, requestOptions).then(() => {
    console.log('Item', entry.id, 'removed succesfully')
  })
}

async function getMetadata(selectedID) {
  const data = await loadResult(selectedID)
  metadataStr.value = formatMetadata(data.result)
  console.log('Metadata succesfully requested')
}

async function getNameTagsMail(selectedID) {
  const data = await loadResult(selectedID)
  console.log('Metadata succesfully requested')
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
  } else if (status == status.toDo) {
    title = 'Cancel experiment?'
    description = `Are you sure you want to cancel scheduled experiment ${item.name}?`
  } else {
    removeFromStore = false
    title = 'Abort experiment?'
    description = `Are you sure you want to abort active experiment ${item.name}?`
  }
  selectedEntry.value = {
    id: item.id,
    title: title,
    description: description,
    removeFromStore: removeFromStore,
    fromQueue: fromQueue,
  }
  deleteModalShow.value = !deleteModalShow.value
}

function getCancelIcon(item) {
  if (!item.status) return 'bi-trash'
  const status = item.status.slice(statusPrefix.length)
  if (status == status.toDo) return 'bi-x-lg'
  else return 'bi-x-octagon-fill'
}

// Get music detail info
// TODO refactor
async function showMusicDetail(spotifyId) {
  const token = await getSpotifyToken()
  track.value = await getInfoFromSpotifyID(token, spotifyId)
  //console.log('track', track.value)

  // TODO
  /*
  //get AcousticBrainz highlevel features using LastFM's mbid
  highlevelFeatures.value = await songInfo.value.AcousticBrainz[
    songInfo.value.LastFM.track.mbid
  ][0]['highlevel']*/

  musicModalShow.value = !musicModalShow.value
}
</script>

<template>
  <!--Shows when the user wants to delete an entry-->
  <b-modal
    id="deletion-modal"
    v-model="deleteModalShow"
    :title="selectedEntry.title"
    ok-title="Yes"
    ok-variant="danger"
    cancel-title="No"
    @ok="removeEntry()"
  >
    <p>{{ selectedEntry.description }}</p>
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
    v-if="props.headerOptions"
    id="change-columns-modal"
    v-model="updateHeadersModalShow"
    title="Select headers"
    @ok="$emit('updateHeaders', checkedColumns)"
  >
    <p>Select the extra headers you want to be shown</p>
    <template v-for="category in Object.keys(props.headerOptions)">
      <p>{{capitalise(category)}} specific:</p>
      <div
        class="form-check form-switch"
        v-for="header in props.headerOptions[category]"
        :key="header"
      >
        <input
          v-model="checkedColumns"
          class="form-check-input"
          type="checkbox"
          :value="header"
          :id="header"
        />
        <label class="form-check-label" :id="header">
          {{ makeHeader(header).name }}
        </label>
      </div>
    </template>
  </b-modal>

  <b-modal
    id="change-columns-modal"
    v-model="filtersModalShow"
    title="Change filters"
    @ok="$emit('changeFilters', filters)"
  >
    <FormGroupList
      v-model="filters"
      name="filter"
      title="filters"
      :options="filterOptions"
    />
  </b-modal>

  <MusicModal
    v-if="track"
    v-model:show="musicModalShow"
    :track="track"
    :lastFmTrack="songInfo.lastFM.track"
    :highlevelFeatures="highlevelFeatures"
  />

  <b-table-simple hover striped responsive caption-top>
    <caption>
      {{
        props.caption
      }}

      <template v-if="expandable">
        <link
          href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css"
          rel="stylesheet"
        />

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
        <b-th v-if="overview" :style="colItemStyle"></b-th>
        <b-th
          v-for="(header, index) in headers"
          :key="header"
          class="text-center"
          :colspan="header.subheaders ? header.subheaders.length : 1"
          :style="{ ...colItemStyle, cursor: 'pointer' }"
          @click="setsorting(index)"
        >
          {{ header.name }}
        </b-th>
        <b-th v-if="overview"></b-th>
      </b-tr>
      <b-tr>
        <b-th v-if="overview" :style="colItemStyle"></b-th>
        <b-th
          v-for="subheader in subheaders"
          :key="subheader"
          class="text-center"
          :style="colItemStyle"
        >
          {{ subheader }}
        </b-th>
        <b-th v-if="overview"></b-th>
      </b-tr>
    </b-thead>
    <b-tbody>
      <b-tr v-for="(item, index) in sorted" :key="item"
        ><b-td class="align-middle" v-if="overview" :style="colItemStyle">
          <b-button
            variant="outline-primary fw-bold"
            @click="$emit('viewResult', item.id)"
            >View result</b-button
          >
        </b-td>
        <b-td
          v-for="[key, value] in Object.entries(item)"
          :key="`${descending}_${sortindex}_${index}-${key}`"
          class="text-center"
          :style="colItemStyle"
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
          <template v-else>
            <template v-if="key == 'track_spotify-uri'">
              <template v-if="value">
                <b-button @click="showMusicDetail(item['track_spotify-uri'])"
                  >View track</b-button
                >
              </template>
            </template>
            <template v-else>{{ value }} </template></template
          >
        </b-td>
        <b-td
          class="align-middle"
          v-if="overview || removable"
          :style="colItemStyle"
        >
          <b-row class="m-0 float-end">
            <b-col md="auto" class="mx-0 px-0">
              <b-button
                v-if="editable"
                variant="primary"
                class="mx-1"
                @click="
                  ;(editModalShow = !editModalShow),
                    (selectedEntry = index),
                    getNameTagsMail(item.id)
                "
                data-testid="edit"
                ><i class="bi bi-pencil-square"></i
              ></b-button>
            </b-col>
            <b-col md="auto" class="mx-0 px-0">
              <b-button
                variant="primary"
                class="mx-1"
                @click=";(viewModalShow = !viewModalShow), getMetadata(item.id)"
                data-testid="view-meta"
                ><i class="bi bi-info-circle"></i
              ></b-button>
            </b-col>
            <b-col md="auto" class="mx-0 px-0">
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
                @click="setEntryRemoval(item)"
                data-testid="delete"
              >
                <i :class="'bi ' + getCancelIcon(item)"></i>
              </b-button>
            </b-col>
          </b-row>
        </b-td>
        <b-td class="align-middle" v-if="overview" :style="colItemStyle">
          <SettingsModal :resultId="item.id" />
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
