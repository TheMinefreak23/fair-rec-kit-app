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

const emit = defineEmits(['update:show'])
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
  // Get more info using Spotify track and artist
  const track = props.track.name.split('(')[0].trim() // Get main name from track name
  const artist = props.track.artists[0].name // use first artist's name
  // console.log('track', track, 'artist', artist)

  const songInfo = await getSongInfo(track, artist)

  lastFmTrack.value = songInfo.LastFM.track

  if (songInfo.AcousticBrainz) {
    // get AcousticBrainz highlevel features using LastFM's mbid
    const highlevelFeatures = songInfo.AcousticBrainz[0]['highlevel']

    generateChart(highlevelFeatures)
  }
})

// Generate the data for the audiofeatures Bar-chart
async function generateChart(highlevelFeatures) {
  chartInfo.value = { labels: [], datasets: [] }
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
    backgroundColor: 'orange',
    data: data,
  }
  chartInfo.value.labels = ['danceability'].concat(
    moods.map((mood) => mood + '-ness')
  )
}
</script>

<template>
  <b-modal
    body-bg-variant="dark"
    header-bg-variant="dark"
    footer-bg-variant="dark"
    body-text-variant="info"
    header-text-variant="info"
    footer-text-variant="info"
    v-if="track.artists"
    v-model="modalShow"
    :title="track.name + ' by ' + track.artists[0].name"
    size="lg"
  >
    <div class="wrap">
      <div class="content">
        <b-container class="p-3">
          <b-card style="background-color: rgba(0, 0, 0, 0.6)">
            <b-row class="p-3">
              <h1>{{ track.name }}</h1>
              <h2>
                <!--TODO refactor into component with dynamic formatting-->
                Artist(s):
                <template v-for="artist in track.artists">{{
                  artist.name
                }}</template>
              </h2>
              <h4>Album: {{ track.album.name }}</h4>
            </b-row>

            <b-row class="p-3">
              <!-- Graph and description -->
              <b-col cols="6">
                <!-- Chart -->
                <b-card
                  v-if="chartInfo"
                  :style="{
                    backgroundColor: 'rgba(0, 0, 0, 0.9)',
                    opacity: 0.9,
                  }"
                >
                  <Bar :chartData="chartInfo"> </Bar>
                </b-card>
                <h4 v-else>(No chart available)</h4>
              </b-col>
              <b-col cols="6">
                <!--Using medium sized image-->
                <img :src="track.album.images[1].url" />
              </b-col>
            </b-row>
            <b-row v-if="lastFmTrack">
              <!-- Wiki summary -->
              <b-col>
                <b-card v-if="lastFmTrack.wiki" class="bg-dark">
                  <p v-html="lastFmTrack.wiki.summary"></p>
                </b-card>
                <h4 v-else>(No wiki available)</h4>
              </b-col>
              <!-- Tags -->
              <b-col>
                <b-card class="bg-dark">
                  <b>LastFM tags:</b>
                  <div v-for="item in lastFmTrack.toptags.tag" :key="item">
                    <a :href="item.url" class="text-info">{{ item.name }}</a>
                  </div>
                </b-card>
              </b-col>
            </b-row>
            <b-row class="p-3">
              <AudioSnippet :trackId="track.id" />
            </b-row>
          </b-card>
          <b-row class="p-3">
            <b-button v-b-toggle.collapse-1 variant="primary"
              >Show raw info</b-button
            >
            <b-collapse id="collapse-1">
              <h3>
                debug | id: {{ track.id }} | preview url:
                {{ track.preview_url }}
              </h3>
              <p v-for="[key, value] of Object.entries(track)" :key="key">
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

<style scoped>
.wrap {
  position: relative;
  background-color: black;
}

.wrap:before {
  content: ' ';
  display: block;
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  opacity: 0.3;
  filter: blur(1px);
  background-image: url('public/background.png');
  background-repeat: repeat;
  background-position: 50% 0;
  background-size: 100%;
}

.content {
  position: relative;
}
</style>
