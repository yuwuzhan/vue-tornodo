import Vue from 'vue'
import Vuex from 'vuex'
import apiUrl from '../util/baseUrls'
Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        ws: '',
        gopToken: '',
        hcToken: ''
    },
    mutations: {
        changeGopToken(state, newToken) {
            state.gopToken = newToken
            window.localStorage.gopToken = newToken
        },
        changeHcToken(state, newToken) {
            state.hcToken = newToken
            window.localStorage.hcToken = newToken
        },
        closeWs(state) {
            if (state.ws) {
                state.ws.close()
                window.localStorage.removeItem('gopToken')
                window.localStorage.removeItem('hcToken')
                state.ws = ''
            }
        },
        openWs(state) {
            state.ws = new WebSocket(apiUrl.ws)
            state.ws.onopen = () => {  // 连接建立好后的回调
                state.ws.send(state.hcToken);  // 向建立的连接发送消息
            }
            state.ws.onmessage = (evt) => {  // 收到服务器发送的消息后执行的回调
                this.commit('changeGopToken', evt.data)
            }
            state.ws.onerror = (ev) => {
            }
            state.ws.onclose = (ev) => {
                window.localStorage.removeItem('gopToken')
                window.localStorage.removeItem('hcToken')
            }
        },
    },
})