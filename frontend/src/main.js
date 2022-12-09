import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import vuetify from '@/node_modules/vuetify'
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import '@mdi/font/css/materialdesignicons.css'
import './node_modules/vue.logger'
import './node_modules/vue.notifications'
import './node_modules/api.service'
import './auth.control'

import Default from '@/layouts/Default.vue'
import Centered from '@/layouts/Centered.vue'

Vue.component('default-layout', Default)
Vue.component('centered-layout', Centered)

Vue.config.productionTip = false
new Vue({
router,
store,
vuetify,
render: h => h(App)
}).$mount('#app')


