<script setup>
/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

defineProps({ trackId: String })
</script>

<template>
  <div>
    <iframe
      style="border-radius: 12px"
      :src="
        'https://open.spotify.com/embed/track/' +
        trackId +
        '?utm_source=generator'
      "
      width="100%"
      height="80"
      frameBorder="0"
      allowfullscreen=""
      allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
    />
  </div>
</template>
