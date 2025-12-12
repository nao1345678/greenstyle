<!-- src/pages/marques/[id].vue -->
<script setup lang="ts">
import { onMounted, ref } from "vue"
import { RouterLink } from "vue-router"

import NavBar from "../../components/navbar.vue"
import Intro from "../../components/intro.vue"
import ProductGrid from "../../components/ProductGrid.vue"

import { listBrands, type BrandOut } from "../../api/brand"

const title = ref("Marques")
const intro = ref(
  "Notre mission est de vous offrir un classement éthique des marques de vêtements…"
)

type GridItem = { id: string; src: string; alt: string }
const items = ref<GridItem[]>([])
const loading = ref(false)
const error = ref<string | null>(null)

onMounted(async () => {
  loading.value = true
  error.value = null
  try {
    const brands: BrandOut[] = await listBrands()
    items.value = brands.map(b => ({
      id: b.id,                                
      src: b.logo || "https://placehold.co/600x450?text=Logo",
      alt: b.brand_name,
    }))
  } catch (e: any) {
    error.value = e?.response?.data?.detail || e.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <NavBar />
  <div class="page-bg">
    <main class="wrap">

      <div class="intro">
        <Intro :title="title" :text="intro" />
      </div>

      <p v-if="loading" class="state">Chargement…</p>
      <p v-else-if="error" class="state err">{{ error }}</p>

      <div v-else class="grid-wrap">
        <ProductGrid :items="items" title="Toutes les marques" :cols="4" />
      </div>
    </main>
  </div>
</template>

<style scoped>
.page-bg{
  background: #fff5e6;
  min-height: 100svh;
  padding: 16px 0;
}
.wrap{ max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.back{ display:inline-block; margin: 6px 0 10px; text-decoration:none; color:#555; }
.intro{ max-width: 70vw; }
.state{ margin: 12px 0; }
.err{ color:#b00020; }
.grid-wrap{ margin-top: 12px; }
</style>
