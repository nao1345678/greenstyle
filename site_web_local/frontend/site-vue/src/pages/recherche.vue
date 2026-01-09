<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import SearchBar from '../components/SearchBar.vue'
import ProductCard from '../components/ProductCard.vue'
import { listBrands, getBrandByName } from '../api/brand'

const router = useRouter()
const route = useRoute()

const query = ref(route.query.q || '')
const results = ref([])
const loading = ref(false)
const error = ref(null)

const performSearch = async () => {
  if (!query.value.trim()) {
    results.value = []
    return
  }

  loading.value = true
  error.value = null

  try {
    // Mise à jour de l'URL avec la requête
    router.push({ query: { q: query.value } })

    // Recherche de marques via l'API
    const allBrands = await listBrands()
    const searchTerm = query.value.toLowerCase().trim()
    const filteredBrands = allBrands.filter(brand => 
      brand.brand_name?.toLowerCase().includes(searchTerm)
    )
    
    results.value = filteredBrands.map(brand => ({
      id: brand.id || brand._id,
      src: brand.logo || '/src/assets/product1.png',
      alt: brand.brand_name || '',
      brand: brand
    }))
  } catch (err) {
    console.error('Erreur lors de la recherche:', err)
    error.value = 'Erreur lors de la recherche. Veuillez réessayer.'
    results.value = []
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  performSearch()
}

onMounted(() => {
  // Si une requête est présente dans l'URL, effectuer la recherche
  if (query.value) {
    performSearch()
  }
})

// Écouter les changements dans l'URL
watch(() => route.query.q, (newQuery) => {
  query.value = newQuery || ''
  if (newQuery) {
    performSearch()
  }
})
</script>

<template>
  <div class="recherche-page">
    <div class="container">
      <h1 class="title">Rechercher une marque</h1>
      
      <div class="search-section">
        <SearchBar 
          v-model="query" 
          @search="handleSearch"
          placeholder="Rechercher une marque (ex: Veja, Patagonia...)"
        />
      </div>

      <div v-if="loading" class="loading">
        Recherche en cours...
      </div>

      <div v-if="error" class="error">
        {{ error }}
      </div>

      <div v-if="!loading && !error && results.length === 0 && query" class="no-results">
        Aucun résultat trouvé pour "{{ query }}"
      </div>

      <div v-if="!loading && !error && results.length > 0" class="results">
        <h2 class="results-title">{{ results.length }} résultat(s) trouvé(s)</h2>
        <div class="grid">
          <ProductCard
            v-for="item in results"
            :key="item.id"
            :src="item.src"
            :alt="item.alt"
            :to="{ name: 'marque-detail', params: { id: item.id } }"
          />
        </div>
      </div>

      <div v-if="!loading && !error && !query" class="empty-state">
        <p>Entrez le nom d'une marque pour commencer votre recherche</p>
      </div>
    </div>
  </div>
</template>


<style scoped>
.recherche-page {
  min-height: calc(100vh - 85px);
  background: var(--page-bg, #DBC9AF);
  padding: 40px 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.title {
  font-family: "Jersey 10", system-ui, sans-serif;
  font-size: 36px;
  color: var(--green-dark, #017740);
  margin-bottom: 32px;
  text-align: center;
}

.search-section {
  margin-bottom: 32px;
}

.loading, .error, .no-results, .empty-state {
  text-align: center;
  padding: 40px 20px;
  font-size: 18px;
  color: var(--green-dark, #017740);
}

.error {
  color: var(--pink, #B70064);
}

.results-title {
  font-family: "Jersey 10", system-ui, sans-serif;
  font-size: 24px;
  color: var(--pink, #B70064);
  margin-bottom: 24px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 24px;
}

@media (max-width: 768px) {
  .grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 16px;
  }
  
  .title {
    font-size: 28px;
  }
}

@media (max-width: 480px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .title {
    font-size: 24px;
  }
}
</style>

