import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/index.vue'
import MarqueList from '../pages/marques/[id].vue'
import MarqueDetail from '../pages/marque-detail.vue'
import Recherche from '../pages/recherche.vue'
import APropos from '../pages/a-propos.vue'
import Login from '../pages/login.vue'
import Favorites from '../components/favorites.vue'

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/recherche', name: 'recherche', component: Recherche },
  { path: '/marques', name: 'marques-list', component: MarqueList },
  { path: '/marques/:id', name: 'marque-detail', component: MarqueDetail, props: true },
  { path: '/marque/:id', name: 'marque-detail-alt', component: MarqueDetail, props: true },
  { path: '/a-propos', name: 'a-propos', component: APropos },
  { path: '/login', name: 'login', component: Login },
  { path: '/favorites', name: 'favorites', component: Favorites },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})
