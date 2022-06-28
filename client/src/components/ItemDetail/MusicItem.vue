<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { onMounted, ref } from 'vue'
import MusicModal from './MusicModal.vue'
import { getSpotifyTrack } from '../../helpers/songInfo'

defineEmits(['update:modelValue'], ['changeColumns'])
const props = defineProps({
  uri: String,
  // header: String, // Table column header
})

const track = ref()
const musicModalShow = ref(false)

onMounted(async () => {
  //getTrackItemInfo(props.uri)
  track.value = await getSpotifyTrack(props.uri)
  // console.log('track', track.value)
})
</script>

<template>
  <div>
    <MusicModal v-if="track" v-model="musicModalShow" :track="track" />
    <b-button @click="musicModalShow = !musicModalShow"> View track </b-button>
  </div>
</template>
