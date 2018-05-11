import chat from '../components/chat.vue'
import temp from '../components/temp.vue'
import tank from '../components/tank.vue'
export default [
    {path: '/chat', component: chat,name:'chat',},
    {path: '/login', component: temp,name:'login',},
    {path: '/tank', component: tank,name:'tank',},
]
