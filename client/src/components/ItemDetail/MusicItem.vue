<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { onMounted, ref } from 'vue'
import MusicModal from './MusicModal.vue'
// import { getInfoFromSpotifyID, getSpotifyToken } from '../../helpers/songInfo'

const emit = defineEmits(['update:modelValue'], ['changeColumns'])
const props = defineProps({
  uri: String,
  // header: String, // Table column header
  track: Object,
})

//const track = ref()
const musicModalShow = ref(false)

/*
onMounted(() => {
  getTrackItemInfo(props.uri)
})*/

/**
 * Get music detail info for a table item
 * @param {String}  spotifyId - the spotifyID of the item you want music details for
 */

/*
async function getTrackItemInfo(spotifyId) {
  const token = await getSpotifyToken()
  track.value = await getInfoFromSpotifyID(token, spotifyId)
  // console.log('track', track.value)
  const info = [
    { header: 'Album', value: track.value.album.name },
    { header: 'Snippet', value: spotifyId },

  ]
  emit('update:modelValue', info)

}*/
</script>

<template>
  <div>
    <MusicModal v-if="track" v-model="musicModalShow" :track="track" />
    <b-button @click="musicModalShow = !musicModalShow"> View track </b-button>
  </div>
</template>
