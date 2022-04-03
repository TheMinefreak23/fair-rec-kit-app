/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import { createApp } from 'vue'
import BootstrapVue3 from 'bootstrap-vue-3'
// import the root component App from a single-file component.
import App from './App.vue'
import '../scss/custom.scss'

const app = createApp(App)
app.use(BootstrapVue3)
app.mount('#app')
