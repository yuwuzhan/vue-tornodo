import Vue from 'vue'
import VueRouter from 'vue-router'
import routerConfig from './config'


Vue.use(VueRouter);
const router = new VueRouter({
  mode: 'history',
  routes: routerConfig
})
export default router
