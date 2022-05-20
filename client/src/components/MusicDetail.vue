<script setup>
import { onMounted, ref } from "vue";
import { API_URL } from "../api";
import { getSpotifyToken, getSongInfo } from "../helpers/songInfo";
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

const token = ref("test");
const tracks = ref([]);
const track = ref({});
const trackModalShow = ref(false);
const query = ref({ track: "orion", artist: "metallica" });
const songInfo = ref();
const chartInfo = ref({ labels: [], datasets: [] });

onMounted(async () => {
  token.value = await getSpotifyToken();
  getInfo();
});

// Get music detail info
async function getInfo() {
  songInfo.value = await getSongInfo(
    token.value,
    query.value.track,
    query.value.artist
  );

  tracks.value = await songInfo.value.Spotify;
  track.value = tracks.value.items[0];
  //get AcousticBrainz highlevel features using LastFM's mbid
  const highlevelFeatures = await songInfo.value.AcousticBrainz[
    songInfo.value.LastFM.track.mbid
  ][0]["highlevel"];

  await generateChart(await highlevelFeatures);
}

//Generate the data for the audiofeatures Bar-chart
async function generateChart(highlevelFeatures) {
  //available moods from AcousticBrainz
  const moods = [
    "acoustic",
    "aggressive",
    "electronic",
    "happy",
    "party",
    "relaxed",
    "sad",
  ];
  //also include danceability seperately
  const danceability = highlevelFeatures["danceability"]["all"]["danceable"];
  const data = [danceability];
  for (const mood of moods) {
    const tagname = "mood_" + mood;
    const feature = highlevelFeatures[tagname];
    console.log("value", feature);
    data.push(feature.all[mood]);
  }
  chartInfo.value.datasets[0] = {
    label: "Attributes",
    backgroundColor: "#000080",
    data: data,
  };
  chartInfo.value.labels = ["danceability"].concat(
    moods.map((mood) => mood + "-ness")
  );
}
</script>

<template>
  <b-container>
    <h1 class="text-center">Music Detail</h1>
    <b-row>
      <b-form @submit="getInfo">
        <b-row>
          <b-col>
            <b-form-group label="Track">
              <b-form-input
                v-model="query.track"
                placeholder="Enter track name"
              />
            </b-form-group>
          </b-col>
          <b-col>
            <b-form-group label="Artist">
              <b-form-input
                v-model="query.artist"
                placeholder="Enter artist name"
              />
            </b-form-group>
          </b-col>
          <b-col>
            <b-button type="submit" variant="primary">Submit</b-button>
          </b-col>
        </b-row>
      </b-form>
    </b-row>
    <b-card>
      <h3>Found tracks:</h3>
      <ul>
        <li v-for="(queryTrack, index) in tracks.items">
          {{ queryTrack.name }}
        </li>
      </ul>
    </b-card>

    <template v-if="track">
      <b-button
        style="width: 20vw; display: block"
        class="mx-auto"
        variant="primary"
        @click="trackModalShow = !trackModalShow"
        >Show track
      </b-button>
      <b-modal
        body-bg-variant="dark"
        header-bg-variant="dark"
        footer-bg-variant="dark"
        body-text-variant="info"
        header-text-variant="info"
        footer-text-variant="info"
        v-if="track.artists"
        v-model="trackModalShow"
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
                      <template v-for="(artist, index) in track.artists">{{
                        artist.name
                      }}</template>
                    </p>
                    <p>Album: {{ track.album.name }}</p>
                    <div  :style = "{backgroundColor : 'coral', opacity: 0.9}">
                                        <Bar :chartData="chartInfo" >
                    </Bar>
                    </div>


                    <div>
                      <p v-html="songInfo.LastFM.track.wiki.summary"></p>
                    </div>
                    <div>
                      <b>LastFM tags:</b>
                      <div v-for="item in songInfo.LastFM.track.toptags.tag">
                        <a :href="item.url">{{ item.name }}</a>
                      </div>
                    </div>
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
  </b-container>
</template>

<style scoped>
.wrap {
  position: relative;
}

.wrap:before {
  content: " ";
  display: block;
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  opacity: 0.3;
  filter: blur(1px);
  background-image: url("public/background.png");
  background-repeat: repeat;
  background-position: 50% 0;
  background-size: 100%;
}

.content {
  position: relative;
}
</style>
