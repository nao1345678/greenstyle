import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/index.vue'
import MarqueDetail from '../pages/marques/[id].vue'
const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/marques/:id', name: 'marque-detail', component: MarqueDetail, props: true },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})
