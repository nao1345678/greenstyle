import { createRouter, createWebHistory } from "vue-router";
import Home from "../pages/index.vue";
import MarqueDetail from "../pages/marques/[id].vue";
import AProposDeNous from "../pages/AProposDeNous.vue";

const routes = [
  { path: "/", name: "home", component: Home },
  {
    path: "/marques/:id",
    name: "marque-detail",
    component: MarqueDetail,
    props: true,
  },
  {
    path: "/about",
    name: "about",
    component: AProposDeNous,
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
