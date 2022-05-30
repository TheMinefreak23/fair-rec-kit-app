<script setup>
/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

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

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

const emit = defineEmits(['update:show'])
const props = defineProps({
  track: Object,
  lastFmTrack: Object,
  highlevelFeatures: Object,
  show: Boolean,
})
const chartInfo = ref()

const modalShow = computed({
  get() {
    return props.show
  },
  set(localValue) {
    emit('update:show', localValue)
  },
})

onMounted(() => {
  if (props.highlevelFeatures) generateChart(props.highlevelFeatures)
})

//Generate the data for the audiofeatures Bar-chart
async function generateChart(highlevelFeatures) {
  chartInfo.value = { labels: [], datasets: [] }
  //available moods from AcousticBrainz
  const moods = [
    'acoustic',
    'aggressive',
    'electronic',
    'happy',
    'party',
    'relaxed',
    'sad',
  ]
  //also include danceability seperately
  const danceability = highlevelFeatures['danceability']['all']['danceable']
  const data = [danceability]
  for (const mood of moods) {
    const tagname = 'mood_' + mood
    const feature = highlevelFeatures[tagname]
    //console.log('value', feature)
    data.push(feature.all[mood])
  }
  chartInfo.value.datasets[0] = {
    label: 'Attributes',
    backgroundColor: '#000080',
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
          <b-row v-if="track.album">
            <b-row class="p-3">
              <b-col>
                <p>
                  <!--TODO refactor into component with dynamic formatting-->
                  Artist(s):
                  <template v-for="artist in track.artists">{{
                    artist.name
                  }}</template>
                </p>
                <p>Album: {{ track.album.name }}</p>
                <div
                  v-if="chartInfo"
                  :style="{ backgroundColor: 'coral', opacity: 0.9 }"
                >
                  <Bar :chartData="chartInfo"> </Bar>
                </div>

                <template v-if="lastFmTrack">
                  <div>
                    <p v-html="lastFmTrack.wiki.summary"></p>
                  </div>
                  <div>
                    <b>LastFM tags:</b>
                    <div v-for="item in lastFmTrack.toptags.tag">
                      <a :href="item.url">{{ item.name }}</a>
                    </div>
                  </div>
                </template>
              </b-col>
              <b-col>
                <!--Using medium sized image-->
                <img :src="track.album.images[1].url" />
              </b-col>
            </b-row>
          </b-row>
          <b-row class="p-3">
            <iframe
              style="border-radius: 12px"
              :src="
                'https://open.spotify.com/embed/track/' +
                track.id +
                '?utm_source=generator'
              "
              width="100%"
              height="80"
              frameBorder="0"
              allowfullscreen=""
              allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
            />
          </b-row>
          <b-row class="p-3">
            <b-button v-b-toggle.collapse-1 variant="primary"
              >Show raw info</b-button
            >
            <b-collapse id="collapse-1">
              <h3>
                debug | id: {{ track.id }} | preview url:
                {{ track.preview_url }}
              </h3>
              <p v-for="[key, value] of Object.entries(track)">
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
