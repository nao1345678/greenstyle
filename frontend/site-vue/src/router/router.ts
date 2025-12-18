import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/index.vue'
import MarqueDetail from '../pages/marques/[id].vue'
import Favorites from '../components/favorites.vue'
const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/marques/:id', name: 'marque-detail', component: MarqueDetail, props: true },
  { path: '/favorites', name: 'favorites', component: Favorites },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})
