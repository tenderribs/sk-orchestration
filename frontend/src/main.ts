import './assets/tailwind.css'
import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './main.router'
import { createPinia } from 'pinia'
import './main.xsrf'


const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

app.mount('#app')
