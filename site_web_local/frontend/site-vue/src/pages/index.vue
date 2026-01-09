<script setup>
import NavBar from '../components/navbar.vue'
import HeroSection from '../components/heroSection.vue'
import ProductGrid from '../components/ProductGrid.vue'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { listBrands } from '@/api/brand'

const router = useRouter()

const items = ref([])
const loading = ref(true)
const error = ref(null)

const goSearch = () => {
  router.push({ name: 'recherche' })
}

onMounted(async () => {
  try {
    loading.value = true
    error.value = null
    
    // Charger les marques depuis l'API/DB
    const brands = await listBrands()
    
    if (!brands || brands.length === 0) {
      throw new Error('Aucune marque trouvée dans la base de données')
    }
    
    // Transformer les marques pour ProductGrid avec toutes les infos
    items.value = brands.slice(0, 12).map(brand => ({
      id: brand.id || brand._id,
      src: brand.logo || null,
      logo: brand.logo || null,
      alt: brand.brand_name || 'Marque',
      brand_name: brand.brand_name || 'Marque inconnue',
      final_score: brand.final_score !== undefined ? brand.final_score : null,
      score: brand.final_score,
      score_label: brand.score_label || '',
      score_color: brand.score_color || 'yellow'
    }))
    
    console.log(`✅ ${items.value.length} marques chargées depuis la DB`)
  } catch (err) {
    console.error('Erreur lors du chargement des marques:', err)
    error.value = 'Impossible de charger les marques depuis la base de données. Vérifiez que le backend est accessible.'
    // Fallback avec des images par défaut
    items.value = [
      { id: 1, src: '/src/assets/product1.png', logo: null, alt: 'Baskets', brand_name: 'Marque exemple' },
      { id: 2, src: '/src/assets/product2.png', logo: null, alt: 'T-shirt', brand_name: 'Marque exemple' },
      { id: 3, src: '/src/assets/product3.png', logo: null, alt: 'Veste', brand_name: 'Marque exemple' },
      { id: 4, src: '/src/assets/product4.png', logo: null, alt: 'Sac', brand_name: 'Marque exemple' },
    ]
  } finally {
    loading.value = false
  }
})

</script>

<template>
  <NavBar />
  <HeroSection />
  <div v-if="loading" class="loading-section">
    <p>Chargement des marques depuis la base de données...</p>
  </div>
  <div v-else-if="error" class="error-section">
    <p>{{ error }}</p>
  </div>
  <ProductGrid 
    v-else
    :items="items" 
    title="Marques durables" 
    :cols="4"
    :use-brand-card="true"
    :loading="loading"
    :error="error"
  />
</template>

<style >
:root{
  --page-bg:  #DBC9AF;
  --panel-bg: #F4E8D7;
  --green:    #009C22;
  --green-dark:#017740;
  --product-bg: #FFF5E6;
  --pink: #B70064;

}

html, body, #app { margin: 0; background: var(--page-bg); }

.loading-section,
.error-section {
  text-align: center;
  padding: 40px 20px;
  background: var(--product-bg, #FFF5E6);
  margin: 20px 0;
}

.loading-section p,
.error-section p {
  font-size: 18px;
  color: var(--green-dark, #017740);
  font-family: system-ui, sans-serif;
}

.error-section p {
  color: var(--pink, #B70064);
}

</style>