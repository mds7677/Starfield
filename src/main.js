import { createApp } from 'vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faBars, faChevronDown,faFileArrowDown,faDownload} from '@fortawesome/free-solid-svg-icons'
import App from './App.vue'
import './style.css'
library.add(faBars, faChevronDown,faFileArrowDown,faDownload)
const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')