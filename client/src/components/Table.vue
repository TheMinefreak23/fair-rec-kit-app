<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */
import { computed, onMounted, ref } from 'vue'
import sortBy from 'just-sort-by'
// import { HEADERS_ORDER } from '../helpers/resultFormatter'
import { statusPrefix, statusVariant, status } from '../helpers/queueFormatter'
import SettingsModal from './Table/Modals/SettingsModal.vue'
import MusicItem from './ItemDetail/MusicItem.vue'
import AudioSnippet from './ItemDetail/AudioSnippet.vue'
import InfoModal from './Table/Modals/InfoModal.vue'
import DeletionModal from './Table/Modals/DeletionModal.vue'
import EditModal from './Table/Modals/EditModal.vue'

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
  pagination: Boolean,
  recs: Boolean,
  comparing: Boolean,
  results: Array,
  headers: Array,
  removeText: String,
  removable: Boolean,
  editable: Boolean,
  viewItem: Boolean,
  serverFile: String,
  serverFile2: String,
  caption: String,
  defaultSort: Number,
  startIndex: Number,
})

// Column width
const colWidth = 6

// Pagination
const entryAmount = ref(10)

// Sorting
const sortindex = ref()
const descending = ref()
const sortIcon = ref({ true: ' ▲', false: ' ▼' })

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
  if (props.comparing) entryAmount.value = 5
  // Sort on default column if it is given
  // If no column is given, the table is not sortable
  if (props.defaultSort) {
    sortindex.value = props.defaultSort
    descending.value = true // For now sort by descending on default, TODO refactor
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
</script>

<template>
  <div>
    <!-- Table -->
    <b-table-simple hover striped responsive caption-top id="customScrollbar">
      <caption>
        {{
          props.caption
        }}
        <div v-if="recs">
          <slot></slot>
        </div>
      </caption>

      <!-- Headers -->
      <b-thead head-variant="dark">
        <!-- Main headers -->
        <b-tr>
          <template v-for="(header, index) in headers" :key="header">
            <b-th
              class="text-center"
              :colspan="header.subheaders ? header.subheaders.length : 1"
              :style="{ ...colItemStyle(colWidth), cursor: 'pointer' }"
              @click="setsorting(index)"
            >
              {{
                header.name +
                (sortindex && index == sortindex ? sortIcon[descending] : '')
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
            <!-- Audio snippet column -->
            <b-td
              v-if="key === 'audio_snippet'"
              class="text-center"
              style="width: 400px"
            >
              <template v-if="value">
                <AudioSnippet :trackId="value"
              /></template>
              <template v-else></template>
            </b-td>
            <b-td v-else class="text-center" :style="colItemStyle">
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
                <template v-if="value">
                  <!-- Spotify column -->
                  <template v-if="key === 'track_spotify-uri'">
                    <MusicItem :uri="item[key]" />
                  </template>
                  <!-- Regular column -->
                  <template v-else-if="value.toString().startsWith('http')">
                    <b-link :href="value" target="_blank">{{ value }}</b-link>
                  </template>
                  <template v-else>
                    {{ value }}
                  </template>
                </template>
                <template v-else></template>
              </template>
            </b-td>
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
                v-if="
                  !item.status ||
                  item.status.slice(statusPrefix.length) == status.done
                "
                :id="item.id"
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
                  <InfoModal
                    v-if="
                      !item.status ||
                      item.status.slice(statusPrefix.length) == status.done
                    "
                    :id="item.id"
                  />
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
      />
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
