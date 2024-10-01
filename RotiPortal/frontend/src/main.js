import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import 'v-calendar/dist/style.css'

const app = createApp(App)
app.use(router)
app.mount('#app')
