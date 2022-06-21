<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */
import { computed, onMounted, ref } from 'vue'
import sortBy from 'just-sort-by'
import FormGroupList from './Form/FormGroupList.vue'
import { emptyFormGroup } from '../helpers/optionsFormatter'
import { statusPrefix, statusVariant, status } from '../helpers/queueFormatter'
import SettingsModal from './Table/Modals/SettingsModal.vue'
import MusicItem from './ItemDetail/MusicItem.vue'
import AudioSnippet from './ItemDetail/AudioSnippet.vue'
import InfoModal from './Table/Modals/InfoModal.vue'
import DeletionModal from './Table/Modals/DeletionModal.vue'
import EditModal from './Table/Modals/EditModal.vue'
import HeadersModal from './Table/Modals/HeadersModal.vue'

const emit = defineEmits([
  'viewResult',
  'loadResults',
  'loadMore',
  'paginationSort',
  'changeFilters',
  'updateHeaders',
])
const props = defineProps({
  viewItem: Boolean,
  recs: Boolean,
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
  filters: Object,
  filterOptions: Array,
  defaultSort: Number,
  startIndex: Number,
})

// Column width
const colWidth = 6

// Pagination
const entryAmount = ref(10)

// Modals
const filtersModalShow = ref(false)

// Filters
const filters = ref(emptyFormGroup(false))

// Sorting
const sortindex = ref()
const descending = ref()
const sortIcon = ref({ true: ' ▲', false: ' ▼' })

// Item detail
const infoHeaders = ref([])
const itemsInfo = ref([])
const additionalInfoAmount = ref(0)

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
  if (!props.pagination) return sort(sortindex.value)
  else return props.results
})

onMounted(() => {
  // Sort on default column if it is given
  // If no column is given, the table is not sortable
  if (props.defaultSort) {
    sortindex.value = props.defaultSort
    descending.value = true // For now sort by descending on default, TODO refactor
  }
  if (
    props.headers
      .map((header) => header.name)
      .some((name) => name.includes('spotify-uri'))
  ) {
    toggleInfoColumns(['Album', 'Snippet'])
  }
})

function colItemStyle(colWidth) {
  const width = colWidth + 'em'
  return {
    minWidth: width,
    width,
    maxWidth: width,
    inlineSize: width,
    overflowWrap: 'break-word',
  }
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
  } else {
    sortindex.value = i
  }
  emit('paginationSort', i)
}

/**
 * Checks whether a given string is a key.
 * @param {String}	key	- the string that needs to be checked
 * @return	{Bool} boolean stating whether the string is a key.
 */
function isItemKey(key) {
  const lowerKey = key.toLowerCase()
  const itemKeys = ['item']
  return itemKeys.includes(lowerKey) || lowerKey.includes('id')
}

// Hide item (ID) columns and show info columns
function toggleInfoColumns(addHeaders) {
  infoHeaders.value = [
    ...props.headers.filter((header) => !isItemKey(header.name)),
    ...addHeaders.map((header) => ({ name: header })),
  ]
  additionalInfoAmount.value = addHeaders.length
}

function isRecsHeader(key) {
  return (
    key &&
    filteredHeaders()
      .map((header) => header.name.toLowerCase())
      .includes(key.split('_').join(' '))
  )
}

const filteredHeaders = () => {
  return !props.recs || infoHeaders.value.length === 0
    ? props.headers
    : [...props.headers, ...[{ name: 'Album' }, { name: 'Snippet' }]]
}
</script>

<template>
  <div>
    <!-- Filters Modal -->
    <b-modal
      id="change-columns-modal"
      v-model="filtersModalShow"
      title="Change filters"
      @ok="$emit('changeFilters', filters)"
    >
      <FormGroupList
        v-model="filters"
        name="filter pass"
        title="subset"
        :options="filterOptions"
      />
    </b-modal>

    <!-- Table -->
    <b-table-simple hover striped responsive caption-top>
      <caption>
        {{
          props.caption
        }}

        <template v-if="expandable">
          <!-- Bootstrap icons -->
          <link
            href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css"
            rel="stylesheet"
          />

          <!-- Headers and filters modal buttons -->
          <div class="float-end">
            <HeadersModal
              :headerOptions="headerOptions"
              @updateHeaders="(e) => emit('updateHeaders', e)"
            />
            <b-button
              @click="filtersModalShow = !filterModalShow"
              class="m-1"
              data-testid="filterButton"
            >
              Filters
            </b-button>
          </div>
        </template>
      </caption>

      <!-- Headers -->
      <b-thead head-variant="dark">
        <!-- Main headers -->
        <b-tr>
          <template v-for="(header, index) in filteredHeaders()" :key="header">
            <b-th
              class="text-center"
              :colspan="header.subheaders ? header.subheaders.length : 1"
              :style="{ ...colItemStyle(colWidth), cursor: 'pointer' }"
              @click="setsorting(index)"
            >
              {{
                header.name + (index == sortindex ? sortIcon[descending] : '')
              }}
            </b-th>
          </template>
          <b-th v-if="overview" :style="colItemStyle(colWidth)"></b-th>
        </b-tr>
        <!-- Subheaders -->
        <b-tr v-if="!recs">
          <template v-for="subheader in subheaders" :key="subheader">
            <b-th class="text-center" :style="colItemStyle(colWidth)">
              {{ subheader }}
            </b-th>
          </template>
          <b-th v-if="overview" :style="colItemStyle(colWidth)"></b-th>
        </b-tr>
      </b-thead>

      <!-- Sorted table items -->
      <b-tbody>
        <b-tr v-for="(item, index) in sorted" :key="item">
          <!-- Table results content -->
          <template
            v-for="[key, value] in Object.entries(item)"
            :key="`${descending}_${sortindex}_${index}-${key}`"
          >
            <!-- For recs tables, show filtered columns -->
            <b-td
              v-if="!recs || isRecsHeader(key)"
              class="text-center"
              :style="colItemStyle"
            >
              <!--Special pill format for status-->
              <template
                v-if="
                  typeof value === 'string' && value.startsWith(statusPrefix)
                "
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
              <!-- Non-status columns -->
              <template v-else>
                <!-- Spotify column -->
                <template v-if="key === 'track_spotify-uri'">
                  <template v-if="value">
                    <MusicItem v-model="itemsInfo[index]" :uri="item[key]" />
                  </template>
                  <template v-else></template>
                </template>
                <!-- Regular column -->
                <template v-else-if="value && value.toString().startsWith('http')">
                  <b-link :href="value" target="_blank">{{ value}}</b-link>
                </template>
                <template v-else>
                  {{ value }}
                </template>
              </template>
            </b-td>
          </template>
          <!-- Additional item info -->
          <template v-if="recs">
            <template v-for="i in additionalInfoAmount" :key="i">
              <b-td
                v-if="itemsInfo[index]"
                class="text-center"
                :style="colItemStyle(colWidth * 3)"
              >
                <template
                  v-if="
                    itemsInfo[index][i - 1] &&
                    itemsInfo[index][i - 1].header.toLowerCase() === 'snippet'
                  "
                >
                  <AudioSnippet :trackId="itemsInfo[index][i - 1].value" />
                </template>
                <template v-else>
                  {{ itemsInfo[index][i - 1].value }}
                </template>
              </b-td>
              <b-td :style="colItemStyle(colWidth * 3)" v-else></b-td>
            </template>
          </template>
          <b-td
            class="align-middle"
            v-if="overview || removable"
            style="width: 150px"
          >
            <b-row class="m-0 float-end d-block">
              <b-button
                variant="primary"
                @click="$emit('viewResult', item.id)"
                class="m-1"
                style="width: 142px"
                v-if="!item.status || 
                  item.status.slice(statusPrefix.length) == status.done" :id="item.id"
              >
                {{ viewItem ? 'View result' : 'Open result' }}
              </b-button>
              <div class="p-0" style="width: 150px">
                <b-col md="auto" class="mx-0 px-0 d-inline">
                  <EditModal
                    v-if="editable"
                    :id="item.id"
                    :index="index"
                    :editUrl="serverFile2"
                    @loadResults="emit('loadResults')"
                  />
                </b-col>
                <b-col md="auto" class="mx-0 px-0 d-inline">
                  <InfoModal v-if="!item.status || 
                    item.status.slice(statusPrefix.length) == status.done" :id="item.id" />
                </b-col>

                <b-col md="auto" class="mx-0 px-0 d-inline">
                  <DeletionModal
                    v-if="
                      removable &&
                      (!item.status ||
                        [status.toDo, status.active].includes(
                          item.status.slice(statusPrefix.length)
                        ))
                    "
                    :item="item"
                    :removalUrl="serverFile"
                  />
                </b-col>
              </div>
            </b-row>
          </b-td>

          <b-td
            class="align-middle"
            v-if="overview"
            :style="colItemStyle(colWidth)"
          >
            <SettingsModal :resultId="item.id" />
          </b-td>
        </b-tr>
      </b-tbody>
    </b-table-simple>

    <!-- Pagination -->
    <div v-if="pagination">
      <b-button
        @click="$emit('loadMore', false, entryAmount)"
        variant="outline-primary"
        :disabled="entryAmount < 1 || entryAmount > props.startIndex"
      >
        Show previous {{ entryAmount }} items
      </b-button>
      Showing entries {{ props.startIndex + 1 }} -
      {{ props.startIndex + props.results.length }}
      <b-button
        @click="$emit('loadMore', true, entryAmount)"
        variant="outline-primary"
        :disabled="entryAmount < 1"
      >
        Show next {{ entryAmount }} items
      </b-button>
      <b-form-input
        v-model="entryAmount"
        :state="entryAmount >= 1"
        type="number"
        v-on:keyup.enter="$emit('loadMore', null, entryAmount)"
        v-on:focusout="$emit('loadMore', null, entryAmount)"
        >20</b-form-input
      >
    </div>
  </div>
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
