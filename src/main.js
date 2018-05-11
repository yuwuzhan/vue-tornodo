import Vue from 'vue';
import App from './App.vue';
import VueRouter from 'vue-router';
import iView from 'iview';
import axios from 'axios';
import router from './router/router';
import store from './store/'
import pas from './api/api'
import 'iview/dist/styles/iview.css';

Vue.use(VueRouter);
Vue.use(iView);
const loginService = axios.create({
  timeout: 60000,                  // 请求超时时间
  transformRequest: [function (data) {
    // Do whatever you want to transform the data
    let ret = ''
    for (let it in data) {
      ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
    }
    return ret
  }],
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
  },
  withCredentials: true
})
// request拦截器
loginService.interceptors.request.use(config => {
  if (store.state.gopToken) {
    config.headers['hcToken'] = store.state.hcToken
  }
  return config
}, error => {
  return Promise.reject(error)
})

Vue.prototype.$loginAjax = loginService
window.addEventListener("storage", function (e) {
  if (e.key === 'gopToken') {
    if (!e.newValue) {
      location.reload()
    }
  }
  if (e.key === 'username') {
    if (e.oldValue !== e.newValue) {
      location.reload()
    }
  }
});
router.beforeEach((to, from, next) => {
  console.log(from.name + '=====>', to.name)
  if (window.localStorage.hcToken) {
    /* 
    这个if判断本地有没有hcToken,如果vuex里没有,就把本地的hcToken赋
    给vuex里(store.state.hcToken在刷新页面时会丢失,只能从window.
    localStorage.hcToken取出重新赋值。)
    */
    if (!store.state.hcToken) {
      store.commit('changeHcToken', window.localStorage.hcToken)
    }
  }
  /* 
  如果不跳到登录页面并且有登录信息,请求token,判断登录是否过期,
  如果没有登录信息,关闭ws,
  */
  if (to.name !== 'login' && store.state.hcToken) {
    loginService(pas.token).then((res) => {
      /* 
      如果登录不过期,则继续执行,否则退到登录页
       */
      if (res.data.code === 200) {
        if (!store.state.ws || store.state.readyState === 3) {
          /* 
          登录未过期,ws未开启或者已关闭
           */
          store.commit('openWs')
        }
        if (to.name) {
          next()
        }
        else {
          next({
            name: 'chat'
          })
        }
      }
      else {
        next({ name: 'login' })
      }
    })
  }
  else {
    store.commit('closeWs')
    if (to.name !== 'login') {
      next({ name: 'login' })
    }
    else {
      next()
    }
  }
})
new Vue({
  el: '#app',
  store,
  router: router,
  render: h => h(App)
})
