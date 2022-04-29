<script setup>
import { onMounted, ref } from 'vue'
import { API_URL } from '../api'
import { getSpotifyToken, getSongInfo } from '../helpers/songInfo'

const token = ref('test')
const tracks = ref([])
const track = ref({})

onMounted(async () => {
  token.value = await getSpotifyToken()
  tracks.value = await getSongInfo(token.value, 'orion', 'metallica')
  track.value = tracks.value.items[0]
})
</script>

<template>
  <h1>Music Detail</h1>
  {{ token.token_type + ': ' + token.access_token }}
  <b-card>
    <h3>Found tracks:</h3>
    <ul>
      <li v-for="(queryTrack, index) in tracks.items">{{ queryTrack.name }}</li>
    </ul>
  </b-card>

  <template v-if="track">
    <p>{{ track }}</p>
    <h1>Best track:</h1>
    <h3>track: {{ track.name }}</h3>
    <h3>id: {{ track.id }}</h3>
    <template v-if="track.album">
      <h3>album: {{ track.album.name }}</h3>
      <h3>images:</h3>
      <div v-for="(image, index) in track.album.images">
        <img :src="image.url" /></div
    ></template>
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
    <h3>preview url: {{ track.preview_url }}</h3>
  </template>
</template>
