<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { onMounted, ref } from 'vue'
import MusicModal from './MusicModal.vue'
import { getInfoFromSpotifyID, getSpotifyToken } from '../../helpers/songInfo'

const emit = defineEmits(['update:modelValue'], ['changeColumns'])
const props = defineProps({
  uri: String,
  //header: String, // Table column header
})

const track = ref()
const highlevelFeatures = ref()
const songInfo = ref({ lastFM: {} }) // TODO
const musicModalShow = ref(false)

onMounted(() => {
  loadMusicDetail(props.uri)
})

// Get music detail info
// TODO refactor
async function loadMusicDetail(spotifyId) {
  const token = await getSpotifyToken()
  track.value = await getInfoFromSpotifyID(token, spotifyId)
  //console.log('track', track.value)
  const info = [
    { header: 'Album', value: track.value.album.name },
    { header: 'Snippet', value: spotifyId },
    //track.value.name,
    //track.value.artists.map((artist) => artist.name).join(', '),
  ]
  emit('update:modelValue', info)
  //emit('changeColumns', ['Track', 'Album', 'Artist'])
  emit(
    'changeColumns',
    info.map((item) => item.header)
  )

  // TODO
  /*
  //get AcousticBrainz highlevel features using LastFM's mbid
  highlevelFeatures.value = await songInfo.value.AcousticBrainz[
    songInfo.value.LastFM.track.mbid
  ][0]['highlevel']*/
}
</script>

<template>
  <MusicModal
    v-if="track"
    v-model:show="musicModalShow"
    :track="track"
    :lastFmTrack="songInfo.lastFM.track"
    :highlevelFeatures="highlevelFeatures"
  />
  <b-button @click="musicModalShow = !musicModalShow"> View track </b-button>
</template>
