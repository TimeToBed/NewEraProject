import vueEmitter from 'core/emitter'
import { createApp, h } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import App from './App.vue'
import AppComponents from './components'
import VueSweetAlert2 from 'vue-sweetalert2'
import axios from 'axios' // 引入axios

import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import 'sweetalert2/dist/sweetalert2.min.css'

import './index.css'
import router from './router'

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/'
})

// create new app instance
const createNewApp = () => {
  const app = createApp({
    render: () => h(App),
  })
  library.add(fas, fab)

  app.config.globalProperties.axios = axios
  app.component('font-awesome-icon', FontAwesomeIcon)
  app.provide('eventHub', vueEmitter)
  app.use(router)
  app.use(ElementPlus)
  app.use(AppComponents)
  app.use(createPinia())
  app.use(VueSweetAlert2)
  app.provide('axios', axiosInstance) // 将 axiosInstance 注入到全局
  
  app.mount('#app')
  app.config.performance = true
}

const initApp = async () => {
  createNewApp()
}

initApp().then(() => {
  // initialized
})
