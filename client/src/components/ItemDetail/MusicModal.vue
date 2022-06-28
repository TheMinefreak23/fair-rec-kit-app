<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { computed, onMounted, ref } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js'
import AudioSnippet from './AudioSnippet.vue'
import { getSongInfo } from '../../helpers/songInfo'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const emit = defineEmits('update:modelValue')
const props = defineProps({
  track: Object,
  modelValue: Boolean,
})
const chartInfo = ref()
const lastFmTrack = ref()

const modalShow = computed({
  get() {
    return props.modelValue
  },
  set(localValue) {
    emit('update:modelValue', localValue)
  },
})

onMounted(async () => {
  // console.log('props track', props.track)
  // Get more info using Spotify track and artist
  const track = props.track.name.split('(')[0].trim() // Get main name from track name
  const artist = props.track.artists[0].name // use first artist's name
  // console.log('track', track, 'artist', artist)

  const songInfo = await getSongInfo(track, artist)

  lastFmTrack.value = songInfo.LastFM.track

  if (
    songInfo.AcousticBrainz &&
    Object.entries(songInfo.AcousticBrainz)[0][1][0]
  ) {
    // console.log(Object.entries(songInfo.AcousticBrainz)[0])
    const highlevelFeatures = Object.entries(songInfo.AcousticBrainz)[0][1][0][
      'highlevel'
    ]
    generateChart(highlevelFeatures)
  }
})

/**
 * Generate the data for the Audio Features Bar-chart
 * @param {Array}  highlevelFeatures    -Array with high-Level features from AcousticBrainz
 */
async function generateChart(highlevelFeatures) {
  chartInfo.value = { labels: [], datasets: [], options: { responsive: true } }
  // available moods from AcousticBrainz
  const moods = [
    'acoustic',
    'aggressive',
    'electronic',
    'happy',
    'party',
    'relaxed',
    'sad',
  ]
  // also include danceability seperately
  const danceability = highlevelFeatures.danceability.all.danceable
  const data = [danceability]
  for (const mood of moods) {
    const tagname = 'mood_' + mood
    const feature = highlevelFeatures[tagname]
    // console.log('value', feature)
    data.push(feature.all[mood])
  }
  chartInfo.value.datasets[0] = {
    label: 'Attributes',
    color: 'white',
    backgroundColor: '#017C8E',
    responsive: true,
    data: data,
  }
  chartInfo.value.labels = ['danceability'].concat(
    moods.map((mood) => mood + '-ness')
  )
}
</script>

<template>
  <b-modal
    body-bg-variant="white"
    body-padding="0"
    header-bg-variant="dark"
    footer-bg-variant="dark"
    body-text-variant="black"
    header-text-variant="white"
    footer-text-variant="black"
    v-if="track.artists"
    v-model="modalShow"
    :title="track.name + ' - ' + track.artists[0].name"
    size="lg"
    hide-footer
  >
    <div class="modal-body p-0">
      <div class="content bg-white p-0">
        <b-container class="p-0">
          <b-row class="p-3 align-middle rounded-3 mx-1 bg-secondary">
            <b-col cols="6" class="text-center">
              <!--Using medium sized image-->
              <img :src="track.album.images[1].url" style="width: 80%" />
            </b-col>
            <b-col>
              <h2>{{ track.name }}</h2>
              <h4 class="fst-italic">
                <!--TODO refactor into component with dynamic formatting-->
                <template v-for="(artist, index) in track.artists">{{
                  (index == 0 ? '' : ', ') + artist.name
                }}</template>
              </h4>
              <h4>Album: {{ track.album.name }}</h4>
              <AudioSnippet :trackId="track.id" class="mt-2" />
            </b-col>
          </b-row>

          <b-row v-if="lastFmTrack" class="mt-2 mx-1">
            <!-- Tags -->
            <b-col class="p-0">
              <b-card class="bg-secondary border-0">
                <b>LastFM tags:</b>
                <b-badge
                  variant="dark"
                  v-for="item in lastFmTrack.toptags.tag"
                  :key="item"
                  class="d-inline ms-2 p-2"
                >
                  <a
                    :href="item.url"
                    class="text-white"
                    style="font-size: 14px"
                    >{{ item.name }}</a
                  >
                </b-badge>
              </b-card>
            </b-col>
          </b-row>

          <b-row v-if="lastFmTrack" class="mt-2 mx-1">
            <!-- Wiki summary -->
            <b-col class="p-0 rounded-end-0">
              <b-card v-if="lastFmTrack.wiki" class="bg-secondary border-0">
                <p v-html="lastFmTrack.wiki.summary"></p>
              </b-card>
              <b-card v-else class="bg-secondary border-0">
                <i>No wiki available</i>
              </b-card>
            </b-col>
          </b-row>

          <b-row class="mt-2 mx-1 bg-secondary">
            <!-- Graph and description -->
            <b-col class="p-0 bg-secondary">
              <!-- Chart -->
              <b-card v-if="chartInfo" class="bg-secondary border-0">
                <div>
                  <Bar :chartData="chartInfo"> </Bar>
                </div>
              </b-card>
              <b-card v-else class="bg-secondary border-0">
                <i>No chart available</i>
              </b-card>
            </b-col>
          </b-row>
          <b-row class="py-2 mx-1">
            <b-button v-b-toggle.collapse-1 variant="primary"
              >Toggle show raw info</b-button
            >
            <b-collapse id="collapse-1">
              <h6 class="mt-1">
                debug | id: <i>{{ track.id }}</i
                ><br />
                preview url:
                <a :href="track.preview_url">{{ track.preview_url }}</a>
              </h6>
              <p
                class="m-0"
                v-for="[key, value] of Object.entries(track)"
                :key="key"
              >
                <b>{{ key }}</b
                >: {{ value }}
              </p>
            </b-collapse>
          </b-row>
        </b-container>
      </div>
    </div>
  </b-modal>
</template>
