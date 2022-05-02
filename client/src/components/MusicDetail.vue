<script setup>
import { onMounted, ref } from 'vue'
import { API_URL } from '../api'
import { getSpotifyToken, getSongInfo } from '../helpers/songInfo'

const token = ref('test')
const tracks = ref([])
const track = ref({})
const trackModalShow = ref(false)
const query = ref({ track: 'orion', artist: 'metallica' })

onMounted(async () => {
  token.value = await getSpotifyToken()
  getInfo()
})

// Get music detail info
async function getInfo() {
  tracks.value = await getSongInfo(
    token.value,
    query.value.track,
    query.value.artist
  )
  track.value = tracks.value.items[0]
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
        :style="{
          backgroundColor: 'black',
          color: 'black',
        }"
        v-if="track.artists"
        v-model="trackModalShow"
        :title="track.name + ' by ' + track.artists[0].name"
        size="lg"
      >
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
                <p>Attributes (graph of danceability etc): TODO</p>

                <p>..:</p>
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
              >Show full info</b-button
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
      </b-modal>
    </template>
  </b-container>
</template>

<style></style>
