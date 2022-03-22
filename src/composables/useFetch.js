// code adapted from https://vuejs.org/guide/reusability/composables.html

/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/
/*
Playground component: Shows off a couple Vue 3 + Bootstrap 5 features.
Check out https://vuejs.org/examples 
and https://getbootstrap.com/docs/5.0/getting-started/introduction/ for more
*/

import { ref, isRef, unref, watchEffect } from 'vue'

export function useFetch(url) {
  const data = ref(null)
  const error = ref(null)

  async function doFetch() {
    // reset state before fetching..
    data.value = null
    error.value = null

    // resolve the url value synchronously so it's tracked as a
    // dependency by watchEffect()
    const urlValue = unref(url)

    try {
      // unref() will return the ref value if it's a ref
      // otherwise the value will be returned as-is
      const res = await fetch(urlValue)
      data.value = await res.json()
    } catch (e) {
      error.value = e
    }
  }

  if (isRef(url)) {
    // setup reactive re-fetch if input URL is a ref
    watchEffect(doFetch)
  } else {
    // otherwise, just fetch once
    doFetch()
  }

  return { data, error, retry: doFetch }
}
