<script setup>
//import NavBar from "../components/navbar.vue";
import HeroSection from "../components/heroSection.vue";
import ProductGrid from "../components/ProductGrid.vue";
//import AProposDeNous from "../components/AProposDeNous.vue";
import { onMounted, ref } from "vue";
import { listUsers } from "@/api/users";

const items = [
  { id: 1, src: "/src/assets/product1.png", alt: "…" },
  { id: 2, src: "/src/assets/product2.png", alt: "…" },
  { id: 3, src: "/src/assets/product3.png", alt: "…" },
  { id: 4, src: "/src/assets/product4.png", alt: "…" },
];
const goSearch = () => window.alert("TODO: router vers la page recherche");

const users = ref([]);
onMounted(async () => {
  users.value = await listUsers();
  console.log(users.value);
});
</script>

<template>
  <NavBar />
  <HeroSection />
  <ProductGrid :items="items" title="Catégories de marques" :cols="4" />
  <AProposDeNous />
</template>

<style>
:root {
  --page-bg: #dbc9af;
  --panel-bg: #f4e8d7;
  --green: #009c22;
  --green-dark: #017740;
  --product-bg: #fff5e6;
  --pink: #b70064;
}

html,
body,
#app {
  margin: 0;
  background: var(--page-bg);
}
</style>
